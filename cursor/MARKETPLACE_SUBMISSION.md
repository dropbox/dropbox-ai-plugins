# Cursor Marketplace Submission

Use these values when submitting the Dropbox plugin through the Cursor Marketplace publishing flow.

| Field | Value |
| --- | --- |
| Organization name | Dropbox |
| Organization handle | `dropbox` |
| Contact email | `ethanh@dropbox.com` |
| Description | The Dropbox plugin for Cursor connects your Dropbox files directly to Cursor, so you can search, organize, save generated content, and create sharing links without switching tools. It respects your existing Dropbox permissions, and Cursor only works with files you already have access to. |
| GitHub repository | `https://github.com/dropbox/dropbox-ai-plugins/tree/main/cursor` |
| Owner | Team Dropbox |
| Website URL | `https://www.dropbox.com` |

## Submission Checklist

- [ ] Product and Design approve the listing copy.
- [ ] Brand/Legal approve a Dropbox logo and its use; add the approved asset to this directory and reference it with a relative `logo` path in `.cursor-plugin/plugin.json`.
- [ ] Security, Traffic, Product Analytics, and operational owners approve launch readiness.
- [ ] Repository validation tests pass.
- [ ] The plugin loads from `~/.cursor/plugins/local/dropbox/` and Cursor discovers the MCP server and all six skills.
- [ ] Dropbox OAuth, `tools/list`, representative read and write calls, failure cases, logging, and file preview (if supported) are validated through Cursor.
- [ ] The public repository URL and approved listing metadata are submitted at `https://cursor.com/marketplace/publish`.

The logo field intentionally remains unset until an approved asset and usage decision are available.
