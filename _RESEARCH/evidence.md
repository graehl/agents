# Research evidence integrity

> Rules and rationale for reproduction, evaluation scale, result sanity, data conditions, and significance claims.

Read this packet before accepting a newly ingested or materially transformed
dataset, presenting a newly wired experimental result, making a comparison or
significance claim, treating a completed run's score or stop/gate outcome as
decision evidence, or summarizing train/eval/gate conditions. `RESEARCH.md`
is the router and wins on conflict.

## Binding rules

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
Detailed formatting and decoration conventions appear below under “Reproduce
before comparing (the overselling prior).”


### Evaluation scale and significance

Use head-20 to head-50 only for smoke/reject-bad checks, not conclusions. Tune
on dev, increasing N as needed. Default test evaluation is head-1000 after
selection; full test runs once for final paper confirmation and never chooses
methods. A project may override these dataset-specific defaults explicitly.

A superiority claim uses paired bootstrap over per-example scores, normally
10,000 two-tailed resamples, reports both means, difference, p-value, and win
rate, and uses at least N=200. Save per-example scores so later comparisons do
not rerun the model. Significance symbols are `*` p<.05, `**` p<.01 unless a
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
- Reread the governing guidance: the frozen protocol and every `PROGRAM.md`
  from the artifact's directory upward, for stated requirements the failing
  path may not implement (for example, sentence-segmenting data on intake).
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


## Retained detail and examples

### Reproduce before comparing (the overselling prior)

