# Dropbox for Cursor

Dropbox for Cursor connects Cursor to your Dropbox account so you can find, inspect, save, download, organize, share, and clean up Dropbox content without leaving Cursor.

Use it to locate files and folders, save generated text content, summarize supported file content, inspect shared-link state, create or reuse shared links, invite viewers by email when requested, collect uploads with file requests, organize folders, and delete content only after explicit review.

## What You Can Do

- Check which Dropbox account or team is connected.
- Search Dropbox for files and folders by name, keyword, type, or location.
- Browse folders and inspect file or folder metadata.
- Save generated text content into Dropbox as new files.
- Read, preview, and summarize supported file content.
- Generate temporary single-use download URLs for files.
- Inspect Dropbox shared links and create or reuse shared links after confirmation.
- Invite viewers by email when creating a shared link.
- Create and inspect Dropbox file requests for collecting uploads.
- Create folders, copy content, move content, and check asynchronous file-operation jobs.
- Delete files or folders only after Cursor presents exact targets and receives explicit confirmation.
- Preview Dropbox content when Cursor supports the MCP file preview resource.

## Included Skills

- `check-dropbox-account`: identify the connected Dropbox account, team, and namespace roots.
- `find-dropbox-content`: search Dropbox and browse folders without changing anything.
- `inspect-dropbox-file`: inspect metadata, shared-link state, previews, and supported file content.
- `download-dropbox-content`: generate temporary single-use download URLs for files.
- `upload-to-dropbox`: save generated text content or create new text files in Dropbox.
- `share-dropbox-content`: create, reuse, or inspect Dropbox shared links and invite viewers by email.
- `collect-files-with-request`: create, inspect, and list Dropbox file requests.
- `organize-dropbox-folder`: create folders, copy, move, or rename content into a cleaner structure.
- `clean-up-dropbox-content`: review and delete Dropbox files or folders with explicit confirmation.


## Skill Reference

For inputs, outputs, and usage examples for every skill, see [`shared/SKILL_REFERENCE.md`](../shared/SKILL_REFERENCE.md).

## Install and Authenticate

1. Install the Dropbox plugin from the Cursor Marketplace. For local testing, copy the `cursor/` directory to `~/.cursor/plugins/local/dropbox/`.
2. Reload Cursor with **Developer: Reload Window**.
3. Confirm Dropbox appears under **Settings > Plugins > Installed** and that the `dropbox` MCP server and all nine skills are available.
4. When Cursor asks for Dropbox access, complete Dropbox OAuth authentication and review the requested permissions before granting access.

The plugin manifest lives at `.cursor-plugin/plugin.json`, and the production Dropbox MCP endpoint is configured in `mcp.json`.

## Required OAuth Scopes

Dropbox for Cursor requires these Dropbox OAuth scopes:

- `account_info.read`: identify the authenticated Dropbox account and support preview flows.
- `files.metadata.read`: search Dropbox, browse folders, and read file or folder metadata.
- `files.content.read`: read supported file content for summaries and extraction.
- `files.content.write`: create folders, create files, copy content, move content, delete content, and check file-operation jobs.
- `sharing.read`: inspect Dropbox shared links.
- `sharing.write`: create Dropbox shared links and invite viewers.
- `file_requests.read`: list and inspect Dropbox file requests.
- `file_requests.write`: create Dropbox file requests.

## Safety

Cursor must confirm write actions before calling write-capable Dropbox tools. That includes creating folders, creating files, creating file requests, creating shared links, inviting viewers, copying, moving, and deleting content.

Deletion workflows require a review list with exact paths or stable identifiers before any Dropbox content is deleted. Organizing workflows should distinguish copy from move, confirm destination paths, and report pending asynchronous jobs when applicable.

Public, anyone-with-the-link, team-wide, and editor links are not created by the Cursor artifact. If a user asks for those link types, Cursor should explain the limitation and offer a private view-only shared link or Dropbox web UI guidance when appropriate.

## Known Limitations

- Public, team-wide, and editor shared links are not available through the current Dropbox MCP tools.
- Binary file upload is not supported through the Cursor artifact; use text-oriented `create_file` workflows or a Dropbox file request instead.
- Revision history and restore workflows are not available until the required Dropbox MCP tools are exposed.
- File content extraction depends on the supported file types and limits of the Dropbox MCP service.
- Some file operations may complete asynchronously and require job-status checks before reporting final results.
- File preview depends on Cursor support for MCP Apps UI resources.

## Example Prompts

- "Which Dropbox account am I connected to?"
- "Find the Q4 planning deck in Dropbox."
- "Summarize this Dropbox file and tell me when it was last modified."
- "Give me a temporary download link for this Dropbox file."
- "Save this summary to my Dropbox Projects folder."
- "Create a shared link for the Launch folder."
- "Share this deck with alice@example.com."
- "Create a Dropbox file request for vendor invoices."
- "Copy final PDFs into the Final folder."
- "Review duplicate exports in this folder and ask before deleting anything."

## Support

- For plugin packaging or documentation problems, open an issue in the [Dropbox AI Plugins repository](https://github.com/dropbox/dropbox-ai-plugins/issues).
- For Dropbox account or product support, visit [Dropbox Support](https://www.dropbox.com/support).
- For Cursor installation or Marketplace problems, visit [Cursor Support](https://cursor.com/support).
