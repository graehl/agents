---
name: harsh-review
description: Deliberately strict structural + correctness audit — hunts code-judo simplifications, spaghetti, leaky abstraction, and logic that breaks on a concrete input. Use when the user invokes /harsh-review, $harsh-review, or asks for a harsh/deep structural review rather than a routine merge gate.
---

# Harsh review

Review procedure for the three docs that hold the definitions and reasoning. Read them first:
- `~/agents/topics/software-aesthetic.md` — universal per-unit rules
- `~/agents/topics/software-aesthetic.coordinated.md` — project-wide rules (apply when the project follows them; see `AGENTS.user.md` ask-once)
- `~/agents/topics/design-thinking.md` — the problem-approach principles behind the structural calls

The terms below — *code judo*, *spaghetti*, *leaky abstraction*, *divergence point*, *seam* — are used in their `GLOSSARY.md` sense.

Review past the diff. Judge the structure the change lands in, and ask whether the problem had a better approach from the outside. Hunt actively for code-judo: a restructuring that deletes whole branches, layers, or concepts while preserving behavior. Demanding a restructure on every merge just churns the system, so the procedure tags each item *blocker* or *advisory*; raise advisories with conviction but weigh the fix against the churn of blocking now. Exception: when the diff already opens the relevant *seam*, fixing it now is cheap and the bar to block drops.

## Review pass

Walk these in order; skip any with no real hit — a short review is success, not a form left unfilled.

1. **Code judo** — is there a reframing that deletes complexity instead of rearranging it? Repeated conditionals or mode flags usually signal a missing model; push for the model, not a tidier chain. *(advisory; blocker at a seam)*
2. **File growth** — did an already-large file grow? If the diff touches a seam where splitting is cheap, split now. *(advisory; blocker at a seam)*
3. **Spaghetti** — ad-hoc conditionals or special cases bolted onto unrelated flows belong behind one abstraction or module. *(blocker)*
4. **Misplaced logic** — feature logic in a shared path, or logic in the wrong layer; copy-paste across callers that wants a shared helper — unless the copies are *divergence points* meant to evolve apart. *(blocker)*
5. **Unearned abstraction** — leaky abstractions, pass-through wrappers, one-offs duplicating a canonical helper, nullable/type-erasure churn that hides an invariant. *(blocker)*
6. **Boundary shape** — at an input/output boundary the diff touches, name the concrete same-outcome alternative from the aesthetic docs rather than only flagging the mess. *(advisory)*
7. **Sequencing** — independent work serialized, or partial-update patterns that can leave state half-applied. *(advisory)*
8. **Caller impact** — when the diff touches a shared facility, check call sites outside the diff: does the change break or surprise an existing caller; does the new behavior hold under every call site's assumptions; if the contract moved (signature, semantics, errors, performance), is every caller updated or aware? Matters most where no CI battery catches the ripples and the facility sits at a boundary many callers cross. *(blocker)*
9. **Glossary conformance** — bring code and the project's `GLOSSARY.md` closer together. Does a new symbol, comment, log phrase, doc heading, or option name reuse the established term, or coin a synonym/paraphrase for a concept the glossary already names? Did the diff introduce a cross-cutting concept that deserves a glossary row (or a topic doc) and didn't get one? Did it rename or change a concept such that an existing row is now stale? Name the existing term to adopt, or the row to add/fix. Cheap when the diff already touches the naming; do not block a correct change purely on vocabulary. *(advisory; blocker at a seam)*

## Correctness

For each meaningful change, demand evidence:
- Simulate execution through the key paths. Does the logic hold? Are edge cases handled, or provably unreachable?
- What tests cover this — the real contract, or only the happy path?
- For a non-trivial path with no test, ask for one or for an explicit argument that it is unnecessary.

Flag logic that reads fine but breaks on a concrete input: an empty collection, an off-by-one, a race, a caller assumption nothing enforces.

## Approval bar

The changed paths read as near-provably correct, and the diff does not worsen the structure it touches. Be direct and demanding — do not soften a structural blocker into a suggestion.
