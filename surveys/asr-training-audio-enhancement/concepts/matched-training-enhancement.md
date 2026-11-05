# Match enhancement exposure to deployment

[G] `single-source`: Zorila et al., *An Investigation into the Effectiveness of
Enhancement in ASR Training and Test for CHiME-5 Dinner Party Transcription*,
ASRU 2019. [Primary full text](https://arxiv.org/html/1909.12208v1),
[retained extract](../related-work/extract/zorila2019-enhancement/html/1909.12208v1.md).

## What the experiment separates

The paper crosses training and test enhancement rather than treating
enhancement as a universal preprocessing improvement. CHiME-5 consists of
real dinner-party speech recorded by worn microphones and six four-channel
arrays. Guided source separation (GSS) uses diarization information; GSS6
uses all 24 array channels. The pipeline combines dereverberation with
separation and is much more informed than generic monaural mastering.

Table 3 reports CNN-TDNNF WER, DEV (EVAL):

| Training enhancement | Hours | Raw evaluation | GSS6 evaluation |
|---|---:|---:|---:|
| None | 2046 | 69.3 (59.9) | 51.8 (51.6) |
| BeamformIt | 680 | 68.9 (59.1) | 48.8 (49.9) |
| GSS1 | 791 | 74.3 (67.5) | 48.0 (47.5) |
| GSS6 | 308 | 78.5 (73.1) | 45.4 (45.7) |

All training configurations retain raw worn-microphone data and use threefold
speed perturbation. Enhanced multichannel views collapse to fewer examples,
so the rows do not hold training hours constant. The result supports matching
training exposure to the deployed signal-processing pipeline; it does not
show that replacing arbitrary poor mono recordings helps raw-audio deployment.

## Why segment conditions matter

Section 5.2 and Figure 5 examine overlap. GSS1's masking damages low-overlap
speech; removing that mask helps this condition but hurts aggregate recognition
on the overlap-heavy data. This is a concrete reason to compare intervention
by defect and segment, rather than infer every segment benefits from a better
whole-corpus score.

The nearest alternatives are raw multi-condition training, simpler beamforming,
and stronger separation. The paper's headline final scores also incorporate
discriminative training, language-model and annotation refinements. They are
not an isolated estimate of enhancement's contribution.
