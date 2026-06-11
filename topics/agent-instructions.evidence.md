# agent-instructions — verification evidence

A ledger for the instruction system: trace-simulation catches (see
the "Verifying instruction changes" section of
`agent-instructions.md`), incident reports of instructions that
caused mistakes or confusion in practice, and the agent's own notes
— observations, hypotheses, decisions, or beliefs — on the
instruction system. The wider convention is documented in
`AGENTS.md § Authority and instruction files`.

This companion is **not** loaded by normal instruction-following agents.
Consult it only when proposing an instruction change, or when auditing
whether a rule is safe to follow as written. Keeping the evidence here
rather than in inline `<!-- verified -->` markers means the provenance
costs no tokens until an agent is actually in one of those modes.

Append new entries at the top; do not rewrite prior ones. Agents are
licensed to append trace findings, incident reports, and clarifying
examples encountered while consulting this file.

## 2026-06-10 — Git patch output must bypass human diff config

- **Incident** — agents still sometimes ran patch-producing Git commands
  that inherited the user's human-facing `diff.external=difft` or
  `core.pager=delta` config, then had to rerun because the first output was
  difftastic/delta-formatted rather than plain unified text.
- **Decision** — broadened `AGENTS.md` from a presentation-only
  `git diff --no-ext-diff --no-color` preference to a patch-output rule:
  patch-producing Git reads and instruction templates use `git --no-pager`
  plus `--no-ext-diff --no-color`, and the C++ `clang-format-diff` template
  includes the same flags.
- **Trace** — agent reviews a diff in a user shell with `diff.external=difft`:
  the literal rule yields a plain patch on the first command instead of
  a human layout that must be rerun. Agent copies the C++ modified-lines
  template into a pipe: `clang-format-diff` receives unified patch text, not
  difftastic output. Agent retrieves commit-message text with
  `git log --format=%B`: the rule does not add irrelevant diff flags because
  that command is not patch-producing.

## 2026-06-09 — harsh review of the topic-trigger compression

- **Finding** — three blocks were deleted rather than moved, leaving
  new read triggers pointing at docs that lacked the promised detail:
  the active-sessions file schema (`AGENTS.md` routed "active-session
  semantics" to `agentctl`, which disclaimed the convention while
  `/others` still parses "the schema-defined scope declaration"); the
  shared-worktree amend procedure (`AGENTS.md` claimed the full
  procedure lives in `commits`, which carried only message mechanics);
  and the vernacular-row → topic-doc bar (the trigger names that
  decision; `glossary` did not answer it).
- **Repair** — restored each block into the doc its trigger names, and
  re-inlined two write-time triggers that fire when no topic doc is
  open (glossary check when prose spells out what one term could
  carry; bearings read on a stated recollection of where work stands).
- **Lesson** — compression review must verify the pointer target
  actually contains the displaced content, block by block; "the
  owning topic has it" is a per-block claim to check, not a per-file
  one.

## 2026-06-09 — AGENTS.md topic-trigger compression

- **Decision** — shortened long `AGENTS.md` procedure blocks by keeping
  first-turn safety obligations inline and moving slower mechanics behind
  explicit topic-read triggers. Active-session implementation details point
  to `agentctl`; full commit-message and topic-trailer rationale moved to
  `commits`; topic-doc format and glossary regeneration/sub-glossary
  mechanics point to their existing topics.
- **Trace** — no-`.agentctl/` shared repo: the compressed active-session
  rule still requires creating `.agentctl/active/<session-id>`, discovering
  the provider id first, checking fresh non-DONE peers, and marking `DONE`;
  deeper `agentctl active` behavior is correctly deferred to `agentctl`.
  Local correction after a commit: the compressed commit section still
  routes non-trivial messages and all amends to `commits`, and the shared
  worktree amend ban remains inline. New topic/glossary maintenance:
  creation, normalization, regeneration, promotion, and ambiguity resolution
  now have explicit read triggers, while ordinary first-repo-use glossary
  lookup remains inline.
- **Residual** — effect on outcome is still assumed. The compression reduces
  first-load size but intentionally leaves big-effect gates, discard bans,
  edit-mechanism discipline, and symptom-vs-invariant examples inline
  because a missed trigger there would be costlier than the saved tokens.

## 2026-06-04 — provider mechanics split from shared policy

