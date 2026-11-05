# Mission Control (local Cursor plugin)

Chief-of-staff plugin for Tam's 7 offices. **Not food.**

## Installed skills

### Core + routing

| Skill | Office |
| --- | --- |
| `mission-control-core` | Mission Control |
| `office-router` | Mission Control |
| `org-performance-connectors` | Mission Control + org-performance pack |

### Org performance plugins (companion)

Vendored in `/org-performance/`; also installed under `~/.cursor/plugins/local/`:

- `continual-learning` — memory into `AGENTS.md`
- `advisor` — second opinion on decisions
- `orchestrate` — parallel cloud agents (needs API key)

### Ops pack (10 office fixes)

| # | Skill | Fix |
| --- | --- | --- |
| 1 | `decision-board` | One live decision board |
| 2 | `dual-brief` | 6 AM + evening close-out only |
| 3 | `deadline-alarm-pass` | Alarms for every deadline + 6 AM backup |
| 4 | `auto-file-vault` | Same-day file finals + flag duplicates |
| 5 | `master-deadline-calendar` | One legal/VA/housing/school/money calendar |
| 6 | `unknown-activity-gate` | One alert then pause on unknown activity |
| 7 | `weekly-security-sweep` | Sign-ins, credit, exposure, password list |
| 8 | `batch-backlog-clear` | Batch Waiting-on-Tam yeses |
| 9 | `voice-friendly-reply` | Phone-short replies + voice-slip learning |
| 10 | `friday-scorecard` | Per-office finished / stuck / cost |

Happening now (priority): **1, 3, 4, 8**. Full tool wiring: [`INTEGRATION_MAP.md`](./INTEGRATION_MAP.md).

### VA / File Vault workflow pack (Dropbox source)

| Skill | Office |
| --- | --- |
| `dropbox-preflight-fact-check` | VA Benefits + File Vault |
| `silver-platter-filing-pack` | VA Benefits |
| `personal-credential-quarantine` | File Vault |
| `live-migraine-shift-log` | VA Benefits / School & Work |
| `visual-evidence-catalog` | Photo + File Vault |
| `legal-pile-gatekeeper` | VA Benefits |
| `cp-dbq-prep-card` | VA Benefits |
| `va-deadline-tracker` | VA Benefits + Mail |
| `ibew-apprentice-packet` | School & Work |
| `dual-vault-index-sync` | File Vault |

Source pack: Dropbox `/00_Intake/00_MASTER_INDEX_AND_ACTIVE_BRIEFS/00_INTEGRATED_10_GROK_WORKFLOW_SKILLS.txt`

Companion: local `dropbox` plugin (9 Dropbox MCP skills) for File Vault.

## Path

`~/.cursor/plugins/local/mission-control/`

Reload Cursor plugins / restart the agent session after install.

## Next step for Tam

Pick fix numbers to activate live (Notion DB, timers, filing pass). Skills are installed; live wiring waits for that pick.
