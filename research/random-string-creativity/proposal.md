# Random-string creativity — research proposal

Proposal, 2026-09-21; user-directed preservation of an experiment to perform.
**Experiments unrun and unscheduled.** This records the research questions, not
an effectiveness claim or authorization to launch experiments. The related
`/riff` skill is a usable workflow, separate from experimental validation.
Contributing-model: 6-Astra.

Part of the broader proposed
[generative creativity intervention and distillation inquiry](../generative-creativity/proposal.md).
The [field interpretation](../../surveys/generative-creativity/README.md)
connects this prompt-level experiment with internal interventions, creative
fine-tuning, and teacher-to-student transfer. This document remains the focused
experiment's canonical proposal.

## The interesting question

Does an agent's biased, possibly "creative" randomness make a better stimulus
than externally generated noise? The target is **interestingly distinct,
useful alternatives**, not maximal entropy or difference for its own sake.
The user particularly wants to retain this contrast as a fun experiment.

Motivation: four independent runs of the same prompt asking for something
"varied" can converge on the same preferred interpretation of variety. The
user observes that deployed sampling does not naturally vary responses much;
this is motivation, not an established diagnosis of temperature or provider
settings. Putting all four alternatives into one conversation is a different
condition: later outputs can avoid earlier ones.

An arbitrary string changes the conditioning input while the task stays fixed.
The model then interprets that stimulus into a coherent direction. Candidate
explanations, with no preferred conclusion yet:

- Agent-generated strings may already reflect useful task associations,
  yielding more sensible or interesting inspiration. Those same biases might
  repeatedly select similar directions.
- External noise may break those generation biases. It need not already
  contain meaningful structure: humans and models can find or impose patterns
  in noise. This weakens any assumed coherence advantage for agent generation.
- Model biases enter both generation and interpretation in the first case,
  and interpretation alone in the second. Neither guarantees better outcomes.
- If strings help current strong models more than a good explicit request for
  diversity, that suggests a gap in activating useful exploration on request.
  It does not by itself prove that an entropy source is absent: available
  entropy can fail to become semantic variety.

"True randomness" is the motivating contrast, not a claim about a shell's
implementation. Use an external, model-independent random generator with a
declared alphabet and sampling method; an operating-system random source is
sufficient for this comparison. Record the source without claiming a physical
randomness experiment. "Seed" here means an inspiration string, not the
provider's decoding seed or a guarantee of reproducible output.

## Prompt and primary comparison

