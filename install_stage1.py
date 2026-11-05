#!/usr/bin/env python3
"""Generate Mission Control Stage 1 operational files (CSV + rules)."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE1 = ROOT / "mission_control_stage1"

LIVE_STATUSES = {"Active", "Waiting", "Needs Approval"}
STALE_STATUS = "Stale"

RULES_TEXT = """Mission Control — Stage 1 Rules
================================

Source of truth = decisions list (decisions.csv).
Chat is not the official record.

Live items
----------
Only Active, Waiting, and Needs Approval items are live.
Those rows appear in live_decisions.csv.

Stale items
-----------
Stale items go to stale_review.csv.
Old items must be reviewed and archived or resolved.

Approvals and actions
---------------------
No office may send, pay, delete, share, or file without approval.
Max 7 approvals per day.
Drafts are not filings.

Offices and lanes
-----------------
One lead office and one support office per item.
Only the lead office tells the user.
No office crosses its lane.

Escalation and reminders
------------------------
If an issue loops 3 times, escalate.
Calendar + alarms are the reminder system.

Stage 1 scope
-------------
This pack is Stage 1 only: simple CSV + plain-text rules.
It does not automate sending, paying, deleting, sharing, or filing.
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

# Starter decisions — mixed live + stale for Stage 1 filters.
DECISIONS = [
    {
        "id": "D001",
        "title": "ETASV refresh and grab",
        "status": "Active",
        "lead_office": "School & Work",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "loop_count": "0",
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
        "notes": "Top-3 brief. Chat is not the official record — log outcomes here.",
    },
    {
        "id": "D008",
        "title": "Old ETASV reminder",
        "status": "Stale",
        "lead_office": "School & Work",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "loop_count": "3",
        "notes": "Looped 3 times — escalate; review and archive or resolve.",
    },
]

DECISION_FIELDS = [
    "id",
    "title",
    "status",
    "lead_office",
    "support_office",
    "needs_approval",
    "loop_count",
    "notes",
]

OFFICE_FIELDS = [
    "office",
    "role",
    "lane",
    "may_contact_user",
    "notes",
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    STAGE1.mkdir(parents=True, exist_ok=True)

    (STAGE1 / "mission_control_rules.txt").write_text(RULES_TEXT, encoding="utf-8")
    write_csv(STAGE1 / "offices.csv", OFFICE_FIELDS, OFFICES)
    write_csv(STAGE1 / "decisions.csv", DECISION_FIELDS, DECISIONS)

    live = [row for row in DECISIONS if row["status"] in LIVE_STATUSES]
    stale = [row for row in DECISIONS if row["status"] == STALE_STATUS]
    write_csv(STAGE1 / "live_decisions.csv", DECISION_FIELDS, live)
    write_csv(STAGE1 / "stale_review.csv", DECISION_FIELDS, stale)

    print(
        f"Stage 1 ready: {STAGE1}/ "
        f"({len(DECISIONS)} decisions, {len(live)} live, {len(stale)} stale, "
        f"{len(OFFICES)} offices)"
    )


if __name__ == "__main__":
    main()
