---
slug: harsh-review-fixing-amending-and-skip-repair
noticed: 2026-11-13
where: scripts/review-due, skills/harsh-review/SKILL.md, research survey docs
---

**Gap:** the 2026-11-13 strict review
(`harsh-review/80e80e3dbef9..ed441c97f4f1.verdict.md`, untracked) returned
"not approved" with four blockers that are still open:

1. `review-due skip` repair drops the skip row when the repaired `--to` span
   has no code changes; removing the last row deletes
   `gaps/unreviewed-code.md` too (`scripts/review-due` near the repair path).
2. The skill's `amending` section allows a history rewrite with peers active;
   `AGENTS.global.md` § Amends and `topics/commits.md` § History rewrites
   forbid that. Changing either needs graehl's decision.
3. The skill's `fixing` marker rules contradict § Review marker. The line-2
   reviewed-end note triggers a delta review, and moving to "the new HEAD"
   can skip peer commits that landed during the review.
4. `amending` makes its `fixup!` commits before the published-commit, peer
   and clean-tree stop checks, and `rebase --abort` leaves them on HEAD.

Advisories from the same verdict that are also open:

- `unreviewed_code` rebuilds `set(paths)` per entry (quadratic on the hook).
- The printed repair command lacks `--reason`; a repair overwrites the
  approved reason/date and accepts any `--to` in HEAD's history.
- Rewriting through `SkipRecord` reorders hand-written prose.
- `Limits` was renamed `Settings`, but `_limits()` keeps the old name.
- `not-ai-lint` misses one-word `__word__` bold, and its run-in-head rule
  exempts wrapped continuation lines.
- `handoff-age` treats `#` lines as front-matter comments.
- Survey consistency: per-paper concept headings missing, "only"/"none"
  claims contradicted within the survey, stale "survey.md not yet written",
  the 74.0 F1 attribution (Wikipedia-then-YouTube, not YouTube alone),
  `papers.yaml` header fields, and `field-map.md` on `extract/`.

**Noticed while:** fixing math in the repo-view contents sidebar.
**Fix sketch:** fix (1), (3), (4) and the code advisories in their own
commits; put (2) to graehl.
