---
name: auto-file-vault
description: File Vault same-day auto-file — move final packets out of loose Dropbox piles, park finals in vault paths, and flag duplicates for Tam's OK. Use for SCCHA housing piles and Ready_to_sending clutter.
disable-model-invocation: false
---

# Auto-File Vault (ops fix #4 — happening now)

## Problem

Drafts and finals pile loose (e.g. multiple SCCHA packets under `/Pictures of the day/`). File Vault should file the final and flag duplicates the same day.

## Workflow (same day)

1. **Find** loose candidates — Dropbox `search` by matter keywords (SCCHA, Form 998, Diversified, packet names).
2. **Classify** — Draft vs Final vs Duplicate (size + name + modified time; prefer newest complete packet as Final candidate).
3. **Propose file plan** — destination under Housing / VA / Finance vault paths; never auto-delete.
4. **Flag for OK** — Decision Board or Team Task Board card: "File these / trash or archive these duplicates?"
5. **On Tam yes** — Dropbox `move` / `copy` into vault; leave README stub in old location if needed.
6. **Index** — run `dual-vault-index-sync` line for each filed item.

## Known mess (example)

SCCHA response packets loose in `/Pictures of the day/` alongside proper paths under `/02_Personal/Housing/…`. Prefer Housing vault for finals; flag Pictures copies as duplicates.

## Tools

- **Dropbox** `search`, `list_folder`, `get_file_metadata`, `move`, `copy`, `create_folder`, `create_file` (notes only)
- Local Dropbox plugin skills: `find-dropbox-content`, `organize-dropbox-folder`, `clean-up-dropbox-content`, `inspect-dropbox-file`
- Companion skills: `dual-vault-index-sync`, `personal-credential-quarantine`, `silver-platter-filing-pack`
- **Notion** Decision Board / Team Task Board for same-day OK

## Rules

- Ready_to_sending stays **DRAFT-ONLY** until SEND — auto-file does not mean send.
- Quarantine credentials/SSN before any share path.
- Prefer `id:<file_id>` then `ns_path` for all Dropbox mutations.
- Never permanent-delete; move to Deleted files only with explicit OK.
- Do not invent exhibit lists or filings.
