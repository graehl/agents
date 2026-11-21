**Source:** *FFASR: Benchmarking Far-Field Automatic Speech Recognition using High-Fidelity Simulated RIRs* — [PDF](https://arxiv.org/pdf/2609.38897) · [arXiv](https://arxiv.org/abs/2609.38897)

# saini2026-ffasr

2026-11-21, sonnet-5.5. Purpose: a benchmark with matched static and moving-talker
conditions. Read: abstract, benchmark construction, Table III, setup.

**Claims.** 15,637 held-out utterances (newly recorded anechoic speech,
15 talkers) in nine conditions: anechoic near field, a measured vs
simulated office lab pair, static high/mid/low SNR, and moving-talker
variants at matched SNR; hybrid wave/geometrical-acoustics room impulse
responses from 14 furnished rooms; scenes with up to two interferers,
including directional transient sources and ambient noise (figure 2
caption, line 174). Mean WER across 15 leading systems
([extract](../extract/saini2026-ffasr/html/2609.38897.md):182-210): near field 4.4%;
static high / mid / low SNR 10.1 / 20.5 / 41.3%; moving high / mid / low
11.5 / 23.2 / 43.5%; motion penalty 1.3 / 2.7 / 2.2 points; measured vs
simulated lab differ by 1.3 points on average. Moving talker is simulated
by a time-varying room impulse response along a trajectory while
interferers stay fixed (lines 140-152).

**Means for us.** Moving talker is a small penalty (1 to 3 points on a
base of 10 to 41%) in simulation. The benchmark simulates a moving
source with a static microphone, not a handheld microphone, and no mid-
recording route changes.

**Not shown.** Transient noise as its own condition; a phone; a
conditioned or adapted recognizer.
