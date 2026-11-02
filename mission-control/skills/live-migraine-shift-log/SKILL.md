---
name: live-migraine-shift-log
description: Append migraine episodes and work shifts into existing logs without creating duplicates. Owner Office - VA Benefits with School and Work for shifts.
disable-model-invocation: false
---

# Live Migraine / Shift Log

## Purpose

Append new migraine episodes and work shifts into **existing** logs.

## Files

- `artifacts/logs/migraine-log.jsonl`
- `artifacts/logs/shift-log.jsonl`

## Rules

- Never start a duplicate log.
- Never invent frequencies, hours, or attack counts.
- Do not average frequencies for DC 8100 ratings from thin notes.
- OPEN cites stay OPEN.
