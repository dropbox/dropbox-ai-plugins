#!/usr/bin/env python3
"""Mission Control Stage 2 — validate queue, generate live/stale/brief/reminder/loop outputs."""

from __future__ import annotations

import csv
from datetime import date, datetime, timedelta
from pathlib import Path

STAGE2 = Path(__file__).resolve().parent
BOTS = STAGE2 / "bots"

LIVE_STATUSES = {"Active", "Waiting", "Needs Approval"}
STALE_STATUS = "Stale"
MAX_APPROVALS_PER_DAY = 7
LOOP_ESCALATE_AT = 3

DECISION_FIELDS = [
    "id",
    "title",
    "status",
    "lead_office",
    "support_office",
    "needs_approval",
    "loop_count",
    "due_date",
    "notes",
]

OFFICE_FIELDS = ["office", "role", "lane", "may_contact_user", "notes"]

REMINDER_FIELDS = [
    "decision_id",
    "office",
    "reminder_type",
    "scheduled_for",
    "status",
    "created_at",
]

LOOP_FIELDS = [
    "decision_id",
    "office",
    "reason",
    "loop_count",
    "created_at",
]

RULES_TEXT = """Mission Control — Stage 2 Rules
================================

Source of truth = decisions list (decisions.csv) and the live queue (live_decisions.csv).
Chat is coordination only — not the official record.

Live items
----------
Only Active, Waiting, and Needs Approval items reach the user.
Those rows appear in live_decisions.csv.

Stale items
-----------
Stale items are archived or reactivated.
Stale rows appear in stale_review.csv.
Old items must be reviewed and closed or archived.

Approvals and actions
---------------------
No office may send, pay, delete, share, or file without approval.
Max 7 approvals per day.
Drafts are not filings.
Stage 2 may read, validate, route, summarize, alert, queue, and remind.
Stage 2 may not send final messages, pay bills, delete files, share files, or file anything without approval.

Offices and lanes
-----------------
One lead office and one support office per item.
Only the lead office tells the user.
No office crosses its lane.

Escalation and reminders
------------------------
If an issue loops 3 times, escalate (see loop_alerts.csv).
Calendar events and alarms are the reminder system (see reminder_log.csv).
Daily brief summarizes active decisions, stale review, and loop alerts.
"""

OFFICES = [
    {
        "office": "Mission Control",
        "role": "Lead router / decision board",
        "lane": "Decisions, briefs, batch asks, escalation",
        "may_contact_user": "yes",
        "notes": "Only lead office tells the user when MC is lead",
    },
    {
        "office": "Mail & Schedule",
        "role": "Mailroom and calendar",
        "lane": "Drafts, mail prep, calendar, alarms",
        "may_contact_user": "when_lead",
        "notes": "No send without approval; drafts are not filings",
    },
    {
        "office": "Money & Debt",
        "role": "Money desk",
        "lane": "Bills, collectors, subscriptions, validation letters",
        "may_contact_user": "when_lead",
        "notes": "No pay / no mail Certified without approval",
    },
    {
        "office": "VA Benefits",
        "role": "VA claims and housing benefits",
        "lane": "VA deadlines, HLR, HUD-VASH, SCCHA packets",
        "may_contact_user": "when_lead",
        "notes": "No file or send without approval",
    },
    {
        "office": "File Vault",
        "role": "Records and vault",
        "lane": "Filing, duplicates, exposure, backups",
        "may_contact_user": "when_lead",
        "notes": "No delete / share / file without approval",
    },
    {
        "office": "School & Work",
        "role": "Career and school",
        "lane": "IBEW/ETASV, classes, job applications",
        "may_contact_user": "when_lead",
        "notes": "No send without approval",
    },
    {
        "office": "Photo Design & Creation",
        "role": "Photo and design",
        "lane": "Photos, design assets, handoffs to File Vault",
        "may_contact_user": "when_lead",
        "notes": "No share without approval",
    },
]

