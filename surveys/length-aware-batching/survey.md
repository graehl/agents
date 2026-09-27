# Length-aware weighted sampling for physical batches

**Grounded, focused review. Search cutoff: 2026-09-27.** Four paper full
texts and two implementation-documentation pages fetched and read in the
relevant sections; extracts and provenance are under `related-work/`.
The fixed-cycle extension below uses two additional primary full-text HTML
reads whose archival conversion failed fidelity checks, plus two verified
abstracts. The user-supplied Koloskova figure prompted one further primary
HTML read. Those five entries are explicitly unextracted in the manifest.
Anchors: Morishita et al. (2017), Doetsch et al. (2017), Ge et al. (2021).
OpenAlex forward citations of Ge, sorted by both recency and citation
count, recovered Gonzalez et al. (2023). Backward references connect all
four. Keyword searches covered weighted bucketing, length-aware sampling,
semi-sorting, dynamic batching and streaming implementations. This bounded
search did not establish exhaustive citation saturation or a novelty claim.

## Finding

Simple published physical-batching algorithms exist, including a direct
padding-versus-randomness control. I did not locate a paper establishing
the complete combination of arbitrary row weights, multi-stream logical
step representation, controlled repeat intervals, changing co-residency,
bounded startup and optional without-replacement coverage. The components
are familiar; the combined contract needs an explicit composition and tests.

The practical starting point is a continuous weighted draw stream feeding
a bounded length-aware packing buffer, with physical batches assigned to
logical steps afterward. The buffer may span multiple optimizer steps and
epoch boundaries. This recommendation is an engineering synthesis, not a
published guarantee of training quality.

User constraints established in the discussion: independently sampling each
small logical step and sorting only within it has unacceptable padding cost;
keep that as a statistical reference, not the proposed production algorithm.
Carrying pending draws across epochs and completing their batches from
nearby-length future draws is acceptable, with or without replacement.
No sampler implementation or training run was requested or performed.

## Published mechanisms and their limits

| Mechanism | What it supplies | What remains for this contract |
|---|---|---|
| [Ge: semi-sorted batching](concepts/semi-sorted.md) | Add noise to length, sort, batch, shuffle batch order; continuous randomness/padding knob | Row-weight law, bounded streaming and logical-step composition |
| [Doetsch: alternated sorting](concepts/alternating-sort.md) | Shuffle into larger bins, length-sort each bin, cut physical batches | Weighted input, streaming adaptation and step mixing |
| [Morishita: sorting study](concepts/sorting-quality.md) | Shows throughput and convergence can disagree even with shuffled batch order | Does not propose the full requested sampler |
| [Gonzalez: speech-enhancement comparison](concepts/task-dependent-quality.md) | Bounds claims that sorting necessarily harms quality | Different task; no weighted multi-stream guarantees |
| [Lhotse: buffered dynamic bucketing](concepts/streaming-implementations.md) | Bounded input buffer, replenishment, configurable length constraints; separate per-item weighted sampler | Composition and requested metrics must be verified |
| [Transformers: batch rebalance](concepts/streaming-implementations.md) | Sorts within a logical step and balances physical work across devices | Falls under the user's rejected small-step starting point |

Ge's explicit key is `length + Uniform(-a/2, a/2)`, where
`a = randomness_factor * (max_length - min_length)`. This is especially
close to the requested standalone Pareto. It changes partners across
epochs without requiring independent logical-step membership. Its reported
speed result combines semi-sorting, randomized batch order and, for the
largest gain, dynamic batch sizes. See the digest for attribution limits.

## Weighted draws and physical packing

Let row i have nonnegative configured weight w_i and normalized mass
`p_i = w_i / sum(w)`. These are sampling weights, not an additional loss
multiplier. For stream masses, allocate a stream's mass across its rows
before packing. A stream-weight target must specify whether it counts rows
or tokens; the stated desiderata use rows.

**Buffered composition, recommended first.** Generate draws with the selected
law, retain a bounded number of draw occurrences indexed by length, construct
physical batches from that buffer, and replenish consumed occurrences. The
buffer need not equal one logical step. It can hold many physical batches
while the trainer receives earlier groups. Distinct occurrences of one row
remain distinct: deduplicating them would change the sampling law.

The accounting invariant is exact: consumed occurrences equal generated
occurrences minus pending occurrences. With no dropping, duplication or
unbounded postponement, packing preserves long-run row marginals. A bounded
pending count bounds count discrepancy at a prefix, but does not by itself
bound any particular item's waiting time. Enforce an age limit separately.

