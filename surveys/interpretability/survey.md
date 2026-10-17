# Interpretability: specific concepts and causal tests

Some billion-parameter language models contain individual neurons with narrow,
causally supported roles. Other useful representations occupy directions or
combinations of neurons. Neither observation establishes that every concept has
one location, or that a readable label exhausts a component's function. The
practical objective is to find an interpretation that predicts responses and
intervention effects across a specified range of inputs, then try to break it.

This survey is for an ML practitioner who understands transformer computation
but has not conducted interpretability experiments. It concentrates on
near-monosemantic concepts in models of at least one billion parameters,
including what prompted reports and output probabilities can reveal without
internal access. Vision and smaller models clarify the alternatives.
Vocabulary is indexed in [GLOSSARY.md](GLOSSARY.md).

**Grounding: source-backed, with incomplete local archival coverage.** Primary
full texts were fetched and their relevant methods, results, and limitations
read; this is not a claim to have audited every appendix or rerun experiments.
The [manifest](related-work/papers.yaml) records 25 checked citations, ten
accepted full-text extracts, and ten concept digests. Foundational
extracts already held in the [LLM-intelligence survey](../llm-intelligence/survey.md)
are linked rather than duplicated. Goodfire's interactive page was read, but
its faithful local conversion failed; its [text edition](https://already-clean.goodfire.com/essay.md)
was also fetched and read. Thirteen further paper conversions are incomplete;
one provisional counterpoint was deliberately read online only. The
[archive gap](gaps/source-archive.md) records these boundaries. Search horizon:
17 October 2026, with bounded coverage rather than
a claim of field completeness. Results below are author-reported unless a
separate comparison is named. Search anchors, databases, and limits are
recorded in [the search record](#reading-route-and-search-record).

## Self-report is useful in trained regimes, without general reliability

The strongest practical evidence supports training models to report learned
behavioral tendencies. [Binder et al.](concepts/trained-self-report.md#behavioral-self-prediction-can-beat-an-external-observer)
show self-prediction advantages over external observers trained on the same
behavior. [Introspection Adapters](concepts/trained-self-report.md#a-shared-adapter-can-elicit-behaviors-it-was-not-explicitly-taught-to-name)
train a shared adapter across related model variants and elicit descriptions
of held-out behaviors. This makes weights or a sufficiently capable adapter
training API a promising access regime. It is not available through ordinary
prompting alone, and the evaluated audit success includes multiple candidate
hypotheses rather than a guarantee that an individual report is true.

Reports of a current hidden state face a different evidential bar. Injection
experiments find some positive cases, while input-only baselines and misleading
textual suggestions expose confounds. A smaller model can also implement a
learned preference in decisions while reporting it poorly. The
[self-report digest](concepts/trained-self-report.md) separates these results
and explains why Li et al.'s feature-description method, despite its relevance,
still requires internal-vector access. There is no generally reliable
self-report interface established by this evidence.

## Logits add detail and sampling efficiency, without locating a concept

Full output probabilities reveal distinctions hidden by the generated token,
including low-probability alternatives and a linear image of the final hidden
representation. They can replace thousands of samples when estimating a rare
token's probability. Output-subspace extraction and language-model inversion
provide concrete demonstrations that the readout contains substantial
information. These results do not identify earlier sites, native neuron axes,
or a unique number of concepts; see [logits-only inference](concepts/logits-only.md).

Three nearby methods make the proposed exploration concrete:

| Method | Observable representation | Access boundary |
|---|---|---|
| QA-Emb | Responses to interpretable yes/no questions | Text answers suffice for the principal method |
| PromptReps, sparse branch | Prompted next-token vocabulary scores | Raw-logit transformation needs adaptation for normalized log-probabilities |
| KCluster | Conditional sequence-likelihood similarities | Must score supplied continuations, directly or through repeated full-distribution queries |

The [prompted-concepts digest](concepts/prompted-concepts.md) covers their
methods, costs, and negative comparisons. Their clusters or axes concern
inputs and behaviors. Calling a cluster “Colorado” does not show that the
model has a single Colorado site. A prompt that asks about Colorado also
changes the computation being inspected. Top-probability truncation, label
wording, prompt templates, and lexical overlap are substantive controls.

## Calibrating concept surfaces on an open model

An open model can supply the missing validation while discovery remains blind
to its internals. Here “surfaces” can mean different lexical expressions of
one distinction, stable context-dependent subdivisions, or separately usable
internal implementations. Measure these separately. The following is a
proposed experiment, not a run, a novelty claim, or a model-selection result.

1. Choose one concept family and contrast set. For Colorado, separate
   geography, government, recreation, literal mentions, and task-relevant
   context. Include matched other-state examples and paraphrases without the
   name. Hold out templates, entities, and context lengths before discovery.
2. Use only outputs to discover candidate subdivisions. Compare hard answers,
   fixed-answer log-odds, prompted vocabulary profiles, and sequence-likelihood
   similarity where available. Include lexical baselines. Count all prompts,
   scored tokens, latency, and training costs; match discovery budgets.
3. Freeze labels, cluster assignments or assignment rules, and predictions.
   Require each proposed subdivision to predict a distinct pattern on held-out
   contexts, beyond prompt wording and token overlap. Report stable distinctions
   at the tested resolution, rather than the model's total number of concepts.
4. Reveal the same model's activations. Compare individual neurons, sparse and
   dense probes, and available SAE features for the frozen distinctions. This
   measures whether output discovery predicts internal separability; selecting
   a probe on the test set would destroy that comparison.
5. Test selective use through controlled donor patching or ablation. A claimed
   subdivision should predict which downstream behaviors change and which
   remain intact. Test redundancy and joint effects before equating a weak
   single-neuron intervention with absence. Compare to equally searched
   controls using the [intervention-validity guidance](concepts/intervention-validity.md).

Add trained self-report as a separate arm if training access is available,
with held-out behaviors and unchanged-base false-positive tests. Re-measure
object-level behavior after training. Useful endpoints include the precision
of output-discovered subdivisions as predictors of selective causal effects,
and improvement per query or unit of compute over hard answers. A failure
could reflect poor reporting, poor clustering, or no separable mechanism;
the internal comparison distinguishes those explanations. Success on one
open model calibrates that model and protocol; it does not transfer a causal
localization claim to an unrelated closed model.

## Goodfire's claim and the examples that motivated this survey

Nick Cammarata's [*Neural Networks Are Already Clean*](https://already-clean.goodfire.com/)
is an informal research essay and working hypothesis. Its proposal is stronger
than automating a search for appealing activation labels: study native neurons
with their inputs, readers, signs, training trajectories, and falsifiable
predictions. It argues that much apparent polysemanticity comes from inadequate
tools, architectures, context, or related generalizations. Its preliminary
Qwen3-32B estimate concerns **neuron poles**, with threshold-dependent meanings
of “one job”; it is not a validated census of concepts or a whole-model causal
explanation. Treat the sweeping conclusion as `single-source`, provisional.

The essay also reports prospective tests: an agent generated positive and
near-miss examples from descriptions of 200 randomly selected gallery neurons
before measuring their responses. Among 183 positive-side descriptions, the
reported strong-response rates were 76% for positives and 11% for near misses;
the displayed figure contains the first twenty. Selected recitation experiments
remove neurons and partly restore behavior through downstream activations.
These support particular predictive and causal claims. They do not establish
that the gallery represents the whole network or exclude undiscovered roles.

The essay spans InceptionV1, modified ConvNeXts, DINOv2, and language models.
The supplied image compares visualization methods on the **same two InceptionV1
neurons**. Its natural-image examples make the shared patterns persuasive;
better-looking optimization results alone cannot establish exclusivity or
downstream function. The “iy” example branches through “diy” to the expanded
phrase **“do it yourself”**, which lacks that contiguous substring. The Colorado
and long-context anecdotes motivate inspecting where context is carried, rather
than labeling only the token at an activation peak.

The strongest justified takeaway is methodological: a failed interpretation
should prompt tests of the measurement and hypothesis. It does not justify
“nobody could interpret because they weren't rigorous.” Earlier work already
performed selective neuron ablations and tested automated explanations;
[Gurnee et al.](https://arxiv.org/html/2305.01610v2) and
[Huang et al.](https://arxiv.org/html/2309.10312) provide concrete examples.
Whether exhaustive native-neuron investigation scales to an adequate account
of large-model behavior remains a separate empirical question.

For the Colorado interpretation, hiking is a weak discriminator: outdoor
recreation, mountains, vacation planning, or the American West could produce
the same response. The more interesting hypothesis is that the activation
maintains geographic context which later computations use. It predicts
responses to non-outdoor Colorado material, rejection of matched Utah hiking
material, and specific effects on downstream geographic judgments. The
[experiment below](#a-first-experiment-that-could-reject-its-own-interpretation)
makes that claim testable. This is a proposed test, not a reproduction of the
blog's example.

Long context is an identifiability issue. If a scalar at a comma depends on a
topic established several paragraphs earlier, displaying only the last few
sentences removes a variable that explains its activity. Restoring the omitted
context may resolve the apparent mixture. It does not follow that every
unexplained neuron has a hidden coherent context, or that punctuation is always
a summary location. Those alternatives need context manipulations and tests of
how subsequent computation reads the activation.

## Double-negative means the two SwiGLU factors are negative

For one SwiGLU MLP coordinate, suppressing biases and the preceding normalization,

\[
g_i=w_{g,i}^{\mathsf T}h,\qquad
v_i=w_{v,i}^{\mathsf T}h,\qquad
a_i=\operatorname{SiLU}(g_i)v_i,
\qquad \operatorname{SiLU}(g)=g\sigma(g).
\]

Its contribution to the residual stream is \(a_iw_{o,i}\). Because the sigmoid
is positive, SiLU has the sign of its input. Thus \(g_i<0\) and \(v_i<0\)
produce \(a_i>0\), just as two positive factors do. For example,
\(\operatorname{SiLU}(-1)(-4)\approx1.08\). This has nothing to do with
grammatical negation, nor does a negative factor automatically mean a semantic
opposite. SiLU's negative branch tends back toward zero for very negative
inputs; it is not a binary closed gate, and a sufficiently large negative value
factor can still matter.

There is directly relevant prior art. Gerstner and Schütze's February 2026
[*GLUScope*](https://arxiv.org/html/2602.23826) explicitly separates all four
sign combinations. In OLMo-7B, its “again” example has intelligible
negative-times-negative activations that a pooled top-positive list would miss.
The September 2026 [*Weakening Neurons*](https://arxiv.org/html/2609.18612v1)
manuscript adds conditional-ablation evidence in OLMo-7B and Llama-3.2-3B.
These predate Goodfire's essay and bound any broad claim that nobody had noticed
the regime. They do not independently verify Goodfire's particular prevalence
or benchmark claims. See [sign regimes](concepts/sign-regimes.md).

The experimental consequence is simple: cache the gate preactivation, the value,
and their product. Analyze the four sign combinations and both output signs
before attaching one label to all positive product values. A scalar output
does not reveal which route produced it.

## The unit of interpretation changes the question

A **neuron** here is an actual hidden MLP coordinate. A **feature** is a proposed
interpretable variable; it may align with a neuron, a direction, a subspace, or
a nonlinear structure. The residual stream has no automatic semantic privilege
for its coordinate axes. An MLP's elementwise nonlinearity gives its hidden
coordinates an architectural distinction, but does not guarantee that each
corresponds to one human concept.

Three arrangements are easy to conflate. A distributed representation spreads
one property across coordinates. Superposition represents more recoverable
feature directions than the ambient dimension, usually exploiting sparse
co-occurrence and tolerating interference. Composition builds a new property
from several earlier properties. A concept requiring several neurons is not by
itself proof of superposition: it may be composed or distributed without the
relevant capacity-overloading claim.

[*Toy Models of Superposition*](https://transformer-circuits.pub/2022/toy_model/index.html)
constructively demonstrates superposition in controlled synthetic networks;
that is a different evidential achievement from measuring its prevalence in
large language models. Clean native neurons and an overcomplete representation
in the residual stream can coexist. Consequently, explaining a formerly
confusing neuron does not by itself refute superposition elsewhere, and a toy
superposition result does not establish that a particular confusing neuron is
an arbitrary mixture. The [existing digest](../llm-intelligence/concepts/superposition.md)
holds the foundational account.

Your intuition about matmul-related parameters splitting a conditional
activation is a useful architectural model. Each coordinate reads a learned
combination of earlier state, applies a nonlinearity or multiplicative gate,
and writes a direction that later computations can use. A conjunction such as
“pointed shape in a roughly face-like arrangement” can be useful to several
object categories. In language, the analogous condition could involve the
current entity, an unresolved syntactic dependency, or a topic relevant to
predicting the next token. These are hypotheses about learned computation,
not obligations imposed by matrix multiplication.

The analogy becomes incomplete if “split” implies an exclusive partition.
Several coordinates can respond to the same input; contributions add and
cancel; residual paths preserve earlier information; and attention moves
information between positions before and after an MLP acts locally. A token's
MLP input is already contextual. “This is a Colorado detector” and “this
contributes Colorado-relevant information at this punctuation position” are
different resolutions of explanation, and the second may be more faithful.

## What different evidence can establish

**Observation and probing** test what can be recovered from activations.
Top-activating examples suggest hypotheses; a held-out classifier tests
decodability. Neither establishes that the original model uses the recovered
property. Top examples also provide little evidence about recall, weak but
important responses, or rare unrelated roles. [Huang et al.](concepts/neuron-explanations.md)
show the practical gap: GPT-4 descriptions of GPT-2 XL neurons can correlate
with activity while failing downstream causal tests. Their negative result
targets that description procedure, not all possible neuron explanations.

**Ablation and restoration** test contribution under a specified manipulation.
Removing a component from an otherwise clean run asks whether the behavior
depends on it in that setting. Restoring a component in a corrupted run asks
whether it can recover the behavior given what the corrupted run retains.
Redundant routes can mask ablation effects; missing prerequisites can mask
restoration effects. Natural donor activations reduce one source of artificial
state, but combining donor and recipient components can still create an
unnatural joint state. [Heimersheim and Nanda](https://arxiv.org/html/2404.15255v1)
provide the most useful short practical introduction.

**Steering** tests whether a chosen manipulation can influence behavior.
Large injected values may recruit a pathway rarely used in ordinary inference.
A topical output change is useful control evidence, but stronger semantic
claims require predictable changes and invariances across contexts.
**Path patching** restricts an intervention to a downstream connection, helping
test how information is used rather than only where it can be restored.
[Zhang and Nanda](https://arxiv.org/html/2309.16042) demonstrate that corruption,
metric, and intervention window materially affect localization results.

**Causal abstraction** proposes a higher-level variable and tests whether
interchanging its implementation produces the higher-level model's predicted
counterfactuals. It is closer to “what computation does this implement?” than
finding an activation correlate. But its force depends on the counterfactual
family and competing abstractions. The
[subspace-patching dispute](concepts/intervention-validity.md) shows why causal
success is not self-interpreting: Makelov et al. exhibit misleading patches,
while Wu et al. dispute their diagnostic and evaluation. The robust lesson is
to demand discriminating tests, not to discard interventions or accept a
universal nullspace criterion.

For empirical semantic-role claims, “causal probing is the only reliable way to
say what something does” captures the need for intervention-backed validation.
Direct architectural or algebraic analysis can also establish limited function,
as the SwiGLU sign calculation does. Interventions need observational and
architectural evidence to specify what they changed and why. The output effect
itself can be established while its semantic explanation remains
underdetermined.

## What has actually worked at billion-parameter scale

**Native context neurons:** [Gurnee et al.](concepts/native-neurons.md) study
Pythia models through 6.9B. A 1B example distinguishes Go-language context, and
ablating selected context neurons changes loss preferentially within their
associated contexts. Their scaling observations include specialization,
splitting, and patterns that persist across sizes. This supports investigating
individual neurons without first training a sparse autoencoder. It does not
establish a globally one-concept-per-neuron organization. Evidence:
`single-source` for these experiments.

**Factual recall and editing:** [ROME and its counterevidence](concepts/localization-and-editing.md)
provide constructive studies in GPT-2 XL, GPT-J, and GPT-NeoX. Restoring
middle-layer MLP computations after subject corruption can recover factual
predictions; selected weight changes can rewrite associations. Hase et al.
find that per-example causal-tracing strength poorly predicts where editing
works. The edit is real, but successful editing does not validate a unique
storage-location claim. Evidence: `contested` for the stronger localization
inference, rather than a failed replication of editing.

**SAE feature discovery:** a sparse autoencoder fits a sparse code whose decoded
vectors reconstruct a layer's activations. Its coordinates are candidate
features, not native neurons. [*Scaling Monosemanticity*](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)
extracts interpretable features from Claude 3 Sonnet, including concepts with
steering effects. The parameter count is undisclosed, so this is production-LM
evidence rather than a verified numeric scale point. Dictionary size changes
which concepts split into narrower features; the authors explicitly acknowledge
incompleteness. Reconstruction and sparsity are useful objectives, not proof
that the resulting dictionary uniquely recovers the model's causal variables.
Evidence: `single-source`; see the [existing SAE digest](../llm-intelligence/concepts/sae.md).

**Circuit tracing:** [Anthropic's 2025 method](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
and [biology study](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
use cross-layer transcoders, sparse models trained to approximate MLP outputs,
to expose pathways in Claude 3.5 Haiku. Selected interventions check proposed
mechanisms. These provide richer explanations than isolated feature labels,
but the replacement model is approximate and the graphs have method-specific
blind spots. Attribution through a simplified graph is not automatically a
verified causal account of every edge in the original model. Evidence:
`single-source` case studies; [existing digest](../llm-intelligence/concepts/attribution-graphs.md).

## Contested results

The central disagreement is partly about the target. Native-neuron analysis
asks what the implemented components do. Dictionary learning searches for a
useful decomposition of their activity. Either can reveal structure the other
misses. Evaluating both solely by whether an LLM can assign attractive labels
would leave the original functional question unanswered.

Goodfire's explanation for apparent mixtures is a live hypothesis, not an
established replacement for the superposition account. A semantic relationship
between two stimuli is weak evidence unless it predicts unseen activations,
training development, or downstream use better than competing explanations.
Conversely, an unsuccessful interpretation is not positive evidence of
arbitrary packing. The [frontier file](frontier.md) keeps these unresolved
claims separate from the field map's methodological lessons.

The disagreement over subspace patching also concerns what counts as a valid
abstraction. Different internal descriptions can agree on a limited set of
counterfactuals. Useful progress can be a broader, more selective predictive
account without establishing a unique semantic ontology.

## Negative and quiet results

[Huang et al.](concepts/neuron-explanations.md) show that observationally
plausible automated neuron descriptions can fail causal evaluations in GPT-2
XL. [Hase et al.](concepts/localization-and-editing.md) separate factual
editability from localization. These are published boundary-setting results;
this survey does not claim a comprehensive inventory of unpublished failures.

[Korznikov et al.](concepts/sae-sanity-checks.md), a February 2026 preprint,
find that constrained-random SAE baselines approach learned SAE scores on
interpretation, probing, and attribute editing. The strongest comparisons
include **partially trained** models and learned intervention masks. The result
does not mean an entirely untrained random model is equivalent to a learned
SAE. It challenges whether the measured successes uniquely certify recovery
of the intended decomposition. Evidence: `single-source`, provisional, in
the paper's tested regimes.

## Baseline sensitivity

[Kantamneni et al.](concepts/sparse-probing.md) compare SAE probing against
strong supervised alternatives on 113 datasets, principally Gemma-2-9B with
Llama-3.1-8B comparisons. Adding SAE probes does not consistently improve mean
held-out performance across their tested regimes. Pooling, feature selection,
and baseline tuning matter. This is evidence about discovering known labels
with probes, not a test of every exploratory or mechanistic use of SAEs.
Evidence: `single-source` multi-task comparison.

For a proposed semantic component, compare raw neurons, a sparse combination,
a dense linear probe or contrastive direction, and a learned SAE feature when
available. Match supervision, selection budget, token pooling, and intervention
strength. Otherwise an apparent representational advantage may come from
better labels or more search. Random-direction controls should match the
intervention's scale and selection process; one unselected random direction
is a weak baseline for a heavily optimized feature.

## A first experiment that could reject its own interpretation

Start with one open model and a narrow claim. Pythia-1B offers continuity with
the native-neuron literature; OLMo-7B offers published sign-aware examples and
[GLUScope's inspection resources](https://sjgerstner.github.io/gluscope/).
For a first investigation, reproducing a documented neuron is a cheaper
scientific starting point than independently discovering one. No model run or
download is part of this survey.

For a fresh Colorado hypothesis, write the intended claim before searching:
“At specified layer/positions, this component carries Colorado context used by
later geographic predictions.” Then:

1. Construct contrasts. Include non-outdoor Colorado contexts; matched
   Utah and other-state contexts; hiking with no Colorado relation; geographic
   near misses; and examples with the same punctuation. Separate quoted or
   denied mentions from the task-relevant location. Use both short prompts and
   documents where the relevant evidence occurs much earlier.
2. Separate discovery from confirmation. Use one set to inspect examples
   and formulate the label. Freeze the interpretation and thresholds before
   evaluating new templates, entities, genres, and context lengths. Record all
   tested candidates so agent search does not hide its selection budget.
3. Measure detection. Inspect the full activation range and false positives
   and negatives. For SwiGLU, record both factors and all sign regimes. Test
   whether changing the earlier location changes activity at the same comma;
   compare nearby non-punctuation positions.
4. Measure use. On matched prompts, test removal and donor activation
   replacement in both directions. Ask questions whose predicted answers depend
   on the location, rather than scoring only topical prose. Keep interventions
   within observed ranges; compare mean replacement, zeroing, random controls,
   and a simple contrastive direction. Natural donors still require controls
   for incompatible recipient context.
5. Measure specificity. Track the intended geographic effect alongside
   unrelated factual accuracy, fluency, and other attributes. Test matched
   recreation questions to distinguish location from outdoors. A change in all
   answers or overall confidence is not the same result as a selective
   geographic effect.
6. Trace the mechanism. Test which upstream evidence produces the state and
   which downstream paths use it. If individual effects are small, examine
   jointly implicated components before concluding irrelevance. If an injected
   value has a large effect, establish whether ordinary runs use that pathway.

A defensible endpoint is a claim such as “this component selectively mediates
these geographic predictions on held-out contexts, with these exceptions.”
“It is the Colorado concept” would require much broader coverage. An agent's
patience makes more hypotheses and tests affordable; confidence still comes
from predictions that survive attempts to falsify them.

## Reading route and search record

For no-internals investigation, start with
[trained self-report](concepts/trained-self-report.md), then
[logits-only inference](concepts/logits-only.md) and
[prompted concept discovery](concepts/prompted-concepts.md). Binder and
Introspection Adapters are the strongest entry points for behavioral reporting;
Li et al. provide the internal-access feature-description comparator.

Read [the patching guide](https://arxiv.org/html/2404.15255v1) first for the
experimental logic, then [native neurons](concepts/native-neurons.md) for a
concrete billion-parameter case, [sign regimes](concepts/sign-regimes.md) for
modern gated MLPs, and [intervention validity](concepts/intervention-validity.md)
for the causal-inference dispute. Read Goodfire alongside these, then the
[SAE](../llm-intelligence/concepts/sae.md) and
[circuit-tracing](../llm-intelligence/concepts/attribution-graphs.md) accounts
as alternative instruments rather than mandatory preprocessing.

Anchors were *Toy Models of Superposition*, *Finding Neurons in a Haystack*,
ROME, *Scaling Monosemanticity*, and the activation-patching methodological
literature. Backward references and explicit rebuttals supplied counterevidence;
targeted 2025–2026 searches covered SAE baselines, native-neuron analysis,
SwiGLU sign regimes, and Goodfire's exact claims. Primary venues include
NeurIPS, ICLR, ACL/BlackboxNLP, arXiv, Transformer Circuits, and Goodfire.

The output-access extension used *Looking Inward*, Lindsey's introspection
study, *Logits of API-Protected LLMs*, *Language Model Inversion*, and QA-Emb as
anchors. Reference following and targeted descendant searches added
Introspection Adapters, Singh's reality check, Atkinson's internal validation,
Li's self-explainers, PromptReps, and KCluster. Searches covered “black-box
concept discovery,” “logits-only representations,” “trained introspection,”
and “conditional likelihood clustering,” including COLM, EMNLP, and EDM.
PromptReps' sparse-only results, top-probability censoring, self-report
hallucinations, and input-only/gaslighting controls bounded the positive
claims. OpenAlex title-resolution and Semantic Scholar citation endpoints
were attempted for the new anchors but unavailable through the retrieval tool;
this extension therefore has no complete database-ranked forward-citation pass.

Forward snowballing was incomplete: Semantic Scholar retrieval failed;
OpenAlex's resolved subspace-illusion record returned zero citers under both
date and citation-count sorts despite the located reply. That is an indexing
limitation, not evidence of no descendants. Citation counts are not reported
where unverified, and saturation was not reached. The map is deliberately
selective: it does not cover all attention algorithms, multimodal models,
training-data attribution, or safety applications.
