# Generative creativity — intervention and distillation sketch

Status: proposed research, unrun and unscheduled. This preserves hypotheses
and candidate experiments; it does not authorize runs or claim effectiveness.
Captured: 2026-09-27. User-directed scope and inspirations; experimental
definitions below are proposed elaborations.
Contributing-model: 6-Astra.

Study interventions that make generative models more creative, and ways to
distill a teacher's "creative spirit": its tendencies to notice, associate,
choose, and develop possibilities. The scope includes language models using
text and tools, image and audio generators, and other generative models. The
target is useful, interesting work and panels of meaningfully different ways
to realize a goal, including departures from a model's usual preferred modes.

The [field interpretation](../../surveys/generative-creativity/README.md)
owns the organizing questions and links to neighboring fields. This document
owns concrete proposals, including ones crossing those fields. The existing
[random-string creativity proposal](../random-string-creativity/proposal.md)
is a focused strand and remains authoritative for that experiment.

## Creative decisions within competent problem solving

For an agent, creativity can enter through framing a problem, choosing a
representation, noticing an analogy, arranging a composition, choosing a tool
or exploratory action, selecting among candidates, and deciding what to keep
through revision. Ordinary task competence remains necessary. The question is
whether some of these decision points benefit from a disposition different
from the usual instruction-tuned response.

For example, a visual brief leaves choices about which source detail becomes
the organizing motif; an explanation leaves choices about the analogy that
carries its argument. Several choices can satisfy the brief while making
substantially different artifacts. Test those choices separately from factual
accuracy, tool execution, and preservation of constraints. Local interventions
during exploration can be compared with continuous intervention and with
returning to the base model for selection and execution.

"Creative" is initially a collection of judgments: interesting associations,
conceptual distinctness, coherence, goal fit, and development of a promising
idea. Preserve these dimensions separately. Strange output, lexical diversity,
and a recognizably artistic surface are not sufficient evidence of success.

## Fine-tune a model to become more creative

Begin with ordinary fine-tuning on several worthwhile solutions per brief,
then compare selection mechanisms: final artifacts alone; observable
alternatives and revisions; and preference feedback on candidate sets. The
research question is which supervision changes future choices on new briefs,
rather than reproducing the training collection's surface style.

Include the rejected commonplace candidate when it makes a preference
informative. Distinguish rejection for dullness from rejection for error or
poor goal fit. Training only on each brief's favorite could remove exactly the
alternative approaches that made a panel valuable. Compare that recipe with
retaining several high-quality, conceptually distinct candidates. Neither
recipe is presumed superior before evaluation.

Use held-out briefs, subjects, and task families to distinguish transfer from
memorized motifs. Keep a competence check and an equal-data fine-tuning control
whose examples were not selected for creativity. A useful outcome could be a
controllable creative mode rather than a universal change to default behavior.

## Distill a teacher's "creative spirit"

Start with conventional teacher-to-student compression, but ask what must
transfer for the student to preserve the teacher's creative tendencies. Treat
candidate generation, selection, and development as separable targets:

| Transfer target | Candidate supervision | Discriminating question |
|---|---|---|
| Range of worthwhile alternatives | Several teacher outputs per brief, with their conditions retained | Does the student preserve distinct approaches on new briefs? |
| Choice among alternatives | Teacher rankings or comparisons of a shared candidate pool | Does the student recognize promising ideas it did not generate? |
| Development and revision | Observable drafts, edits, tool actions, and resulting artifacts | Can the student improve an unfamiliar seed without flattening its distinguishing idea? |
| Response to an intervention | Paired base/intervened teacher examples and the intervention settings | Does the student reproduce the change in behavior when the control is varied? |
| Internal dispositions, if accessible | Selected representations or attention behavior, with an explicit alignment | Does transferring that component cause useful behavior beyond output-only distillation? |

An expressed rationale is observable text, not automatically the causal
process behind the teacher's decision. Closed teachers support output and
interaction supervision; internal matching requires actual access and an
architecture-appropriate correspondence.

Use a fixed candidate pool to isolate selection from generation. Give teacher
and student the same external seeds to isolate development. Compare a student
trained on the teacher's ordinary outputs with one trained on its creative
outputs at matched data and training cost. Also compare against the student's
own selected outputs, so extra curation is not mistaken for teacher transfer.
Small/large capacity pairs and same-capacity transfer answer different
questions; compression is one regime, not a prerequisite.

Part-selective distillation could target a small adapter, chosen layers or
heads, or learned control representations. First identify a behavioral effect
and test interventions on candidate components. Do not infer a localized
"creativity module" merely because a feature correlates with artistic output.
The scientific target is a transferable disposition, not a single creativity
score or an assumption that the teacher has one indivisible style.