For the first baseline, compare bounded shuffled-window sorting against
random selection within a permitted length band. The latter allows more
partner variation at a fixed padding tolerance. Length-only selection still
changes correlations and exposure timing; count preservation does not make
it distributionally identical to independent sampling.

**Direct length-indexed sampling, a second simple baseline.** Partition rows
into disjoint length buckets. With fixed physical batch size B, let bucket k
have probability mass `P_k = sum(p_i in k)`. Draw k with probability P_k;
fill B slots with replacement from its rows using probabilities `p_i/P_k`.
For every slot, `Pr(row i) = P_k * p_i/P_k = p_i`. Thus arbitrary weights
are exact marginals without generating an epoch schedule. Cumulative-weight
indexes or alias tables make the draws inexpensive after preprocessing.

This is our elementary derivation from hierarchical sampling, not a claim
that a reviewed paper supplies this complete design. It has deliberate
within-batch dependence and can burst repeats in small buckets. Choosing a
weighted seed and filling from its overlapping neighborhood is not the same
proof: neighborhood overlap and normalization generally alter companion
marginals. Likewise, forbidding duplicate rows within the physical batch
invalidates the with-replacement calculation.

If bucket k emits a deterministic B_k rows per visit, choosing buckets by
P_k overexposes buckets with larger B_k in row counts. For long-run row
exposure, choose visit probability proportional to `P_k/B_k`, or schedule
row mass explicitly. Random stopping rules need their own analysis; do not
substitute the fixed-size formula blindly. Objective weighting also needs
the correct row/token denominator across microbatches.

## Logical steps without independently drawing their rows first

Build physical batches using a larger candidate population, then deal a
bounded group into optimizer steps. Randomized stratification by length can
prevent all-long or all-short steps while retaining cheap physical batches.
Use stream deficits as a separate constraint and keep length balance soft.
Random tie-breaking prevents a deterministic assignment from fixing partners.

Packing all occurrences and merely permuting complete batches preserves
group counts. Searching for batches and rejecting unwanted ones does not
have that guarantee unless rejected occurrences remain pending. Bound the
group size and pending age so early batches are available promptly.

Under nonuniform weights, the target length distribution is the weighted
draw distribution, not the unweighted corpus distribution. Compare logical
steps against both that target and an independent-sampling baseline with
the same row count. Physical clusters reduce the effective number of
independent length choices; low total variation is not proof of independence.

If every stream must appear in every L-row step, `L * stream_mass >= 1`
for every stream is necessary. Whole-stream-homogeneous B-row microbatches
strengthen this necessary condition to `L * stream_mass >= B`. Which bound
applies depends on a real physical-batch constraint, not length bucketing
alone.

## Carry leftovers across accounting epochs

Maintain one continuous generator and a persistent packing buffer. At a
nominal epoch boundary, incomplete batches retain their pending occurrences
and may draw compatible lengths from future generated occurrences. Items
passed over remain pending; they are neither dropped nor silently redrawn.

- With replacement: continue the weighted generator. “Epoch” is only a draw
  budget or reporting boundary.
- Without replacement: concatenate independently shuffled passes. Preserve
  the originating pass of each occurrence if exact pass coverage matters.
  Consumption can cross those boundaries, so an observed training epoch
  need not contain exactly one copy of every row.
- Weighted low-variance draws: retain the selected occurrences across packing
  boundaries just as above. Their count/gap law differs from independent
  sampling and should be named separately.

Force service when an occurrence reaches a maximum age, allowing a wider
length match or a short batch. Otherwise a rare extreme-length row can wait
forever even in a bounded buffer. Track carry-in, generated, consumed,
carry-out and oldest pending age. At final shutdown, flush the buffer under
the documented wider/partial policy if complete coverage is required.

Increasing an omitted row's future weight is a different feedback policy.
It can reduce discrepancy, but does not by itself prove eventual service or
bounded debt. Carrying actual occurrences is simpler. A complete weighted
permutation uses every row once, so its weights influence ordering, not
full-pass frequencies; nonuniform exposure requires another definition.

## Repeat intervals and count variance

The following are analytic references, not measured sampler results.
For independent with-replacement row draws, the gap G_i between successive
occurrences, counting draw positions, is geometric on positive integers:

`Pr(G_i > g) = (1-p_i)^g`, `E[G_i] = 1/p_i`,
`Var(G_i) = (1-p_i)/p_i²`.

For small p_i, `p_i * G_i` is approximately unit exponential. Counts in T
draws are binomial, approximately Poisson when p_i is small with T*p_i
moderate. Poisson describes counts, not inter-arrival gaps. Mean gaps mostly
restate exposure frequency: periodic schedules have the same mean.

