# Dropbox AI Plugins

This repository contains Dropbox's MCP Host-specific AI plugin artifacts for Claude and OpenAI Codex.

Claude and Codex require different packaging, metadata, and submission flows, so their artifacts are maintained separately. Shared material is kept small and only used when it is safe and accurate for both MCP Hosts.

## Repository Layout

- `claude/` contains the Claude MCP Host artifact for Claude Code and Claude Cowork.
- `codex/` contains the Codex MCP Host artifact.
- `shared/` contains MCP Host-neutral reference material, including shared OAuth scope documentation.
- `releases/` contains release records and MCP Host submission checklists.

## MCP Host Artifacts

Use the MCP Host-specific directory for setup instructions, capabilities, known limitations, plugin metadata, and Skills.

- Claude: start with `claude/README.md`.
- Codex: start with `codex/README.md`.
- OAuth scopes: see `shared/OAUTH_SCOPES.md`.

Each MCP Host artifact owns its manifest/configuration, Skills, README, examples, and marketplace submission metadata. MCP Host-specific content should stay in the MCP Host directory. Shared content should only live under `shared/` when both MCP Host artifacts can use it without changing meaning or behavior.

## Authentication And Scopes

The plugin artifacts use Dropbox OAuth. Do not add OAuth client secrets, refresh tokens, access tokens, or user tokens to this repository.

The current OAuth scope inventory and tool-to-scope mapping are documented in `shared/OAUTH_SCOPES.md`. Review that file before each MCP Host submission and whenever the visible tool list changes.

## Release Process

Claude and Codex artifacts are versioned independently with MCP Host-scoped tags:

- Claude tags use `claude-vX.Y.Z`.
- Codex tags use `codex-vX.Y.Z`.

Each MCP Host submission should have a completed release manifest under `releases/` recording the MCP Host, artifact path, version tag, submitted commit SHA, submission date, and submission notes.

Use `releases/SUBMISSION_CHECKLIST.md` before submitting an artifact to an MCP Host marketplace.

## Security And Privacy

This repository is intended to be public. Do not add secrets, credentials, private repository paths, private URLs, internal-only documentation, unreleased endpoint details, or sensitive implementation references.

All write-capable tools and examples must make their write behavior clear to users. MCP Host endpoint configuration must point only at reviewed production endpoints.

## Reviews

Before MCP Host submission, each artifact should complete Product, Content Design, Legal, Security, Analytics, and Engineering review.

The submitted artifact path, version tag, commit SHA, and submission date should be recorded in the MCP Host release manifest under `releases/`.

## License

Unless otherwise noted:

    Copyright (c) 2026 Dropbox, Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
