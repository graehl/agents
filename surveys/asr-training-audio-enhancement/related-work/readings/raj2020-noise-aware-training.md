**Source:** *Frustratingly Easy Noise-aware Training of Acoustic Models* — [PDF](https://arxiv.org/pdf/2011.02090v2) · [arXiv](https://arxiv.org/abs/2011.02090v2)

# raj2020-noise-aware-training

2026-11-21, sonnet-5.5. Purpose: noise-aware training, utterance-level
condition vectors and i-vector style conditioning as side information.
Read: abstract, related work, method, Tables 2-4, comparison text.

**Claims.** Append to every input frame a "noise vector": the mean feature
vector of speech frames and of non-speech frames, split by a speech
activity detector, estimated over the utterance (offline) or online by
maximum likelihood. Hybrid TDNN/TDNN-F lattice-free MMI models. WER
([extract](../extract/raj2020-noise-aware-training/raj2020-noise-aware-training.md):89-103):
AMI single-distant-microphone dev/eval, base 38.8/42.6, i-vector 35.2/39.4,
Seltzer-style noise vector from the first and last 10 frames (NAT-vector)
38.1/42.0, noise vector 34.9/38.8 (10% relative); Aurora-4 eval-92, base
7.94, i-vector 8.24 (worse), NAT-vector 8.17 (worse), noise vector 7.37
(7.1% relative). Online estimates reach 35.4 and 7.72. Combined with
i-vectors on AMI about 12.8% relative; with multi-condition training on
Aurora-4 (6x data) 21.6% relative over baseline, where multi-condition
training alone is better than noise vectors but the two are
complementary (lines 153-161).

**Means for us.** Utterance-level condition vectors help hybrid models on
mismatched noise and reverberation, but not uniformly (i-vectors and
Seltzer's noise vectors hurt Aurora-4); they add to, and do not replace,
multi-condition data. Per-band information here is the mean spectrum of
non-speech frames, so it is a per-band noise-level estimate fed as input.

**Not shown.** Any end-to-end, Conformer or pretrained encoder; the claim
about Seltzer et al.'s original 2013 paper is not read, only its
re-implementation here (that paper's own numbers are a lead).
