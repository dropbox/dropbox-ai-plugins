# Release Records

This directory tracks provider submission records for the Dropbox Claude and
Codex plugin artifacts.

## Current Draft Records

| Provider | Manifest | Artifact path | Version tag | Submitted SHA | Status |
| --- | --- | --- | --- | --- | --- |
| Claude | `claude-v1.0.0.json` | `claude/` | `claude-v1.0.0` | `0b2ec55e1f0d4d36cf30cd7dc9aca93960bacf75` | Ready for submission |
| Codex | `codex-v1.0.0.json` | `codex/` | `codex-v1.0.0` | `0b2ec55e1f0d4d36cf30cd7dc9aca93960bacf75` | Ready for submission |

The submitted SHA above is the current public artifact commit prepared for
review. Update it if release-record edits are included in the final submitted
commit.

## Release Flow

Use `SUBMISSION_CHECKLIST.md` before each provider submission to confirm
package, OAuth, copy, security, and release-record requirements.

Create future release records by copying the previous provider manifest. Each
completed manifest should record the provider, artifact path, version tag,
submitted commit SHA, submission date, validation state, and any submission
notes.

Do not mark a provider record as submitted or launched until the artifact has
completed Product, Content Design, Legal, Security, Analytics, and Engineering
review.
