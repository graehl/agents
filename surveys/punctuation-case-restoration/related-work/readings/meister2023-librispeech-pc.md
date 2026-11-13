**Source:** *LibriSpeech-PC: Benchmark for Evaluation of Punctuation and Capitalization Capabilities of end-to-end ASR Models* — [PDF](https://arxiv.org/pdf/2310.02943) · [arXiv](https://arxiv.org/abs/2310.02943)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/meister2023-librispeech-pc/html/2310.02943.md`.

### Claims

- **Dataset.** LibriSpeech with punctuation and case restored by aligning
  transcripts to the source books; over 90% of every split kept (449.10 +
  333.13 + 91.61 h train) (`:143`, `:160-168`). Dropped: non-standard
  Unicode, more than two words of mismatch, clips under one second,
  all-uppercase samples (`:147-150`). Only `. , ?` are kept for training and
  scoring (`:251`).
- **Metric.** Punctuation error rate, PER = (I+D+S)/(I+D+S+C) over
  punctuation tokens after a word alignment in which all marks are masked to
  one symbol (`:88`, `:101-116`); bounded in [0, 1] (`:136`).
- **Why not F1.** F1 is only computable where WER is zero: 48–66% of
  utterances, and only 375 (15.5%) of test-clean and 1119 (39.1%) of
  test-other are perfect for both systems (`:389-391`).
- **Formatted recogniser vs cascade, test-clean / test-other.** Conformer-CTC
  115M fine-tuned 100,000 steps from the words-only checkpoint, 128-token
  vocabulary (`:267`): PER 29.48 / 27.37, WER 2.83 / 5.65, WER C 4.72 / 7.57,
  WER PC 8.11 / 10.48 (`:322-331`). Cascade of the words-only checkpoint
  plus BERT 109M tagger tuned 3 epochs: PER 36.60 / 37.42, WER 2.86 / 6.26,
  WER PC 9.45 / 12.90 (`:311-320`). Same tagger untuned: PER 38.38 / 38.60,
  WER 2.60 / 5.79, WER PC 26.36 / 29.96 (`:300-309`).
- **Zero-WER F1.** Punctuation 84.75 vs 87.40 (test-clean) and 83.40 vs
  88.27 (test-other), cascade vs formatted; capitalisation 94.47 vs 94.85
  and 94.53 vs 95.50 (`:196-242`).
- **Token LM in beam search.** 7-gram over LibriSpeech-PC text: PER 29.27,
  WER 2.22. Over Common Crawl text only: PER 32.40, WER 2.24. Mixture: PER
  29.24, WER 2.22 (`:333-364`, `:371-379`).
- **Per mark (test-clean):** PER period 24.01%, comma 33.26%, question
  15.99%; comma insertions 18.23%, deletions 13.53%; 9.93% of periods become
  commas (`:417-426`).
- **Whisper-base 74M:** PER 36.97 / 40.27, WER 4.50 / 11.23 (`:289-298`).

### Meaning for our purpose

- The cascade (our default form) lost to the formatted recogniser by about 7
  PER points and 1.3–2.4 WER PC points even after in-domain tuning of the
  tagger; the plain-WER cost of formatting was +0.23 on test-clean and −0.14
  on test-other. This is the main evidence against "text-only is
  sufficient", for one BERT-base tagger.
- Case is the easy half: capitalisation F1 is about 94.5–95.5 for both
  routes; punctuation is where they differ.
- An untuned off-the-shelf tagger is unusable by WER PC (26.36); domain and
  convention match of the text model matters far more than its architecture.
- PER with a per-mark breakdown, plus WER / WER C / WER PC, is a ready-made
  protocol for scoring a restorer on recogniser output.
- Book-alignment is a route to formatted audio data when the source text of
  read speech exists.

### What it does not show

- The cascade's tagger is BERT-base only; the tuning text is not named
  (`:263`). No larger or better-trained text model, no ASR-error
  augmentation.
- One run per system; no variance. The tuned cascade's plain WER (2.86)
  differs from the base cascade's (2.60) without explanation.
- Offline CTC, 115M, English read audiobooks; nothing streaming, small, or
  conversational. The per-mark table does not name the model it describes.
- F1 comparisons use each system's own zero-WER subset.

### Leads worth fetching

- Nozaki et al. 2022, *End-to-end speech-to-punctuated-text recognition*
  (arXiv 2207.03169): the cascade-vs-end-to-end comparison everyone cites.
- Zhou, Tan, Qian, ICASSP 2022, *Punctuation prediction for streaming
  on-device speech recognition*: the on-device case, separate punctuation
  decoder.
- Nguyen et al., O-COCOSDA 2019, *Fast and accurate capitalization and
  punctuation for ASR using Transformer and chunk merging* (`:448`): authors
  appear to be a Vietnamese group; language not stated in this extract.
- Păiş and Tufiş 2021, *Capitalization and punctuation restoration: a
  survey* (`:441`).
- Guan 2020, arXiv 2012.02012: source of the slot-error-rate metrics.
