**Source:** *Dual-Encoder Architecture with Encoder Selection for Joint Close-Talk and Far-Talk Speech Recognition* — [HTML](https://arxiv.org/html/2109.08744) · [arXiv](https://arxiv.org/abs/2109.08744)

# weninger2021-dual-encoder

2026-11-21, sonnet-5.5. Purpose: a learned input-condition selector routing to
condition-specific encoders. Read: abstract, introduction, method, setup;
result tables not transcribed.

**Claims.** One E2E recognizer (attention-based LAS and RNN-T) with a
close-talk single-channel encoder and a far-talk multi-channel encoder with
neural beamforming, plus an encoder-selection network that classifies each
utterance (or frame) from the input features and picks or mixes encoders.
On conversational medical speech recorded simultaneously with a close-talk
device and a microphone array, the dual-encoder system "obtains up to 9%
relative WER reduction when using both CT and FT input, compared to the best
single-encoder system trained and tested in matched condition"
([extract](../extract/weninger2021-dual-encoder/html/2109.08744.md):9).
A large single-encoder baseline with a similar parameter count (87 M) is
also trained (line 148).

**Means for us.** A learned estimate of the input condition selects
parameters; the gain is up to 9% over matched single encoders. The signal
is a device/array difference, not noise, and both inputs are available.

**Not shown.** Single-microphone phone input; per-condition numbers (not
transcribed here).
