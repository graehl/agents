# char-crf-transfer — the shared character network is what transfers

> Read-backed digest `[G]` (cluster A, trust `single-source`). Cotterell and Duh
> tie the *character* network across related languages and leave the word
> embeddings language-specific. The result is the sharpest published statement of
> when a character-driven tagger wins and when it loses: at 100 target sentences
> it loses to a feature CRF by up to 8.5 F1 alone, and beats it by up to 9.8 F1
> once a related language's data is pooled through the shared character encoder.

**Paper.** Cotterell and Duh, "Low-Resource Named Entity Recognition with
Cross-lingual, Character-Level Neural Conditional Random Fields," IJCNLP 2017
(also arXiv:2404.09383). **Full text:**
[ACL page](https://aclanthology.org/I17-2016/) ·
[PDF](https://aclanthology.org/I17-2016.pdf) ·
[arXiv PDF](https://arxiv.org/pdf/2404.09383) ·
local extract `related-work/extract/cotterell2017-cross-lingual-char-crf/`.

## Mechanism

A neural CRF in the Lample et al. shape: per word, an LSTM over that word's
characters concatenated with a word-type embedding, then a sentence-level
BiLSTM, then CRF transitions. The cross-lingual variant adds a language-ID
embedding and, critically, **shares the character LSTM and the tag transitions
across languages while keeping the word embeddings language-specific**. Training
sums the target-language log-likelihood and a weighted source-language term.

Read the architecture honestly: this is a char-*word* hybrid, not a sole
character encoder. What it isolates is which *component* carries cross-lingual
abstraction, and the answer is the character component.

## Evidence

15 languages, 5 low-resource targets (Galician, West Frisian, Ukrainian,
Marathi, Tagalog), F1:

| target ← source | 100 sentences: log-linear CRF | neural | Δ | 10 000 sentences: log-linear | neural | Δ |
|---|---|---|---|---|---|---|
| gl ← — | 57.64 | 49.19 | −8.45 | 87.23 | 89.42 | +2.19 |
| gl ← es | 71.46 | 76.40 | +4.94 | 87.50 | 89.46 | +1.96 |
| gl ← fr | 58.22 | 68.02 | +9.80 | 87.92 | 89.38 | +1.46 |
| fy ← — | 62.71 | 58.43 | −4.28 | 90.42 | 91.03 | +0.61 |
| fy ← nl | 68.15 | 72.12 | +3.97 | 90.94 | 91.01 | +0.07 |
| tl ← ceb | 75.29 | 81.79 | +6.50 | 74.02 | 79.51 | +5.48 |
| uk ← ru | 70.94 | 76.74 | +5.80 | 86.01 | 87.42 | +1.41 |
| mr ← ur | 49.32 | 58.92 | +9.60 | 70.75 | 74.81 | +4.07 |

Three regimes, cleanly separated:

1. **High-resource monolingual (10k sentences):** the neural character model
   wins by +0.6 to +4.9 F1.
2. **Low-resource monolingual (100 sentences):** the *feature-engineered
   log-linear CRF wins* by 0.75 to 8.45 F1. Neural character models are
   sample-hungry.
3. **Low-resource with a related source language pooled in:** the neural model
   wins by +3.97 to +9.80, and gains far more from the pooled data than the
   log-linear model does (e.g. gl ← fr: neural 49.19 → 68.02, log-linear 57.64 →
   58.22).

The authors also note a residual: 100 target + 10 000 source sentences still
trails 10 000 target sentences by a wide margin (e.g. Galician 76.40 vs. 89.42).
Transfer reduces the annotation requirement; it does not remove it.

## Design edge and limits

Two things to carry: (a) a character encoder is the *transferable* part of a
multilingual tagger — sharing it across related languages, with only a language
embedding to separate them, is what converts a small target corpus into a usable
model; (b) below roughly a thousand target sentences, an unpooled neural
character model is the wrong tool, and a feature CRF is the honest baseline.
Limits: 2017 architecture, no pretrained multilingual encoder in the comparison,
Wikipedia-derived silver NER data (Pan et al. 2017), a word-embedding channel
still present, and no throughput or parameter accounting.
