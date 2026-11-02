---
name: download-dropbox-content
description: Get temporary Dropbox download links for files. Use when the user asks to download a Dropbox file, get a direct download URL, export raw file bytes, or fetch a one-time download link.
disable-model-invocation: false
---

# Download Dropbox Content

Use this skill to generate short-lived, single-use download URLs for Dropbox files.

## Tools

- `download_link`
- `get_file_metadata`
- `search`
- `list_folder`
- `file_preview`

## Workflow

1. Identify the target file. Folders, Paper docs, and Cloud Docs are not supported by `download_link`.
2. If the target is ambiguous, use `search` or `list_folder` and ask the user to choose.
3. Call `get_file_metadata` to confirm the exact file. Prefer the returned file ID for follow-on calls.
4. If the user mainly wants a visual preview or Open in Dropbox experience, prefer `file_preview` instead of a download URL.
5. Call `download_link` only when the user explicitly wants a direct download URL or raw file bytes outside preview or text extraction. When the user confirmed multiple files, request those download links in parallel.
6. Treat returned download URLs as sensitive, short-lived, and single-use. Do not store them in long-lived docs or shared notes unless the user asks.
7. If a download-link call fails, report the error with the path or file ID and continue with any remaining confirmed files.
8. If the user also wants durable sharing, switch to `share-dropbox-content` for a shared link.

## Output

Return:

- File name
- Path, preferring path_display when available
- File ID when available
- Temporary download URL
- Clear note that the URL is short-lived and single-use

## Safety

Do not generate download links for folders. Do not convert a preview request into a download link unless the user asks for a download URL. Do not create shared links from this skill. Prefer file IDs over reconstructed display paths.

## Good Triggers

- "Give me a download link for this Dropbox file."
- "Download the Q4 planning deck."
- "Get a temporary URL so I can fetch this file."
- "Export the raw bytes for this Dropbox PDF."

## Do Not Use When

- The user wants extracted text or a summary. Use `inspect-dropbox-file`.
- The user wants a durable share link. Use `share-dropbox-content`.
- The user only wants to find a file. Use `find-dropbox-content`.
- The user wants other people to upload files. Use `collect-files-with-request`.
