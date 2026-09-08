# Distillation through labels, selection, and structure

**Mode: grounded, bounded first edition. Coverage cutoff: 2026-09-08.**
This map concentrates on learning compact classifiers and span taggers from
stronger teachers: selecting useful examples, distinguishing learnable errors
from noise, and separating data, architecture, and optimization limitations.
Seven primary texts were fetched and their relevant methods and results read.
Four background sources reuse the sibling span-tagging survey. This is not a
comprehensive survey of generative language-model distillation. Search scope,
snowballing, exclusions, and unfinished coverage are in
[search notes](related-work/search-notes.md).

The motivating question is whether inexpensive student diagnostics can predict
which teacher errors will become recoverable after a specific intervention.
That is a stronger experimental target than explaining a score gap afterward.
It does not presume that a small student can cheaply reach its teacher.

## Teacher access determines the available methods

Distillation includes training on a teacher's hard predictions. Access to the
teacher's internal states is not a prerequisite for that form. The distinction
matters when importing recipes that obtain substantially richer supervision.

| Available signal | What can be trained | Additional requirement or limitation |
|---|---|---|
| Emitted spans and types | Ordinary span/tag loss; selective acquisition; reviewed disagreements | Label omissions can become incorrect negative supervision |
| Repeated emitted annotations | Empirical agreement or alternative hypotheses | Repeated errors are correlated; frequencies are not calibrated tag probabilities |
| Teacher probabilities over tags or complete structures | Soft-label or structured distribution matching | Needs a defined, aligned distribution, not JSON-token likelihoods |
| Teacher hidden states or attention | Intermediate feature matching | Requires accessible internals and an alignment across architectures |
| Teacher explanations | Auxiliary textual supervision or separate judgments | Explanations are generated outputs, not hidden states or evidence of causality |

**Current motivating deployment: Luna supplies emitted annotations only.**
Its internal representations and BIOES tag marginals are unavailable. Student
logits and representations remain available for diagnostics. Asking Luna for
confidence does not manufacture the missing distributions. A locally trained
intermediate teacher could expose them, but introduces another model, error
source, and cost; its value would require a separate comparison.

The foundational soft-target and multilingual representation/structure recipes
are mapped in the [existing small-tagger digest][small-tagger]. Their presence
here is background, not a claim that all are runnable against a closed teacher.

## Selecting examples as the student changes

[Dynamic KD](concepts/dynamic-selection.md) ranks examples using the student's
uncertainty and queries the teacher for a subset. This separates **acquisition**
of new labels from **resampling** labels already purchased. Uncertainty needs
no teacher internals; the paper's distillation losses do.

**Effectiveness: single-source.** In Li et al.'s augmented text-classification
setting, uncertainty selection retained most performance while reducing teacher
queries. On the original datasets, random selection was competitive. The
20-fold augmented pool is a consequential condition, not an incidental detail.

[Active curation](concepts/learnable-selection.md) asks a different question:
is an example difficult for the student but easy for a reference model? Its
loss-difference score attempts to avoid spending the budget on examples that
neither can explain. This is related to, but not identical to, disagreement.

**Effectiveness: single-source.** The ACID/ACED work reports benefits against
several tuned distillation objectives in large image-text pretraining, with
27 evaluations. Selection alone loses to ordinary distillation on four of those
evaluations. Its actual score requires reference losses; replacing those with
reviewed label reliability is an untested adaptation for closed teachers.

For span labeling, whole-segment uncertainty can be dominated by length and
abundant outside-entity tokens. Candidate selection should account for those
effects, preserve language/domain coverage and random sampling, and avoid
equating a confidently missed entity with an easy example. Select whole
documents when annotation context and split membership are document-level.

## Training dynamics as diagnostics

[Error Decay on Groups](concepts/error-decay.md) is the closest predecessor
to predicting annotation value: it fits error-versus-support curves on
feature-defined groups and chooses batches for expected improvement. It was
tested on NER, including noisy pseudo-labels and selection transferred between
CNN and BiLSTM-CRF taggers. **Effectiveness: single-source.** It improves over
diversification in several regimes but does not uniformly beat uncertainty
sampling on clean data. Its within-group independence approximation loses
contextual interactions. Thus the general proposal to predict recoverability
already has direct prior art; a new study needs a narrower empirical question.

[Dataset cartography](concepts/training-dynamics.md) uses the mean and variation
of the student's probability assigned to an observed label across training.
It distinguishes consistently easy, variable, and consistently hard examples.
It requires labels and student checkpoints; it does not require teacher states.

**Effectiveness: single-source.** RoBERTa experiments on inference, commonsense,
and question-answering datasets find useful generalization from variable
examples. Very small all-ambiguous subsets can fail to optimize, and some
consistently hard examples are mislabeled. Thus neither maximum loss nor maximum
variability is an unconditional acquisition policy.

For structured prediction, record boundary, type, and missed-span behavior
separately. A sentence-level loss can hide different mechanisms. Repeated
predictions from different training recipes are a useful stability diagnostic,
but are not the same as cartography along one controlled trajectory.

## Learning from an annotation-only language model

[Clinical instructors](concepts/annotation-only-teachers.md) directly studies
an LLM emitting clinical entities, aligned back to text and used to train
encoders. It is closer to a Luna annotation pipeline than hidden-state matching.

