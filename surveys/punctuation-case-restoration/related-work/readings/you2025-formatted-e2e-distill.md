**Source:** *Enhancing Fully Formatted End-to-End Speech Recognition with Knowledge Distillation via Multi-Codebook Vector Quantization* — [PDF](https://arxiv.org/pdf/2512.18967) · [arXiv](https://arxiv.org/abs/2512.18967)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/you2025-formatted-e2e-distill/you2025-formatted-e2e-distill.md`.

### Claims

- **Setup.** Zipformer-medium transducer (icefall recipe), 65M, trained on
  LibriSpeech-PC with a 500-token SentencePiece vocabulary whose output
  covers upper and lower case and `, . ?`; 30 epochs on four V100; beam 4
  (`:79-87`). Words and marks are space-separated in the targets (`:81`).
- **Auxiliary loss.** Encoder layer 11 predicts 16 codebook indexes derived
  from layer 36 of HuBERT-XL fine-tuned on LibriSpeech; weight 0.1; teacher
  labels precomputed; nothing added at inference (`:56-73`, `:85-87`).
- **Main result, test-clean / test-other, no LM.** PER 29.74 / 28.18, WER
  2.20 / 5.23, WER C 4.20 / 7.27, WER PC 7.58 / 10.21, against Meister's
  115M Conformer at 29.48 / 27.37, 2.83 / 5.65, 4.72 / 7.57, 8.11 / 10.48
  and Whisper-large (1550M) at PER 30.52 / 30.55, WER PC 8.60 / 11.29
  (`:126-129`).
- **With a 3×1024 LSTM LM (25M) on LibriSpeech-PC text, shallow fusion.**
  PER 27.24 / 26.55, WER 1.87 / 4.56, WER PC 6.65 / 9.05 (`:91`, `:131`).
- **Ablation.** Offline without / with distillation: PER 30.23 / 29.74
  (clean), 29.51 / 28.18 (other); WER 2.42 / 2.20, 5.55 / 5.23. Streaming:
  PER 30.01 / 28.74, 29.05 / 28.81; WER 3.13 / 2.85, 7.85 / 7.55. GPU hours
  152 → 164 and 188 → 200 (`:147-151`).
- **Loss weight.** WER PC 7.62 / 7.58 / 7.67 on test-clean for 0.05 / 0.1 /
  0.2 (`:158-160`).
- **Zero-WER F1.** Punctuation 88.57 and 89.03; capitalisation 95.76 and
  96.13; 76% and 59% of utterances are perfect (`:116-119`).

### Meaning for our purpose

- This is the closest architecture to ours: a 65M Zipformer transducer in
  the same toolkit family as a sherpa-onnx model, emitting case and
  punctuation from a 500-token vocabulary. It works at that size.
- Streaming did not hurt punctuation (PER 30.01 vs 30.23 without
  distillation) while costing 0.7–2.3 WER points; for a phone transducer the
  punctuation tokens are not what streaming degrades.
- The teacher is a speech model trained on words-only transcripts; the gain
  is mostly better words (WER 2.42 → 2.20) and 0.5–1.3 PER. It is not a way
  to move a text restorer's knowledge into the recogniser.
- A small LM over formatted text helps punctuation more than distillation
  does (PER −2.5 on test-clean).

### What it does not show

- No words-only Zipformer baseline: the WER cost or benefit of formatted
  targets at this size is not measured. No cascade rerun; cascade numbers
  are not even quoted.
- English read audiobooks, about 874 h of formatted audio; no low-resource
  or other-language result. Streaming latency settings are not given.
- F1 is on each system's own zero-WER subset (acknowledged, `:133`). One run
  per row; gains of 0.2–1.3 without variance.
- A fine-tuned HuBERT-XL teacher in the target language is assumed to exist.

### Leads worth fetching

- Zhou, Tan, Qian, ICASSP 2022, *Punctuation prediction for streaming
  on-device speech recognition* (`:198`): separate punctuation decoder,
  on-device.
- Caseiro et al., Interspeech 2020, *Mixed case contextual ASR using
  capitalization masks* (`:194`): case output without doubling the
  vocabulary.
- O'Neill et al., Interspeech 2021, *SPGISpeech: 5,000 hours ... for fully
  formatted end-to-end speech recognition* (`:200`).
- Ling et al., ICASSP 2024, *Adapting large language model with speech for
  fully formatted end-to-end speech recognition* (`:206`).
- Hentschel, Tsunoo, Okuda, ICASSP 2021, *Making punctuation restoration
  robust and fast with multi-task learning and knowledge distillation*
  (`:192`): a small, fast text restorer.
- Pappagari et al., ASRU 2021, *Joint prediction of truecasing and
  punctuation for conversational speech in low-resource scenarios* (`:191`).
- Švec et al., TSD 2021, *Transformer-based automatic punctuation prediction
  and word casing reconstruction of the ASR output* (`:193`).
