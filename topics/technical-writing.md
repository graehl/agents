# Technical writing

> Shared cold-reader guidance for research handouts, progress reports, blog
> posts, and papers: make the current claim, evidence, scope, and decision
> self-contained and legible when scanned.

Topic: `technical-writing`

## Common contract

Use this topic before substantially revising a research handout, progress
report, blog post, or paper for readers outside the working session. The
artifact-specific topic adds its own purpose, lifecycle, and evidentiary bar;
this topic owns the advice they share. When the artifact makes research claims,
also follow [`research-writing`](research-writing.md) for prior-art,
attribution, and citation coverage.

Assume a first-time reader whose attention has not yet been earned. They do
not know the working vocabulary, may have ignored earlier updates, and will
first decide whether the document deserves attention by scanning it. That
scan should yield at least one specific evidence-grounded takeaway; a full
reading should deliver the artifact's complete reader promise.

The artifacts differ mainly in how they select and reshape program work:

| artifact | selection basis | relationship to research effort |
|---|---|---|
| serious paper | chosen theme and governing form | backfill justified evidence and interest-building work until the claim is supported or narrowed |
| handout | rewarding discussion lead plus representative account of what was done | open selectively, then organize existing work by theme; add only a small, labeled prospective coordination layer |
| progress report | prior promised threads plus work since | reconcile the delta, group threads by theme when useful, and state concise dispositions/plans |
| research blog | the cool thing that worked | showcase-selective; bound the claim and point to the fuller record |

## Order material for the reader

A working document naturally accretes in the order experiments, meetings, and
ideas happened. Before dissemination, perform a substantial whole-document
consolidate, review, and revise pass. The mechanism may be direct revision or
an available dream/review workflow; the required outcome is the revised
artifact, not a ritual invocation. Lead with:

1. why the subject deserves attention now;
2. the current claim, result, or decision;
3. the evidence that supports and bounds it; and
4. what the reader should conclude, decide, or do.

Reorganize or cut chronology that does not explain a current conclusion. An
artifact may retain chronology when its reader promise is specifically to
report change over time, but it must curate that chronology for the reader.
Merely prepending an executive summary to an accumulated raw log does not
complete the pass.

## Reconstruct lost context

- Link the applicable glossary near the opening when one exists, but still
  define dominant jargon and abbreviations at first use.
- Replace internal run ids, checkpoint nicknames, and stage labels with literal
  reader-facing names. Retain an internal handle only as a provenance link.
- Separate measured observations, interpretations, deployment assumptions,
  normative choices, pending work, and downstream consequences. Do not rely on
  prose cadence to imply that one establishes another.
- State the regime of a result: population or task, data/split, model-access
  boundary, and material cost or deployment constraint.

## Make displays self-decoding

Every claim-bearing table or figure identifies its population and comparison,
metric direction, split and N when applicable, principal baseline, and cost
boundary. Define nonstandard columns and conditions adjacent to the display.
State the intended takeaway in its caption or nearby prose rather than asking a
reader to infer it from bold cells.

Before selecting or generating a graph, diagram, or quantitative display,
follow [`document-writing-figures`](document-writing-figures.md). It maps the
reader's information need to Quarto-native tables, images, panels, Mermaid, or
Graphviz and to reproducible external plotting when the claim is quantitative.

Place an effective results table or representative input/output example inline
beside the claim it illustrates. Give examples enough source, condition, and
output labeling to stand on their own. An appendix or final raw-results dump may
preserve exhaustive support, but it is not the sole home for the display that
makes a central claim understandable.

Run a scan-only pass: headings, captions, tables, figures, and emphasized text
should convey the correct current claim and decision without requiring the
reader to reconstruct the working session. Full prose then supplies evidence,
qualification, and explanation.

## Artifact-specific contracts

- [`research-writing`](research-writing.md) adds the research-specific
  prior-art and citation layer without making citation density a generic
  technical-writing requirement.
- [`blog-post-writing`](blog-post-writing.md) owns static-site structure,
  navigation, rich web elements, and blog-specific citation presentation.
- [`handout-writing`](handout-writing.md) owns the mutable, paper-like decision
  snapshot and its cooperative-review proof bar.
- [`progress-report`](progress-report.md) owns the dated, cumulative, frozen
  report stream, clearly marked refresher, delta chronology, and
  pursue/hold/park triage.
- [`research-blog-writing`](research-blog-writing.md) owns the selective
  showcase of one cool result, demo, tool, or recipe.
- [`paper-writing`](paper-writing.md) owns the form-led durable publication
  argument; [`paper-drafting`](paper-drafting.md) owns proposal selection and
  promotion into that draft.

Do not flatten these differences into the common layer. Sharing the reader
contract does not make a handout a paper or a progress report a mutable draft.
