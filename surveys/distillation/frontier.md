# Can inexpensive probes predict recoverable student errors?

**Status: proposed experiment, not an established novel method.** This note
extends the [bounded grounded map](survey.md). Active selection, training
dynamics, structured distillation, and teacher/student capacity comparisons
already have substantial prior art. No claim of an empty research area is made.

In particular, [Error Decay on Groups](concepts/error-decay.md) already predicts
the value of additional NER annotations from group-level learning curves and
tests selection across tagger architectures. The possible contribution here
is a controlled account of where such forecasts succeed or fail under a broad
multilingual ontology, context dependence, and different output heads—not the
invention of predicting annotation benefit.

The interesting target is an intervention prediction: given a student's error
profile and training history, can we predict which new investment will help?
Candidate investments are additional annotations, additional context, a richer
head, encoder capacity, and more optimization. A useful discovery must improve
that choice on outcomes the diagnostic was not fitted to explain.

## Begin by separating measurable causes

| Candidate cause | Cheap diagnostic | Stronger intervention | What would weaken the interpretation |
|---|---|---|---|
| Output cannot represent the label | Round-trip gold through actual tokenization, projection, decoder constraints | A compatible span decoder on the same inputs | Nearly all evaluated gold already round-trips |
| Boundary convention or annotation noise | Review a stratified disagreement sample against the guideline, blinded to model identity | Evaluate on independently resolved labels | Gap persists on high-agreement cases |
| Teacher uses missing context | Inspect annotation inputs and judge context dependence | Matched extra context or teacher restricted to student input | Similar gap with equal information |
| Scarce coverage | Training exposure, held-out surface/context novelty, error concentration | Matched targeted versus random label acquisition | Added verified examples do not improve the target slices |
| Head restriction | Boundary/type oracle diagnostics; small frozen-encoder head comparison | Matched span versus token head with encoder adaptation | Improvement needs a different pretrained encoder/data |
| Encoder or optimization restriction | Controlled fit and longer-budget curves | Encoder-size contrast under equal data and disclosed compute | Gap closes with unchanged architecture and adequate optimization |

Oracle diagnostics describe remaining opportunities, not additive causal
shares. Boundary fixes can change type errors and matching assignments.
Likewise, language prediction from representations establishes decodability,
not that language information harms semantic transfer.

## A tractable acquisition contrast

Freeze a candidate pool independent of development and confirmation documents.
Use observed errors only to define language/type/context strata. Construct a
targeted acquisition arm and a random arm matched for annotation tokens and
language/domain exposure. Retain the established training stream in both.
Candidate student scores must be available before new teacher calls; actual
student/teacher disagreement is available only after a label has been bought.
Label reliability review has the same budget in both arms.

First test resampling of an unchanged pool separately from buying more labels.
The latter comparison then answers whether targeted acquisition beats simply
obtaining more representative data. Include teacher calls, review, scoring,
and GPU time in the cost account. Freeze the primary metric and practically
meaningful effect before training; use document-clustered paired uncertainty.

## Retrospective discovery, prospective test

Discover candidate diagnostics using old trajectories, explicitly marking
those results exploratory. Before the next independent data increment or
architecture intervention, freeze the rule and its predicted direction by
slice. Compare it with simple baselines: initial error rate, sample count,
and random ranking. Validate on a separate intervention and source documents,
not merely another checkpoint already used to design the rule.

A negative result remains useful if it establishes that a seemingly sensible
proxy predicts current errors but fails to predict training benefit. A stronger
positive result identifies which proxy forecasts improvement across more than
one encoder or data regime. Neither result requires claiming teacher parity.

## Test the choice of intervention, not just the next annotation

The [architecture and input connections](survey.md#architecture-and-input-changes-with-an-annotation-only-teacher)
expand the prospective question beyond selecting data. One bounded design
crosses token versus span head with isolated-target versus neighboring-context
input, retaining the same encoder initialization, target labels, and source
splits. This measures separate head/context effects and their interaction.
Frozen-feature pilots screen accessibility; matched adaptation establishes
whether the finding survives training the encoder.

For a forecast, predict before running the intervention which error strata
will improve. Compare with initial error rate, training support, random
ranking, and always choosing the cheapest intervention. A forecast that merely
finds difficult examples is insufficient. Measure cost including review,
acquisition, diagnostics, training, and deployment changes. Test another
encoder or domain before presenting a general decision rule.

The component methods are established or ordinary experimental controls.
Their combination is a proposed evaluation design, not a newly established
algorithm or an assertion that this combination has never been studied.

## Remaining falsification search

Before claiming novelty, read the queued work on reducible loss, active NER,
contextualized distillation corpora, and student-feedback selection in
[search notes](related-work/search-notes.md). Extend the search around influence
methods and learning-curve prediction. This first edition selects an empirical
question; it does not certify a publication claim or prescribe a large sweep.
