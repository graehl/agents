# Enhancing audio for ASR training

Grounded, bounded field survey; searched through 2026-11-05. Four primary
papers fetched and read; four citation records verified. Results below are
`single-source` unless stated otherwise; none was independently reproduced
here. The search covers enhancement-induced distortion and train/test matching,
not a comprehensive review of codecs, bandwidth extension or restoration.

## Training benefit depends on what is changed at deployment

There is evidence against replacing arbitrary poor training recordings with
generically enhanced versions. There is also evidence for enhancement within
matched training/inference systems, and narrower evidence for retaining original
training audio alongside enhanced copies. Human intelligibility, perceived
quality and downstream training value are different objectives.

The distinction matters for the question motivating this survey: can processing
poor recordings make them more useful for training a recognizer that will later
receive unprocessed audio? A front end that improves recognition at inference
does not answer that question. Neither does better recognition of the processed
training files by an existing recognizer.

| Approach and grounded node | Training input | Evaluation input | Reported result and boundary |
|---|---|---|---|
| [Matched enhancement](concepts/matched-training-enhancement.md), Zorila et al. 2019 | Raw vs guided source separation | Raw or identically enhanced | CHiME-5 EVAL WER: raw/raw 59.9%; enhanced/raw 73.1%; raw/enhanced 51.6%; enhanced/enhanced 45.7%. Multichannel, annotation-assisted; training hours differ. |
| [Frozen perceptual enhancement](concepts/distortion-independent-training.md), Plantinga et al. 2021 | Noisy or enhanced | Corresponding pipeline | Voicebank test WER: noisy 3.43%; frozen spectral enhancer 3.25%; frozen spectral+phonetic-loss enhancer 2.80%. This is a front-end pipeline comparison. |
| [ASR-aware artifact reduction](concepts/artifact-noise-tradeoff.md), Iwamoto et al. 2023 | Fine-tune recognizer, enhancer, or both | Enhanced | CHiME-4 real EVAL: raw 4.8%; independent enhancement 9.4%; recognizer-only adaptation 8.8%; enhancer adaptation 3.9%; joint 3.8%. |
| [Original plus enhanced augmentation](concepts/artifact-noise-tradeoff.md), Ochiai et al. 2024 | Original, enhanced-only, or both | Raw | Simulated WSJ+CHiME: raw-only 15.9%; enhanced-only 30.5%/23.9%; combined 15.5%/14.9% for two enhancers. Combined training doubles utterances and iterations. |

These are distinct experimental systems, not comparable entries on one
leaderboard. The last row is the closest direct evidence for training-only
processing, but it does not isolate the effect from additional training.

## Artifacts can cost more than residual noise

The [artifact studies](concepts/artifact-noise-tradeoff.md) decompose enhancement
error into components attributable to reference speech/noise and a remainder
outside their span. In their tested systems, suppressing that remainder matters
more for recognition than suppressing additional residual noise. Mixing some
original observation back into enhanced audio can therefore improve recognition
even while worsening signal-to-noise measures. Reference signals are needed for
the decomposition; it is not directly a no-reference filter for arbitrary web
recordings.

The practical alternatives are to preserve original examples, tune enhancement
against recognition, or condition processing on the defect. Zorila et al.'s
low-overlap analysis illustrates the last option: a separation mask that helps
an overlap-heavy corpus can damage speech with little overlap. A single
recording-level quality score would hide this difference.

## Contested results

The located papers do not establish a direct failed replication. Their apparent
disagreement over whether enhancement helps largely changes the recognizer,
processing objective, training exposure and inference condition. Plantinga et
al. favor a frozen enhancer in their setup; Iwamoto et al. obtain their best
results by adapting enhancement with ASR loss. Neither establishes a universal
choice between frozen and joint training.

Enhancement built for human listeners need not rescue training data, which is
consistent with these distinctions. An absolute claim
that processing cannot help ASR training would exceed the evidence, particularly
the matched-system and combined-training results.

## Negative / quiet results

Wholesale enhanced-only training substantially worsens raw-test recognition in
both the CHiME-5 and simulated WSJ+CHiME comparisons. Adapting only the recognizer
does not repair the independently trained enhancer's damage in Iwamoto et al.
Plantinga et al.'s spectral enhancer also worsens test WER when attached to a
recognizer trained on noisy inputs: 3.58% versus 3.43% without enhancement.
These are reported negative conditions within successful papers; this search
does not establish that any technique was abandoned by the field.

## Baseline sensitivity

Before attributing a training improvement to enhancement, compare against
repeating the original audio for the same number of updates. Preserve speaker,
language and acoustic-domain composition when comparing dropping with repair.
Evaluate on unprocessed, held-out deployment audio; a matched-enhancement test
set answers a different question. Keep corruption repair separate: preventing
quantization loss or decoding an existing signal correctly does not require a
learned enhancer to reconstruct information.

Perceptual scores may nominate suspicious segments, but evidence here does not
justify using them as training-utility targets. The adjacent filtering evidence
is maintained in the draft repository's ASR filtering survey,
`research/speech-recognition/surveys/asr-data-filtering/survey.md`.
Candidate tests are in [frontier.md](frontier.md); the project-specific proposal
is the draft repository's
`research/speech-recognition/gaps/sketches/audio-enhancement-and-filtering.md`.

## Retrieval and coverage

Search anchors were Zorila's explicit train/test experiment, Plantinga's
perceptual-loss comparison, and Iwamoto/Ochiai's artifact analyses. Queries
included `speech enhancement training data automatic speech recognition
retraining distortion` and `ASR enhanced training data noise reduction
observations adding enhanced speech training`, followed by exact-title primary
retrieval and reference inspection. A Semantic Scholar citation query for
arXiv:1909.12208 returned 38 citers; OpenAlex returned HTTP 429. The newest
grounded anchor is the 2024 distortion study, despite the 2026 search date.

Unresolved leads include Watanabe et al.'s *Student-Teacher Network Learning with
Enhanced Features* (ICASSP 2017), and *Audio Enhancement for Computer Audition—An
Iterative Training Paradigm Using Sample Importance* (2024). Neither contributes
a quantitative claim here. Enhancement-assisted supervision of a raw-audio
student merits a full-text follow-up. Codec restoration, clipping repair,
bandwidth extension, modern generative enhancement and large multilingual
training remain coverage gaps; no novelty or literature-saturation claim is
made for the proposed experiments.

Verified bibliography and reconstructible source provenance:
[papers.yaml](related-work/papers.yaml). Each concept page links the primary
full text and the retained extract.
