# Topic: research-survey

> How the project surveys an active research field and maps its
> frontier; governs `literature-search.md`, `field-map.md`,
> `frontier-map.md`, and the `surveys/` artifact tree.

## Contracts

- A **field survey is standalone reference material**, not a branch-scoped
  `research/` artifact. It lives under `surveys/<field-slug>/` and outlives
  any single experiment branch. Research papers *reference* a `surveys/`
  subdir rather than duplicating per-paper related-work extraction.
- One field map serves both the survey paper/presentation use and the
  prior-art-reconnaissance, instruction, and personal-mastery-reference uses;
  these are views or sparse overlays on the map, not separate factual
  artifacts.
- **Frontier analysis depends on a field map.** Void-ranking is unfounded
  without a map of what is already filled; `frontier-map.md` builds
  the relevant region of `survey.md` first if none exists.

## Invariants

- **Grounding mode is explicit and orthogonal to length.** `recall` (model
  memory + light search) vs `grounded` (fetch → markdown → citation-verified)
  is stated at the top of every output. A `recall` survey caps effectiveness
  grades at `single-source` and carries a provenance banner; it must not
  present itself as grounded.
- Every effectiveness claim is graded (`reproduced` / `single-source` /
  `contested` / `failed-replication` / `folklore`) and conditioned on
  baseline, benchmark, and regime. A bare "works well" is rejected.
- A fresh, decision-relevant claim remains in `frontier.md` with its exact
  claim, regime, independent-check status, and revisit condition until its
  evidence changes what `survey.md` should teach.
- Discovery narratives distinguish documented history, retrospective,
  rational reconstruction, and conjecture; a finished-method decomposition
  is not presented as the path by which its pieces were noticed and combined.
- A frontier void is not a capstone candidate until a falsification search
  (aimed at *finding* prior work, not confirming absence) is recorded.

## Known edge cases

- An active field's survey decays; recency is load-bearing. Surveys carry a
  coverage-cutoff date and search scope — but no per-claim "last updated"
  dates, which create false confidence.
- `recall`-mode frontier passes are allowed for brainstorming but every
  candidate is labeled speculative: recall cannot rule out that a "void" is
  already filled.
