# Research evidence integrity

> Rules and rationale for reproduction, evaluation scale, result sanity, data conditions, and significance claims.

Read this packet before accepting a newly ingested or materially transformed
dataset, presenting a newly wired experimental result, making a comparison or
significance claim, treating a completed run's score or stop/gate outcome as
decision evidence, or summarizing train/eval/gate conditions. `RESEARCH.md`
is the router and wins on conflict.

## Binding rules

Read Data goal-fit review for changed data semantics/distribution; Result-sanity
preview for a newly wired output path; Reproduce before comparing and Evaluation
scale and significance for comparisons; Read the failure before reporting it
for decision-bearing run outcomes; and Reporting eval conditions precisely for
train/eval/gate summaries. Read every matching section and follow its routes.

### Reproduce before comparing

Treat published effectiveness as unverified until reproduced under the
comparison you will claim. Reproduce the strongest relevant existing variants
before saying a new method beats them. Report with/without each technique under
controls that block selection/evaluation leakage: frozen non-selection splits,
independent metric families where applicable, controlled seeds/config search,
tuned baselines, and per-compute cost.

A research result table always states scoring split and N. Training/decode
comparisons also include wall time; concurrent decode states batch width. Use
one typed column per quantity, carry units in headers, and put free-form caveats
in footnotes rather than numeric cells. Add explicit `TBD` cells for intended
unrun comparisons, remove stale conditions to the log, and correlate important
paper numbers to their run/log artifacts with stable hidden references.
For table authoring, follow `_RESEARCH/artifacts.md` § Result tables and
document boundaries.


### Evaluation scale and significance

Use head-20 to head-50 only for smoke/reject-bad checks, not conclusions. Tune
on dev, increasing N as needed. Default test evaluation is head-1000 after
selection; full test runs once for final paper confirmation and never chooses
methods. A project may override these dataset-specific defaults explicitly.

A superiority claim uses paired bootstrap over per-example scores, normally
10,000 two-tailed resamples, reports both means, difference, p-value, and win
rate, and uses at least N=200. Save per-example scores so later comparisons do
not rerun the model. Eval tools should compare two hypothesis files and rerun
bootstrap comparisons from saved scores without loading the model again.
Significance symbols are `*` p<.05, `**` p<.01 unless a
project declares otherwise.

After editing `research/<branch>.md`, show the modified diff, eliding only long
unchanged spans to stay readable.

### Data goal-fit review

At each decision boundary after a change that can alter a dataset's meaning,
labels, coverage, or distribution—and before committing substantial downstream
work—inspect a compact human-readable sample and ask whether the resulting data
could plausibly teach or evaluate the behavior required by the research goal.
Do this early enough to redirect corpus intake, extraction, labeling,
translation, augmentation, filtering, merging, or resampling, not only after
the final build.

Declare the axes that are acceptance-critical for this decision. Exhaustively
show every represented level only for a critical axis with at most 12 levels;
language and example/label type are common examples, but their names alone do
not make them exhaustive. For higher-cardinality or secondary axes, select
levels by observed frequency and risk: include common mass, rare and boundary
cases, known or plausible failures, and any level whose omission could hide a
decision-changing defect. Report levels shown versus total and the selection
basis.

Keep the primary table to at most 32 rows unless the project declares a
different bound before review. Cover cross-products only when interactions are
a material risk and charge those cells to the same cap. If exhaustive review
of a high-cardinality axis is itself required, make it a separate audit
artifact rather than expanding the early diagnostic sample without bound.
The compact table contains the strata, source/input, resulting example or
label, a rough English gloss for non-English content, and any observed concern.
Include informative failures, not only clean examples.

