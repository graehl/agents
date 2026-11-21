**Source:** *E-BATS: Efficient Backpropagation-Free Test-Time Adaptation for Speech Foundation Models* — [HTML](https://arxiv.org/html/2506.07078) · [arXiv](https://arxiv.org/abs/2506.07078)

# dong2025-ebats

2026-11-21, sonnet-5.5. Purpose: test-time adaptation of self-supervised speech
encoders without backpropagation (phone-relevant cost). Read: abstract,
introduction, method outline, results text; tables not transcribed.

**Claims.** A prompt vector added to the frame embeddings (a learnable
per-utterance shift), found by CMA-ES (derivative-free search), with a
multi-scale loss (token-level entropy plus utterance-level alignment of
latent statistics to source-domain centroids) and a time-smoothed (EMA)
update across utterances. Wav2Vec2-Base and HuBERT-Large CTC models, four
noisy datasets, sixteen acoustic conditions. Compared with 13 baselines:
"4.1% to 13.5%" accuracy gains over backpropagation-free baselines; 2.0 to
6.4 times less peak GPU memory than backpropagation-based methods; lowest
WER on 3 of 5 datasets even against backpropagation-based methods, up to
30.7% relative ([extract](../extract/dong2025-ebats/html/2506.07078.md):398-400).
The authors report the search adds adaptation latency (limitation).

**Means for us.** A published route to test-time adaptation without
gradients, with a small per-utterance vector that is carried by an EMA
across utterances. SSL CTC models only, not Whisper.

**Not shown.** Whisper or transducers; phone latency or energy.
