# Shared Material

This directory is reserved for optional material that is safe and useful for both Claude and Codex artifacts.

Use this directory for shared copy, examples, compatibility notes, or reference material only when both MCP Host artifacts can consume it without MCP Host-specific behavior changes. If MCP Host behavior diverges, keep the content in the MCP Host-specific directory instead.

MCP Host skill files live only in MCP Host-specific directories. MCP Host manifests must reference only MCP Host-local skill files whose referenced tools exist for that MCP Host.

- `OAUTH_SCOPES.md` documents the Dropbox OAuth scopes used by the Codex and Claude MCP plugin artifacts.
