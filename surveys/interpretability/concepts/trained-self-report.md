# Trained self-report can reveal learned tendencies, with bounded reliability

Grounded, selective reading through 17 October 2026. Evidence is
`single-source` for each experiment below; the broader interpretation is
`contested`. Relevant primary methods and results were read, not every
appendix. No experiments were reproduced. Archive status is recorded in
[the manifest](../related-work/papers.yaml) and [gap](../gaps/source-archive.md).

Three questions require different evidence: can a model predict its behavior,
describe a learned tendency, or identify the internal state causing its current
answer? A useful answer to the first two need not establish the third. The
located evidence supports trained, task-specific self-report; it does not
establish a generally reliable introspective interface.

## Behavioral self-prediction can beat an external observer

[Binder et al., *Looking Inward* (ICLR 2025; 2024 preprint)](https://arxiv.org/html/2410.13787)
fine-tune models to predict properties of their own answers to hypothetical
prompts. The key comparison trains another model on the target's behavior,
then tests both on unseen questions. GPT-4, GPT-4o, and Llama-3 experiments
show a self-prediction advantage, including cases where the observer is more
capable overall. Further behavioral fine-tuning can change answers while
preserving useful self-prediction. Complex output properties and broader
out-of-distribution generalization remain failures.

This is the most directly applicable precedent for a text fine-tuning API:
training labels come from observable behavior. It establishes an advantage
under that comparison, rather than arbitrary access to private concepts or
their locations. The paper allows self-simulation as a possible mechanism.

## A shared adapter can elicit behaviors it was not explicitly taught to name

[Shenoy et al., *Introspection Adapters* (2026)](https://arxiv.org/html/2604.16812v2)
train a shared reporting adapter across many behaviorally fine-tuned variants
of a common base. Frozen behavioral adapters are merged into the base; the
reporting adapter learns descriptions through supervised fine-tuning followed
by preference optimization. At inference it is applied to a held-out variant
and asked to describe that model's tendencies. Training spans multiple
behavior families, rather than memorizing reports for one target.

On AuditBench's 56 models with 14 implanted behaviors, the authors report
59% audit success versus 53% for the next-best method and 44% for the best
white-box baseline. An investigator produces ten ranked hypotheses and
succeeds if any is correct; results average sixteen runs per model. This is
not 59% accuracy for a single self-report. Correct reports occur at least once
for 50 of 56 models, another distinct statistic. The authors construct the
training and conduct the evaluation; these numbers have not been independently
reproduced here.

The limitations matter for concept discovery: reports hallucinate tendencies,
especially for an unchanged base; generalization can be weak; and a reward-model
sycophant reports some biases without identifying its underlying reward-score
objective. Training is substantial even if later reports are cheap. Smaller
Qwen models learn the task, and a single-layer rank-one adapter retains part
of the full adapter's performance, but neither observation establishes
reliable reporting in a new small model. The authors explicitly leave strict
privileged-access introspection unresolved.

An API would need to support the relevant shared-adapter training and
application across model variants. Ordinary inference access, or merely a
service that fine-tunes one isolated model, does not automatically provide
that operation. Full weights are sufficient infrastructure, not a prerequisite
of every possible self-report method.

## Learned representations and their verbalization can come apart

[Atkinson, Plunkett, and Bau, *Identifying Introspection From the Inside*
(COLM 2026)](https://arxiv.org/html/2610.07186v1) train random preferences into
models through decisions, without preference-report supervision, then ask
for explicit reports. Some models report the learned preferences faithfully;
others make accurate preference-driven decisions but report them poorly.
Layer-restricted training and internal interventions connect these differences
to whether the learned information reaches the reporting computation.

This is a useful calibration precedent for a smaller open model: failure to
name a distinction is not evidence that its decisions lack that distinction.
Conversely, an accurate report still needs a test connecting it to the
decision mechanism. The experiment concerns a constructed preference task,
not a census of naturally acquired semantic concepts.

## Some self-explanation methods require internal vectors at inference

[Li et al., *Training Language Models to Explain Their Own Computations*
(December 2025 version)](https://arxiv.org/html/2511.08579v2) train explainers
on feature descriptions, activation-patching outcomes, and input-ablation
effects. In their feature task, an internal direction is supplied as a
continuous token at the embedding layer. A target-matched explainer can
outperform a larger external explainer; the target is fixed while the explainer
is trained, so “self” here means a trained copy.

This directly addresses concept descriptions, but its feature method requires
activation access and injection, both for constructing supervision and for
querying an arbitrary feature. LoRA support alone does not supply this
interface. It is an internal-access comparator for the proposed experiment,
not an inference-only solution.

## Current-state reports need controls against prompt inference

[Lindsey's injection experiments](https://transformer-circuits.pub/2025/introspection/index.html)
provide evidence that some Claude models sometimes recognize injected concepts;
the effect is unreliable and context-dependent. The existing
[introspection digest](../../llm-intelligence/concepts/introspection.md)
contains the source reading. The validation itself needs internal intervention.

[Singh, Linzen, and Ravfogel, *Can LLMs Introspect? A Reality Check*
(COLM 2026)](https://arxiv.org/html/2605.26242v2) distinguish privileged access
from monitoring a current internal process. In their open-model experiments,
input-only predictors can match some apparent introspection results, and a
textual suggestion of intervention confounds detection of actual intervention.
These are boundary tests, not a direct replication of inaccessible Claude
internals or a refutation of trained behavioral reporting.

For any proposed reporter, evaluate unseen tendencies, unchanged-base false
positives, misleading textual suggestions, and an observer with the same
behavioral examples. Measure the behavior again after adding reporting
training: a reporter that changes the target has changed what its labels mean.
