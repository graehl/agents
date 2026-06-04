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

## 2026-06-04 — activity register confused with task notes

- **Incident** — an agent doing implementation work was nudged to "log your
  activity" and repeatedly updated a task note / pre-edit-rule note instead
  of creating `.agentctl/active/<session-id>`. A later direct challenge
  surfaced the actual `Agent activity register` rule.
- **Decision** — `AGENTS.md` now states that `.agentctl/active/` must be
  created if missing, that task notes/snapshots/run logs/commit status do
  not satisfy the register, and that agents should use the provider's real
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
