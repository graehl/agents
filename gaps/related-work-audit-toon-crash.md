---
slug: related-work-audit-toon-crash
noticed: 2026-08-16
where: scripts/related-work verb_audit, acli/emit.py write_toon_table
---

**Gap:** `related-work audit --toon` crashes with
`AttributeError: 'str' object has no attribute 'keys'` on the **clean** path.
The failure path emits a findings table, which is uniform and TOON-shaped; the
success path emits the single status mapping `{"ok": true, "drift": 0, …}`
through the same formatter, and `write_toon_table` materializes a bare mapping
into its keys as strings before asking the first element for `.keys()`. So the
one outcome an agent most wants to confirm — no drift — is the one that raises,
while a drifting survey prints normally. Exit code is still 0, so a caller that
ignores stderr sees success with a traceback in its output.

**Noticed while:** Auditing the new `surveys/tokenizer-free-span-tagging`
related-work tree after staging its extracts; `--toon` crashed, plain
`related-work audit` printed the expected `"ok":true,"drift":0` line.

**Fix sketch:** In `write_toon_table`, wrap a non-sequence mapping in a
single-row list (a one-row table is the correct TOON rendering of a status
mapping), or have `verb_audit` route the clean-status emit through the same
table helper the findings path uses. Add a regression test covering
`audit --toon` on a survey with zero findings — the existing tests only cover
the drift case.
