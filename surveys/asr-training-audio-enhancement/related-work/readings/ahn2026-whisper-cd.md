**Source:** *Whisper-CD: Accurate Long-Form Speech Recognition using Multi-Negative Contrastive Decoding* — [HTML](https://arxiv.org/html/2603.06193) · [arXiv](https://arxiv.org/abs/2603.06193)

# ahn2026-whisper-cd

2026-11-21, sonnet-5.5. Purpose: Whisper with previous-text context across
segments; whether carrying text state helps. Read: abstract, introduction,
datasets and results text.

**Claims.** On Whisper large-v3, conditioning decoding on the previous
segment's transcript increases WER by over 190 points on CORAAL and over
500 points on Earnings22, mainly through errors accumulating and
hallucination or repetition loops propagating
([extract](../extract/ahn2026-whisper-cd/html/2603.06193.md):120). The paper's
fix is training-free contrastive decoding against three audio
perturbations (Gaussian noise, silence, temporal shift), reducing WER by up
to 24.3 points on CORAAL across five long-form benchmarks; large-v3 baseline
WER exceeds 100% on some sets and remains 45.77% on CORAAL after the fix
(line 290).

**Means for us.** Carrying text (the previous transcript) as state into
Whisper is harmful in long-form audio, in contrast to the acoustic-state
carry-over results for transducers. A cautionary result for any design that
feeds Whisper its own earlier output.

**Not shown.** Short noisy utterances; acoustic (not text) carry-over for
Whisper.
