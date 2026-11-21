**Source:** *When De-noising Hurts: A Systematic Study of Speech Enhancement Effects on Modern Medical ASR Systems* — [PDF](https://arxiv.org/pdf/2512.17562v1) · [arXiv](https://arxiv.org/abs/2512.17562v1)

# chondhekar2025-denoising-hurts

2026-11-21, sonnet-5.5. Purpose: inference-time enhancement in front of
large recognizers. Read: abstract, setup, results text and Table 1.

**Claims.** MetricGAN+ (VoiceBank-trained) denoising applied to 500
English medical recordings under nine synthetic noise conditions plus the
originals raised semantic WER in all 40 model-by-condition cells, for
Whisper large-v3, NVIDIA Parakeet, Gemini Flash 2.0 and a medical-tuned
model (Parrotlet-a)
([extract](../extract/chondhekar2025-denoising-hurts/chondhekar2025-denoising-hurts.md):261-279).
Mean change +7.83 points; on the unmodified recordings +2.06 points
(Table 1). Whisper background noise at 10 dB SNR: 8.82% raw vs 25.83%
enhanced; at 50 dB: 6.54% vs 9.82% (line 243). Gaussian noise gives the
largest harm (Whisper 16.19% to 51.11%, line 257).

**Means for us.** Strongest simple demonstration that a standalone
perceptual enhancer is a net harm for a large robust recognizer, including
when the input is already clean. Noise is added synthetically, so the
test noise is not what the enhancer saw at training; "SNR 10 dB" is called
severe by the authors but is moderate by usual standards.

**Not shown.** Real-world noisy recordings; any enhancer trained against
recognition loss; non-English or low-resource speech. The metric is a
custom normalized WER (semWER). Technical report, not peer reviewed.
The title's causal story (internal robustness) is the authors' inference,
not tested by layer analysis.
