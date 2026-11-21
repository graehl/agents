**Source:** *Invariant Representations for Noisy Speech Recognition* — [PDF](https://arxiv.org/pdf/1612.01928) · [arXiv](https://arxiv.org/abs/1612.01928)

# serdyuk2016-invariant

2026-11-21, sonnet-5.5. Purpose: domain-adversarial (condition-removing)
training against multi-condition training as a function of how many noise
types were seen. Read: abstract, method, experiments, Table 1.

**Claims.** Hybrid DNN (6 x 2048) on Aurora-4; a binary clean/noisy domain
classifier on layer 4 trained with a gradient-reversal style adversary.
Average WER across all test conditions, invariance vs multi-condition
baseline, by number of noise types seen in training: 1 type 16.36 vs 18.14;
2 types 15.56 vs 17.39; 3 types 14.24 vs 14.67; 4 types 13.61 vs 13.84; 5
types 13.41 vs 13.02; 6 types (all) 12.62 vs 12.60 (the "invariance" column
first; [extract](../extract/serdyuk2016-invariant/serdyuk2016-invariant.md):75-86).
The authors conclude the gain is largest when few noise types are
available (lines 92).

**Means for us.** Removing the condition helps when augmentation covers few
conditions and vanishes with full multi-condition coverage. Supports the
view that coverage in training, not an extra mechanism, closes the gap.

**Not shown.** E2E or pretrained models; the explicit-input alternative.
