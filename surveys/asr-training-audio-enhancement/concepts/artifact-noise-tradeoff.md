# Preserve speech cues even if residual noise increases

[G] `single-source` per experiment; related studies by substantially the same
author group, not independent replications:

- Iwamoto et al., *How does end-to-end speech recognition training impact speech
  enhancement artifacts?*, arXiv 2023.
  [Primary full text](https://arxiv.org/html/2311.11599v1),
  [extract](../related-work/extract/iwamoto2023-artifacts/html/2311.11599v1.md).
- Ochiai et al., *Rethinking Processing Distortions: Disentangling the Impact of
  Speech Enhancement Errors on Speech Recognition Performance*, arXiv 2024.
  [Primary full text](https://arxiv.org/html/2404.14860v1),
  [extract](../related-work/extract/ochiai2024-distortions/html/2404.14860v1.md).

## Enhancement artifacts are a distinct error component

Orthogonal projection decomposes enhancement error into speech-related error,
residual interference/noise, and an artifact component outside the reference
signals' span. Ochiai et al. scale these components separately in simulated
English and Japanese noisy/reverberant speech. In their tested recognizers,
reducing artifacts improves recognition more than reducing residual noise or
interference. The decomposition needs reference sources and cannot directly
score arbitrary unpaired recordings.

Two practical interventions follow: penalize artifacts more in enhancer
training, or mix part of the noisy observation back into enhanced output
(observation adding). The latter reduces artifact concentration at the expense
of admitting noise. A higher signal-to-noise ratio is therefore not a reliable
recognition objective.

## Strong recognizers still suffer from independently trained enhancement

Iwamoto et al. combine Conv-TasNet with a Transformer CTC/attention recognizer
and frozen WavLM-Large features on CHiME-4. Table 1 reports real EVAL WER:

| Configuration | WER |
|---|---:|
| Raw audio | 4.8 |
| Independently trained enhancement | 9.4 |
| Fine-tune recognizer only on enhanced inputs | 8.8 |
| Fine-tune enhancer with ASR loss | 3.9 |
| Joint fine-tuning | 3.8 |
| Independent modules plus observation adding | 4.3 |

Adapting the recognizer alone does not remove the problem. ASR-aware enhancer
tuning reduces artifacts while accepting more residual noise. These are
enhanced-inference comparisons; they do not by themselves establish a benefit
from offline enhancement of training data for raw deployment.

## Mixed training offers a more relevant, confounded precedent

Ochiai et al. Table V explicitly crosses training input and evaluation input.
The recognizer is a Kaldi DNN-HMM trained with lattice-free MMI and decoded
with a trigram language model. On simulated single-talker WSJ+CHiME, raw-input
evaluation gives:

| Training inputs | Raw-test WER |
|---|---:|
| Noisy originals | 15.9 |
| Time-domain enhancement only | 30.5 |
| Frequency-domain enhancement only | 23.9 |
| Originals + time-domain enhancement | 15.5 |
| Originals + frequency-domain enhancement | 14.9 |

Section V-B2 states that combined training doubles both utterances and
iterations. Its modest raw-test gains nominate enhancement as augmentation;
an equal-update repeated-original control is needed to isolate why it helps.
Enhanced-only training instead creates a large mismatch. Under matched
enhanced inference, the same table has better results, which answer a different
deployment question.

Table VI extends the inference-side finding to real CHiME-3 recordings: raw
WER is 28.7%, conventional signal-to-noise-loss enhancement 31.7%, artifact-
penalized enhancement 22.3%, and conventional enhancement with observation
adding 22.5%. The mixing weights were tuned; they are not universal constants.
The nearest alternatives are no enhancement, conventional denoising loss,
recognizer-only adaptation and retaining raw examples.
