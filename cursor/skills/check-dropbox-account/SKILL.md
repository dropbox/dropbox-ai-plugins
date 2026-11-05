---
name: check-dropbox-account
description: Identify the connected Dropbox account, team context, and namespace roots. Use when the user asks who is signed in, which Dropbox account or team is connected, where the home or root namespace is, or when path roots are ambiguous before other Dropbox work.
disable-model-invocation: false
---

# Check Dropbox Account

Use this skill to establish Dropbox identity and namespace context before searching, saving, sharing, or organizing content.

## Tools

- `who_am_i`

## Workflow

1. Call `who_am_i` to retrieve the connected account identity, team context when present, and namespace root information.
2. Summarize only the details needed for the user request.
3. If the user asked because a path was ambiguous, explain whether the next action should use the personal home namespace or a team namespace, then switch to the relevant Dropbox skill.
4. Do not invent account, team, or namespace values. If the tool fails, report the failure clearly and ask the user to re-authenticate if needed.

## Output

Return:

- Display name when available
- Account identifier when available
- Email when available
- Team name or team context when available
- Home or root namespace guidance relevant to the next action
- Any authentication or permission error with enough detail to act on it

## Safety

This is a read-only identity workflow. Do not create, move, share, download, or delete content from this skill.

## Good Triggers

- "Which Dropbox account am I connected to?"
- "Am I on a Dropbox team?"
- "What is my Dropbox home path?"
- "Why are these team folder paths failing?"

## Do Not Use When

- The user wants to search files. Use `find-dropbox-content`.
- The user wants file metadata or content. Use `inspect-dropbox-file`.
- The user wants to change files or sharing. Use the relevant write skill after confirming identity if needed.
