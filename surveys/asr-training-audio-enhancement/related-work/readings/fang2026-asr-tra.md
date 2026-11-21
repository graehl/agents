**Source:** *Boosting ASR Robustness via Test-Time Reinforcement Learning with Audio-Text Semantic Rewards* — [HTML](https://arxiv.org/html/2603.05231v1) · [arXiv](https://arxiv.org/abs/2603.05231v1)

# fang2026-asr-tra

2026-11-21, sonnet-5.5. Purpose: guarding test-time adaptation against
adapting to its own errors, and a recognizer-independent check on a
transcript (the audio-to-text direction). Read: abstract, method summary,
Table 1 and its discussion.

**Claims.** On Whisper-Tiny with eight MS-SNSD noise types at 10 dB SNR,
confidence-driven adaptation (SUTA) can reinforce high-confidence errors:
mean WER baseline 32.71, SUTA 32.27, SGEM 30.22, ASR-TRA 28.64; SUTA is worse
than no adaptation on three of eight noises (BA 36.85 to 40.12, CM 39.40 to
43.52, MU 29.98 to 34.12)
([extract](../extract/fang2026-asr-tra/html/2603.05231v1.md):236-337).
ASR-TRA samples several decodings with a learnable decoder prompt, scores
each with a CLAP audio-text similarity reward, and updates by policy
gradient; reported latency about 0.72 s per utterance against 1.69 s for
SUTA (hardware as given in the paper; not checked here). The authors also
report an effect among the 100 highest-confidence samples under Gaussian
noise (figure 2).

**Means for us.** Evidence, on a Whisper-class model, that
confidence-driven test-time adaptation can be net harmful and that an
independent audio-text scorer works as the signal instead. The scorer is
CLAP (a general audio-text embedding), not a text-to-audio likelihood; the
paper does not test a model that goes from text toward a specification of
the audio.

**Not shown.** Real phone noise; non-English; CLAP's effectiveness on
languages other than English; ablation separating the prompt, the RL
update and the reward is in the paper's Table 3 (not read).
