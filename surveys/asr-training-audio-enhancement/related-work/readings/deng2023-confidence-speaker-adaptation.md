**Source:** *Confidence Score Based Speaker Adaptation of Conformer Speech Recognition Systems* — [HTML](https://arxiv.org/html/2302.07521) · [arXiv](https://arxiv.org/abs/2302.07521)

# deng2023-confidence-speaker-adaptation

2026-11-21, sonnet-5.5. Purpose: confidence-weighted guard against adapting
to first-pass errors, for a modern end-to-end recognizer; speaker-level
adaptation. Read: abstract, method, introduction, results discussion for
Switchboard and AMI.

**Claims.** Compact speaker-dependent parameters (LHUC, hidden-unit bias,
parameterized activation, linear hidden network) are fitted at test time
to a speaker's data from the first-pass transcript of a Conformer
(attention-encoder-decoder). Without speaker-adaptive training, test-time
adaptation gave no significant gain over the speaker-independent model
([extract](../extract/deng2023-confidence-speaker-adaptation/html/2302.07521.md):689);
with it, it did. Selecting only the most confident part of each speaker's
data using a trained confidence estimator, plus Bayesian handling of the
parameters, beat adaptation on all data: on Switchboard Hub5'00 / RT02 /
RT03, 1.0 / 1.3 / 1.4 absolute (9.5% / 10.9% / 11.3% relative) over the
speaker-independent Conformer; on AMI dev/eval 2.7 and 3.3 absolute (8.9%
and 10.2% relative). Confidence-selected over unselected adaptation:
e.g. 0.7% absolute on the RT03 FSH subset, and AMI 0.7 to 2.6 absolute (3.4
to 6.3% relative; lines 1614, 2236).

**Means for us.** Modern descendant of confidence-weighted MLLR: a
recognizer's own raw softmax confidence is unreliable in attention
models, so a small separate confidence module was trained; selecting about
70% of adaptation data (AMI) beat using all. Unsupervised speaker
adaptation needs speaker-adaptive training to work at all in this setup.

**Not shown.** Pretrained or Whisper-class recognizers; noisy or phone
conditions beyond Switchboard and AMI; small data (300 h and 233 h
corpora, lots of per-speaker data); phone compute.
