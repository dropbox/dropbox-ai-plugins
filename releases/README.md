# Release Records

This directory tracks MCP Host submission records for the Dropbox Claude and
Codex plugin artifacts.

## Current Draft Records

| MCP Host | Manifest | Artifact path | Version tag | Submitted SHA | Status |
| --- | --- | --- | --- | --- | --- |
| Claude | `claude-v1.0.0.json` | `claude/` | `claude-v1.0.0` | `0b2ec55e1f0d4d36cf30cd7dc9aca93960bacf75` | Ready for submission |
| Codex | `codex-v1.0.0.json` | `codex/` | `codex-v1.0.0` | `0b2ec55e1f0d4d36cf30cd7dc9aca93960bacf75` | Ready for submission |

The submitted SHA above is the current public artifact commit prepared for
review. Update it if release-record edits are included in the final submitted
commit.

## Release Flow

Use `SUBMISSION_CHECKLIST.md` before each MCP Host submission to confirm
package, OAuth, copy, security, and release-record requirements.

Create future release records by copying the previous MCP Host manifest. Each
completed manifest should record the MCP Host, artifact path, version tag,
submitted commit SHA, submission date, validation state, and any submission
notes.

Do not mark an MCP Host record as submitted or launched until the artifact has
completed Product, Content Design, Legal, Security, Analytics, and Engineering
review.
