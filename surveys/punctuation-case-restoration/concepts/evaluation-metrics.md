# Measuring punctuation and case on ASR output

Grounded from fetched full text (2026-11-13). Every number below is quoted
from a local extract and cited as `tag:line`. No figure comes from recall.

**Sources read** (full text; `tag` is the citation prefix used below):

- `M` — Meister et al. (NVIDIA), ASRU 2023, *LibriSpeech-PC: Benchmark for
  Evaluation of Punctuation and Capitalization Capabilities of end-to-end ASR
  Models* — [HTML](https://arxiv.org/html/2310.02943) ·
  [PDF](https://arxiv.org/pdf/2310.02943) ·
  [extract](../related-work/extract/meister2023-librispeech-pc/html/2310.02943.md)
- `K` — Kim et al. (NAVER), 2023, *Improved Training for End-to-End Streaming
  ASR Model with Punctuation* — [HTML](https://arxiv.org/html/2306.01296) ·
  [PDF](https://arxiv.org/pdf/2306.01296) ·
  [extract](../related-work/extract/kim2023-e2e-streaming-punct/html/2306.01296.md)
- `Y` — You et al. (Cisco), 2025, *Enhancing Fully Formatted End-to-End
  Speech Recognition with Knowledge Distillation via Multi-Codebook Vector
  Quantization* — [PDF](https://arxiv.org/pdf/2512.18967) ·
  [arXiv](https://arxiv.org/abs/2512.18967) ·
  [extract](../related-work/extract/you2025-formatted-e2e-distill/you2025-formatted-e2e-distill.md)
- `Ko` — Koluguri et al. (NVIDIA), 2024, *Longer is (Not Necessarily)
  Stronger* — [HTML](https://arxiv.org/html/2409.05601) ·
  [PDF](https://arxiv.org/pdf/2409.05601) ·
  [extract](../related-work/extract/koluguri2024-punctuated-long-seq/html/2409.05601.md)
- `G` — Gris et al., 2023, *Evaluating OpenAI's Whisper ASR for Punctuation
  Prediction and Topic Modeling of life histories of the Museum of the
  Person* — [HTML](https://arxiv.org/html/2305.14580) ·
  [PDF](https://arxiv.org/pdf/2305.14580) ·
  [extract](../related-work/extract/gris2023-whisper-punct/html/2305.14580.md)
- `Z` — Zhu, Wu, Cheng, Wang (ByteDance), 2022, *Unified Multimodal
  Punctuation Restoration Framework for Mixed-Modality Corpus* —
  [HTML](https://arxiv.org/html/2202.00468) ·
  [PDF](https://arxiv.org/pdf/2202.00468) ·
  [extract](../related-work/extract/zhu2022-unipunc/html/2202.00468.md)

## The problem

A text restorer evaluated on reference words is a tagging task: one label
per word, so per-class precision, recall and F1 are well defined (`Z:36`).
On recogniser output the hypothesis words differ from the reference, the
label sequences have different lengths, and a per-word comparison no longer
exists. The sources handle this in four ways.

## Metrics in use

| Metric | Definition | Used by | What it hides |
|---|---|---|---|
| Per-class P / R / F1 on reference words | tag each reference word with the mark that follows it; score per mark; "overall" pools the marks | `Z:338`; the IWSLT 2011 and Fisher results quoted in `G:59-71` | all recognition errors; says nothing about the deployed pipeline |
| Per-class F1 on zero-WER utterances | keep only utterances the system recognised perfectly, then score as above | `M:389`, `Y:95` | most of the test set, and a different part of it per system (below) |
| Per-class P / R / F1 after alignment | align hypothesis to reference first, then score marks | `K:240`; Nozaki as described at `G:73`; `G:464-472` | the alignment rule, which no source specifies precisely enough to reproduce; what happens to a mark next to a misrecognised word |
| WER, WER C, WER PC | word error rate on normalised text, on cased text without punctuation, and on cased text with each mark as a token | `M:55`, `M:395`; `Y:95`; Koluguri's four columns `Ko:227-238` | punctuation errors, diluted by the much larger number of word tokens; which mark failed |
| PER (punctuation error rate) | errors on punctuation tokens only, after a word-level alignment in which every mark is masked to one `[PUNCT]` symbol | `M:83-121` | case entirely; per-mark detail unless broken out; sensitivity to how the masked alignment places marks near word errors |
| Slot error rates on a Damerau-Levenshtein alignment | named as the third family | `M:57` (Guan 2020, not read) | not described further in any extract |
| Readability or downstream proxy | BLANC score of a punctuation-segmented video summary, with and without punctuation | `G:549`, `G:560-590` | anything about individual marks; it measures segmentation usefulness for one application |

## PER in detail

PER is defined as
\[ \mathrm{PER} = \frac{I_P + D_P + S_P}{I_P + D_P + S_P + C_P} \]
over punctuation tokens only (`M:88`). The steps (`M:67`, `M:101-116`):

1. Replace every punctuation token on both sides by `[PUNCT]`.
2. Run the usual Levenshtein alignment over words and `[PUNCT]`.
3. Where a reference `[PUNCT]` is aligned to a hypothesis `[PUNCT]`, compare
   the actual marks: equal is correct (\(C_P\)), unequal is a substitution
   (\(S_P\)).
4. Deletions and insertions follow from counts:
   \(D_P = N_{P,\mathrm{ref}} - (S_P + C_P)\),
   \(I_P = N_{P,\mathrm{hyp}} - (S_P + C_P)\).

The denominator includes insertions, so PER lies between 0 and 1, unlike WER
(`M:136`). It is computed on every utterance whatever the word errors, which
is its advantage over zero-WER F1.

Worked examples from the paper: reference "I was done ." against "I was
done" gives PER 100.0% and WER PC 25.0% (`M:407`); "Let's eat , Bob !"
against "Let's eat Bob !" gives PER 50.0% and WER PC 20.0% (`M:409`).

A per-mark breakdown is possible and is the informative form: on
LibriSpeech-PC test-clean, period PER 24.01%, comma 33.26%, question mark
15.99%, with separate correct, deletion, insertion and substitution-target
rates (`M:417-426`).

## Measured disagreements between metrics

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Zero-WER F1 discards a third to a half of the test set, and a different part for each system | LibriSpeech-PC, two systems | zero-WER utterances: 66.94% and 66.40% of test-clean, 48.17% and 50.38% of test-other (`M:199`, `M:211`, `M:223`, `M:235`); utterances perfect for both: 375 (15.5%) and 1119 (39.1%) (`M:391`). A better recogniser changes the subset: 76% and 59% for Zipformer (`Y:117-119`) | benchmark-reported (two groups, same test set) |
| Zero-WER F1 compresses differences that PER shows | same two systems, test-clean | punctuation F1 84.75 vs 87.40 (`M:204`, `M:216`), a 2.65-point gap, where PER is 36.60 vs 29.48 (`M:313`, `M:324`), a 7.12-point gap | single-source; the gaps are our subtraction |
| Zero-WER F1 and PER describe the same system very differently | formatted Conformer | punctuation F1 87.40 on its perfect utterances (`M:216`) and PER 29.48 on all utterances (`M:324`) | single-source |
| WER PC can move by a factor of nearly three while PER barely moves | cascade before and after tuning its text model | WER PC 26.36 → 9.45, PER 38.38 → 36.60, WER C 4.83 → 5.09 (`M:302-305`, `M:313-316`) | single-source; with case nearly unchanged and PER nearly unchanged, the paper does not say which tokens account for the WER PC drop |
| PER and plain WER can move in opposite directions | adding a web-text LM to the formatted model | plain WER 2.83 → 2.24, PER 29.48 → 32.40 (`M:324-325`, `M:346-347`) | single-source |
| Case and punctuation each add a large share of formatted WER on long-form speech | Earnings-21, best formatted model | plain 11.63, punctuation-only 13.65, case-only 17.09, both 18.86 (`Ko:242`) | single-source |
| Scores on reference text overstate scores on recogniser output | IWSLT 2011, a RoBERTa-large tagger with error augmentation (Alam et al. 2020, quoted second-hand) | overall F1 82.9 on reference transcripts vs 74 on ASR transcripts; question mark 87.8 vs 63.4; comma 76.7 vs 66.3; period 88.9 vs 82.3 (`G:59`) | single-source, second-hand; the original paper was not read |
| Aligned F1 depends on how much text the aligner accepts | Whisper-large on Portuguese interviews, 16:48:34 h | 85.44% of reference segments aligned; marks were compared at aligned segment ends (`G:464-472`); plain WER on the aligned part 14.50% (`G:474`) | single-source |
| Macro-averaged F1 is dominated by rare marks | same | macro F1 46.4 ± 32.7 over five marks, while comma is 77.5 and question 68.0 (`G:496-503`); exclamation is 0.92% and ellipsis 1.56% of reference marks (`G:357`, `G:365`) | single-source |

Reporting problems visible in the extracts themselves, relevant when quoting
them:

- Gris et al. give Whisper's comma / period / question F1 as 77.3 / 62.3 /
  67.6 in the summary table (`G:99`) and 77.5 / 63.9 / 68.0 in the results
  table (`G:496-501`).
- The female-sample exclamation row lists precision 31.2, recall 0.4 and F1
  6.8 (`G:518`); no F1 of 6.8 is consistent with that precision and recall.
- Zhu et al. state the margin over baselines as "at least 0.8" in the
  abstract (`Z:9`) and "at least 0.7" in the results (`Z:348`), and their
  test-set statistics list 490 sentences against 120,940 audio clips
  (`Z:118`), which cannot both be counts of the same test items.
- You et al. compare zero-WER F1 across systems on each system's own subset
  and say so (`Y:133`).

## Recommended protocol when hypothesis words contain errors

This is our synthesis of the above, not a protocol any one source states.

1. **Report the text model alone on reference words** with per-mark P, R and
   F1. This is the only setting in which restorers from different papers are
   comparable, and it isolates the restorer from the recogniser.
2. **Report the pipeline on recogniser output with per-mark PER**, including
   the deletion, insertion and substitution-target breakdown of `M:417-426`.
   It uses every utterance and needs no agreement on words.
3. **Report plain WER, WER C and WER PC side by side.** The difference
   between plain WER and WER C is the case cost; between WER C and WER PC,
   the punctuation cost in word-token units (`M:395`). Fix the tokenisation
   of marks (space-separated, as in `M:252`) and the mark inventory before
   comparing systems.
4. **Do not rank systems by zero-WER F1.** If it is reported for continuity
   with the literature, use the intersection of the systems' perfect
   utterances and state its size (`M:391`).
5. **Use whole recordings as well as segments for a streaming system.**
   Period F1 was 46.6 on whole talks and 27.3 on their 5.8-second segments
   for the same model (`K:203-216`, `K:286-291`), and segment-final marks
   are trivially predictable when the segmenter has already found the
   sentence end (`K:25`).
6. **Keep per-mark results; avoid macro averages over rare marks.**
7. **Check the reference convention.** Whisper produced 26.6% more sentences
   than the human transcribers on the same audio (`G:227`); much of a
   "period error" count can be a difference in sentence-length style, which
   no metric here separates from real errors.

## What this does not show

- **No case-specific metric beyond WER C and zero-WER F1.** No source
  separates sentence-initial capitals from proper nouns, though they fail
  for different reasons; Gris et al. only count them in one example
  (`G:203-205`).
- **No human judgement of readability.** The only downstream measure is one
  summarisation proxy, better with punctuation in 9 of 10 videos (`G:596`).
- **No analysis of how PER's masked alignment behaves next to word errors**,
  and no inter-annotator ceiling for any mark.
- **No significance tests or variance** for any metric in any source.
- **Nothing on number formatting, Vietnamese orthography, or a reference
  written in a different casing convention** from the system output.
- **The alignment used for aligned F1 is unspecified** in Kim et al. and
  only described in outline in Gris et al., so those F1 values are not
  reproducible from the papers.

## Per-paper reading notes

[meister2023-librispeech-pc](../related-work/readings/meister2023-librispeech-pc.md) ·
[kim2023-e2e-streaming-punct](../related-work/readings/kim2023-e2e-streaming-punct.md) ·
[you2025-formatted-e2e-distill](../related-work/readings/you2025-formatted-e2e-distill.md) ·
[koluguri2024-punctuated-long-seq](../related-work/readings/koluguri2024-punctuated-long-seq.md) ·
[gris2023-whisper-punct](../related-work/readings/gris2023-whisper-punct.md) ·
[zhu2022-unipunc](../related-work/readings/zhu2022-unipunc.md)
