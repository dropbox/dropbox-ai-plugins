---
name: save-food-list-to-dropbox
description: Save a generated restaurant or food list to Dropbox as a Markdown file. Use when the user asks to save, export, or upload a food list, restaurant guide, or dining recommendations to Dropbox.
disable-model-invocation: false
---

# Save Food List to Dropbox

Use this skill to persist restaurant lists and food guides produced by `restaurant-list-generator` or `best-restaurant-finder` (or equivalent chat content) into Dropbox.

## Tools

Dropbox MCP tools (require an authenticated Dropbox connection):

- `create_file`
- `create_folder`
- `list_folder`
- `search`
- `get_file_metadata`
- `file_preview`
- `who_am_i` (only when account/namespace context is unclear)

## Default Destination

Prefer a food-mission folder under AI Notes when the user has not named a path:

- `/06_AI_Notes/Food_Mission/`
- Filename pattern: `YYYY-MM-DD__[City]_[Cuisine]_Restaurants.md` (or a clear equivalent)

If that folder may not exist, confirm the path, then create missing parents with `create_folder` (one segment at a time).

## Workflow

1. Identify the Markdown content to save. Prefer the latest completed restaurant list from this chat. Strip ephemeral tool chrome; keep the curated guide body.
2. Determine the destination folder. If the user named an exact path, use it. Otherwise propose `/06_AI_Notes/Food_Mission/` (or the closest existing AI Notes / Food folder found via `search` / `list_folder`).
3. Propose one filename with a `.md` extension that matches city, cuisine, and date.
4. Optionally call `get_file_metadata` when a same-name conflict is likely. If a file already exists, stop and ask whether to use a different filename; do not overwrite.
5. **Before calling `create_file`, confirm** with the user:
   - Exact destination folder path
   - Filename and extension
   - Short content summary (for example "Top 10 Asian restaurants in Santa Clara")
6. Call `create_file` with UTF-8 Markdown text only. Wrap the call in try/catch-style handling and include status code plus destination path in any error message.
7. Prefer returned `id:<file_id>` for follow-on Dropbox calls. Fall back to `ns_path`, then `fq_path` / `path_display` only as a last resort.
8. After success, call `file_preview` with the file ID when the host supports it, and include any open-in-Dropbox URL.
9. If `create_file` returns a name conflict, stop and ask for another name. Do not silently retry with a guessed name.
10. If create or folder creation fails, report the error with the destination path and ask how to proceed.

## Confirmation Required

Before creating a file, confirm:

- Exact destination folder path
- Filename and extension (propose one if the user did not name it)
- Content type and summary of what will be saved

## Output

After a successful create, return:

- Full Dropbox path (`path_display` when available)
- Filename
- File ID when returned
- Confirmation that the file was created
- Open-in-Dropbox link when `file_preview` returns one

## Safety

- Do not create a file or destination folder without explicit confirmation.
- Do not overwrite existing files.
- Do not create shared links from this skill unless the user separately asks to share.
- Do not upload binaries; this skill is Markdown/text only.
- Do not invent Dropbox paths, file IDs, or links.
- Do not create files directly in a team root when a project folder is available.

## Good Triggers

- "Save this restaurant list to Dropbox"
- "Export the food guide to my Dropbox"
- "Upload tonight's dining list"
- "Put this Top 10 in AI Notes"

## Do Not Use When

- The user still needs restaurant research — use `restaurant-list-generator` or `best-restaurant-finder` first.
- The user wants a shared link for an existing Dropbox file — use the Dropbox `share-dropbox-content` skill / `create_shared_link` flow.
- The user wants to collect uploads from other people — use Dropbox file requests.
