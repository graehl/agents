**Source:** *Whisper-AT: Noise-Robust Automatic Speech Recognizers are Also Strong General Audio Event Taggers* — [HTML](https://arxiv.org/html/2307.03183v1) · [arXiv](https://arxiv.org/abs/2307.03183v1)

# gong2023-whisper-at

2026-11-21, sonnet-5.5. Purpose: direct evidence on whether a large
supervised encoder already infers the input's noise condition. Read:
introduction, section 3 (probing), section 4-5 summary.

**Claims.** Linear probes on frozen encoders classify the 50 ESC-50
sound classes best from Whisper, and, unlike other ASR encoders, Whisper's
deeper layers keep background-sound information rather than discarding it
([extract](../extract/gong2023-whisper-at/html/2307.03183v1.md):52). Whisper
is also more robust to those sounds. Class by class, Whisper's robustness
to a given noise class correlates positively with how well its
representation recognizes that class (line 60). The authors read this as
"first encodes the background sound, then transcribes conditioned on it",
contrasted with explicit noise-aware training that supplies the noise type
manually (line 60), and caution that noise-invariance may still be the
practical route for self-supervised or small-data models (line 62).

**Means for us.** Evidence that Whisper-class encoders already carry the
condition information internally, which is what side information would
supply. The link to robustness is correlational and class-level; there is
no experiment that injects a condition label or per-band estimate into the
encoder and measures WER.

**Not shown.** Any gain or no-gain from side information in Whisper or
wav2vec 2.0; low-resource languages.
