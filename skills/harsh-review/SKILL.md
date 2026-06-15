---
name: harsh-review
description: Deliberately strict structural + correctness audit — finds deleting reframes, spaghetti, leaky abstraction, and logic that breaks on a concrete input. Use when the user invokes /harsh-review, $harsh-review, or asks for a harsh/deep structural review rather than a routine merge gate; covers code diffs and, via a dedicated pass, agent-instruction and doc diffs.
---

# Harsh review

First classify each changed artifact, not the diff as a whole: **code** walks § Review pass; **prose** (agent instructions, topic docs, READMEs, manuals, plans) walks § Non-code review pass — so a mixed diff walks both, each over its own files, and a code project's doc files get judged as documents, not as code. A prose-only review reads `~/agents/topics/design-thinking.md`, skips both software-aesthetic docs, and skips § Review pass and § Correctness entirely — the non-code pass is self-contained.

A review touching code reads all three docs that hold the definitions and reasoning, first:
- `~/agents/topics/software-aesthetic.md` — universal per-unit rules
- `~/agents/topics/software-aesthetic.coordinated.md` — project-wide rules (apply when the project follows them; see `AGENTS.user.md` ask-once)
- `~/agents/topics/design-thinking.md` — the problem-approach principles behind the structural calls

The terms below — *deleting reframe*, *spaghetti*, *leaky abstraction*, *divergence point*, *seam* — are used in their `GLOSSARY.md` sense.

Review past the diff. Judge the structure the change lands in, and ask whether the problem had a better approach from the outside. Always check for a deleting reframe: a restructuring that deletes whole branches, layers, or concepts while preserving behavior. Demanding a restructure on every merge just churns the system, so the procedure tags each item *blocker* or *advisory*; raise advisories with conviction but weigh the fix against the churn of blocking now. Exception: when the diff already opens the relevant *seam*, fixing it now is cheap and the bar to block drops.

## Range and scope

Resolve what to review before classifying. The reviewed diff runs from the parent of the first reviewed commit to the last. A single commit (`harsh-review SHA1`) reviews just that commit: `SHA1^..SHA1`, not `SHA1` to HEAD. An inclusive start — "SHA1 to SHA2", "from SHA1 on" — counts SHA1 as first reviewed, so it diffs `SHA1^..SHA2` (or `SHA1^..HEAD`). "Since SHA1" instead treats SHA1 as the baseline and reviews what came after: `SHA1..HEAD`. A subject-shaped request ("recent commits on X") defaults to a ~48h lookback; widen only if nothing matches, until commits are found.

Output rule: review the net effect over the range, not each commit in isolation. A bug introduced in one in-range commit and fixed by a later one is already resolved — do not report it. Reason about in-between states freely, but flag an in-range issue only where its resolution is missing, incomplete, or ineffective by the end of the range.

## Review pass

Walk these in order; skip any with no real hit — a short review is success, not a form left unfilled.

1. **Deleting reframe** — is there a reframing that deletes complexity instead of rearranging it? Repeated conditionals or mode flags usually signal a missing model; push for the model, not a tidier chain. *(advisory; blocker at a seam)*
2. **File growth** — did an already-large file grow? If the diff touches a seam where splitting is cheap, split now. *(advisory; blocker at a seam)*
3. **Spaghetti** — ad-hoc conditionals or special cases bolted onto unrelated flows belong behind one abstraction or module. *(blocker)*
4. **Misplaced logic** — feature logic in a shared path, or logic in the wrong layer; copy-paste across callers that wants a shared helper — unless the copies are *divergence points* meant to evolve apart. *(blocker)*
5. **Unearned abstraction** — leaky abstractions, pass-through wrappers, one-offs duplicating a canonical helper, nullable/type-erasure churn that hides an invariant. *(blocker)*
6. **Boundary shape** — at an input/output boundary the diff touches, name the concrete same-outcome alternative from the aesthetic docs rather than only flagging the mess. *(advisory)*
7. **Sequencing** — independent work serialized, or partial-update patterns that can leave state half-applied (`software-aesthetic.md` § Sequencing and partial state). *(advisory)*
8. **Caller impact** — when the diff touches a shared facility, sweep call sites outside the diff (`design-thinking.md` § Sweep callers when a contract moves): is every caller updated or aware, and does the new behavior hold under each one's assumptions? Matters most where no CI battery catches the ripples. *(blocker)*
9. **Glossary conformance** — bring code and the project's `GLOSSARY.md` closer together. Does a new symbol, comment, log phrase, doc heading, or option name reuse the established term, or coin a synonym/paraphrase for a concept the glossary already names? Did the diff introduce a cross-cutting concept that deserves a glossary row (or a topic doc) and didn't get one? Did it rename or change a concept such that an existing row is now stale? Name the existing term to adopt, or the row to add/fix. Cheap when the diff already touches the naming; do not block a correct change purely on vocabulary. *(advisory; blocker at a seam)*

## Correctness

For each meaningful change, demand evidence:
- Simulate execution through the key paths. Does the logic hold? Are edge cases handled, or provably unreachable?
- What tests cover this — the real contract, or only the happy path?
- For a non-trivial path with no test, ask for one or for an explicit argument that it is unnecessary.

Flag logic that reads fine but breaks on a concrete input: an empty collection, an off-by-one, a race, a caller assumption nothing enforces.

## Non-code review pass

For prose artifacts; self-contained, same blocker/advisory discipline and stance as the code pass. Before walking the items, name each doc's role and audience — agent instructions, topic doc/contract, root README, user manual, tutorial, API reference, developer plan — and judge against that role: a tutorial wants the worked example a reference doc would cut, a README orients a first-time reader, a plan captures decisions. Generated artifacts (e.g. API docs built from source) are reviewed at their source, not the generated output. Walk in order; skip items with no real hit.

1. **Reframing** — can a restructure delete whole rules, caveats, or sections while preserving the steered behavior? Repeated special-case caveats around one rule signal a missing concept; push for the concept. *(advisory; blocker when the diff already rewrites that section)*
2. **Doc growth** — did an already-long doc grow? When the diff touches the section anyway, split it or move slow-path detail behind a read-trigger now. *(advisory)*
3. **Misplaced content** — content at the wrong level or in the wrong role: global vs. project instructions, topic doc vs. task file, inline boot rule vs. behind a read-trigger, tutorial material in a reference doc, plan material in a README. *(blocker)*
4. **Unearned vocabulary or indirection** — a coined term where established wording exists, or a pointer/layer that doesn't pay for the lookup it costs. *(blocker)*
5. **Citer impact** — sweep every doc, read-trigger, and skill that cites a changed claim. When the diff compresses content behind a pointer, verify block by block that the target actually holds the displaced content — "the owning topic has it" is a per-block claim, not a per-file one. *(blocker)*
6. **Glossary conformance** — new wording reuses the established `GLOSSARY.md` term rather than coining a synonym; a new cross-cutting concept gets a row; a changed concept doesn't leave a stale row. *(advisory)*

Correctness bar, replacing execution simulation, judged per role. Agent instructions and topic docs: each kept rule is load-bearing (`AGENTS.md` § Load-bearing instructions), no trigger promises detail its target lacks, and worked examples that stop a weaker agent reasoning around a rule are preserved. Reader-facing docs (README, manual, tutorial): every claim matches the current artifact — commands run, paths exist, options are spelled as implemented — and the content serves the named audience's first read.

## Approval bar

The changed paths read as near-provably correct (for prose-only, the non-code correctness bar), and the diff does not worsen the structure it touches. Be direct and demanding — do not soften a structural blocker into a suggestion.
