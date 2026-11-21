# Carried state, speaker/session adaptation and transcript-driven fitting

[G] `single-source` per result. Full texts: Gomez-Alanis et al. 2022
([HTML](https://arxiv.org/html/2210.16238v1)), Wagner et al. 2022
([HTML](https://arxiv.org/html/2211.08774v3)), van Dalen et al. 2025
([HTML](https://arxiv.org/html/2506.10653)), Deng et al. 2023
([HTML](https://arxiv.org/html/2302.07521)), Lin et al. 2024
([HTML](https://arxiv.org/html/2406.11064v2)), Fang et al. 2026
([HTML](https://arxiv.org/html/2603.05231v1)). Notes in
[readings](../related-work/readings/).

## Two ideas, one table

Idea A: keep an explicit running estimate (speaker, channel, microphone
path, room) across utterances and give it to the recognizer. Idea B: use
the first-pass transcript, top-down, to fit that estimate (the
MLLR/fMLLR lineage), guarding against adapting to errors.

| Mechanism | Recognizer, setting | Result | Source |
|---|---|---|---|
| Previous (and future) utterance audio fed to the encoder, learned implicitly | Conformer-transducer, 50 K h far-field assistant audio | streaming: 2.9% (1 past), 5.4% (2 past) relative WER; dual-mode 6.3%; non-streaming up to 12.1% with one past plus one future | [gomezalanis2022](../related-work/readings/gomezalanis2022-contextual-utterance.md) |
| Per-utterance speaker vectors (i-/x-vector, ECAPA) concatenated | transformer; wav2vec 2.0 base; LibriSpeech and Switchboard with added noise | transformer up to 16.3% relative, rising with noise; wav2vec 2.0 up to 6.3%, vanishing at 9 and 0 dB SNR | [wagner2022](../related-work/readings/wagner2022-speaker-adaptation-noisy.md) |
| Speaker code (1024 numbers) fitted unsupervised from 1 to 10 min, entropy loss over multiple hypotheses | 100M Conformer, far-field noise-augmented Common Voice | 24.4% unadapted; 22.2% with code-trained model and zero code; 19.4% adapted (20% rel.), 29% with 10 min | [vandalen2025](../related-work/readings/vandalen2025-entropy-speaker-codes.md) |
| Speaker-dependent parameters from first-pass transcript, confidence-selected | Conformer AED; Switchboard 300 h, AMI 233 h | 9.5 to 11.3% relative (Switchboard), 8.9 and 10.2% (AMI); selection beats using all data; without speaker-adaptive training, test-time adaptation gave no significant gain | [deng2023](../related-work/readings/deng2023-confidence-speaker-adaptation.md) |
| Continual vs reset-each-utterance test-time adaptation | wav2vec 2.0 base CTC; noise types and CHiME-3 | CHiME-3 30.0 source; 23.3 reset each time; 21.7 carried state; changing-condition stream MD-Hard 60.4 reset vs 39.8 carried with dynamic reset; naive carried state collapses (83.6) | [lin2024](../related-work/readings/lin2024-dsuta.md) |
| Confidence vs independent reward as the adaptation signal | Whisper-Tiny, MS-SNSD noises at 10 dB | SUTA 32.27 vs 32.71 baseline, worse on 3 of 8 noises; reward-based 28.64 | [fang2026](../related-work/readings/fang2026-asr-tra.md) |

## What this says about the owner's bet

The bet: explicit running analysis wins in the field over noise-augmented
training alone. No located paper compares the two head to head. The
located evidence:

- Carrying information across utterances helps in every modern case read
  (2.9 to 20% relative), so the direction is supported.
- None of these is a replacement for augmentation. van Dalen's baseline is
  already trained on augmented data and the code adds to it; Lin's
  per-utterance baseline has no carried state; Gomez-Alanis' baseline has
  no history. The comparison "augmentation alone vs augmentation plus
  carried state" is therefore answered (plus helps); "state instead of
  augmentation" is not.
- Whether the explicit estimate beats leaving the encoder to infer from
  each utterance: the most direct hint is negative for large pretrained
  encoders: a late-injected utterance vector gave wav2vec 2.0 a smaller
  gain than a from-scratch transformer, and none in strong noise (Wagner);
  and Whisper's encoder already carries noise information (Gong, in
  [side information](condition-side-information.md)). Both are indirect.
- The gains are 5 to 20% relative on small to mid-sized recognizers;
  nothing was found on Whisper-class recognizers.

## On using the transcript top-down

Lineage and guard rails: Seltzer-style conditioning and MLLR/fMLLR are
hybrid-era (not fetched: MLLR, fMLLR, VTS originals; IBM's lattice-based
MLLR is attested only by a search summary). Modern forms read here:
Deng et al. (confidence selection, needs speaker-adaptive training to
work), van Dalen et al. (multi-hypothesis entropy), Lin et al. (reset and
continual), Fang et al. (independent reward). Common finding: raw
first-pass confidence is a poor guard, an adaptation that uses one
transcript propagates its errors, and two guards help (a trained
confidence estimator, or a loss over many hypotheses).

## For a phone

Speaker-code or speaker-vector state is small (about 1 K numbers) and fits
a session; fitting it needs backpropagation or an extra encoder pass over
previous audio, which costs compute. Layer-norm-only test-time adaptation
(Lin et al. 2022) is the cheapest located version.
