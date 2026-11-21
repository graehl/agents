**Source:** *Dynamic Model-Bank Test-Time Adaptation for Automatic Speech Recognition* — [PDF](https://aclanthology.org/2025.emnlp-main.1107.pdf)

# dmsuta2025-model-bank

2026-11-21, sonnet-5.5. Purpose: follow-up to DSUTA on collapse in continual
test-time adaptation. Read: abstract, introduction, method, Table 1 and
benchmarks; Table 2 not transcribed.

**Claims.** A bank of adapted checkpoints, with a subset chosen per
utterance by confidence and uncertainty, and bank maintenance that resets
collapsed or inactive models. Source model wav2vec 2.0-base fine-tuned on
LibriSpeech (as in SUTA and DSUTA). WER (%) per noise type (Table 1,
[extract](../extract/dmsuta2025-model-bank/dmsuta2025-model-bank.md):118-135),
source / continual SUTA / DSUTA / DM-SUTA: NB 120.1 / 68.1 / 36.3 / 35.8; BA
66.9 / 63.4 / 33.2 / 34.1; GS 75.6 / 58.4 / 37.0 / 35.8; CM 49.7 / 53.4 /
33.5 / 32.5; AA 40.6 / 39.8 / 25.9 / 25.2. Multi-domain streams MD-Easy
(2,500 samples), MD-Hard, MD-Long (10,000 samples, random segment lengths of
20 to 500) are defined in the paper (lines 153-155).

**Means for us.** The follow-up improves on DSUTA by 0 to 1 WER point on most
noise types; the collapse risk of naive continual adaptation (continual SUTA)
is again visible.

**Not shown.** Whisper-class models; changes in microphone or device.
