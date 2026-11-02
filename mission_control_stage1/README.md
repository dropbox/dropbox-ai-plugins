# Mission Control — Stage 1

Beginner-friendly operational kit. Source of truth is `decisions.csv` (not chat).

## Files

| File | Purpose |
| --- | --- |
| `mission_control_rules.txt` | Stage 1 policy |
| `offices.csv` | Seven offices and lanes |
| `decisions.csv` | Full decisions list (source of truth) |
| `live_decisions.csv` | Only Active, Waiting, Needs Approval |
| `stale_review.csv` | Only Stale |

## Install / refresh

From the repo root:

```bash
python3 install_stage1.py
```

Creates `mission_control_stage1/` and regenerates all files.

## Hard limits (Stage 1)

- No send / pay / delete / share / file without approval
- One lead + one support office per item; only the lead tells the user
- Drafts are not filings; max 7 approvals per day
- Loop 3 times → escalate
- Calendar + alarms for reminders
