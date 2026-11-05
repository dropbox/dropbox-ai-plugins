#!/usr/bin/env python3
"""Mission Control Stage 3 — safe AI-assisted routing and decision layer (CLI)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

STAGE3 = Path(__file__).resolve().parent
if str(STAGE3) not in sys.path:
    sys.path.insert(0, str(STAGE3))

from agents.mission_control_agent import MissionControlAgent
from agents.office_agent import OfficeAgent
from services.common import (
    DATA,
    DECISION_FIELDS,
    OFFICE_FIELDS,
    audit,
    load_office_rules,
    now_iso,
    write_csv,
)

SEED_DECISIONS = [
    {
        "id": "D001",
        "title": "ETASV refresh and grab",
        "status": "Active",
        "urgency": "medium",
        "lead_office": "School & Work",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "missing_fields": "",
        "loop_count": "0",
        "due_date": "2026-11-01",
        "notes": "Refresh ETASV status; draft only until approved.",
        "created_at": "2026-10-30T00:00:00+00:00",
        "updated_at": "2026-10-30T00:00:00+00:00",
    },
    {
        "id": "D002",
        "title": "Old HLR review",
        "status": "Stale",
        "urgency": "low",
        "lead_office": "VA Benefits",
        "support_office": "File Vault",
        "needs_approval": "no",
        "missing_fields": "",
        "loop_count": "2",
        "due_date": "2026-10-15",
        "notes": "Old Higher-Level Review — archive or resolve.",
        "created_at": "2026-09-01T00:00:00+00:00",
        "updated_at": "2026-10-01T00:00:00+00:00",
    },
    {
        "id": "D003",
        "title": "Calendar reminder cleanup",
        "status": "Needs Approval",
        "urgency": "medium",
        "lead_office": "Mail & Schedule",
        "support_office": "Mission Control",
        "needs_approval": "yes",
        "missing_fields": "",
        "loop_count": "0",
        "due_date": "2026-10-31",
        "notes": "Clean outdated reminders; calendar + alarms are the reminder system.",
        "created_at": "2026-10-30T00:00:00+00:00",
        "updated_at": "2026-10-30T00:00:00+00:00",
    },
    {
        "id": "D004",
        "title": "Bill and subscription sweep",
        "status": "Waiting",
        "urgency": "high",
        "lead_office": "Money & Debt",
        "support_office": "Mail & Schedule",
        "needs_approval": "yes",
        "missing_fields": "",
        "loop_count": "1",
        "due_date": "2026-11-01",
        "notes": "Sweep bills/subscriptions. No pay without approval.",
        "created_at": "2026-10-29T00:00:00+00:00",
        "updated_at": "2026-10-29T00:00:00+00:00",
    },
    {
        "id": "D005",
        "title": "Duplicate cleanup",
        "status": "Needs Approval",
        "urgency": "medium",
        "lead_office": "File Vault",
        "support_office": "Photo Design & Creation",
        "needs_approval": "yes",
        "missing_fields": "",
        "loop_count": "0",
        "due_date": "2026-11-02",
        "notes": "Flag duplicates. No delete/file without approval.",
        "created_at": "2026-10-30T00:00:00+00:00",
        "updated_at": "2026-10-30T00:00:00+00:00",
    },
    {
        "id": "D006",
        "title": "Newsletter draft",
        "status": "Active",
        "urgency": "low",
        "lead_office": "Photo Design & Creation",
        "support_office": "Mail & Schedule",
        "needs_approval": "yes",
        "missing_fields": "",
        "loop_count": "0",
        "due_date": "2026-11-03",
        "notes": "Draft only — no send without approval.",
        "created_at": "2026-10-30T00:00:00+00:00",
        "updated_at": "2026-10-30T00:00:00+00:00",
    },
    {
        "id": "D007",
        "title": "Daily brief",
        "status": "Active",
        "urgency": "medium",
        "lead_office": "Mission Control",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "missing_fields": "",
        "loop_count": "0",
        "due_date": "2026-10-31",
        "notes": "Top-3 brief. Chat is coordination only.",
        "created_at": "2026-10-31T00:00:00+00:00",
        "updated_at": "2026-10-31T00:00:00+00:00",
    },
    {
        "id": "D008",
        "title": "Old ETASV reminder",
        "status": "Stale",
        "urgency": "low",
        "lead_office": "School & Work",
        "support_office": "Mail & Schedule",
        "needs_approval": "no",
        "missing_fields": "",
        "loop_count": "3",
        "due_date": "2026-10-20",
        "notes": "Looped 3 times — escalate; archive or resolve.",
        "created_at": "2026-08-15T00:00:00+00:00",
        "updated_at": "2026-10-20T00:00:00+00:00",
    },
]


def seed_data(force: bool = False) -> None:
    """Create starter CSV files if missing.

    --force-seed overwrites starter decisions/offices only.
    Approvals and audit logs are never wiped by --force-seed.
    Derived queues are created empty only when missing; callers rebuild them.
    """
    DATA.mkdir(parents=True, exist_ok=True)
    decisions_path = DATA / "decisions.csv"
    if force or not decisions_path.exists():
        write_csv(decisions_path, DECISION_FIELDS, SEED_DECISIONS)

    offices_path = DATA / "offices.csv"
    if force or not offices_path.exists():
        office_rows = []
        for office in load_office_rules()["offices"]:
            office_rows.append(
                {
                    "office": office["name"],
                    "role": office["role"],
                    "lane": office["lane"],
                    "may_contact_user": office.get("may_contact_user", "when_lead"),
                    "notes": "forbidden without approval: "
                    + ", ".join(office.get("forbidden_without_approval", [])),
                }
            )
        write_csv(offices_path, OFFICE_FIELDS, office_rows)

    # Derived / operational logs: create headers if missing. Never force-wipe
    # approvals or audit — the safety model depends on those ledgers.
    create_if_missing = (
        ("live_decisions.csv", DECISION_FIELDS),
        ("stale_review.csv", DECISION_FIELDS),
        ("reminder_log.csv", ["decision_id", "office", "reminder_type", "scheduled_for", "status", "created_at"]),
        ("loop_alerts.csv", ["decision_id", "office", "reason", "loop_count", "created_at"]),
        ("approvals.csv", ["approval_id", "decision_id", "action", "office", "status", "requested_at", "decided_at", "notes"]),
        ("audit_log.csv", ["timestamp", "actor", "action", "decision_id", "detail"]),
    )
    for name, fields in create_if_missing:
        path = DATA / name
        if not path.exists():
            write_csv(path, fields, [])

    audit("app", "seed_data", "", f"force={force} at {now_iso()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mission Control Stage 3 — safe routing and decision layer"
    )
    parser.add_argument(
        "--force-seed",
        action="store_true",
        help="Overwrite starter decisions/offices CSVs only (never wipes approvals or audit)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Seed data files and rebuild queues/brief")

    intake = sub.add_parser("intake", help="Intake a raw task into decisions.csv")
    intake.add_argument("--title", required=True)
    intake.add_argument("--notes", default="")
    intake.add_argument("--due-date", default="")
    intake.add_argument("--urgency", default="")
    intake.add_argument(
        "--action",
        default="",
        help="Requested action (send/pay/delete/share/file/government_filing need approval)",
    )

    sub.add_parser("refresh", help="Rebuild live/stale queues, reminders, loop alerts")
    sub.add_parser("brief", help="Generate daily brief")

    req = sub.add_parser("request-approval", help="Queue a high-risk action (does not execute)")
    req.add_argument("--decision-id", required=True)
    req.add_argument("--action", required=True)
    req.add_argument("--office", required=True)
    req.add_argument("--notes", default="")

    dec = sub.add_parser("decide-approval", help="Approve or deny a pending approval")
    dec.add_argument("--approval-id", required=True)
    dec.add_argument("--approve", action="store_true")
    dec.add_argument("--deny", action="store_true")
    dec.add_argument("--notes", default="")

    lane = sub.add_parser("lane", help="List live items for one office")
    lane.add_argument("--office", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    seed_data(force=args.force_seed)
    mc = MissionControlAgent()

    if args.command == "init":
        counts = mc.refresh()
        brief = mc.brief()
        print(
            "Stage 3 ready: "
            f"{counts['total']} decisions, {counts['live']} live, {counts['stale']} stale, "
            f"{counts['reminders']} reminders, {counts['loop_alerts']} loop alerts."
        )
        print(f"Brief written ({len(brief.splitlines())} lines).")
        return 0

    if args.command == "intake":
        record = mc.intake(
            {
                "title": args.title,
                "notes": args.notes,
                "due_date": args.due_date,
                "urgency": args.urgency,
                "requested_action": args.action,
            }
        )
        mc.brief()
        print(
            f"Created {record['id']}: {record['title']} | {record['status']} | "
            f"lead={record['lead_office']} support={record['support_office']} | "
            f"urgency={record['urgency']}"
        )
        return 0

    if args.command == "refresh":
        counts = mc.refresh()
        print(
            f"Refreshed: live={counts['live']} stale={counts['stale']} "
            f"reminders={counts['reminders']} loops={counts['loop_alerts']}"
        )
        return 0

    if args.command == "brief":
        # Always rebuild derived queues from decisions.csv before reading them.
        mc.refresh()
        text = mc.brief()
        print(text)
        return 0

    if args.command == "request-approval":
        row = mc.request_approval(
            args.decision_id, args.action, args.office, args.notes
        )
        print(
            f"Approval {row['approval_id']} pending for {row['action']} "
            f"on {row['decision_id']} (not executed)."
        )
        return 0

    if args.command == "decide-approval":
        if args.approve == args.deny:
            parser.error("Specify exactly one of --approve or --deny")
        row = mc.decide_approval(args.approval_id, approve=args.approve, notes=args.notes)
        print(f"Approval {row['approval_id']} -> {row['status']} (action still not auto-executed).")
        return 0

    if args.command == "lane":
        # Rebuild so lane view is never stuck on an empty/stale derived queue.
        mc.refresh()
        agent = OfficeAgent(args.office)
        rows = agent.lane_items()
        print(f"{args.office}: {len(rows)} live lane item(s)")
        for row in rows:
            tell = "LEAD/tell-user" if agent.may_tell_user(row) else "support-only"
            print(f"- [{row['id']}] {row['title']} | {row['status']} | {tell}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
