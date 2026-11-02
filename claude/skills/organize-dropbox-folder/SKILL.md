---
name: organize-dropbox-folder
description: Organize Dropbox files and folders by creating folders, copying content, moving content, or renaming items into a cleaner structure. Use when the user asks to organize, archive, consolidate, restructure, copy, move, or rename Dropbox content.
disable-model-invocation: false
---

# Organize Dropbox Folder

Use this skill to safely organize Dropbox content through folder creation, copying, moving, and renaming.

## Tools

- `list_folder`
- `search`
- `get_file_metadata`
- `create_folder`
- `copy`
- `move`
- `check_job_status`

## Workflow

1. Understand the desired organization goal and target scope.
2. Use `list_folder` or `search` to inventory the relevant content.
3. Resolve metadata for candidates before mutating. When several items need metadata, request those lookups in parallel rather than one by one. Prefer returned file IDs for follow-on mutation calls.
4. Draft a proposed change plan before any mutation. For renames, treat the operation as a `move` to a new name in the same parent folder.
5. If needed, create destination folders with `create_folder` after confirmation. Create missing parents from the top down; `create_folder` only creates the final segment.
6. Batch related `copy` or `move` entries in one tool call when the user confirmed the full set. Use autorename only when the user explicitly wants conflict renaming.
7. Use `copy` when preserving the original location matters or when the user says copy/duplicate.
8. Use `move` when the user explicitly wants content relocated, archived, or renamed.
9. Use `check_job_status` for any asynchronous copy or move job until it completes or must be reported as pending. Respect recommended poll delays; do not poll in a tight loop.
10. After changes, summarize all created, copied, moved, renamed, and pending paths. Prefer path_display in user-facing results.
11. On per-entry failures, report the failed entry with the error code or message and the path or file ID. Do not blindly retry the entire batch. Ask how to proceed for the failed entries only.

## Confirmation Required

Before any mutation, confirm:

- Source paths or file IDs
- Destination paths or new names
- Whether the operation is copy, move, or rename
- Whether destination folders should be created
- Whether autorename is allowed on conflicts
- Expected result after the operation

## Output

Before mutation, present a plan:

- Folders to create
- Files or folders to copy
- Files or folders to move or rename
- Items that need clarification

After mutation, report:

- Successfully created folders
- Successfully copied items
- Successfully moved or renamed items
- Pending jobs and current status when relevant
- Any failures or skipped items, including error details and path or file ID

## Safety

Prefer copy over move when the user intent is ambiguous. Do not move shared folders or high-level team folders without extra confirmation. Do not delete anything; use `clean-up-dropbox-content` only when deletion is explicitly requested.

## Good Triggers

- "Organize these files into folders by client."
- "Archive last year's project folder."
- "Copy these assets into the launch folder."
- "Move all final PDFs into the Final folder."
- "Rename draft-v3.pdf to launch-brief.pdf."

## Do Not Use When

- The user only wants to search or inspect content. Use `find-dropbox-content` or `inspect-dropbox-file`.
- The user asks to delete content. Use `clean-up-dropbox-content`.
- The user asks to restore content. Explain that recovery is unavailable until the Dropbox restore tool is exposed.
