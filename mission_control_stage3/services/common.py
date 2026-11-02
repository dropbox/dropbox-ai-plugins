"""Shared paths, CSV helpers, and audit logging for Stage 3."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGE3 = Path(__file__).resolve().parent.parent
CONFIG = STAGE3 / "config"
DATA = STAGE3 / "data"
PROMPTS = STAGE3 / "prompts"

DECISION_FIELDS = [
    "id",
    "title",
    "status",
    "urgency",
    "lead_office",
    "support_office",
    "needs_approval",
    "missing_fields",
    "loop_count",
    "due_date",
    "notes",
    "created_at",
    "updated_at",
]

OFFICE_FIELDS = [
    "office",
    "role",
    "lane",
    "may_contact_user",
    "notes",
]

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

APPROVAL_FIELDS = [
    "approval_id",
    "decision_id",
    "action",
    "office",
    "status",
    "requested_at",
    "decided_at",
    "notes",
]

AUDIT_FIELDS = [
    "timestamp",
    "actor",
    "action",
    "decision_id",
    "detail",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_global_rules() -> dict[str, Any]:
    return load_json(CONFIG / "global_rules.json")


def load_office_rules() -> dict[str, Any]:
    return load_json(CONFIG / "office_rules.json")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def append_csv(path: Path, fieldnames: list[str], row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def audit(actor: str, action: str, decision_id: str = "", detail: str = "") -> None:
    append_csv(
        DATA / "audit_log.csv",
        AUDIT_FIELDS,
        {
            "timestamp": now_iso(),
            "actor": actor,
            "action": action,
            "decision_id": decision_id,
            "detail": detail,
        },
    )


def live_statuses() -> set[str]:
    rules = load_global_rules()
    return set(rules.get("live_statuses", ["Active", "Waiting", "Needs Approval"]))


def next_decision_id(decisions: list[dict[str, str]]) -> str:
    max_n = 0
    for row in decisions:
        raw = row.get("id", "")
        if raw.startswith("D") and raw[1:].isdigit():
            max_n = max(max_n, int(raw[1:]))
    return f"D{max_n + 1:03d}"
