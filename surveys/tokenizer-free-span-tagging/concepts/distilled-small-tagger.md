# distilled-small-tagger — the lever that makes a small span tagger competitive

> Read-backed digest `[G]` (cluster E, trust `single-source` each). Four papers
> establish that a ~1M–10M-parameter tagger distilled from a large encoder
> retains most of the teacher's span quality at 20–50× the speed — and, in the
> low-gold regime, *beats* both the teacher and a fine-tuned BERT. None of the
> located students is character-level; every one keeps a word or subword
> embedding table, which is exactly the component a chars-only student deletes.

**Papers.** Mukherjee and Hassan Awadallah, "XtremeDistil: Multi-stage
Distillation for Massive Multilingual Models," ACL 2020; Wang, Jiang, Bach,
Wang, Huang, and Tu, "Structure-Level Knowledge Distillation For Multilingual
Sequence Labeling," ACL 2020; Farina, Pappadopulo, Gupta, Huang, Irsoy, and
Solorio, "Distillation of encoder-decoder transformers for sequence labelling,"
Findings of EACL 2023; Nityasya, Wibowo, Chevi, Prasojo, and Aji, "Which Student
is Best? A Comprehensive Knowledge Distillation Exam for Task-Specific BERT
Models," arXiv:2201.00558, 2022.
**Full text:** [XtremeDistil PDF](https://aclanthology.org/2020.acl-main.202.pdf) ·
[Structure-KD PDF](https://aclanthology.org/2020.acl-main.304.pdf) ·
[Farina HTML](https://arxiv.org/html/2302.05454) ·
[Student-exam HTML](https://arxiv.org/html/2201.00558) ·
local extracts under `related-work/extract/`.

## What distillation buys on span tagging

**Massive multilingual compression (XtremeDistil).** Teacher mBERT (179M) →
BiLSTM student on WikiAnn-41 (41 languages, 705K labelled sentences, 7.2M
unlabelled transfer sentences):

| system | F1 (41-language avg) |
|---|---|
| mBERT, fine-tuned | 91.86 ± 2.7 |
| mBERT-single | 90.76 ± 3.1 |
| MMNER (per-language models) | 89.20 ± 2.8 |
| **XtremeDistil student** | **88.64 ± 3.8** |

at **35× fewer parameters and 51× lower batch-inference latency**, retaining
~95% of teacher F1.

The strategy ablation is the useful part:

| training signal | 0.7M transfer | 1.4M | 7.2M |
|---|---|---|---|
| hard labels, per language | 71.26 | — | — |
| hard labels, all languages jointly | 81.44 | — | — |
| + teacher logits | 82.74 | 84.52 | 85.94 |
| staged representation → logits → labels | 84.82 | 87.07 | 87.87 |
| + gradual unfreezing | **87.10** | **88.64** | 88.52 |

Distillation signal is worth ~+7 F1 over hard labels, and 10× more unlabelled
transfer data another ~+1.5. In their zero-shot/unseen-language table the
transfer set size is decisive: 19.12 F1 with 4.1K transfer sentences versus
77.26 with 7.2M.

**Three findings that specifically favour a character student.**

1. *The word embedding matters far less than its parameter count suggests.*
   Student word-embedding initialization: SVD of fine-tuned mBERT 88.64, GloVe
   88.16, fastText 87.91, **random 87.43** — a spread of 1.2 F1 across the whole
   question. A character alphabet is "random init" with ~200 rows.
2. *Parameters and latency are different budgets.* "Parameter compression does
   not necessarily lead to an inference speedup. Reduction in the word embedding
   dimension leads to massive model compression, however, it does not have a
   similar effect on the latency. The BiLSTM hidden states … constitute the real
   latency bottleneck." Report both, separately.
3. *Which teacher layer the student mimics barely matters* (88.19–88.64 across
   layers 1–11), so a student with a completely different tokenization does not
   need a carefully chosen alignment layer — only a projection.

**Low-gold regime: the student beats the teacher (Farina et al.).** A 1M-parameter
BiLSTM distilled from a fine-tuned T5-base (220M), 100 gold train / 50 dev
sentences plus pseudo-labelled remainder, test F1:

| dataset | BiLSTM | BERT (110M) | T5 (220M, teacher) | **BiLSTM distilled (1M)** |
|---|---|---|---|---|
| ATIS | 79.93 | 79.43 | 85.01 | **86.75** |
| SNIPS | 51.63 | 52.16 | 54.33 | **57.18** |
| Movie | 60.82 | 61.80 | 67.09 | **70.51** |
| Restaurant | 47.26 | 53.17 | 56.87 | **61.13** |
| mTOP (en) | 43.12 | 46.08 | 51.94 | **54.77** |
| mTOD (en) | 68.68 | 76.95 | 79.43 | **82.26** |

The distilled 1M student beats its 220M teacher on all seven datasets at 100
gold sentences and on six of seven at 300. With full gold data the same 1M
BiLSTM is within about 0–2.5 F1 of BERT-base and occasionally above it (ATIS
95.56 vs. 95.27). The paper also shows soft-label KD beats pseudo-labels,
especially when the distillation set is small — so access to teacher *logits*,
not just teacher decisions, is worth engineering for.

**The multilingual capacity tax (Wang et al.).** One multilingual BiLSTM-CRF
student versus per-language monolingual teachers, CoNLL NER (en/nl/es/de):
teachers average 89.38, plain multilingual baseline 87.36, best structure-level
distillation 87.72. A single joint model costs ~2 F1 against per-language
models, and their best KD recovers about 0.4 of it. Any single multilingual
chars-only tagger should budget for that tax.

**Student architecture (Nityasya et al.).** Distilling task-specific BERT-base
into BiLSTM, CNN and pruned-BERT students across 12 Indonesian classification
and sequence-labelling datasets: the best BiLSTM student is **3% of BERT's size,
22× faster on CPU, 3–4 F1 lower**; a BERT-Mini student is 9% of the size and 10×
faster; ONNX export takes the BiLSTM to ~100× faster at 2.5% of the size. Their
conclusion is that BiLSTM and CNN students dominate pruned transformers on the
quality-per-resource frontier. XtremeDistil independently observes "BiLSTMs as
students to be more accurate than Transformers for low latency configurations".

## Contested and negative details

- Every student here inherits a word or subword vocabulary from its teacher;
  none is character-level. The favourable "random embeddings cost only 1.2 F1"
  reading is an extrapolation from an ablation, not a demonstration.
- Farina et al.'s datasets are narrow English slot-filling corpora (ATIS, SNIPS,
  MIT Movie/Restaurant, mTOP, mTOD), where a small model can plausibly cover the
  domain. Their teacher is T5-base, not a strong multilingual encoder.
- Nityasya et al. distil fine-tuned teachers without pretraining the students,
  in one language; their 3–4 F1 gap is the *aggregate* across 12 datasets.
- The compression multipliers (35×, 51×, 22×, 100×) come from different
  hardware, batch sizes and export toolchains and are not mutually comparable.

## Design edge and limits

This cluster is why a chars-only tagger is worth attempting at all: the
supervision bottleneck that sinks character models trained on gold data alone
(see `char-crf-transfer.md`, `deep-char-cnn.md`) is exactly what a teacher's
logits over unlimited unlabelled text remove. The open cell is that no located
work distils a large multilingual encoder into a *character-level* student — the
prior-art search for that is recorded in `../frontier.md`.