## Dynamic style tokens and registers

Explore a small set of learned control tokens or internal registers whose
representations change the model's creative choices. Two update timescales
deserve separate experiments:

- Persistent learning: update embeddings, adapters, or a controller across
  training episodes using artifact or preference feedback.
- Within-generation state: update an activation-level register as the model
  notices, explores, or commits to a direction, while weights stay fixed.

A control could modulate revisiting a motif, associative distance, attention
spread, or when to switch from exploration to development. Those are proposed
interpretations to test, not semantic labels guaranteed by a learned vector.
Measure whether interpolating a control produces a usable behavioral change,
whether it transfers across briefs, and whether several settings collapse to
the same familiar style. A distillation experiment could teach the student the
teacher's response to these controls rather than its average response alone.

## Mechanical interventions and altered-state inspirations

User inspiration: some humans describe interesting artistic output under
pharmacological or other brain-influencing interventions, including electrical
stimulation. This motivates exploring altered generative dynamics; it is not
evidence that a particular model intervention reproduces a human state.

"On coffee" and "on mushrooms" have two intended roles. They suggest coarse
mechanisms such as attention gain, persistence versus switching, activation
perturbation, competition between representations, or a time-varying exploration
schedule. They also name a user-expected possibility: interventions may induce
recognizable style families across models, perhaps universal in human
perception, or at least readily classifiable. The latter is a substantive
hypothesis about observable output, not merely a memorable experimental label.

Several mechanisms could converge on a perceived style; the same mechanism
could manifest differently across models. Give each condition a mechanical
definition, then test the relationship between that intervention and the style
people perceive. Keep prompting with the evocative label as a separate
comparator. Agreement between label-prompted and mechanically induced outputs
would itself be interesting; disagreement could reveal where the metaphor
misleads.

Initially manipulate one mechanism and its intensity, including zero. Later
compare combinations and phase schedules if individual effects warrant them.
Candidate questions include whether a temporary perturbation discovers a useful
direction that the unmodified model can then develop, and whether distillation
can retain that benefit without requiring the intervention at deployment.

### Do intervention styles transfer across models?

Build matched output sets for the same briefs under base and intervention
conditions across several models. Initially hide intervention names and model
identities. Ask people to group outputs by perceived style, describe the
differences, and judge whether a grouping persists across models. Only then
test whether evocative names fit those groups. This separates discovering a
shared perceptual structure from agreement induced by being given its label.

Train an intervention/style classifier on some models and briefs, then test on
held-out model families and briefs. Splitting only outputs from the same model
is insufficient for the cross-model hypothesis. Compare classifying the
intervention directly with predicting human-derived style groups: a reliable
mechanical fingerprint and a human-recognizable style are distinct findings.
Match output length, formatting, task, and sampling budgets where appropriate,
and inspect whether simple artifacts explain classifier success. Retain
unmodified examples from every model so model identity cannot stand in for
intervention identity.

Cross-model universality is the stronger conjecture; a stable family of effects
over a stated set of architectures, tasks, and intervention strengths is a
bounded result worth reporting. Cross-modality resemblance is a further test,
not implied by transfer between language models. Dose-dependent movement along
a perceived style dimension may be more informative than a binary label.

Style recognizability and creative value remain separate outcomes. An easily
identified intervention could consistently produce dull or incoherent work.
Conversely, useful creative variation may resist one shared style label. If
stable style families do emerge, distillation can test whether a student
preserves both their recognizable character and their usefulness on new tasks.

## First proposed experiment: bias for or against repeated attention

The user's first intervention to try is a simple bias toward or away from
repeated attention, possibly specific to a source image or prompt. Start with
revisiting positions in a fixed conditioning source. Output-token repetition
penalties, repeated attention to a token, and repeated semantic ideas are
different objects; measure their relationships rather than equating them.

For a selected attention layer/head, let S be a fixed set of source positions
and z[t,j] the ordinary pre-softmax attention logit for source position j.
Maintain c[t,j], a decayed history of prior attention to that position,
initialized to zero. A minimal candidate is:

```text
b[t,j] = beta * (c[t,j] - mean(c[t,S]))
z'[t,j] = z[t,j] + b[t,j]                  for j in S
c[t+1,j] = rho*c[t,j] + (1-rho)*a'[t,j]
```

