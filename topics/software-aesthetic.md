# Software aesthetic

> Shared criteria for how code should look and be structured — applied both when writing it and when reviewing it.

Topic: software-aesthetic

Every rule here is universal: it applies to a single unit of code regardless of project. Rules that only pay off when a whole project observes them live in [software-aesthetic.coordinated.md](software-aesthetic.coordinated.md).

## Core

The ideal piece of code is the shortest conventional, readable form that correctly expresses its contract. Cleverness earns its place only on a hot path where it measurably buys size or speed; anywhere else it costs the next reader more than it saves.

## Naming

A name should carry a known domain concept, so the reader navigates the code without holding all of it in their head — the right name does the work a comment otherwise would. This extends to predicates and booleans: name the concept they decide, even when the body is a single comparison. Avoid names a reader has to look straight through to learn anything: `Manager`, `Handler`, `Processor`, `Helper`.

## Comments

Write none by default. Add one only for a *why* the code cannot show on its own — a hidden constraint, a subtle invariant, a workaround for a specific bug. Never restate what the code does; the names already say it. One line; no docstring essays.

## Structure

- Delete complexity instead of relocating it. A reframing that makes the conditionals vanish beats one that gathers them somewhere tidier — and usually that means fixing the model, not the branches (*code judo*; see [design-thinking](design-thinking.md)).
- Decompose at *seams* — natural boundaries where behavior can change without editing the surrounding code.
- Put *spaghetti* — ad-hoc conditionals, mode flags, special cases threaded through unrelated flows — behind one abstraction, state machine, or module.
- Keep feature logic out of shared paths, and single-use helpers next to their use.
- An element that must obey a container's contract belongs *inside* that container's representation, as an instance of it — not as a bespoke sibling rendered beside it. A sibling can't inherit the contract (e.g. a mini-sidebar's "collapsed → icon-only"), so it forces per-instance patching: the special case the invariant was meant to delete. Add to the existing representation in a form compatible with it; don't stuff a new element into adjacent space.

## Abstraction

An abstraction earns its keep on two conditions: callers can use it correctly without knowing its internals (it is not *leaky*), and it names a stable concept rather than just renaming a call. Pass-through wrappers and one-offs that re-implement a canonical helper are indirection wearing the costume of abstraction.

Duplication is correct at *divergence points* — copies you expect to evolve apart. The real smell is the opposite move: folding genuinely distinct cases into one function steered by mode or flag arguments.

## Input boundaries

Guard at the top and assume valid below: prefer early-exit validation where input enters. (The output side — normalizing on the way in, repairing on the way out — is a project-wide commitment; see [coordinated](software-aesthetic.coordinated.md).)

## Size and performance

A file too large to hold in your head is a candidate for splitting at its nearest seam. On a hot path, refuse needlessly quadratic work — precompute, or lean on a known library contract, to reach n log n or better — and learn whether memory or compute is the bottleneck before you trade one away for the other. Treat recomputation as a design bug: reuse cached, prefetched, or intermediate results, and repair only the state that actually changed.
