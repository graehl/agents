# Checkpoint and weight averaging

> **Mode:** grounded field survey. **Coverage cutoff:** 2026-08-22.
> The search covered checkpoint/weight averaging, SWA, EMA, LAWA, model
> soups, mode connectivity, cross-lingual checkpoint averaging, model merging,
> and paired significance tests. `[G]` marks a fetched and read primary source.

## Decision summary

For nearby checkpoints from one transformer trajectory, use an **unweighted
mean over a predeclared eligible tail or plateau window**. This is the strong
cheap baseline. Do not pick ingredients by the noisy maximum of the same
development F1, and do not continuously weight them by an improvised health
score. In well-annealed late training, expect a small variance-reduction gain,
not a new headline result. Recent broad benchmarking finds the largest benefit
earlier in training and only mild final-generalization gains after a strong
learning-rate decay [G].

Use exponential moving averaging (EMA) when future runs can maintain it online,
but state its half-life in optimizer steps or data exposure and compare it with
a uniform tail average. Use stochastic weight averaging (SWA) only as the
actual recipe it names: continue from a trained point with a small nonzero
constant or cyclic learning rate, sample distinct excursions, and average
them. A mean of several ordinary late checkpoints is checkpoint averaging, not
evidence for the SWA mechanism.

Raw parameter averaging has a different risk profile for divergent models.
Common-initialization fine-tunes may support a uniform or validation-gated model
soup. Independently initialized or intentionally displaced models need an
interpolation-barrier check and may require permutation alignment. A logit
ensemble is useful there as a diagnostic upper bound on complementarity. It is
not worth the inference cost for nearly identical same-trajectory checkpoints
whose weight mean already matches it.

## Grounding and coverage

Sixteen primary full texts were fetched, read, and distilled into the linked
concept pages. The 1992 Polyak--Juditsky paper is included only as a
metadata-verified historical anchor because its full text was access
controlled; no read-backed concept page or detailed claim is derived from it.

The search began from SWA, mode connectivity, and model soups; followed
backward and forward references into latest-window, exponential, validation-
window, multilingual, and merging work; and searched the reframings
`checkpoint averaging`, `weight averaging`, `model averaging`, `model soup`,
`mode connectivity`, and `model merging`. The decision-relevant region reached
saturation after the 2025 AlgoPerf benchmark and task-near multilingual/NMT
papers stopped adding a new averaging regime. This is a focused survey of
consolidating checkpoints and fine-tunes, not an exhaustive map of
multi-task/model-merging methods.

## Regime map

| regime | safest first recipe | why it works or fails | main check |
|---|---|---|---|
| one trajectory, ordinary annealed training | uniform eligible-tail mean | reduces stochastic tail noise; late gains shrink as learning rate approaches zero | ingredients are healthy and in one low-loss basin |
| one trajectory, deliberate post-plateau exploration | SWA: constant/mild cyclic LR plus uniform mean | samples more separated points before averaging toward the basin center | same-budget nonaveraged continuation control |
| online continuation | EMA after burn-in | cheap low-pass filter with recency-controlled horizon | predeclared half-life and update interval |
| common initialization, distinct fine-tunes | uniform soup; greedy soup only with disjoint selector | shared basin can make weight interpolation approximate output ensembling | weak ingredients and interpolation barrier |
| pretrained zero-shot to fine-tuned endpoint | scalar interpolation | trades in-domain adaptation against retained pretrained robustness | in-domain/OOD objective is explicit |
| independent or deliberately displaced starts | do not raw-average by default | permutation symmetry or distinct basins can create a high-loss midpoint | logit-oracle benefit, then alignment/barrier test |
| any materially divergent candidates | logit ensemble as diagnostic | measures usable prediction diversity without assuming parameter alignment | extra inference cost and paired gain |

### Trajectory averaging and its limits

SWA averages parameter samples gathered after conventional convergence while a
constant or cyclic learning rate keeps the optimizer exploring a connected
high-performing region [trajectory averaging](concepts/trajectory-averaging.md)
[G]. Later analysis separates variance reduction from the stronger claim that
averaging necessarily finds a wider optimum: the latter does not hold in every
setting. The practical common ground is smoothing, not a guaranteed geometric
transformation.

