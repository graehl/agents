**Source:** *Read What You Hear: Reference-Free Hypotheses Evaluation with Acoustic Discrepancy* — [HTML](https://arxiv.org/html/2606.04680) · [arXiv](https://arxiv.org/abs/2606.04680)

# li2026-read

2026-11-21, sonnet-5.5. Purpose: a text-to-audio likelihood as a score of an
ASR transcript that is independent of the recognizer. Read: abstract,
introduction, method outline, experimental setup, rescoring and noisy-speech
sections; Table 1-3 cells were not transcribed.

**Claims.** READ scores a hypothesis by the likelihood a pretrained
autoregressive discrete-token TTS model (CosyVoice2, official checkpoint, no
extra training) assigns to the speech tokens given the hypothesis text;
spikes in loss mark misaligned segments. Used for N-best rescoring (top 5
from Whisper large-v3) and for system combination (Whisper medium and
large-v3, NeMo, Qwen2.5-Omni), on LibriSpeech clean/other, SPGISpeech,
Switchboard and others, plus noise-augmented copies (WHAM! noise at 0, 10
and 20 dB). The abstract reports "up to 20% relative error rate reduction,
with particularly strong gains under noisy conditions"
([extract](../extract/li2026-read/html/2606.04680.md):11); sentence-level
rescoring "consistently outperforms the original top-1" across datasets
(line 301); the advantage grows as SNR falls (line 551), which the authors
attribute to errors being more acoustic in noise (line 553). The READ-derived
duration-proportion metric correlates with WER across noise conditions
(line 179).

**Means for us.** The one read paper that uses a synthesis model scoring
audio given text, as a transcript quality and rerank signal, independent of
the recognizer's own confidence. The audio-side score is a likelihood over
speech tokens, at the TTS model's description level, not waveform synthesis.

**Not shown.** Low-resource languages (the TTS model's coverage is a
precondition); use as a label-quality filter for training data; cost on a
phone (it needs a TTS model of the size of CosyVoice2).
