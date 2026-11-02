# Mission Control — Stage 3

Safe AI-assisted **routing and decision layer**. Upgrades Stage 2 with intake,
classification, routing, validation, reminders, live queue, daily brief, audit
trail, and an approval gate for high-risk actions.

Stage 3 **never** sends, pays, deletes, shares, or files on its own.

## Layout

```
mission_control_stage3/
  app.py
  config/office_rules.json
  config/global_rules.json
  data/*.csv
  prompts/*_prompt.txt
  agents/
  services/
```

## Quick start

```bash
cd mission_control_stage3
python3 app.py init
python3 app.py brief
python3 app.py intake --title "Pay water bill" --action pay --due-date 2026-11-05
python3 app.py request-approval --decision-id D009 --action pay --office "Money & Debt"
python3 app.py decide-approval --approval-id A001 --approve
```

## Safety rules

- Source of truth = `data/decisions.csv` (chat is coordination only)
- Live = Active / Waiting / Needs Approval → `live_decisions.csv`
- Stale → `stale_review.csv`
- High-risk (`send`, `pay`, `delete`, `share`, `file`, `government_filing`) stay behind approvals
- High-risk intake always lands as `Needs Approval` (missing fields are recorded, not demoted to Waiting)
- Max 7 approvals/day; loop ≥3 → escalate
- Only the lead office tells the user; no lane crossing (`no_lane_crossing` in `global_rules.json`)
- `approval_service.is_action_allowed` enforces lanes: global `safe_without_approval` does not grant every office Mission Control actions; `approved=True` still cannot cross lanes
- Calendar + alarms = reminder system (`reminder_log.csv`)
- Every action appends to `audit_log.csv`

## Office rules (`config/office_rules.json`)

Each office includes: `name`, `role`, `lane`, `keywords`, `allowed_actions`,
`forbidden_without_approval`, `may_contact_user`, `default_support`, `urgency_default`.

An action is in-lane when it appears in that office's `allowed_actions` or
`forbidden_without_approval`. Out-of-lane requests are rejected even after approval.