# Same Stage 1 sample rows + due_date for reminder log.
DECISIONS = [
    {
        "id": "D001",
        "title": "ETASV refresh and grab",
        "status": "Active",
        "lead_office": "School & Work",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "loop_count": "0",
        "due_date": "2026-11-01",
        "notes": "Refresh ETASV status; grab next steps. Draft only until approved.",
    },
    {
        "id": "D002",
        "title": "Old HLR review",
        "status": "Stale",
        "lead_office": "VA Benefits",
        "support_office": "File Vault",
        "needs_approval": "no",
        "loop_count": "2",
        "due_date": "2026-10-15",
        "notes": "Old Higher-Level Review item — review and archive or resolve.",
    },
    {
        "id": "D003",
        "title": "Calendar reminder cleanup",
        "status": "Needs Approval",
        "lead_office": "Mail & Schedule",
        "support_office": "Mission Control",
        "needs_approval": "yes",
        "loop_count": "0",
        "due_date": "2026-10-31",
        "notes": "Clean outdated reminders; calendar + alarms are the reminder system.",
    },
    {
        "id": "D004",
        "title": "Bill and subscription sweep",
        "status": "Waiting",
        "lead_office": "Money & Debt",
        "support_office": "Mail & Schedule",
        "needs_approval": "yes",
        "loop_count": "1",
        "due_date": "2026-11-01",
        "notes": "Sweep bills/subscriptions. No pay without approval.",
    },
    {
        "id": "D005",
        "title": "Duplicate cleanup",
        "status": "Needs Approval",
        "lead_office": "File Vault",
        "support_office": "Photo Design & Creation",
        "needs_approval": "yes",
        "loop_count": "0",
        "due_date": "2026-11-02",
        "notes": "Flag duplicates for archive. No delete/file without approval.",
    },
    {
        "id": "D006",
        "title": "Newsletter draft",
        "status": "Active",
        "lead_office": "Photo Design & Creation",
        "support_office": "Mail & Schedule",
        "needs_approval": "yes",
        "loop_count": "0",
        "due_date": "2026-11-03",
        "notes": "Draft only — drafts are not filings; no send without approval.",
    },
    {
        "id": "D007",
        "title": "Daily brief",
        "status": "Active",
        "lead_office": "Mission Control",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "loop_count": "0",
        "due_date": "2026-10-31",
        "notes": "Top-3 brief. Chat is coordination only — log outcomes in decisions.csv.",
    },
    {
        "id": "D008",
        "title": "Old ETASV reminder",
        "status": "Stale",
        "lead_office": "School & Work",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "loop_count": "3",
        "due_date": "2026-10-20",
        "notes": "Looped 3 times — escalate; review and archive or resolve.",
    },
]

