# agent-instructions — testing rider

> How to check a change to the instruction corpus before committing it.
> Convention: [`testing-rider.md`](testing-rider.md).

Topic: `agent-instructions`

Two tiers, cheap-first.

## Mandatory — trace-simulation (cheap, always run)

Before finalizing any instruction change, run the forward-trace pass from
[`agent-instructions.md`](agent-instructions.md) § "Verifying instruction
changes": triage the rules most likely to misfire, construct 2–3 concrete
scenarios each, and play them forward. A change is not done until the
edited rules survive their traces. Highest-risk case is compression/
reword, which can invert a rule's logic while reading fine — see the
2026-05-15 inversion caught in
[`agent-instructions.evidence.md`](agent-instructions.evidence.md).

Passing: each touched high-risk rule has a traced scenario where
following it literally produces a *better* outcome than not having it,
and none produces a worse one.

For main/packet compression, also verify mechanically and by trace:

- the pre-compression body remains recoverable in a mapped packet or Git;
- each governed action still has an observable trigger and
  post-compaction/resume persistence rule in a compaction-protected main or
  short routed index, while its binding action remains in the named packet;
- the default no-reread exception requires verified exact packet
  reconstruction rather than summarized memory or a once-per-session read;
  any broader harness/model/effort override names its evidence and fallback;
- every repository citation to a moved main-file heading resolves to its new
  packet;
- ordinary and rare cases reach only their matching packets, with direct
  compaction-protected routes for narrow high-cost misses; and
- before/after protected and routed-read byte counts are recorded.

## Optional / deferred — outcome ablation (expensive)

For a change whose effect is plausibly measurable on engineering tasks,
the real validation is an outcome comparison, not introspection. Method:
[`instruction-ablation.md`](instruction-ablation.md) — a paired
SWE-bench-style A/B over the corpus with the change vs. without, network
off, paraphrase sweep, McNemar test, CI reported. Run when the change is
load-bearing enough to justify the compute and a pilot shows the effect
clears the noise floor; otherwise record the change's effect as `assumed`
and let local use confirm or kill it.

Passing: a confidence interval on paired resolution that excludes zero in
the claimed direction, stable across paraphrases.
