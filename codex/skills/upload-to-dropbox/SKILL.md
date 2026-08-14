---
name: upload-to-dropbox
description: Save and upload files or content to Dropbox. Use when the user asks to upload files, save generated content, create files in Dropbox, save chat content, export content to Dropbox, or write new files to their Dropbox account.
disable-model-invocation: false
---

# Upload to Dropbox

Use this skill to save generated content or upload files to Dropbox.

## Tools

- `create_file`
- `create_folder`
- `list_folder`
- `search`
- `get_file_metadata`

## Workflow

1. Identify what content needs to be saved or uploaded to Dropbox.
2. Determine the target destination folder path.
3. If the destination is ambiguous or not specified, ask the user to confirm the target location.
4. Use `search` or `list_folder` to verify the destination folder exists and is accessible.
5. If the destination folder does not exist, ask the user whether to create it before proceeding.
6. Use `create_folder` only after explicit confirmation when a new folder is needed.
7. Determine the target filename. If not specified, suggest a descriptive filename with appropriate extension based on content type.
8. Check if a file with the same name already exists at the destination using `get_file_metadata`.
9. If a file exists, ask the user whether to overwrite, create a new version, or use a different filename.
10. Before calling `create_file`, confirm the exact destination path, filename, and content summary with the user.
11. After successful upload, report the file path and offer to create a shared link if appropriate.

## Confirmation Required

Before creating a file, confirm:

- Exact destination folder path
- Target filename and extension
- Content type and summary of what will be saved
- Handling of naming conflicts if a file already exists
- Whether the destination folder should be created if it does not exist

Before creating a destination folder, confirm:

- Exact folder path
- Whether parent folders already exist
- That the folder is not a team root or the user's personal root without a child folder

## Output

After a successful upload, return:

- Full file path in Dropbox
- Filename and file size when available
- Confirmation that the file was created or updated
- Whether any folders were created as part of the operation
- Offer to create a shared link or perform additional actions

## Safety

Do not create files or folders without explicit confirmation. Do not assume the destination folder or filename without verifying with the user. When naming conflicts exist, never silently overwrite without user approval.

Prefer specific destination folders over generic locations like the user's root folder. When the user's intent for folder structure is unclear, suggest organizing content into topic or project-specific folders.

The `create_file` tool is designed for text-oriented content. For large binary files, complex file formats, or bulk file operations, confirm the content type and size are appropriate before proceeding.

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
