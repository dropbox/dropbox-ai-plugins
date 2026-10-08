---
name: upload-to-dropbox
description: Save and upload files or content to Dropbox. Use when the user asks to upload files, save generated content, create files in Dropbox, save chat content, export content to Dropbox, or write new files to their Dropbox account.
disable-model-invocation: false
---

# Upload to Dropbox

Use this skill to save generated content or upload files to Dropbox.

## Tools

- `upload_file`
- `create_folder`
- `file_preview`
- `list_folder`
- `search`

## Workflow

1. Identify what content needs to be saved or uploaded to Dropbox.
2. Determine the destination path. If the user named an exact path, use it. Use `search` or `list_folder` only when the folder is ambiguous.
3. If the destination folder does not exist, confirm the path and create it with `create_folder`. `upload_file` does not create missing parent folders. `create_folder` only creates the last path segment, so create any missing parent first.
4. If the user did not name the file, propose one filename and extension.
5. Before calling `upload_file`, confirm the exact destination path, filename, and content summary with the user.
6. After a successful upload, report that the file was created, including the path and filename. Then call `file_preview` for that file.
7. If `upload_file` returns a name conflict, stop and ask the user before trying another name.
8. If the user wants a shared link, switch to `share-dropbox-content`. Do not create a shared link from this skill.

## Confirmation Required

Before creating a file, confirm:

- Exact destination folder path
- Filename and extension. If the user did not name the file, include the one filename you are proposing.
- Content type and summary of what will be saved

## Output

After a successful upload, return:

- Full file path in Dropbox
- Filename
- Confirmation that the file was created
- File size only when `upload_file` returns it

If `upload_file` returns a name conflict, report the conflict and wait for the user to choose another name.

## Safety

Do not upload without explicit confirmation of the destination path, filename, and content. Do not create a destination folder without confirming the path. Do not assume the destination folder or filename without verifying with the user. Do not retry with a different filename after a name conflict until the user chooses one. Do not create a shared link from this skill. Call `file_preview` only after `upload_file` returns success.

Prefer specific destination folders over generic locations like the user's root folder. When the user's intent for folder structure is unclear, suggest organizing content into topic or project-specific folders.

The `upload_file` tool supports various file types and content. For large files, complex file formats, or bulk file operations, confirm the content type and size are appropriate before proceeding.

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
- The user wants to delete files. Use `clean-up-dropbox-content`.