BOT_PROMPTS = {
    "mission_control_prompt.txt": (
        "You are the Mission Control bot. You manage the live decision queue, "
        "the daily brief, the approval gate, and loop escalation. Use the "
        "decision queue as the source of truth. Keep each office in its lane. "
        "Escalate repeated issues after 3 loops. Never allow send, pay, delete, "
        "file, or share without approval."
    ),
    "mail_schedule_prompt.txt": (
        "You are the Mail & Schedule bot. You sort mail, manage calendars, "
        "track deadlines, and handle thread cleanup. Your work stays in your "
        "lane. Drafts are not filings. No final send without approval."
    ),
    "money_debt_prompt.txt": (
        "You are the Money & Debt bot. You track bills, balances, subscriptions, "
        "and forms. You may prepare, but you may not pay or send without approval."
    ),
    "va_benefits_prompt.txt": (
        "You are the VA Benefits bot. You track HLRs, letters, exams, and claims. "
        "You may draft but not finalize government filings without approval."
    ),
    "file_vault_prompt.txt": (
        "You are the File Vault bot. You organize, back up, rename, and clean "
        "duplicate files. You may not delete, share, or file records without "
        "approval."
    ),
    "school_work_prompt.txt": (
        "You are the School & Work bot. You manage ETASV, school tasks, deadlines, "
        "jobs, and time tickets. Keep only active items in your queue. You may "
        "draft applications, but you may not send, pay, delete, share, or file "
        "without approval."
    ),
    "photo_design_prompt.txt": (
        "You are the Photo Design & Creation bot. You generate visuals and "
        "newsletters. Do not send or share final content without approval."
    ),
}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ensure_seed_files() -> None:
    """Write starter decisions/offices/rules/bot prompts if missing."""
    STAGE2.mkdir(parents=True, exist_ok=True)
    BOTS.mkdir(parents=True, exist_ok=True)

    rules_path = STAGE2 / "mission_control_rules.txt"
    if not rules_path.exists():
        rules_path.write_text(RULES_TEXT, encoding="utf-8")

    offices_path = STAGE2 / "offices.csv"
    if not offices_path.exists():
        write_csv(offices_path, OFFICE_FIELDS, OFFICES)

    decisions_path = STAGE2 / "decisions.csv"
    if not decisions_path.exists():
        write_csv(decisions_path, DECISION_FIELDS, DECISIONS)

    for name, text in BOT_PROMPTS.items():
        prompt_path = BOTS / name
        if not prompt_path.exists():
            prompt_path.write_text(text.strip() + "\n", encoding="utf-8")


def validate_queue(
    decisions: list[dict[str, str]], offices: list[dict[str, str]]
) -> list[str]:
    """Return validation warnings (non-fatal). Keep offices in lane."""
    warnings: list[str] = []
    office_names = {row["office"] for row in offices}
    known_status = LIVE_STATUSES | {STALE_STATUS, "Done", "Parked"}

    for row in decisions:
        did = row.get("id", "?")
        lead = row.get("lead_office", "")
        support = row.get("support_office", "")
        status = row.get("status", "")
        if lead not in office_names:
            warnings.append(f"{did}: unknown lead_office '{lead}'")
        if support not in office_names:
            warnings.append(f"{did}: unknown support_office '{support}'")
        if lead and support and lead == support:
            warnings.append(f"{did}: lead and support must be different offices")
        if status not in known_status:
            warnings.append(f"{did}: unexpected status '{status}'")
        try:
            int(row.get("loop_count") or "0")
        except ValueError:
            warnings.append(f"{did}: loop_count must be an integer")
    return warnings


def build_reminders(
    live: list[dict[str, str]], created_at: str
) -> list[dict[str, str]]:
    """Calendar/alarm-style reminder rows for live items with due dates."""
    rows: list[dict[str, str]] = []
    for item in live:
        due = (item.get("due_date") or "").strip()
        if not due:
            continue
        lead = item.get("lead_office", "Mission Control")
        rows.append(
            {
                "decision_id": item["id"],
                "office": lead,
                "reminder_type": "due_date",
                "scheduled_for": f"{due}T09:00:00",
                "status": "scheduled",
                "created_at": created_at,
            }
        )
        # Day-before alarm when due is parseable.
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
                    "created_at": created_at,
                }
            )
        except ValueError:
            pass
    return rows


def build_loop_alerts(
    decisions: list[dict[str, str]], created_at: str
) -> list[dict[str, str]]:
    alerts: list[dict[str, str]] = []
    for item in decisions:
        try:
            loops = int(item.get("loop_count") or "0")
        except ValueError:
            loops = 0
        if loops < LOOP_ESCALATE_AT:
            continue
        alerts.append(
            {
                "decision_id": item["id"],
                "office": item.get("lead_office", "Mission Control"),
                "reason": f"loop_count {loops} >= {LOOP_ESCALATE_AT}; escalate",
                "loop_count": str(loops),
                "created_at": created_at,
            }
        )
    return alerts


