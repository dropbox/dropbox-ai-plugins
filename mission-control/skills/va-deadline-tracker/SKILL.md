---
name: va-deadline-tracker
description: Extract 30/60/90-day due-process windows from VA letters into a deadline tracker. Owner Office - VA Benefits with Mail and Schedule for alarms.
disable-model-invocation: false
---

# VA Deadline Tracker

## Purpose

Extract 30/60/90-day due-process windows from VA letters into `va-deadlines.tsv` (or Team Task Board + calendar).

## Fields

`letter_date | deadline | type | source_path_or_id | status | notes`

## Rules

- Do not assume finality or clock status when OPEN.
- Ask Mail & Schedule to set alarms that reach Tam's phone.
- Never invent a deadline not in the letter body.
