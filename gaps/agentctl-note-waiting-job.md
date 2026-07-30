---
slug: agentctl-note-waiting-job
noticed: 2026-07-30
where: agentctl.py note_job / write_meta
---

**Gap:** `agentctl note <waiting-job> ...` writes the analysis field, then
crashes in `write_meta` with `KeyError: 'started_at'` because a dependency-
waiting job has not launched. The command should either support queued state
without run-only metadata or reject it before mutating state with a clear
message.

**Noticed while:** correcting the interpretation of a queued PII checkpoint
evaluation after its predecessor's scheduler-horizon confound was found.

**Fix sketch:** validate supported job phases before writing, or make the
human-readable metadata writer represent waiting jobs without requiring
`started_at`; cover the non-mutating rejection or successful queued-note path.
