---
slug: harsh-review-fixing-amending-and-skip-repair
noticed: 2026-11-13
where: skills/harsh-review/fixing.md, research survey docs
---

**Gap:** the 2026-11-13 strict review
(`harsh-review/80e80e3dbef9..ed441c97f4f1.verdict.md`, untracked) found
blockers and advisories that `a7cd61e4`, `a876606d` and `3cfb8d7f`
closed; the 2026-11-14 review confirmed them fixed. Still open:

- Survey consistency: per-paper concept headings missing, "only"/"none"
  claims contradicted within the survey, stale "survey.md not yet written",
  the 74.0 F1 attribution (Wikipedia-then-YouTube, not YouTube alone),
  `papers.yaml` header fields, and `field-map.md` on `extract/`.
- From the 2026-11-14 review
  (`harsh-review/a7cd61e44a7c..5c0c4d26ad9e.verdict.md`): after an aborted
  rebase, `fixing.md`'s stop question leaves `fixup!` commits at the tip,
  but the options it offers would then need a reword or reset, the very
  rewrites the file says to avoid.

**Noticed while:** fixing math in the repo-view contents sidebar.
**Fix sketch:** fix the survey items in their own commit; give the
aborted-rebase stop question an option that keeps the `fixup!` commits as
ordinary follow-up commits.
