# BART — text infilling with full reconstruction

> Read-backed digest (cluster: text infilling, trust `single-source` for the
> ablation; summarization results `benchmark-reported`). The extract is arXiv
> v1, which does not cite T5.

**Paper.** Lewis et al., “BART: Denoising Sequence-to-Sequence Pre-training
for Natural Language Generation, Translation, and Comprehension,” ACL 2020
([HTML](https://arxiv.org/html/1910.13461v1),
[PDF](https://arxiv.org/pdf/1910.13461v1),
[local extract](../related-work/extract/lewis2020-bart/html/1910.13461v1.md)).

## Mechanism

Corrupt a document with any noising function, then have an autoregressive
decoder regenerate the entire original document. The loss is computed over
every output token, not only the corrupted positions. **Text infilling**, the
noise that won, draws span lengths from Poisson(\(\lambda=3\)) and replaces
each span with a single [MASK]. A zero-length span inserts a [MASK], so the
model must also infer how many tokens are missing. The final model combines
text infilling, masking 30% of tokens, with sentence permutation.

Two differences from T5's [span corruption](span-corruption.md) matter. T5
uses one sentinel per span, and its target holds only the dropped spans. BART
uses a single unlabeled [MASK] whose length the model must infer, and its
target is the full text. BART's decoder therefore always trains on clean,
fluent context, close to the generation regime. T5's targets are shorter and
cheaper.

BART-large has 12 encoder and 12 decoder layers at width 1024. It was trained
at RoBERTa scale on 160 GB of English text.

## Evidence

- **Objective ablation** (base models, identical data). No objective wins on
  every task:
  - Token masking or deletion is essential.
  - Document rotation and sentence permutation fail on their own; rotation
    drops SQuAD to 77.2.
  - Deletion beats masking on generation.
  - Text infilling is the most consistent: SQuAD 90.8, MNLI 84.0, CNN/DM
    perplexity 5.83, against 90.0, 83.5 and 7.06 for the MLM arm.
  - A pure left-to-right LM has the best ELI5 perplexity (21.40 vs 24.26) but
    collapses on SQuAD (76.7).
  - The MASS-like masked seq2seq arm is competitive on generation and weaker
    on SQuAD and MNLI (87.0 and 82.1).

  Learning rates and normalization were tuned per objective (`single-source`).
- **Scale.** BART-large about matches RoBERTa on GLUE and SQuAD (MNLI
  89.9/90.1 vs 90.2/90.2) and set the summarization state of the art at the
  time: XSum ROUGE-1 45.14 against 38.81 for the best prior system
  (`benchmark-reported`).
- **Translation.** With English-only pretraining, BART helps
  Romanian→English only with extra machinery:
  - a new randomly initialized 6-layer source encoder replaces BART's input
    embeddings;
  - two-stage training, first the new encoder with most of BART frozen, then
    everything.

  On WMT16 RO-EN with back-translation, the baseline Transformer-large scores
  36.80, frozen BART 36.29 and fully tuned BART 37.96. The authors report the
  approach is “less effective without back-translation data, and prone to
  overfitting” (`single-source`).

## Decision edge and limits

BART is the canonical answer to “what is text infilling”. It also shows that
denoising objectives trade understanding against generation by task. Its
translation result is a caution: an English-only denoising model is a
monolingual target-side LM, and using it for MT needed a bolted-on source
encoder plus back-translation. BART itself attributes the larger MT gains in
prior work (MASS, XLM) to pretraining on both the source and the target
languages. A pure LM still won on the loosely input-constrained generation
task.
