---
name: voice-friendly-reply
description: Keep Mission Control messages short enough to read on a phone and tolerate Tam's voice-typing slips. Apply to all briefs, decision asks, alerts, and scorecards.
disable-model-invocation: false
---

# Voice-Friendly Reply (ops fix #9)

## Format rules

- **≤8 short lines** for alerts and asks; briefs follow `dual-brief` template.
- One ask per message when possible; if multiple, number them `1) 2) 3)`.
- Lead with the action word: `Need you:`, `Alert:`, `Done:`, `Stuck:`.
- No walls of markdown tables in chat — put tables in Notion; chat gets the summary.
- Prefer plain words over jargon; expand acronyms once if new.

## Voice-typing slip book (learn and keep)

Maintain a short correction list in Notion or `/06_AI_Notes/voice_slips.md` as Tam corrects:

| Heard / typed | Meant |
| --- | --- |
| (fill as Tam corrects) | |

When ambiguous, confirm in one short line: `Did you mean X or Y?`

## Tools

- Delivery: Cursor chat (primary), optional Slack via subscriptions, Gmail draft only if Tam wants email briefs
- Durable prefs/voice slips: `AGENTS.md` via continual-learning, plus Notion or `/06_AI_Notes/voice_slips.md` (Adapter declined)
- Never store passwords or SSN in the slip book

## Apply everywhere

`dual-brief` · `decision-board` · `unknown-activity-gate` · `weekly-security-sweep` · `batch-backlog-clear` · `friday-scorecard` · alarm alerts
