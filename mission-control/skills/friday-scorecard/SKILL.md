---
name: friday-scorecard
description: Friday scorecard per office — what finished, what is stuck, and what it costs. Use for weekly Mission Control close-out.
disable-model-invocation: false
---

# Friday Scorecard (ops fix #10)

## Cadence

Friday evening (or last dual-brief PM of the week). Timer: `mc-friday-scorecard`.

## Per office (one block each)

Offices: Mail & Schedule · Money & Debt · VA Benefits · File Vault · School & Work · Photo · Mission Control

```
<Office>
Finished: …
Stuck: …
Cost: … (time/agent runs/fees if known — else "n/a")
```

## Roll-up (voice-friendly)

```
Friday scorecard <date>
Top wins: 1) 2) 3)
Still stuck: …
Waiting on you: N
Cost note: …
```

## Tools

- **Notion** Team Task Board — filter Done this week vs Stuck / Waiting on Tam
- **cursor-cloud** `list-cloud-agents` — agent runs this week (rough cost proxy)
- **Dropbox** optional archive under `/06_AI_Notes/scorecards/`
- **Gmail** `create_draft` only if Tam wants emailed scorecard (DRAFT until SEND)
- Feeds Decision Board counts + dual-brief PM

## Rules

- Do not invent costs; if unknown, say `n/a`.
- Do not shame offices — facts only.
- Pair security findings into `weekly-security-sweep` section or one line "Security: see sweep".
