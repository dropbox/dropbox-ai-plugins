---
name: dual-brief
description: Run only two Mission Control briefs — 6 AM open and evening close-out — each with the 3 most important items on top. Other check-ins feed these two instead of spawning their own lists.
disable-model-invocation: false
---

# Dual Brief (ops fix #2)

## Cadence

| Pass | When (America/Los_Angeles) | Job |
| --- | --- | --- |
| Morning open | ~6:00 AM | Top 3 + deadlines today/tomorrow + open Decision Board rows |
| Evening close-out | ~8:00–9:00 PM | What finished, what's stuck, what needs tomorrow's Top 3 |

All other check-ins (midday, office pings, agent notes) **append facts into the next brief draft** — they do not send their own list to Tam.

## Format (phone-readable)

```
MC [AM|PM] <date>
1) …
2) …
3) …
Deadlines: …
Waiting on you: N (see Decision Board)
```

Max ~8 short lines. Top 3 only for action; everything else is one-line status or parked.

## Tools

- **cursor-subscriptions** `subscribe_timer` — cron for 6 AM and ~8:30 PM PT
- **Notion** Decision Board + Team Task Board query
- **Google Calendar** `list_events` for today's deadlines
- **Gmail** `create_draft` (optional) — DRAFT ONLY until Tam says send; prefer chat/Slack delivery when available
- **Dropbox** `create_file` under `/06_AI_Notes/` for archive copy of each brief

## Timer prompts (when Tam enables #2)

- `mc-am-brief`: "Run dual-brief morning open. Top 3 only. Voice-friendly."
- `mc-pm-brief`: "Run dual-brief evening close-out. Top 3 for tomorrow. Voice-friendly."

## Rules

- Mid-day office noise → update Notion / brief draft, do **not** ping Tam unless a hard deadline moved or unknown-activity-gate fires.
- Never send outbound email without SEND.