Latest Weight Averaging (LAWA) retains the most recent fixed number of
checkpoints; EMA retains the whole history with exponentially decaying weight
([latest window](concepts/latest-window.md),
[exponential averaging](concepts/exponential-averaging.md)) [G]. Their horizon
and checkpoint frequency are coupled. Saving more frequently without lengthening
the window shortens the represented training interval. A broad seven-workload
benchmark found both methods similar when tuned, with substantial
steps-to-target savings but only mild final validation gains
[modern benchmark](concepts/modern-benchmark.md) [G].

High learning rates and farther checkpoint spacing can create more useful
diversity early, while a learning-rate schedule that has already annealed to
zero leaves less noise for averaging to remove
[spacing and learning rate](concepts/spacing-and-learning-rate.md) [G].
Validation-window methods such as SWAD offer eligibility gates for excluding
overfit tails, but directly fitting the averaging window to one development
curve can itself overfit [validation window](concepts/validation-window.md)
[G].

### Simple means versus learned or health-weighted means

NMT comparisons of last-*K*, top-*K*, development-perplexity weighting,
gradient adjustment, and learned interpolation weights found the simple mean
robust and the elaborate weighting schemes unable to deliver a reliable extra
gain [simple mean baseline](concepts/simple-mean-baseline.md) [G]. This is the
closest direct negative result for continuously weighting nearby checkpoints
by apparent quality.

The task-nearest transformer evidence is cross-lingual XLM-R checkpoint
averaging on NER and POS. Averaging epoch checkpoints improved mean transfer
quality and reduced variance relative to the last/source-development choices;
poor early checkpoints could still hurt, and independently randomized
classifier heads were incompatible without special alignment
[cross-lingual averaging](concepts/crosslingual-averaging.md) [G]. The evidence
supports a hard eligibility gate followed by a mean, not a fine-grained
health-weighting formula.

### Soups, interpolation, and divergent models

Model soups average common-initialization fine-tunes. A uniform soup is the
baseline; a greedy soup adds validation-ranked ingredients only when the
selector score improves. Weak or high-learning-rate ingredients can introduce
an interpolation error barrier and make the uniform soup fail
[model soups](concepts/model-soups.md) [G]. When endpoints are close and the
function is locally linear, a weight soup can approximate a logit ensemble;
that is why their near-tie is expected rather than evidence to pursue both.

Pretrained-to-fine-tuned interpolation addresses a different question: retaining
zero-shot robustness while gaining in-domain accuracy
[pretrained interpolation](concepts/pretrained-interpolation.md) [G]. Fisher
weighting and permutation re-basing address more divergent checkpoints, at the
cost of curvature estimation or model alignment
[divergent merging](concepts/divergent-merging.md) [G]. Neither complexity is
justified for close checkpoints from one XLM-R lineage.

Mode-connectivity and fast-geometric-ensemble work explains when output
ensembling is worth measuring: deliberately separated points can disagree
while remaining accurate, creating an ensemble gain
[trajectory geometry](concepts/trajectory-geometry.md) [G]. For close points,
the absence of a meaningful logit-ensemble advantage is a stopping result.

## Recommended recipes

### R1. Existing close checkpoints: eligible-tail mean

1. Freeze the evaluation membership, metric, decoder, and candidate checkpoint
   list before examining the confirmation view.
2. Define a contiguous plateau/tail window by training exposure and objective
   health, not by the highest development exact F1.
3. Exclude only checkpoints that fail a predeclared hard gate.
4. Average every floating model parameter uniformly. Preserve non-floating
   buffers from the common lineage; recompute batch-normalization statistics if
   the model has them. Layer-normalized transformers do not have that burden.
5. Compare the mean once with the predeclared single-checkpoint baseline on a
   disjoint selector or confirmation view.

Spacing is expressed in optimizer steps or sentence/token exposure. Sentence
length needs no corrective weighting merely because the training examples are
sentences; a token-heavy sentence already contributes more token losses.

