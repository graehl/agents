**Source:** *Robust wav2vec 2.0: Analyzing Domain Shift in Self-Supervised Pre-Training* — [PDF](https://arxiv.org/pdf/2104.01027) · [arXiv](https://arxiv.org/abs/2104.01027)

# hsu2021-robust-w2v2

2026-11-21, sonnet-5.5. Purpose: how large-scale self-supervised recipes
handle 8 kHz telephone data and multi-domain pooling. Read: abstract, setup,
sections 4.1-4.8 text; tables 2-7 partly.

**Claims.** All data are resampled to 16 kHz for consistency, including the
8 kHz Switchboard and Fisher telephone corpora and the 48 kHz Common Voice
([extract](../extract/hsu2021-robust-w2v2/hsu2021-robust-w2v2.md):55-57).
Adding unlabeled in-domain audio (for example telephone) to pre-training
closes 66 to 73% of the gap between a model fine-tuned on out-of-domain
labels and one fine-tuned on in-domain labels (line 13). Pre-training on
several domains improves unseen domains: a LARGE model pre-trained on
Libri-Light, Switchboard+Fisher and Common Voice and fine-tuned on
LibriSpeech cuts WER by a relative 35 to 50% on Switchboard, Common Voice and
TED-LIUM against the single-dataset baseline in the cited prior work
(line 210).

**Means for us.** The standard recipe for mixed-bandwidth is plain
upsampling to a common rate and pooling; no bandwidth flag is used. Telephone
audio in the pre-training mix is the dominant gain for telephone test sets.

**Not shown.** An ablation of the upsampling itself or of a channel flag;
codec effects; lower-resource languages (English only).
