**Source:** *Longer is (Not Necessarily) Stronger: Punctuated Long-Sequence Training for Enhanced Speech Recognition and Translation* — [PDF](https://arxiv.org/pdf/2409.05601) · [arXiv](https://arxiv.org/abs/2409.05601)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/koluguri2024-punctuated-long-seq/html/2409.05601.md`.

### Claims

- **Setup.** FastConformer-XXL, 1.1B, hybrid TDT + CTC (CTC weight 0.3),
  fine-tuned 25,000 steps on 64 GPUs from a pretrained checkpoint (`:213`).
  Training data with punctuation and case: 18,784 h of 0–20 s fragments, or
  17,983 h of complete sentences, plus 7,123 h at 20–40 s and 5,557 h at
  40–60 s (`:125-128`). Evaluation on Earnings-21 / Earnings-22 cut to
  roughly 17-minute segments, numerals converted to words (`:138`,
  `:152-153`).
- **Complete sentences vs fragments (0–20 s, equal duration).** Punctuated
  cased WER 24.86 → 19.96 (Earnings-21) and 30.19 → 23.58 (Earnings-22);
  plain WER 12.44 → 12.12 and 15.6 → 14.72 (`:239-240`, `:244-245`).
- **Longer segments.** 0–40 s: 18.98 and 22.62; 0–60 s: 18.86 and 22.4;
  plain WER 11.61 / 11.63 and 14.13 / 14.15 (`:241-242`, `:246-247`).
- **Formatted vs words-only labels, same 0–60 s data.** Plain WER 11.63 vs
  11.71 and 14.15 vs 14.69, formatted lower (`:265-266`).
- **Cascade.** The words-only model plus NeMo's BERT tagger trained on
  LibriSpeech and Fisher text: punctuated cased WER 23.44 and 26.71 against
  18.86 and 22.4 end-to-end; case-only 19.60 / 22.76 vs 17.09 / 20.54;
  punctuation-only 16.20 / 18.81 vs 13.65 / 16.38 (`:272`, `:315-351`).
- **Short lowercase benchmarks.** Average WER over nine leaderboard sets
  6.95 for the reference row, 6.82 / 6.73 / 6.81 for complete-sentence
  models at 20 / 40 / 60 s (`:198-201`).
- **Memory.** Batch size 2 at 60 s and 8 at 40 s on an 80 GB GPU (`:219`).

### Meaning for our purpose

- The cleanest evidence in this batch that formatted targets do not cost
  plain WER: same model, same audio, labels with and without punctuation and
  case, formatted slightly better.
- If we train a formatted recogniser, the training segments should be whole
  sentences; fragments that begin or end mid-sentence cost about 5–6.6
  absolute points of formatted WER here. Our Vietnamese training segments
  would need checking for this.
- A generic text tagger applied to out-of-domain recogniser output loses
  4.3–4.6 formatted-WER points to the formatted recogniser.
- Segments beyond 40 s buy nothing.

### What it does not show

- 1.1B offline full-attention model and 18k+ hours of formatted audio;
  nothing about a 68M streaming transducer or a few hundred hours.
- The cascade's tagger is not adapted to earnings calls and is BERT-base; no
  strong-text-model cascade. So the cascade gap is an upper bound on what a
  tuned text restorer would lose.
- Only WER variants are reported: no per-mark results, no PER, no F1.
- The leaderboard reference row is the published words-only model, not
  necessarily a matched run (`:205`). No variance; much of the training data
  is internal.
- Numbers are scored as words; no inverse text normalisation.

### Leads worth fetching

- O'Neill et al. 2021, *SPGISpeech* (arXiv 2104.02014, `:462`): 5,000 h of
  fully formatted audio and the earliest formatted Conformer result.
- Pappagari et al., ASRU 2021, *Joint prediction of truecasing and
  punctuation for conversational speech in low-resource scenarios* (`:445`).
- Żelasko et al. 2018, *Punctuation prediction model for conversational
  speech* (arXiv 1807.00543, `:444`).
- Fox et al. 2023, *Updated corpora and benchmarks for long-form speech
  recognition* (arXiv 2309.15013, `:457`): long-segment training precedent.
