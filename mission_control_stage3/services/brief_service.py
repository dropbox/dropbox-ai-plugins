"""Generate the daily brief from live queue, stale review, loops, and approvals."""

from __future__ import annotations

from pathlib import Path

from .common import DATA, audit, load_global_rules, now_iso, read_csv


def generate_daily_brief(output_path: Path | None = None) -> str:
    rules = load_global_rules()
    max_approvals = int(rules.get("max_approvals_per_day", 7))
    loop_at = int(rules.get("loop_escalate_at", 3))

    live = read_csv(DATA / "live_decisions.csv")
    stale = read_csv(DATA / "stale_review.csv")
    loops = read_csv(DATA / "loop_alerts.csv")
    approvals = read_csv(DATA / "approvals.csv")
    pending = [r for r in approvals if r.get("status") == "pending"]
    needs = [r for r in live if r.get("status") == "Needs Approval"]

    # Top 3 by urgency then id.
    urgency_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    top = sorted(
        live,
        key=lambda r: (urgency_rank.get((r.get("urgency") or "medium").lower(), 9), r.get("id", "")),
    )[:3]

    generated = now_iso()
    lines = [
        "Mission Control — Daily Brief (Stage 3)",
        f"Generated: {generated}",
        "",
        "Source of truth: data/decisions.csv",
        "Chat is coordination only.",
        "No send / pay / delete / share / file / government filing without approval.",
        "Only the lead office tells the user.",
        "",
        f"Top 3 live items",
    ]
    if not top:
        lines.append("- (none)")
    for row in top:
        lines.append(
            f"- [{row['id']}] {row['title']} | {row.get('status')} | "
            f"urgency={row.get('urgency', '')} | lead={row.get('lead_office')}"
        )

    lines.extend(
        [
            "",
            f"Live queue ({len(live)}) — Active / Waiting / Needs Approval",
            f"Needs Approval: {len(needs)} | Pending approval rows: {len(pending)} "
            f"(max {max_approvals}/day)",
        ]
    )
    for row in live:
        missing = row.get("missing_fields") or ""
        missing_bit = f" | missing={missing}" if missing else ""
        lines.append(
            f"- [{row['id']}] {row['title']} | {row['status']} | "
            f"lead={row['lead_office']} support={row['support_office']}{missing_bit}"
        )

    lines.extend(["", f"Stale review ({len(stale)}) — archive or resolve"])
    if not stale:
        lines.append("- (none)")
    for row in stale:
        lines.append(
            f"- [{row['id']}] {row['title']} | loops={row.get('loop_count', '0')} | "
            f"lead={row.get('lead_office')}"
        )

    lines.extend(["", f"Loop alerts ({len(loops)}) — escalate at {loop_at}+"])
    if not loops:
        lines.append("- (none)")
    for row in loops:
        lines.append(f"- [{row['decision_id']}] {row['office']}: {row['reason']}")

    lines.extend(
        [
            "",
            "Reminders: data/reminder_log.csv (calendar + alarms).",
            "Approvals: data/approvals.csv (gate only — Stage 3 never executes risky actions).",
            "Audit: data/audit_log.csv",
        ]
    )

    text = "\n".join(lines) + "\n"
    path = output_path or (DATA.parent / "daily_brief.txt")
    path.write_text(text, encoding="utf-8")
    audit("brief_service", "generate_daily_brief", "", f"live={len(live)} stale={len(stale)}")
    return text
