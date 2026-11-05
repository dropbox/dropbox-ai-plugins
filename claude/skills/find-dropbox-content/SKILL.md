---
name: find-dropbox-content
description: Find Dropbox files and folders relevant to a user request. Use when the user asks to search Dropbox, find a document, locate recent files, browse a folder, identify likely source files, or narrow down where content lives before reading, sharing, organizing, or restoring it.
disable-model-invocation: false
---

# Find Dropbox Content

Use this skill to locate relevant Dropbox files and folders without changing anything.

## Tools

- `search`
- `list_folder`
- `get_file_metadata`
- `who_am_i`

## Workflow

1. Clarify the search target only if the user request is too broad to act on.
2. Use `who_am_i` when team versus personal namespace context matters for interpreting paths or roots. If identity itself is the question, switch to `check-dropbox-account`.
3. Use `search` for broad keyword, title, file type, or natural-language searches.
4. When the user needs filters, exhaustive paging, or more than the first simplified page, use advanced `search` by including an extra parameter such as max_results, path, file_extensions, file_categories, filename_only, order_by, reverse_order, last_modified_after, or last_modified_before.
5. When `search` returns a cursor and more results are needed, continue with `search` using the cursor only. Do not claim completeness while a cursor remains. For long exhaustive scans, present partial results and ask before continuing many pages.
6. Use `list_folder` when the user names a folder or wants to browse a location. Continue with the returned cursor when more folder results are needed.
7. Use `get_file_metadata` for strong candidates before presenting a final recommendation. When several candidates need enrichment, request those metadata lookups in parallel.
8. Prefer returned file IDs for any follow-on Dropbox tool calls. Prefer path_display when showing paths to the user. Keep namespace paths intact when a tool returns them.
9. If a lookup fails, report the error with the path or file ID that failed and continue with remaining candidates when possible.

## Output

Return the best matches first. For each result, include:

- Name
- Object type: file or folder
- Path or stable identifier, preferring path_display and file ID when available
- Modified time when available
- Why it matched the request
- Any ambiguity, pagination caveat, or confidence caveat

## Safety

Do not create, copy, move, delete, restore, download, or share content. If the user asks to take one of those actions after finding content, switch to the relevant Dropbox skill.

## Good Triggers

- "Find the Q4 planning deck in Dropbox."
- "Search Dropbox for onboarding docs."
- "What files are in this folder?"
- "Find recent PDFs about the launch plan."
- "Where is the customer contract?"
- "List every Markdown file under Projects."

## Do Not Use When

- The user already provided an exact file and wants its content inspected. Use `inspect-dropbox-file`.
- The user wants account or team identity details. Use `check-dropbox-account`.
- The user wants a temporary download URL. Use `download-dropbox-content`.
- The user explicitly asks to create a shared link. Use `share-dropbox-content`.
- The user asks to share with named recipients. Use `share-dropbox-content`.
- The user asks to restore or recover content. Explain that recovery is unavailable until the Dropbox restore tool is exposed.