- **Decision** — introduced `AGENTS.codex.md` and `AGENTS.claude.md` for
  provider-scoped mechanics, while `AGENTS.md` keeps the shared contract and
  routes agents to the matching supplement. Codex-specific session JSONL
  lookup and skill-path aliasing moved out of the shared file; Claude's
  local transcript path is recorded in its supplement.
- **Trace** — a Codex session reads `AGENTS.md`, then `AGENTS.codex.md`, and
  can recover the real resumable id from `~/.codex/sessions/` before writing
  `.agentctl/active/<session-id>`. A Claude session reads
  `AGENTS.claude.md` and searches `~/.claude/projects/**/*.jsonl` when the
  shared policy says "provider session logs." A future provider sees only the
  shared contract; if no supplement exists, it reports once and continues
  without inheriting Codex/Claude-specific paths.

## 2026-06-04 — active-sessions entry confused with task notes

- **Incident** — an agent doing implementation work was nudged to "log your
  activity" and repeatedly updated a task note / pre-edit-rule note instead
  of creating `.agentctl/active/<session-id>`. A later direct challenge
  surfaced the actual `Active sessions` rule.
- **Decision** — `AGENTS.md` now states that `.agentctl/active/` must be
  created if missing, that task notes/snapshots/run logs/commit status do
  not satisfy active sessions, and that agents should use the provider's real
  resumable session id from session metadata/logs when discoverable.
- **Trace** — in a repo with no `.agentctl/` directory, the first
  planning-to-act step creates `.agentctl/active/<real-session-id>` before
  implementation edits. In a context compaction or resume, the agent
  recovers the same provider id from session metadata/logs and updates the
  existing register file rather than minting a new tag. In a provider
  environment with no discoverable id, a stable unique personal tag is
  permitted only after the metadata/log search fails, and it must be reused.

## 2026-05-30 — concrete ablation method + `.testing` rider convention

- **Decision** — wrote [`instruction-ablation.md`](instruction-ablation.md),
  the concrete realization of the deferred validation plan: a paired
  SWE-bench-style A/B over the corpus, network-off and directory-scoped
  (no OS-level isolation — user does not demand it for a supervised
  workflow), with McNemar pairing, a paraphrase sweep, contamination
  invariants, and a cheap pilot to estimate the noise floor before the
  full spend. Still a proposal — nothing has been run.
- **Convention** — standardized an optional `<topic>.testing.md` rider
  (see [`testing-rider.md`](testing-rider.md)): how to check a change to
  a topic's concern. The agent-instructions rider
  ([`agent-instructions.testing.md`](agent-instructions.testing.md))
  makes trace-simulation the mandatory cheap tier and the ablation the
  optional/deferred tier. Decision-relevant for a future agent proposing
  an instruction change: there is now a named check to run.

## 2026-05-29 — the whole instruction corpus is intuition, not measurement

- **Claim** — the habits and triggered focusings these docs prescribe
  (map-before-drilling, reframe-before-patching, glossary reuse, the
  topic/bearings reading triggers, etc.) actually produce better design,
  debugging, tech-debt avoidance, reliability, and clearer user
  communication.
- **Status** — `assumed`. No rule in `AGENTS.md` or the topic docs has
  been validated by an outcome comparison (with-rule vs. without-rule on
  comparable work). The justification is entirely introspective: the
  load-bearing test ("would a capable agent get this wrong otherwise?")
  and trace-simulation ("play the rule forward, does it backfire?") are
  both *predictions* about behavior, not observations of it.
- **Method** — none beyond reading-pass and trace-sim. The 2026-05-15
  entry below is the closest to evidence, and even it only establishes
  that a *failure* was real (a reword inverted a rule), not that a rule
  *fixes* anything. The underlying bet is the unmeasured premise that
  "agents can read and understand meaningful text and will act on it."
- **Residual** — no cheap general validation exists; outcomes are
  confounded and per-session. The cheapest real signals are local:
  (a) glossary buy-in is directly observable — a term either gets picked
  up in user speech and code or it keeps getting paraphrased around, and
  an unused row failed regardless of how well it reads; (b) a rule that
  fires on a known failure mode can be spot-checked the next time that
  mode would have recurred. Default posture: mark a new rule's effect
  `assumed` and let real use confirm or kill it; do not treat a
  well-written rule as settled because it reads well.

