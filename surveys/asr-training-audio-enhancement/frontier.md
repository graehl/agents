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
