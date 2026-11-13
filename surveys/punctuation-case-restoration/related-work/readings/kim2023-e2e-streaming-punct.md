**Source:** *Improved Training for End-to-End Streaming Automatic Speech Recognition Model with Punctuation* — [PDF](https://arxiv.org/pdf/2306.01296) · [arXiv](https://arxiv.org/abs/2306.01296)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/kim2023-e2e-streaming-punct/html/2306.01296.md`.

### Claims

- **Setup.** Streaming CTC recogniser, 12-layer 256-wide Transformer, about
  18M parameters, 2000 lowercase wordpieces including `' , . ?` (`:228`,
  `:232-234`); 1 s chunks with 2 s past and 1 s future context (`:240`);
  MuST-C English, at least 385 h (`:226`); beam 5, no LM. Punctuation P/R/F1
  computed after aligning hypothesis to reference; WER excludes punctuation
  (`:240`).
- **Method.** Concatenate pairs of random utterances (audio and labels) so
  sentence-final marks occur mid-sequence, and add a second CTC loss on
  chunk-wise emissions, weight 0.5 (`:71`, `:108`, `:234`).
- **Whole talks (11 min average).** Baseline: WER 18.2; F1 comma 50.3,
  period 35.8, question 34.0, average 40.0; period recall 23.6. Proposed:
  WER 15.8; F1 50.8 / 46.6 / 37.9, average 45.1; period recall 33.6
  (`:173-216`).
- **5.8 s segments.** Baseline WER 18.5, average F1 34.4, period F1 16.0;
  proposed WER 16.3, average 41.2, period 27.3 (`:272-291`).
- **Ablation.** Without the chunk loss: WER 21.3, period F1 52.9, question
  25.8, average 41.2. Without concatenation: WER 16.0, period 41.0, average
  41.7 (`:313-332`).
- **Intermediate CTC on unpunctuated labels** (Nozaki) as reimplemented:
  WER 18.5, average F1 36.1 on talks; 18.9 and 28.7 on segments, worse than
  baseline (`:188-201`, `:279-284`).
- **Cost.** No inference overhead; more training time and memory (`:342`).

### Meaning for our purpose

- A small streaming recogniser that emits punctuation itself, with no text
  model, gets under half the periods (best period F1 46.6) on English TED
  talks. That is far below what the other papers report for text taggers on
  reference text, so the formatted-recogniser route is not automatically
  better at small size and in streaming.
- If we retrain the recogniser with punctuation, training on concatenated
  utterances matters, and a naive concatenation costs 5.5 WER points unless
  the streaming-condition loss is added.
- Scoring only on short segments understates or misstates sentence-final
  behaviour; evaluate on continuous audio too.

### What it does not show

- No words-only baseline, so no measurement of what punctuation tokens cost
  in WER. No cascade baseline at all.
- No case (everything lowercased). CTC only; no transducer. One dataset, one
  run per row, WER of 16–18% is a weak recogniser.
- The alignment used for F1 is not specified. Segment-level and talk-level
  F1 are not obviously comparable.
- The interCTC row is the authors' reimplementation in a different regime
  from the original.

### Leads worth fetching

- Nozaki et al., Interspeech 2022, *End-to-end speech-to-punctuated-text
  recognition* (`:360`): original offline result this paper fails to
  transfer.
- Behre et al. 2022, *Streaming punctuation for long-form dictation with
  transformers* (`:357`): a streaming text-side restorer, the cascade form
  we would deploy.
- Huang et al., Interspeech 2022, *E2E Segmenter: joint segmenting and
  decoding for long-form ASR* (`:361`): sentence boundaries from the
  recogniser.
- Sunkara et al., Interspeech 2020 (`:363`): multimodal semi-supervised
  punctuation.
