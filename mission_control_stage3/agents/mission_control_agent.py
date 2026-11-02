"""Mission Control agent — safe orchestrator for Stage 3 routing."""

from __future__ import annotations

from pathlib import Path

from services import (
    approval_service,
    brief_service,
    intake_service,
    routing_service,
)
from services.common import PROMPTS, audit


class MissionControlAgent:
    """Coordinates intake → classify → route → queue → brief. Never executes risky actions."""

    def __init__(self) -> None:
        self.prompt = (PROMPTS / "mission_control_prompt.txt").read_text(encoding="utf-8")

    def prompt_text(self) -> str:
        return self.prompt

    def intake(self, raw: dict) -> dict[str, str]:
        record = intake_service.intake_task(raw)
        routing_service.rebuild_queues()
        routing_service.create_reminders_for_live()
        routing_service.refresh_loop_alerts()
        audit("mission_control_agent", "intake", record["id"], record["title"])
        return record

    def refresh(self) -> dict[str, int]:
        counts = routing_service.rebuild_queues()
        counts["reminders"] = routing_service.create_reminders_for_live()
        counts["loop_alerts"] = routing_service.refresh_loop_alerts()
        audit("mission_control_agent", "refresh", "", str(counts))
        return counts

    def brief(self) -> str:
        return brief_service.generate_daily_brief()

    def request_approval(
        self, decision_id: str, action: str, office: str, notes: str = ""
    ) -> dict[str, str]:
        row = approval_service.request_approval(decision_id, action, office, notes)
        routing_service.rebuild_queues()
        return row

    def decide_approval(
        self, approval_id: str, approve: bool, notes: str = ""
    ) -> dict[str, str]:
        return approval_service.decide_approval(approval_id, approve, notes)