Here a'[t,S] is the resulting attention distribution conditional on attending
within S; rho is a fixed history-decay coefficient in [0,1), and beta controls
the sign and strength. Positive beta favors revisiting, negative beta
discourages it, and zero is the base control. The current query uses only the
previous history. The centering clarifies relative preference; a constant
offset cancels when normalizing within S. The formula is an agent-proposed
operationalization, not an established creativity mechanism.

For a decoder mixing source and generated tokens in one attention operation,
redistribute the base attention mass within S while preserving its total mass
and leaving other positions unchanged. This separates where the model looks
within the source from how much it attends to the source overall. Preserve
causal/padding masks. For source-only cross-attention, ordinary softmax over
the eligible source positions suffices. Require the zero setting to recover
the base path within a stated numerical tolerance.

For an autoregressive model, t advances with generated queries; keep history
per layer/head rather than mixing their scales. For diffusion cross-attention,
t can instead advance over denoising steps, aggregating over spatial queries
before updating history. Do not make arbitrary spatial iteration order a
hidden recurrent process. A source-image arm requires accessible image patch
keys; text-conditioning attention alone cannot implement that arm. Repeated
visits across denoising time and across generated tokens are distinct regimes.

Fix the source region, layer/head selection, history decay, and intervention
window before the first comparison; vary only the sign and modest intensity.
Prompt-content-only, image-region-only, global, and phase-specific treatments
are later contrasts. A region selected because the same evaluated output
looked interesting is an exploratory selection, not held-out evidence.

### What might happen

Discouraging repeated attention might interrupt fixation on the most salient
cue and expose an overlooked detail. It could also make the model abandon an
important constraint. Encouraging repeats might deepen a motif and sustain
coherent development, or amplify a loop. Test both signs without assigning
either the meaning "more creative" in advance.

The controller is content-blind beyond the model's own attention: it remembers
where attention went, not whether the associated idea is exhausted. A movement
in attention is a manipulation check; useful conceptual movement is the
outcome. Residual pathways and other heads can preserve an association even
when the targeted attention moves.

### Small comparison before training

Use one accessible model and one bounded task family first. Compare the base
model, positive bias, negative bias, and an ordinary sampling/diversity control
at equal output and selection budgets. Fix initial seeds within matched sets
where supported, and repeat across seeds and briefs. Include an equal-scale
fixed or shuffled-position bias to ask whether history matters beyond generic
perturbation. Keep the main sign comparison interpretable before adding arms.

Retain every initial candidate, failure, and setting. Judge panels blind for
conceptual distinctness, coherence, goal fit, interestingness, and whether a
candidate is worth developing. Record individual quality separately from panel
coverage. Inspect attention changes, omitted constraints, repetitive motifs,
and source neglect as diagnostics. A few appealing examples motivate a larger
test; they do not establish superiority.

There are nearby precedents to investigate before a novelty claim. Tu et al.,
[Modeling Coverage for Neural Machine Translation](https://arxiv.org/abs/1601.04811)
(ACL 2016), feed attention history back into attention to address translation
coverage. Chefer et al.,
[Attend-and-Excite](https://yuval-alaluf.github.io/Attend-and-Excite/)
(SIGGRAPH 2023), use attention-based guidance to strengthen neglected prompt
subjects in text-to-image generation. Their targets differ from useful creative
variation. These references were checked at abstract/project-page level for
this sketch; a full prior-art survey and mechanism comparison remain undone.

## Random strings connect prompting, intervention, and transfer

Retain the existing contrast between external model-independent randomness
and strings generated without tools by the model itself or a teacher. An
operating-system generator is not automatically a claim of physical true
randomness; declare the actual source. Cross generator and interpreter rather
than assuming a teacher's strings carry its creative tendencies to a student.

The new connection is to ask whether attention-history interventions change
which features of the same string become consequential, and whether training
can preserve a useful string-to-choice disposition. First establish the string
effect and the attention effect separately. Their interaction and distillation
are follow-ups, with the same saved strings and fresh interpreter contexts.

## Proposed sequence and decision boundaries

1. Define creative decision points and a small set of briefs whose constraints
   leave meaningful room for alternatives; establish the panel rubric.
2. Try the repeated-attention sign comparison with fixed weights, then decide
   whether any useful effect survives matched perturbation and sampling controls.
3. Compare creative fine-tuning with ordinary fine-tuning; separate generation,
   selection, and development in teacher-to-student transfer.
4. Test learned tokens/registers and selective internal transfer only when they
   address a demonstrated limitation or a clearly separate question.

The first experiment is a proposed priority, not a run queued by this document.
Negative results can distinguish ineffective mechanical steering from useful
prompting or learned creative behavior; none of these mechanisms is required
to work for the broader inquiry to remain interesting.
