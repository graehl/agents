# Agent Instructions Theory

> The repo's core correctness claim: committed global instructions
> give future agents stable, searchable policy across projects
> without relying on stale chat state.

Topic: `agent-instructions`

This repo's main correctness claim is that committed global instructions give
future agents enough stable, searchable policy to behave consistently across
projects without relying on stale chat state.

Provider placement, compaction behavior, and the request-conditioned boot
mechanism are developed in YA's
[agent-context-injection topic](https://github.com/graehl/yepanywhere/blob/main/topics/agent-context-injection.md).
That topic owns harness facts and launch mechanics; this repository owns policy
selection, scoped model/harness corrections, and instruction ablation. Each
repository remains usable without the other.

## Contracts

- `AGENTS.global.md` is the authoritative global policy file and the source
  installed into each harness's global instruction location.
- `AGENTS/` contains optional clarification packets and is never an install
  target or routine directory read. `AGENTS.global.md` retains every binding
  rule and wins on conflict.
- The root `AGENTS.md` is this checkout's project boot. It must not be used as
  a harness-global install target, or work launched here receives the global
  corpus again as project context.
- `RUNS.md` and `RESEARCH.md` are compact action-triggered routers. Their
  canonical subdirectories contain binding concern packets; observable cues in
  the routers and selected compaction-protected global routes name which
  packets to read.
- Local project instructions may add narrower rules, but global policy changes
  belong here first.
- Correctness topics are defined by committed `topics/*.md` basenames, and
  related commit series use matching `Topic:` trailers.
- Task files may track work, but they are not the durable source of global
  correctness arguments.

## Invariants

- Instruction changes should be load-bearing: they should steer behavior that
  a capable agent would otherwise plausibly get wrong.
- A rule that introduces process cost should identify the failure mode it
  prevents.
- Procedural rules should name the end state their steps serve, so a
  capable reader can judge when a step's purpose is already met
  (`AGENTS.frontier.md` grants that step-skipping latitude explicitly,
  priced at a stated one-line deduction). When the observable step
  itself is the contract — a gate record, a stop, a coordination
  write — the rule should say so rather than leave it to inference.
- Topic and theory names should stay searchable from commits, tasks, and
  instruction text.
- Theory docs should explain why contracts are believed, not accumulate a
  chronological list of every change.
- Boot-loaded text (`AGENTS.global.md`, routed model/harness supplements, and
  anything else read every session) budgets every token: a sentence earns its place only by
  steering behavior. Worked examples and rationale that stop a weaker
  agent reasoning around a rule qualify. When the user endorses a
  rule's rationale, do not offer to write the endorsement back into
  the rule — that is validating commentary, not steering; it belongs
  in the unloaded riders (`.evidence.md`).
- Instructions should steer behavior, not flatter the reader. Prefer
  phrasing that changes what an agent does over wit that evokes several
  related-but-non-instrumental meanings: an aphorism or clever reversal
  reads as profound while leaving the directive ambiguous, and an agent
  can comply with it performatively without changing behavior. When a
  rule needs its *why*, name the concrete failure it prevents rather than
  restating the rule in fancier words.

## Contract Notes

- The topic namespace depends on `ls topics/*.md`, so agents have one
  committed place to inspect both the topic name and its correctness model.
- The `agent-instructions` topic spans commit policy, task cross-references,
  and theory docs because all three determine how future agents recover the
  intended policy from repository state.

## Shared worktree: isolation traded for observability

The ecosystem's standard answer to concurrent coding agents is
worktree-per-agent isolation: it converts silent concurrent clobbering
into deferred, visible merge conflicts, and it presumes high fan-out of
independent tasks. <!-- verified: web search 2026-06-10 --> This repo
deliberately occupies a different operating point — a few deliberate,
overlapping sessions in one shared dirty worktree; high fan-out has
never been the workload here.

The trade is isolation for observability:

- interrupted or quota'd-out efforts stay visible in `git status`,
  where the user or the next session trips over them, rather than
  orphaned in a forgotten worktree — resume-from-live-state works
  *because* the live state contains everything;
- integration is continuous, and a collision is resolved at edit time
  by the second writer with both contexts warm, not at merge time by
  someone with neither;
- the human can read the entire world state in one place;
- agents can work with the user's uncommitted WIP, which a fresh
  worktree definitionally cannot see — though this cuts both ways:
  the user's manual work is thereby foisted on agents too, and every
  session inherits half-done human state it did not create and must
  preserve and work around;
- a plain filesystem convention stays uniform across harnesses, which
  keeps the subagent-agnostic stance cheap.

The shared-workdir conventions buy back the safety isolation would
have provided: active-session files with scope declarations supply the
peer awareness isolation substitutes for; pre-edit rereads,
path-limited edits and commits, and the discard/amend bans target the
silent-clobber risk that motivates isolation in the first place.

Known residuals the conventions only shrink, not remove: an agent may
read a peer's mid-edit state and reason from it as settled
(mental-model contamination); shared runtime state — a dev server,
database, or watcher — collides independently of file discipline; and
the approach has a write-concurrency ceiling. For genuinely
independent batch fan-out, ancillary worktrees remain the right tool
and are already permitted.

The conventions also charge their own pace tax: active-session
writes, peer checks, and heartbeats are per-session overhead paid
even when no peer is present, and peer-aware caution (amend bans,
scope negotiation) slows work further when peers do appear. Whether
the awareness is worth that tax is untested — an ablation-shaped
question like the rest of this file (see *Limits of these methods*).

## Section extraction

The instruction surface is every file reachable at its trigger moment
(before committing, before testing, on a named verb or situation), not
only the always-read root. When adding or growing instruction content,
prefer a short trigger paragraph in the boot-loaded file — "when
<situation>, read <doc> and follow it" — with the detail in the
dedicated file, once the content exceeds a short paragraph. Inline
boot-loaded text is for rules that must fire unconditionally. Two
conditions make the pattern safe: the trigger is concrete
(verb/situation-anchored — a rule behind a missed trigger never
fires), and the trigger sentence itself carries the immediate steer (the
command to run, the stop to make) so an agent that defers the read
still acts safely.

Compaction makes the trigger boundary temporal as well as topical. Exact
survival of `AGENTS.global.md` does not protect a prior tool-read policy body.
A load-bearing read trigger therefore fires again at the governed action after
compaction/resume; “already read this session” is not sufficient. Under the
unknown-capability default, skipping that refresh requires verified harness
reconstruction of the exact current routed packet, not a model's recollection
that it read the file. A boot-loaded scoped supplement may define another
evidence-backed cadence under the capability model below. The routed index is
compact enough to pay the repeat cost when protection is absent. Its
condition-routed packets preserve the binding bodies and rare clarification
without becoming a second mandatory boot.

The original narrower case: when a topic doc would benefit from
referencing a specific `AGENTS.global.md` section, prefer extracting that
section to a dedicated file so `AGENTS.global.md` keeps a pointer and the file
carries the full content. Avoids restatement and lets topic docs link
the dedicated file rather than a deep `AGENTS.global.md` section.

## Modeling agent capability and tendency

The right refresh policy is a capability/tendency model, not a universal
reread cadence and not the agent's self-report that it remembers. *Capability*
means what exact state the harness preserves or reconstructs and what the model
at a given effort can reliably retrieve and apply. *Tendency* means observed
behavior in the governed situation: for example, acting from a vague compacted
summary, skipping a routed read because the filename feels familiar, or
reloading a whole packet when one located section would suffice.

Choose the policy for a routed packet from four inputs:

- **Residency:** is the exact current packet protected or reconstructable in
  model context, merely represented in a summary, or absent?
- **Retrieval and application:** under traces or outcome measurements, does
  this route and model find the applicable section and obey it after the
  relevant interruption? Provider or model-family reputation is not evidence
  for the specific behavior.
- **Effort and request class:** reasoning effort and task shape may change
  retrieval and application. Do not assume the change is monotonic; record the
  actual setting with the observation.
- **Stakes and cost:** price the consequence of a missed rule against read
  latency, repeated tokens, protected-context burden, and displacement of
  recent goal/task state. This selects whole-packet read, section location, or
  justified reliance on protected content.

With no scoped evidence, the conservative fallback remains: after compaction
or resume, refresh the compact binding main at the governed action. Verified
exact reconstruction discharges that refresh. A harness-, model-, or
effort-scoped supplement may tune the cadence only when it names the packet,
trigger, evidence, relaxation, and safe fallback. Avoid the instruction "read
it if you forgot it": an agent cannot reliably observe content it has forgotten
and a summary can create false familiarity. Use observable events and action
boundaries instead.

The project `AGENTS.md` states the durable-routing aspiration and points here;
it should not freeze a universal cadence. Changes to this model are hypotheses
subject to the trace and ablation disciplines below.

For the initial personal integration, YA may compile this repository's selected
policy into the exact global boot a harness protects. The provider-side
contract and opt-in boundary live in the linked YA topic; the deferred local
compiler/install work is captured in
[`gaps/agent-specific-durable-boot-compilation.md`](../gaps/agent-specific-durable-boot-compilation.md).

## Verifying instruction changes

A reading pass finds rules that *look* wrong; it misses rules that only
misfire when practiced. Before finalizing an instruction change — and
especially after compressing or rewording existing rules — run a
trace-simulation pass:

1. Triage (cheap): pick the rules most likely to misfire — those that fire
   often, overlap with other rules, hedge, or create perverse incentives.
2. Simulate (bounded): for each, construct 2-3 concrete scenarios and play
   the rule forward. Does following it literally produce a worse outcome
   than not having it?
3. Keep only changes that survive their traces; fix the ones that fail.

This is the falsification discipline applied inward: "what realistic
situation makes this rule backfire?" Compression is the highest-risk case —
a reword can invert a rule's logic while still reading fine on the page,
and the inversion surfaces only in a trace.

Past trace passes and what they caught are recorded in the companion
ledger `agent-instructions.evidence.md` — consult it when proposing an
instruction change, not routinely.

When a trace exposes that the rule's gap is only safe because a frontier
agent infers around it, prefer adding redundancy (a worked example, or the
rule's rationale) over leaving the gap, since non-frontier agents also edit
these projects.

## Limits of these methods

The verification apparatus here — trace-simulation and the
`*.evidence.md` ledgers — is intuition-grade, not measurement. Every
rule rests on the unverified premise that an agent reads meaningful
text and acts on it; none has been validated by an outcome comparison
(see `agent-instructions.evidence.md`, 2026-05-29).

Be skeptical of the evidence-ledger ritual itself. Appending something
true and interesting-in-the-moment *feels* like progress — capture,
provenance, diligence — while changing no future behavior. That is the
celebratory failure of [design-thinking](design-thinking.md) wearing a
lab coat: a note can read as insight and be inert. Append only what
would plausibly change a later decision (the ledger's own trigger), and
treat the act of writing as zero evidence that the underlying rule
works.

The real validation, deferred until compute is cheap enough, is to test
agents on engineering tasks under varied instruction setups and measure
outcomes — an ablation over the instruction corpus, not introspection
about it. Until then, a well-written rule is a hypothesis, not a result.
The concrete method for that ablation — SWE-bench-style, paired,
network-off, with the confound and contamination controls a small effect
needs — is [`instruction-ablation.md`](instruction-ablation.md); how to
check any instruction change (cheap trace-sim now, ablation when worth
it) is the rider [`agent-instructions.testing.md`](agent-instructions.testing.md).

Prior art grounding that plan <!-- verified: web search 2026-05-29 -->:
- **SWE-agent** (Yang, Jimenez et al., NeurIPS 2024; arXiv 2405.15793) —
  ablation on 300 SWE-bench issues: a tailored agent-computer interface
  solves 10.7 pp more than the same model on a bare shell. The closest
  existing evidence that scaffolding/instruction design has a large,
  measurable effect on engineering success.
- **SWE-bench** (Jimenez et al., ICLR 2024; arXiv 2310.06770) — the
  real-GitHub-issue benchmark such an ablation would run on.
- **"State of What Art? A Call for Multi-Prompt LLM Evaluation"**
  (Mizrahi et al., TACL 2024; arXiv 2401.00595) — across 6.5M instances,
  20 models, 39 tasks, instruction paraphrases change absolute *and
  relative* performance. An instruction ablation must therefore sweep
  paraphrases, not conclude from one wording.
- **"An Empirical Study on the Effects of System Prompts in
  Instruction-Tuned Models for Code Generation"** (arXiv 2602.15228) —
  360 configurations isolating system-prompt detail for code gen; close
  to the experiment template this plan wants.
- **"Trust Over Fear: Motivation Framing in System Prompts Affects AI
  Agent Debugging Depth"** (arXiv 2603.14373) — measured: framing shifts
  agents from breadth-first scanning to depth-first investigation (~74%
  more investigative steps, ~25% more hidden issues found). Direct
  evidence that instruction *tone*, not only content, moves engineering
  behavior — encouraging for this corpus, and a caution that effects are
  framing-confounded.
- **"LLMs Cannot Self-Correct Reasoning Yet"** (Huang et al., DeepMind,
  ICLR 2024; arXiv 2310.01798) — without external feedback, intrinsic
  self-correction does not help and can degrade. Direct caution that a
  self-recorded evidence ledger is not self-grounding.

## Frontier-capability review register

Guidance whose appropriate strictness or routing may change with model or
harness capability is selectively indexed in
[`frontier-capability-review.md`](frontier-capability-review.md). Its owning
instruction remains authoritative. A major frontier generation, fresh user
experience, or the 60-day backstop may trigger review; no-op is valid. Start
with ordinary traces, use a bounded presumption switch when cheap, and reserve
controlled instruction ablation for explicitly high-value questions.

## Harness-, backend-, and model-scoped supplements

`AGENTS.codex.md` and `AGENTS.claude.md` are sibling instruction files for
harness-specific mechanics: session-log locations, real resume identifiers,
provider skill paths, and launcher quirks. Each reads the model id from its
harness transcript and routes matching model-scoped behavior patches.
`AGENTS.global.md` routes agents to the matching harness supplement when present but
keeps cross-provider policy in the main file.

`AGENTS.copilot.md` is route-scoped rather than model-scoped. Native Copilot
CLI exposes `COPILOT_CLI=1`; YA propagates `YEP_COPILOT_API=1` only after an
Anthropic-compatible gateway explicitly identifies itself through its model
catalog response. Both routes load the same stricter optional-subagent proof,
and a Claude Gateway launch also retains its Claude and model supplements.

`AGENTS.weak.md` is a sibling instruction file carrying restatements of
behavior that frontier agents perform by default but weaker models
(Haiku, Kimi, Spark-class) tend to miss. It is surfaced by provider-specific
launcher conventions when a smaller model is in use.

Edit policy: `AGENTS.weak.md` is for restatements of frontier defaults
only. Anything load-bearing — a rule a capable agent would otherwise
plausibly get wrong — belongs in `AGENTS.global.md` itself, so every model
loading the main file gets it.

`AGENTS.frontier.md` is the dual of `AGENTS.weak.md`: latitude
grants — currently end-state-over-checklist step skipping — that a
weaker model would read as a rationalization license. The Claude and
Codex supplements route to it; the Grok supplement does not, and both
the pointer and the file itself disclaim the file when
`AGENTS.weak.md` was also surfaced (a frontier-provider harness can
still be running a small model). Both supplements also name an explicit
model floor (Claude: haiku-class is weak; Codex: below GPT-5.5,
Spark-class included) that self-serves `AGENTS.weak.md` without
depending on the launcher. Tier is determined by grepping the
harness-recorded model id from the session's own transcript, never by
the model's self-knowledge of its name — models misreport that.

Edit policy: `AGENTS.frontier.md` carries relaxations only — never a
rule an agent must follow, since weaker-model launches never load it.
Anything binding belongs in `AGENTS.global.md`.

`AGENTS.anthropic.md`, `AGENTS.opus.md`, and `AGENTS.sol.md` are model-scoped
behavior patches. Both harness supplements route to them from the
harness-recorded id, so a model keeps its patch when served through another
harness. The Anthropic-family patch requires technical glosses to state the
relevant operational distinction, expose uncertainty, or be omitted. Opus
additionally carries the path-trace rule against overconfident assertions about
unread code and the boot-list check before calling a request verb ambiguous.
Sol carries the confirmation rule formerly housed in the Codex supplement and
the direct-work correction for Sol served through Claude Gateway.

Edit policy: model supplements carry model-specific tightenings only. A rule
that would improve every model belongs in `AGENTS.global.md`; a relaxation belongs in
`AGENTS.frontier.md`; transport, session, log, and tool-format mechanics belong
in the harness supplement. A backend supplement may tighten behavior only
where the backend or its quota/visibility constraints make the distinction
load-bearing.
