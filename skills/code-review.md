---
name: code-review
description: Strict maintainability review focused on structural simplification, abstraction quality, and spaghetti growth. Use for a deep code quality audit or unusually harsh review.
disable-model-invocation: true
---

# Code Quality Review

This review enforces:
- `~/agents/topics/software-aesthetic.md` — universal per-unit rules
- `~/agents/topics/software-aesthetic.coordinated.md` — project-wide rules (active by default for graehl's projects)
- `~/agents/topics/design-thinking.md` — problem-approach principles that inform structural judgments

Read all three if not already loaded. The rules below operationalize those preferences as reviewer obligations.

Look beyond the diff: consider the adjacent structure the diff touches and ask whether there was a better way to approach the problem from the outside. Actively search for code-judo moves — restructurings that preserve behavior while deleting whole branches, layers, or concepts.

**Scope calibration.** This review surfaces structural opportunities that narrow diff-reading misses. Demanding restructuring as a precondition for every merge increases total system churn. Distinguish accordingly:

- **Hard blockers:** correctness failures, clear behavioral regressions, and structure violations where the diff actively makes the codebase harder to work in.
- **Advisory flags:** code-judo opportunities, decomposition suggestions. Surface with conviction as pressure toward a better state, not a gate — unless the author is already touching a natural seam, where the cost of fixing it now is low and the blocker threshold drops.

## Hard Rules

1. **No file bloat.** Flag when the diff substantially enlarges an already large file; ask whether it should be split before merging, especially if the diff touches a seam where splitting is cheap.

2. **No spaghetti.** Ad-hoc conditionals, mode flags, or special-case branches bolted onto unrelated flows belong behind a dedicated abstraction, state machine, or separate module.

3. **Delete complexity, don't rearrange it.** Do not approve a refactor that rearranges complexity without reducing it. If a simpler model is visible, push for it — often the move is reframing the model so the conditionals disappear rather than cleaning them up. At input/output boundaries, actively suggest concrete same-outcome alternatives: on the input side: early-exit validation (guard at the top, assume valid below) or liberal-accept normalization (absorb variation at the boundary, with or without a warning); on the output side: fix+warn (detect problems at the output stage, fix and warn rather than failing or silently misbehaving) — but only where the system's error-handling philosophy and use case call for defensive recovery rather than hard failure.

4. **No unearned abstraction.** Flag leaky abstractions, pure pass-through wrappers, bespoke one-offs duplicating canonical helpers, or indirection/type-erasure/nullable churn that obscures real invariants. Named predicates and booleans that express a domain concept in the codebase's vocabulary are welcome even when the implementation is trivial.

5. **Logic in the canonical layer.** Feature logic leaking into shared paths, logic in the wrong module/layer, or copy-paste where a shared helper would serve multiple callers, are blockers. Exception: duplication is correct when the copies are *divergence points* — each expected to evolve independently. The smell to reject is collapsing distinct use cases into one shared function distinguished by mode/flag arguments.

6. **Atomic and parallel where it simplifies.** Flag sequential orchestration of independent work, or partial-update patterns that leave state half-applied.

## Key Questions

For each meaningful change:

- Is there a code-judo move — a reframing that deletes complexity rather than rearranges it?
- Did a file grow substantially? Does the diff touch a seam where splitting is cheap?
- Are repeated conditionals signaling a missing model? If so, push for the model, not a tidier condition chain.
- Did the diff add indirection or unconstrained types that obscure a real invariant?

## Caller Impact

When the diff touches a shared facility, check callers outside the diff:

- Does the change break or surprise any existing caller?
- Does the new behavior hold under every call site's assumptions, not just the ones the author had in mind?
- If the contract changed (signature, semantics, error behavior, performance), are all callers updated or aware?

This check matters most when there is no CI battery catching ripple failures and when the facility sits at a layer boundary crossed by many callers.

## Correctness

For each meaningful change, demand evidence of correctness:

- Read the code and simulate execution through the key paths. Does the logic hold? Are edge cases handled or provably unreachable?
- What tests cover this? Are they testing the actual contract or just the happy path?
- If no test exists for a non-trivial path, ask for one or an explicit argument for why it is unnecessary.

Flag logic that looks plausible on first read but breaks under a concrete input, a race, an empty collection, an off-by-one, or a caller assumption that is not enforced.

## Approval Bar

Hard bar: logic reads as near-provably correct on the changed paths, and the diff does not actively worsen the structure it touches. Structural improvements beyond the hard bar are advisory — flag them with conviction, but weigh the cost of demanding them now against the churn of blocking the change.

## Tone

Direct and demanding. Do not soften structural blockers into suggestions.
