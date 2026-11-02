# Org performance pack (Mission Control boost)

Deep-research pick: **3 Cursor plugins** that improve how a multi-bot org runs — memory, decision quality, and real AI-over-AI orchestration.

Installed locally at `~/.cursor/plugins/local/` and vendored here.

## The three (why these, not fifty)

| Plugin | Org job | Maps to your MC fixes |
| --- | --- | --- |
| **continual-learning** | Stack learns your voice slips, prefs, and durable facts into `AGENTS.md` | #9 voice-friendly; less re-teaching |
| **advisor** | Stronger second model at major decisions / stuck / before done | #1 decision board quality; fewer bad asks |
| **orchestrate** | Fan work to parallel cloud agents with planner → workers → handoffs | True MC “orders the offices” pattern |

These beat random lifestyle plugins: they raise **organization performance**, not novelty.

## Already connected (keep using)

| Connector | Org use |
| --- | --- |
| Notion | Team Task Board + Decision Board |
| Dropbox + dropbox plugin | File Vault |
| Gmail | Security sweep / draft briefs |
| Google Calendar | Deadline alarms |
| cursor-subscriptions `subscribe_timer` | Dual briefs, alarm backup, Friday scorecard |
| cursor-cloud `list-cloud-agents` | Unknown-activity gate |

## Connector status

| Connector | Why | Status |
| --- | --- | --- |
| **Slack MCP** | Push briefs/alerts to phone channel | Connected (ask Tam which channel) |
| **Adapter** memory | Durable facts across chats | Declined — use `AGENTS.md` + Notion |
| **Google Sheets** | Live deadline + scorecard tables | Declined — use Notion + Calendar |
| **AgentMail** | SMS-style alarm bridge | Optional only if Tam designates an inbox |

## Orchestrate note

Needs `CURSOR_API_KEY` (and `bun`) to spawn real parallel agents. Without the key, the skill is installed but kickoff won’t run. Set key from [Cursor Integrations](https://cursor.com/dashboard/integrations).

## Advisor note

In chat: `/advisor` to enable second-opinion checkpoints (default strong Grok advisor).

## Continual-learning note

Writes plain bullets under `AGENTS.md` → `Learned User Preferences` / `Learned Workspace Facts`. Pair with Mission Control `voice-friendly-reply`.

## Source

Official Cursor plugins: https://github.com/cursor/plugins  
License: MIT (each plugin).
