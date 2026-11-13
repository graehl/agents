# Small and on-device punctuation and case models: what has been measured

Grounded from fetched full text (read 2026-11-13). Numbers are cited as
`extract/<key>:line`; the key names the extract under `../related-work/extract/`.
"Our arithmetic" and "our cross-paper comparison" mark things computed or
assembled here that no single source states.

**Sources read**

- You, Li (Cisco), 2024, *A light-weight and efficient punctuation and word
  casing prediction model for on-device streaming ASR* —
  [PDF](https://arxiv.org/pdf/2407.13142) · [arXiv](https://arxiv.org/abs/2407.13142) ·
  [extract](../related-work/extract/you2024-cnn-bilstm/you2024-cnn-bilstm.md) ·
  [reading note](../related-work/readings/you2024-cnn-bilstm.md)
- Ling, Lai, Chen, Huang, Liu, 2023, *A Small and Fast BERT for Chinese
  Medical Punctuation Restoration* —
  [PDF](https://arxiv.org/pdf/2308.12568) · [arXiv](https://arxiv.org/abs/2308.12568) ·
  [extract](../related-work/extract/ling2023-small-fast-bert/html/2308.12568.md) ·
  [reading note](../related-work/readings/ling2023-small-fast-bert.md)
- Alam, Khan, Alam, W-NUT 2020, *Punctuation Restoration using Transformer
  Models for High- and Low-Resource Languages* —
  [PDF](https://aclanthology.org/2020.wnut-1.18.pdf) ·
  [extract](../related-work/extract/alam2020-transformer-punct/alam2020-transformer-punct.md) ·
  [reading note](../related-work/readings/alam2020-transformer-punct.md)
- Courtland, Faulkner, McElvain, IWSLT 2020, *Efficient Automatic Punctuation
  Restoration Using Bidirectional Transformers with Robust Inference* —
  [PDF](https://aclanthology.org/2020.iwslt-1.33.pdf) ·
  [extract](../related-work/extract/courtland2020-robust-inference/courtland2020-robust-inference.md) ·
  [reading note](../related-work/readings/courtland2020-robust-inference.md)
- Uyen, Tu, Huy, Interspeech 2022 (FastText ablation only) —
  [PDF](https://arxiv.org/pdf/2207.01312) · [arXiv](https://arxiv.org/abs/2207.01312) ·
  [extract](../related-work/extract/uyen2022-jointcappunc/html/2207.01312.md) ·
  [reading note](../related-work/readings/uyen2022-jointcappunc.md)
- Vandeghinste, Guhr 2023 (parameter counts and one cited comparison) —
  [PDF](https://arxiv.org/pdf/2301.03319) · [arXiv](https://arxiv.org/abs/2301.03319) ·
  [extract](../related-work/extract/vandeghinste2023-fullstop-dutch/html/2301.03319.md) ·
  [reading note](../related-work/readings/vandeghinste2023-fullstop-dutch.md)
- Păiș, Tufiș 2021 survey (one cited distillation result) —
  [PDF](https://arxiv.org/pdf/2111.10746) · [arXiv](https://arxiv.org/abs/2111.10746) ·
  [extract](../related-work/extract/pais2021-survey/pais2021-survey.md) ·
  [reading note](../related-work/readings/pais2021-survey.md)

## Inventory

| Model | Architecture | Size | Tasks | Trained on | Speed figure |
|---|---|---|---|---|---|
| CNN-BiLSTM (You & Li) | 5000-piece BPE, 100-d embeddings; 3 residual 1-D conv layers (kernel 3, 100 channels); 2 BiLSTM layers and 1 unidirectional LSTM, hidden 384; two linear heads (`extract/you2024-cnn-bilstm:47-67`, `:107`) | 7 MB quantized ONNX (`:170`, `:178`); parameter count not stated | punctuation (4 labels) + case (4 labels) | 55M English words, from scratch, 30 epochs, about 2 h on one RTX 3090 Ti (`:87`, `:107`) | 10 ms for one 42-word paragraph on an Intel Core i5-1035G1 in sherpa-onnx (`:170`, `:178`) |
| PMP-H256 (Ling et al.) | 6-layer Transformer, hidden 256, FFN 1024, 8 heads (`extract/ling2023-small-fast-bert:127`) | 10.3M parameters, 10.1% of teacher (`:127`) | punctuation (4 labels), Chinese | distilled on 50M-token unlabelled medical text, then fine-tuned (`:205`) | none reported |
| PMP-H312 | 4 layers, hidden 312, FFN 1200, 12 heads (`:128`) | 11.4M | same | same | none |
| PMP-H768 | 6 layers, hidden 768 (`:126`) | 59.7M | same | same | none |
| DistilBERT / DistilRoBERTa off the shelf | 6-layer distilled encoders, fine-tuned as taggers | "40% fewer parameters" than BERT (`extract/alam2020-transformer-punct:132`); DistilRoBERTa "12% smaller", about 1.2× faster than RoBERTa-base (`extract/courtland2020-robust-inference:109`) | punctuation, English | IWSLT 2.1M words | relative only |
| ALBERT-base | 12 layers with shared weights | 10.5M parameters (`extract/ling2023-small-fast-bert:122`) | punctuation | — | none; sharing cuts parameters, not layers computed |

The paragraph timed for the CNN-BiLSTM is the one in the paper's Table 5
(`extract/you2024-cnn-bilstm:148`); the word count of 42 is our count of
that example.

## CNN-BiLSTM: accuracy and what it was compared against

IWSLT 2011 reference test, punctuation
(`extract/you2024-cnn-bilstm:124-132`):

| Model | Comma P / R / F1 | Period P / R / F1 | Question P / R / F1 | Overall P / R / F1 |
|---|---|---|---|---|
| BLSTM-CRF (best earlier non-Transformer overall) | 58.9 / 59.1 / 59.0 | 68.9 / 72.1 / 70.5 | 71.8 / 60.6 / 65.7 | 66.5 / 63.9 / 65.1 |
| Self-attention word+speech | 67.4 / 61.1 / 64.1 | 82.5 / 77.4 / 79.9 | 80.1 / 70.2 / 74.8 | 76.7 / 69.6 / 72.9 |
| CT-Transformer | 68.8 / 69.8 / 69.3 | 78.4 / 82.1 / 80.2 | 76.0 / 82.6 / 79.2 | 73.7 / 76.0 / 74.9 |
| CNN-BiLSTM | 71.5 / 54.0 / 61.5 | 76.7 / 82.6 / 79.5 | 73.8 / 70.5 / 72.1 | 74.4 / 67.9 / 71.0 |

Case, same test (`:139-142`):

| Model | UPP F1 | CAP P / R / F1 | MIX F1 | Overall F1 |
|---|---|---|---|---|
| Corr-BiRNN (earlier joint model) | 73.2 | 82.6 / 71.9 / 76.9 | not predicted | 82.4 |
| CNN-BiLSTM | 98.9 | 85.4 / 84.4 / 84.9 | 80.0 | 87.8 |

Size and time (`:167-170`): CT-Transformer 280 MB and 25 ms; CNN-BiLSTM 7 MB
and 10 ms.

Claims and grades:

- Against earlier non-Transformer models on IWSLT 2011 reference text, the
  CNN-BiLSTM is 5.9 overall F1 above the best (71.0 vs 65.1), which the paper
  states as 9% relative (`:159`). Grade: benchmark-reported, with a
  **training-data confound**: the baselines' numbers are copied from papers
  that trained on the 2.1M-word IWSLT set, while this model trained on 55M
  words of other text (`:87`, `:111`).
- Against CT-Transformer it is 3.9 overall F1 lower, with comma F1 7.8 lower
  (61.5 vs 69.3), period 0.7 lower, question 7.1 lower (our arithmetic). The
  comma deficit is recall: 54.0 against 69.8.
- Case: 87.8 overall against 82.4 for a 2017 BiRNN. Grade: single-source.

**The baseline is not a strong pretrained encoder.** CT-Transformer is the
only Transformer the paper runs, taken as a sherpa-onnx Chinese–English
release (`:163-165`); its IWSLT scores are quoted from its own paper. The
related-work section mentions BERT and RoBERTa punctuation models (`:25`)
but none appears in the tables. For case there is no Transformer baseline at
all: CT-Transformer does not predict case (`:178`).

**Our cross-paper comparison on the same test set** (different training data
and recipes, so indicative only):

| Model | Comma F1 | Period F1 | Question F1 | Overall F1 | Source |
|---|---|---|---|---|---|
| CNN-BiLSTM, 7 MB | 61.5 | 79.5 | 72.1 | 71.0 | `extract/you2024-cnn-bilstm:132` |
| DistilBERT-base-uncased | 66.3 | 79.0 | 73.5 | 72.7 | `extract/alam2020-transformer-punct:186` |
| BERT-base-uncased | 70.9 | 82.8 | 79.6 | 76.9 | `extract/alam2020-transformer-punct:180` |
| RoBERTa-base (Alam) | 74.3 | 86.2 | 82.8 | 80.3 | `extract/alam2020-transformer-punct:182` |
| RoBERTa-base, 9-window aggregation (Courtland) | 76.2 | 87.7 | 87.9 | 83.9 | `extract/courtland2020-robust-inference:59` |
| RoBERTa-large + augmentation | 76.7 | 88.9 | 87.8 | 82.9 | `extract/alam2020-transformer-punct:191` |

Read this way the small model trails a RoBERTa-base tagger by 12.8–14.7
comma F1, 6.7–8.2 period F1 and 9.3–12.9 overall F1 (our arithmetic). The
period gap is about half the comma gap, not zero. Grade: none; this is an
unpaired comparison across papers.

**Error pattern.** Commas are most often missed entirely and next most often
predicted as periods; questions are often predicted as periods; the largest
CAP error is CAP predicted lower-case, which the authors tie to missed
sentence-final marks (`extract/you2024-cnn-bilstm:180-186`).

**"Streaming" is the ASR system's property, not the model's.** The model is
bidirectional over 200-token sequences (`:49-55`, `:101`); the paper reports
no experiment with limited right context or incremental re-tagging.

## Distillation: recipe and what it recovers

**Ling et al. recipe** (Chinese medical reports, CMRPT: 4,332,870 O /
434,981 comma / 83,248 period / 33,304 colon training tokens;
`extract/ling2023-small-fast-bert:146-151`):

1. Teacher: Chinese RoBERTa-wwm, 12 layers, 102.3M parameters, given a
   punctuation-mark-prediction pre-training task on unlabelled in-domain
   text: classify the mark at each `[MASK]` slot, cross-entropy plus a
   supervised contrastive term weighted 0.1 (`:79-113`, `:351`).
2. Student initialised from selected teacher layers and trained to match
   teacher hidden states by mean squared error through a learned projection,
   100K steps (`:171-181`, `:351`).
3. Fine-tune the student as a slot tagger, 10 epochs, lr 3e-5; results are
   means over 10 seeds (`:351`).

Results on the CMRPT test set, F1 (`:231-327`):

| Model | Parameters | Comma | Period | Colon | Overall |
|---|---|---|---|---|---|
| RoBERTa-wwm (teacher) | 102.3M | 95.03 | 91.00 | 86.00 | 90.68 |
| RBT-6 (generic 6-layer) | 59.7M | 89.88 | 86.62 | 81.99 | 86.16 |
| MiniRBT (generic) | 10.3M | 88.66 | 82.49 | 81.41 | 84.18 |
| TinyBERT (generic) | 11.4M | 88.9 | 82.95 | 79.99 | 83.95 |
| PMP-H768 | 59.7M | 94.65 | 91.24 | 83.43 | 89.77 |
| PMP-H256 | 10.3M | 90.07 | 86.83 | 80.32 | 85.74 |
| PMP-H312 | 11.4M | 89.81 | 87.26 | 80.29 | 85.78 |
| ALBERT-base-Chinese | 10.5M | — | — | — | 87.54 |

(ALBERT row: `:122`, `:335`.)

Claims, single-source, in-domain clean text, 10-seed means:

- A 10.3M student keeps 94.6% of the teacher's overall F1 (85.74 / 90.68,
  our arithmetic; the paper says 95%, `:357`) and loses 4.96 comma, 4.17
  period and 5.68 colon F1. **Period loses nearly as much as comma.**
- Task-specific distillation is worth 1.56 overall F1 over a generic student
  of identical shape (85.74 vs MiniRBT 84.18), almost all of it on period
  (+4.34) and comma (+1.41); colon is 1.09 lower (our arithmetic).
- A 59.7M 6-layer student is within 0.91 overall F1 of the teacher, and 3.61
  above the generic 6-layer model.
- Comma recall is where the small students fall: PMP-H256 comma R 87.07
  against the teacher's 95.71, at precision 93.28 against 94.35 (`:302-303`,
  `:232-233`).

Problems with the paper's own framing:

- **ALBERT, at 10.5M parameters, scores 87.54, above both ~10M students**
  (85.74, 85.78). The paper compares ALBERT only with the 59.7M PMP-H768
  (`:331-336`, `:359`) and describes the two as having "the same number of
  parameters", which contradicts its Table 1 (`:122`, `:126`). ALBERT still
  computes 12 full-width layers, so it is small on disk but not fast.
- The text reports a 4.3% improvement over ALBERT in each of P, R and F1;
  the table gives 1.43, 2.92 and 2.23 (`:335-336`, `:359`).
- In the 30K-step ablation, "w/o KD" scores 88.44 against 86.72 with
  distillation; the text says this comes "with large model size and longer
  inference time", so that row is probably not a 10.3M model (`:342-345`,
  `:365`). The ablation therefore does not isolate what distillation adds at
  fixed size.
- No latency is reported despite the title.
- The text says the results show "narrow and deep models" beat "wide and
  shallow" ones (`:357`), but the 6×256 and 4×312 students tie (85.74 vs
  85.78).

**Off-the-shelf distilled encoders on English** (fine-tuned directly, no
task-specific distillation):

| Comparison | Reference overall F1 | Comma F1 | Period F1 | ASR overall F1 | Citation |
|---|---|---|---|---|---|
| DistilBERT-base vs BERT-base (Alam) | 72.7 vs 76.9 | 66.3 vs 70.9 | 79.0 vs 82.8 | 61.8 vs 64.9 | `extract/alam2020-transformer-punct:180`, `:186`, `:194`, `:200` |
| DistilRoBERTa vs RoBERTa-base (Courtland) | 73.7 vs 83.9 | 67.1 vs 76.2 | 80.8 vs 87.7 | — | `extract/courtland2020-robust-inference:59`, `:66` |
| Distil-mBERT vs mBERT (Alam, English) | 69.3 vs 75.9 | 61.5 vs 69.2 | 76.9 vs 82.7 | 59.3 vs 64.6 | `extract/alam2020-transformer-punct:187`, `:190`, `:201`, `:204` |
| Distil-mBERT vs XLM-R-large (Alam, Bangla news) | 70.1 vs 87.0 | 66.0 vs 81.2 | 73.0 vs 90.8 | 47.5 vs 63.2 | `extract/alam2020-transformer-punct:227-229`, `:237-239` |
| ALBERT-base vs BERT-base (Alam) | 78.4 vs 76.9 | 72.7 vs 70.9 | 84.5 vs 82.8 | 66.0 vs 64.9 | `extract/alam2020-transformer-punct:180`, `:184`, `:194`, `:198` |
| ALBERT-base vs RoBERTa-base (Courtland) | 75.4 vs 83.9 | 69.4 vs 76.2 | 82.7 vs 87.7 | — | `extract/courtland2020-robust-inference:59`, `:65` |

Grade: benchmark-reported for each row. Courtland's text gives the
DistilRoBERTa loss as 9.1 where its table gives 10.2 (`:109`, `:59`, `:66`).
In both papers a half-depth generic student loses 4–10 overall F1, and comma
and period fall by similar amounts (4.6 and 3.8 in Alam; 9.1 and 6.9 in
Courtland, our arithmetic).

**Ensemble-to-single distillation** (as cited, not read): Yi et al. 2017
train a single network against an ensemble teacher with a KL-divergence
loss; the student is below the ensemble and above each individual model
(`extract/pais2021-survey:238`).

## Models without a pretrained encoder

| Evidence | Numbers | Grade |
|---|---|---|
| Vietnamese, same joint heads on FastText embeddings instead of vELECTRA (ViCapPunc) | case F1 60.73 vs 86.75; punctuation F1 49.47 vs 80.10; recall 49.05 and 41.03 (`extract/uyen2022-jointcappunc:272-306`) | single-source; no recurrent or convolutional context layer is described for the FastText variant, so it understates what a trained small model can do |
| English, CNN-BiLSTM from scratch on 55M words | 71.0 punctuation, 87.8 case (above) | single-source |
| Seq2seq Transformer from scratch, 6 layers, embedding 256, on 6M BNC sentences | upper-case F1 0.87, period 0.73, comma 0.56, question 0.71 with chunk merging (`extract/nguyen2019-chunk-merging:68`, `:121`, `:229-247`) | single-source; no other system on this data |
| GRU model at SEPP-NLG 2021 (as cited, not read) | 10 to 20 points lower F1 than the best Transformer models (`extract/vandeghinste2023-fullstop-dutch:108`) | as cited |

## How large the "ceiling" encoders are, as stated

XLM-R base 270M and large 550M parameters, with an estimated 5% macro-F1
gain from large that the authors did not run
(`extract/vandeghinste2023-fullstop-dutch:234`); Chinese RoBERTa-wwm base
102.3M (`extract/ling2023-small-fast-bert:121`). RoBERTa-large gave +2.1
overall F1 over base in one paper and −0.4 in another at about 1.5× the
runtime (`extract/alam2020-transformer-punct:182-183`,
`extract/courtland2020-robust-inference:109`). On Vietnamese, PhoBERT-large
with a BiLSTM-CRF head was 2.73 macro F1 above the best base model on News
and 1.21 below it on Novels (see [vietnamese](vietnamese.md)).

## What this does not show

- A small model distilled from, or even compared on equal training data
  with, a strong pretrained encoder **for case restoration**. Every
  small-vs-large case number is missing; the only case comparison is against
  a 2017 BiRNN.
- A per-class case gap for proper names versus sentence-initial words.
- Any small Vietnamese model.
- Phone latency. The one absolute timing is a laptop CPU, one paragraph, no
  variance, model quantized, baseline quantization not stated.
- Parameter counts for the 7 MB model, and accuracy of the quantized model
  as opposed to the float one (the paper does not say which was scored).
- Distillation into a non-Transformer student (CNN, LSTM) from a pretrained
  teacher; the two lines of work do not meet in these papers.
- Robustness of small models to ASR errors: the only small-model ASR-output
  numbers are DistilBERT's (61.8) and Distil-mBERT's.
- Whether the Chinese distillation recipe transfers to a space-delimited
  language with case; its slot-tagging trick depends on inserted mask
  tokens and Chinese word segmentation.
