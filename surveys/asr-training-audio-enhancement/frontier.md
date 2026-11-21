# Candidate tests for poor training audio

Grounded inputs: [field survey](survey.md), four read primary sources through
2026-11-05. Proposed tests below are hypotheses, not established improvements
or novelty claims. None has been run for the motivating corpus.

## Preserve originals before trying wholesale replacement

Ochiai et al.'s mixed-training result makes original-plus-enhanced augmentation
the most direct small test: compare raw-only, repeated raw-only, enhanced-only,
and original-plus-enhanced under equal optimizer updates and audio exposure.
Use unprocessed deployment evaluation and repeat seeds. A gain over raw-only
that disappears against repeated raw-only would reject enhancement-specific
benefit in that setup. Revisit the claim after a matched-compute comparison,
especially with a modern multilingual recognizer.

## Target diagnosed segments and compare with dropping them

Zorila et al.'s overlap-conditioned result motivates testing processing only
where its assumed defect exists. Compare retaining, dropping, repairing and
soft-weighting the same identified segments; include random dropping matched
by duration, speaker and language. Audit the text alignment after segmentation.
A lower aggregate WER accompanied by lost coverage on the repaired domain
would not establish rescue of that domain's data.

Encoding repair should precede learned restoration. Recovering available
samples from the source or avoiding destructive requantization has a different
causal explanation from synthesizing missing speech. Separate gain errors,
clipping, codec damage, reverberation, interference and transcription errors
before assigning treatments. This taxonomy is a proposed experimental design,
not evidence that a particular repair will work.

## Treat recognition-aware processing as a larger research branch

The artifact studies support testing mild interpolation with the original
waveform, and enhancement objectives that preserve recognition features.
Their positive evidence concerns inference front ends; transfer to training-only
processing remains unverified. Test frozen and jointly tuned alternatives,
because the located studies favor different choices under different recipes.

An enhanced teacher supervising a raw-input student is another candidate, with
Watanabe et al. 2017 as a discovery lead requiring full-text grounding before
designing the comparison. Such a student could retain deployment conditions
while using a stronger training view. It should compete with ordinary teacher
supervision on the original audio.

## Prior-art search does not establish an empty field

The survey searched explicitly for enhancement in ASR training, retraining,
distortions and observation adding, followed citations from the train/test
anchor, and found direct precedents. Thus augmentation, artifact-aware losses,
matched training, and enhanced-teacher supervision are not proposed as new
ideas. Modern codec/generative restoration and sample-importance selection
need further grounded coverage before claiming a contribution there.

The motivating project's concrete proposal and filtering-granularity controls
live in the draft repository's
`research/speech-recognition/gaps/sketches/audio-enhancement-and-filtering.md`.
The objective is the trained recognizer's utility on held-out audio, separate
from designing a system-ranking ASR evaluation metric.

# Inference-time candidates for a phone recognizer

