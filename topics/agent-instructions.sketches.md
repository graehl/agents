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
