"""Classify raw tasks by office, urgency, and approval need (rule-based Stage 3)."""

from __future__ import annotations

import re

from .common import audit, load_global_rules, load_office_rules

URGENCY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def _token_in_text(token: str, text: str) -> bool:
    """True when token appears as a whole word/phrase (not a raw substring)."""
    token = token.lower().strip()
    if not token:
        return False
    pattern = r"(?<!\w)" + re.escape(token) + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _score_office(text: str, keywords: list[str]) -> int:
    score = 0
    for keyword in keywords:
        if _token_in_text(keyword, text):
            score += 1
    return score


def classify_task(
    title: str,
    notes: str = "",
    requested_action: str = "",
    urgency_hint: str = "",
) -> dict:
    """Return lead office candidate, urgency, and whether approval is required."""
    offices = load_office_rules()["offices"]
    global_rules = load_global_rules()
    high_risk = {a.lower() for a in global_rules.get("high_risk_actions", [])}

    blob = f"{title} {notes}".lower()
    scored: list[tuple[int, dict]] = []
    for office in offices:
        scored.append((_score_office(blob, office.get("keywords", [])), office))
    scored.sort(key=lambda item: item[0], reverse=True)

    best_score, best_office = scored[0]
    if best_score == 0:
        best_office = next(o for o in offices if o["name"] == "Mission Control")

    urgency = (urgency_hint or best_office.get("urgency_default") or "medium").lower()
    if urgency not in URGENCY_RANK:
        urgency = "medium"

    # Bump urgency for explicit urgency words (word-boundary match).
    if any(_token_in_text(k, blob) for k in ("urgent", "deadline", "overdue", "today")):
        urgency = "high" if URGENCY_RANK[urgency] < URGENCY_RANK["high"] else urgency

    action = requested_action.lower().strip()
    needs_approval = action in high_risk
    if not action:
        # Infer high-risk intent from whole words/phrases only.
        # Prefer longer phrases first so "government filing" wins over "file".
        for risk in sorted(high_risk, key=len, reverse=True):
            phrase = risk.replace("_", " ")
            if _token_in_text(phrase, blob) or _token_in_text(risk, blob):
                needs_approval = True
                action = risk
                break

    result = {
        "office_name": best_office["name"],
        "office": best_office,
        "urgency": urgency,
        "needs_approval": needs_approval,
        "requested_action": action,
        "score": best_score,
    }
    audit(
        "classification_service",
        "classify",
        "",
        f"office={result['office_name']} urgency={urgency} needs_approval={needs_approval}",
    )
    return result
