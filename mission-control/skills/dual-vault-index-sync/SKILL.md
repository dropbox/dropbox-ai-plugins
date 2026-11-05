---
name: dual-vault-index-sync
description: Maintain the master retrieval registry across Drive and Dropbox in real time. Owner Office - File Vault.
disable-model-invocation: false
---

# Dual Vault Index Sync

## Purpose

Maintain master retrieval registry across Drive and Dropbox.

## Format

`YYYY-MM-DD | PILE | STATUS | TITLE | PATH_OR_ID | NOTES`

## Rules

- Prefer file IDs / ns_path for Dropbox follow-ons.
- Hash-only deletes; rename only after reading PDF body.
- Dropbox MCP cannot upload local PDF binaries — note gaps (see BINARY_GAP_ANALYSIS).
- Sync after filing-pack or quarantine work.
