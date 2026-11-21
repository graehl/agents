**Source:** *Joint Training of Speech Enhancement and Self-supervised Model for Noise-robust ASR* — [PDF](https://arxiv.org/pdf/2205.13293v1) · [arXiv](https://arxiv.org/abs/2205.13293v1)

# zhu2022-joint-se-ssl

2026-11-21, sonnet-5.5. Purpose: front ends trained jointly with a wav2vec
2.0-class model, and fusing noisy with enhanced features. Read: abstract,
method summary, Tables I-V discussion, Table IV in full.

**Claims.** An enhancement module plus a wav2vec 2.0 model trained jointly
(pre-training on 100 to 460 h LibriSpeech with synthetic noise, then
fine-tuning on 100 h), with a dual-attention fusion of noisy and enhanced
features. In their noise-set average WER (SNR 0 to 20 dB), the
noisy-only enhanced-target model (EW2) reaches 16.23; adding the jointly
trained SE module with fusion reaches 14.55 (initialized from the public
wav2vec 2.0 checkpoint), and 14.98 without a pretrained initialization
([extract](../extract/zhu2022-joint-se-ssl/zhu2022-joint-se-ssl.md):306-315).
Joint SE-only (SEW2) from random initialization is poor (29.36), with a
pretrained initialization 15.17 to 15.44, which the authors read as the
pretrained model absorbing the SE module's distortion (line 294). Fusing
noisy and enhanced features recovers information lost by enhancement alone.

**Means for us.** Two supports for the prior: (1) a pretrained encoder
reduces the distortion cost of an attached enhancer; (2) the best result
keeps the noisy path, as observation adding does. Gains are about 1 to 1.7
WER points on a 100 h-labelled base model, small relative to what
fine-tuning on noisy data already gives.

**Not shown.** Large supervised recognizers; real noise beyond CHiME-4,
where the table's row alignment is ambiguous in the extract (we do not
cite its CHiME-4 numbers). Effect is shown with synthetic training noise
and a small labelled set; comparison with simply fine-tuning on noisy data
at equal budget is in the paper's baselines but not the comparison we need.