def write_daily_brief(
    path: Path,
    live: list[dict[str, str]],
    stale: list[dict[str, str]],
    loops: list[dict[str, str]],
    warnings: list[str],
    generated_at: str,
) -> None:
    needs = [r for r in live if r.get("status") == "Needs Approval"]
    approval_note = (
        f"{len(needs)} Needs Approval (max {MAX_APPROVALS_PER_DAY}/day)"
    )
    lines = [
        "Mission Control — Daily Brief (Stage 2)",
        f"Generated: {generated_at}",
        "",
        "Source of truth: decisions.csv + live_decisions.csv",
        "Chat is coordination only.",
        "No send / pay / delete / share / file without approval.",
        "",
        f"Live decisions ({len(live)}) — Active / Waiting / Needs Approval",
        f"Approval gate: {approval_note}",
    ]
    if not live:
        lines.append("- (none)")
    for row in live:
        lines.append(
            f"- [{row['id']}] {row['title']} | {row['status']} | "
            f"lead={row['lead_office']} support={row['support_office']}"
        )

    lines.extend(["", f"Stale review ({len(stale)}) — archive or reactivate"])
    if not stale:
        lines.append("- (none)")
    for row in stale:
        lines.append(
            f"- [{row['id']}] {row['title']} | loops={row.get('loop_count', '0')} | "
            f"lead={row['lead_office']}"
        )

    lines.extend(["", f"Loop alerts ({len(loops)}) — escalate at {LOOP_ESCALATE_AT}+"])
    if not loops:
        lines.append("- (none)")
    for row in loops:
        lines.append(
            f"- [{row['decision_id']}] {row['office']}: {row['reason']}"
        )

    if warnings:
        lines.extend(["", "Validation warnings"])
        for w in warnings:
            lines.append(f"- {w}")

    lines.extend(
        [
            "",
            "Reminders: see reminder_log.csv (calendar + alarms).",
            "Only the lead office tells the user.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_seed_files()

    # Always refresh rules text to Stage 2 policy (safe overwrite of known file).
    (STAGE2 / "mission_control_rules.txt").write_text(RULES_TEXT, encoding="utf-8")
    for name, text in BOT_PROMPTS.items():
        (BOTS / name).write_text(text.strip() + "\n", encoding="utf-8")

    decisions = read_csv(STAGE2 / "decisions.csv")
    offices = read_csv(STAGE2 / "offices.csv")
    _ = (STAGE2 / "mission_control_rules.txt").read_text(encoding="utf-8")

    warnings = validate_queue(decisions, offices)
    live = [r for r in decisions if r.get("status") in LIVE_STATUSES]
    stale = [r for r in decisions if r.get("status") == STALE_STATUS]

    created_at = datetime.now().replace(microsecond=0).isoformat()
    reminders = build_reminders(live, created_at)
    loops = build_loop_alerts(decisions, created_at)

    write_csv(STAGE2 / "live_decisions.csv", DECISION_FIELDS, live)
    write_csv(STAGE2 / "stale_review.csv", DECISION_FIELDS, stale)
    write_csv(STAGE2 / "reminder_log.csv", REMINDER_FIELDS, reminders)
    write_csv(STAGE2 / "loop_alerts.csv", LOOP_FIELDS, loops)
    write_daily_brief(
        STAGE2 / "daily_brief.txt",
        live,
        stale,
        loops,
        warnings,
        created_at,
    )

    print(
        "Stage 2 ready: "
        f"{STAGE2.name}/ "
        f"({len(decisions)} decisions, {len(live)} live, {len(stale)} stale, "
        f"{len(reminders)} reminders, {len(loops)} loop alerts, "
        f"{len(offices)} offices, {len(BOT_PROMPTS)} bot prompts)"
    )
    if warnings:
        print(f"Validation warnings: {len(warnings)}")


if __name__ == "__main__":
    main()