For independent L-row logical steps, probability of at least one occurrence
is `q_i = 1-(1-p_i)^L`, and the gap between steps containing the row is
geometric(q_i). Also retain within-step multiplicity, which that presence
indicator hides. With variable step sizes, compare against the product of
per-step no-hit probabilities rather than one constant q_i.

Direct B-row bucket sampling has hit probability per physical batch
`q_i_bucket = P_k * [1-(1-p_i/P_k)^B]`, despite expected count B*p_i.
Independent bucket visits make batch-presence gaps geometric with this
different parameter. With K independent physical batches per step, its
step-hit probability is `1-(1-q_i_bucket)^K`. Step stratification changes
that law again. These formulas expose burstiness that marginal counts hide.

Recommended diagnostics:

1. Normalize gaps by expected exposure, and report their empirical survival
   curve plus short-gap and upper-tail excess over the selected reference.
2. Report within-step duplicates and window-count variance at several
   horizons. Independent sampling has variance/mean `1-p_i`; systematic
   resampling or coverage correction suppresses it deliberately.
3. Separate rare rows, high-weight rows, length extremes and streams. Pooling
   raw gaps across heterogeneous weights creates spurious heavy tails.
4. Include rows with zero observed repeats via no-hit/age statistics and
   right-censoring; otherwise the worst-starved rows disappear from the test.
5. Preserve gaps across epoch boundaries. Epoch-reset statistics conceal
   boundary artifacts introduced by reshuffling or quota resets.

Finite-run “every item observed” and independent replacement sampling are
not simultaneously guaranteed. For p_i > 0, eventual sampling holds almost
surely under infinite independent draws; finite no-hit probability is
`(1-p_i)^T`. A bounded starvation guarantee changes the law.

## Repeating one initially random permutation

This is **single shuffle** or **shuffle once**, a studied legitimate baseline.
It is distinct from arbitrary cyclic order, fresh random reshuffling each
epoch, and independent sampling with replacement.

