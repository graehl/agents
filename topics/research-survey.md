# Topic: research-survey

> How the project surveys an active research field and maps its
> frontier; governs `literature-search.md`, `field-map.md`,
> `frontier-map.md`, and the `surveys/` artifact tree.

## Contracts

- A **field survey is standalone reference material**, not a branch-scoped
  `research/` artifact. It lives under `surveys/<field-slug>/` and outlives
  any single experiment branch. Research papers *reference* a `surveys/`
  subdir rather than duplicating per-paper related-work extraction.
- **Per-survey layout.** A survey subdir holds: `survey.md` (the "total
  survey" — map + territory/relationships, linking to concept pages by short
  handle); `GLOSSARY.md` (survey-scoped vocabulary, governing every doc below
  the subdir by path, as a research program's glossary governs its subtree);
  `concepts/<short>.md` (committed per-concept understanding/analysis pages);
  `related-work/` (`papers.yaml` manifest + `fetch.sh` + git-ignored
  `extract/`); and `frontier.md` (the frontier overlay). Each survey subdir is
  also listed as a row in the top-level `~/agents/GLOSSARY.md` so surveys are
  discoverable from the repo's shared vocabulary.
- **Field and frontier are two views on one representation, not two artifact
  kinds.** A frontier-survey is *additive*: it foregrounds the
  **lower-trustworthiness** subset of a field — unproven / unreproduced claims —
  and adds void + capstone analysis in `frontier.md`. Trust level is already
  carried by each node's effectiveness grade and `[G]`/`[R]` tag; the frontier
  view filters and ranks on it rather than re-representing the field. A frontier
  pass may run *within* an established survey dir (`field-map.md` builds the map;
  `frontier-map.md` overlays on it — same `surveys/<field-slug>/`
  representation, same grounding mode).
- **Concept artifacts: three tiers, keyed by a short handle** (our name for the
  concept, which may only vaguely resemble the paper title). (1) A durable
  full-text **extract** (`related-work/extract/<short>/`) — a linked reference,
  read on demand, not routinely traversed. (2) A committed **understanding**
  page (`concepts/<short>.md`) — our distillation, the working artifact, which
  **records the source URL(s)** so the extract can be reconstituted. (3) The
  compact **map node** in `survey.md`, linking to both. `papers.yaml` carries
  each concept's `short` handle alongside its citation key.
- **Extracts are computed, git-ignored, reconstitutable.** Extraction produces a
  good `.md` — via **marker-pdf** (`AGENTS.md § PDF reading` + the
  `AGENTS.user.md` host recipe) for PDFs, or the equally valid **arXiv HTML
  view** (`arxiv.org/html/<id>`) — or a saved **HTML** file (markdown is not
  required; marker-pdf→md is the *proposed PDF path*, not a mandate). Extracts
  are `.gitignore`d — a *shared* policy so every clone ignores them (deliberately
  `.gitignore`, not the `.git/info/exclude` used for owner-might-track
  convention dirs): they are regenerable "computed" artifacts, durable in the
  author's workdir, retrieved under the user's own authorization to access the
  source, and not redistributed by default. The committed understanding page
  (plus its source URL) is the **primary artifact reasoned and traversed on**;
  drop to the git-ignored full-text extract only for a specific the summary omits.
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
