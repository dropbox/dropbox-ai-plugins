---
name: decision-board
description: Maintain one live Decision Board — each pending decision, recommendation, due date, and status — so nothing is asked twice or lost across brief notes. Use when consolidating Waiting-on-Tam items or when Tam asks for decisions needing sign-off.
disable-model-invocation: false
---

# Decision Board (ops fix #1 — happening now)

## Purpose

Replace dozens of scattered brief notes with **one** live board. Each row = one decision needing Tam.

## Schema (Notion database under Master Command Center)

| Property | Type | Notes |
| --- | --- | --- |
| Decision | Title | One clear ask |
| Recommendation | Rich text | Mission Control's advice |
| Due | Date | Hard date when known |
| Status | Status | `Open` · `Asked` · `Decided` · `Parked` |
| Office | Select | Mail · Money · VA · Records · Career · Photo · MC |
| Source | URL / text | Brief note / task card ID |
| Batch | Select | Optional group for batch-backlog-clear |

Parent page: Master Command Center `(Master Command Center id — private operator config)`  
Feed from: Team Task Board `(Team Task Board id — private operator config)` (Status = Waiting on Tam)

## Tools

- **Notion** `notion-create-database` / `notion-create-pages` / `notion-update-page` / `notion-query-data-sources` / `notion-search`
- Deduplicate: before adding a Decision, search title + Source; if same ask exists, update status — do not create a second row
- Cap: still **≤7 Open/Asked decisions per day** brought to Tam (MC core rule)

## Workflow

1. Sweep Team Task Board for `Waiting on Tam`.
2. Upsert into Decision Board (one row per unique ask).
3. Fill Recommendation before asking Tam.
4. After Tam answers → Status `Decided`, note the answer, close related board cards.

## Guardrails

- Never invent a decision Tam did not need.
- Do not create the live Notion DB until Tam approves fix #1.
- Voice replies stay short (see `voice-friendly-reply`).
