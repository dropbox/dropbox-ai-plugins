# Shared Material

This directory is reserved for optional material that is safe and useful for both Claude and Codex artifacts.

Use this directory for shared copy, examples, compatibility notes, or reference material only when both provider artifacts can consume it without provider-specific behavior changes. If provider behavior diverges, keep the content in the provider-specific directory instead.

Provider skill files live only in provider-specific directories. Provider manifests must reference only provider-local skill files whose referenced tools exist for that provider.

- `OAUTH_SCOPES.md` documents the Dropbox OAuth scopes used by the Codex and Claude MCP plugin artifacts.
