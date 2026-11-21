**Source:** *An Investigation of End-to-End Models for Robust Speech Recognition* — [HTML](https://arxiv.org/html/2102.06237) · [arXiv](https://arxiv.org/abs/2102.06237)

# prasad2021-e2e-robust

2026-11-21, sonnet-5.5. Purpose: noise-augmented training vs the same plus
a noise-type classification target (multitask) vs the opposite, a
gradient-reversal noise classifier. Read: introduction, noise data, methods
4.2-4.4, Table 3 and discussion; Table 2 was not transcribed.

**Claims.** DeepSpeech2-style E2E CTC model with a small custom noise set
(seven types: babble, airport/station, car, metro, cafe, traffic, AC/vacuum,
plus clean). Data augmentation training (DAT, soft-freezing, noise added to
half of utterances): clean WER 10.90, 0 dB babble 77.4. Multitask learning
with an auxiliary noise-type classifier after LSTM 2 (MTL): clean 11.05,
babble 0 dB 71.4, cafe 0 dB 44.9 vs 49.1 (DAT), AC/vacuum 0 dB 57.0 vs 63.1
([extract](../extract/prasad2021-e2e-robust/html/2102.06237.md):720). Adversarial
training (AvT, gradient reversal on the noise classifier) trades clean
accuracy for noisy accuracy: clean WER 13.07 to 13.79 against about 11;
it is best at low SNR and sometimes behind MTL at high SNR (line 732). Both
MTL and AvT are "significantly better than the DAT techniques" (line 732).
Among enhancement front ends Demucs beat the others; the conclusion states
adversarial learning gave the largest gains on non-stationary noise types
and Demucs on relatively stationary ones (line 736).

**Means for us.** A direct arm comparison: augmentation only, plus explicit
noise-type as a training target (condition-aware, gains of 8 to 20%
relative at 0 dB, clean unchanged), plus the opposite (condition-invariant,
larger low-SNR gains, clean cost 20%). On a small CTC model with a small
noise set.

**Not shown.** Large pretrained encoders; real recordings; a noise-type
input (as opposed to target).
