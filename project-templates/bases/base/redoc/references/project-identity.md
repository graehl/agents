# Project-local identity ownership

The root `.project-identity.json` records deliberate **post-creation** human
naming/description edits. It is authoritative for preservation outside YA as
well as inside it. Do not consult a private YA data directory as a substitute.
Create it only when a protected edit occurs; initial setup and automatic agent
refinement do not create protection. A project may exclude the file from Git
without changing its local meaning.

Version 1 has optional `name` and `description` entries:

```json
{
  "formatVersion": 1,
  "name": {
    "humanText": "Garden notes",
    "editedAt": "2026-09-21T12:00:00Z"
  },
  "description": {
    "humanText": "A place for our experiments, mistakes, and discoveries.",
    "editedAt": "2026-09-21T12:00:00Z",
    "agentCoda": " Includes a searchable collection and illustrated notes."
  }
}
```

An absent entry is unprotected. An entry's presence marks its exact
`humanText` as protected, including punctuation, case, Unicode and whitespace.
`editedAt` is the actual human-edit time, not the last agent refresh. JSON
escaping may differ; the decoded string must remain identical. For Markdown
prose, preserve the literal prefix rather than rewrapping or normalizing it.

The effective description is `humanText + agentCoda`. The coda owns its leading
separator; it may be empty, replaced or removed as behavior changes. Never
grow a history of obsolete codas. Names have no coda: use the protected name
verbatim in descriptive name/title locations. Formatting syntax surrounding a
title or serialized string is not part of the protected text.

YA must write this file when its user deliberately changes a project name or
caption after creation, including for imported/non-template projects. The
caption editor edits the human portion separately from the agent coda. When
the first protected description is recorded, start with an empty coda; never
append the entire old derived caption. Later human edits replace the human
portion only; an explicit reset may remove its protection. Keep name and
description ownership independent. YA integration is separately implemented;
do not assume a private caption override already produced this file.

YA's UI records this marker after a deliberate later edit. Redoc consumes it;
it does not infer or create protected authorship from existing prose, Git
history or ordinary doc revision. Initial creation intent remains provisional
even if supplied verbatim by the user. A user can explicitly request a marker
change or supply another revision procedure, but direct README edits do not
automatically become protected regions. This is an identity exception, not a
general document-authorship ledger.

Read the file afresh before writing. Preserve unrelated entries, refuse a
malformed or unsupported version for identity edits, and do not replace a
concurrent human edit with an older snapshot. Agents never clear
protection or change `humanText` merely to make documentation more accurate;
append truthful current context or ask the user to resolve the contradiction.
Write the record and its documented projections as one reviewable change.

The marker does not mean a machine package name is a display name. Keep
`package.json` `name`, import paths and distribution identifiers unchanged
unless the user separately requested that rename. Existing manifest
`description` fields may carry the protected description plus a suitable coda;
do not invent a nonstandard "long name" key.
