**Source:** *Towards Pretraining Robust ASR Foundation Model with Acoustic-Aware Data Augmentation* — [HTML](https://arxiv.org/html/2505.20606v1) · [arXiv](https://arxiv.org/abs/2505.20606v1)

# liu2025-acoustic-aware-augmentation

2026-11-21, sonnet-5.5. Purpose: whether generic spectrogram masking
(SpecAugment) already covers acoustic variation, in a small-data
foundation-model pretraining setting. Read: abstract, sections 5.1-5.4 and
Table 1.

**Claims.** Whisper-base architecture pre-trained on LibriSpeech-960 h
(with synthetic TTS data) under different augmentations; test sets
LibriSpeech clean/other, ENNI (child), MyST (child), L2-ARCTIC (accented).
WER: no augmentation 14.85/29.00/90.44/77.28/56.57; SpecAugment
13.34/24.41/92.25/64.96/46.11; SpecMix 10.37/22.30/85.34/67.50/44.14; the
authors' pitch/duration/accent-style augmentation, at 20 k, 40 k and 60 k
hours of augmented exposure, 11.27 to 8.58 / 25.01 to 21.84 / 82.42 to
82.67 / 63.08 to 58.04 / 44.90 to 40.28; the original Whisper base
(680 k h) 5.93/13.00/50.88/31.74/21.99
([extract](../extract/liu2025-acoustic-aware-augmentation/html/2505.20606v1.md):98-177).
They state SpecAugment, as used for Whisper-v2, is not optimal for
acoustic diversity and acoustic-centric augmentation gives up to 19.24%
lower WER than no augmentation (line 202).

**Means for us.** Generic masking was not enough on out-of-domain sets in
this small-data setting; targeted acoustic augmentation helped more. The
augmentations are pitch, duration and accent-like changes; codec,
bandwidth and noise are not among them, so this does not answer the
codec-augmentation question.

**Not shown.** Narrowband or codec augmentation; cost on clean wideband
input beyond the LibriSpeech columns; a Whisper-scale or multilingual
result. A preprint with a small model.
