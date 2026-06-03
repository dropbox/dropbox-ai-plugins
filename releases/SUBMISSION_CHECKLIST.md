# Provider Submission Checklist

Use this checklist before submitting a reviewed provider artifact to a provider
marketplace.

Status as of 2026-06-03:

- Claude artifact: draft release record created in `claude-v1.0.0.json`.
- Codex artifact: draft release record created in `codex-v1.0.0.json`.
- Local standalone validation passed:
  - `provider_skills_tests.py: 7 tests passed`
  - `package_validation_tests.py: 5 tests passed`
- OAuth sign-in, provider-client smoke tests, and write-flow validation are
  marked complete.
- Protected-resource metadata endpoints returned HTTP 200 for Claude and Codex.
- Product and Content Design approval for user-facing copy is marked complete.
- Manual security/privacy and license checks are marked complete.

## Artifact Package

- [x] Confirm the provider artifact path is correct: `codex/` for Codex or `claude/` for Claude.
- [x] Confirm the provider manifest is present and valid JSON.
- [x] Confirm the MCP configuration is present and points at the intended production MCP endpoint.
- [x] Confirm no generated, temporary, or local-only test files are included in the submitted artifact.

## Local Validation

- [x] Run the provider-specific validation flow.
- [x] Complete OAuth authentication in the provider client.
- [x] Run a read-only Dropbox smoke test.
- [x] If write-capable tools are included, validate at least one low-risk write flow in a test account or reviewed test environment.
- [x] Record any validation notes in the release manifest.

## OAuth And Scopes

- [x] Confirm the production protected-resource metadata endpoint is reachable.
- [x] Confirm the protected-resource metadata scope list matches `../shared/OAUTH_SCOPES.md`.
- [x] Confirm the visible provider tool list matches the tool-to-scope mapping in `../shared/OAUTH_SCOPES.md`.
- [x] Confirm write scopes are only requested for submitted tools that need write behavior.

## User-Facing Copy

- [x] Confirm plugin display name, description, short description, long description, keywords, and example prompts have Product and Content Design approval.
- [x] Confirm capability descriptions accurately describe read and write behavior.
- [x] Confirm known limitations are documented in provider-appropriate copy.
- [x] Confirm usage examples are safe, accurate, and approved for launch.

## Security And Privacy

- [x] Confirm no OAuth client secrets, refresh tokens, access tokens, user identifiers, or private credentials are present.
- [x] Confirm public-facing docs contain no private repository paths, internal-only URLs, or sensitive implementation details.
- [x] Confirm any third-party dependency license or copyright notices are preserved.

## Pre-Submission Gates

- [ ] Replace all manifest and copy placeholders with approved launch content.
- [ ] Confirm the public repository has branch protection requiring at least two approvals and Dropbox-only push access.
- [ ] Confirm Issues, Discussions, and Wiki are disabled for the public repository unless explicitly approved for launch.
- [ ] Confirm CODEOWNERS covers provider Skill and configuration paths with the required security review owners.
- [ ] Confirm the staging-to-public copy pipeline runs validation tests as a required gate.

## Release Record

- [x] Create a provider-specific release manifest.
- [x] Record the provider name.
- [x] Record the submitted artifact path.
- [x] Record the provider-scoped version tag.
- [x] Record the exact submitted commit SHA.
- [x] Record the submission date.
- [x] Record any submission notes, exceptions, or follow-up requirements.
