---
name: share-dropbox-content
description: Share Dropbox files or folders by creating shared links, inviting viewers by email when supported, inspecting existing shared links, or explaining current shared-link state. Use only when the user explicitly asks to create a shared link, invite viewers, check access, or inspect a Dropbox shared link.
disable-model-invocation: false
---

# Share Dropbox Content

Use this skill to create or inspect Dropbox shared links, invite viewers by email when requested, and explain shared-link state.

## Tools

- `create_shared_link`
- `list_shared_links`
- `get_shared_link_metadata`
- `get_file_metadata`
- `search`
- `list_folder`

## Workflow

1. Identify the target file or folder.
2. If the target is ambiguous, use `search` or `list_folder` and ask the user to choose.
3. Use `get_file_metadata` to confirm the exact target. Prefer the returned file ID for follow-on calls.
4. Use `list_shared_links` when checking current sharing state or before creating a new link if existing links matter; continue while the response indicates has_more or returns a cursor before treating the existing-link state as complete.
5. Use `get_shared_link_metadata` when the user provides or asks about a specific shared link.
6. Before calling `create_shared_link`, summarize the exact sharing plan and ask for explicit confirmation. Include any viewer emails the user asked to invite.
7. When the user asks to share with named people, pass their emails to `create_shared_link` as viewers. Do not invent email addresses.
8. After sharing, report the resulting URL, whether the link was created or reused, effective access settings, invited viewers, and any warnings or share errors. When member addition partially fails, list successful invites and share_errors separately.
9. If a share call fails, report the error code or message with the target path or file ID and ask how to proceed. Do not retry repeatedly on permission or policy errors.
10. If the user asks for a public, anyone-with-the-link, team-wide, or editor link, explain that this tool creates private view-only links and that broader link types must be managed in the Dropbox web UI.

## Confirmation Required

Before creating a shared link, confirm:

- Exact target file or folder
- Viewer emails to invite, when requested
- Link/access settings requested by the user
- Expiration, password, or download settings when supported

## Output

After a successful action, include:

- Shared link URL
- Whether the link was newly created or reused
- Effective access settings
- Viewers successfully invited, when applicable
- Any share errors or warning that existing link settings differ from requested settings
- Whether shared-link pagination was complete when existing links were checked
- How to revoke or manage sharing in Dropbox when relevant

## Safety

Never create a link automatically after finding, downloading, or creating content. Only invite viewers the user explicitly named. Do not claim public or team-wide access was granted. Prefer file IDs over reconstructed display paths for tool calls.

## Good Triggers

- "Create a share link for this Dropbox folder."
- "Create a link to this file."
- "Share this deck with alice@example.com."
- "Check who can access this Dropbox link."
- "Send me a share link for the launch deck."

## Do Not Use When

- The user only wants to find a file. Use `find-dropbox-content`.
- The user only wants metadata or content summary. Use `inspect-dropbox-file`.
- The user wants to collect uploads from others. Use `collect-files-with-request`.
