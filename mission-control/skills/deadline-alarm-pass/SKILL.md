---
name: deadline-alarm-pass
description: Ensure every dated Mission Control item has a phone-reaching alarm. Run a 6 AM backup pass and verify each dated Decision Board / calendar / VA deadline item has a Calendar reminder. Use when alarms were late or the phone was offline.
disable-model-invocation: false
---

# Deadline Alarm Pass (ops fix #3 — happening now)

## Problem

Google Calendar reminders ≠ guaranteed phone SMS. If the phone is offline at the set-alarm pass (e.g. 9 PM), alarms land late.

## Passes

| Pass | When (PT) | Action |
| --- | --- | --- |
| Primary | Evening (with dual-brief PM) | Create/update Calendar events + reminders for new dated items |
| Backup | 6:00 AM (with dual-brief AM) | Re-check every dated open item; create any missing alarms |

## Coverage checklist

For each dated item from:

- Decision Board (Due)
- Team Task Board due dates
- `va-deadline-tracker` rows
- Master deadline calendar

Verify:

1. Google Calendar event exists (title includes office + short label)
2. Reminder set (popup + email when available)
3. Alarm-status note on the source card: `alarm:set <eventId>` or `alarm:missing`

## Tools

- **Google Calendar** `list_events`, `create_event` / `create_events`, `update_event`, `get_event`
- **cursor-subscriptions** `subscribe_timer` — `mc-alarm-backup` cron `0 6 * * *` America/Los_Angeles (or equivalent UTC cron)
- **Notion** update Source cards with alarm status
- Companion: `va-deadline-tracker`, `master-deadline-calendar`

## Phone bridge (gap)

Calendar alone may not buzz a locked phone. Prefer:

1. Calendar event with reminders (always)
2. Optional SMS/voice bridge only if Tam designates a channel (AgentMail inbox calendar, or human SMS app) — **never invent a phone number or send without SEND**

## Rules

- Never invent deadlines.
- Examples to cover when present: Diversified Thu 10/29, SCCHA Nov 10, Form 998 Nov 10, Form Dec 13.
- Idempotent: if event already exists for that item, update — do not duplicate.
