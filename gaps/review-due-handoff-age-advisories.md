---
slug: review-due-handoff-age-advisories
noticed: 2026-11-10
where: scripts/review-due, scripts/handoff-age
---

**Gap:** advisories from the two 2026-11-10 strict reviews (verdicts under
`harsh-review/`, ranges `a8164da8541d..9dc1d6016a9c` and
`9dc1d6016a9c..80e80e3dbef9`) that are real and not fixed:

- `review-due`: the skipped-range record's format has no single home. The
  row pattern, the row template, the file preamble, and the rewrite that
  keeps the preamble sit in four places, and `Limits.skips_file` is a path
  carried in a thresholds type.
- `review-due`: one `hook` run takes about 4.8 s on a 561,884-line backlog,
  and an oversized backlog now persists until a skip is approved. The
  marker-to-HEAD changed-file listing runs twice. Not timed against the
  earlier version.
- `handoff-age`: `Section.cls` mixes the three heading tags with
  `unclassified` and `gap`.
- A refused cut is not recorded, so each new session asks again.
- `AGENTS/investigation.md` (a fold's journal "read in full before each
  append") and `topics/handoffs.md` § Advisor intake for handoff repair
  still describe whole-file reads of a handoff. Whether they are exceptions
  to "never whole" is undecided.

**Noticed while:** adding age to handoffs and the oversized-backlog cut.
**Fix sketch:** give the record one small type that owns parse, render, and
rewrite; reuse the first changed-file listing; decide the two prose cases
with graehl.
