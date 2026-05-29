# Design thinking

> How to approach a change before and during implementation — independent of language or domain.

Topic: design-thinking

For how these show up in the code itself, see [software-aesthetic.md](software-aesthetic.md) and [software-aesthetic.coordinated.md](software-aesthetic.coordinated.md).

## Reframe before patching

Repair the model of the problem rather than force the output. Before you add a special case, name the invariant it protects and ask whether a different representation removes the need for it entirely. A run of "if this input, force that output" clauses is a design smell unless each branch follows from a stated domain rule. The same test gates every new concept or abstraction: name the problem it solves and the invariant it holds, then check whether a simpler representation makes it unnecessary.

This is *code judo* — a reframing that preserves behavior while deleting whole branches, layers, or concepts. The aim is to make the change look inevitable in hindsight, not to polish the structure already there.

## Map before drilling

Entering an unfamiliar area, build the high-level map first — the modules, callers, and invariants that matter, named in the project's vocabulary — before opening any single function. The map decides which functions are worth reading; you do not start deep inside one function and reconstruct the system outward from it. On re-entry, refresh the map before drilling again.

## Hypotheses over traces

Treat every assumption as a hypothesis until you check it. Form one that fits the known invariants, then test it against the trace — not the reverse. Replaying the trace with no hypothesis in hand produces patches, not understanding.

## Scope discipline

Build for the problem in front of you, not a hypothetical future. A bug fix needs no surrounding cleanup; a one-shot needs no helper. Add no feature, refactor, or abstraction the task did not ask for.
