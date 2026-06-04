# Dropbox AI Plugins

This repository contains Dropbox's AI plugin artifacts for Claude and OpenAI Codex.

## Repository Layout

- `claude/` contains the Claude MCP Host artifact for Claude Code and Claude Cowork.
- `codex/` contains the Codex MCP Host artifact.
- `shared/` contains shared reference material, including OAuth scope documentation.

## MCP Host Artifacts

Use the MCP Host-specific directory for setup instructions, capabilities, known limitations, plugin metadata, and Skills.

- Claude: start with `claude/README.md`.
- Codex: start with `codex/README.md`.
- OAuth scopes: see `shared/OAUTH_SCOPES.md`.

## Authentication And Scopes

The plugin artifacts use Dropbox OAuth. The current OAuth scope inventory and tool-to-scope mapping are documented in `shared/OAUTH_SCOPES.md`.

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
