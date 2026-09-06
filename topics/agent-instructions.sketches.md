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

Proposed 2026-09-06; the shared first pass has since been applied at the user's
request. Its current contracts live in the owning instruction files. Remaining
model-specific candidates and outcome experiments below remain deferred.
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

### Shared first pass promoted

The user authorized direct improvements and reported scoped extractions honored
since at least Opus 4.8/Sol. The applied pass narrows program reads to the entered
chain except for project-wide work, selects relevant topic sections and complete
ledger entries, removes repeated preference/commit prose, and explains only
material checklist deviations. Rare Codex recovery/run mechanics and the PDF
recipe now have conditional owners; YA capability detail routes to the existing
environment inventory. The shared edit-anchor invariant remains in global boot.

Current authoring policy and the extraction contract are in
[`agent-instructions.md`](agent-instructions.md); its evidence ledger records
the before/after source sizes, displaced-content map, and trace checks. No
outcome improvement or new post-compaction refresh latitude is claimed.

### Astra-specific candidates

Start with no additional teaching of ordinary competence. If a behavior still
fails under the shared reduction, use its actual model, harness, request class,
and defect class to choose scope. A raw error-rate difference between Astra and
Sol does not show that a rule helps one more than the other: the question is
the with/without-rule difference within each model, then their interaction.

Remaining candidates for an Astra presumption switch are generic design and
checklist coaching beyond the shared cuts, not authorization, shared dirty
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

The agents checkout's private local commit section now reflects the global
proactive-commit rule. Other project candidates remain proposals: draft's root
boot still names `~/agents/AGENTS.md` as the global source; X repeats Gerrit identity and
single-review requirements in several places. Preserve the actual per-project
workflow and private exceptions while removing stale authority descriptions
and repetitions. Do not infer from the shared frontier population that a
temporary project model block, vendor boundary, or publish restriction expired.

The replacement decision after an incident is now part of the authoring topic:
consider tool fixes, no change, narrower text, and deletion alongside addition.
That is a judgment-based policy, not a discovered optimum.

The larger search is now specified in
[`instruction-ablation.sketches.md`](instruction-ablation.sketches.md): find
themes recurring in successful guidance-evolution trajectories, then project
back to a minimal reasonable seed that can regenerate useful model-scoped,
defect-scoped guidance. The deferred
[testbed gap](../gaps/instruction-guidance-evolution-testbed.md) tracks that
missing capability. Wait for a later model and explicit budget before running
it; this proposal is not a queued experiment.
