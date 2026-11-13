# Per-word tagging for punctuation and case: what the formulation is and what has been measured

Grounded from fetched full text (read 2026-11-13). Every number below is
taken from an extract and cited as `extract/<key>:line`, where the key names
the file in the table below (paths relative to `../related-work/`). Sums and
differences marked "our arithmetic" are computed here from cited numbers.

**Sources read**

| Key | Paper | Original | Extract file |
|---|---|---|---|
| `nguyen2026-phopunct` | Nguyen, Huynh, Nguyen 2026, *PhoPunct: A Large-Scale Benchmark of Transformer Architectures for Vietnamese Punctuation Restoration* | [PDF](https://arxiv.org/pdf/2611.09107) · [arXiv](https://arxiv.org/abs/2611.09107) | [extract](../related-work/extract/nguyen2026-phopunct/html/2611.09107.md) |
| `uyen2022-jointcappunc` | Uyen, Tu, Huy, Interspeech 2022, *Vietnamese Capitalization and Punctuation Recovery Models* | [PDF](https://arxiv.org/pdf/2207.01312) · [arXiv](https://arxiv.org/abs/2207.01312) | [extract](../related-work/extract/uyen2022-jointcappunc/html/2207.01312.md) |
| `nguyen2019-chunk-merging` | Nguyen et al. (VAIS), O-COCOSDA 2019, *Fast and Accurate Capitalization and Punctuation for ASR Using Transformer and Chunk Merging* | [PDF](https://arxiv.org/pdf/1908.02404) · [arXiv](https://arxiv.org/abs/1908.02404) | [extract](../related-work/extract/nguyen2019-chunk-merging/html/1908.02404.md) |
| `you2024-cnn-bilstm` | You, Li (Cisco) 2024, *A light-weight and efficient punctuation and word casing prediction model for on-device streaming ASR* | [PDF](https://arxiv.org/pdf/2407.13142) · [arXiv](https://arxiv.org/abs/2407.13142) | [extract](../related-work/extract/you2024-cnn-bilstm/you2024-cnn-bilstm.md) |
| `ling2023-small-fast-bert` | Ling et al. 2023, *A Small and Fast BERT for Chinese Medical Punctuation Restoration* | [PDF](https://arxiv.org/pdf/2308.12568) · [arXiv](https://arxiv.org/abs/2308.12568) | [extract](../related-work/extract/ling2023-small-fast-bert/html/2308.12568.md) |
| `alam2020-transformer-punct` | Alam, Khan, Alam, W-NUT 2020, *Punctuation Restoration using Transformer Models for High- and Low-Resource Languages* | [PDF](https://aclanthology.org/2020.wnut-1.18.pdf) | [extract](../related-work/extract/alam2020-transformer-punct/alam2020-transformer-punct.md) |
| `courtland2020-robust-inference` | Courtland, Faulkner, McElvain (Capital One), IWSLT 2020, *Efficient Automatic Punctuation Restoration Using Bidirectional Transformers with Robust Inference* | [PDF](https://aclanthology.org/2020.iwslt-1.33.pdf) | [extract](../related-work/extract/courtland2020-robust-inference/courtland2020-robust-inference.md) |
| `vandeghinste2023-fullstop-dutch` | Vandeghinste, Guhr 2023, *FullStop: Punctuation and Segmentation Prediction for Dutch with Transformers* | [PDF](https://arxiv.org/pdf/2301.03319) · [arXiv](https://arxiv.org/abs/2301.03319) | [extract](../related-work/extract/vandeghinste2023-fullstop-dutch/html/2301.03319.md) |
| `pais2021-survey` | Păiș, Tufiș 2021, *Capitalization and Punctuation Restoration: a Survey* | [PDF](https://arxiv.org/pdf/2111.10746) · [arXiv](https://arxiv.org/abs/2111.10746) | [extract](../related-work/extract/pais2021-survey/pais2021-survey.md) |

Per-paper reading notes:
[phopunct](../related-work/readings/nguyen2026-phopunct.md) ·
[jointcappunc](../related-work/readings/uyen2022-jointcappunc.md) ·
[chunk-merging](../related-work/readings/nguyen2019-chunk-merging.md) ·
[cnn-bilstm](../related-work/readings/you2024-cnn-bilstm.md) ·
[small-fast-bert](../related-work/readings/ling2023-small-fast-bert.md) ·
[alam2020](../related-work/readings/alam2020-transformer-punct.md) ·
[courtland2020](../related-work/readings/courtland2020-robust-inference.md) ·
[fullstop-dutch](../related-work/readings/vandeghinste2023-fullstop-dutch.md) ·
[pais2021-survey](../related-work/readings/pais2021-survey.md).

The survey was read for its task description, neural-methods section,
evaluation section and conclusions (lines 17–53, 170–371); sections 2.1–2.6
(rules, n-grams, hidden-event LMs, boosting, CRFs) were skimmed.

## The formulation

**One label per word, read off the first subword.** The input is the
lowercased, punctuation-stripped word sequence; the model emits, for each
word, the mark that follows it or "none". The encoder runs on subwords and
the word's label is taken from the final-layer state of its first subword
(`extract/nguyen2026-phopunct:101-105`, `:125`). The 7 MB CNN-BiLSTM does the
same: only the first subword enters the recurrent layers, later subwords are
masked (`extract/you2024-cnn-bilstm:49`, `:103`). Variants seen:

- sum the subword states into a word vector (`extract/uyen2022-jointcappunc:78`);
- predict at every subword and ignore predictions inside a word
  (`extract/alam2020-transformer-punct:168`);
- for Chinese, insert a `[MASK]` slot after each segmented word and classify
  only the slots, so no mark can fall inside a word
  (`extract/ling2023-small-fast-bert:187-199`).

None of the nine sources compares these alignment choices against each other.

**Alternatives to tagging** named in the sources: sequence-to-sequence
"translation" from bare to formatted text, and multimodal models that add
audio (`extract/ling2023-small-fast-bert:23`); character-level models that
predict case per letter and a mark at each space
(`extract/pais2021-survey:172`).

## Label sets

| Source | Punctuation labels | Case labels |
|---|---|---|
| PhoPunct (Vietnamese) | O, Period, Comma, Colon, QMark, Exclam, Semicolon (`extract/nguyen2026-phopunct:87`) | none |
| JointCapPunc (Vietnamese) | O, comma, period, question mark | 0 lower, 1 CAP (first letter), 2 ALL-CAP (`extract/uyen2022-jointcappunc:39-41`) |
| CNN-BiLSTM (English) | O, COMMA, PERIOD, QUESTION | O lower, UPP all-upper, CAP first-letter, MIX mixed such as iPhone, PhD (`extract/you2024-cnn-bilstm:45`) |
| IWSLT 2011 convention (English) | Comma absorbs colons and dashes; Period absorbs exclamation marks and semicolons; Question; O (`extract/alam2020-transformer-punct:89`) | none |
| FullStop (Dutch + 4 languages) | `: - , ? .` and 0 (`extract/vandeghinste2023-fullstop-dutch:28`) | none; input is already truecased (`:126`) |
| Chunk merging (English, seq2seq) | `$` none, `.`, `,`, `?` | U (first or all letters upper) vs L, fused with punctuation into two-symbol tokens such as `U$`, `L,` (`extract/nguyen2019-chunk-merging:111`, `:123`) |
| Chinese medical | O, comma, period, colon (`extract/ling2023-small-fast-bert:205`) | not applicable |

The survey's canonical case scheme is four word-level classes, all-lower,
first-upper, all-upper and mixed-case, written {AL, FU, AU, MC}, with an
optional fifth "no case" class for numbers and symbols
(`extract/pais2021-survey:37`, `:108-114`).

**Mixed case.** A MIX class says a word is mixed-case but not which letters
are upper; the CNN-BiLSTM paper does not describe how the surface form is
recovered. On the IWSLT 2011 test set it reports MIX F1 80.0 at P = R = 80.0,
calls the class very rare, and says twenty percent of MIX words were
predicted CAP (`extract/you2024-cnn-bilstm:142`, `:186`). Earlier BiRNN work
on the same test did not predict the class at all (`:139-140`, `:161`).
Character-level truecasers avoid the problem by labelling letters: two
character RNN systems reach F1 93.2 and 94.0 on a Wikipedia corpus
(`extract/pais2021-survey:340-349`), a different benchmark from every
word-level number here. Grade: single-source for each number.

**Single-letter "I".** The CNN-BiLSTM folds the single-letter-word class used
by earlier work into all-upper (`extract/you2024-cnn-bilstm:161`), so its
UPP F1 of 98.9 (`:142`) is not a measure of acronym recovery.

## Joint or separate heads

Three couplings of the two tasks appear:

1. **Independent heads on a shared encoder.** The CNN-BiLSTM uses two
   softmax branches and a loss \(\mathcal{L} = \mathcal{L}^c + \alpha\mathcal{L}^p\)
   with \(\alpha = 0.7\) (`extract/you2024-cnn-bilstm:73-81`, `:107`). The
   punctuation branch reads the current and next state, the case branch the
   previous and current state (`:67-73`). No single-task ablation is reported.
2. **Punctuation first, case conditioned on it.** Sunkara et al. 2020 (as
   cited, not read) concatenate punctuation probabilities to the encoder
   output before the case layer (`extract/pais2021-survey:202`,
   `extract/uyen2022-jointcappunc:35`).
3. **Case first, punctuation conditioned on it.** JointCapPunc multiplies the
   case probabilities by a learned matrix to get a 256-dimensional "soft
   capitalization embedding", concatenates it to the word vector, and feeds a
   CRF punctuation head; loss \(\lambda\mathcal{L}_{cap} + (1-\lambda)\mathcal{L}_{punc}\)
   with tuned \(\lambda = 0.15\) (`extract/uyen2022-jointcappunc:100-138`, `:174`).

**Measured effect of joint training** — ViCapPunc test set (Vietnamese
medical Q&A text), micro F1, one run per cell
(`extract/uyen2022-jointcappunc:198-249`):

| Encoder | Model | Case P / R / F1 | Punct P / R / F1 |
|---|---|---|---|
| XLM-R | single-task | 84.14 / 82.98 / 83.55 | 79.00 / 77.96 / 78.48 |
| XLM-R | punctuation-then-case (Sunkara-style) | 84.84 / 83.36 / 84.10 | 78.97 / 78.25 / 78.58 |
| XLM-R | JointCapPunc | 85.66 / 85.12 / 85.39 | 79.02 / 78.45 / 78.74 |
| vELECTRA | single-task | 83.97 / 83.10 / 83.53 | 79.35 / 77.96 / 78.65 |
| vELECTRA | punctuation-then-case | 84.67 / 83.65 / 84.16 | 79.36 / 79.31 / 79.33 |
| vELECTRA | JointCapPunc | 86.55 / 86.95 / 86.75 | 80.79 / 79.43 / 80.10 |

Claim: against two separately fine-tuned taggers on the same encoder, joint
training raises case F1 by 1.84 (XLM-R) and 3.22 (vELECTRA) and punctuation
F1 by 0.26 and 1.45 (our arithmetic from the table). Regime: clean written
text, 211,831 training sentences, no seeds or intervals. Grade:
single-source. The survey states that "mixed" studies exist but reports no
controlled joint-vs-separate comparison of its own
(`extract/pais2021-survey:39`).

In the same paper's ablation, removing the case feature from the punctuation
head costs 0.97 punctuation F1 and 3.62 case F1; the text reports different
drops for the FastText row (23.43 and 29.86) than its table (26.02 and
30.63) (`extract/uyen2022-jointcappunc:281-306`, `:322`).

## Encoders and heads

**Encoder size and family, English IWSLT 2011, reference transcripts and ASR
output** — one fine-tuning recipe (encoder + BiLSTM + linear, 256-token
sequences, 10 epochs) across encoders
(`extract/alam2020-transformer-punct:116`, `:164`, `:180-205`):

| Encoder | Ref comma F1 | Ref period F1 | Ref overall F1 | ASR comma F1 | ASR period F1 | ASR overall F1 |
|---|---|---|---|---|---|---|
| DistilBERT-base-uncased | 66.3 | 79.0 | 72.7 | 52.2 | 72.3 | 61.8 |
| BERT-base-uncased | 70.9 | 82.8 | 76.9 | 55.8 | 75.8 | 64.9 |
| ALBERT-base-v2 | 72.7 | 84.5 | 78.4 | 56.1 | 77.7 | 66.0 |
| RoBERTa-base | 74.3 | 86.2 | 80.3 | 59.3 | 78.9 | 68.2 |
| RoBERTa-large | 76.3 | 88.6 | 82.4 | 61.8 | 81.9 | 71.3 |
| mBERT-uncased | 69.2 | 82.7 | 75.9 | 55.4 | 75.0 | 64.6 |
| XLM-R-base | 72.7 | 85.1 | 79.0 | 58.0 | 77.9 | 67.7 |
| XLM-R-large | 76.7 | 87.1 | 81.8 | 61.0 | 81.9 | 70.6 |
| RoBERTa-large + augmentation | 76.7 | 88.9 | 82.9 | 66.3 | 82.3 | 74.0 |

"Overall" is the micro average over the three marks, excluding O. Grade:
benchmark-reported (shared public split; scores are self-reported).
Courtland et al. on the same reference test report RoBERTa-base 83.9 and
RoBERTa-large 83.5 overall and conclude base is enough
(`extract/courtland2020-robust-inference:59-61`, `:109`), where Alam et al.
find large 2.1 points better. Whether large beats base on this benchmark is
contested between these two papers; both are single runs on a 12.6k-word
test set with 46 question marks (`extract/alam2020-transformer-punct:67`).

**Head variants.**

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| A BiLSTM-CRF head does not beat a linear head | Vietnamese News and Novels, four base encoders, one shared budget (8 epochs, lr 2e-5), macro F1 over 7 labels | Plain ≥ BiLSTM-CRF in 7 of 8 pairs; XLM-R 58.25 vs 57.89 News, 49.79 vs 46.90 Novels; ViBERT 49.82 vs 45.91 Novels (`extract/nguyen2026-phopunct:272-281`) | single-source, one seed |
| A CRF alone gives under half a point | same | XLM-R + CRF 58.62 / 50.18 vs plain 58.25 / 49.79 (`extract/nguyen2026-phopunct:247-255`, `:264`) | single-source |
| A CRF gives nothing on English | IWSLT 2011, RoBERTa-large | Ref 82.4 both; ASR 71.3 linear vs 70.9 CRF (`extract/alam2020-transformer-punct:270-271`, `:299`) | single-source |
| A CRF helps in the joint model | ViCapPunc, vELECTRA | punctuation F1 80.10 with CRF vs 78.71 softmax; case F1 86.75 vs 83.98 (`extract/uyen2022-jointcappunc:272-297`) | single-source |

Taken together the CRF's value is **contested**: two controlled comparisons
find none, one finds +1.39. The PhoPunct authors attribute their result
partly to under-training new head parameters at the encoder's learning rate
and do not claim tuned heads are useless (`extract/nguyen2026-phopunct:307`).
In the JointCapPunc ablation a change to the punctuation head moved case F1
by 2.77, which the paper does not explain.

Adding self-attention on top of the small CNN-BiLSTM lowered overall
punctuation F1 from 71.0 to 69.6 and left case F1 at 87.8
(`extract/you2024-cnn-bilstm:131-132`, `:141-142`).

**Losses for class imbalance.** Focal loss, class weighting and both together
did not beat plain cross-entropy on IWSLT
(`extract/courtland2020-robust-inference:86`). A supervised contrastive term
during distillation pre-training was worth 1.16 overall F1 in one Chinese
ablation (86.72 vs 85.56; `extract/ling2023-small-fast-bert:342-344`).

## Long or unsegmented input

ASR output has no sentence boundaries, so the tagger sees fixed windows and
the words near a window edge lack context on one side.

| Method | What it does | Measured | Grade |
|---|---|---|---|
| Fill-to-length windows | Pack whole words until 256 subwords (or 200 for the small model) and start the next window at the overflow word (`extract/alam2020-transformer-punct:164`, `:209`; `extract/you2024-cnn-bilstm:101-103`) | no ablation | — |
| Sentence-aligned segments | 150-word segments that end at a sentence end (`extract/uyen2022-jointcappunc:41`) | no ablation; unavailable at inference on real ASR output | — |
| Overlapped chunk merging | Chunks of \(k\) words advanced by \(k/2\); in each overlap drop the last `min_words_cut` words of the earlier chunk and keep the later chunk's (`extract/nguyen2019-chunk-merging:78-80`) | English BNC, seq2seq Evolved Transformer, per-class F1 with vs without: upper-case 0.87 vs 0.81, period 0.73 vs 0.61, comma 0.56 vs 0.41, question 0.71 vs 0.56 (`:229-272`). With a seq2seq LSTM the gain is 0.01–0.02 per class (`:164-207`). Best cut is mid-overlap, 4–10 of 15 words; case is insensitive to it (`:146`, `:363`) | single-source; a seq2seq model, not a tagger |
| Sum over overlapping windows | Each token is predicted in several 100-token windows; pre-softmax activations are summed (`extract/courtland2020-robust-inference:39`, `:72`) | IWSLT reference, RoBERTa-base, overall F1 by predictions per token: 1 → 76.3, 2 → 79.4, 3 → 81.8, 6 → 83.2, 9 → 83.9; CPU cost 1×, 1.8×, 2.6×, 5.2×, 7.7× (`:92-99`). Summing activations beat averaging probabilities by 0.3 (`:107`) | single-source |
| Vote over sliding windows | 200-word window slid over the stream; a boundary is accepted when predicted in more than a fraction \(\theta\) of the windows containing the word (`extract/vandeghinste2023-fullstop-dutch:27-32`) | Dutch, out-of-domain subtitles, sentence-boundary F1 0.8742 (period only) and 0.9053 (period or question) for the best model, against 0.4219 for a seq2seq baseline (`:316-326`). \(\theta\) had no significant effect (`:403`) | single-source |

Caution on the Courtland numbers: their network classifies a whole window
through a layer that concatenates all token states, and its single-pass
score of 76.3 is below the 80.3 a plain per-token RoBERTa-base tagger gets
on the same test in Alam et al. (`extract/alam2020-transformer-punct:182`).
The 7.6-point aggregation gain may therefore be partly repair of that
architecture; no source measures window aggregation on a plain per-token
tagger.

## Training data from written text, and ASR-error augmentation

**Construction.** Every source builds labels by stripping punctuation (and
case) from formatted text; the survey describes this as the standard
procedure (`extract/pais2021-survey:254`). Details that vary:

- which marks are kept and which sentences are discarded: the CNN-BiLSTM
  drops any sentence containing a mark outside comma, period, question
  (`extract/you2024-cnn-bilstm:87`); JointCapPunc and chunk merging delete
  other marks and keep the sentence (`extract/uyen2022-jointcappunc:41`,
  `extract/nguyen2019-chunk-merging:84`);
- the source mix: 55M English words, 57.6% Wikipedia, 25.3% interview
  transcripts, 17.1% TED, with Wikipedia chosen for its proper nouns
  (`extract/you2024-cnn-bilstm:87-97`);
- FullStop keeps true case in the input because its ASR system emits it
  (`extract/vandeghinste2023-fullstop-dutch:126`), so its scores do not
  transfer to an all-caps or all-lower input.

**Mismatch between written training text and speech.**

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| ASR output costs about 11 overall F1 against reference transcripts, mostly comma precision | IWSLT 2011, RoBERTa-large, trained on TED transcripts | overall 82.4 → 71.3; comma P 76.9 → 56.6; question F1 81.9 → 58.1 (`extract/alam2020-transformer-punct:183`, `:197`) | benchmark-reported |
| Earlier systems lose about 4 | same test, four pre-2021 systems | e.g. 77.8 → 73.3, 72.9 → 68.8 (`extract/pais2021-survey:309-318`) | benchmark-reported |
| Register shift costs more than ASR errors | Bangla, XLM-R-large trained on news; tested on news, manual transcripts of read stories, and ASR output at 14.8% WER | overall F1 87.0 news, 68.8 manual transcript, 63.2 ASR; comma F1 81.2, 38.1, 36.9 (`extract/alam2020-transformer-punct:95`, `:229`, `:234`, `:239`) | single-source |

**Augmentation.** Alam et al. corrupt each training batch on the fly: with
probability \(\alpha\) a token is changed; the change is a substitution by
the unknown token (label kept), a deletion (token and label removed) or an
insertion of the unknown token with label O
(`extract/alam2020-transformer-punct:150-156`). Best setting
\(\alpha = 0.15\), \(\alpha_{sub} = 0.4\), \(\alpha_{del} = 0.4\) (`:217`).
RoBERTa-large on IWSLT (`:280-291`):

| Augmentation | Ref overall F1 | ASR overall F1 | ASR comma P / F1 |
|---|---|---|---|
| none | 82.4 | 71.3 | 56.6 / 61.8 |
| substitution, unknown token | 83.3 | 72.4 | 57.0 / 63.1 |
| substitution, random token | 82.9 | 71.7 | 57.2 / 62.7 |
| deletion | 82.1 | 73.1 | 60.0 / 64.8 |
| insertion | 82.9 | 71.6 | 57.4 / 61.9 |
| all three | 82.9 | 74.0 | 64.1 / 66.3 |

Claim: +2.7 overall F1 on ASR output against the same model without
augmentation, from precision. Grade: single-source, one run, a 12.8k-word
test set. On Bangla the same augmentation moved ASR overall F1 from 63.2 to
64.0 and reference from 68.8 to 69.5 (`:234-240`), which the authors call
marginal (`:248`).

Two further approaches are reported second-hand by the survey (as cited, not
read): training a CRF sentence-end detector on noisy ASR output gained 2% F1
over training on clean transcripts (`extract/pais2021-survey:168`), and
Sunkara et al. add ASR output aligned to reference text
(`extract/pais2021-survey:202`).

## Evaluation metrics and their pitfalls

- **What "overall" means differs.** IWSLT papers micro-average over the
  punctuation classes only (`extract/you2024-cnn-bilstm:111`). FullStop's
  micro F1 includes the no-punctuation class and reads 0.983 where the macro
  F1 over the same predictions is 0.789
  (`extract/vandeghinste2023-fullstop-dutch:191-198`). PhoPunct reports
  macro F1 only (`extract/nguyen2026-phopunct:226`). These three numbers are
  not comparable.
- **Macro F1 is hostage to rare classes.** PhoPunct's Novels test has 320
  colons and 6 semicolons; both leading systems score 0.00 on semicolon, and
  colon F1 is 0.19 for one and 0.00 for the other
  (`extract/nguyen2026-phopunct:89`, `:295`). The best macro F1 values, 61.35
  News and 50.18 Novels (`:260`, `:255`), therefore say little about comma
  and period, and the paper gives per-class scores only as a figure.
- **Tiny test sets.** IWSLT 2011 has 46 question marks in the reference test
  and 35 in the ASR test (`extract/alam2020-transformer-punct:67-68`);
  question-mark F1 swings by 5–9 points between otherwise similar rows
  (`:281-285`).
- **Class conflation.** IWSLT's Comma includes colons and dashes and its
  Period includes exclamation marks and semicolons
  (`extract/alam2020-transformer-punct:89`).
- **Position versus identity.** Merging to "any mark vs none" raises Bangla
  ASR F1 from 64.0 (4 classes) to 80.6 (2 classes)
  (`extract/alam2020-transformer-punct:255-257`).
- **Gold punctuation is not unique.** A human-agreement study on other data
  is cited at about 76% for location and 70% for the same mark
  (`extract/courtland2020-robust-inference:127`, as cited, not read);
  FullStop's error walk-through finds most comma disagreements defensible
  (`extract/vandeghinste2023-fullstop-dutch:276`).
- **Case metrics pool unlike things.** Chunk merging merges first-upper and
  all-upper into one U class (`extract/nguyen2019-chunk-merging:123`);
  JointCapPunc reports one micro F1 over CAP and ALL-CAP
  (`extract/uyen2022-jointcappunc:168`). No source separates sentence-initial
  capitals from proper-name capitals.
- **Slot error rate** is converted by \(1 - F \approx 0.7\,\mathrm{SER}\) in
  the survey (`extract/pais2021-survey:301-303`).

**Which classes are hard.** Comma has the lowest F1 of the three common marks
in every neural system tabulated on IWSLT, with period ahead by more than 10
F1 (`extract/pais2021-survey:299`, `:332`), and the same ordering holds in
Dutch, Bangla and the small English model
(`extract/vandeghinste2023-fullstop-dutch:192-193`,
`extract/alam2020-transformer-punct:261`,
`extract/you2024-cnn-bilstm:159`). Grade: reproduced in direction across
independent groups. Comma errors are mostly omissions: precision exceeds
recall on reference text (`extract/pais2021-survey:338`); on ASR output with
a strong encoder the sign flips, P 56.6 vs R 67.9
(`extract/alam2020-transformer-punct:197`). For case, the most frequent CAP
error in the small model is CAP predicted as lower, which the authors
attribute to missed periods and question marks
(`extract/you2024-cnn-bilstm:186`).

## What this does not show

- No source evaluates a tagger on input that is all upper-case with numbers
  spelled out, or measures the effect of number spell-out on punctuation.
- No source separates sentence-initial from proper-name capitalisation, so
  "which capitals are hard" is not measured here.
- Joint-vs-separate evidence is one paper, one dataset, single runs.
- Window aggregation is measured on a non-standard head (Courtland), on a
  seq2seq model (chunk merging) and for sentence boundaries only (FullStop);
  not on a plain two-head tagger.
- Streaming or low-latency operation (limited right context) is not measured
  in any of the nine; the "streaming" CNN-BiLSTM is bidirectional over
  200-token sequences.
- ASR-error augmentation is tested with unknown-token noise only; realistic
  confusions (homophones, Vietnamese tone or syllable errors) are untested.
- Prosody is out of scope here; the survey reports that models adding pause
  duration beat text-only ones in the work it covers
  (`extract/pais2021-survey:363-365`).
