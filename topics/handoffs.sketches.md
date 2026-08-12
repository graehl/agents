# Working handoff sketches

> Dormant candidate extensions to the working-handoff and durable-advisor
> protocol; none is current guidance until promoted into `handoffs.md`.

Topic: `handoffs`

## Capability-asymmetric advisor standing

This is dormant: no underpowered-research-worker deployment is anticipated,
and the safe calibration between today's symmetric verification stance and
“trust absolutely” is unresolved. If a future program deliberately uses
workers known to be materially lower-capability than its advisor, reconsider
the current “assess each other's claims by support rather than role” default.
Metadata could attest the intended capability ordering and shift the worker's
epistemic prior toward the advisor, reducing the failure where a weaker worker
confidently re-litigates and degrades stronger advice. Do not yet prescribe how
far that shift goes.

That trust shift would remain epistemic, not an authority transfer. Advisor
recommendations, want-to-sees, new gates, and rescope would retain their current
authorization treatment. Do not activate the shift from role labels, model
self-report, or ordinary disagreement; require a deliberate program policy,
credible model/effort/capability provenance, and an explicit moderation rule.
Before making this binding, trace the opposite failure: a stronger advisor can
still be stale, wrong about live object state, or overgeneralize outside its
evidence, while a weaker worker may possess the decisive fresh observation.

## Compiled durable boot for a long-running advisor

A long-running advisor is a strong candidate for the proposed compiled-AGENTS
facility in
[`gaps/agent-specific-durable-boot-compilation.md`](../gaps/agent-specific-durable-boot-compilation.md).
Its generated profile could place the exact current charter stack, declared
program scope, authorization/epistemic stance, restart policy, and selected
program instructions in the harness state preserved across compaction. The
source metadata and charter remain authoritative; the compiled profile is a
manifested snapshot of those inputs, never a second place to edit policy.

Routine semantic progress does not justify recompilation or restart. Program
assessment, ranked want-to-sees, document cursors, and intake history continue
to evolve in the advisor's logical-continuity bundle. A material change to the
declared program scope, charter stack, authorization/epistemic policy, or
restart behavior should instead mark the compiled profile stale and advise a
recompile plus clean serving-incarnation restart. That succession validates the
saved bundle, uses the ordinary generation fence, and starts the successor from
the new compiled-input digest. Minor clarification or ordinary evidence
updates leave the incumbent running. This remains a design sketch until the
compiler and its compaction behavior are implemented and tested.

## Advisor-specific interaction wrapper

A future advisor wrapper could sit above a generic session-turn transport and
mechanically assemble the interaction envelope without turning advisor policy
into YA transport semantics. It would resolve the logical advisor metadata and
serving incumbent, verify the generation/session projection, allocate or accept
an interaction id, prepend the opening origin line, and require a final sign-off
before reporting the interaction closed. It could validate the returned close
receipt and updated continuity projection while streaming the advisor's native
conversation between those boundaries.

The wrapper must remain permissive where the protocol is deliberately
best-effort: id reuse, stale metadata, an unavailable incumbent, or a missing
receipt yields structured uncertainty and a user-visible proceed/recovery path,
not an unrecoverable refusal. It does not decide whether advice is correct,
promote advisor objections into gates, or replace the worker's epistemic check.
The generic transport remains independently useful for non-advisor sessions.

## Multiple open-work discovery

If bare `/hi` repeatedly fails to discover important simultaneous work, consider
a plain `tasks/OPEN` manifest naming `tasks/ROOT` plus other open tasks. Do not
introduce `tasks/open/` merely for categorization: nested files would escape
existing `tasks/*.md` discovery, while a symlink set would add cleanup and stale
membership failure modes. Adopt either form only with observed misses and a
defined writer, freshness signal, and retirement lifecycle.
