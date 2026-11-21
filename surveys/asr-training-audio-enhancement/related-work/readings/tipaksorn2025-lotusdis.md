**Source:** *LOTUSDIS: A Thai far-field meeting corpus for robust conversational ASR* — [HTML](https://arxiv.org/html/2509.18722v1) · [arXiv](https://arxiv.org/abs/2509.18722v1)

# tipaksorn2025-lotusdis

2026-11-21, sonnet-5.5. Purpose: single-channel dereverberation and
denoising in front of a fine-tuned Whisper in a lower-resource language
(far-field boundary case). Read: corpus design, Table 3, sections 4.3-4.6.

**Claims.** Thai meeting speech, 114 h, nine single-channel devices from
0.12 m to 10 m. Zero-shot Whisper-large-v3 overall WER 79.84%, far-field
100.82%; a Thai-tuned Whisper large-v3 baseline fine-tuned on all
microphones reaches 38.33% overall (49.54% far, 21.59% near)
([extract](../extract/tipaksorn2025-lotusdis/html/2509.18722v1.md):68). Adding
WPE dereverberation: 48.00% overall (near 35.92%, far 56.12%); MMSE
log-spectral-amplitude denoising: 42.89% (near 24.92%, far 54.55%) (line 68,
text line 100). Training-side augmentation of a condenser-only fine-tune
with real room impulse responses cut far-field WER from 79.54% to 65.39%;
SpecAugment alone 67.15% (line 68, 104).

**Means for us.** In a lower-resource language with a recognizer tuned on
distance-diverse data, classical single-channel front ends worsened both
near and far fields; the authors conclude data diversity beat processing.
Reverberation augmentation in training beat test-time dereverberation as a
route.

**Caveat (ours).** The paper's table does not say whether the model behind
the WPE/MMSE rows was fine-tuned on processed audio or only tested on it;
the text reads as test-side processing of a model trained on raw audio, so
the harm may be a train/test mismatch rather than an inherent cost. The
WPE settings are NaraWPE defaults, not tuned. No Whisper-RIR-style paired
comparison for the same device.

**Not shown.** A learned dereverberator; beamforming; effect on clean
close-talk when the model is retrained on processed audio.
