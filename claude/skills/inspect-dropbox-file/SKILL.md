---
name: inspect-dropbox-file
description: Inspect a Dropbox file or folder by checking metadata, shared links, and file content when needed. Use when the user asks what a file is, whether it is shared, when it changed, what access links exist, or asks to read/analyze a Dropbox file.
disable-model-invocation: false
---

# Inspect Dropbox File

Use this skill to understand a Dropbox file or folder before summarizing, comparing, sharing, restoring, or organizing it.

## Tools

- `get_file_metadata`
- `fetch`
- `file_preview`
- `list_shared_links`
- `get_shared_link_metadata`
- `search`
- `list_folder`

## Workflow

1. Identify the target file or folder from the user request.
2. If the target is ambiguous, use `search` or `list_folder` to find likely matches.
3. Call `get_file_metadata` for the chosen item. Prefer the returned file ID for follow-on calls.
4. If the user asks about content, summary, extraction, or analysis, use `fetch` for files.
5. If the user asks to preview, show, or open the file visually, prefer `file_preview`. When it returns an open-in-Dropbox URL, include that link in the response.
6. If the user explicitly asks for a direct download URL or raw file bytes, stop this skill and switch to `download-dropbox-content` (do not call `download_link` from inspect).
7. If the user asks about version history or rollback options, explain that the current Dropbox MCP tools do not expose revision listing or restore operations.
8. If the user asks about sharing or access, use `list_shared_links`; continue while the response indicates has_more or returns a cursor before claiming the shared-link listing is complete.
9. If the user provides a Dropbox shared link or asks about a specific link, use `get_shared_link_metadata`.

## Output

Summarize only the details relevant to the user request. Include:

- Name and path, preferring path_display when available
- File ID when available
- File or folder type
- Size and modified time when available
- Sharing/link status when relevant, including whether shared-link pagination is complete
- Version-history limitation when relevant
- Fetched content summary or preview guidance when relevant
- Recommended next action, if the user asked for one

## Safety

This is a read-only workflow. Do not create links, change sharing, copy, move, delete, restore content, or generate temporary download URLs. If the user asks for a mutation or a download URL, explain the intended action and switch to the relevant Dropbox skill (`download-dropbox-content` for download URLs).

## Good Triggers

- "What is this Dropbox file?"
- "Summarize this file."
- "Preview this Dropbox file."
- "Check whether this folder is shared."
- "Show me the revision history."
- "When was this document last updated?"

## Do Not Use When

- The user only wants to search or browse. Use `find-dropbox-content`.
- The user wants a temporary download URL. Use `download-dropbox-content`.
- The user wants to create a shared link or invite viewers. Use `share-dropbox-content`.
- The user wants to restore a revision. Explain that recovery is unavailable until the Dropbox restore tool is exposed.
