---
name: edit-dropbox-paper-document
description: Edit native Dropbox Paper documents through the Dropbox operations catalog. Use when the user asks to change a Paper document's content or tables.
---

# Edit Dropbox Paper Document

Paper capabilities are available as `paper_*` operations in the Dropbox operations catalog, even when no Paper-specific tools appear in the top-level tool list. The catalog provides the available operations, instructions, and input schemas.

## Tools

- `list_dropbox_operations`
- `get_dropbox_operation`
- `run_read_dropbox_operation`
- `run_write_dropbox_operation`

## Workflow

1. Discover Paper operations with `list_dropbox_operations`, then inspect the relevant operation with `get_dropbox_operation` using its exact returned ID. Execute it through the runner specified by the catalog. Operation names are not directly callable tools.
2. For document editing, usually start with `paper_read_document` to obtain current content, revision, edit addresses, and receipts. Follow each operation's requirements and use values from the latest read.
3. Prefer targeted edits for small changes. Reserve `paper_apply_markdown` for populating a new document or a requested major rewrite, since replacing content can lose comment anchors and rich constructs. Follow the plugin's write-action policy before mutations.
4. Re-read to verify changes and before further addressed edits after inserts or deletes. On revision or receipt conflicts, re-read and reconcile concurrent changes before retrying. If a write's outcome is unknown, inspect the current document before retrying.

Creating a .md file or changing its extension to .paper does not create a native Paper document. When creating a document, use the catalog's native creation operation, then read the new document before populating it. If population fails, report the existing document URL and unfinished step rather than creating a second document.

## Output

Return the document title and URL when available, a summary of the changes, and the returned diff. State any failed step or verification limit.