- [Mishchenko, Khaled and Richtárik, NeurIPS 2020](https://arxiv.org/html/2006.05988)
  analyze shuffle once alongside random reshuffling and incremental gradient
  descent. Their smooth convex and strongly convex results establish useful
  convergence guarantees for shuffle once. They do not prove arbitrary
  fixed schedules optimal for neural-network training.
- [Yun, Sra and Jadbabaie, COLT 2021](https://arxiv.org/html/2103.07079)
  report single shuffle beating reshuffling in an interpolating linear
  regression experiment. The broader matrix inequality supporting that
  ordering is explicitly a conjecture, with special cases proved. This is
  evidence against a universal requirement to reshuffle, not universal
  superiority of fixed cycles.
- [Safran and Shamir, COLT 2020](https://proceedings.mlr.press/v125/safran20a.html)
  prove a worst-case separation favoring repeated shuffling for smooth,
  strongly convex finite sums with constant step sizes. This entry was
  checked at abstract level; it is not a transformer performance prediction.
- [Wu, Yun and Sra, ICML 2023](https://proceedings.mlr.press/v202/wu23x.html)
  show that batch normalization can make single shuffle unstable where
  reshuffling avoids distortion or divergence, with empirical validation.
  Abstract-level read here; this specific mechanism does not automatically
  apply to LayerNorm.

These are single-source results within different regimes. There is no
universal winner established by this review. Fixed physical partners and
fixed optimizer-step order are separate interventions. The batching papers
above generally shuffle batch order, so their success does not establish
that repeating their entire schedule is equally good.

For the user's question, compare (A) one packed, logically mixed schedule
repeated unchanged, (B) the same logical batches in a new step order each
epoch, and (C) rebuilt physical batches and logical steps. Keep exposure,
batch sizes, optimizer and learning-rate schedule matched. B versus A tests
step order; C versus B tests rebuilding membership, including logical
membership. Additional arms would be needed to isolate physical partners.
This is a suggested comparison, not a run performed or scheduled here.

A fixed N-row permutation has inter-arrival gap exactly N and zero gap
variance. That alone is not evidence of inferior learning. Poisson-like gaps
and changing partners should therefore be policy-specific diagnostics, not
universal quality gates, if fixed cycles are admitted as candidates.
For arbitrary row weights, a finite repeated deck fixes exposure to integer
counts divided by deck size. It approximates weights unless those ratios
match exactly; regenerating weighted counts or carrying fractional deficits
escapes that restriction but ceases to be one fixed finite cycle.

The fixed-cycle primary HTML reads are summarized directly here. Their
cached extraction failed the shared engine's fidelity gate; see
[capture gap](../../gaps/related-work-math-html-fidelity.md). No failed
conversion was promoted to a checked extract.

## Interpreting the user's convergence figure and existing sampler

The supplied figure is Figure 1(a) of
[Koloskova et al., ICML 2024](https://arxiv.org/html/2305.19259v4).
Section 6 explicitly defines SGD as sampling with replacement, SS as one
permutation reused, and RR as a fresh permutation each epoch. The figure is
a synthetic quadratic with dimension 100 and 50 components, plotting
gradient norm over 10,000 epochs at fixed learning rates. It supports a
sampling-law effect on optimization, not a numerical prediction of held-out
quality for weighted language-model training. The paper additionally
reports logistic-regression, MNIST and CIFAR comparisons. Relevant methods
and experiment sections were read directly; no checked local extract yet.
Use v4 or the proceedings: the earlier v3 title makes a stronger claim and
its header explicitly reports a proof error.

For systematic resampling, an epoch of M draws gives row i either floor
or ceiling of M*p_i occurrences under the standard single-offset scheme.
The total is exact; per-row expected fractional counts are not integer
counts that can all be exact. If M*p_i < 1, presence is Bernoulli(M*p_i).
With independent offset resets each epoch, that row's epoch-level gaps are
geometric. This is similar to replacement in allowing repeated omissions,
but differs from M independent row draws: the latter permits within-epoch
duplicates and has presence probability 1-(1-p_i)^M.

Carrying fractional entitlement across epochs can control those omissions.
The user's description of a new `carried` option was not checked against
its implementation in this review. Carrying rounding debt and carrying
already-selected packing leftovers are distinct mechanisms; the former
changes future counts, while the latter preserves pending occurrences.

## Contested results

Aggressive sorting harms quality in the reviewed recurrent ASR/NMT settings,
while the Conv-TasNet study finds sorted batches competitive. These are
different tasks and training configurations, not contradictory replications.
All effectiveness statements here are **single-source** in their respective
regimes. The papers do not establish a monotone relationship between a
standalone randomness score and endpoint quality.

## Negative and quiet results

Morishita finds that high-throughput target-length ordering can converge
worse. Ge's fixed-size semi-sorted result does not dominate random batching
on validation loss; the strongest claim adds dynamic sizes. No located
source validates a universal Poisson-gap requirement for length batching.
An absent full-contract match in this bounded search is not proof of novelty.

## Baseline sensitivity and smallest useful comparison

Hold generated row occurrences fixed when comparing packing policies, then
compare independent replacement versus systematic/coverage-controlled draws
separately. Otherwise count variance and packing effects are confounded.
Use the current `~/draft` weighted sampler as an existing baseline: its
`_sample_epoch_indices` uses systematic resampling and materializes the
epoch's draw list before packing windows (`trainlib.py`, read 2026-09-27).
That is distinct from the proposed continuous bounded generator.

Compare three candidates: bounded sorted windows, bounded random-within-band
packing, and direct mass-weighted buckets. Sweep packing width or buffer
size independently of optimizer-step size. Measure the user's exposure,
coverage, diversity, padding, logical-step representation and co-residency
criteria, plus repeat gaps and carry age. Ratchet a frozen suite across
multiple seeds and adversarial sparse tails; preserve a Pareto set rather
than tightening every dimension independently into an infeasible contract.

Padding inflation is a useful proxy, not measured speed. For padded
attention, also consider the squared-length work proxy; final ranking needs
actual throughput including CPU startup, steady-state packing and device
work. A small quality check should compare candidates that survive the
standalone screen. No such performance or training experiments were run here.

## Retrieval record and coverage limits

OpenAlex anchor: W3197549883, two indexed citers on the retrieval date.
Both recency and citation-count orderings returned Gonzalez (2023) and
NeuralPDR (2025); the latter is outside this focused batching-method review.
OpenAlex omitted the anchor's reference list, so backward traversal used
the full text. Semantic Scholar API access failed through the web tool.
Citation counts for other sources were not retrieved and are not guessed.

Disconfirming search specifically sought sorting degradation, weighted
bucketing and later batching comparisons; Gonzalez supplies the key
boundary result. Additional verified abstract-only background:
[Kocmi and Bojar, RANLP 2017](https://arxiv.org/abs/1707.09533) reports no
effect of minibatch homogeneity in its English–Czech setting;
[Douc, Cappé and Moulines, 2005](https://arxiv.org/abs/cs/0507025) distinguishes
systematic from residual/stratified resampling variance guarantees. Neither
was full-text extracted in this pass, so neither supports a concept digest
or a broad theorem claim here.
