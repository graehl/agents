# Establishing a data and ML research program

> Upfront decisions for data, representations, models, evaluation and reproducibility, with composable text, audio and image guidance.

Topic: `research-program-setup`
Glossary: omit

Use this topic when establishing a data or ML research program, or materially
revising its data, representation or evaluation contracts. Define the applicable
categories upfront, even as explicit placeholders. A small program can use
sections of one existing topic; link established owners instead of creating a
parallel checklist. Keep the descriptive charter concise under
[TOPICS](../TOPICS.md#program-scope-charters).

The categories below are suggestions for program design. Record which defaults
the program adopts; they do not silently migrate existing corpora, checkpoints
or scoring protocols. An unresolved choice is acceptable until work depends on
it: name the decision needed before that boundary. Do not invent binding
`Program instructions` while merely inferring a charter.

## Common decisions

| Category | Define upfront |
|---|---|
| Purpose and scope | Intended use, research question, target populations and domains, exclusions, and what outcome would change the next decision. |
| Unit and modalities | Example and source-group identity; text, audio, images, or any combination; inputs, supervision and outputs may use different modalities. |
| Data and rights | Sources, versions, permitted uses, access/privacy constraints, sampling, coverage, labels and annotation quality. |
| Representations | Raw preservation, model inputs/targets, preprocessing and normalization, coordinate systems, and versioned derived views. |
| Splits and exposure | Train/development/test roles, grouping and deduplication, selection history, synthetic-data ancestry and contamination checks. |
| Models and training | Initial model/tokenizer/processor, baseline, objective, adaptation scope, replay or capability preservation, resource budget. |
| Evaluation | Task metrics, meaningful improvement, preservation checks, error slices, uncertainty unit, and promotion criteria. |
| Execution and artifacts | Canonical implementation, manifests, hashes, run/checkpoint lineage, reproducibility and deployment constraints. |

For each applicable category, record a choice or `unresolved`, its current
reason/evidence, and the next check when needed. `Not applicable` is useful for
an absent modality; absence is different from an unexamined choice. Choose any
one, two or all three modality sections below. An audio-only program needs no
invented transcript pipeline; a multimodal program uses the selected sections
plus their joint alignment contract.

Keep immutable source material or a recoverable source identity separate from
derived training and scoring views. Record ancestry from original object to
segments, augmentations, annotations and final examples. Split at the group
that can leak task-relevant information—document, recording, speaker, session,
scene, patient or source collection as appropriate—before treating segments as
independent examples. See [training data](training-data.md) for acquisition and
partitioning, and [research artifacts](../_RESEARCH/artifacts.md#program-guidance-and-process-records)
for process maps, inventories and exposure history.

## Text: normalization is a representation decision

Whenever human text enters a model, labels, retrieved context or evaluation,
specify its Unicode form and task-specific transformations. Suggested default:
**NFC** at declared derived-text boundaries, with the original strings retained.
NFC unifies canonically equivalent sequences without the additional
compatibility folding of NFKC. It is not a lowercasing or case-folding policy.
NFKC can map compatibility characters to differently cased ordinary letters
(for example modifier capital A to A), as well as collapsing width and
typographic distinctions. Treat those transformations as explicit choices.

Decomposed forms are valid when a tokenizer or task deliberately exploits
their units; otherwise NFC is a useful conventional default. Unicode form is
only one layer. Decide casing, punctuation, whitespace, script-specific marks,
digits and number words, symbols, markup, control characters and unknown-text
handling separately. Preserve distinctions needed by the task: identifiers,
PII span boundaries, equations and case-sensitive labels need different
treatment from a case-insensitive speech score.

Distinguish four contracts:

- Source text and annotations: exact bytes/code points, offsets and provenance.
- Model input and target text: transformations used before tokenization and
  the required output presentation.
- Tokenizer behavior: its own normalization, vocabulary, unknowns and
  byte/subword handling, including transformations hidden inside a processor.
- Evaluation views: what equivalences the scorer deliberately accepts.

Check the final transformed string for the promised Unicode form: character
deletion, case conversion or concatenation can undo an earlier NFC pass.
Never normalize an offset-bearing string without preserving or recomputing
its alignment. Keep raw hashes distinct from derived hashes. An existing
checkpoint's preprocessing is part of its interface; introduce a named new
policy and explicit migration rather than changing an old policy in place.

For MT, also define language direction, scripts, domain, code-switching,
translation versus transliteration, sentence/document boundaries, parallel
alignment and source/target presentation. Keep these choices independent on
the two sides where their languages require it. For annotation or redaction,
define span units and alignment through every transformation.

Normalization research needs both equivalence scoring and preservation
evidence. Normalize both references and hypotheses for a promoted scoring
protocol. To diagnose presentation improvement separately, choose references
already in the desired style independently of candidate outputs, freeze them,
and compare the same hypotheses with and without normalization. Report slice
membership, error counts and changed examples. Even fixed references do not
make a destructive mapping safe: replacing everything with one token can beat
an insertion-heavy WER above 100%. Check retained content, whole values and
controls, not just the scalar score. A style-selected slice is not a
representative estimate of overall recognition or translation quality.

## Audio: preserve the signal the task needs

Specify decoded waveform dtype/range, sample rate, channel count and layout,
timebase, codec/container and decoding version. Distinguish source properties
from the model's required input. Retain the source and derive model-specific
resampling or channel mixing; do not adopt 16 kHz mono merely because an ASR
model uses it. Re-encoding already compressed audio can add loss without
recovering information.

Decide amplitude/loudness normalization, clipping checks, silence treatment,
segmentation, overlap, padding and duration limits. Record timing changes and
map segment times back to source samples. Resampling, trimming and time stretch
must also transform aligned labels. Define whether gain, noise, reverberation,
pitch shift or speed changes preserve the target before using them as
augmentation. Speaker/session/source grouping may matter more than random
clip separation.

Speech transcription adds transcript style, disfluencies, speaker turns,
timestamps, language/script labels and the text contract above. Audio-only
tasks can instead concern events, speakers, separation, acoustics or music.
Music may require pitch, rhythm, long-range structure and stereo information
that a speech preprocessing recipe discards. Select quality metrics and
listening checks for the actual output; transcript WER cannot judge a
text-free audio system. For generation, include audible artifacts, conditioning
fidelity and latency/duration behavior in the evaluation plan.

## Images: starting representation questions

These are initial engineering suggestions, not conclusions from local image
experiments. Validate them against the selected model and task before adopting
a recipe.

Specify decoding and orientation, color space/profile, channel order,
bit depth, alpha handling, pixel range and normalization statistics. Preserve
the source and record the transformation to model input. Decide resolution,
aspect-ratio policy, resize interpolation, crops/tiles and padding based on
the information the task needs; no universal square crop or resolution is
suggested here. Small text, fine boundaries and global layout may impose
different requirements.

Define the coordinate system for boxes, keypoints and masks, including whether
coordinates refer to source or transformed pixels. Apply corresponding spatial
transforms to labels; use label-appropriate interpolation for masks. Check
whether rotation, mirroring or color changes alter meaning before assuming
augmentation invariance. Group crops, frames and alternate encodings of the
same source across splits. For image generation or reconstruction, define
perceptual/content checks alongside numerical metrics and preserve the
rendering conditions used for visual review.

## Combining modalities

A paired example needs an explicit relation, not just neighboring filenames.
Record source identity, which objects correspond, alignment precision, and
missing/corrupt-modality behavior. Audio/video uses sample and frame timebases;
image/text tasks may need region-to-span mappings; spoken text needs
word/segment timing only if the task requires it. Preserve the mapping through
cropping, resampling, segmentation and text normalization.

Define which modalities are available at training and deployment, whether
supervision introduces a modality absent at inference, and what happens when
one is unavailable. Split all derived views of a shared source together where
their content could leak. Compare useful single-modality baselines with the
combined system and test missing or mismatched inputs when relevant: a model
can appear multimodal while solving the benchmark from one modality's shortcut.
Video adds temporal sampling and frame order to the image/audio decisions;
it does not make either representation contract disappear.

## Models, evaluation and promotion

Start with a reproducible baseline and a cheap real-path smoke that checks
data, labels, processors and outputs together. Recover existing implementation
and evidence through [shared ML model development](ml-model-development.md);
transfer mechanisms deliberately rather than copying task-specific constants.
Record initialization, tokenizer/processor versions, objective, trainable
parameters, replay and expected capability retention. Budget training and
inference separately, including preprocessing, storage and latency constraints.

Define what a meaningful gain would buy: fewer consequential errors at matched
cost, improved quality at a deployable latency, or equal quality with lower
resource use. Keep paired outputs and denominators, inspect regressions and
relevant populations, and estimate uncertainty at the independent source-group
level when appropriate. Separate selecting on development data from claims on
unexposed evaluation data. Repeatedly inspected challenge cases are useful
regressions, but cease to be fresh evidence.

Before promotion, check the whole adopted pipeline, including normalization
and scoring, against its predecessor and preservation controls. Version the
changed contract and identify descendants requiring regeneration or rescoring.
Do not compare scores from different reference views as if only the model
changed. Follow [research evidence](../_RESEARCH/evidence.md) for comparisons
and [RUNS](../RUNS.md) for execution and artifact provenance; this topic adds
setup questions rather than replacing those owners.
