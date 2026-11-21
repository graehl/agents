**Source:** *Bridging the Gap: Integrating Pre-trained Speech Enhancement and Recognition Models for Robust Speech Recognition* — [HTML](https://arxiv.org/html/2406.12699v1) · [arXiv](https://arxiv.org/abs/2406.12699v1)

# wang2024-bridging

2026-11-21, sonnet-5.5. Purpose: direct evidence on whether enhancement
helps Whisper, and on mixing the original back in ("observation adding").
Read: method (bridge module), all three results tables and discussion.

**Claims.** Four pretrained enhancers (CMGAN, MP-SENet, DEMUCS, SEMamba)
in front of frozen Whisper base and large-v3. On LibriSpeech with
DNS-challenge noise (SNR -12 to 12 dB), enhancement alone is worse than
the noisy input for every enhancer: average WER base 32.1% noisy vs
35.4 to 50.9% enhanced; large-v3 15.4% noisy vs 22.8 to 39.9% enhanced
([extract](../extract/wang2024-bridging/html/2406.12699v1.md):112-390).
The harm is largest at low SNR (-12 dB, large-v3: 44.3% noisy vs 69.1%
with CMGAN) and small at 12 dB (3.2% vs 3.7%).

A "bridge module" predicts a coefficient in [0.6, 1] from the noisy and
enhanced spectrograms and returns a weighted sum of noisy and enhanced
waveforms (observation adding; floor 0.6 chosen because "Whisper is
inherently noise-robust"; lines 56-58). Average WER with the module:
base 29.1 to 31.3% (vs 32.1% noisy), large-v3 14.4 to 15.5% (vs 15.4%
noisy); best large-v3 gain is DEMUCS, 15.4 to 14.4% (lines 391-393).
Aurora-4: large-v3 17.3 to 17.1 to 17.2% (lines 623-625). VoiceBank-DEMAND:
large-v3 3.1% to 2.6 to 2.9%; base 9.0% to 7.6 to 8.5%.

**Means for us.** Two results at once: (1) raw enhancement hurts Whisper;
(2) interpolating with the observation recovers the loss and gives a small
gain over noisy input (large-v3: about 0 to 1 point absolute on LibriSpeech
plus DNS noise, relative gains of up to 6.5%). Higher PESQ/STOI did not
predict lower WER (lines 395, 625). The gains for the large model are small
and the module needs an enhancer plus a second network at inference.

**Not shown.** Whisper-fine-tuned or low-resource conditions; real noise;
the bridge module was trained on CMGAN outputs and applied to others.
Whether the small gains survive a repeated-seed or alternative-scoring check
is not examined. A 2025 follow-up with a speech-trained bridge
(arXiv 2501.02452) was not read.
