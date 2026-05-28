# Software aesthetic

> Shared criteria for how code should look, feel, and be structured — applied both when writing code and when reviewing it.

Topic: software-aesthetic

Rules here are universal — each applies to any individual code unit regardless of project context. Rules that pay off only when observed project-wide live in [software-aesthetic.coordinated.md](software-aesthetic.coordinated.md); apply those to greenfield projects or ones that already follow them.

## Core

The ideal piece of code is the shortest conventional readable form that correctly expresses the contract. Clever tricks are welcome on hot paths when they measurably improve size or speed; avoid them elsewhere.

## Naming

Names should evoke known domain terms or patterns so the code is navigable without full context. A name evoking the concept beats a comment explaining it. Named predicates and booleans that express a domain concept in the codebase's vocabulary are welcome even when the implementation is trivial. Avoid names that force the reader to look through them immediately — `Manager`, `Handler`, `Processor`, `Helper`.

## Comments

Write no comments by default. Add one only when the WHY is non-obvious: a hidden constraint, a subtle invariant, a workaround for a specific bug. Never explain what the code does; well-named identifiers already do that. One short line maximum — no multi-paragraph docstrings or multi-line comment blocks.

## Structure

- Delete complexity rather than rearrange it. A reframing that makes conditionals disappear is better than one that centralizes them — often this means reframing the model, not the conditions (see *code judo*).
- Prefer repairing the model of the problem over output-forcing patches. A chain of "if this input then force that output" clauses is a design smell unless each branch follows from an explicit domain rule.
- Decompose at seams — natural boundaries where behavior can be altered without editing surrounding code.
- Spaghetti (ad-hoc conditionals, mode flags, special-case branches scattered across unrelated flows) belongs behind a dedicated abstraction, state machine, or separate module.
- Feature logic should not leak into shared paths.
- Single-use facilities belong close to their use.

## Abstraction

An abstraction earns its keep when callers do not need to understand its internals to use it correctly (not *leaky*) and when it names a stable concept rather than just renaming a call. Pass-through wrappers and bespoke one-offs duplicating canonical helpers are indirection without abstraction.

Three similar lines is better than a premature abstraction. Duplication is correct at *divergence points* — copies expected to evolve independently. The smell to reject is collapsing distinct use cases into one shared function distinguished by mode/flag arguments.

## Input/output contracts

At input boundaries, prefer early-exit validation: guard at the top, assume valid below.

## Size and performance

A file that has grown too large to hold in a reader's head at once is a candidate for decomposition at the nearest seam. On hot paths, avoid needlessly quadratic work — use precomputation or verified library-contract assumptions to reach n log n or better; know whether memory or compute is the bottleneck before spending scratch space to save time. Treat redundant computation as a design bug: reuse cached/prefetched/intermediate work and repair only the states that need repair.
