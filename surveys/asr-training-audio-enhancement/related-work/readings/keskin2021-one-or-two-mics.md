**Source:** *Do You Listen with One or Two Microphones? A Unified ASR Model for Single and Multi-Channel Audio* — [HTML](https://arxiv.org/html/2106.02750v2) · [arXiv](https://arxiv.org/abs/2106.02750v2)

# keskin2021-one-or-two-mics

2026-11-21, sonnet-5.5. Purpose: two-microphone processing with a jointly
trained neural beamforming front end. Read: abstract, architecture,
datasets, sections 5-6.

**Claims.** Industrial far-field recognizer (Amazon) with a single-channel
front end and a two-auxiliary-channel neural beamforming layer feeding a
shared backend; 45 h human-transcribed three-channel test set. A
multi-channel model trained on 10 K hours beats the single-channel model
trained on twice the data (E4 vs E3) by 10.3% relative WER on single-speaker
utterances ([extract](../extract/keskin2021-one-or-two-mics/html/2106.02750v2.md):201);
14.8% relative below 10 dB SNR (line 217). Unified single/multi training
adds 2.2 to 2.5% (line 205); the abstract's headline is up to 12.5%
relative (16.0% in low SNR) over primary-channel-only. Zero-padding
single-channel data into the multi-channel model is worse than the unified
design by 3.1 to 4.0% relative (line 182).

**Means for us.** A trained two-channel front end gives real gains for a
proprietary recognizer on distant devices with 65 K-hour-scale data; it is
a learned, jointly trained front end, not a fixed beamformer plus an
off-the-shelf model.

**Not shown.** Handset geometry (two microphones centimetres apart, mouth
near-field); any pretrained or open recognizer; a fixed beamformer
baseline on the same data; the device type is not described in the parts
read.
