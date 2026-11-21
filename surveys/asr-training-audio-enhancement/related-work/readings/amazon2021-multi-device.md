**Source:** *Unified modeling of multi-domain multi-device ASR systems* — [PDF](https://cdn.amazon.science/ba/d7/679a60ab4bcdb9a8b57f34a5dc45/unified-modeling-of-multi-domain-multi-device-asr-systems.pdf)

# amazon2021-multi-device

2026-11-21, sonnet-5.5. Purpose: device ID as explicit input, device experts
and a device-removing adversary, in one pooled recognizer. Read: abstract,
method, setup, Table 1 and analysis.

**Claims.** Amazon Alexa RNN-T (40.6 M parameters), Indian-English queries
from three device types, 15 K h human plus 45 K h machine transcribed.
All numbers are WER reduction relative to three individually fine-tuned
device-specific models (absolute WER withheld by the authors; positive is
better), columns for the three devices
([extract](../extract/amazon2021-multi-device/amazon2021-multi-device.md):103-123):
adversarial device removal (DAT) 3.9 / 2.5 / 1.4%; a larger single
model 3.8 / 3.1 / 3.5%; device-type one-hot as input to all encoder and
decoder layers 3.6 / 0.8 / -0.6%, to the decoder only -0.5 / -3.7 / -2.1%;
mixture of device experts (adapters switched by device ID) 5.4 to 7.9 / 1.5
to 5.0 / 2.2 to 5.7%; attentive mixture of experts up to 10.3 / 5.8 / 4.5%
(+7.0 M parameters, 7.3 on the third). Device ID input "gave some gains for
P1 and P2 but for P3 some regression" (line 131).

**Means for us.** In a production transducer a device-ID input alone is a
weak and inconsistent lever (about -4 to +4%), adversarial removal is a
steady small gain, and device-specific parameters selected by the ID give
the largest gains (up to 10%) for modest parameter cost. All arms use the
device ID known, not estimated.

**Not shown.** Augmentation-only arm versus ID arm (the baselines are
fine-tuned device models); unseen devices (the ID needs to be known); any
public benchmark; absolute WER.