### R2. Future online run: EMA plus uniform-tail control

Start EMA after a predeclared burn-in. Specify the decay through its effective
half-life, `log(0.5) / log(beta)` EMA updates, and multiply by the update
interval to express it in optimizer steps or data exposure. Save enough
ordinary checkpoints to construct one matched uniform tail. Choose one or two
horizons on development evidence, then freeze them before confirmation; do not
search many decays on the fresh view.

### R3. Deliberate SWA continuation

From a healthy post-plateau checkpoint, continue for a fixed budget with a
small nonzero constant or mild cyclic learning rate. Sample points far enough
apart to show nontrivial parameter/prediction distance, average them uniformly,
and retain a same-budget continuation with the ordinary annealed schedule.
This tests exploration-plus-averaging rather than merely relabeling a tail
mean. If the ordinary trajectory is already poor, averaging is unlikely to
rescue it.

### R4. Common-start divergent branches

Try a uniform soup first. If ingredients differ materially in hyperparameters
or data order, a greedy soup is defensible only with a selector disjoint from
the final confirmation and only when it tests a short, predeclared candidate
list. First verify the linear interpolation path does not cross a material loss
barrier. Learned mixture weights are a later arm, not the baseline.

### R5. Independent/displaced branches

First compute the output-ensemble oracle on the selector set. If it shows no
meaningful gain over the best member, close the merge line. If it does, inspect
pairwise disagreement and the interpolation barrier. Only then consider
permutation alignment/re-basing or Fisher weighting. Keep the output ensemble
as the upper-bound control; do not deploy it automatically.

## Checkpoint health and weighting

Health is primarily an eligibility decision. A checkpoint should receive zero
weight if it has any of these objective faults:

- nonfinite loss, gradients, weights, or a corrupt/incomplete state dictionary;
- a loss/gradient spike beyond the run's declared tolerance;
- an optimizer, scheduler, resume, label-schema, or decoder discontinuity;
- the wrong exposure, data-mixture, ontology, tokenizer, or source-admission
  contract; or
- validation negative log-likelihood outside a predeclared plateau tolerance.

Among eligible checkpoints, record rather than optimize over:

- validation negative log-likelihood and exact typed F1, including per-source
  and per-language slices;
- calibration error where probability quality matters;
- loss and gradient-norm spikes around the save point;
- parameter/update distance from neighboring ingredients;
- prediction disagreement or Jensen--Shannon divergence; and
- loss along the linear interpolation path.

These diagnostics answer different questions. Loss/finite-state checks detect
damage; distance/disagreement detect potential diversity; interpolation loss
tests whether averaging is geometrically safe. None establishes a calibrated
continuous coefficient. Default to equal weights after the hard gate. If an
EMA is used, its recency weights come from a predeclared horizon, not a
post-hoc health score. Fisher/curvature weights are reserved for genuinely
different fine-tunes where the extra estimation has a capability-preservation
hypothesis.

## Significance and power for exact typed micro F1

Use a **paired provenance-cluster bootstrap**, not an independent bootstrap of
spans or sentences. Resample the smallest units that can reasonably be treated
as independent--normally intake documents or source groups--and carry every
sentence and annotation from each sampled unit together. For a fixed target
mixture, resample within source strata and restore the declared source weights.
For each replicate, recompute pooled TP, FP, FN, both micro-F1 values, and their
difference [paired resampling](concepts/paired-resampling.md) [G].

Use at least 10,000 paired replicates for the final comparison and report the
observed delta, a 95% interval, and the bootstrap probability that the delta is
positive. Predeclare a practical-equivalence margin as well as the zero null.
For a mature system, `0.001--0.002` absolute F1 is a reasonable starting
decision margin; the application may set another value before seeing the
fresh scores. A delta around `0.0002` is below that floor and should be called
negligible unless the program explicitly values such a change.