Grounded inputs: [inference-time section of the survey](survey.md#inference-time-processing-of-the-input-audio),
sixteen read primary sources through 2026-11-21. These are hypotheses; none
has been run for the motivating recognizer. Revisit when a Whisper-class
low-resource test of any of them appears.

## Provisional claims

| Claim | Regime and evidence | Check status | Cheapest discriminating check |
|---|---|---|---|
| A standalone denoiser before a Whisper-class recognizer raises WER | three independent studies, synthetic noise, English-heavy | consistent across groups, not reproduced by us; weak baselines in one | run one enhancer on the target-language dev set, raw vs enhanced vs 0.6-weighted mix, same recognizer |
| Mixing the original back in is the safe form | one study (Wang et al.), LibriSpeech/Aurora-4/VoiceBank, Whisper base and large-v3 | single-source, gains of 0 to 1 point absolute for large-v3 | the same run as above, adds one column |
| A narrowband/wideband flag plus a common sampling rate helps small narrowband data | one hybrid DNN, 600 h narrowband | single-source, pre-pretrained-encoder era | add a bandwidth flag embedding when fine-tuning on mixed 8 kHz/16 kHz data; compare with upsampling alone |
| Whisper-class encoders infer noise condition without side information | linear probe plus class-level correlation (Gong et al.) | no intervention experiment | inject an oracle SNR/bandwidth label into a fine-tuned encoder and see if dev WER moves |
| Voice-activity trimming matters only when long non-speech is present | one Whisper large-v3 padding experiment | built-in failure case | measure hallucination rate on real phone recordings with and without trimming |
| Test-time adaptation could stand in for an enhancer | one wav2vec 2.0 base CTC study | not tested on Whisper-class or on phone compute | adapt layer norm only for 5 to 10 steps on a handful of mismatched utterances; time it |

## Void map for the owner's question (axes: operation by recognizer class)

- Filled with a read result: denoising, observation adding, recognizer-loss
  front end, WPE (one Thai study), VAD (one study), joint training (one
  study), test-time adaptation (one study), mixed bandwidth (hybrid only),
  noise-aware training (hybrid only).
- Untried in located work, not believed impossible: a band-presence or
  per-band reliability side input to a pretrained encoder; bandwidth or
  codec flag conditioning of a self-supervised or Whisper-class model;
  utterance-level environment vector for end-to-end models. Falsification
  search recorded: web queries "noise-aware training", "mixed bandwidth",
  "environment embedding conditioning wav2vec Whisper" returned only hybrid
  or adjacent work (see the survey's coverage section); no forward-citation
  search, so these are not yet capstone candidates.
- Not searched deeply: missing-feature and uncertainty decoding as applied to
  end-to-end models; speaking-rate normalization; codec restoration.

# Carried state, transcript-driven fitting and augmentation (second pass)

Grounded inputs: [survey section](survey.md#carried-state-top-down-fitting-changing-conditions-augmentation),
ten further primary sources through 2026-11-21. Hypotheses, none run.

## Provisional claims

| Claim | Regime and evidence | Status | Cheapest discriminating check |
|---|---|---|---|
| Explicit running session or speaker state beats noise-augmented training alone | no paper compares them head to head; carried state helps on top of augmentation (speaker code 24.4 to 19.4% on simulated far-field, 100M Conformer) | untested as stated; the bet is plausible but unproven | train two small recognizers on identical data: augmentation only vs augmentation plus a learned session code fitted from the first N seconds, evaluated on whole sessions with a channel switch |
| Carried state beats reset-per-utterance adaptation, and needs a shift detector | one CTC wav2vec 2.0 base study, synthetic noise streams | single-source | reproduce on the target language with real phone sessions; measure a naive carry vs reset vs detector |
| Large pretrained encoders infer the condition themselves, so explicit vectors help them less | per-utterance vectors gave wav2vec 2.0 at most 6.3% and none at 9 and 0 dB; Whisper probe | indirect | oracle channel label injected into a fine-tuned encoder (also listed above) |
| First-pass confidence is an unreliable guard for transcript-driven adaptation | SUTA worse than no adaptation on 3 of 8 noises (Whisper-Tiny); confidence selection needs a trained estimator for Conformers | two sources | compare raw confidence, a small trained estimator and multi-hypothesis loss on a held-out noisy set |
| Steady-noise benchmarks hide event-noise and path-switch failures | SRB and BERSt measure steady or static conditions; no event benchmark found | search-limited | build a small test: concatenate clean and event-corrupted segments and a mid-recording codec switch; compare augmentation recipes |
| Mixing band-limited and codec copies into training is safe for clean wideband if the share is moderate | only a hybrid-era mixed-bandwidth study (wideband unchanged) and non-ASR summaries | weak | train with 0, 10, 25, 50% band-limited/codec copies; measure clean wideband and narrowband WER |

## Void map additions

- Untried in located work, not believed impossible: explicit carried
  session state compared head to head with augmentation on a
  pretrained encoder; a benchmark of event noise and mid-recording path
  switches; narrowband/codec augmentation share and clean-wideband cost for
  modern recognizers; a text-to-audio likelihood as a label-quality score.
  Falsification search: web queries on each returned only the adjacent
  items listed in the survey's unretrieved leads; no forward-citation
  search, so none is yet a capstone candidate.
