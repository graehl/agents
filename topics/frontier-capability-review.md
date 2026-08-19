# Frontier capability review

> A selective register of instruction guidance whose strictness or routing may
> need reevaluation as frontier models improve, reviewed from new evidence or
> on a 60-day backstop without making heavyweight evaluation routine.

Topic: `frontier-capability-review`

This is the durable landing page for model-capability-sensitive guidance, not
a gap that remains open until every entry disappears. The owning instruction or
topic remains authoritative. This register says why a rule is worth revisiting,
what evidence would change it, and whether experience has already downgraded or
retired an earlier default.

## Admission bar

List an item only when model or harness capability plausibly changes the right
strictness, routing, or ceremony and a future review could materially improve
behavior or reduce prompt cost. Do not index every provisional rule, ordinary
product TODO, or policy whose need is independent of capability.

A review is due after a major frontier-model generation, when the user brings
fresh experience, or on the 60-day scheduled backstop. A due review is allowed
to conclude that no evidence changed and make no wording edits.
The tracked prompt source at
[`at/frontier-capability-review.md`](../at/frontier-capability-review.md) and
its clone-local activation implement that backstop.

## Evidence and disposition

Use the lightest evidence that can change the decision:

1. Start with new user experience and ordinary task/session traces.
2. When a plausible capability improvement is cheap to test, run a bounded
   anecdotal **presumption switch**: temporarily assume the new frontier model
   can supply the formerly missing judgment, relax the selected rule for one
   suitable session, and inspect the outcome.
3. Reserve controlled guidance-A versus guidance-B evaluation—such as the
   paired SWE-bench-style design in
   [`instruction-ablation.md`](instruction-ablation.md)—for explicitly
   high-value items whose likely benefit justifies the substantial compute and
   analysis cost. A calendar review never requires this tier by itself.

For each reviewed item choose `retain`, `narrow`, `relax`, `promote`, or
`retire`. Update the owning guidance first, then this register, and append the
evidence or trace to
[`frontier-capability-review.evidence.md`](frontier-capability-review.evidence.md)
or the owning instruction ledger. Do not churn wording merely to prove that a
review occurred.

## Register

| Guidance | Current stance | Owning guidance | Why capability-sensitive / what would change it |
|---|---|---|---|
| Outsourcing worker decisions to an advisor | **Retired.** Ask for findings and arguments for and against the worker's proposed choice, then decide independently; do not ask the advisor to choose, rank what the worker should do, grant permission, or accept a rebuttal. | [`_RESEARCH/direction.md`](../_RESEARCH/direction.md) and [`advisor/serve.md`](../advisor/serve.md) | Reconsider only if the user or a governing artifact explicitly delegates a decision, or a later advisor demonstrably has broader relevant context and an agreement loop improves decisions enough to repay its latency. |
| Frontier end-state-over-checklist latitude | **Frontier-only relaxation.** | [`AGENTS.frontier.md`](../AGENTS.frontier.md) | Promote, narrow, or retire based on whether newer tiers reliably infer checklist purpose without bypassing observable gates. |
| Frontier latitude for opportunistic cleanup in user-authored code | **Frontier-only relaxation.** | [`AGENTS.frontier.md`](../AGENTS.frontier.md) | Revisit when a new tier's scope judgment or blame-aware cleanup quality changes materially. |
| Opus path-trace tightening for claims about unread code | **Model-specific tightening.** | [`AGENTS.opus.md`](../AGENTS.opus.md) | Narrow or retire if a successor generation stops making consequential ungrounded cross-file claims in long tasks. |
| Opus continuation through long, compacted sessions | **Model-specific tightening.** | [`AGENTS.opus.md`](../AGENTS.opus.md) | Narrow or retire if a successor generation stops inferring false context exhaustion, or a harness exposes a reliable capacity signal the model uses correctly. |
| Copilot route's strict delegation proof | **Route-specific tightening; the former global delegation gate is retired.** | [`AGENTS.copilot.md`](../AGENTS.copilot.md) | Relax if current route traces no longer show planning-subagent or overdelegation pressure; retain if the harness tendency persists. |
| Post-compaction routed-packet refresh | **Conservative unknown-capability default; exact harness reconstruction may discharge it.** | [`AGENTS.global.md`](../AGENTS.global.md) and [`agent-instructions.md`](agent-instructions.md) | Adjust only from observed residency/retrieval behavior for the named harness, model, effort, packet, and request class, with a safe fallback. |

## Review output

A useful review records the trigger, model/harness/effort, evidence inspected,
disposition per affected row, and exact owning guidance changed—or `no change`
with the reason. It may add a newly observed high-value item or remove one whose
owner and historical disposition are sufficiently discoverable elsewhere.