Prospective power is empirical: retain per-cluster prediction/annotation
records, simulate or perturb paired contingency outcomes at candidate true
deltas (`0.0002`, `0.0005`, `0.001`, `0.002`), and estimate how often the
planned interval excludes zero or lies inside the equivalence band. Report the
curve rather than one sample-size number. The attainable power depends on
cluster count, error correlation, entity density, and source mixture.

Development-set bootstrap uncertainty does not repair adaptive checkpoint
selection. If a checkpoint, window, or soup was chosen after seeing that same
set, its apparent maximum is selected evidence. Use a disjoint selector for
recipe choice and perform exactly one paired comparison on the fresh
confirmation view. Statistical significance on an old domain also does not
establish transfer to a fresh domain.

## Contested results

- SWA's original geometric story emphasizes a wider, more central optimum;
  later work finds averaging can help without consistently increasing measured
  width. Variance reduction is the safer shared mechanism.
- High learning rate plus wider spacing improved early averaging in one LLM
  pretraining study; the 2025 multi-workload benchmark did not find high
  learning rates inherently beneficial across its tuned settings.
- Weight averaging can mimic a shorter learning-rate decay and expose a good
  model earlier, but broad benchmarking finds it does not generally replace a
  well-tuned decay-to-zero schedule.

## Negative and quiet results

- Validation-perplexity weights, learned mixture weights, and gradient-adjusted
  checkpoint averages did not reliably improve over a simple mean in the NMT
  study.
- Averaging a failed or materially weak trajectory generally does not rescue it.
- Very long windows admit stale checkpoints; very short windows barely smooth.
- Uniform soups can fail when weak/high-learning-rate ingredients create an
  error barrier.
- Raw averaging of independently initialized networks can be destructive
  because functionally equivalent hidden units need not share coordinates.
- Output ensembles offer no practical reason to continue when close-checkpoint
  logits already agree and the weight mean matches their score.

## Baseline sensitivity

Averaging gains are largest against noisy, early, high-learning-rate, or
otherwise non-annealed checkpoints. They shrink against a strong late checkpoint
after the learning rate has annealed to zero. Claims should therefore always
name the underlying optimizer/schedule, averaging horizon and spacing, training
budget, single-checkpoint baseline, and whether selection used a disjoint set.

For multilingual span tagging, the strongest relevant baseline is the frozen
single checkpoint under the same native exact typed micro-F1 decoder and source
mixture. Report the absolute delta and paired interval; do not headline the
average if it merely changes the fourth decimal place.

## Read-backed digests

| cluster | digest | decision-relevant result |
|---|---|---|
| A | [trajectory averaging](concepts/trajectory-averaging.md) | SWA's exploration-plus-mean recipe; width claim is bounded |
| A | [latest window](concepts/latest-window.md) | uniform recent-window average; horizon and save cadence interact |
| A | [exponential averaging](concepts/exponential-averaging.md) | online smoothing with a recency half-life |
| A | [validation window](concepts/validation-window.md) | hard start/end gates can exclude bad tails but can overfit validation |
| A | [spacing and learning rate](concepts/spacing-and-learning-rate.md) | early gains grow with useful separation and shrink after decay |
| A | [modern benchmark](concepts/modern-benchmark.md) | broad speed-to-target gain; mild final gain; no replacement for LR decay |
| B | [simple mean baseline](concepts/simple-mean-baseline.md) | elaborate checkpoint weights do not reliably beat the mean |
| B | [cross-lingual averaging](concepts/crosslingual-averaging.md) | XLM-R NER/POS evidence and the randomized-head incompatibility |
| B | [model soups](concepts/model-soups.md) | common-start fine-tunes; weak ingredients and barriers matter |
| B | [trajectory geometry](concepts/trajectory-geometry.md) | separated accurate points can justify output ensembling |
| C | [pretrained interpolation](concepts/pretrained-interpolation.md) | pretrain-to-fine-tune interpolation trades adaptation and OOD retention |
| C | [divergent merging](concepts/divergent-merging.md) | Fisher weighting and permutation alignment belong to harder regimes |
| D | [paired resampling](concepts/paired-resampling.md) | paired bootstrap supports complex F1; domain shift remains outside the test |
