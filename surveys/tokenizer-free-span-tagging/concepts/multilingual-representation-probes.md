# multilingual-representation-probes — pooled meaning and token alignment

> Read-backed digest `[G]` (cluster G, trust `single-source` each). This node
> separates evidence already present in a frozen encoder from evidence created
> by a learned cross-lingual mapping or an alignment-specific objective.

**Direct sources.** [Sentence-BERT](https://aclanthology.org/D19-1410/)
isolates what pooling plus cosine can and cannot establish;
[Conneau et al.](https://aclanthology.org/2020.acl-main.536/) compare layers at
word, contextual-word, sentence, and subspace levels;
[SimAlign](https://aclanthology.org/2020.findings-emnlp.147/) extracts word
alignments from frozen mBERT and XLM-R; and
[Awesome-Align](https://aclanthology.org/2021.eacl-main.181/) shows the separate
gain from fine-tuning multilingual embeddings on parallel/alignment objectives.
Full text is cached under `related-work/extract/`.

## Two questions, not one invariance score

Meaning-equivalent translations or rewrites can agree at two granularities:

- **Pooled sentence or span representations:** do whole translations,
  paraphrases, or corresponding spans retrieve each other or receive greater
  similarity than meaning-changing controls?
- **Aligned token representations:** where the texts have local
  correspondences, do source tokens retrieve the correct target tokens?

Sentence agreement does not identify which tokens correspond. Token agreement
is undefined for many free rewrites, where one phrase may be deleted, split, or
expressed only by a sentence-level construction. Use span or sentence tests for
those cases rather than forcing one-to-one token links.

## Frozen protocol

Keep the candidate encoder unchanged. Construct held-out positive pairs from
translations, independently authored paraphrases, or meaning-preserving
rewrites. Add hard negatives that preserve topic, named entities, length, and
lexical overlap while changing a relation, argument, polarity, quantity, or
label-relevant fact. Random unrelated negatives make language or topic
shortcuts look semantic.

Sweep **every encoder layer** and state every reduction operation. For pooled
representations, compare at least first/`CLS`, mean, and the downstream span or
word pooling actually contemplated. For token tests, state how subtokens become
words; averaging subtokens and promoting any subtoken edge to a word edge are
different estimands.

| question | quantitative probe | visualization | evidence of suitability |
|---|---|---|---|
| Are equivalent sentences/spans close under the intended readout? | positive-minus-hard-negative cosine margin; paired retrieval P@1/Recall@1 and MRR; Spearman correlation when graded semantic similarity is available | layer × pooling heatmap; positive and hard-negative similarity distributions | held-out positives consistently outrank matched negatives across language pairs and rewrite types |
| Are local equivalents directly recoverable? | mutual-nearest-neighbor or IterMax links scored by precision, recall, F1, and alignment error rate against human links | token × token similarity matrix with gold/predicted edges; layer × alignment-score heatmap | a frozen layer gives useful held-out alignment without a learned bilingual transform |
| Are two representation spaces geometrically similar? | centered kernel alignment (CKA), reported per layer | cross-language layer × layer CKA matrix | evidence of similar subspace geometry only; not evidence that paired items occupy nearby coordinates |

PCA, UMAP, or t-SNE plots colored by language and joined across paired examples
can reveal gross language clustering or outliers. They remain exploratory:
neighborhoods depend on projection settings, and a visually mixed cloud does
not show that the correct translations or rewrites are nearest neighbours.

## Comparing candidate encoders across a language portfolio

Freeze one language order before looking at encoder scores. For a commercial
deployment, use the deployment brief's descending business priority—for
example expected users, traffic, revenue, or support obligation—with a stated
date and deterministic tie-break. For a research deployment, substitute a
declared external coverage or resource order. Do not sort languages separately
for each encoder: that hides whether an encoder's apparent breadth comes from
doing well only on its preferred European, high-resource, or shared-script
subset.

Use the same held-out examples, layer/pooling sweep, and extraction rule for
every encoder, then show one primary table/visualization and three supporting
views:

1. **Annotated encoder × language heatmap (primary):** one fixed-order column
   per language and one row per encoder for pooled retrieval, token-alignment
   F1, or frozen task span F1; use separate small multiples rather than mixing
   metric scales. Print a rounded value or missing-data glyph in every cell,
   use a perceptually ordered colorblind- and grayscale-safe palette, and mark
   important thresholds with borders or symbols that survive monochrome
   printing. Add region, script, resource, and deployment-priority bands and
   counts rather than treating a sparse cell as a zero.
2. **Optional head-to-tail coverage curve:** when the heatmap is too wide or
   cumulative breadth matters, add languages from left to right in the same
   fixed order. For every prefix, plot both macro score and a floor statistic
   such as the bottom-quartile mean or tenth percentile. Overlay the newly
   added language's score as a faint point. A stable macro with a collapsing
   floor exposes a multilingual claim carried by head languages; this curve
   summarizes but does not replace the readable cell values above.
3. **Compact encoder scorecard:** report priority-weighted mean, unweighted
   macro, worst-language and bottom-quartile scores, head-versus-tail gap, and
   missing-language count. Keep latency/model size beside these quality
   columns when they affect the deployment choice.
4. **Task-confusion margin matrix:** for predeclared contrastive label pairs
   such as PERSON versus ORG, show languages as columns and encoder/layer pairs
   as rows. For an example whose true class is `a` and contrast is `b`, report
   either the prototype margin
   `cos(h, centroid(a)) - cos(h, centroid(b))` or the frozen linear-probe logit
   margin `z_a - z_b`. Include the median, lower decile, and fraction at or
   below zero; a two-dimensional scatter is only a companion view. Prefer the
   bounded cosine margin for cross-encoder comparison, or calibrate/standardize
   probe margins on development data because raw logit scales are not
   comparable across probes.

For the last two views, add a brief frozen-encoder task probe: fit the same
regularized linear head for every candidate under fixed per-language label
budgets, update counts, seeds, and splits, without updating the encoder. Report
strict span F1, pairwise margins, labels used, and fit time. Plot score against
labels or online-MDL compression when label efficiency matters. This is
head-only probe training, not encoder fine-tuning; the control/selectivity and
leakage rules are in
[`token-classifier-objectives`](token-classifier-objectives.md#frozen-pre-flight-is-task-information-usable-before-fine-tuning).

## What the papers establish

The layer is an empirical variable. SimAlign tested every layer of frozen
mBERT and XLM-R and found a roughly parabolic word-alignment curve, with layer
8 best in its setup. It averaged subtokens for word representations, also
tested subtoken-level links, and evaluated against human word alignments. That
is direct evidence that some untouched multilingual encoders expose usable
token correspondences, not a license to hard-code layer 8 for another encoder
or language pair.

Conneau et al. show why one optimum cannot stand in for another. With
independently trained monolingual BERTs, sentence retrieval after a learned
orthogonal mapping was best in lower layers, contextual transfer after mapping
was best in middle layers, and early layers had the highest CKA similarity.
Their post-hoc mapping used bilingual dictionaries or parallel pairs. It shows
that spaces can be **alignable**; it does not show that the untouched spaces
already use the same coordinates. Because CKA is invariant to orthogonal
rotation, high CKA has the same limitation.

Pooling also changes the question. Sentence-BERT reports that raw BERT mean and
`CLS` vectors perform poorly with cosine on semantic textual similarity while
the same raw vectors remain useful to a fitted logistic classifier. A failed
pooled-cosine test therefore rejects that layer–pooling–metric combination, not
all task information in the encoder. Conversely, a strong frozen linear probe
shows decodable information, not metric alignment suitable for nearest-neighbour
retrieval.

Awesome-Align is the tuned comparison, not an independent witness for the base
encoder. It selects hidden layers empirically, extracts bidirectional links,
and fine-tunes on parallel text with translation-language-modeling,
self-training, parallel-sentence, and consistency objectives. Its gains show
that alignment can be manufactured or strengthened. They cannot be cited as
proof that the original encoder offered those representations without
alignment-specific tuning. The paper also finds that the best layer varies by
encoder and sometimes by language pair.

## Claim ladder and stopping rule

1. **Already metric-aligned:** the frozen encoder, declared layer and declared
   pooling/alignment extraction rule pass held-out paired retrieval or human
   alignment tests without fitting a bilingual transform.
2. **Task information is accessible:** a frozen-encoder linear probe succeeds,
   even if raw cosine or nearest-neighbour retrieval does not. This supports a
   classifier readout, not interchangeable embeddings.
3. **Alignable:** a held-out evaluation succeeds only after fitting an
   orthogonal/linear mapping on separate bilingual pairs.
4. **Alignment-tunable:** success requires parallel fine-tuning or an explicit
   contrastive/alignment objective.

Choose an encoder for translation/rewrite invariance only at the rung the
intended system is allowed to use. Report the full layer × pooling grid, per
language-pair results, hard-negative construction, subtoken reduction, and
whether any mapping or parallel objective was fitted. Then verify the selected
configuration on the actual downstream label task; representation probes are
pre-flight evidence, not a substitute for the matched end-to-end comparison.
