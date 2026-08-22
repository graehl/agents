# FIELD MAP supplement — surveying an active research field

Loaded when the task is to build or maintain an active field map: survey a
field, teach or learn the structure behind a current method, build an
explanatory paper/presentation, or answer "what is known about subtopic X"
(typically prior-art reconnaissance before planning a solution).

Loading this supplement for an ordinary explanation does not itself authorize
a persistent file edit. An explicit field- or frontier-survey request carries
the mode and persistence default below; otherwise use an existing map as a
read-only source or answer in conversation.

Grounded work builds one persistent artifact — a **field map** — and reads it
at two zoom levels; ungrounded work returns only a conversational projection.
Frontier/void-mapping work that consumes the same map is a separate task; see
`frontier-map.md`. The retrieval method that *finds* the papers this map
organizes — citation snowballing from anchors, paper-DB queries, keyword search
filtered by a known-labs/authors prior — is `literature-search.md`; the "light
search for recent releases" below means that method run in ungrounded mode.

## Map/survey modes — `ungrounded` vs `grounded`

Two independent axes are often conflated. Keep them separate:
- **grounding** — were sources fetched and read? This is the load-bearing
  property and what the mode specifier selects.
- **length** — brief or full. Just how much is written; not a mode.

A brief grounded survey (short, citation-verified) and a long ungrounded
survey (extensive, unverified) are both legitimate.

An explicit field- or frontier-survey request defaults to **`grounded`**.
Only an explicit **`light`**, **`recall`**, or **`ungrounded`** modifier selects
the ungrounded path. An ordinary explanation or "what is known about X"
question that does not request a survey remains conversational and does not
silently create one.

- **`ungrounded`** — the common mode selected by `light`, `recall`, or
  `ungrounded`. Answer from pretrained knowledge plus, optionally, a light
  search for recent releases. Do not download primary sources and do not
  create or modify `survey.md`, `GLOSSARY.md`, `concepts/`, `related-work/`,
  `frontier.md`, or another persistent survey artifact.
- **`grounded`** — the default when a survey request has no ungrounded
  modifier. Run the full fetch → markdown → citation-verified pipeline and
  maintain the persistent survey tree.

State the mode chosen at the top of the output. Length remains independent:
`brief grounded field survey` asks for concise, citation-verified output.

### Ungrounded-mode obligations

An ungrounded survey must not pass itself off as grounded:
- Open the conversational output with a provenance line: mode, the model's
  training cutoff, the date and scope of any light search run, and an explicit
  "claims are model recall/light search, not citation-verified".
- **Cap effectiveness grades at `single-source`.** `reproduced`,
  `externally-evaluated`, `benchmark-reported`, `contested`, and
  `failed-replication` assert source or evaluation details that the ungrounded
  pass has not checked; do not use them. `folklore` is allowed and often
  honest in this mode.
- Name techniques and the gist of who/when, but do not fabricate precise
  citations (exact venue, year, author lists). Flag what would need a
  grounded pass to pin down.

Upgrading an ungrounded answer later means rerunning the request as grounded,
creating the canonical survey tree, and revising grades against fetched
sources; the earlier answer is not itself a persisted survey.

## Where surveys live

A field survey is cross-branch reference material, not the output of one
experiment line, so it is **not** branch-scoped like `research/<branch>.md`.

```
surveys/<field-slug>/
  survey.md            "total survey": field map + territory/relationships,
                       linking to concept pages by short handle
  GLOSSARY.md          survey-scoped vocabulary (governs the subtree by path)
  concepts/<short>.md  committed per-concept understanding/summary page
                       (our distillation; records source URL); the primary
                       artifact we reason/traverse on
  related-work/      driven by `related-work` (fetch / audit / status / init);
                       never a per-survey fetch script
    papers.yaml        metadata manifest (carries each concept's short handle)
    extract/<key>/     full-text extract + images — .gitignored, workdir-durable,
                       a computed artifact; consulted only for specifics the
                       summary omits. Keyed by citation key, not short handle
  frontier.md          provisional claims + void map (see frontier-map.md)
```

