**Source:** *Bandwidth Embeddings for Mixed-bandwidth Speech Recognition* — [PDF](https://arxiv.org/pdf/1909.02667v1) · [arXiv](https://arxiv.org/abs/1909.02667v1)

# mantena2019-bandwidth-embeddings

2026-11-21, sonnet-5.5. Purpose: bandwidth-conditioned and mixed-bandwidth
recognizers; the audio analogue of erasing an input difference. Read:
abstract, approach, database, baselines, embedding results and summary.

**Claims.** A hybrid DNN acoustic model (2 convolution + dense layers) with
3,400 h wideband (WB) and 600 h narrowband (NB) training data, tested on
54 h WB and 4 h NB sets. WER (WB / NB) in
[extract](../extract/mantena2019-bandwidth-embeddings/html/1909.02667v1.md):129-217:
WB-only model 13.1 / 23.8 (NB test upsampled to 16 kHz); NB-only model
at 8 kHz 22.4 / 21.0; WB+NB mixed without upsampling 13.6 / 26.2;
WB+NB with NB upsampled to 16 kHz 13.4 / 20.9. Adding a learned
embedding of a binary narrowband/wideband flag to the first dense layer:
12.9 / 20.2 (no upsampling) and 13.0 / 18.2 (upsampled), the latter 13%
relative below the NB-only model on NB (line 221). Adding parallel
convolutions per bandwidth and the embedding to the non-upsampled model
reaches a 6% relative NB gain over NB-only while matching WB-only (line 387).

**Means for us.** Mixing narrowband with wideband training data naively
hurts narrowband (26.2 vs 21.0); resampling to a common rate removes
most of that (20.9); a one-bit condition flag as extra input then adds a
further 13% relative. This is the nearest located case where a small
narrowband set is helped by folding it into a larger set through an input
transformation (common sampling rate) plus a condition signal, on a
hybrid DNN, not a pretrained encoder.

**Not shown.** Pretrained or self-supervised encoders; a flag that is
estimated rather than known (the flag here is given from the data
source); lower-resource languages; single-source, hybrid DNN era.
