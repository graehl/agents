**Source:** *The third CHiME speech separation and recognition challenge: Analysis and outcomes* — [PDF](https://eprints.whiterose.ac.uk/110977/1/barker_csl.pdf)

# barker2017-chime3

2026-11-21, sonnet-5.5. Purpose: the handheld tablet benchmark and what it
characterizes about non-stationary noise and device variation. Read: abstract,
data and task, environment and channel analysis (sections 2 and 3); the
participant-results section was not read.

**Claims.** Six-microphone tablet held by the talker in four real noise
environments (bus, cafe, street, pedestrian area) with a booth reference;
8 hours of separate background recordings; simulated training data built
with time-varying impulse responses modelling talker motion
([extract](../extract/barker2017-chime3/barker2017-chime3.md):73-126). Using a
GMM likelihood decay over time since a training segment, pedestrian and
cafe backgrounds are the most stationary, the bus less so and the street
the least, dominated by a passing vehicle so that level changes over a
6 s utterance (line 161-177). The authors caution that a smooth
approaching-car change differs from distinct events in a cafe that the
frame-independent model cannot see (line 185). Microphone failures
(cross-channel energy correlation) concentrate in channels 3 to 5 and in
the bus, pedestrian and street environments, not the booth or cafe
(line 195-199). Talker speech level and rate vary widely across talkers
(line 211).

**Means for us.** CHiME-3 is the handheld-device benchmark that measures
non-stationarity and device failures directly, with simulated motion in
training. The participants' WER outcomes are not read here.

**Not shown (in the parts read).** Results of submitted systems; any
carried-state or adaptation arm.
