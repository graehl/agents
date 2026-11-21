**Source:** *An Investigation of Deep Neural Networks for Noise Robust Speech Recognition* — [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/0007398.pdf)

# seltzer2013-noise-aware-training

2026-11-21, sonnet-5.5. Purpose: the original noise-aware training (NAT),
and early evidence on enhancement in front of a neural recognizer. Read:
abstract, method sections 3.1-3.4, experiments and conclusion.

**Claims.** Hybrid DNN-HMM on Aurora 4 (multi-condition training, 7x2048
layers, 3202 senones, filterbank features). Appending a fixed
per-utterance noise estimate (the mean of the first frames, assuming
stationary noise) to every input window is "noise-aware training"
([extract](../extract/seltzer2013-noise-aware-training/seltzer2013-noise-aware-training.md):114-127).
Average WER over the four test sets A-D: baseline 13.4; feature
enhancement before the network 13.8 (better on the clean sets A and C,
worse on the noisy B and D); NAT 13.1; dropout 12.9; NAT plus dropout 12.4
(7.5% relative over the best published Aurora 4 result), lines 171-181.
A DNN trained on multi-condition data without any compensation matched
or beat published GMM-HMM systems that used VTS adaptation (line 199).

**Means for us.** (1) The side-information idea has a small measured gain
from its origin (13.4 to 13.1, about 2% relative alone). (2) The authors
conjecture that feature enhancement makes the network "less robust to
mismatched conditions" because it sees fewer variations in training
(line 171): the 2013 antecedent of the finding that enhancement hurts
robust models. (3) The noise estimate is start-of-utterance and
stationary-noise only; Raj et al. 2020 later replace it with speech and
non-speech means.

**Not shown.** Anything for end-to-end or pretrained encoders; any
non-stationary noise; any carry-over between utterances (the estimate is
recomputed per utterance). The note in Raj 2020 that this start/end
variant hurt Aurora-4 there is a different recipe.
