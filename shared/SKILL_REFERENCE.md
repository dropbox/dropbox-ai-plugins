# Dropbox Skill Reference

Shared documentation for Dropbox AI plugin skills. Host packages may expose a subset of these skills; Codex also keeps a host-specific `upload-to-dropbox` variant that uses `upload_file`.

## check-dropbox-account

- **Inputs:** optional question about account, team, or namespace roots.
- **Outputs:** display name, account identifier, email when available, team context, and home or root namespace guidance.
- **Example:** `Which Dropbox account am I connected to?`

## find-dropbox-content

- **Inputs:** search query or folder path; optional filters such as extensions, categories, path scope, and modified-time bounds.
- **Outputs:** ranked matches with name, type, path_display or file ID, modified time when available, and pagination caveats.
- **Example:** `Find recent PDFs about the launch plan under /Projects.`

## inspect-dropbox-file

- **Inputs:** file or folder path, file ID, or shared link; whether the user wants metadata, text summary, preview, or sharing state.
- **Outputs:** metadata summary, content summary when fetched, preview or open-in-Dropbox guidance, and shared-link state when requested.
- **Routing:** Temporary download URLs are out of scope — switch to `download-dropbox-content` (do not call `download_link` from this skill).
- **Example:** `Summarize this Dropbox file and tell me when it was last modified.`

## download-dropbox-content

- **Inputs:** exact file path or file ID. Folders, Paper docs, and Cloud Docs are unsupported.
- **Outputs:** temporary single-use download URL plus file name, path_display, and file ID. Treat the URL as sensitive and short-lived.
- **Example:** `Give me a temporary download link for this Dropbox file.`

## upload-to-dropbox

- **Inputs:** content to save, destination folder, filename and extension, and confirmation that parents may be created.
- **Outputs:** created file path_display, filename, file ID, size when returned, and preview or open-in-Dropbox link when available.
- **Host note:** Cursor, Claude, and Antigravity use `create_file` for UTF-8 text. Codex uses `upload_file` for broader file uploads.
- **Example:** `Save this summary to my Dropbox Projects folder as launch-notes.md.`

## share-dropbox-content

- **Inputs:** target file or folder; optional viewer emails; optional password, expiry, or download settings when supported.
- **Outputs:** shared link URL, created-or-reused status, effective access settings, invited viewers, and any warnings or share errors.
- **Example:** `Share this deck with alice@example.com and send me the link.`

## collect-files-with-request

- **Inputs:** request title, destination child folder, optional deadline, and open/closed state.
- **Outputs:** request URL, title, destination, status, deadline when set, and any follow-up the user must take.
- **Example:** `Create a Dropbox file request for vendor invoices in /Finance/Invoices.`

## organize-dropbox-folder

- **Inputs:** source items, destination paths or new names, copy/move/rename choice, autorename preference, and whether destination folders should be created.
- **Outputs:** created folders, copied, moved, or renamed items, pending async job status, and failed or skipped entries with error details.
- **Example:** `Rename draft-v3.pdf to launch-brief.pdf and copy final PDFs into the Final folder.`

## clean-up-dropbox-content

- **Inputs:** cleanup scope, explicit deletion candidates, and optional preserve-copy destination.
- **Outputs:** review list before delete; after delete, copied, deleted, pending, failed, and skipped items.
- **Example:** `Review duplicate exports in this folder and ask before deleting anything.`
