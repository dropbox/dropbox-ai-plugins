---
name: unknown-activity-gate
description: Detect unexpected overnight or background activity (e.g. Cursor cloud agents). Send one alert, then pause further autonomous work until Tam answers. Use when agents run without a clear open task from Tam.
disable-model-invocation: false
---

# Unknown Activity Gate (ops fix #6)

## Rule

Unexpected activity → **one** alert → **pause** until Tam answers. No second nag; no silent continue.

## What counts as unknown

- Cursor cloud agent RUNNING/IDLE overnight without a matching open Team Task Board card or Tam prompt
- New automation / timer firing that Tam did not approve
- Outbound draft created without an owning office card
- New login / device signal (hand to `weekly-security-sweep`)

## Tools

- **cursor-cloud** `list-cloud-agents` — filter `statuses: RUNNING|IDLE`, check `createdAfter` / overnight window
- **cursor-cloud** `get-events` — soft failures / MCP auth errors
- **cursor-subscriptions** `list_subscriptions` — unexpected timers
- **Notion** Decision Board row: "Allow agent X to continue? Y/N"
- Delivery: chat (preferred) or Gmail `create_draft` DRAFT ONLY

## Workflow

1. Detect unknown run (name, URL, branch, started time).
2. Alert once: short voice-friendly line + link.
3. Set gate flag: `MC_GATE=paused` on Decision Board / note.
4. Stop starting new autonomous passes (except life-safety deadlines already on calendar).
5. On Tam yes → clear gate, continue. On no → stop/archive the agent work and note why.

## Rules

- Do not kill another agent's process unless Tam says so.
- Do not expand scope while paused.
- Pair with `subscribe_timer` only for approved MC passes (dual-brief, alarm backup, security sweep, friday scorecard).
