# Paper drafting

> Turn a research program's evidence into candid, strength-ranked paper
> proposals, then promote a selected proposal into a working draft without
> confusing narrative promise with evidentiary support.

Topic: `paper-drafting`

## Start from the program record

Use this topic when choosing a paper focus or form, creating or amending a
paper proposal, or promoting one into a working draft. Load the applicable
`RESEARCH.md` packets first, especially evidence and judgment when the proposal
compares results or rests on a simple-baseline claim.

For a declared research program, begin with its `PROGRAM.md`, glossary, and
durable advisor bundle: the advisor's compact notes, followed-document state,
and the narrow set of working documents relevant to the candidate. Then inspect
the cited papers, handouts, research logs, result tables, run metadata, and
primary artifacts. Earlier “paper drafts” are useful records of directions and
attempted narratives, but their claims remain hypotheses until traced to
evidence.

Do not turn the advisor transcript or research chronology into the paper. The
program record is an evidence index from which to recover a current case.

## Establish the evidence ceiling first

Before proposing a form, state the strongest claim the present evidence can
honestly carry. At minimum assess:

- the exact task, scenario, data, model-access, and deployment regime;
- the measured effect size, uncertainty, evaluation N, split discipline, and
  stability across relevant seeds, languages, domains, or scales;
- the strongest simple baseline a competent community practitioner could
  plausibly build under the same compute, latency, cost, scenario, public-data,
  and model-access constraints;
- whether the method beats that baseline materially, merely ties it, loses, or
  has not yet been compared;
- which contribution survives if the headline effectiveness claim is removed;
  and
- which code, data, labels, weights, logs, or evaluation assets can actually be
  shared.

Missing evidence is not a small-print caveat. It limits the candidate form. A
result that has not beaten the matched practitioner baseline does not support a
headline-result proposal. It may still support an empirical audit, failure
atlas, diagnostic instrument, corrective-metascience paper, challenge problem,
or another form whose reader promise matches what was learned. Changing form
can reveal the real contribution; it cannot convert absent evidence into one.

Use [`successful-paper-forms`](successful-paper-forms.md) for form names and
[`paper-attractiveness`](paper-attractiveness.md) only after the evidence
ceiling is explicit.

## Keep a proposal portfolio

Every multi-paper program keeps:

```text
research/<program>/paper-proposals.md
```

This is the comparative index and the initial home for compact proposal cards.
Discuss candidates with the user by amending those cards rather than replacing
the portfolio with a one-shot recommendation. When one candidate develops a
substantial skeleton, evidence matrix, or repeated review history, move its
full card to:

```text
research/<program>/paper-proposals/<form>-<focus>.md
```

The index then retains only its provisional name, governing form, evidence
verdict, status, and pointer. Keep one owner for the full proposal; do not copy
the card into both places. Provisional slugs use the taxonomy name so the
intended reader promise stays visible, for example
`empirical-audit-public-baselines.md`. Rename while provisional if the
governing form changes.

Use a compact card with these fields:

```markdown
## <form>-<focus>

Status: seed | exploring | credible-if | promoted | parked | rejected
Governing form: <one form from successful-paper-forms>
Focus / reader promise: <one sentence>
Central result: <claim plus supported/provisional/unsupported status>
Strength: <effect, uncertainty, stability, and practical materiality>
Matched baseline: <best simple practitioner baseline and verdict>
Regime: <task, cost, scenario, public-data, and model-access boundary>
Contribution that survives: <what remains if the headline weakens>
Community assets: <what can actually be released>
Privileged access / yield: <inaccessible advantage and transferable output>
Load-bearing gaps: <missing controls, evidence, or related work>
Required TBDs: <measurement and outcome that would change the verdict>
Backfill case: <evidence or interest-building effort justified by this form>
Paper-shape sketch: <section cadence implied by the governing form>
Advisor disposition: <latest review or not yet reviewed>
```

Prefer several genuinely distinct candidates to superficial changes of title.
A paper normally has one governing form. If two candidates would stand as
separate papers, keep them separate; use the theory-plus-empirical exception
only when both support the same central claim.

Rank the backfill case with the proposal. A compelling paper shape can justify
new effort, but only when the expected evidence or reader value is material
relative to its cost and the unresolved baseline risk.

When privileged access is part of the attraction case, use
[`paper-attractiveness`](paper-attractiveness.md) to separate the unavailable
input from the finding or community asset readers actually receive.

## Promote a selected proposal

Once the user selects a candidate or otherwise authorizes a working draft,
create:

```text
research/<program>/papers/<paper-slug>.md
```

Freeze the proposal as the candid selection record, mark it `promoted`, and
link it to the draft. The draft owns the publication narrative; the proposal
continues to explain why that narrative was considered supportable. Existing
papers directly below a program root need no migration.

The new draft starts with an explicit epistemic status and links back to the
proposal, `PROGRAM.md`, program glossary, and canonical internal topic when one
exists. Follow the speculative-draft, paper/log boundary, result-table, and
related-work contracts in `_RESEARCH/artifacts.md`. A `TBD` names the missing
measurement and its falsifier; it never impersonates a result.

The `.md` path is the lightweight skeleton form. When the draft first needs a
renderer, bibliography, local assets, or multiple outputs, follow
[`document-writing`](document-writing.md) and relocate it—without leaving a
second editable copy—to:

```text
research/<program>/papers/<paper-slug>/index.<source-extension>
```

Use `index.qmd` for the Quarto default; another renderer uses the source name
selected under `document-writing.md`. The directory then owns its references,
figures, data, components, styles, and build configuration. Existing papers
directly below a program root need no migration until they need that document-
project boundary.

Creating the intended v1 of the proposal portfolio or promoted draft is a
working-document change under `research-advisor.md`. Notify the program advisor
and propose it for the followed set when its future revisions matter.

Continue from a promoted proposal under
[`paper-writing`](paper-writing.md). Renderer and output mechanics remain
irrelevant to proposal selection, but become binding through the document-
writing topics once the selected draft needs buildable web or print output.
