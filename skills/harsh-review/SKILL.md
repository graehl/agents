---
name: harsh-review
description: Deliberately strict structural + correctness audit — hunts code-judo simplifications, spaghetti, leaky abstraction, and logic that breaks on a concrete input. For a deep review, not a routine merge gate.
disable-model-invocation: false
---

# Harsh review

This skill operationalizes three docs as reviewer obligations:
- `~/agents/topics/software-aesthetic.md` — universal per-unit rules
- `~/agents/topics/software-aesthetic.coordinated.md` — project-wide rules (apply when the project follows them; see `AGENTS.user.md` ask-once)
- `~/agents/topics/design-thinking.md` — the problem-approach principles behind the structural calls

Read all three first. They hold the definitions and the reasoning; this file is the review procedure, not a summary of them. The terms below — *code judo*, *spaghetti*, *leaky abstraction*, *divergence point*, *seam* — are used in their `GLOSSARY.md` sense.

Review past the diff. Judge the structure the change lands in, and ask whether the problem had a better approach from the outside. Hunt actively for code-judo: a restructuring that deletes whole branches, layers, or concepts while preserving behavior.

**Calibration.** Demanding a restructure on every merge just churns the system, so separate the bars:
- **Blocker** — correctness failures, behavioral regressions, and changes that actively make the surrounding code harder to work in.
- **Advisory** — simplification and decomposition opportunities: push with conviction as pressure toward a better state, not as a gate. Exception: when the diff already opens the relevant *seam*, fixing it now is cheap, so the bar to block drops.

## Review pass

Walk these in order; skip any with no real hit — a short review is success, not a form left unfilled.

1. **Code judo** — is there a reframing that deletes complexity instead of rearranging it? Repeated conditionals or mode flags usually signal a missing model; push for the model, not a tidier chain. *(advisory; blocker at a seam)*
2. **File growth** — did an already-large file grow? If the diff touches a seam where splitting is cheap, split now. *(advisory; blocker at a seam)*
3. **Spaghetti** — ad-hoc conditionals or special cases bolted onto unrelated flows belong behind one abstraction or module. *(blocker)*
4. **Misplaced logic** — feature logic in a shared path, or logic in the wrong layer; copy-paste across callers that wants a shared helper — unless the copies are *divergence points* meant to evolve apart. *(blocker)*
5. **Unearned abstraction** — leaky abstractions, pass-through wrappers, one-offs duplicating a canonical helper, nullable/type-erasure churn that hides an invariant. *(blocker)*
6. **Boundary shape** — at an input/output boundary the diff touches, name the concrete same-outcome alternative from the aesthetic docs rather than only flagging the mess. *(advisory)*
7. **Sequencing** — independent work serialized, or partial-update patterns that can leave state half-applied. *(advisory)*

## Caller impact

When the diff touches a shared facility, check call sites outside the diff:
- Does the change break or surprise an existing caller?
- Does the new behavior hold under every call site's assumptions, not just the ones the author had in mind?
- If the contract moved — signature, semantics, errors, performance — is every caller updated or aware?

This matters most where no CI battery catches the ripples and the facility sits at a boundary many callers cross.

## Correctness

For each meaningful change, demand evidence:
- Simulate execution through the key paths. Does the logic hold? Are edge cases handled, or provably unreachable?
- What tests cover this — the real contract, or only the happy path?
- For a non-trivial path with no test, ask for one or for an explicit argument that it is unnecessary.

Flag logic that reads fine but breaks on a concrete input: an empty collection, an off-by-one, a race, a caller assumption nothing enforces.

## Approval bar

The changed paths read as near-provably correct, and the diff does not worsen the structure it touches. Everything beyond that is advisory — raise it with conviction, but weigh the fix against the churn of blocking now.

## Tone

Direct and demanding. Do not soften a structural blocker into a suggestion.