Treat a published effectiveness claim as **unverified until you reproduce it
yourself**, especially on competitive benchmarks. A large fraction of influential
results (graehl's estimate: **≥2/3**) carry significant *effective* overselling
through standard multi-hypothesis / peeking malpractice — metric circularity
(select and evaluate with the same metric family), test/oracle peeking, best-of-many
seeds or decoding configs reported as "the method", under-tuned or cherry-picked
baselines, and rerank/MBR that leaks the evaluation metric. The cost asymmetry
settles the policy even if the true fraction is lower: reproduction is cheap
insurance against building a new contribution on a false baseline. So **always
reproduce the known methods you will compare against** before claiming a new method
beats them, and onboard the strongest existing variant per aspect so the comparison
is correct. Report **with-vs-without** each technique under controls that block the
peeking paths: leave-one-out metric families, frozen non-selection splits, and
per-compute cost. Worked instance: a MetricX-QE selector scored by MetricX-reference
manufactured a 2–8× "cross-family win" that vanished under an independent metric.

### Evaluation scale and significance

**Eval split sizing defaults**:
- **Smoke / reject-bad**: `head-20` to `head-50`; no conclusions from these.
- **Pilot / hillclimbing**: dev set; grow slice size as needed for significance.
- **Default test evaluation**: use the first 1,000 lines of the test split (`head-1000`).
  Any improvement detectable only beyond 1,000 test pairs is unlikely to be practically
  meaningful; do not spend compute proving marginal differences at full scale.
- **Final paper revision only**: run the full test split (e.g. 3,334 pairs) once, after
  all method selection is finalized, to confirm the headline result holds at full scale.
  Never use full-test numbers to choose between methods.

**Statistical significance**: when reporting that method A is better than method B,
use bootstrap resampling over per-example scores to establish significance:
- * = p < 0.05, ** = p < 0.01 (two-tailed, 10,000 bootstrap iterations)
- Report: mean_A, mean_B, diff(A−B), p-value, and % of bootstrap samples where A wins
- **Minimum eval N = 200** for any conclusion; head-20/head-50 are smoke-tests only
- Use the full split for final results

### Result-sanity preview

Before presenting any newly wired
experiment/eval/benchmark/scorer/decode/parser/extraction result
as meaningful, do a cheap output-contract sanity preview,
including for prototypes and pilots.

Check, as applicable: item counts and empty/malformed outputs;
producer format vs. consumer format (`txt`, JSONL, auto,
extracted field); one aligned example per new condition showing
input, expected target when one exists, produced output, and the
exact payload consumed by the scorer/downstream tool; and
condition order plus item/row mapping for promptsets, multi-policy
outputs, concatenations, extractions, or joins.

When reporting a new result, quote the preview unless the path is
unchanged. Treat results as provisional until it passes; if it
fails, fix the path and explicitly supersede contaminated numbers.
Never present new-wiring scores whose consumed examples could be
wrappers, record objects, prompt echoes, parser markers,
diagnostic text, or shifted rows.

For outputs with no exact reference (generation, MT, model judgments),
the scorer is a soft-check oracle — a property/metric or rubric over a
kept case set, with metamorphic relations (paraphrase / terminology
invariance) the native form for translation. See `topics/soft-checks.md`
for the oracle-choice and no-leak-to-generator rules.


### Read the failure before reporting it (worked instance)

A frozen four-role annotation protocol's direct pass "failed its zero-error
stop rule," and the first readout presented the saved score as the finding.
Under review, the campaign held four dead invocations (a source-guard
rejection, an unknown-argument exit 2, a malformed allocator setting, a scorer
called off-contract) around one valid run, and nothing had established which
invocation produced the score. Reading two raw rows reclassified the result:
one span-copy repair, and one output truncated at exactly the 3,072-token
ceiling by a 6,000-character clinical chunk eliciting 101 findings — a
protocol defect, not model-quality evidence, on a score covering one of four
roles. Each check above was minutes of work and each caught something the
aggregate hid; the raw-row read happened only on user pushback, not in the
readout.

### Reporting eval conditions precisely

When summarizing a research run, eval result, or claimed "gate", report the
data conditions explicitly rather than relying on branch-local shorthand such as
"dev200 gate" or "same-pool" alone.

At minimum, state:
- train corpus / split / head-N (or full-N) actually used for fitting
- epoch ceiling and whether early stopping or schedule exhaustion determined the
  final checkpoint
- early-stopping / model-selection corpus, including exact split, head-N, and
  whether it was fixed-explicit or derived from train
- decode / evaluation corpus, including exact split, head-N, and whether it is
  the same pool as the early-stopping set or a disjoint slice
- score/reference corpus when separate from the decode inputs
- which of the protocol's roles/conditions the score covers, when the readout
  could be mistaken for the whole protocol
- overlap status among train, early-stop, and eval sets, especially when any
  quoted result comes from the same pool used for checkpoint selection

For quick train-smoke checks, say explicitly that the decode/eval examples came
from the training split and that such numbers are only correctness-smoke
evidence, not generalization evidence.

For head-N pilot or smoke-test evaluations, compare against prior full runs by reusing
saved hypothesis outputs or saved per-example score files whenever possible, rather than
re-running old baselines from scratch. Prefer evaluation paths that gracefully handle any
number of lines or expose a `--head` flag so small-slice comparisons remain directly
comparable to earlier full-split runs.

For machine translation (MT) evals, apply the global result-sanity preview
using MT-specific alignment: verify source/reference/hypothesis counts,
inspect at least one aligned source/ref/hyp example per new condition, and
confirm the scored hypothesis is plain translated text rather than JSONL
wrappers, prompt echoes, parser markers, diagnostic text, or shifted rows.

**Dev vs test set discipline**:
- **Dev set**: use freely for model selection, hyperparameter tuning, blend weight search,
  early-stopping decisions, and all iterative exploration. Report dev results as "dev performance."
- **Test set**: run once, after all selection decisions are finalized, to measure generalization.
  Never use test results to choose between methods — that turns test into a second dev set and
  invalidates it as a generalization estimate.
- If dev and test rankings diverge consistently, treat it as a real signal: the model or
  pipeline may be overfitting to dev (too many epochs, too strong LoRA scale, or too many
  blend-weight candidates explored — each candidate counts as a parameter tuned on dev).
- A sweep over K blend weight candidates on dev effectively has K × (dev size) degrees of
  freedom; the resulting "best" may not generalize. Verify with held-out dev subsets or
  accept that test divergence is informative, not a "bad slice."

Eval scripts should output per-example scores (one float per line) so bootstrap
comparisons can be run without re-invoking the model. The eval script should also
support comparing two hypothesis files in one invocation and rerunning the
bootstrap from saved score files without loading the model again.