`related-work/` follows the existing RESEARCH.md related-work conventions
verbatim: a regenerable fetch/extract script, a `papers.yaml`/`papers.bib`
metadata manifest (stable key, title, authors, venue, year, DOI/arXiv/etc.,
PDF URL, fetched/extracted timestamp, tool version), tiered extraction
(fully extract the high-value tier, leave background papers on demand), and
`rg`-able generated markdown. Do not respecify or reinvent that machinery.

The default and canonical cross-project location is
`~/agents/surveys/<field-slug>/`. Use another project-local location only when
the user explicitly requests it. Other projects link to the canonical map
rather than copying it.

## When to create or extend a map

Do not create an empty survey for every conversation. Create or extend the
smallest relevant region when at least one of these is true:

- the user requests a field or frontier survey without an ungrounded modifier,
  or explicitly asks for a durable field map or teaching artifact;
- a live design or research decision depends on the concept;
- a prerequisite relation is needed to understand a consequential method;
- a nearby alternative is easy to confuse and would change the decision;
- a fresh claim needs placement against the established field;
- the same explanation is being reconstructed repeatedly from scattered
  sources.

Partial maps are expected. If a related survey exists, extend its touched
region rather than opening a parallel artifact.

## The field map (`survey.md`)

Organized by **concept and technique**, not chronology. A history of
seminal contributions and citations is not the goal — explaining common
concepts/techniques and *how well they work* is.

### Addressable map nodes

A map node is usually a named Markdown section in `survey.md`, not a separate
file per concept. It should contain enough relational structure to support a
decision:

- the proposition or mechanism;
- its nearest confusable alternative;
- prerequisites;
- the discovery, observation, or falsifier supporting it;
- the regime in which it applies;
- the design decision it changes.

Private mastery state is a sparse overlay on this larger map. A mastery entry
references a node as
`<project-alias>:surveys/<field-slug>/survey.md[#section]`; most map nodes need
no mastery entry. The default alias is the project root relative to `~/`
(`~/draft` → `draft`); roots outside the home directory use their canonical
absolute path. A project `GLOSSARY.md` supplies canonical terminology, while the
map node supplies the explanation and relations. Outside research fields,
mastery may instead reference the canonical topic, design note, glossary row,
or other explanatory section. Preserve referenced headings where practical and
update mastery references when a heading or path moves.

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
- `reproduced` — an independent group reran the method or the consequential
  procedure and obtained a compatible result
- `externally-evaluated` — an independent benchmark operator executed the
  submitted artifact or predictions under a controlled or hidden evaluation;
  this verifies that score, not the training or method claim
- `benchmark-reported` — the result is comparable on a standard benchmark but
  the located leaderboard or table does not independently execute or verify it
- `single-source` — one paper, not independently confirmed
- `contested` — conflicting published results
- `failed-replication` — claimed effect that did not hold up
- `folklore` — widely repeated, no locatable primary source

Unlabeled means "single-source, not specifically verified" — but prefer to
label explicitly, since the grade is the load-bearing content of a survey.

### Discovery paths

When a node is taught through a discovery narrative, require a plausible path,
not a hindsight decomposition of the finished method. Explain the purpose or
pressure organizing attention, which pieces were then available, what made one
piece salient, why it appeared to fit the purpose, what bridge inference
suggested the composition, which nearby alternatives failed, and what
observation turned the connection into a live method.

Label the account as documented contemporary history, author retrospective,
historically informed rational reconstruction, or conjecture. Papers commonly
document justification better than discovery; do not present a clean
explanation of why a method works as evidence of how it was found.

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

## Uses of the same map

The survey paper, presentation, instructional narrative, and focused
prior-art answer use the same field map underneath. A presentation is a
compressed readout — the taxonomy, effectiveness grades, and
contested/negative sections, with per-paper detail dropped. Instruction
selects the shortest prerequisite and discovery path needed for the current
method. Do not maintain separate factual maps for these views.
