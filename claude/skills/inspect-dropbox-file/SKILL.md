---
name: inspect-dropbox-file
description: Inspect a Dropbox file or folder by checking metadata and file content when needed. Use when the user asks what a file is, when it changed, or asks to read/analyze a Dropbox file.
---

# Inspect Dropbox File

Use this skill to understand a Dropbox file or folder before summarizing, comparing, sharing, restoring, or organizing it.

## Tools

- `get_file_metadata`
- `fetch`
- `search`
- `list_folder`

## Workflow

1. Identify the target file or folder from the user request.
2. If the target is ambiguous, use `search` or `list_folder` to find likely matches.
3. Call `get_file_metadata` for the chosen item.
4. If the user asks about content, summary, extraction, or analysis, use `fetch` for files.
5. If the user asks about version history or rollback options, explain that the current Dropbox MCP tools do not expose revision listing or restore operations.
6. If the user asks about sharing, access links, or a specific Dropbox shared link, explain that Claude cannot inspect Dropbox shared-link state until those MCP tools are available.

## Output

Summarize only the details relevant to the user request. Include:

- Name and path
- File or folder type
- Size and modified time when available
- Shared-link limitation when relevant
- Version-history limitation when relevant
- Fetched content summary when relevant
- Recommended next action, if the user asked for one

## Safety

This is a read-only workflow. Do not create links, change sharing, copy, move, delete, or restore content. If the user asks for a mutation, explain the intended action and switch to the relevant Dropbox skill.

## Good Triggers

- "What is this Dropbox file?"
- "Summarize this file."
- "Check whether this folder is shared."
- "Show me the revision history."
- "When was this document last updated?"

## Do Not Use When

- The user only wants to search or browse. Use `find-dropbox-content`.
- The user wants to create a shared link. Use `share-dropbox-content`.
- The user wants to inspect existing shared links or add recipients. Explain that Claude cannot inspect or manage shared-link state until the required MCP tools are exposed.
- The user wants to restore a revision. Explain that recovery is unavailable until the Dropbox restore tool is exposed.
