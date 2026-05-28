# Design thinking

> Principles for approaching a change or problem before and during implementation — independent of language or domain.

Topic: design-thinking

For how these principles manifest in code specifically, see [software-aesthetic.md](software-aesthetic.md) and [software-aesthetic.coordinated.md](software-aesthetic.coordinated.md).

## Reframe before patching

Prefer repairing the model of the problem over output-forcing patches. Before adding a special case, name the invariant it preserves and check whether a simpler representation removes the need entirely. A chain of "if this input then force that output" clauses is a design smell unless each branch follows from an explicit domain rule.

Look for *code judo* moves — reframings that preserve behavior while deleting whole branches, layers, or concepts. The goal is to make the change feel inevitable in hindsight, not to polish the existing structure.

## Map before drilling

When entering an unfamiliar area, build a higher-level map first — relevant modules, callers, and invariants in the project's vocabulary — before drilling into a specific function. Deep inspection follows the map, not the other way around.

## Hypotheses over traces

Treat assumptions as hypotheses until checked. Form a hypothesis that satisfies known invariants, then check it against the trace — not the reverse. Replaying the observed trace without a hypothesis produces patches, not understanding.

## Complexity accounting

Before adding a concept, abstraction, or special case: name what problem it solves, name the invariant it must preserve, and ask whether a simpler representation makes it unnecessary. Three similar instances is better than a premature abstraction.

## Scope discipline

Do not add features, refactor, or introduce abstractions beyond what the task requires. A bug fix does not need surrounding cleanup; a one-shot operation does not need a helper. Design for the problem at hand, not hypothetical future requirements.
