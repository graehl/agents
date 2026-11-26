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

Lineage and guard rails: Gales's report on maximum-likelihood linear
transforms (MLLR and the constrained feature-space form) was fetched and read
in the third pass ([reading](../related-work/readings/gales1997-mllr-cmllr.md)):
hybrid HMM, unsupervised from the first-pass transcript, unknown-microphone
task 9.00 to 7.15 to 7.99 WER (11 to 21% relative), clean HUB1 eval 9.20 to
7.75 to 8.48. Not fetched: VTS originals, the 1998 journal version, IBM's
lattice-based and Jha's confidence-based MLLR (attested only by search
summaries); Saon 2013 stays unretrieved (only an IBM abstract page, DOI
10.1109/ASRU.2013.6707705 and later papers' citations of it; Wagner 2022
cites it and Raj 2020 reproduces the i-vector baseline). Modern forms read here:
Deng et al. (confidence selection, needs speaker-adaptive training to
work), van Dalen et al. (multi-hypothesis entropy), Lin et al. (reset and
continual), Fang et al. (independent reward). Common finding: raw
first-pass confidence is a poor guard, an adaptation that uses one
transcript propagates its errors, and two guards help (a trained
confidence estimator, or a loss over many hypotheses).

## Third pass additions

**Stateful inference at the encoder (area 6).**

| Mechanism | Recognizer, data | Result | Source |
|---|---|---|---|
| Carry the encoder cache across turns; roll back after a short backchannel turn; vs reset each turn (the common voice-agent practice) | cache-aware FastConformer-RNNT, 114M and 0.6B; CallHome and Switchboard telephone dialogue | 15 to 21% relative WER at utterance onsets; rollback lowest overall WER in all model/dataset pairs; holds at latencies below 250 ms and with VAD turn boundaries; no extra memory | [chattopadhyay2026](../related-work/readings/chattopadhyay2026-fresh-starts.md) |
| Cached, attention-pooled history of preceding utterances | streaming Conformer-transducer, Gigaspeech M 1,000 h | 0.5 to 0.7 absolute (3.1 to 4.3% relative); real-time factor +7.5% (compact) | [cui2023](../related-work/readings/cui2023-compact-context.md) |
| Previous transcript as decoding context | Whisper large-v3, long-form CORAAL and Earnings22 | WER up by over 190 and 500 points (error propagation, loops); contrastive decoding recovers up to 24.3 points | [ahn2026](../related-work/readings/ahn2026-whisper-cd.md) |
| Model bank of adapted checkpoints, with collapse-guarding resets | wav2vec 2.0 base CTC, LibriSpeech-C noises | DM-SUTA vs DSUTA: NB 35.8 vs 36.3, GS 35.8 vs 37.0, BA 34.1 vs 33.2; continual SUTA 68.1 on NB (source 120.1) | [dmsuta2025](../related-work/readings/dmsuta2025-model-bank.md) |
| Backpropagation-free adaptation: a per-utterance vector added to frame embeddings by CMA-ES, smoothed across utterances | wav2vec 2.0 base and HuBERT-large CTC; 4 noisy sets, 16 conditions | 4.1 to 13.5% over BP-free baselines; 2.0 to 6.4 times less GPU memory than BP methods; lowest WER on 3 of 5 sets, up to 30.7% relative over BP methods | [dong2025](../related-work/readings/dong2025-ebats.md) |

Reading: carried acoustic state helps in streaming transducers at inference
time even without retraining (the nearest to "encoders with a rolling state or
marked-boundary history"), while carrying Whisper's own text hurts in
long-form audio. No read paper adapts Whisper unsupervised at test time
with carried speaker state (search summaries
list per-speaker Whisper LoRA studies on dysarthric speech, supervised; not
read). The cross-utterance papers not fetched: arXiv 2508.10456, 2409.08797.
Test-time adaptation follow-ups not fetched: DSS, AWMC, SGEM, SUTA-LM, ZO-ASR.

**Inverse direction (area 5).**
[READ](../related-work/readings/li2026-read.md) scores a transcript by the
likelihood a pretrained discrete-token TTS model (CosyVoice2) gives the
speech tokens given the text, with no extra training. Used to rerank the
top 5 Whisper large-v3 hypotheses and to combine systems (Whisper medium and
large-v3, NeMo, Qwen2.5-Omni) on LibriSpeech, SPGISpeech, Switchboard and
noise-augmented copies: up to 20% relative error reduction, with the largest
advantage at low SNR. This overturns the earlier "no text-to-speech
likelihood score located". Search summaries also named recognizer-based
label scoring (CTC scores), TTS and ASR cycle training (Baskar et al.,
Makishima et al.) and a speech-translation filter using model likelihoods;
none was read. Not found: use of such a score as a training-data
label-quality filter for ASR, energy-based or diffusion models scoring audio
given text, and speech-language-model scoring of a transcript.

## For a phone

Speaker-code or speaker-vector state is small (about 1 K numbers) and fits
a session; fitting it needs backpropagation or an extra encoder pass over
previous audio, which costs compute. Layer-norm-only test-time adaptation
(Lin et al. 2022) is the cheapest located version.
