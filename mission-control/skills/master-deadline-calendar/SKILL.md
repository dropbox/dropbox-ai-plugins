---
name: master-deadline-calendar
description: Maintain one deadline calendar covering legal, VA, housing, school, and money dates. Sync dated items onto Tam's Google Calendar and keep a single list. Examples - Diversified, SCCHA, Form 998, Form Dec.
disable-model-invocation: false
---

# Master Deadline Calendar (ops fix #5)

## Purpose

One list. Every legal / VA / housing / school / money deadline. Mirrored on Google Calendar.

## Canonical list (Notion or Dropbox TSV)

Columns: `deadline | domain | title | source | calendar_event_id | alarm_status | owner_office`

Domains: `legal` · `va` · `housing` · `school` · `money`

## Seed examples (verify before writing — do not invent)

| Item | Domain | Target window |
| --- | --- | --- |
| Diversified | money/legal | Thu 10/29 |
| SCCHA | housing | Nov 10 |
| Form 998 | va | Nov 10 |
| Form (Dec) | va | Dec 13 |

Only add a date after it appears in a letter, board card, or Tam confirmation.

## Tools

- **Google Calendar** `list_events`, `create_event` / `create_events`, `update_event`, `search_events`
- **Notion** page/DB under Master Command Center (or relation from Decision Board Due)
- **Dropbox** optional archive `va-deadlines.tsv` / `master-deadlines.tsv` under `/06_AI_Notes/`
- Feeds: `va-deadline-tracker`, `deadline-alarm-pass`, `dual-brief`

## Sync rules

1. List existing Calendar events tagged `[MC-DEADLINE]` in the title prefix.
2. Diff against canonical list.
3. Create missing; update moved dates; never silently delete — mark cancelled and ask Tam.
4. After sync, run `deadline-alarm-pass` coverage check.

## Owner

Mail & Schedule owns Calendar writes; Mission Control owns the canonical list; offices own source facts.
