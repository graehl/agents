# Random-string creativity — research proposal

Proposal, 2026-09-21; user-directed preservation of an experiment to perform.
**Unrun and unscheduled.** This records the idea, not an effectiveness claim,
an installed `/riff` skill, or authorization to launch experiments.
Contributing-model: 6-Astra.

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
"random" signal transfer across weights? **User prior: probably no meaningful
transfer across unrelated weights, with local training-lineage stability a
distinct positive hypothesis.** Keep the possibility open rather than treating
subliminal-learning results as either a guarantee or a disproof of this
different intervention.

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

A future portable `/riff [request]` could apply the same template four times,
then present alternatives and refine the user's favorite. With no argument it
would recover the most recent creative request and its constraints; an explicit
argument supplies a new request. The string-source default remains undecided
pending the contrast above. A usable fun tool need not imply validated gains.

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
