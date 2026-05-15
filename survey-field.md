# SURVEY supplement — mapping an active research field

Loaded when the task is to survey a research field: build an explanatory
survey paper/presentation, or answer "what is known about subtopic X"
(typically prior-art reconnaissance before planning a solution).

This template builds one artifact — a **field map** — and reads it at two
zoom levels. Frontier/void-mapping work that consumes the same map is a
separate task; see `research-frontier.md`.

## Survey modes — `recall` vs `grounded`

Two independent axes are often conflated. Keep them separate:
- **grounding** — were sources fetched and read? This is the load-bearing
  property and what the mode specifier selects.
- **length** — brief or full. Just how much is written; not a mode.

A brief grounded survey (short, citation-verified) and a long recall survey
(extensive, unverified) are both legitimate.

The invocation carries a leading mode word:

- **`recall`** — triggered by "quick", "brief", or "recall" survey of X.
  Built from pretrained knowledge plus, optionally, a light search for
  recent paper releases. No PDF fetch, no `related-work/` directory. A full grounded
  survey is search-, token-, and reading-intensive; `recall` is the cheap
  path when the user wants orientation, not a citable artifact.
- **`grounded`** — "full survey of X", "for a paper", or prior art the user
  will act on. Runs the full fetch → markdown → citation-verified pipeline
  and builds `related-work/`.

Default to `recall` for casual questions; choose `grounded` when the user
says "full", mentions a paper/presentation deliverable, or will plan real
work off the result. State the mode chosen at the top of the output.

### `recall`-mode obligations

A `recall` survey must not pass itself off as grounded:
- Open `survey.md` (or the subtopic note) with a provenance banner: mode,
  the model's training cutoff, the date and scope of any light search run,
  and an explicit "claims are pretrained recall, not citation-verified".
- **Cap effectiveness grades at `single-source`.** `reproduced`,
  `contested`, and `failed-replication` assert a cross-source check that
  recall has not performed; do not use them. `folklore` is allowed and
  often honest in this mode.
- Name techniques and the gist of who/when, but do not fabricate precise
  citations (exact venue, year, author lists). Flag what would need a
  grounded pass to pin down.

Upgrading a `recall` survey to `grounded` later is expected: re-run as
`grounded`, build `related-work/`, and revise grades against fetched
sources.

## Where surveys live

A field survey is cross-branch reference material, not the output of one
experiment line, so it is **not** branch-scoped like `research/<branch>.md`.

```
surveys/<field-slug>/
  survey.md            the field map (this template's product)
  related-work/        fetch/extract artifacts + metadata manifest
  frontier.md          void map / capstone analysis (see research-frontier.md)
```

`related-work/` follows the existing RESEARCH.md related-work conventions
verbatim: a regenerable fetch/extract script, a `papers.yaml`/`papers.bib`
metadata manifest (stable key, title, authors, venue, year, DOI/arXiv/etc.,
PDF URL, fetched/extracted timestamp, tool version), tiered extraction
(fully extract the high-value tier, leave background papers on demand), and
`rg`-able generated markdown. Do not respecify or reinvent that machinery.

## The field map (`survey.md`)

Organized by **concept and technique**, not chronology. A history of
seminal contributions and citations is not the goal — explaining common
concepts/techniques and *how well they work* is.

### Coverage cutoff

State once, at the top: the date through which the literature was searched
and the search scope (venues, arXiv categories, query terms). This is a
search horizon, not a freshness guarantee — an active field's survey decays.
Do not put per-claim "last updated" dates; they create false confidence.
Re-survey by re-running the `related-work/` fetch script and diffing.

### Technique entries

Each technique gets: what it is, the problem it addresses, its relation to
1–3 nearest field-known alternatives, and a graded **effectiveness** claim.

An effectiveness claim is rejected if it is bare ("works well", "widely
adopted"). It must be relative and conditioned:
- against *what* baseline,
- on *what* benchmark/metric,
- in *what* regime (scale, data budget, compute, modality).

Tag every effectiveness claim with an evidence grade:
- `reproduced` — independent replication, multiple groups, or a standard
  benchmark leaderboard
- `single-source` — one paper, not independently confirmed
- `contested` — conflicting published results
- `failed-replication` — claimed effect that did not hold up
- `folklore` — widely repeated, no locatable primary source

Unlabeled means "single-source, not specifically verified" — but prefer to
label explicitly, since the grade is the load-bearing content of a survey.

### Mandatory sections

A survey that omits these is a history dressed as a survey:
- **Contested results** — where the literature disagrees, and on what axis
  (benchmark choice, baseline strength, hyperparameter budget).
- **Negative / quiet results** — techniques that were proposed and quietly
  did not replicate or were superseded; what specifically failed.
- **Baseline sensitivity** — claimed gains that shrink or vanish against a
  stronger baseline or larger compute budget.

### Disconfirming pass

Apply the AGENTS.md disconfirming-search discipline: for each headline
effectiveness claim, actively search for the result that *refutes or bounds*
it, not just confirming restatements. Confirmation-shaped search results are
easy to over-trust. Record what was checked.

## Use as prior-art reconnaissance (subtopic query)

A "what is known about X" request is a filtered slice of the field map, not
a fresh survey. Produce a focused subtopic note: the relevant techniques,
their graded effectiveness, contested points, and known negative results.
Still run the disconfirming pass. If the field map already exists, query it
and extend only the touched region; if not, build just that region of
`survey.md` rather than the whole map.

## Survey paper vs. presentation

Same field map underneath. A presentation is a compressed readout — the
taxonomy, the effectiveness grades, and the contested/negative sections,
with the per-paper detail dropped. Do not maintain a separate artifact.