**Effectiveness: single-source.** On five-language E3C clinical extraction,
encoder students exceed the teacher in some languages and fall behind in
others. Mixing dictionary and LLM labels helps some conditions. Small evaluation
sets, prompt selection using the reported test set, and ontology-specific span
conventions limit what the scores establish. This is evidence of feasibility
in a narrow task, not a reliable estimate of a multilingual PII gap.

The practical lesson is to separate teacher reliability from student
learnability. An annotation disagreement can be a student error, teacher error,
boundary convention, missing context, or genuine ambiguity. Unioning emitted
spans can improve recall while introducing false positives; agreement alone
cannot certify correctness. Preserve raw hypotheses and make a reviewed,
explicit projection for the student's output space.

## Structure and representation supervision

The sibling survey's [small-tagger digest][small-tagger] covers XtremeDistil,
Structure-Level KD, and encoder-decoder-to-sequence-labeler distillation. Their
shared source extracts are listed in the [manifest](related-work/papers.yaml).
These are **shared-background readings**, not new independent replications.

Token probability matching, a conditional random field's structured marginals,
and intermediate feature matching convey different information. A better
structured loss does not by itself give a flat decoder the ability to emit
overlapping spans. Conversely, a flat head can in principle express flat
contiguous spans without guaranteeing that its encoder learns the required
features. Neither observation proves that an affine head is the current
bottleneck.

A useful controlled contrast fixes training labels, text/context, tokenizer,
encoder initialization, and evaluation, then compares the token head with a
span scorer. A pretrained span-labeling system with a different encoder,
pretraining corpus, or label-description interface answers a broader system
comparison; it cannot isolate the head's causal contribution.

## Capacity and optimization are separate hypotheses

[Teacher assistants](concepts/teacher-assistants.md) insert an intermediate
student between a large teacher and a small student. **Effectiveness:
single-source.** Vision experiments report improvement over direct
soft-target distillation. They do not establish that hard Luna annotations
need an intermediate teacher, nor that replacing them with a weaker teacher
helps. Additional supervision and compute must be charged to that arm.

[Patient, consistent teaching](concepts/patient-consistent.md) demonstrates
that short optimization and inconsistent teacher/student views can mimic a
capacity limit. **Effectiveness: single-source.** Image experiments obtain
substantial improvements with matched views, freshly evaluated soft targets,
and very long training. Those results do not transfer mechanically to replaying
fixed hard spans for more epochs.

The corresponding text question is whether teacher and student receive the
same information. A teacher using neighboring sentences may resolve a label
that an isolated student input cannot. More parameters and more copies of the
same isolated sentence cannot restore missing evidence. This possibility must
be measured; the current Ont3 gap does not quantify its contribution.

## Contested results

No independent replication dispute was established in this bounded pass.
There are meaningful regime differences: larger teachers sometimes hurt
small-student distillation, while carefully optimized function matching can
remove gaps that shorter runs suggest are structural. These are not mutually
exclusive claims. Teacher access, augmentation, student family, and compute
differ. Treating them as a universal verdict about small models would erase
the conditions that explain the disagreement.

## Negative / quiet results

- Dynamic KD's original-data comparison leaves little advantage over random
  selection; the favorable redundant-pool result needs its own matched control.
- EDG's interpretable group curves can sacrifice sampling efficiency compared
  with uncertainty methods when contextual interactions matter on clean data.
- Cartography's very small all-ambiguous subsets can fail to learn. Hardness
  also attracts some labeling errors.
- ACID selection underperforms ordinary distillation on four evaluations;
  aggressive filtering can lose useful coverage.
- In clinical extraction, multilingual mixing and LLM labels do not improve
  every language. The source documents boundary conventions that differ from
  its prompt's generic clinical interpretation.
- Patient teaching's fixed-target arm overfits despite more optimization.
  “Train longer” is not sufficient without its other conditions.

These are reported negative arms, not claims of independent failed replication.

## Baseline sensitivity

Compare active acquisition with a random arm matched for annotation tokens,
language/domain mix, duplicate policy, and student training compute. Separately
compare resampling on an unchanged labeled pool: otherwise better selection
and simply more labels become inseparable. Charge scoring, review, auxiliary
teachers, and hyperparameter search. Preserve the ordinary training stream
while emphasizing a diagnosed weakness; difficult-only training changes the
objective and can destroy coverage.

Before declaring an architecture limit, require a controlled optimization
continuation and checked training fit. Before declaring a data limit, require
a learning curve with additional independent documents. Before declaring a
representation limit, compare heads on the same encoder, then allow controlled
encoder adaptation. Memorizing a tiny set demonstrates fit, not generalization.

## Research questions worth testing

The [frontier note](frontier.md) gives a bounded proposal: use existing outcomes
to discover error-recoverability diagnostics, freeze their predictions, then
test them on an unseen data increment or head intervention. No novel-method or
empty-literature claim is made. A useful outcome could be a validated decision
rule about when to buy labels, supply context, or change the decoder—even if
the final student remains substantially behind the teacher.

[small-tagger]: ../tokenizer-free-span-tagging/concepts/distilled-small-tagger.md
