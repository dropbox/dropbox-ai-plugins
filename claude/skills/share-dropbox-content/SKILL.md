---
name: share-dropbox-content
description: Share Dropbox files or folders by creating shared links. Use only when the user explicitly asks to create a shared link to Dropbox content.
---

# Share Dropbox Content

Use this skill to create Dropbox shared links for files or folders.

## Tools

- `create_shared_link`
- `get_file_metadata`
- `search`
- `list_folder`

## Workflow

1. Identify the target file or folder.
2. If the target is ambiguous, use `search` or `list_folder` and ask the user to choose.
3. Use `get_file_metadata` to confirm the exact target.
4. Before calling `create_shared_link`, summarize the exact sharing plan and ask for explicit confirmation.
5. After sharing, report the resulting URL and any warnings or partial failures.
6. If the user asks to inspect existing shared links, check access, or inspect a specific Dropbox shared link, explain that Claude cannot inspect Dropbox shared-link state until those MCP tools are available.
7. If the user asks to add viewers, add recipients, or share directly with named people, explain that recipient-sharing is unavailable until those MCP tools are available. Offer to create a shared link instead when appropriate.

## Confirmation Required

Before creating a shared link, confirm:

- Exact target file or folder
- Link/access settings requested by the user, if supported
- Any known access implications

## Output

After a successful action, include:

- Shared link URL
- Whether the link was newly created or reused, if the tool reports it
- Any effective access settings reported by the tool
- Any warning that the tool reports

## Safety

Never create a link automatically after finding, downloading, or creating content. Do not claim access was granted to named recipients or viewers; recipient-sharing tools are not available.

## Good Triggers

- "Create a share link for this Dropbox folder."
- "Create a link to this file."
- "Send me a share link for the launch deck."

## Do Not Use When

- The user only wants to find a file. Use `find-dropbox-content`.
- The user only wants metadata or content summary. Use `inspect-dropbox-file`.
- The user wants to collect uploads from others. Explain that Claude file-request collection is unavailable until the required MCP tools are exposed.
- The user wants to add viewers or share directly with named recipients. Explain that recipient-sharing is unavailable until the required MCP tools are exposed.
