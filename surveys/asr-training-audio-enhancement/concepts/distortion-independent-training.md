# A frozen enhancer can outperform joint tuning

[G] `single-source`: Plantinga, Bagchi and Fosler-Lussier, *Perceptual Loss with
Recognition Model for Single-Channel Enhancement and Robust ASR*, arXiv 2021.
[Primary PDF](https://arxiv.org/pdf/2112.06068v1),
[retained extract](../related-work/extract/plantinga2021-perceptual/plantinga2021-perceptual.md).

The enhancer learns a spectral loss plus a perceptual loss from intermediate
phonetic representations. Its purpose is to retain recognition-relevant local
features, which need not be the features rewarded by a powerful full-word
recognizer. The paper's distortion-independent setup freezes the pretrained
enhancer while training the recognizer with additional noise.

## Voicebank+DEMAND comparison

Sections V.C–VI and Table VI use a LibriSpeech-pretrained recognizer fine-tuned
for 30 epochs, with OpenRIR noise augmentation at 0–15 dB. Enhancer and encoder
are frozen for the first three epochs of fine-tuning; the main contrast is
whether enhancement subsequently stays frozen or is jointly tuned.

| Pipeline | DEV WER | Test WER |
|---|---:|---:|
| Clean | 1.44 | 2.29 |
| Noisy | 4.32 | 3.43 |
| Spectral masking, joint | 3.12 | 3.77 |
| Spectral + perceptual, joint | 3.57 | 3.58 |
| Spectral masking, frozen | 2.88 | 3.25 |
| Spectral + perceptual, frozen | 2.89 | 2.80 |

The frozen perceptual enhancer improves test WER over noisy training/evaluation
in this setup, while joint training does not. However, enhancement is also
present at inference. This does not demonstrate that enhancing only training
audio improves a raw-deployment recognizer.

Table IX tests a recognizer trained on noisy inputs with enhancement inserted
only for evaluation: spectral enhancement yields 3.58% test WER and perceptual
enhancement 3.34%, against the same 3.43% noisy baseline. Training exposure
therefore changes the result. The nearest alternatives are spectral-loss-only
enhancement, jointly optimized enhancement/recognition, and direct noisy
training; their relative ordering is specific to this dataset and recipe.

The design implication is to retain frozen and joint variants as separate
hypotheses. Iwamoto's later artifact study obtains improvements from ASR-aware
enhancer adaptation in another setup, so this result cannot settle that choice
for a new training corpus.