This review fires only when semantics or distribution may have changed. Skip
it after a demonstrably semantics-preserving step whose relevant invariants
have already been checked; determinism alone is not such proof. Treat the
sample as diagnostic evidence, not an acceptance oracle: imperfect
semi-supervised or unsupervised data is acceptable when a controlled,
non-leaky downstream comparison improves the incumbent. Otherwise fix pipeline
defects and consider additional corpus or resource intake, teacher supervision,
and filtering or reweighting before abandoning the direction. For row-wise
transforms, this complements rather than replaces the structural provenance
and alignment checks in `_RUNS/provenance.md`.

### Result-sanity preview

Before presenting a newly wired experiment, evaluator, scorer, decode, parser,
or extraction result as meaningful—even a pilot—preview the output contract:

- counts, empty/malformed output, and producer/consumer formats;
- one aligned example per new condition: input, expected target when present,
  produced output, and the exact scorer/downstream payload; and
- condition order plus row/item mapping for concatenations, joins, prompt sets,
  extractions, and multi-policy output.

Quote the preview with a new result unless the path is unchanged. Until it
passes, numbers are provisional; fix the path and explicitly supersede
contaminated results. For no-reference outputs, use a kept-case property,
metric, or rubric plus metamorphic checks without leaking the oracle into the
generator (`topics/soft-checks.md`).


### Read the failure before reporting it

Before treating a completed run's aggregate score, gate outcome, or frozen
stop-rule trigger as evidence for a decision — stop, park, reject, select, or
a user-facing readout — and always when the result is negative or surprising:

- Verify the producing run: exact command, exit status, row count against the
  protocol's N, and the artifact's identity via its run record or meta
  back-pointer (`_RUNS/provenance.md`). When sibling invocations failed or
  were retried, classify each as harmless orchestration or score-contaminating
  before quoting the survivor's number.
- Read the raw rows behind the score: at least one input/output pair per
  failure category the scorer counts. A counter or repair statistic is a
  pointer into the artifact, not a substitute for reading it.
- Sweep the run log for anomaly markers — token/length-ceiling hits,
  truncation, retries, empty decodes, guard rejections, fallbacks — before
  summarizing; a hit routes to the post-run option audit in
  `_RESEARCH/judgment.md`.
- Reread the governing guidance: the frozen protocol and the artifact's full
  governing `PROGRAM.md` chain, respecting explicit self-rooted boundaries,
  for stated requirements the failing path may not implement (for example,
  sentence-segmenting data on intake).
- State the failure class in the readout: invocation error, harness/resource
  error, protocol defect (a design artifact such as an output ceiling or
  oversized chunk, or an unmet stated requirement), or genuine model-output
  failure. Only the last supports a claim about model quality. A protocol
  defect still fires a mechanical stop rule but caps what the stop proves,
  and does not by itself license respending past the frozen protocol.

Routine intermediate scores that decide nothing are exempt; the rule fires
when the number would change what happens next.

### Reporting eval conditions precisely

A run/eval/gate summary states, without branch shorthand:

- train corpus/split/N actually fit;
- epoch ceiling and checkpoint-selection/early-stop rule;
- selection corpus, exact split/N, and fixed versus derived status;
- decode/eval corpus, exact split/N, and overlap with selection;
- separate score/reference corpus when applicable;
- which protocol roles/conditions the score covers, when fewer than the
  protocol defines; and
- overlap among train, selection, and eval.

Training-split smokes are labeled correctness checks, not generalization.
Reuse saved hypotheses/per-example scores for small comparable pilots when
possible. For MT, also verify source/reference/hypothesis counts and inspect
aligned plain-text outputs.

Dev is for selection; test is once after selection. A test result never chooses
a method. Divergent dev/test ranking is evidence about overfitting, not a “bad
slice.”

Before leaving a substantial weak or surprising experiment line, run reasonable
closure tests: the run/row/log checks under “Read the failure before reporting
it,” the strongest cheap baseline, and same-budget null controls where
combination-only gains need them. Record the closure evidence before parking
the line. When logs suggest a tool anomaly,
search current `--help` and nearby option descriptions before declaring a tool
limit; name the relevant option and smallest discriminating follow-up.
