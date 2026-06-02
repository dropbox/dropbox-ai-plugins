# OAuth Scopes

This document records the Dropbox OAuth scopes used by the Dropbox MCP plugin artifacts for Codex and Claude.

## Provider Surfaces

| Provider artifact | MCP endpoint | Protected resource metadata |
| --- | --- | --- |
| Codex | `https://mcp.dropbox.com/chatgpt_app_mcp` | `https://mcp.dropbox.com/.well-known/oauth-protected-resource/chatgpt_app_mcp` |
| Claude | `https://mcp.dropbox.com/claude_app_mcp` | `https://mcp.dropbox.com/.well-known/oauth-protected-resource/claude_app_mcp` |

The OAuth authorization server is Dropbox. The plugin artifacts must not include OAuth client secrets, refresh tokens, or user tokens.

## Scope Summary

| Scope | Capability enabled | Codex | Claude |
| --- | --- | --- | --- |
| `account_info.read` | Identify the authenticated account and support file preview resources. | Yes | Yes |
| `files.metadata.read` | Search, list folders, and read file or folder metadata. | Yes | Yes |
| `files.content.read` | Fetch file text content and generate download metadata. | Yes | Yes |
| `files.content.write` | Create files, create folders, move files, copy files, delete files, and check async file-operation jobs. | Yes | Yes |
| `sharing.read` | List shared links and read shared-link metadata. | Yes | No |
| `sharing.write` | Create shared links. | Yes | Yes |
| `file_requests.read` | List and inspect file requests. | Yes | No |
| `file_requests.write` | Create file requests. | Yes | No |

## Codex Tool Scope Mapping

The Codex artifact points at `chatgpt_app_mcp`.

| Tool | Required scope | Notes |
| --- | --- | --- |
| `search` | `files.metadata.read` | Read-only search over Dropbox file metadata. |
| `list_folder` | `files.metadata.read` | Read-only folder listing. |
| `get_file_metadata` | `files.metadata.read` | Read-only metadata lookup. |
| `get_shared_link_metadata` | `sharing.read` | Read-only shared-link metadata lookup. |
| `who_am_i` | `account_info.read` | Read-only account identity check. |
| `list_shared_links` | `sharing.read` | Read-only shared-link listing. |
| `list_file_requests` | `file_requests.read` | Read-only file-request listing. |
| `get_file_request` | `file_requests.read` | Read-only file-request lookup. |
| `create_file_request` | `file_requests.write` | Creates a Dropbox file request. |
| `fetch` | `files.content.read` | Reads extracted text content from a file. |
| `download_link` | `files.content.read` | Creates download metadata for file access. |
| `file_preview` | `account_info.read` | Reads preview metadata and preview-resource context. |
| `create_folder` | `files.content.write` | Creates a Dropbox folder. |
| `create_file` | `files.content.write` | Creates a text-oriented Dropbox file. |
| `create_shared_link` | `sharing.write` | Creates or reuses a shared link. |
| `move` | `files.content.write` | Moves Dropbox content. |
| `copy` | `files.content.write` | Copies Dropbox content. |
| `delete` | `files.content.write` | Deletes Dropbox content. |
| `check_job_status` | `files.content.write` | Checks async file-operation job status. |

## Claude Tool Scope Mapping

The Claude artifact points at `claude_app_mcp`.

| Tool | Required scope | Notes |
| --- | --- | --- |
| `search` | `files.metadata.read` | Read-only search over Dropbox file metadata. |
| `list_folder` | `files.metadata.read` | Read-only folder listing. |
| `get_file_metadata` | `files.metadata.read` | Read-only metadata lookup. |
| `fetch` | `files.content.read` | Reads extracted text content from a file. |
| `file_preview` | `account_info.read` | Reads preview metadata and preview-resource context. |
| `create_folder` | `files.content.write` | Creates a Dropbox folder. |
| `create_file` | `files.content.write` | Creates a text-oriented Dropbox file. |
| `create_shared_link` | `sharing.write` | Creates or reuses a shared link. |

## Release Review Checklist

Before provider submission:

- Confirm the scope list against each production protected-resource metadata endpoint.
- Confirm each provider's visible tool list still matches the tool-to-scope tables above.
- Confirm all write-capable tools have user-facing descriptions that make the write behavior clear.
- Confirm the submitted plugin metadata describes both read and write capabilities.
- Confirm no OAuth client secrets, refresh tokens, access tokens, or user identifiers are included in the submitted artifact.
- Record the submitted commit SHA in `releases/release-manifest.template.json` or the provider-specific release manifest created from it.

## Known Scope Limitations

- The Claude surface intentionally exposes a smaller tool set than the Codex surface.
- Scope support follows the registered MCP tool inventory. Adding or removing a tool can change the protected-resource metadata scope list.
- `account_info.read` is included even when the visible user action is not an account lookup because identity and preview-resource flows require account context.
- Read scopes do not allow creating, moving, deleting, or sharing Dropbox content.
- Write scopes are required before the provider can create files, folders, links, or file requests.
