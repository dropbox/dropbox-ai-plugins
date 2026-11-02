---
name: weekly-security-sweep
description: Weekly security sweep for new sign-ins, credit-check mail, and exposed personal info, plus a running list of passwords to change. Owner Office - File Vault with Mission Control scheduling.
disable-model-invocation: false
---

# Weekly Security Sweep (ops fix #7)

## Cadence

Friday morning or Sunday evening (pair with `friday-scorecard` or dual-brief). Timer name: `mc-security-sweep`.

## Checks

| Check | How |
| --- | --- |
| New sign-ins | Gmail search: `subject:(new sign-in OR security alert OR new login OR unusual activity) newer_than:7d` |
| Credit checks / freezes | Gmail: `subject:(credit OR Equifax OR Experian OR TransUnion OR AnnualCreditReport) newer_than:7d` + existing Team Task Board credit cards |
| Exposed personal info | Drive/Dropbox public-link / sharing review via File Vault skills; quarantine hits via `personal-credential-quarantine` |
| Passwords to change | Running Notion list (or vault note) — add only when a real exposure or reset is confirmed |

## Tools

- **Gmail** `search_emails`, `read_email` (summarize — do not paste secrets)
- **Google Drive** `list_comments` / permissions tools when reviewing shared files
- **Dropbox** `list_shared_links`, `get_file_metadata`
- **Notion** Team Task Board security cards + Decision Board if Tam action needed
- Companion: `personal-credential-quarantine`
- Optional research: **Context** `web-search` / `create-monitor` only for public breach pages Tam already tracks — never submit PII to third parties
- **Opsera** `security-scan` is for **code repos**, not personal accounts — use only on git changes

## Output (voice-friendly)

```
Security week of <date>
Sign-ins: …
Credit: …
Exposure: …
Passwords to change: N (list titles only)
Need you: …
```

## Rules

- Never print full SSN, full account numbers, or password values.
- Never email contacts on the private do-not-email list.
- Flag FoundersCard / ChatGPT export style cards already on the board — do not duplicate.
