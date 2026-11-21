**Source:** *Channel-Aware Pretraining Of Joint Encoder-Decoder Self-Supervised Model For Telephonic-Speech ASR* — [HTML](https://arxiv.org/html/2211.01669) · [arXiv](https://arxiv.org/abs/2211.01669)

# sukhadia2023-channel-aware

2026-11-21, sonnet-5.5. Purpose: pooling narrowband and wideband audio for a
self-supervised encoder and a channel indicator. Read: abstract, datasets,
baselines, results Tables 2-5.

**Claims.** A HuBERT-style encoder with a Transformer decoder, pretrained on
LibriSpeech-360 (16 kHz), Switchboard-300 (8 kHz) or both, then fine-tuned on
100 h. Narrowband test (Switchboard dev WER): wideband-only pretraining
17.8, narrowband-only 16.8, simple pooling 13.2, pooling with non-overlapping
cluster IDs per channel (a channel indicator) 12.6, about 5% relative
([extract](../extract/sukhadia2023-channel-aware/html/2211.01669.md):185).
Wideband test (LibriSpeech 100 h fine-tune, test-clean / test-other): wideband-only 11.5 / 30.6;
narrowband-only 12.9 / 33.6; pooled 8.2 / 22.3; channel-aware 7.6 / 21.5
(line 237). On pseudo-narrowband test sets (8 kHz downsampling) the channel
indicator gives about 6.7% and 3.2% on LibriSpeech and 4.0% on TED-LIUM (lines
243-244). Its reference list names Zhuang et al. 2017 (Bluetooth
narrowband) and Li et al. 2012 (mixed-bandwidth CD-DNN-HMM).

**Means for us.** Pooling 8 kHz and 16 kHz audio in pretraining helps both
bandwidths, and a bandwidth-style channel indicator adds 4 to 7% relative on
top. The pooled model also sees more data (660 h vs 360 h), so part of the
pooling gain is data quantity.

**Not shown.** Lower-resource languages; Whisper-scale models; the
effect of a channel flag when the model is fine-tuned on mixed data; no
SpecAugment comparison.
