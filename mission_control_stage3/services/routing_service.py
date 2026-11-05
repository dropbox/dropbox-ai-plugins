"""Route classified tasks to lead + support offices; rebuild live/stale queues."""

from __future__ import annotations

from datetime import date, timedelta

from .common import (
    DATA,
    DECISION_FIELDS,
    LOOP_FIELDS,
    REMINDER_FIELDS,
    audit,
    live_statuses,
    load_global_rules,
    now_iso,
    read_csv,
    write_csv,
)


def assign_offices(classification: dict) -> dict[str, str]:
    """One lead + one different support office. No lane crossing."""
    office = classification["office"]
    lead = office["name"]
    support = office.get("default_support") or "Mission Control"
    if support == lead:
        support = "Mail & Schedule" if lead != "Mail & Schedule" else "Mission Control"
    audit(
        "routing_service",
        "assign_offices",
        "",
        f"lead={lead} support={support}",
    )
    return {"lead_office": lead, "support_office": support}


def rebuild_queues() -> dict[str, int]:
    """Filter decisions into live_decisions.csv and stale_review.csv."""
    rules = load_global_rules()
    live_set = live_statuses()
    stale_status = rules.get("stale_status", "Stale")
    decisions = read_csv(DATA / "decisions.csv")

    live = [row for row in decisions if row.get("status") in live_set]
    stale = [row for row in decisions if row.get("status") == stale_status]

    write_csv(DATA / "live_decisions.csv", DECISION_FIELDS, live)
    write_csv(DATA / "stale_review.csv", DECISION_FIELDS, stale)
    audit(
        "routing_service",
        "rebuild_queues",
        "",
        f"live={len(live)} stale={len(stale)} total={len(decisions)}",
    )
    return {"live": len(live), "stale": len(stale), "total": len(decisions)}


def create_reminders_for_live() -> int:
    """Calendar + alarm reminder rows for live items with due dates."""
    live = read_csv(DATA / "live_decisions.csv")
    created = now_iso()
    rows: list[dict[str, str]] = []
    for item in live:
        due = (item.get("due_date") or "").strip()
        if not due:
            continue
        lead = item.get("lead_office") or "Mission Control"
        rows.append(
            {
                "decision_id": item["id"],
                "office": lead,
                "reminder_type": "due_date",
                "scheduled_for": f"{due}T09:00:00",
                "status": "scheduled",
                "created_at": created,
            }
        )
        try:
            due_d = date.fromisoformat(due)
            day_before = (due_d - timedelta(days=1)).isoformat()
            rows.append(
                {
                    "decision_id": item["id"],
                    "office": "Mail & Schedule",
                    "reminder_type": "alarm",
                    "scheduled_for": f"{day_before}T18:00:00",
                    "status": "scheduled",
                    "created_at": created,
                }
            )
        except ValueError:
            pass

    write_csv(DATA / "reminder_log.csv", REMINDER_FIELDS, rows)
    audit("routing_service", "create_reminders", "", f"count={len(rows)}")
    return len(rows)


def refresh_loop_alerts() -> int:
    """Escalate when loop_count >= threshold."""
    rules = load_global_rules()
    threshold = int(rules.get("loop_escalate_at", 3))
    decisions = read_csv(DATA / "decisions.csv")
    created = now_iso()
    alerts: list[dict[str, str]] = []
    for item in decisions:
        try:
            loops = int(item.get("loop_count") or "0")
        except ValueError:
            loops = 0
        if loops < threshold:
            continue
        alerts.append(
            {
                "decision_id": item["id"],
                "office": item.get("lead_office") or "Mission Control",
                "reason": f"loop_count {loops} >= {threshold}; escalate",
                "loop_count": str(loops),
                "created_at": created,
            }
        )
    write_csv(DATA / "loop_alerts.csv", LOOP_FIELDS, alerts)
    audit("routing_service", "loop_alerts", "", f"count={len(alerts)}")
    return len(alerts)