The source recipe is the random-string design prompt in
[Anshu Chimala's newsletter post](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world).
Its structure is: request/purpose; generate a long alphanumeric string; derive
a creative direction from subpatterns or associations; execute with judgment;
keep the string out of the design. The published recipe uses a shell script.
Do not assume its examples are representative or its gains transfer to our
current model. Relative model strength has not been established here.

Use the same task and four independent runs per condition:

| Condition | What changes |
|---|---|
| Ordinary request | The creative brief alone |
| Explicit variety | Add a concrete request for an interesting, distinct solution |
| Agent string | Explicit variety plus a model-generated alphanumeric inspiration string |
| External string | Same string procedure, with the string generated externally through a shell |

The agent-string condition explicitly requests generation by the model itself:
**no tools, shell scripts, reading `/dev/random` or `/dev/urandom`, external
random services, or retrieved strings.** Disable tools for the string-generation
call where supported and record the actual tool policy and any violations.
The shell-generated condition is the deliberate external contrast.

Fix the interpretation instruction, requested string length/alphabet, task
constraints, and output scope across the two string arms. Retain actual strings
and lengths; generator noncompliance is an observation, not permission to
silently curate strings. Generate one string per run without selecting the most
inspiring one. Keep the literal string out of the user-facing creative result.
Do not preassign four styles, metaphors, or artistic visions: that replaces the
mechanism under investigation. A specific human artistic vision is a useful
separate comparator, not something this trick is assumed to outperform.

The first comparison tests the practical end-to-end recipes. It does not fully
separate source statistics from the act of generating the string. If useful
signal appears, a follow-up can feed archived agent-generated and external
strings through identical fresh interpreter contexts. Also consider
task-conditioned versus task-blind string generation, and an extra-planning
control without a string, before attributing gains to randomness itself.

## How does context shape model-generated random text?

An additional research question is whether model-generated strings already
exhibit appreciable conditional entropy under a fixed prompt, and whether
explicitly referring to their patterns amplifies their downstream influence.
Keep the prompt and accessible generation settings fixed across repeats; record
unknown deployment settings rather than assuming deterministic decoding or
claiming an estimate of the entire string distribution from a few samples.

Compare no string, a supplied string without an instruction to interpret it,
and the same supplied string with explicit pattern interpretation. Reuse strings
across conditions and include repeated interpretation of one fixed string.
Measure string variation separately from useful semantic diversity in artifacts.
This distinguishes variation already present in the generated stimulus from
the effect of attending to it, against ordinary interpreter sampling variation.
Here "amplify" means making stimulus differences more consequential or useful;
a deterministic mapping cannot create additional Shannon entropy, and an
interpreter may introduce its own sampling entropy. A creative improvement need
not increase raw output entropy.

The user also wants to examine the strings themselves: how does nominally
"random" text, generated without tools, depend on the preceding context?
This can be studied before building or judging any creative artifact.

Hold the model, generation instruction, requested alphabet/length, and available
sampling settings fixed while varying context: neutral/minimal; the actual
creative brief; contrasting topics, styles, or personas; the original default
attempt; and earlier generated strings. Include matched-length unrelated
contexts and paraphrases so context length and particular wording are not
silently equated with semantic content. Repeat within every condition to
compare context effects with ordinary sampling variation. These are proposed
contrasts, not a requirement to run a full factorial experiment immediately.

Retain exact contexts and strings. Inspect character/token frequencies,
repetition, readable fragments, and cross-sample similarity without assuming
which features carry an effect. Test any context classifier on held-out
strings and context paraphrases; finding a cue after looking at all samples is
exploration. Obvious copied words are a different finding from less readable
distributional shifts. An inability to classify context does not establish
that no context information is present.

Then pass saved strings from different generation contexts to fresh interpreters
with the **same** creative brief and no access to the generating context. This
asks whether context-dependent string differences mediate downstream choices.
As a complementary contrast, hold the string fixed and vary interpretation
context. Keep these interventions separate from continuing in the generator's
conversation, where context can directly influence the artifact without being
carried by the string. Cross them with the model/lineage comparison below when
useful; no weights are changed in this context-dependence experiment.

## What does attending to the string mean across models?

A second user-directed question concerns the interpretation step itself: what
does an agent from a particular lab or model generation do when asked to
"attend to patterns in this random string" while designing or writing?
Possible behaviors include noticing readable fragments, repetitions, numeric
associations, or visual rhythms; using model-specific token associations; or
producing a familiar concept and a retrospective story about the string.
These are hypotheses, not direct access to attention or internal computation.

The user's proposed mechanism is an **idiosyncratic, initialization-sensitive,
potentially chaotic mapping**, locally stable over a small number of training
steps in one lineage. The relation between "kinds of random number" an agent
generates and "kinds of pattern seen in true noise" is not presumed to be a
universal or uniquely determined consequence of training on all human corpora.
The conjecture concerns contingent learned associations; it does not assert
that repeated sampling from fixed weights produces identical artifacts.

This makes training-lineage proximity an important experimental axis: exact
checkpoint repeats, nearby checkpoints or lightly fine-tuned descendants,
distant descendants, and independently initialized/trained models. Shared lab
or generation labels are imperfect proxies for shared weights. Where checkpoint
access exists, test whether generator effects and string-to-pattern responses
persist locally and weaken with training distance. Record the update type and
size: a few large or targeted updates need not resemble a few ordinary steps.
Where lineage is opaque, report only the observed model-pair behavior. Local
stability and initialization sensitivity are hypotheses to test, not conclusions
available from a comparison of two vendor endpoints.

Cross the string generator and the interpreting model. For at least two
models, retain these four cells plus external-string controls for each reader:

| String generator | Interpreter 1 | Interpreter 2 |
|---|---|---|
| Model 1 | Model 1 strings → model 1 artifacts | Model 1 strings → model 2 artifacts |
| Model 2 | Model 2 strings → model 1 artifacts | Model 2 strings → model 2 artifacts |
| External generator | External strings → model 1 artifacts | External strings → model 2 artifacts |

Give both interpreters the exact same saved strings from each source, with
source identity hidden and no generator commentary. Even the same-model cell
uses a fresh interpreter context: otherwise private generation context changes
the treatment. Include same-family generations and different labs when budget
allows; tokenizer and harness differences are recorded conditions, not proof
of a weights-only effect.

The user's concrete question is whether model 1 strings interpreted by model 2
make results resemble model 1 interpreting its own strings: does the apparent
"random" signal transfer across weights? The initial user prior was probably
no meaningful transfer across unrelated weights, with local training-lineage
stability a distinct positive hypothesis. The later
[shared-string and structured-use hypothesis](#shared-strings-across-diverged-histories)
keeps cross-model transfer open and asks whether the interpretation workflow
can make it more likely. Neither subliminal-learning results nor the initial
prior settle this different intervention.

Hold the interpreter fixed when estimating the generator effect: compare
model 1 → model 2 with model 2 → model 2 and external → model 2. Then ask
whether any movement is toward independently characterized model 1 outputs.
Simply finding similarity between model 1 → model 1 and model 1 → model 2
cannot isolate transfer from a shared brief, common training conventions, or
ordinary readable fragments in the string. Distinguish stable generator-style
transfer from both readers occasionally finding the same obvious association.
Blind style judgments need held-out reference outputs and calibration; retain
human judgments and avoid inferring transfer from whichever classifier or
feature happens to separate the first samples.

For interpretation probes, compare repeated use of one string, fresh strings,
character-order shuffles preserving counts, and small localized substitutions.
Keep the exact-string arm beside each perturbation. These can test sensitivity
to order, recurring fragments, and whether the stimulus matters beyond ordinary
run variance. Record character and token statistics as diagnostics; matching
character length need not match tokenization across models.

An optional, separately labeled condition can request a short design brief
stating the selected associations before artifact generation. That exposes an
observable intermediate decision and may itself alter the outcome; it is not
faithful internal reasoning by assumption. Compare with direct generation,
and test whether changing an alleged influential fragment changes the artifact
in the predicted direction. Separate the practical benefit of the recipe from
any mechanistic account of why it works.

## Shared strings across diverged histories

User-directed extension, 2026-09-27. Contributing-model: 6-Astra.

The transfer question includes strings generated without tools by one model
and supplied unchanged to different fine-tunes of that model, or to unrelated
models. Can referring to the same string recover a related creative leaning
even after the recipients have followed different histories and made different
earlier choices? Recipient weights stay fixed during this test: string-mediated
transfer is distinct from training on the generator's outputs.

Separate three possible findings:

- A reproducible string effect within one model: different strings induce
  different observable tendencies across repeated runs.
- A shared string effect across recipients: the same string induces related
  tendencies in several fine-tunes or model families.
- Transfer of a generator's creative leaning: its strings move recipients
  toward a tendency independently observed in that generator, beyond the
  shared-string effect of arbitrary external strings.

The third is stronger than the second. Two models might interpret the same
external string similarly without transmitting a generator-specific quality.
Conversely, model-generated strings might carry a useful bias without making
the resulting artifacts converge in every respect.

The user's conjecture is that successful transfer may require the instructed
workflow to tend toward convergence despite diverged histories and earlier
choice points. The minimal operational target is a stable, string-conditioned
leaning in selected observable dimensions. For example, distinct compositions
could both shift toward sparsity or toward recurrent motifs; these examples
illustrate possible measurements, not directions prescribed to the models.
Convergence of complete artifacts or internal trajectories is a stronger claim.

Test the stronger claim by saving deliberately different valid drafts or plans
for the same brief, then branching each into continuations with a common string,
different strings, and no string under otherwise matched instructions. Include
a matched revision instruction without strings. Judge the same style dimensions
before and after continuation: do outputs starting farther apart become closer
under the shared string, beyond ordinary revision effects? A shared directional
shift can leave their distance unchanged; report that as shared steering rather
than contraction. Preserve early commitments where the brief requires them,
and do not count erasing content or genericizing every draft as useful convergence.

Use several histories, strings, and recipient models, and hold out combinations
when testing transfer. For an output-only test, score cross-model string
recognition or similarity with strings and labels removed. The conditional
readouts below deliberately expose selected context. Define dimensions on separate
development material or blinded human groupings; do not choose a feature after
seeing a successful-looking test pair. This deliberately exposed-history arm
is separate from the fresh-context primary comparison below.

### Learn the readout when similarities are hard to name

User expectation: predictable downstream similarities may be identifiable only
after inspecting outputs and still be difficult to judge. Treat discovery of
an informative readout as a research task. Optimize a feature extractor,
classifier, or judging procedure to recover information about the stimulus or
its generating model from the downstream artifact. Human-readable style axes
are one possible result, not a prerequisite for finding a signal.

Here "which model did this" means the full producing configuration: base model,
specific fine-tune/checkpoint (and adapter when applicable), intervention and
its settings, and exact prompt/workflow version. Record that configuration for
both the string generator and the artifact-producing recipient. Their roles
remain distinct even when their base model is the same. Predict factors
individually as well as the joint configuration; interactions may carry a
signature that no factor has by itself.

### Conditional classifiers and explicit input masks

The classifier may consider the prompt, the random strings, the "brain"
intervention, the teacher, and observations of the output, with selected fields
masked. The task prompt, workflow instructions, intervention settings, teacher
identity or reference behavior, and recipient identity are separately recorded
fields. Output observations may be the artifact itself, an excerpt, features,
or an observed production/revision trace. Every main classifier condition sees
some output evidence; it need not see the complete artifact.

Write each prediction task as a target plus an input mask over this bundle.
For example, infer a recipient fine-tune from its output while seeing the task
prompt, stimulus strings, intervention settings, and teacher identity. Or infer
an intervention while seeing the strings and model/fine-tune but masking the
intervention field. Teacher information may include a conditioning teacher
distinct from the string-generating model; record those roles explicitly.

Output-only classification is one baseline. Other conditions can expose prompt
and output, strings and output, or the full bundle except the target and fields
that directly name it. A classifier given candidate strings can test their
relationship to the output instead of recovering their identity from the output
alone. Likewise, a classifier given the intervention can test which fine-tune
responds to it in a particular way.

Compare each contextual condition with a diagnostic that receives the same
unmasked context but no output evidence, using the same held-out split. The
additional predictive value of the output is the relevant signal when context
already predicts some of the target. This diagnostic is an ablation, not the
main output-observing classifier. If the target is a joint configuration, mask
or score its withheld components explicitly rather than counting supplied
components as successful inference.

Retain exact masks and provenance. A condition exposing a workflow's literal
prompt can legitimately recognize that workflow from the prompt; it does not
thereby establish a downstream fingerprint. Balanced configurations, matched
contrasts, and context-only diagnostics separate direct recognition from
information supplied by the output. Masking an identifier alone may leave an
equivalent disclosure elsewhere in the prompt or metadata, so inspect the
actual visible bundle.

### Cheap readouts relative to candidate-model scoring

The user's expensive reference is to supply the full conditioning details and
score the observed output under each candidate model/fine-tune, intervention,
and workflow. Where exact conditional likelihood is available, compare models
on the same observed sequence; generating a fresh sample is not the same test.
This could be a strong attribution reference. Similar candidate distributions,
incomplete context, and opaque tool or provider state can still make attribution
ambiguous, so likelihood is a reference method rather than an identity oracle.
For non-text or tool-mediated outputs, specify the likelihood or replay
approximation actually available instead of assuming an autoregressive score.

The intended research target is a substantially cheaper readout, chiefly for
what it teaches us about the signal. Candidate probes include simple output
statistics, a frozen embedding with a small classifier, a compact trained
encoder, or a bounded judge over selected observations. Avoid making evaluation
depend on rerunning or scoring every candidate generator. Count feature
extraction and judge calls in the inference cost, and report training/data
collection cost separately; a cheap final classification layer alone does not
make the full readout cheap.

On a bounded reference set where scoring is feasible, compare held-out
identification performance, calibration, and cost with candidate-model scoring.
Measure which context fields and output portions a cheap probe needs, which
features survive swaps and intervention changes, and where it confuses nearby
fine-tunes or workflows. A cheaper imperfect probe that reveals stable
structure can be more informative for this inquiry than expensive accurate
attribution with little insight into the distinguishable tendencies. Learned
features remain predictive candidates until controlled changes support a causal
interpretation.

### Prediction targets and validation

Keep the prediction targets distinct:

| Target recovered from the artifact | What a successful held-out test would establish |
|---|---|
| Which string among a known candidate set | The output carries string-specific information across new histories or recipients |
| Measured string properties, such as repetition or token-pattern statistics | Particular stimulus characteristics have a predictable downstream trace |
| Which model/fine-tune, intervention, and prompt/workflow generated the string | Generator-configuration identity leaves a trace mediated through the supplied string |
| Which model/fine-tune, intervention, and prompt/workflow produced the final artifact | Recipient-configuration identity is recoverable; informative about intervention styles and a baseline for string-mediated transfer |
| A creative tendency independently characterized in the generator | A stronger connection between the transmitted trace and a creative leaning |

The user explicitly proposes optimizing this identification task. Candidate
methods include learned representations, supervised classifiers, and a judge
whose feature descriptions or prompt are improved against development labels.
Start with simple surface-feature baselines so an elaborate readout does not
get credit for information already carried by length, formatting, or copied
fragments. Those features can reveal a real channel; report their nature rather
than relabelling them as a subtle creative effect.

For generator attribution, hold the recipient fixed or balance recipients
across all generator classes. Cross generator, recipient, brief, and history
where feasible, with source identity hidden during artifact generation. The
output-only baseline removes literal strings, model names, and condition labels
from classifier inputs; conditional tests follow their declared masks instead.
Compare real labels with shuffled labels using the same training and selection
procedure, and include external strings plus a no-string condition. Control
alphabet, requested length, and generation instructions so these do not encode
generator identity by experimental design. When the target is the generating
prompt/workflow itself, vary it deliberately while matching nuisance features;
do not control away the factor being studied. Balance crossed factors or use
matched contrasts: if one fine-tune always uses one intervention, classification
cannot tell which supplied the signal. Distinguish recognizing known joint
configurations from generalizing a factor's signature to unseen combinations.

Exploratory feature search is allowed; its optimized accuracy is not its test
result. Separate training, feature/prompt selection, and final evaluation.
Group splits by stimulus string and brief when testing generator or property
generalization, keeping every sibling output out of the other splits. For
closed-set string identification, strings necessarily recur: hold out histories,
briefs, or recipients and state that this is recognition of known strings.
Recognition of unseen strings instead needs a matching/retrieval formulation
that receives candidate strings, or prediction of properties defined for new
strings. These answer different questions.

Freeze the learned readout before testing a new intervention, then check whether
the predicted changes survive new strings and recipients. Later experiments
could optimize the string-use workflow for recoverability; assess those on a
separate readout or new human judgments as well, because the workflow can learn
to expose an easy identifying cue without preserving a creative leaning.
Recoverable information supports transmission; similarity or contraction in
that learned feature space is a further claim, and creative value still needs
its own assessment. A failed probe bounds that probe's sensitivity rather than
proving absence of a downstream trace.

## Several strings assigned to aspects, parts, or phases

The user proposes that explicit assignments may make shared steering more
likely: use one string for a particular aspect of the performance, another for
a part of the output, or different strings for production and revision phases.
This reduces ambiguity about where to use a stimulus while leaving the creative
interpretation of that stimulus open. Assigning an aspect is not assigning the
style it should produce.

Three structures deserve separate comparisons:

| Assignment | Illustrative roles | What might become consistent |
|---|---|---|
| Aspects | Composition, voice, motif development | A string's influence on a named dimension across otherwise different artifacts |
| Output parts | Opening, middle, ending; separate visual regions | Local expression of a leaning without forcing the whole artifact into one style |
| Production phases | Exploration, construction, revision | A repeatable change in how a model chooses or develops a direction |

A candidate aspect instruction is: "Use string A as the recurring inspiration
for composition choices and string B for voice. Revisit the assigned string
when making or revising a choice in that aspect. Derive your own associations;
preserve the brief's constraints; keep the strings out of the final artifact."
This is a proposed prompt, not a change to the operational `/riff` workflow.
Test aspect, part, and phase assignments separately before combining them.

Generate and archive the strings once without tools for the model-generated
arm; every recipient receives the exact same set and role assignments without
the generator's explanation. Keep external-string controls. Compare one global
string, several strings with no assigned roles, several with explicit roles,
and the same role/phase instructions without strings. Match total stimulus
length where possible and report actual token counts, since tokenizers differ.
Repeated consultation also needs a matched reminder/revision budget; otherwise
extra planning is entangled with structured string use.

Swap one string while holding all others fixed, then permute role assignments.
If replacing only the voice string changes composition as much as voice, the
control is coupled rather than aspect-local. Compare reusing a string across
production and revision with introducing a new revision string: the former
may restore a leaning after drift, while the latter may deliberately redirect
it. Both are hypotheses. Test repeated consultation against a single exposure,
and preserve outputs before and after each intervention.

For phase comparisons, branch from the same saved intermediate artifact so an
earlier string does not silently change the starting state of the later test.
Separate this controlled comparison from full workflows, where earlier choices
are allowed to affect everything downstream. A shared semantic interpretation
or verbal style description is a useful additional control, but passing it
between models tests explicit semantic guidance rather than transfer by the
strings alone.

Success would be controllable, recognizable creative leanings across histories
or recipients while retaining worthwhile diversity and goal fit. Greater
consistency under one string should coexist with meaningful differences between
strings; convergence to one default style regardless of the string defeats the
proposal. Whether this structure improves unrelated-model transfer more than
nearby-fine-tune transfer remains open.

## Context, budget, and measurement

Freeze the request and necessary prior facts for every independent run. Exclude
the original default attempt and sibling outputs; a subagent inheriting the
whole conversation is not independent in this sense. Each run starts with the
same source material and separate output storage. A conversation rewind alone
does not undo files, edits, or other observable consequences of the first try.

Treat sequential generation and after-the-fact `/riff` with the original
attempt visible as separate follow-ups. Prior exposure could improve results
through useful discoveries or reduce variety through anchoring; do not assume
the sign. Do not mix that effect into the primary string-source comparison.

Start with a bounded pilot across UI concept refinement, storywriting,
roleplay, and technical-document authoring/revision. Use comparable excerpts
or screens rather than four whole books. Freeze task requirements and the
rubric before viewing outcomes. Technical facts and API behavior remain fixed;
roleplay preserves canon, character knowledge, and player agency.

Preserve **every initial output**, failure, and cost. No near-duplicate rerolls,
post-generation diversity repair, or selected screenshot galleries in the
measurement. Present conditions blind and in randomized order, with equal
scope and generation/refinement budgets. Record model, harness, effort,
available sampling settings, effective context, elapsed time, and token/tool
costs; unknown deployment details remain unknown. Interleave conditions to
reduce drift when model versions cannot be pinned.

Human judgment is central: would the user want to choose among these four,
and is there a favorite worth refining? Record useful conceptual distinctness,
individual quality, constraint violations, and favorite preference separately.
For UI, palette swaps alone need not count as different concepts; for prose,
wording changes alone need not count as different explanations or stories.
Lexical distance and an uncalibrated model score are insufficient substitutes.

Four outputs form one comparison set, not evidence of statistical significance.
Repeat across briefs and sets; retain the clustering by brief when estimating
uncertainty. A small pilot establishes feasibility and suggests effects only.
Choose confirmation size, budget, practical effect threshold, and held-out
briefs before making a superiority claim. Keep initial-generation measurement
separate from any later favorite-refinement round.

## Related evidence and limits

[Sakana's String Seed of Thought](https://pub.sakana.ai/ssot/) reports improved
probabilistic instruction following and open-ended diversity using
model-generated strings. It motivates the agent-string arm; it does not
validate this UI recipe or settle agent-generated versus external strings.

[Cloud, Le et al., "Subliminal Learning: Language Models Transmit Behavioral Traits via Hidden Signals in Data"](https://alignment.anthropic.com/2025/subliminal-learning/)
(Anthropic Alignment Science Blog, July 22, 2025;
[paper](https://arxiv.org/abs/2507.14805),
[Truthful AI cross-post](https://truthful.ai/papers/subliminal-learning/))
reports transfer of preferences through apparently unrelated model-generated
number sequences. Its reported dependence on shared or similar base models
motivates the lineage contrast, without establishing our proposed local
stability or one-shot interpretation effects.
[Token-entanglement follow-up work](https://owls.baulab.info/)
also reports preference effects from prompting with selected number tokens.
These motivate taking associations in apparently meaningless strings seriously.
They do not establish that arbitrary strings improve creativity: selected
tokens, teacher-biased datasets, fine-tuning, and one-shot interpretation are
different interventions. This sketch makes no new replication claim.

## Possible user-facing tool

The portable [`/riff [request]` skill](../../skills/riff/SKILL.md) applies the
same template four times, presents alternatives, and refines the user's
favorite after selection. With no argument it recovers the most recent creative
request and its constraints; an explicit argument supplies a new request.
Its initial default is shell-generated strings, preserving the originally
agreed recipe; an explicit request can select tool-free model generation.
This operational choice does not settle the source comparison or imply
validated gains. The research experiments remain unrun and unscheduled.

A YA-specific wrapper could capture a selected original prompt, rewind before
that request, and send `/riff <original request>` so the coordinator also avoids
the default attempt. YA's `topics/session-rewind.md` owns provider support and
the exact cut semantics; verify those when implementing. Preserve attachments
and needed context, not just text with dangling references. File-state
isolation is still necessary. Rewinding and fresh subagents are mechanisms to
evaluate, not capabilities this sketch installs or invokes.

For UI, prefer a verified interactive comparison view with four expandable
concepts, ordinarily 2×2, or inspected captures shown one at a time. Prose can
be presented sequentially in chat. A literal 4×4 means sixteen cells and is not
required for the four-run experiment. Preserve initial candidates before any
selection or refinement; roleplay alternatives remain unchosen branches until
the user selects one. Reuse [UI design guidance](../../topics/ui-design.md) for rendering
and presentation rather than making a new viewer a prerequisite.
