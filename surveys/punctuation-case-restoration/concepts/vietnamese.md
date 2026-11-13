# Vietnamese punctuation and case restoration: datasets, models, scores

Grounded from fetched full text (read 2026-11-13). Numbers are cited as
`extract/<key>:line`; the key names the extract file listed below (paths
relative to `../related-work/`). Works marked **as cited, not read** are
known here only through what a read paper says about them.

**Sources read**

- Nguyen, Huynh, Nguyen (AISIA), 2026, *PhoPunct: A Large-Scale Benchmark of
  Transformer Architectures for Vietnamese Punctuation Restoration* —
  [PDF](https://arxiv.org/pdf/2611.09107) · [arXiv](https://arxiv.org/abs/2611.09107) ·
  [extract](../related-work/extract/nguyen2026-phopunct/html/2611.09107.md) ·
  [reading note](../related-work/readings/nguyen2026-phopunct.md)
- Uyen, Tu, Huy, Interspeech 2022, *Vietnamese Capitalization and Punctuation
  Recovery Models* —
  [PDF](https://arxiv.org/pdf/2207.01312) · [arXiv](https://arxiv.org/abs/2207.01312) ·
  [extract](../related-work/extract/uyen2022-jointcappunc/html/2207.01312.md) ·
  [reading note](../related-work/readings/uyen2022-jointcappunc.md)
- Nguyen et al. (Vietnam Artificial Intelligence System, VAIS), O-COCOSDA
  2019, *Fast and Accurate Capitalization and Punctuation for ASR Using
  Transformer and Chunk Merging* —
  [PDF](https://arxiv.org/pdf/1908.02404) · [arXiv](https://arxiv.org/abs/1908.02404) ·
  [extract](../related-work/extract/nguyen2019-chunk-merging/html/1908.02404.md) ·
  [reading note](../related-work/readings/nguyen2019-chunk-merging.md)

The other six papers read for this survey (see
[tagger-formulation](tagger-formulation.md)) contain no Vietnamese data or
results.

**Two corrections to how these papers are usually filed.** The chunk-merging
paper is from a Vietnamese group (affiliation VAIS and four Vietnamese
universities, `extract/nguyen2019-chunk-merging:13-20`; the extract shows no
Viettel affiliation) but trains and tests only on the English British
National Corpus (`:121`). PhoPunct is a punctuation-only benchmark; it has
no capitalisation labels or results (`extract/nguyen2026-phopunct:101`).

## Datasets

| Dataset | Size | Domain | Labels | Availability | First described in |
|---|---|---|---|---|---|
| News and Novels | 22,137,597 labelled tokens: News 11,939,762 train / 4,003,912 validation / 3,958,621 test; Novels 1,350,500 / 358,791 / 526,011 (`extract/nguyen2026-phopunct:53-63`) | journalistic prose; literary prose with dialogue (`:49`, `:69`) | O, Period, Comma, Colon, QMark, Exclam, Semicolon; punctuation only (`:87`) | public files released by Pham et al. 2020, CoNLL-style one token per line; no source-document identifiers (`:49`, `:73`). Licence not stated; the authors warn the text "may contain copyrighted material" (`:331`) | Pham et al. 2020 (as cited, not read) |
| ViCapPunc | 425,350 sentences from 50,000 question–answer pairs; 211,831 train / 85,084 validation / 128,435 test sentences (`extract/uyen2022-jointcappunc:39`, `:64`) | medical Q&A crawled from Vinmec, Alobacsi, ISOFHCARE (`:39`) | case: 0, CAP, ALL-CAP; punctuation: O, COMMA, PERIOD, QMARK (`:39-41`) | released with code at `github.com/anhtunguyen98/JointCapPunc` (`:9`); licence not stated in the paper | Uyen et al. 2022 |
| Pham et al. 2019 corpus | 500 news articles and 100 movie-subtitle transcripts (`extract/nguyen2026-phopunct:37`) | news; subtitles | period, comma for news; plus question and exclamation marks for subtitles (`:37`) | not stated | as cited, not read |

ViCapPunc label counts (`extract/uyen2022-jointcappunc:56-64`):

| Label | Train | Validation | Test |
|---|---|---|---|
| COMMA | 228,495 | 92,026 | 137,865 |
| PERIOD | 184,383 | 74,097 | 111,717 |
| QMARK | 27,448 | 10,987 | 16,718 |
| CAP | 318,654 | 127,222 | 191,767 |
| ALL-CAP | 37,542 | 14,582 | 23,173 |

Notes that matter for use:

- **Splits.** ViCapPunc was split 50% / 20% / 30% at random over Q&A pairs
  (`extract/uyen2022-jointcappunc:41`); News and Novels keep the inherited
  splits, and duplication across splits cannot be audited
  (`extract/nguyen2026-phopunct:73`, `:323`).
- **Size discrepancy.** Tran et al. 2021 report about 742K sentences on what
  PhoPunct says is the same corpus; PhoPunct notes the mismatch without
  explaining it (`extract/nguyen2026-phopunct:17`, `:49`).
- **Syllables or segmented words.** Neither paper says whether tokens are
  whitespace syllables or word-segmented units. PhoPunct calls them "words"
  and "lexical tokens" from the distributed file and says nothing about
  running a word segmenter before PhoBERT (`extract/nguyen2026-phopunct:73`,
  `:101-105`). The one ViCapPunc example shows one syllable per row (chào,
  uyên, bạn, có, khoe, không; `extract/uyen2022-jointcappunc:47-52`), which
  fits syllable tokens but does not settle it since each is also a
  one-syllable word. Check the files before relying on either reading.
- **"Spoken language" in ViCapPunc is typed text.** The authors describe the
  Q&A pairs as containing spoken-language context
  (`extract/uyen2022-jointcappunc:22`); they are website posts, not
  transcripts.
- **Segmenting.** ViCapPunc is cut into 150-word segments that end at a
  sentence end (`extract/uyen2022-jointcappunc:41`). Every segment therefore
  ends in a sentence-final mark and starts with a capital, which real ASR
  windows do not.
- **Class balance.** In News and Novels the gap between O and the rarest
  marks is several orders of magnitude; the Novels test has 320 colons and 6
  semicolons (`extract/nguyen2026-phopunct:87-89`). Per-class counts are
  given only as a log-scale figure.

## Models and scores

### Punctuation only: PhoPunct benchmark

Setup: 17 models, each trained once for 8 epochs at lr 2e-5, batch 16, max
256 subwords, selected on validation macro F1; input lowercased and stripped
(`extract/nguyen2026-phopunct:103`, `:208-218`, `:204`). Metric: macro F1 (%)
over the label set (`:226`, `:262`).

| Encoder | Plain News / Novels | +BiLSTM | +CRF | +BiLSTM+CRF |
|---|---|---|---|---|
| mBERT (cased) | 53.71 / 43.84 | 53.90 / 42.56 | 53.76 / 43.39 | 53.54 / 42.37 |
| vELECTRA | 53.80 / 40.70 | 53.42 / 40.46 | 53.84 / 40.64 | 53.45 / 40.22 |
| ViBERT (vibert4news) | 57.47 / 49.82 | 57.74 / 45.87 | 57.97 / 49.78 | 57.66 / 45.91 |
| XLM-R base | 58.25 / 49.79 | 58.07 / 46.83 | 58.62 / 50.18 | 57.89 / 46.90 |
| PhoBERT-large (PhoPunct) | — | — | — | 61.35 / 48.97 |

(`extract/nguyen2026-phopunct:244-260`.)

Claims, each single-source, one seed, clean written text:

- Against the best base-size encoder with the same head family, PhoBERT-large
  with BiLSTM-CRF is 2.73 macro F1 higher on News (61.35 vs 58.62) and 1.21
  lower on Novels (48.97 vs 50.18) (our arithmetic). Size and encoder family
  are confounded, as the paper says (`:121`), and PhoBERT-large was run with
  only one head.
- Among base encoders XLM-R leads and vELECTRA is last, 4.45 below XLM-R on
  News and 9.09 below on Novels with a plain head (our arithmetic).
- Extra heads do not help under this budget; see
  [tagger-formulation § Encoders and heads](tagger-formulation.md#encoders-and-heads).

**Per-class scores are not in the text.** They appear only in a figure; the
text gives colon F1 on Novels as 0.19 for XLM-R+CRF and 0.00 for PhoPunct,
and semicolon F1 0.00 for both (`:295`). No Vietnamese comma or period F1
can be quoted from this paper.

### Case and punctuation jointly: JointCapPunc

Setup: encoder XLM-R or vELECTRA, subword states summed per word, a case
head whose probabilities feed a CRF punctuation head; batch 32, 10 epochs,
lr 5e-5, loss weight 0.15, model picked by mean of the two validation F1
scores (`extract/uyen2022-jointcappunc:78`, `:100-138`, `:174`). Metric:
micro P/R/F1 per task on the ViCapPunc test set.

| Encoder | Model | Case F1 | Punctuation F1 |
|---|---|---|---|
| XLM-R | single-task | 83.55 | 78.48 |
| XLM-R | punctuation-then-case baseline | 84.10 | 78.58 |
| XLM-R | JointCapPunc | 85.39 | 78.74 |
| vELECTRA | single-task | 83.53 | 78.65 |
| vELECTRA | punctuation-then-case baseline | 84.16 | 79.33 |
| vELECTRA | JointCapPunc | 86.75 | 80.10 |
| FastText embeddings in place of the encoder | JointCapPunc | 60.73 | 49.47 |

(`extract/uyen2022-jointcappunc:198-249`, `:299-306`.) Precision and recall
for the best model: case 86.55 / 86.95, punctuation 80.79 / 79.43 (`:244-248`).

Claims, single-source, single runs:

- Best Vietnamese joint result read: case F1 86.75 and punctuation F1 80.10
  with a base-size Vietnamese encoder on in-domain written medical text.
- Without a pretrained contextual encoder the same architecture falls to
  60.73 and 49.47, with recall 49.05 and 41.03 (`:303-305`). This is the only
  Vietnamese number for a non-pretrained model, and FastText plus two feed-
  forward heads is a weak stand-in for a trained-from-scratch small tagger.
- **Encoder ranking flips between the two papers.** Here vELECTRA beats
  XLM-R (80.10 vs 78.74 punctuation); in PhoPunct vELECTRA is the worst base
  encoder. Datasets, label sets, metrics and which XLM-R size was used here
  (not stated) all differ, so this is an open inconsistency, not a ranking.

**No per-class scores.** The paper reports neither comma / period / question
F1 nor CAP versus ALL-CAP F1, and does not separate sentence-initial from
proper-name capitals.

## Real ASR output versus clean text

**None of the Vietnamese results read here was measured on ASR output.**

- PhoPunct tests on the written News and Novels test splits and lists
  conversational ASR as outside its coverage and as future work
  (`extract/nguyen2026-phopunct:323`, `:327`).
- JointCapPunc tests on written Q&A text. It names medical ASR as the target
  application (`extract/uyen2022-jointcappunc:20`) but reports no ASR
  experiment, and states that its encoder may be too slow for an ASR
  pipeline, leaving a smaller model to future work (`:326`).
- The chunk-merging paper "simulates" ASR output by lowercasing and
  stripping English text (`extract/nguyen2019-chunk-merging:84`).

The only measured clean-to-ASR gaps in the nine papers are English and
Bangla ([tagger-formulation § Training data](tagger-formulation.md#training-data-from-written-text-and-asr-error-augmentation)).

## Public artifacts mentioned

| Artifact | What the paper says | Citation |
|---|---|---|
| PhoPunct code | `github.com/aisia-research-lab/PhoPunct`; "source code" — trained checkpoints are not mentioned | `extract/nguyen2026-phopunct:9` |
| JointCapPunc code and ViCapPunc data | `github.com/anhtunguyen98/JointCapPunc`; checkpoints not mentioned | `extract/uyen2022-jointcappunc:9` |
| Encoders used | `bert-base-multilingual-cased`, `xlm-roberta-base`, `FPTAI/velectra-base-discriminator-cased`, `NlpHUST/vibert4news-base-cased`, PhoBERT-large | `extract/nguyen2026-phopunct:113-121` |
| Encoder pre-training data | PhoBERT: 20 GB Vietnamese; vELECTRA: 10 GB Vietnamese; XLM-R: 2.5 TB multilingual of which 137 GB Vietnamese | `extract/nguyen2026-phopunct:121`, `extract/uyen2022-jointcappunc:172` |

No paper read here names a released Vietnamese punctuation or case
checkpoint. The public multilingual FullStop models cover English, German,
French, Italian and Dutch only
(`extract/vandeghinste2023-fullstop-dutch:164`), and the sherpa-onnx models
named in the CNN-BiLSTM paper are English and Chinese–English
(`extract/you2024-cnn-bilstm:165`).

## Other Vietnamese work cited by these papers (as cited, not read)

| Work | What the citing paper says | Citation |
|---|---|---|
| Pham, Nguyen, Cuong 2019, *Punctuation prediction for Vietnamese texts using conditional random fields* (SoICT) | early CRF formulation; 500 news articles and 100 subtitle transcripts; period and comma for news, plus question and exclamation marks for subtitles | `extract/nguyen2026-phopunct:37`, `:346` |
| Pham, Nguyen, Pham, Cao, Nguyen 2020, *Vietnamese punctuation prediction using deep neural networks* (SOFSEM) | seven-category DNN; released the News and Novels corpus (22.1M tokens); did not compare its sequence heads with a plain classifier. Uyen et al.: the only two public Vietnamese punctuation datasets, news and novels, with no spoken language and no case labels; source of the 150-word maximum length | `extract/nguyen2026-phopunct:16`, `:37`; `extract/uyen2022-jointcappunc:18`, `:33`, `:41` |
| Tran, Dinh, Pham, Nguyen 2021, *An efficient transformer-based model for Vietnamese punctuation prediction* (IEA/AIE) | mBERT, XLM-R and Vietnamese encoders on News and Novels, about 742K sentences; sub-point gains from adding sequence layers to its strongest backbone. Uyen et al. use it as their single-task punctuation baseline: a CRF layer on a pretrained encoder | `extract/nguyen2026-phopunct:17`, `:27`, `:37`; `extract/uyen2022-jointcappunc:178`, `:362` |
| O. T. Tran et al. 2021, *Punctuation prediction in Vietnamese ASRs using transformer-based models* (PRICAI) | cited only as an example of pretrained models applied to punctuation prediction | `extract/uyen2022-jointcappunc:24`, `:345` |
| T. T. H. Nguyen et al. 2021, *Toward human-friendly ASR systems: recovering capitalization and punctuation for Vietnamese text* (IEICE Trans.) | example of fusing case and punctuation annotations into one sequence-labelling tag set | `extract/uyen2022-jointcappunc:35`, `:351` |
| T. B. Nguyen et al. 2020, *Improving Vietnamese named entity recognition from speech using word capitalization and punctuation recovery models* (Interspeech) | cited for the claim that restoring case and punctuation helps downstream tasks such as NER | `extract/uyen2022-jointcappunc:18`, `:335` |
| O. T. Tran, V. T. Bui 2021, *Neural text normalization in speech-to-text systems with rich features* (Applied AI) | cited among CRF-plus-CNN/LSTM approaches | `extract/uyen2022-jointcappunc:24`, `:342` |
| T. O. Tran, P. Le Hong et al. 2020, *Improving sequence tagging for Vietnamese text using transformer-based neural models* (PACLIC) | source of vELECTRA | `extract/uyen2022-jointcappunc:172`, `:347` |
| Huyen et al. 2026, *End-to-end Vietnamese ASR with acoustic-aware punctuation and capitalization for edge devices* (JST Smart Systems and Devices) | puts punctuation and capitalisation into the ASR output vocabulary for edge deployment, removing the separate restoration module but coupling formatting to acoustic training | `extract/nguyen2026-phopunct:37`, `:341` |
| Vu, Nguyen, Nguyen 2026, *Vietnamese automatic speech recognition: a revisit* (Findings of EACL) | a large-scale ASR data pipeline that restores punctuation and capitalisation with a separately fine-tuned text model | `extract/nguyen2026-phopunct:37`, `:351` |
| Nguyen and Nguyen 2020, *PhoBERT* (Findings of EMNLP) | monolingual Vietnamese encoder, 20 GB, RoBERTa objective | `extract/nguyen2026-phopunct:121`, `:345` |

PhoPunct's own comparison table lists Uyen et al. 2022 as the only case +
punctuation study among the Vietnamese works it surveys
(`extract/nguyen2026-phopunct:13-19`); Uyen et al. cite T. T. H. Nguyen et
al. 2021 as another.

## What this does not show

- Any Vietnamese result on ASR output, on spontaneous speech, or on text with
  recognition errors.
- Per-class Vietnamese F1 for comma, period, CAP or ALL-CAP in a form that
  can be quoted; PhoPunct's is a figure and JointCapPunc reports aggregates.
- Any Vietnamese capitalisation result outside one medical Q&A dataset, and
  none on news or names-heavy text.
- Mixed-case words: ViCapPunc has only CAP and ALL-CAP labels.
- Any small or distilled Vietnamese model, any latency or size figure. The
  nearest evidence is the FastText ablation above.
- Input conditions matching the target ASR system: all upper-case and
  numbers spelled out. Both datasets keep written digits and other written
  forms as far as the papers say.
- Whether a large encoder helps case restoration: PhoBERT-large was tested
  on punctuation only.
- Seeds or confidence intervals; both papers are single runs
  (`extract/nguyen2026-phopunct:323`).
