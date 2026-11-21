**Source:** *Normalise or condition? Noise-floor front-ends for on-board keyword spotting under UAV rotor ego-noise* — [PDF](https://arxiv.org/pdf/2609.31699) · [arXiv](https://arxiv.org/abs/2609.31699)

# lin2026-normalise-or-condition

2026-11-21, sonnet-5.5. Purpose: a controlled arm with augmentation (noise
in training) only against augmentation plus an explicit per-band noise-floor
input estimated over the preceding seconds, and against subtracting it.
Keyword spotting, not recognition. Read: abstract, method, Table 1, text
of sections 3.1-3.3.

**Claims.** Small-footprint keyword spotters (BC-ResNet 57 k to 349 k
parameters) on 10 command words under real quadrotor ego-noise, trained on
one drone and tested on another. The noise floor per band is tracked over
the two seconds before the decision window. Normalising (subtract the floor,
NFN) vs conditioning (the floor as a second input channel, NPC; level-anchored
NPC-a). Table 1, mean accuracy over seven noisy SNRs (BC-ResNet-8), trained
with the other drone's noise (E): plain log-mel 81.2% (false-alarm rate 3.6%);
NFN 83.2% (6.9%); NPC 83.1% (4.9%); NPC-a 83.5% (2.8%); PCEN 84.0% (3.9%);
PCEN plus NPC-a 84.5% (1.5%)
([extract](../extract/lin2026-normalise-or-condition/html/2609.31699.md):73-97).
With generic speech-commands noise in training (G): log-mel 72.3% (43.1%),
NFN 77.5%, NPC 78.1% (30.3%). Gains from noise-aware front ends are 1.9 to
2.8 points on average with matched-type noise training, mostly below 0 dB
(line 197). In streaming operation on 4.4 h of speech-free rotor noise at 1
false alarm per hour, normalising fronts fall below plain log-mel (0 dB:
NFN 75.3 vs 84.2%) while conditioning keeps log-mel's false-alarm rate and
adds hits (line 207).

**Means for us.** The one located paper that runs the exact comparison:
noise-augmented training alone vs the same plus a per-band running
noise-floor input. Under matched-type noise training the explicit
condition adds about 2 points; under mismatched noise training it adds
5.8 points; and it is better than subtracting the estimate when
false alarms matter.

**Not shown.** Recognition (vocabulary of ten words plus unknown and
silence); speech-like interferers (listed by the authors as the remaining
failure); any pretrained encoder.
