# AGENTS.md — Mission Control memory

Seed file for the **continual-learning** plugin. The updater keeps only plain bullets under the two sections below.

Private identifiers (do-not-email list, VA file suffix, Notion ids) live in **`AGENTS.local.md`** (gitignored). See `AGENTS.local.example.md`.

## Learned User Preferences

- Prefer voice-friendly replies: short enough to read on a phone.
- Mission Control is chief of staff for 7 offices — not food or restaurants.
- Nothing outbound until the operator says send; Ready_to_sending is DRAFT-ONLY.
- Cap decisions needing the operator at ≤7 per day; batch backlog when possible.
- Prefer Top 3 items in briefs (6 AM + evening close-out when dual-brief is on).
- Skip Google Sheets and Adapter MCP; use Notion + Calendar + Slack instead.

## Learned Workspace Facts

- Resolve Team Task Board and Master Command Center ids from private operator config (`AGENTS.local.md`).
- Local plugins: `mission-control`, `dropbox`, `continual-learning`, `advisor`, `orchestrate`.
- Ops priority fires when enabled: decision board (#1), alarms (#3), auto-file (#4), batch backlog (#8).
- Connected MCPs in use: Notion, Dropbox, Google Calendar, Gmail, Slack; Sheets and Adapter declined.
- VA identity: approved file suffix from private operator config only; never print full SSN; never email contacts on the private do-not-email list.
