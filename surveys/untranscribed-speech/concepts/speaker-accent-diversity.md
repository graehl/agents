# Measuring whether a speech source adds diversity

Brief grounded field survey, searched through 2026-10-02. The question is
whether a source adds useful voice and accent variation without comprehensive
speaker or regional metadata. Two directly relevant papers were fetched and
read locally; supporting sources have the narrower reading status recorded
below. Published results are author-reported, not reproduced here. No Arabic
diversity measurements have been run.

Use separate speaker and accent-sensitive representations, with recording
conditions as a third diagnostic view. Measure both variation within a source
and coverage it adds to the existing pool. A scalar or a cluster count is
meaningful only after checking what differences its embedding preserves.

## What the literature establishes

| Representation or method | Evidence relevant to source diversity | Consequence |
|---|---|---|
| Speaker embeddings: x-vectors / ECAPA-TDNN | Speaker identity supervision produces useful voice similarity, but does not isolate identity. Raj et al. probe content and channel information in x-vectors on RedDots. | Use as a voice-redundancy view; neither cosine distance nor cluster count establishes the number of narrators or accents. |
| Language-ID plus speaker embeddings | Ghorbani and Hansen obtain 81.3% accent classification accuracy from frozen LID features, 75.8% from SID features, and 84.1% from their combination with a trained classifier. The comparison covers US, Indian and Australian English. | Complementary views are plausible. A classifier result does not establish that raw cosine distance is calibrated for accent similarity. |
| Accent-trained encoder followed by clustering | Kim et al. freeze an accent-trained encoder and cluster its pooled vectors, including an accent excluded from encoder supervision. Data mined using those clusters improves downstream Indian-English recognition relative to random selection. | Closest evidence for the proposed use. Metadata-free application is possible, although representation learning used accent labels elsewhere. |
| Pooled self-supervised speech features | The existing [representation survey](audio-domain-representations.md) motivates intermediate-layer features as candidates for acoustic variation. | Useful additional baseline; layer, pooling, language and channel sensitivity require validation. The final ASR layer is not automatically the best diversity representation. |

