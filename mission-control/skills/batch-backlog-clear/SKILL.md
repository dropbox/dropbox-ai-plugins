---
name: batch-backlog-clear
description: Collapse ~60 Waiting-on-Tam items into a few batch decisions so one answer clears many. Use when the Decision Board or Team Task Board backlog is too large for daily 7-decision cap.
disable-model-invocation: false
---

# Batch Backlog Clear (ops fix #8 — happening now)

## Problem

~60 items wait on Tam's yes. Asking one-by-one burns the ≤7/day cap and repeats asks.

## Method

1. Pull all `Waiting on Tam` from Team Task Board (`(Team Task Board id — private operator config)`).
2. Cluster into **batch decisions** (3–8 batches), e.g.:
   - File / archive duplicates (SCCHA, Drive publics)
   - Security OK (sign-in / credit / password resets)
   - Money / collectors next steps
   - VA packet SEND vs hold
   - School / IBEW packet actions
   - Calendar / alarm OK for dated set
3. Each batch = one Decision Board row with:
   - Recommendation
   - Bullet list of child cards cleared by "yes"
   - Due (if any)
4. On Tam **yes to batch** → mark all children Decided/Done.
5. On **partial** → split remaining into a new batch; never re-ask cleared items.

## Tools

- **Notion** `notion-search`, `notion-fetch`, `notion-query-data-sources`, `notion-update-page`, `notion-create-pages`
- Decision Board (`decision-board` skill)
- Voice format (`voice-friendly-reply`) — one batch ask per message when possible

## Example ask

```
Batch A — File Vault duplicates (12 items)
Rec: keep newest SCCHA packet; archive Pictures copies.
Reply YES-A / NO-A / PARTIAL-A.
```

## Rules

- Deduplicate before batching (same ask twice → one child).
- Still respect ≤7 Open/Asked decisions shown per day — batches count as one decision each.
- Do not SEND or file until the batch answer covers those children.
