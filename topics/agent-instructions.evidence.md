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

## 2026-05-15 — dcb23f3 — AGENTS.md compression pass

Trace-simulated five high-risk rules during a ~44% token-compression of
AGENTS.md. Caught one regression the compression itself introduced: the
resume-source-priority staleness rule had "older than live files" reworded
from an additional staleness *trigger* into an *exception* ("presume stale
unless ... or older"), inverting it. Fixed in dcb23f3.

Verified claim: a reword can invert a rule's logic while still reading
correctly on the page; only a forward trace surfaces it. A pure reading
pass missed this one.
