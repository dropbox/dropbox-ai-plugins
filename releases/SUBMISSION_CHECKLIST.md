# Provider Submission Checklist

Use this checklist before submitting a reviewed provider artifact to a provider marketplace.

## Artifact Package

- [ ] Confirm the provider artifact path is correct: `codex/` for Codex or `claude/` for Claude.
- [ ] Confirm the provider manifest is present and valid JSON.
- [ ] Confirm the MCP configuration is present and points at the intended production MCP endpoint.
- [ ] Confirm no generated, temporary, or local-only test files are included in the submitted artifact.

## Local Validation

- [ ] Run the provider-specific validation flow.
- [ ] Complete OAuth authentication in the provider client.
- [ ] Run a read-only Dropbox smoke test.
- [ ] If write-capable tools are included, validate at least one low-risk write flow in a test account or reviewed test environment.
- [ ] Record any validation notes in the release manifest.

## OAuth And Scopes

- [ ] Confirm the production protected-resource metadata endpoint is reachable.
- [ ] Confirm the protected-resource metadata scope list matches `../shared/OAUTH_SCOPES.md`.
- [ ] Confirm the visible provider tool list matches the tool-to-scope mapping in `../shared/OAUTH_SCOPES.md`.
- [ ] Confirm write scopes are only requested for submitted tools that need write behavior.

## User-Facing Copy

- [ ] Confirm plugin display name, description, short description, long description, keywords, and example prompts have Product and Content Design approval.
- [ ] Confirm capability descriptions accurately describe read and write behavior.
- [ ] Confirm known limitations are documented in provider-appropriate copy.
- [ ] Confirm usage examples are safe, accurate, and approved for launch.

## Security And Privacy

- [ ] Confirm no OAuth client secrets, refresh tokens, access tokens, user identifiers, or private credentials are present.
- [ ] Confirm public-facing docs contain no private repository paths, internal-only URLs, or sensitive implementation details.
- [ ] Confirm Legal, Security, Privacy, Analytics, Product, Content Design, and Engineering reviews are complete.
- [ ] Confirm any third-party dependency license or copyright notices are preserved.

## Pre-Submission Gates

- [ ] Replace all manifest and copy placeholders with approved launch content.
- [ ] Confirm the public repository has branch protection requiring at least two approvals and Dropbox-only push access.
- [ ] Confirm Issues, Discussions, and Wiki are disabled for the public repository unless explicitly approved for launch.
- [ ] Confirm CODEOWNERS covers provider Skill and configuration paths with the required security review owners.
- [ ] Confirm the staging-to-public copy pipeline runs validation tests as a required gate.

## Release Record

- [ ] Create a provider-specific release manifest from `release-manifest.template.json`.
- [ ] Record the provider name.
- [ ] Record the submitted artifact path.
- [ ] Record the provider-scoped version tag.
- [ ] Record the exact submitted commit SHA.
- [ ] Record reviewer names or approval links.
- [ ] Record the provider marketplace point of contact.
- [ ] Record the launch or submission date.
- [ ] Record any submission notes, exceptions, or follow-up requirements.
