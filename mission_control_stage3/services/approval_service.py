"""Approval gate for high-risk actions. Max N approvals per day."""

from __future__ import annotations

from typing import Any

from .common import (
    APPROVAL_FIELDS,
    DATA,
    DECISION_FIELDS,
    audit,
    load_global_rules,
    load_office_rules,
    now_iso,
    read_csv,
    write_csv,
)


def _today_prefix() -> str:
    return now_iso()[:10]


def approvals_used_today() -> int:
    rows = read_csv(DATA / "approvals.csv")
    today = _today_prefix()
    return sum(
        1
        for row in rows
        if row.get("status") == "approved"
        and (row.get("decided_at") or "").startswith(today)
    )


def _office_by_name(office_name: str) -> dict[str, Any]:
    offices = {o["name"]: o for o in load_office_rules()["offices"]}
    if office_name not in offices:
        raise ValueError(f"Unknown office: {office_name}")
    return offices[office_name]


def is_action_allowed(
    action: str,
    *,
    office: dict[str, Any],
    global_rules: dict[str, Any] | None = None,
    approved: bool = False,
) -> tuple[bool, str]:
    """
    Enforce office lane + approval gate.

    Returns (allowed, reason).
    - Global safe_without_approval does NOT grant every office Mission Control actions.
    - no_lane_crossing (default true) requires the action to be in the office's
      allowed_actions or forbidden_without_approval (in-lane but gated).
    - approved=True still cannot cross lanes.
    """
    rules = global_rules or load_global_rules()
    action_l = action.lower().strip()
    if not action_l:
        return False, "empty_action"

    high_risk = {a.lower() for a in rules.get("high_risk_actions", [])}
    safe = {a.lower() for a in rules.get("safe_without_approval", [])}
    no_lane_crossing = bool(rules.get("no_lane_crossing", True))

    office_allowed = {a.lower() for a in office.get("allowed_actions", [])}
    forbidden = {a.lower() for a in office.get("forbidden_without_approval", [])}
    in_lane = action_l in office_allowed or action_l in forbidden

    if no_lane_crossing and not in_lane:
        return False, "lane_crossing_blocked"

    if action_l in high_risk or action_l in forbidden:
        if approved:
            return True, "approved_high_risk"
        return False, "blocked_pending_approval"

    if action_l in office_allowed:
        return True, "allowed_office_action"

    if action_l in safe:
        # Only reachable when no_lane_crossing is false (in_lane already checked).
        return True, "allowed_safe_action"

    return False, "action_not_in_office_lane"


def request_approval(
    decision_id: str, action: str, office: str, notes: str = ""
) -> dict[str, str]:
    """Queue a high-risk action behind the approval gate (does not execute it)."""
    rules = load_global_rules()
    high_risk = {a.lower() for a in rules.get("high_risk_actions", [])}
    action_l = action.lower().strip()
    if action_l not in high_risk:
        raise ValueError(
            f"Action '{action}' is not high-risk; only high-risk actions use the gate."
        )

    office_cfg = _office_by_name(office)
    # Requesting approval is allowed for in-lane high-risk actions even while
    # unapproved — is_action_allowed would return blocked_pending_approval.
    allowed, reason = is_action_allowed(
        action_l, office=office_cfg, global_rules=rules, approved=False
    )
    if reason == "lane_crossing_blocked":
        raise PermissionError(
            f"Office '{office}' cannot request '{action_l}' (lane crossing blocked)."
        )
    if not allowed and reason not in {"blocked_pending_approval"}:
        raise PermissionError(
            f"Office '{office}' cannot request '{action_l}' ({reason})."
        )

    decisions = {row["id"]: row for row in read_csv(DATA / "decisions.csv")}
    if decision_id not in decisions:
        raise ValueError(f"Unknown decision_id: {decision_id}")

    approvals = read_csv(DATA / "approvals.csv")
    approval_id = f"A{len(approvals) + 1:03d}"
    row = {
        "approval_id": approval_id,
        "decision_id": decision_id,
        "action": action_l,
        "office": office,
        "status": "pending",
        "requested_at": now_iso(),
        "decided_at": "",
        "notes": notes or "Awaiting operator approval; action not executed",
    }
    approvals.append(row)
    write_csv(DATA / "approvals.csv", APPROVAL_FIELDS, approvals)

    # Mark decision Needs Approval.
    all_decisions = read_csv(DATA / "decisions.csv")
    for item in all_decisions:
        if item["id"] == decision_id:
            item["status"] = "Needs Approval"
            item["needs_approval"] = "yes"
            item["updated_at"] = now_iso()
            break
    write_csv(DATA / "decisions.csv", DECISION_FIELDS, all_decisions)

    audit(
        "approval_service",
        "request_approval",
        decision_id,
        f"{approval_id} action={action_l} office={office}",
    )
    return row


def decide_approval(approval_id: str, approve: bool, notes: str = "") -> dict[str, str]:
    """
    Record approve/deny. Never executes send/pay/delete/share/file.
    Enforces max approvals per day. Approved flag does not authorize lane crossing.
    """
    rules = load_global_rules()
    max_per_day = int(rules.get("max_approvals_per_day", 7))
    approvals = read_csv(DATA / "approvals.csv")
    target = None
    for row in approvals:
        if row.get("approval_id") == approval_id:
            target = row
            break
    if target is None:
        raise ValueError(f"Unknown approval_id: {approval_id}")
    if target.get("status") != "pending":
        raise ValueError(f"Approval {approval_id} already {target.get('status')}")

    if approve:
        office_cfg = _office_by_name(target.get("office") or "")
        allowed, reason = is_action_allowed(
            target.get("action") or "",
            office=office_cfg,
            global_rules=rules,
            approved=True,
        )
        if not allowed:
            raise PermissionError(
                f"Cannot approve {approval_id}: {reason} for office "
                f"'{target.get('office')}' action '{target.get('action')}'."
            )
        if approvals_used_today() >= max_per_day:
            raise ValueError(
                f"Max {max_per_day} approvals per day reached. Park or wait until tomorrow."
            )

    target["status"] = "approved" if approve else "denied"
    target["decided_at"] = now_iso()
    if notes:
        target["notes"] = notes
    else:
        target["notes"] = (
            "Approved — operator must still perform the action; Stage 3 does not send/pay/file."
            if approve
            else "Denied — action blocked."
        )
    write_csv(DATA / "approvals.csv", APPROVAL_FIELDS, approvals)
    audit(
        "approval_service",
        "decide_approval",
        target.get("decision_id", ""),
        f"{approval_id} -> {target['status']}",
    )
    return target
