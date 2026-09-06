# Agent-instructions sketches

> Dormant candidate designs for the instruction corpus and its evidence
> pipeline; none is current guidance until promoted into the owning doc.

Topic: `agent-instructions`

## Tool-surprise telemetry: mine session logs for retry-then-success

"Tool surprise" (user's working term, 2026-08-17): an agent misinvokes a
tool or misreads its output contract — expects JSON and gets text, or the
converse — then adapts by retrying. Each episode costs tokens, and with no
cross-session memory the same confusion recurs. The candidate noticing
system is token-free: mine harness session logs for the retry-then-success
signature — one or more failing invocations of a tool followed shortly by a
similar succeeding one — and rank recurring (tool, failure-shape) patterns
across sessions as error-analysis candidates.

Signal grammar, per session: group shell tool calls by normalized leading
tool token. An episode is fail(s) then a similar success (same tool,
overlapping arguments). Two variants are worth keeping: repeated failures
with no similar success (abandonment — the strongest candidate, since the
agent never recovered), and failure on tool A followed by success with tool
B serving the same evident intent (tool abandoned as unusable).

Capture options, in preference order:

- **Scrape logs post hoc (preferred).** Claude transcripts already record
  the full command of every Bash call, and a failed call's result carries
  `is_error` plus a literal `Exit code N` first line
  <!-- verified: transcript sampling 2026-08-17 -->. Zero runtime cost,
  retroactive over all recorded history, no per-command risk.
  `queued-anchor` already demonstrates transcript parsing; per-harness log
  locations and formats stay owned by the harness supplements.
- **Harness hook.** Live and exact, but per-harness configuration, one more
  failure surface on every call, and it adds nothing on a harness whose
  logs already carry exit codes.
- **Mandated per-command wrapper: rejected.** It perturbs quoting on every
  command and destroys exit attribution — the failure recorded in
  `agent-instructions.evidence.md` § "native agentctl watch timeout
  preserves exit provenance", where a wrapper/pipeline form forced
  reconstructing which exit belonged to payload, wrapper, and tail. The
  wrapper would corrupt the very signal it exists to collect.

The crux is false-positive design, which is why this stays a sketch: a
nonzero exit is often information, not failure — `rg` no-match is 1,
`agentctl others` nonzero means peers present, `at-queue claim` exit 3
means nothing due (all observable in this project's own transcripts) — and
permission denials, user interruptions, and deliberate probes are not
incompetence. Single incidents are noise; the unit of signal is a
normalized pattern recurring across sessions. The miner therefore needs a
per-tool information-bearing-exit allowlist, a denial/interruption filter,
and ranking by frequency times estimated retry token cost, reporting each
candidate with example fail/success pairs.

Consumption: a ranked error-analysis candidate list — tool, failing form,
succeeding form, count, sessions, and harness/model breakdown (the model id
is on every transcript line, so harness- or model-specific trouble
separates from "this tool is hard to use"). Remediation menu per
candidate: give the tool a defaulted option or single-script treatment; add
a harness- or model-scoped instruction line; or explicitly no action — a
retry costs a few hundred tokens once, a boot-loaded rule costs tokens
every session, and the frequency data is exactly what prices that trade.

Delivery: a slash-only skill (provisional name `trawl-tool-surprises`) that
takes the requested project, sweeps all known harness session logs for that
project's sessions, runs the miner, and emits the report. Claude-only
first, since that format is verified; other harnesses join as their
supplements document log formats. Epistemically this sits between the
trace-simulation pass and the deferred instruction ablation
(`agent-instructions.md` § Limits of these methods): observational outcome
data, far cheaper than ablation, weaker than a controlled comparison.

Promotion path: before writing the skill, run the miner once as a one-off
script over this project's Claude logs to size the signal; build the skill
only if the top candidates are non-empty and plausibly actionable. The
sketch below consumes this output as its promotion evidence.

## Conditional tolerance for defensive parsing in throwaway orchestration

`AGENTS.global.md` § Anti-slop implementation bans permissive fallbacks
added "merely to make the current trace pass". In throwaway orchestration
scripting, an agent that guessed a tool's output format and observed a
mismatch faces a real fork: resolve the invocation properly (find the
format option) or handle both forms defensively. A blanket ban over-forbids
the second; unconditional tolerance breeds slop. This sketch drafts the
conditions under which both-forms handling is not "merely" that.

Candidate rule text (draft, not binding):

> In throwaway orchestration, handling multiple tool-output forms is
> acceptable when every handled form was actually observed (no speculative
> branches), no form loses or ambiguates the needed information, a misparse
> cannot pass silently (empty or degenerate results fail loudly), and the
> unexpected branch logs that it fired. Spend one bounded probe for a
> format option before writing the branch. When the same tool surprises
> twice, or the code lands in `scripts/` or another reused surface, resolve
> the invocation properly and record the finding (helper option, topic row,
> or `gaps/` entry).

Rationale, compressed from the 2026-08-17 discussion:

- Observed-only kills the worst habit: untested branches codifying a
  hallucinated tool model. Most expect-JSON-get-text bugs come from writing
  the parser before running the tool once.
- Misparses usually yield empty-but-plausible results (`jq` over text →
  zero findings) that pass end-result checks vacuously; hence the
  fail-on-degenerate condition rather than trusting "meaningful tests".
- A silent either/or handler destroys the signal that the tool model is
  wrong; the one-line log converts tolerance into instrumentation.
- "Near-throwaway" is self-serving at decision time; where the code lives
  is checkable.
- Environmental causes — TTY-vs-pipe output switching, version drift — mean
  the tested branch may not be the one that fires later; there the explicit
  format flag is strictly better than any defensive parse.
- The cost knob is amortization over the tool, not rigor per script: chase
  rarely (one bounded probe), capture cheaply (a `gaps/` or topic line),
  resolve on repeat (a second surprise proves recurrence, so the amortized
  fix pays; central tools reach "second" fast, one-off tools never do).

Promotion criterion (pre-registered): this is boot-priced text for a
failure mode whose frequency is currently anecdotal. Promote only if the
telemetry sketch above shows format-confusion and retry episodes at a
frequency times cost exceeding the rule's per-session token price, and
expect the rule's effect to appear as a decline in those episodes.
Placement when promoted: a compact addition adjacent to § Anti-slop
implementation.

Trace-simulation risks any promotion must survive
(`agent-instructions.md` § Verifying instruction changes): over-application
("observed both forms" cited to accumulate branch debt in durable
scripts); probe inflation (the bounded probe becoming a research detour);
log noise (the fired-branch line polluting quiet pipelines).

## Astra and shared instruction reductions

Proposal, 2026-09-06; behavioral reductions below are not active guidance.
The user describes Astra as "sol but fewer mistakes, nothing fundamentally
different" and wants fewer tokens spent supplying judgment it already has.
The intended editing/thinking population is Astra and the Opus/Sol/Fable/
Grok-4.6 tier, not smaller models used for bounded data processing. This is
user experience and workload selection, not a measured capability ordering.

The first decision is a shared competent-agent baseline plus small named
exceptions. `AGENTS.sol.md` already existed. `AGENTS.astra.md` now has its own
route, with no active patches; do not copy Sol's exceptions into it merely
because Astra is a successor. An empty behavioral delta is an honest starting
point. Adding a supplement does not itself reduce the shared prompt.

### What the inspection establishes

At source revision `657dca3d4a82e193c1cd55bfdc2b01e393b36b13`, the five
shared files this Astra/YA/Codex launch selects have these sizes:

| Source | Bytes |
|---|---:|
| `AGENTS.global.md` | 47,201 |
| `AGENTS.user.md` | 12,896 |
| `AGENTS.codex.md` | 7,571 |
| `AGENTS.frontier.md` | 2,735 |
| `AGENTS.ya.md` | 4,836 |
| Total before project instructions and action-triggered reads | 75,239 |

These are file bytes, not tokenizer counts, effective injected context, billed
tokens, or latency measurements. The five listed files constitute that shared
selection; the new Astra supplement adds a small route-specific file. Runtime
cost also includes rereads, generated reasoning, retries, tool calls, and human
correction. Moving prose to a packet every task must read saves no first-read
volume; a useful extraction makes that read conditional.

No outcome ablation has been run on this corpus. Historical ledgers contain
observed failures and some retry counts, which establish failure occurrence,
not the benefit of the resulting instructions. This Astra review itself hit
tool-output truncation through over-batching and undersized result budgets,
then recovered the omitted reads. That supports retaining the concrete
Codex output-budget fact, not attributing the error exclusively to Sol or
adding another universal verification ritual.

OpenAI's current [Astra guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)
describes increased instruction sensitivity and recommends auditing loaded
guidance. That is vendor advice, not evidence for any cut below. Our inference:
overbroad instructions may become more costly when followed more faithfully.

### Recommended first pass: shared reductions by judgment

Each row is a proposed change to its named owner. Preserve repository-specific
facts, user choices, authorization, and work-preservation contracts. Put
incident stories in the existing ledger rather than boot text. No numerical
performance improvement is claimed.

| Priority and owner | Proposed change | Boundary to preserve |
|---|---|---|
| First: `agent-instructions.md`, Verifying instruction changes | Replace the assumption that non-frontier agents perform real editing with the user's actual target population. Keep an example only if it resolves a plausible ambiguity for those models; weaker-model reminders belong in their supplement. | Capability does not make local facts inferable or erase observed frontier failures. |
| First: `AGENTS.codex.md`, Session Identity | Retain the real-id invariant, normal `agentctl` resolution, and one explicit failure route. Move the long invented-id story and rare discovery recipe to the session-mechanics owner. | A missing id triggers recovery, never invention; a present launcher id is already the answer. |
| First: `AGENTS.global.md`, Project-level instructions; `TOPICS.md`, Program scope charters | Read root boot and ancestor program instructions for the paths about to be acted on; discover other program paths cheaply and read their bodies on entry. Reserve all-program reading for project-wide orientation or changes. | Before touching a newly reached subtree, read its entire applicable program chain. Root/project boot and local amendments remain mandatory. |
| First: instruction-authoring ledger route | Locate and read full entries for the affected rule/failure class rather than treating the entire growing ledger as a required read. | Preserve historical entries and inspect actual evidence, not a heading that sounds supportive. |
| Next: `AGENTS.user.md`, Writing and summary style | Keep the concise preference, peer register, exact-phrasing signal, and diagnostic-gloss rule; move worked before/after examples and incident explanations out of ordinary boot. | These are user preferences, not defaults inferred from the model. Retain examples that distinguish easily confused preferences. |
| Next: `AGENTS.frontier.md`, End-state over checklist | Require an explanation only for a material procedural deviation a reviewer needs to assess, rather than a public deduction for every already-satisfied step. | Observable gates, coordination, exact source reads after context loss, and explicit stops remain excluded from latitude. |
| Next: method-topic reading routes | Replace broad whole-topic obligations with exact matching sections where the topic actually has separable concerns; retain full relevant modules when editing unfamiliar code. | Do not let a filename lookup stand in for reading the contract, or an isolated code line stand in for its callers and guards. |
| Next: global and Codex edit-anchor text | Keep one shared copy-from-visible-source invariant and only harness-specific syntax in the supplement. Remove repeated rationale after checking the combined reading path. | Escaped source characters, intervening writers, truncation, and consumed tool handles are real mechanics, not assumed model competence. |

Suggested replacement for the authoring population sentence:

> Author the shared corpus for the frontier models used for real editing,
> reasoning, and implementation. Keep redundancy when it resolves a concrete
> ambiguity for that population; do not retain it solely for smaller models.

Suggested replacement for the program-reading obligation:

> At project entry, discover project-owned `PROGRAM.md` paths and read the
> root program when present. Before acting in a subtree, read every applicable
> ancestor program in full. Read all programs for a project-wide orientation,
> audit, or change; exclude vendored and external repositories.

These are reviewable drafts, not permissions to ignore the existing rule.
The program change has a straightforward scope argument, but its effect on
discovery mistakes still needs observation. Do not change post-compaction
refresh based merely on the claim that Astra remembers better.

### Astra-specific candidates

Start with no additional teaching of ordinary competence. If a behavior still
fails under the shared reduction, use its actual model, harness, request class,
and defect class to choose scope. A raw error-rate difference between Astra and
Sol does not show that a rule helps one more than the other: the question is
the with/without-rule difference within each model, then their interaction.

First candidates for an Astra presumption switch are the explanatory ceremony
and generic design/checklist coaching above, not authorization, shared dirty
work, exact model identity, shell escaping, or active-run ownership. Keep the
same tests and acceptance contract. Any benefit should appear in less
unnecessary reading/reasoning or fewer clarification turns without additional
repair work. This session does not activate a presumption switch.

Do not put negative overrides in `AGENTS.astra.md` merely to cancel paragraphs
it still has to load from the shared source. Shared cuts benefit all selected
models; genuinely model-dependent loading reductions require the separately
proposed [durable boot compiler](../gaps/agent-specific-durable-boot-compilation.md).
Model-scoped relaxations also require an explicit change to the current
authoring policy, which presently admits tightenings only in model files.

### Project amendments and the growth ratchet

The project-local review covered `~/agents`, `~/ya`, `~/draft`, and `~/x`.
YA-specific corrections belong in YA: its local and tracked instructions were
reconciled around the existing formatting, blame, and isolated UI-verification
contracts. Do not copy its operator recipes into global guidance.

Other candidates remain proposals: the agents checkout's local commit section
describes an obsolete global ask-before-commit default; draft's root boot still
names `~/agents/AGENTS.md` as the global source; X repeats Gerrit identity and
single-review requirements in several places. Preserve the actual per-project
workflow and private exceptions while removing stale authority descriptions
and repetitions. Do not infer from the shared frontier population that a
temporary project model block, vendor boundary, or publish restriction expired.

The authoring change worth trying is a replacement decision, not another
per-incident checklist: after a mistake, consider no instruction change, a
tool/interface fix, clarification of the owning rule, scoped text, and deletion
of a misleading rule alongside addition. Price recurrence and consequence
against repeated reading and compliance cost. One incident can justify a
short protection against catastrophic loss; one cheap retry need not buy a
permanent paragraph. Avoid a fixed one-in/one-out quota and automatic expiry
of safety rules. These are candidate authoring themes, not discovered optima.

The larger search is now specified in
[`instruction-ablation.sketches.md`](instruction-ablation.sketches.md): find
themes recurring in successful guidance-evolution trajectories, then project
back to a minimal reasonable seed that can regenerate useful model-scoped,
defect-scoped guidance. The deferred
[testbed gap](../gaps/instruction-guidance-evolution-testbed.md) tracks that
missing capability. Wait for a later model and explicit budget before running
it; this proposal is not a queued experiment.
