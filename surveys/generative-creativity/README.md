# Generative creativity — field interpretation

Status: initial organizing perspective, 2026-09-27. This is our interpretation
and question structure, not a completed literature survey or an effectiveness
claim. The concrete [research sketch](../../research/generative-creativity/proposal.md)
records the proposed interventions and experiments.

## What belongs to this field

We are interested in how generative models produce, select, and develop
worthwhile possibilities beyond their usual preferred responses. Text and
tool-using agents are one setting; images, audio, and other generative outputs
belong too. A panel of meaningfully different realizations of one goal is a
useful unit of study, alongside the quality of each realization.

Our current interpretation separates three questions: what alternatives become
available, what makes the model choose among them, and what lets it develop a
choice without losing its distinguishing qualities. Creativity depends on the
task and the reader/viewer; raw novelty alone does not define the target.

## Axes for organizing understanding

| Axis | Questions to distinguish |
|---|---|
| Intervention site | Prompt and context; sampling; attention and activations; learned control representations; fine-tuning |
| Persistence | One creative decision; one generation; a session; a durable change to weights |
| Function | Generate alternatives; recognize promise; elaborate; revise; select a panel |
| Transfer | Own-model behavior; teacher-generated stimuli; output distillation; selective internal transfer |
| Intervention style | Human-recognizable or classifiable effects across models; strength dependence; shared perceptual dimensions versus model-specific responses |
| Evaluation | Interestingness and meaningful diversity alongside coherence, constraint satisfaction, and cost |

These axes are provisional organization, not a claim that the mechanisms are
independent or that the field has been exhaustively mapped. Human altered-state
accounts motivate questions about altered dynamics. Evocative labels such as
"on coffee" and "on mushrooms" also express the hypothesis that interventions
produce recognizable styles across models, perhaps universal to human
perception or at least easily classifiable. That hypothesis belongs to the
field interpretation independently of whether the styles improve creative
work. Biological equivalence is not part of the interpretation.

## Concrete proposals

- [Generative creativity: intervention and distillation](../../research/generative-creativity/proposal.md)
  covers creative fine-tuning, distilling a teacher's "creative spirit",
  dynamic style tokens/registers, and the first proposed repeated-attention
  intervention.
- [Random-string creativity](../../research/random-string-creativity/proposal.md)
  covers external versus tool-free model-generated inspiration strings,
  generator/interpreter crossings, and useful diversity of resulting artifacts.

## Connections and future field work

The [LLM intelligence map](../llm-intelligence/survey.md) is a neighboring
reference for representations and steering; it does not bound this field to
language models. [Agent prompting and orchestration](../agent-prompting-orchestration/survey.md)
provides a neighboring map of prompt and scaffold interventions.
[Distillation](../distillation/survey.md) currently emphasizes classifiers and
span taggers; generative creative transfer needs its own coverage.

Field interpretation and exploratory field notes live here. Concrete proposals
can cross fields and live under `research/`, with reciprocal links. As grounded
literature work is undertaken, `survey.md` will hold the evidence-backed map,
`concepts/` its read-backed digests, `related-work/` the sources, and
`frontier.md` the provisional research frontier. This entry point does not
pretend those artifacts or a full source review already exist.