## 2026-05-15 — dcb23f3 — AGENTS.md compression pass

Trace-simulated five high-risk rules during a ~44% token-compression of
AGENTS.md. Caught one regression the compression itself introduced: the
resume-source-priority staleness rule had "older than live files" reworded
from an additional staleness *trigger* into an *exception* ("presume stale
unless ... or older"), inverting it. Fixed in dcb23f3.

Verified claim: a reword can invert a rule's logic while still reading
correctly on the page; only a forward trace surfaces it. A pure reading
pass missed this one.

## 2026-06-11 — commentary-validation expansion offer

- User endorsed the rationale of the new AGENTS.md "'Add X' when X
  already exists" rule (an early "this already exists" complaint beats
  finishing the work and disclosing after). Agent responded by
  offering to add a sentence naming that failure mode to the
  boot-loaded rule. User flagged the pattern: offering additive boot
  text to validate a user's commentary is sycophancy-shaped, and
  boot-loaded files want zero wasted tokens — commentary belongs in
  unloaded riders like this one.
- User refinement in the same exchange: searching the discussion for
  worth-the-cost additions is still good; the test for a candidate is
  steering merit, never that the user agreed.
- Invariant added to `agent-instructions.md` same day. Note the
  boundary it must respect: AGENTS.md's load-bearing section
  deliberately keeps weak-agent redundancy (worked examples, rationale
  for counterintuitive rules), so "zero waste" means
  non-steering text, not all redundancy.

## 2026-06-11 — frontier latitude: end-state over checklist

- **Motivating observation** — a mid-capability agent (GPT-5.5 Codex,
  below Fable-class) correctly exercised *unstated* latitude: the only
  change since the HEAD commit was a topic-doc note about future
  possibilities, the commit message already told reviewers to read
  that topic, so it pushed without amending the message. Sound
  deduction; the checklist step's purpose was already met. User
  framing: most projects assume autonomous "implement this considering
  global implications, intended contract, and existing UX
  expectations" — that is a *floor* on instruction-following
  capability, so instructions may spec checklists as a default path
  with the end state as the contract.
- **Change** — added `AGENTS.frontier.md` (end-state-over-checklist
  latitude, stated-deduction requirement, gate/ban carve-out), routed
  from the Claude and Codex supplements only; author-side invariant
  (procedural rules name the end state they serve) added to
  `agent-instructions.md`. Dual of `AGENTS.weak.md`, which adds
  scaffolding downward where this relaxes upward.
- **Trace-sim catches while drafting** —
  (a) "I generally know what `topics/commits.md` says" must not
  satisfy a read-before trigger, so the rule requires the deduction to
  cite session-local evidence, not general confidence;
  (b) a frontier-provider harness can still run a small model (Haiku
  via the Claude supplement), so the weak-guard lives both at the
  supplement pointer and in the frontier file's header;
  (c) gates whose observable step is the contract (gate record,
  discard ban, edit-mechanism discipline, `.agentctl/active/` writes)
  are exactly defenses against "the end state is fine anyway"
  reasoning, so they are excluded by name.
- **Status** — `assumed`, per the 2026-05-29 posture. The latitude was
  already being taken by capable models; the rule's marginal effect is
  making the skip legitimate and auditable (the stated one-line
  deduction) rather than enabling it.

## 2026-06-11 — Codex model floor: below GPT-5.5 is weak

- Same-day follow-up to the frontier-latitude entry above. The
  Haiku-via-Claude guard keyed only on the launcher having surfaced
  `AGENTS.weak.md`; user pointed out Codex 5.3 Spark may run under the
  Codex supplement the same way, so the guard must not depend on the
  launcher. `AGENTS.codex.md` now names an explicit floor: below
  GPT-5.5 counts as weak — self-serve `AGENTS.weak.md`, skip
  `AGENTS.frontier.md`.
- User assessment worth keeping (their direct observation): Spark is
  sloppy enough to be a high-supervision / likely-not-worth-it model
  for this setup, hence floor-by-name rather than trusting a Spark
  launch to self-assess capability.
- Known limit: the floor asks the model to read its own model name
  from harness context and follow a branch — a weak model can fail
  exactly that. Defense in depth, not a guarantee; the
  launcher-surfaced `AGENTS.weak.md` path remains the primary
  mechanism.
