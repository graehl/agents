**Source:** *An analysis of environment, microphone and data simulation mismatches in robust speech recognition* — [PDF](https://eprints.whiterose.ac.uk/111196/1/vincent_CSL16.pdf)

# vincent2017-mismatches

2026-11-21, sonnet-5.5. Purpose: how much environment, microphone and
simulated-vs-real mismatch costs a recognizer trained with multi-condition
data. Read: abstract, introduction, mismatch definitions and parts of the
environment and microphone sections; tables not transcribed.

**Claims.** On CHiME-3, with the exception of MVDR beamforming, most
algorithms behave consistently on real and simulated data and can benefit
from training on simulated data; training on different noise environments
and different microphones "barely affects the ASR performance, especially
when several environments are present in the training data: only the number
of microphones has a significant impact"
([extract](../extract/vincent2017-mismatches/vincent2017-mismatches.md):39).
The log-likelihood ratio used to characterize environment mismatch does not
predict ASR WER (line 426).

**Means for us.** Evidence that diverse training conditions (multiple
environments) neutralize the mismatch that an explicit condition estimate
would address, at least for these tablet recordings and a hybrid recognizer;
the number of microphones is the exception.

**Not shown.** End-to-end or pretrained models; effect of a condition
input.
