**Source:** *Continual Test-time Adaptation for End-to-end Speech Recognition on Noisy Speech* — [HTML](https://arxiv.org/html/2406.11064v2) · [arXiv](https://arxiv.org/abs/2406.11064v2)

# lin2024-dsuta

2026-11-21, sonnet-5.5. Purpose: carrying adapted state across utterances
(continual test-time adaptation) versus resetting after each utterance,
including through changing conditions. Read: introduction, method, results
tables 1-3 and discussion.

**Claims.** Source model: wav2vec 2.0 base fine-tuned on LibriSpeech 960 h
(CTC). Dynamic SUTA (DSUTA) keeps slowly updated "meta-parameters"
across utterances and does a fast per-utterance adaptation on top; a
dynamic reset triggers when a loss-based shift statistic exceeds a
threshold. Single-domain streams, WER (%), noise types AA, AC, BA, CM, GS,
MU, NB, SD, TP, VC on LibriSpeech-C, and CHiME-3
([extract](../extract/lin2024-dsuta/html/2406.11064v2.md):239): source model
CM 49.7, NB 120.1, CHiME-3 30.0; per-utterance reset SUTA 38.7, 112.3,
23.3; naive continual SUTA (CSUTA) 53.4, 68.1, 27.6; AWMC (pseudo-label
continual with an anchor) 37.7, 131.9, 22.4; DSUTA 33.5, 36.3, 21.7.
Multi-domain time-varying streams (Table 2, line 259): source 32.7 / 74.6 /
61.0 (MD-Easy / MD-Hard / MD-Long); SUTA 24.0 / 60.4 / 53.3; CSUTA 37.3 /
83.6 / 100.3 (worse than the source model); DSUTA 24.0 / 45.6 / 43.2; with
dynamic reset 22.7 / 39.8 / 35.8; with fixed-interval reset 22.8 / 49.4 /
45.2.

**Means for us.** Direct comparison of "carry state" with "start fresh each
utterance", on a modest CTC recognizer: carrying state wins by a wide
margin when conditions persist, collapses when naive and conditions change
(CSUTA), and needs a shift detector to stay good when conditions switch
(MD-Hard 60.4 for reset-each-time vs 39.8 with carried state plus dynamic
reset). This is the nearest test of the "switch of audio path mid-session"
case. It is carried model state, not an explicit channel estimate, and the
comparison is against per-utterance adaptation, not noise-augmented
training.

**Not shown.** Whisper-class or Conformer transducers; comparison with a
recognizer trained with noise augmentation; phone compute (adaptation
needs backpropagation); conditions are synthetic noise types switching at
fixed boundaries.
