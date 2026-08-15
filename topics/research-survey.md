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
  `related-work/` (`papers.yaml` manifest + git-ignored `extract/`); and
  `frontier.md` (the frontier overlay). Each survey subdir is
  also listed as a row in the top-level `~/agents/GLOSSARY.md` so surveys are
  discoverable from the repo's shared vocabulary.
- **`related-work/` is driven by the shared `related-work` engine, never by a
  per-survey script.** `~/agents/scripts/related-work` (on `PATH`) owns fetch,
  extraction, and reconciliation for every survey: `init` scaffolds a new
  `related-work/`, `fetch` builds extracts, `audit` reconciles `papers.yaml`
  against `extract/` and exits 3 on drift, `status` derives the grounding
  banner's counts, `list` reports the manifest. Do not write a survey-local
  `fetch.sh`: the last one accumulated three defects the engine now has tests
  for — extracts rekeyed out from under their sentinels, a manifest that
  silently drifted from disk, and a bare invocation that queued every pending
  download at once. A survey needing behavior the engine lacks extends the
  engine.
- **Field and frontier are two views on one representation, not two artifact
  kinds.** A frontier-survey is *additive*: it foregrounds the
  **lower-trustworthiness** subset of a field — unproven / unreproduced claims —
  and adds void + capstone analysis in `frontier.md`. Trust level is already
  carried by each node's effectiveness grade and `[G]`/`[R]` tag; the frontier
  view filters and ranks on it rather than re-representing the field. A frontier
  pass may run *within* an established survey dir (`field-map.md` builds the map;
  `frontier-map.md` overlays on it — same `surveys/<field-slug>/`
  representation, same grounding mode).
- **Concept artifacts: three tiers.** (1) A durable full-text **extract**
  (`related-work/extract/<key>/`) — a linked reference, read on demand, not
  routinely traversed. (2) A committed **understanding** page
  (`concepts/<short>.md`) — our distillation, the working artifact, written
  from a **fetch+read** of the full text and hyperlinking it (invariants
  below). (3) The compact **map node** in `survey.md`, linking to both.
- **Two names per paper, and the extract takes the durable one.** The
  **citation key** exists from the moment a paper enters `papers.yaml`; the
  **short handle** — our name for the concept, which may only vaguely resemble
  the paper title — is added later, and only for a paper that earns a concept
  page. So extracts are keyed by citation key: keying them by `short` orphans
  every already-fetched extract the day a handle is assigned.
- **Extracts are computed, git-ignored, reconstitutable.** The searchable
  target artifact is a good `.md` per paper. Source preference: when an HTML
  view exists (`arxiv.org/html/<id>`, a blog page), derive the `.md` from it
  — cleaner and cheaper than PDF reconstruction; fall back to **marker-pdf**
  (`AGENTS.global.md § PDF reading` + the `AGENTS.user.md` host recipe) only
  for PDF-only papers. Keep a distinct saved **HTML** copy only when it
  carries interactive or presentation elements that do not map well to
  markdown; otherwise the derived `.md` suffices. Extracts
  are `.gitignore`d — a *shared* policy so every clone ignores them (deliberately
  `.gitignore`, not the `.git/info/exclude` used for owner-might-track
  convention dirs): they are regenerable "computed" artifacts, durable in the
  author's workdir, retrieved under the user's own authorization to access the
  source, and not redistributed by default. The committed understanding page
  (plus its full-text hyperlinks) is the **primary artifact reasoned and traversed on**;
  drop to the git-ignored full-text extract only for a specific the summary omits.
  A completed extract carries a `.fetched` sentinel written *only* on success —
  so a crashed extraction is retried rather than cached as done — recording the
  method, source URL, and the server's `ETag`/`Last-Modified` when it offers
  them. `related-work fetch --revalidate` uses those to ask whether a source
  changed; with no validators to send, the answer is "may have changed", never
  "fresh".
- **A figure whose PDF original is vector is extracted as vector.** marker
  rewrites every figure region — vector originals included — to a raster crop
  at a resolution fixed once at extraction time (`_page_<n>_Figure_<k>.jpeg`),
  and no later zoom recovers what that crop did not capture, which is the one
  thing a durable full-text extract exists to protect. So `related-work fetch`
  asks the same marker run for per-block geometry and hands it to
  `scripts/pdf-figures-svg`, which recuts each figure region from the source
  PDF as SVG and repoints the markdown link. The raster crop stays on disk as
  a fallback, and stays *linked* for a region that is genuinely a placed
  bitmap or whose geometry disagrees with the crop — the tool names each such
  case in its output rather than passing over it. `--no-svg-figures` opts out;
  a host that cannot run the pass (no `uv`) reports `figures: raster only
  (…)` on the fetch row, never a silent no-op.
- One field map serves both the survey paper/presentation use and the
  prior-art-reconnaissance, instruction, and personal-mastery-reference uses;
  these are views or sparse overlays on the map, not separate factual
  artifacts.
- **Frontier analysis depends on a field map.** Void-ranking is unfounded
  without a map of what is already filled; `frontier-map.md` builds
  the relevant region of `survey.md` first if none exists.

## Design decisions

- **Run a pinned `html2text` through `uvx` for HTML derivation** (vs. vendoring
  it or requiring a global install): the pure-Python converter stays
  reproducible without importing its source into this repository, and the
  `.fetched` sentinel records its version and exact Markdown path.
- **Retain source HTML according to content loss** (vs. always keeping or
  dropping it): the Markdown derivation substitutes embedded TeX for MathML
  and removes duplicated `data:` payloads, while HTML remains when
  presentation or interaction does not survive that conversion.

## Invariants

- **Grounding mode is explicit and orthogonal to length.** `recall` (model
  memory + light search) vs `grounded` (fetch → markdown → citation-verified)
  is stated at the top of every output. A `recall` survey caps effectiveness
  grades at `single-source` and carries a provenance banner; it must not
  present itself as grounded.
- **Concept understanding pages follow a fetch+read.** `concepts/<short>.md` is
  written from an actual read of the fetched full text — its
  `related-work/extract/<key>/`, or the fetched primary source — not from
  pretrained recall; a durable, checked understanding is the goal. A
  recall-only page is a banner-marked stopgap, not a grounded concept page, and
  its citations stay `verified: false` until a fetch+read confirms them.
- **Understanding pages hyperlink the viewable full text.** Every
  `concepts/<short>.md` includes **direct, clickable** markdown links (not bare
  arXiv ids) to where the full text is viewed/downloaded — the HTML viewer and/or
  the PDF — so a reader on GitHub reaches the paper in one click. Use the exact
  URL the fetch downloads from (`arxiv.org/html/<id>` + `arxiv.org/pdf/<id>`, a
  transformer-circuits `index.html`, or a blog post); it doubles as the extract's
  reconstitution source.
- Every effectiveness claim is graded and conditioned on baseline, benchmark,
  and regime. A bare "works well" is rejected. `field-map.md` owns the grade
  vocabulary and its definitions; do not restate the list here, since a second
  copy is what let this one fall two grades behind.
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
