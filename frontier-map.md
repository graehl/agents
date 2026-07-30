# FRONTIER MAP supplement — provisional claims, voids, and capstones

Loaded when the task is to place a fresh, not-yet-established claim or to find
what a research field has *not* explored and rank the most promising missing
contributions ("suggest the missing capstone result", "where are the voids in
the map").

Frontier maintenance sits on top of a field map. It depends on the
`surveys/<field-slug>/survey.md` produced by `field-map.md`; if no field
map exists, build the relevant region of one first — void-ranking without a
map of what is already filled is unfounded.

This is **not** a long-running autonomous research loop. It is a bounded
analysis: map the voids, rank the best ones, optionally draft a proposal.
It never launches runs. As with the field map, ordinary discussion does not
authorize a persistent frontier edit unless maintenance is requested or
already belongs to the active research workflow.

## Mode

Frontier work inherits the `recall` / `grounded` specifier from
`field-map.md`. The falsification gate below is a real prior-art search,
so a trustworthy capstone ranking needs `grounded` mode. A `recall`-mode
frontier pass is allowed for fast brainstorming but every candidate must be
labeled speculative — its `novelty-confidence` is unverified, since recall
cannot rule out that a "void" is already filled. Do not present a
`recall`-mode ranking as a vetted set of open problems.

## The frontier artifact (`surveys/<field-slug>/frontier.md`)

The same file holds two related but distinct structures: a provisional claim
inbox and, when useful, a void map. A field can need one without yet needing
the other.

### Provisional claim inbox

Create an entry only when a fresh claim is relevant to a live decision, not
for every paper encountered. Record:

- the exact claim and proposed mechanism;
- the incumbent and claimed improvement;
- benchmark, metric, scale, data, and compute regime;
- whether the authors control training and evaluation;
- omitted strong baselines or obvious confounds;
- independent evaluation or reproduction status;
- relevance to a live decision;
- the cheapest discriminating check;
- a date to revisit or expire it.

Preserve the claim's uncertainty in every summary. Citation count and social
uptake are relevance and retrieval signals, not confirmation. Promote or
rewrite the corresponding `survey.md` node only when evidence changes what the
field map should teach; retain enough frontier history to recover the earlier
claim and why confidence moved.

### Void map

Lay the field out as a grid over its natural axes — typically
concept × technique × regime, or whatever axes the field actually has (name
them explicitly; a field with the wrong axes produces fake voids). Each cell
is a concrete combination. Classify every cell:

- `filled` — explored, with a result (cite)
- `untried` — no located prior work
- `tried-failed` — attempted, negative result (cite it)
- `believed-impossible` — a theoretical or empirical barrier blocks it
  (cite the barrier)
- `in-progress` — known active work (cite preprint/group)

A **void** is an `untried` cell that is not `believed-impossible` and is not
merely empty because it is uninteresting or subsumed by a filled cell. Name,
for each void, *why* it is unexplored — that reason is the load-bearing
content. "No one combined A and B" is not interesting unless combining them
plausibly does something.

## Falsification gate

Before a void becomes a capstone candidate, run a prior-art search aimed at
*finding* the work, not confirming its absence — the AGENTS.md
disconfirming-pass discipline, applied hard. The two failure modes this
guards against:

1. proposing work already done that the search simply missed;
2. plausible-sounding recombinations that are trivially uninteresting or
   already subsumed.

Record `prior-art-checked:` with the queries run and what was found. A void
with no falsification search is not yet a candidate.

## Capstone ranking

Score each surviving candidate on three axes, each with stated evidence /
reasoning (not a bare number):

- **impact** — would filling it change practice or understanding, or only
  add a data point;
- **tractability** — feasible with current methods, compute, and data, or
  blocked on an unmet prerequisite;
- **novelty-confidence** — inverse of prior-art risk: how sure are we this
  is genuinely a void after the falsification gate.

Output a ranked list. For each entry: the void, its grid coordinates, the
three scores with reasoning, and the prior-art-check record.

## Depth — decided per request

Default: **analysis only** — deliver the ranked void map and capstone
candidates; a human selects what to pursue.

If the request asks for more, additionally **draft a research proposal** for
the top candidate(s): hypothesis, method sketch, eval plan, the expected
result, and an explicit falsification criterion (what observation would kill
the hypothesis). Stop there — this template never executes runs. Hand a
drafted proposal off to the normal branch/task research workflow.

State which depth was chosen and why at the start of the output.
