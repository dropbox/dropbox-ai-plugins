# Dropbox for Codex

Dropbox for Codex connects Codex to your Dropbox account so you can find, inspect, organize, share, and clean up Dropbox content from a Codex session.

Use it to locate files and folders, summarize supported file content, inspect shared-link state, create or reuse shared links, collect uploads with file requests, organize folders, and delete content only after explicit review.

## What You Can Do

- Search Dropbox for files and folders by name, keyword, type, or location.
- Browse folders and inspect file or folder metadata.
- Read and summarize supported file content.
- Inspect Dropbox shared links and create or reuse shared links after confirmation.
- Create and inspect Dropbox file requests for collecting uploads.
- Create folders, copy content, move content, and check asynchronous file-operation jobs.
- Delete files or folders only after Codex presents exact targets and receives explicit confirmation.

## Included Skills

- `find-dropbox-content`: search Dropbox and browse folders without changing anything.
- `inspect-dropbox-file`: inspect metadata, shared-link state, and supported file content.
- `share-dropbox-content`: create, reuse, or inspect Dropbox shared links.
- `collect-files-with-request`: create, inspect, and list Dropbox file requests.
- `organize-dropbox-folder`: create folders, copy content, and move content into a cleaner structure.
- `clean-up-dropbox-content`: review and delete Dropbox files or folders with explicit confirmation.

## Setup

1. Install the Dropbox plugin in Codex.
2. When Codex asks for Dropbox access, complete Dropbox OAuth authentication.
3. Review the requested permissions before granting access.
4. Ask Codex to search, inspect, share, collect, organize, or clean up Dropbox content.

The plugin manifest lives at `.codex-plugin/plugin.json`, and the production Dropbox MCP endpoint is configured in `.mcp.json`.

## Required OAuth Scopes

Dropbox for Codex requires these Dropbox OAuth scopes:

- `account_info.read`: identify the authenticated Dropbox account and support preview flows.
- `files.metadata.read`: search Dropbox, browse folders, and read file or folder metadata.
- `files.content.read`: read supported file content for summaries and extraction.
- `files.content.write`: create folders, create files, copy content, move content, delete content, and check file-operation jobs.
- `sharing.read`: inspect Dropbox shared links.
- `sharing.write`: create Dropbox shared links.
- `file_requests.read`: list and inspect Dropbox file requests.
- `file_requests.write`: create Dropbox file requests.

## Safety

Codex must confirm write actions before calling write-capable Dropbox tools. That includes creating folders, creating file requests, creating shared links, copying, moving, and deleting content.

Deletion workflows require a review list with exact paths or stable identifiers before any Dropbox content is deleted. Organizing workflows should distinguish copy from move, confirm destination paths, and report pending asynchronous jobs when applicable.

The Codex artifact does not grant access to named recipients or manage viewer lists. If a user asks to share directly with specific people, Codex should explain that recipient-sharing is unavailable and offer a shared link when appropriate.

## Known Limitations

- Recipient-based sharing and viewer management are not available until the required Dropbox MCP tools are exposed.
- Revision history and restore workflows are not available until the required Dropbox MCP tools are exposed.
- File content extraction depends on the supported file types and limits of the Dropbox MCP service.
- Some file operations may complete asynchronously and require job-status checks before reporting final results.

## Example Prompts

- "Find the Q4 planning deck in Dropbox."
- "Summarize this Dropbox file and tell me when it was last modified."
- "Create a shared link for the Launch folder."
- "Create a Dropbox file request for vendor invoices."
- "Copy final PDFs into the Final folder."
- "Review duplicate exports in this folder and ask before deleting anything."