Ghorbani and Hansen's result is **single-source** evidence on
UT-CRSS-4EnglishAccent, containing read and spontaneous speech. Their test
length bins total 6,519 utterances. The combined accent/LID/SID system reaches
87.4%, but that comparison also includes curriculum learning; the simpler
81.3/75.8/84.1 comparison more directly supports complementarity. This remains
English accent evidence, not Arabic dialect validation. See the
[paper](https://arxiv.org/html/2310.11004v1) and
[local extract](../related-work/extract/ghorbani2023multi-embedding/html/2310.11004.md),
§§ II.2–II.4 and IV.1–IV.3.

Kim et al.'s **single-source** downstream result is Indian-English WER
15.2% with randomly sampled additional training speech versus 14.4% with
cluster-mined speech; supervised accent mining reaches 13.7%. The paper reports
similar training-utterance counts and mixes US speech into adaptation.
Its Common Voice Indian test population is 708 utterances / 347 speakers;
the exact selected training counts, wall times and decoding batch widths are
not supplied. The result supports targeted acquisition, not maximizing a
generic diversity score. See the [paper](https://arxiv.org/html/2408.02582v1)
and [local extract](../related-work/extract/kim2024accent-mining/html/2408.02582.md),
§§ 2.3 and 3.3.

The backward citation trail from Ghorbani and Hansen leads to
[Raj et al., ASRU 2019](https://arxiv.org/abs/1909.06351),
*Probing the Information Encoded in X-vectors*, and
[Desplanques et al., Interspeech 2020](https://arxiv.org/abs/2005.07143),
*ECAPA-TDNN*. Their citation metadata and abstracts were checked; their full
texts were not extracted in this pass. Raj et al.'s reported content/channel
leakage supplies a direct counterexample to treating a speaker embedding as a
pure identity coordinate.

## Quantities worth measuring

**Within-source diversity.** Fixed clustering gives cluster occupancy and
effective occupancy, `exp(-sum(p * log(p)))`, at several fixed resolutions.
Report concentration as well as breadth: a source covering many clusters can
still consist mostly of one voice. These are embedding-cluster statistics,
not counts of real people or geographical varieties.

The [Vendi Score](https://arxiv.org/html/2210.02410v2), Friedman and Dieng
(TMLR 2023), offers a continuous alternative: for a positive-semidefinite
similarity matrix K with unit diagonal, take the exponential entropy of the
eigenvalues of K/n. It requires no accent labels or hard clustering. Its
evaluation covers molecules, images and text; applying it to Arabic speech is
an untested proposal. Kernel and bandwidth determine which differences count.
A nearly diagonal kernel can make almost every clip appear distinct. The
definition and limitations were read online; local extraction failed its
fidelity check and is not represented as an accepted extract.

**Incremental coverage.** For each candidate clip, measure its nearest distance
to a frozen reference pool, separately in each representation. Summarize the
distribution and the fraction beyond thresholds calibrated on held-out
recordings from that pool. Also measure how much adding the candidate reduces
nearest-neighbor distances for a fixed, source-balanced audit pool. A source
can be internally repetitive yet add one useful missing variety; high internal
diversity does not imply new coverage.

These nearest-neighbor summaries are proposed diagnostics, not a published
Arabic diversity benchmark. Keep reference size, sample budget, representation
and thresholds fixed across comparisons. Report curves over sample budget:
otherwise a larger source wins simply because more of it was observed.

## A practical first screen

1. Sample equal speech duration from each eligible source, cap contribution
   per known speaker or parent recording, and retain read/prompted-answer/media
   distinctions. Use repeated duration-matched subsamples; unknown speaker and
   region remain unknown. Sample windows of comparable voiced duration, with
   short clips reported separately rather than discarded from the dev set.
2. Start with a frozen ECAPA speaker model and a frozen VoxLingua107 LID
   embedding model, the two readily interpretable views studied together in
   Ghorbani and Hansen. Compare a pooled multilingual SSL encoder if the LID
   view mainly separates code-switching or language. Pin checkpoints, layers,
   pooling, normalization and input preparation. Keep the views separate
   before considering a learned or weighted combination.
3. Produce per-source redundancy, cluster concentration and incremental
   coverage summaries. Fit any PCA or clustering once on a balanced calibration
   pool, then freeze it. Quantify in that fixed space; use UMAP/t-SNE only to
   browse examples. Preserve representative clips and nearest pairs so a
   listener can audit what each reported difference means.
4. Compare independent windows from the same recording and mild gain/codec
   perturbations. A codec change should not count as a new accent. Inspect
   apparent novelty for music, clipping, silence, overlap and source-specific
   channel effects; report these as conditions instead of silently rewarding
   or removing them. Where metadata exists, check across speakers and parent
   recordings rather than holding out random clips from the same recording.
5. Retain source-balanced random sampling as the baseline. For an eventual
   training-data selection claim, compare equal hours and the same recipe on
   an untouched, varied dev set. For dev construction, retain source/style
   slices and WER by slice; do not select solely for maximum distance or the
   current recognizer's errors.

Embeddings can live in versioned array/Parquet files with DuckDB summaries
keyed by audio hash and segment offsets. Store source, representation revision,
input duration, nearest-reference distance, cluster assignment and condition
flags; keep uncertainty resampling grouped by recording, or known speaker.
This screen is proposed follow-up work, not implemented intake behavior.

## Limits, negative findings and baseline sensitivity

No independently reproduced Arabic source-diversity result was located in this
bounded pass. The two central studies address English accent tasks. Kim et al.
explicitly discuss misleading location labels and speaker/channel shortcuts;
their supervised miner outperforms their clustering miner. Ghorbani and Hansen
find speaker embeddings weaker than LID embeddings for their accent task and
find substantial utterance-length sensitivity. Those bounds argue against a
single speaker-cluster count as an accent-diversity certificate.

The disconfirming search covered speaker entanglement, content/channel leakage,
unsupervised accent clustering, and similarity-based accent recognition.
It also surfaced *Similarity-based Accent Recognition with Continuous and
Discrete Self-supervised Speech Representations* (ICASSP 2025) and
*Causally Disentangled Contrastive Learning for Multilingual Speaker Embeddings*
(arXiv:2602.01363). These are leads, not full-text-reviewed evidence here.
No saturation or state-of-the-art claim is made.

## Search trail and remaining work

Anchors were WavLM and Kim et al.'s accent miner. OpenAlex was queried on
2026-10-02: title search resolved the latter to W4403370506, which returned
zero indexed citers under both recency and citation-count sorting. WavLM
(W3209984917) returned 1,868 citing records; the first 20 under each sort were
inspected. The high-citation list includes *Comparative Layer-Wise Analysis of
Self-Supervised Speech Models*, a relevant follow-up for layer selection.
Web/arXiv/ACL/ISCA searches supplied the more directly relevant accent papers.
Local reference-list inspection connected the multi-embedding paper to
x-vectors, ECAPA, VoxLingua107 and the x-vector probing study; Kim et al.'s
references connect its miner to accent multitask learning and group DRO.

The interim Arabic source mix can proceed without this screen. The unresolved
work is to extract the remaining primary sources, select deployable embedding
checkpoints, test nuisance sensitivity on Arabic, and measure whether a
candidate adds coverage beyond source-balanced sampling. Until then, report
source/style breadth and available speaker metadata without claiming measured
accent coverage.
