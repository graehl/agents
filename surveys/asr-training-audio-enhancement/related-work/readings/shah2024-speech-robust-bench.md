**Source:** *Speech Robust Bench: A Robustness Benchmark For Speech Recognition* — [PDF](https://arxiv.org/pdf/2403.07937v3) · [arXiv](https://arxiv.org/abs/2403.07937v3)

# shah2024-speech-robust-bench

2026-11-21, sonnet-5.5. Purpose: which input conditions an ASR robustness
benchmark measures (steady vs event noise, bandwidth, distance, gain) and
how Whisper-class and wav2vec 2.0 compare. Read: abstract, scenario
definitions (section 3), model list, results discussion in text. Table
values were not transcribed.

**Claims.** 114 scenarios in six categories: clean, social gatherings,
speech variations (accents), environmental effects, digital augmentations,
adversarial attacks
([extract](../extract/shah2024-speech-robust-bench/shah2024-speech-robust-bench.md):66-83).
Environmental noise is real noise (ESC-50, MS-SNSD, MUSAN, WHAM!) added at
10, 20, 30 and 40 dB SNR to whole utterances; spatial acoustics are added
by echo and room impulse responses; digital augmentations include amplitude
gain, resampling, low-pass and high-pass filtering, tempo and speed
changes, pitch, chorus, tremolo, phaser and Gaussian noise (lines 79-82).
Across models, Whisper large-v2 is the most robust to non-adversarial
perturbations on English; wav2vec 2.0 and HuBERT, despite 60 K hours of
pretraining, "severely lack robustness" on accents, social scenarios and
spatial acoustics; a leaderboard-topping Canary model is much less robust
than Whisper to echo, real room impulse responses, speed and pitch
(lines 138-150). Larger models are more robust within a family; the
authors note this runs somewhat counter to the claim that scale of data
alone gives robustness (line 188).

**Means for us.** A ready scenario suite that includes lowpass and
resampling (a narrowband proxy), gain and tempo. Every noise scenario adds
steady noise across the whole utterance at a fixed SNR; no scenario in the
parts read has a noise event with a start and end, a moving source, or a
change of audio path inside a recording.

**Not shown.** Codec artifacts (no codec scenario is listed in the parts
read), non-stationary or event noise, and any low-resource language other
than Spanish.
