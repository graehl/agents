# Generative creativity: context, attention, and learned transfer

**Mode: grounded, selective initial survey. Search cutoff: 2026-09-27.**
This map supports the [generative-creativity proposal](../../research/generative-creativity/proposal.md)
and its [random-string strand](../../research/random-string-creativity/proposal.md).
It selects noteworthy 2025–2026 work plus an older attention-intervention
anchor. Four primary texts have accepted local extracts; two further papers
were read online but failed local extraction. Those two nodes are explicitly
marked below. [Search and extraction record](related-work/search-notes.md).
No experiments were run here; effectiveness grades describe the cited evidence.

The [field interpretation](README.md) supplies the broader scope. This first
slice covers text diversity, hidden trait transfer, and image style alignment.
It does not yet cover audio, creative fine-tuning comprehensively, or establish
that a probe-selected internal signal can transfer a creative disposition.

## In-context learning and weight adaptation

For fixed parameters θ, context C changes the conditional computation
`pθ(y | C, x)`. In-context learning (ICL) describes acquiring or adapting a
task behavior from that context without updating θ. The learned ability to do
this was itself acquired during training. A model may infer a rule, reuse an
example, retrieve facts, or implement an update-like computation in its
activations; no single mechanism is implied by the behavioral term.

Weight adaptation instead constructs θ′ from training evidence, then evaluates
`pθ′(y | x)`. Full fine-tuning, attention-only tuning, and low-rank adapters
differ in which parameters change. Distillation describes the source and
objective of supervision, not which parameter subset must be trained.
The [context-distillation node](../distillation/survey.md#generative-and-context-distillation)
shows how behavior induced through C can become a training target for θ′.

Three meanings of “attention weights” need separation:

| Quantity | Ordinary inference | What adapting it means |
|---|---|---|
| Learned projections, such as WQ, WK, WV, WO | Fixed | Parameter learning, including attention-targeted adapters |
| Input-dependent attention probabilities | Recomputed from queries and keys | Ordinary computation, or explicit inference intervention if overridden |
| Cached keys/values or activation-level memory | Accumulates or changes with context | State adaptation; not by itself a learned-parameter update |

Hierarchical or bookmark markers can organize context and support ICL. The
marker mechanism alone is not sufficient evidence of learning: a fixed routing
rule may only retrieve information. Learning marker embeddings is parameter
adaptation; using those learned markers to infer a new task at inference can
be ICL. Likewise, patching attention during generation is an intervention even
if it teaches the model no new rule. Persistence is a useful diagnostic, not
the definition: caches can persist, and test-time parameter updates can reset.

## Random strings and distribution prompting

**String Seed of Thought (SSoT), Misaki and Akiba, ICLR 2026.**
[Primary full text](https://arxiv.org/html/2510.21150v3), §§3, 5 and Appendix D.6;
read online, local extraction blocked. A model generates a string, then uses
it to make stochastic choices. **Effectiveness: single-source.** Appendix D.6
already compares internal generation with external 24-character seed injection
and random-tool calls on DeepSeek-R1-0528/NoveltyBench. Overall Distinct
(Utility) is 6.19 (5.92), 6.00 (5.76), and 5.72 (5.33), respectively.
Tool-call failures and unequal opportunities to request fresh randomness limit
attribution to the source of randomness alone. This is direct prior art for
the source comparison, not evidence of a teacher's creative disposition
passing through strings.

**Verbalized Sampling (VS), Zhang et al., 2025 preprint, 2026 revision.**
[Primary full text](https://arxiv.org/html/2510.01171v4), §4 and Appendix B;
read online, local extraction blocked. Prompt for candidate responses and
their probabilities. **Effectiveness: single-source.** The authors report
greater diversity in poems, stories, and jokes than direct prompting, comparing
methods at matched total response counts. Larger capable models benefit more;
smaller models can lose quality. This is a useful non-string comparator.
Verbalized probabilities are generated text, not privileged access to the
model's sequence probabilities. Candidate counts also do not equate token cost
or independence: jointly generated candidates see earlier candidates.

Both methods alter inference with fixed parameters. Calling every such change
ICL would obscure whether a new rule was inferred or an existing behavior was
elicited. For the proposal, record the exact prompt and observable state change
rather than treating the category label as a mechanism.

## Randomness supplied as a continuous model input

[Reasoning Palette](concepts/latent-randomness.md), Long et al., December 2025,
supplies sampled continuous prefix embeddings, including a single-slot case.
It is direct prior art for a nontext random input available through attention.
Its learned latent decoder and brief model adaptation are distinct from simply
sampling vocabulary tokens. **Effectiveness: single-source.** The authors
compare latent-conditioned greedy decoding with ordinary greedy and stochastic
decoding on reasoning/grounding tasks.

Control uses prefix length and a training schedule for the fraction of guided
rollouts. This is not a learned, state-dependent gate deciding how much fresh
randomness to consume at each generated step. No exact precedent for that
stronger mechanism was verified in this bounded pass; that is a retrieval
limit, not a novelty claim. SSoT's external-string ablation does not test either
continuous-input architecture. These deserve separate comparator categories.

## Hidden traits through training data versus selected prompt tokens

[Subliminal transfer](concepts/subliminal-transfer.md) is the closest training
precedent. **Effectiveness: single-source.** Cloud et al. transfer animal/tree
preferences and other traits by fine-tuning on filtered teacher outputs.
Their §5.2 in-context substitution fails, including with the whole training
dataset in context. Cross-model transfer is also restricted in their tests.
This directly bounds the inference from “a teacher's numbers carry signal” to
“a fresh recipient will adopt its tendencies from one string.”

[Token entanglement](concepts/token-entanglement.md) supplies a narrower
prompting precedent. **Effectiveness: single-source.** Selected numeric tokens
steer animal preferences in Qwen2.5-7B-Instruct; token-frequency patterns also
provide a cheap readout of the teacher's target. Selection uses model evidence,
unlike arbitrary random strings. The mechanism account remains provisional.

For the proposal's masked classifiers, this suggests token frequencies as a
baseline before learned representations. Predicting a teacher trait in a
number dataset, predicting generator identity from a downstream artifact, and
predicting style from masked internal traces are different targets. A result
on the first is motivation for the other two, not their validation.

## Attention can align style while reducing useful variation

[StyleAligned](concepts/shared-attention-style.md), Hertz et al., 2024, is an
older mechanistic anchor: share a reference image's attention keys and values,
with query/key normalization, during diffusion. **Effectiveness: single-source.**
On the authors' SDXL image-set evaluation it improves style consistency over
unmodified generation, with a text-alignment tradeoff; unrestricted sharing
leaks content and reduces diversity. It changes attention computation without
fine-tuning projection matrices.

This makes style consistency, content retention, and panel variety separable
outcomes for the proposed intervention. It is not a precedent for the exact
decayed repeated-attention controller, nor evidence that a common perturbation
induces a universal style across model families. The proposal's cited coverage
and Attend-and-Excite precedents still need their own full mechanism comparison.

## From transient behavior to a distilled disposition

The [distillation extension](../distillation/survey.md#generative-and-context-distillation)
covers on-policy teacher feedback and 2026 context distillation. A student can
learn from a context-conditioned teacher without seeing that context itself.
However, mode-seeking distillation can favor a smaller set of teacher outputs.
Creative transfer therefore needs a separate held-out diversity/quality test,
even when task accuracy or average teacher agreement improves.

For the masked-internal-trace proposal, existing representation supervision
is a method family to consult, not evidence that style is localized or that
the most predictive probe target is the best distillation target. Compare
output-only training against added trace supervision at matched cost, and
evaluate with a readout independent of the one used to select the trace.

## Contested results

This pass establishes no independent replication dispute. The apparent clash
between failed in-context subliminal transfer and successful numeric prompting
uses different inputs and selection procedures. They can both be true.
Similarly, higher style consistency can coexist with lower content diversity.

## Negative / quiet results

- Subliminal Learning's in-context arm fails in its tested regime.
- The token-entanglement blog reports unsuccessful animal/token cases and
  incomplete suppression under probability filtering.
- StyleAligned's unrestricted attention sharing leaks content.
- SSoT's Appendix D.5 reports a QwQ-32B two-choice failure associated with
  biased string prefixes and inadequate extraction of their randomness.
- VS reports capability-dependent quality degradation. These are author-reported
  boundaries, not independently reproduced failures.

## Baseline sensitivity

The first informative comparison includes ordinary sampling, explicit diversity
instructions, VS, external strings, and model-generated strings. Match candidate
and revision budgets; report token/tool costs separately. For source attribution,
match string alphabet/length and opportunities to use randomness; distinguish
fresh independent outputs from a jointly generated panel. For internal steering,
include zero intervention and matched fixed/shuffled perturbations.

Preserve the proposal's separate judgments of quality, conceptual diversity,
recognizable style, and goal fit. A prompt that changes a classifier's prediction
has not thereby improved an artifact. [Frontier questions](frontier.md) retain
that distinction without asserting an unoccupied research area.
