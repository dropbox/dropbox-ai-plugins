# Mission Control — Stage 2

Stage 1 CSV kit plus **safe automation**: validate queue, rebuild live/stale
views, daily brief, reminders, loop alerts, and per-office bot prompts.

Stage 2 may read, validate, route, summarize, alert, queue, and remind.
It does **not** send, pay, delete, share, or file without approval.

## Layout

```
mission_control_stage2/
  auto_stage2.py
  bots/*_bot.txt
  decisions.csv
  live_decisions.csv
  stale_review.csv
  offices.csv
  reminder_log.csv
  loop_alerts.csv
  daily_brief.txt
  mission_control_rules.txt
```

## Quick start

```bash
cd mission_control_stage2
python3 auto_stage2.py
```

Regenerates live/stale CSVs, reminder + loop logs, and `daily_brief.txt`.

## Hard limits

- Source of truth = `decisions.csv` (chat is coordination only)
- Live = Active / Waiting / Needs Approval
- Max 7 approvals/day; loop ≥3 → escalate
- One lead + one support office; only the lead tells the user
- No lane crossing; drafts are not filings
