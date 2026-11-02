---
name: org-performance-connectors
description: Use the org-performance pack — continual-learning, advisor, and orchestrate — plus Notion/Dropbox/Calendar/Gmail timers to improve Mission Control organization speed and quality. Use when Tam asks for better org performance, multi-agent control, memory, or second opinions on decisions.
disable-model-invocation: false
---

# Org performance connectors

## Installed plugins (local)

| Plugin | When to use |
| --- | --- |
| `continual-learning` | After sessions: capture voice slips, prefs, durable MC facts into `AGENTS.md` |
| `advisor` | Before major Decision Board asks, when stuck, before declaring an ops pass done — `/advisor` |
| `orchestrate` | When MC must fan a large goal across parallel cloud agents (needs `CURSOR_API_KEY`) |

## Connected MCPs to prefer

1. Notion — Decision Board / Team Task Board  
2. Dropbox — auto-file vault  
3. Google Calendar + `subscribe_timer` — deadlines / dual briefs  
4. Gmail — security sweep (DRAFT outbound only)  
5. cursor-cloud — unknown-activity gate  

## Connector status

- **Slack MCP** — connected (ask Tam which channel for briefs/alerts)  
- **Adapter** — declined; use `AGENTS.md` + Notion for durable prefs  
- **Google Sheets** — declined; use Notion + Calendar for scorecard/deadlines  

## Rules

- Still ≤7 decisions/day; advisor improves quality, does not raise the cap.  
- Orchestrate does not bypass SEND / do-not-email list / draft-only guards.  
- Not food.
