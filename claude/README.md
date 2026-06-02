# Claude Artifact

This directory contains the Dropbox Claude provider artifact for Claude Code and Claude Cowork.

The artifact includes Claude-specific plugin metadata, Skills, provider examples, and Claude-only supporting material. Its MCP configuration points at the Dropbox Claude MCP endpoint.

Use `plugin.json` for Claude plugin metadata and `skills/` for Claude-specific `SKILL.md` files. Keep provider-specific content in this directory, and put only safe cross-provider reference material in `../shared/`.

Before provider submission, complete Product, Content Design, Legal, Security, Analytics, and Engineering review, then record the submitted artifact path, version tag, and commit SHA under `../releases/`.
