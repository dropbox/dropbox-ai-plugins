# Mission Control ops integration map

Maps the 10 office fixes to tools, MCP servers, and skills already available to this agent.  
**Happening now:** #1, #3, #4, #8. Others are ready to enable when Tam picks numbers.

## Quick map

| # | Fix | Primary tools | Companion skills | Status |
| --- | --- | --- | --- | --- |
| 1 | One decision board | Notion create/query/update | `decision-board`, `batch-backlog-clear` | Skill ready — create DB on Tam OK |
| 2 | Dual briefs (6 AM + PM) | `subscribe_timer`, Notion, Calendar, Dropbox notes | `dual-brief`, `voice-friendly-reply` | Skill ready — timers on Tam OK |
| 3 | Alarms for every deadline | Google Calendar create/list/update, `subscribe_timer` 6 AM backup | `deadline-alarm-pass`, `va-deadline-tracker`, `master-deadline-calendar` | Skill ready |
| 4 | Auto-filing + dup flags | Dropbox search/move/copy, Notion OK card | `auto-file-vault`, `dual-vault-index-sync`, Dropbox plugin organize/clean/find | Skill ready — SCCHA loose files confirmed |
| 5 | Single deadline calendar | Google Calendar + Notion list / TSV | `master-deadline-calendar`, `deadline-alarm-pass` | Skill ready |
| 6 | Unknown activity → alert + pause | cursor-cloud `list-cloud-agents`, `get-events`, subscriptions list | `unknown-activity-gate` | Skill ready |
| 7 | Weekly security sweep | Gmail search, Drive/Dropbox sharing, Notion | `weekly-security-sweep`, `personal-credential-quarantine` | Skill ready |
| 8 | Batch backlog clear | Notion Team Task Board + Decision Board | `batch-backlog-clear`, `decision-board` | Skill ready |
| 9 | Voice-friendly replies | Chat style + `AGENTS.md` / Notion voice slips | `voice-friendly-reply` | Skill ready |
| 10 | Friday scorecard | Notion board + list-cloud-agents | `friday-scorecard`, `dual-brief` | Skill ready |

## MCP / tool inventory (usable now)

### Already connected

| System | What MC uses it for |
| --- | --- |
| **Notion** | Team Task Board `(Team Task Board id — private operator config)`; Master Command Center `(Master Command Center id — private operator config)`; Decision Board (to create); security/credit cards |
| **Dropbox** | File Vault search/move/copy; SCCHA pile under `/Pictures of the day/`; Housing vault `/02_Personal/Housing/`; notes `/06_AI_Notes/`; Ready_to_sending draft lane |
| **Google Calendar** | Deadline events + reminders (phone alarm path) |
| **Gmail** | Brief/scorecard drafts (DRAFT ONLY); security/credit mail search |
| **cursor-subscriptions** | `subscribe_timer` for 6 AM brief, PM close-out, alarm backup, security sweep, Friday scorecard |
| **cursor-cloud** | Overnight/unknown agent detection (`list-cloud-agents`, `get-events`) |
| **Google Drive** | Public-link / exposure checks for security sweep |
| **Slack MCP** | Phone-reachable briefs/alerts (channel TBD — ask Tam; candidates `#332`, `#general`) |
| **Local plugins** | `mission-control`, `dropbox`, **`continual-learning`**, **`advisor`**, **`orchestrate`** (see `/org-performance/`) |

### Org-performance pack (installed)

| Plugin | Improves |
| --- | --- |
| **continual-learning** | Durable prefs/facts → `AGENTS.md` (voice slips, MC rules) |
| **advisor** | Second model on Decision Board / stuck / before done |
| **orchestrate** | Parallel cloud agents under MC (needs `CURSOR_API_KEY`) |

Skill: `org-performance-connectors`.

### Optional / gap fillers

| System | Use | Caveat |
| --- | --- | --- |
| **Context** `create-monitor` | Watch public deadline pages Tam names | Do not submit PII; needs Tam OK |
| **Adapter** remember/ask | Durable voice-slip facts + MC decisions | Declined — use `AGENTS.md` + Notion |
| **Google Sheets** | Deadline + Friday scorecard tables | Declined — use Notion + Calendar |
| **AgentMail** | Optional SMS/calendar bridge for alarms | Only if Tam designates an inbox; never invent phones |
| **Opsera security-scan** | Repo code security | Not for personal login/credit sweeps |
| **Linear** | Not primary — board of record is Notion | |

## Gaps (honest)

1. **Phone SMS alarms** — Calendar reminders help but do not guarantee a buzz if the phone was offline; needs a Tam-approved SMS/voice bridge or always-on Calendar notification settings on device.
2. **True auto-pause of other Cursor agents** — we can alert + stop *this* agent's further autonomous passes; killing/pausing another agent requires Tam confirmation (gate skill).
3. **Credit bureau freezes / password changes** — we surface mail + a change list; Tam (or Money/File Vault with SEND) must perform account actions.
4. **Dropbox binary upload** — MCP cannot upload local PDF binaries; filing is move/copy inside Dropbox + index sync.
5. **Adapter memory** — declined; store voice slips in `AGENTS.md` (continual-learning) and Notion / `/06_AI_Notes/voice_slips.md`.

## Enable order (recommended)

When Tam picks numbers, default enable order for active fires first:

1. `#1` Decision Board DB  
2. `#8` Batch the Waiting-on-Tam pile into that board  
3. `#3` Alarm backup timer + coverage pass  
4. `#4` Same-day SCCHA / loose-file file plan  
5. Then `#2 #5 #6 #7 #9 #10` as chosen  

## Hard guardrails (all fixes)

- Nothing outbound until Tam says **send**
- Never invent filings, deadlines, or exhibits
- Never email the blocked third-party contact
- VA file ending **(approved suffix in private operator config)** only; never print full SSN
- Ready_to_sending = DRAFT-ONLY until SEND
- Not food
