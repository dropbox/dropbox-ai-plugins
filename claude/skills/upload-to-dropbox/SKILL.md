---
name: upload-to-dropbox
description: Save and upload files or content to Dropbox. Use when the user asks to upload files, save generated content, create files in Dropbox, save chat content, export content to Dropbox, or write new files to their Dropbox account.
disable-model-invocation: false
---

# Upload to Dropbox

Use this skill to save generated text content or create new text files in Dropbox.

## Tools

- `create_file`
- `create_folder`
- `list_folder`
- `search`
- `get_file_metadata`
- `file_preview`

## Workflow

1. Identify what text content needs to be saved to Dropbox. Prefer `create_file` for UTF-8 text and code. Do not use this skill for binary uploads such as images, archives, or office files with embedded media; explain that limitation and offer a text export or a Dropbox file request instead when appropriate.
2. Determine the destination folder path. If the user named an exact path, use it. Use `search` or `list_folder` only when the folder is ambiguous.
3. If the destination folder does not exist, confirm the path and create it with `create_folder`. `create_file` does not create missing parent folders. `create_folder` only creates the last path segment, so create any missing parent first.
4. If the user did not name the file, propose one filename and extension that matches the content type.
5. Optionally use `get_file_metadata` when a same-name conflict is likely. If a file already exists, stop and ask whether to use a different filename; do not overwrite.
6. Before calling `create_file`, confirm the exact destination path, filename, and content summary with the user.
7. After a successful create, report that the file was created, including the path_display when available, filename, and file ID.
8. After a successful create, call `file_preview` with the returned file ID when the host supports previews, and include any open-in-Dropbox URL in the response.
9. If `create_file` returns a name conflict, stop and ask the user before trying another name.
10. If create or folder creation fails, report the error with the destination path and ask how to proceed. Do not silently retry with a guessed path.
11. If the user wants a shared link, switch to `share-dropbox-content`. Do not create a shared link from this skill.

## Confirmation Required

Before creating a file, confirm:

- Exact destination folder path
- Filename and extension. If the user did not name the file, include the one filename you are proposing.
- Content type and summary of what will be saved

## Output

After a successful create, return:

- Full file path in Dropbox, preferring path_display when available
- Filename
- File ID when returned
- Confirmation that the file was created
- File size only when the tool returns it
- Open-in-Dropbox link when `file_preview` returns one

If `create_file` returns a name conflict, report the conflict and wait for the user to choose another name.

## Safety

Do not create a file without explicit confirmation of the destination path, filename, and content. Do not create a destination folder without confirming the path. Do not assume the destination folder or filename without verifying with the user. Do not retry with a different filename after a name conflict until the user chooses one. Do not create a shared link from this skill. Prefer returned file IDs for any follow-on Dropbox tool calls.

Prefer specific destination folders over generic locations like the user's root folder. When the user's intent for folder structure is unclear, suggest organizing content into topic or project-specific folders. Do not create files directly in a team root.

## Good Triggers

- "Upload this file to Dropbox"
- "Save this content to my Dropbox"
- "Create a file in Dropbox with this content"
- "Export this to Dropbox"
- "Save our conversation to Dropbox"
- "Put this document in my Dropbox folder"
- "Write this to a file in Dropbox"

## Do Not Use When

- The user wants to collect uploads from other people. Use `collect-files-with-request` to create a file request portal.
- The user wants to move or copy existing Dropbox files. Use `organize-dropbox-folder`.
- The user wants to share existing content. Use `share-dropbox-content`.
- The user wants to find existing files. Use `find-dropbox-content`.
- The user wants to read or inspect existing files. Use `inspect-dropbox-file`.
- The user wants a temporary download URL for an existing file. Use `download-dropbox-content`.
- The user wants to delete files. Use `clean-up-dropbox-content`.
