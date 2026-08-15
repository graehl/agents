---
name: harsh-review
disable-model-invocation: true
description: Deliberately strict structural + correctness audit — finds deleting reframes, spaghetti, leaky abstraction, and logic that breaks on a concrete input. Use when the user invokes /harsh-review, $harsh-review, or asks for a harsh/deep structural review rather than a routine merge gate; covers code diffs and, via a dedicated pass, agent-instruction and doc diffs.
---

# Harsh review

First classify each changed artifact, not the diff as a whole: **code** walks § Review pass; **prose** (agent instructions, topic docs, READMEs, manuals, plans) walks § Non-code review pass — so a mixed diff walks both, each over its own files, and a code project's doc files get judged as documents, not as code. A prose-only review reads `~/agents/topics/design-thinking.md`, skips both software-aesthetic docs, and skips § Review pass and § Correctness entirely — the non-code pass is self-contained.

A review touching code reads all three docs that hold the definitions and reasoning, first:
- `~/agents/topics/software-aesthetic.md` — universal per-unit rules
- `~/agents/topics/software-aesthetic.coordinated.md` — project-wide rules (apply when the project follows them; see `AGENTS.user.md` ask-once)
- `~/agents/topics/design-thinking.md` — the problem-approach principles behind the structural calls

The terms below — *deleting reframe*, *spaghetti*, *leaky abstraction*, *divergence point*, *duplicate fix*, *seam* — are used in their `GLOSSARY.md` sense.

Review past the diff. Judge the structure the change lands in, and ask whether the problem had a better approach from the outside. Always check for a deleting reframe: a restructuring that deletes whole branches, layers, or concepts while preserving behavior. Demanding a restructure on every merge just churns the system, so the procedure tags each item *blocker* or *advisory*; raise advisories with conviction but weigh the fix against the churn of blocking now. Exception: when the diff already opens the relevant *seam*, fixing it now is cheap and the bar to block drops.

## Range and scope

Resolve what to review before classifying. The reviewed diff runs from the parent of the first reviewed commit to the last. No argument reviews HEAD alone: `HEAD^..HEAD`. A single commit (`harsh-review SHA1`) reviews just that commit: `SHA1^..SHA1`, not `SHA1` to HEAD. An inclusive start — "SHA1 to SHA2", "from SHA1 on" — counts SHA1 as first reviewed, so it diffs `SHA1^..SHA2` (or `SHA1^..HEAD`). "Since SHA1" instead treats SHA1 as the baseline and reviews what came after: `SHA1..HEAD`. A bare `since` — nothing after it — takes that baseline from the marker left by the previous review (§ Review marker): `<its line 1>..HEAD`. When the marker is missing, or its commit no longer exists in this repo (rebased or gc'd away), say so and ask for a baseline rather than substituting one; when the range is empty, report that nothing has landed since the last review and stop. A subject-shaped request ("recent commits on X") defaults to a ~48h lookback; widen only if nothing matches, until commits are found.

Immediately resolve both diff endpoints to full SHAs and hold them fixed. Form the artifact range key `<base12>..<end12>` with `git rev-parse --short=12 <base>` and `git rev-parse --short=12 <end>`; record the full SHAs inside each artifact. A moving ref such as `HEAD` may select an endpoint, but it never appears in an artifact key or substitutes for the frozen end after review starts.

Read the range's commit messages before reviewing (`git --no-pager log --no-ext-diff --reverse <range>`): they are the map (`design-thinking.md` § Map before drilling) for a range review, carry the author intent that makes each diff legible, and show how clean the history is — which decides whether you can cut coherent chunks or must slice mechanically.

Coverage is the deliverable (`design-thinking.md` § An audit is scoped by its target): review the whole resolved range, never a self-chosen high-risk subset declared done. When the range is too large to reason about comfortably in one context, a serial fold is *mandatory* (§ Review records and serial fold) — chunk it in commit order and carry findings forward, do not trim; a range that fits comfortably needs no fold ceremony. Either way deliver the whole range, or stop explicitly with a named coverage gap the next review resumes.

Output invariant: never propose a fix already present at the review's end state (HEAD, for the usual review that ends there). A bug introduced in one in-range commit and resolved by a later one needs no remediation — proposing one duplicates a landed fix, leaving two green fixes for one invariant that the next reader can't untangle. Judge resolution once, at delivery, over the collected findings — not per commit as you go, since the fix may sit in a commit you haven't reached and guessing HEAD-state mid-review is unreliable. If the review's end `B` is behind HEAD (a historical range, or HEAD moved during a long review), scan `git diff B..HEAD` over the still-open findings to drop any already landed — reading those commits only to suppress landed fixes, not reviewing them. Reason about in-between states freely and use them: a fix that is incomplete or right only by accident is still worth flagging, as harden/make-deliberate — a different deliverable than re-fixing, so the invariant holds.

## Review marker

Line 1 of `.harsh-review` at the repo root remains the full-SHA high-water-mark up to which review is *delivered and closed*, contiguously from history. Bare `since` reads only line 1 (`<it>..HEAD`); later lines are free-form context (date, range). Before writing review records, create their root-level directory with `mkdir -p harsh-review`. Keep the marker and directory untracked: add any missing `.harsh-review` and `/harsh-review/` patterns to `$(git rev-parse --git-common-dir)/info/exclude` — the per-clone exclude, not the committed `.gitignore`.

On delivering a review, advance the marker to the end actually covered whenever the review closes the prefix contiguously — its reviewed range reaches back to the marker or earlier and runs unbroken to a new end past it. That is the clean extension (base equals the marker) and equally an overlap-and-extend re-review whose base precedes the marker (e.g. `last 5 commits` re-including the marker commit). Only a review starting *past* an unreviewed gap, or one wholly behind the marker, delivers while leaving the marker untouched: it must never jump commits no review has covered. A high-water-mark, not a cursor of the last review.

## Review records and serial fold

Every non-empty review persists the same left-fold. A range too large to reason about comfortably in one context must be chunked in commit order; the discomfort is the trigger, not a line count. A smaller range may complete in one pass, but still writes its working record instead of leaving the review only in session context.

### Advisory range claim

Before touching a range record, list fresh active sessions and stop if another session already claims the same range key or either canonical range file. Otherwise register `agentctl active "HARSH-REVIEW: <range>" "harsh-review/<range>.accum" "harsh-review/<range>.verdict.md"`, then list again to catch a simultaneous claim. On a race, the oldest claim wins (canonical session id breaks an exact mtime tie); every loser marks its entry `DONE` and leaves the review files untouched. This is an advisory same-range lock, not a filesystem lock. Refresh the claim during a long fold and mark it `DONE` only after delivery or an explicit stop.

A review uses one untracked root marker and two records under `harsh-review/`:
- `.harsh-review` — the contiguous-delivery marker (§ Review marker).
- `harsh-review/<range>.accum` — the working review. Its header records the full base and end SHAs, `folded-through` SHA, coverage state, and, for a second opinion, the prior backup pair's paths; its body carries evidence and running findings under `open` and `resolved-in-range`. Write findings here as the review proceeds, including for a one-pass review, so a fresh agent can resume from this file alone. The fold is serial under the advisory range claim.
- `harsh-review/<range>.verdict.md` — the final user-facing findings for exactly that frozen range and the honest coverage achieved.

### Same-range second opinion

When the requested frozen range already has both canonical files, treat a request to review it again as an independent second opinion. After acquiring the advisory range claim and before beginning the review, choose the next free integer `N` from filenames alone and mechanically move the pair to `harsh-review/<range>.prior-N.accum` and `harsh-review/<range>.prior-N.verdict.md`; verify both backups exist, then create a fresh canonical accumulator whose header names that pair by path only. Do not open, grep, summarize, or otherwise inspect either prior file during this phase. If only one prior file exists, stop and report the incomplete history rather than overwrite it.

Complete the new review independently, including an independent provisional verdict in the fresh accumulator, before opening any prior backup. **Time to reconcile now** is the first phase allowed to read the immediately previous pair. Reconcile item by item against the reviewed tree in the fresh accumulator: preserve prior findings that still hold, add new findings, and record a concrete reason for every prior finding dropped or reclassified. Write the canonical verdict as the clean merged findings, without reviewer-comparison annotations or prior/current labels. Prior backups remain review history and are never resume candidates.

Fold one chunk per pass: read the accumulator, review `folded-through..<next cut>` (cut at a green/feature boundary read from the commit messages), carry findings forward as `open` — a later chunk may mark one resolved on sight — advance `folded-through`, and repeat. Before freezing a new target for bare `since`, look for an unfinished `harsh-review/<marker12>..<end12>.accum` whose recorded full base equals the marker and which has no matching verdict; resume its recorded end rather than silently retargeting it to a newer `HEAD`. If more than one such accumulator exists, name them and ask which to resume. A single-commit review (`harsh-review SHA`) is always allowed mid-fold: it uses its own range-keyed files and never touches the in-flight fold.

Finalize and retain: decide remediations under the output invariant (§ Range and scope) over the accumulator's `open` findings. Before communicating any finding to the user, write `harsh-review/<range>.verdict.md`; include the full frozen range, coverage, and final blocker/advisory findings, or an explicit no-findings result. Only after that write succeeds may the marker advance (§ Review marker), to the full end if complete or the honest prefix SHA if the verdict names a coverage gap. Keep both range files as uncommitted review history; except for the mechanical same-range backup above, do not archive, rename, or delete the accumulator on delivery.

The session response links the verdict with its project-relative path as the link text and does not duplicate the findings inline. For a same-range second opinion, also state concise noticed-and-resolved annotations for any valid prior finding the independent pass missed and any valid finding it newly found; keep those reviewer-comparison annotations out of the verdict. If the verdict cannot be written, do not claim delivery or advance the marker.

## Review pass

Walk these in order; skip any with no real hit — a short review is success, not a form left unfilled.

1. **Deleting reframe** — is there a reframing that deletes complexity instead of rearranging it? Repeated conditionals or mode flags usually signal a missing model; push for the model, not a tidier chain. *(advisory; blocker at a seam)*
2. **File growth** — did an already-large file grow? If the diff touches a seam where splitting is cheap, split now. *(advisory; blocker at a seam)*
3. **Spaghetti** — ad-hoc conditionals or special cases bolted onto unrelated flows belong behind one abstraction or module. *(blocker)*
4. **Misplaced logic** — feature logic in a shared path, or logic in the wrong layer; copy-paste across callers that wants a shared helper — unless the copies are *divergence points* meant to evolve apart. *(blocker)*
5. **Unearned abstraction** — leaky abstractions, pass-through wrappers, one-offs duplicating a canonical helper, nullable/type-erasure churn that hides an invariant. *(blocker)*
6. **Duplicate fix** — the diff remediates a defect the tree already handles: a second guard on one invariant, a caller workaround shadowing a callee fix, the same clamp in two layers. Independent authors patch their own projections, so resemblance to an existing fix is a finding, not a coincidence — name the owning invariant's best fix site, keep that one fix, and delete the rest, which may mean keeping the diff's and removing the incumbent. Deliberate layered defense, each layer with its own contract, is not a hit. (The § Range and scope output invariant is this same duty aimed at the reviewer's own proposals.) *(blocker)*
7. **Boundary shape** — at an input/output boundary the diff touches, name the concrete same-outcome alternative from the aesthetic docs rather than only flagging the mess. *(advisory)*
8. **Sequencing** — independent work serialized, or partial-update patterns that can leave state half-applied (`software-aesthetic.md` § Sequencing and partial state). *(advisory)*
9. **Caller impact** — when the diff touches a shared facility, sweep call sites outside the diff (`design-thinking.md` § Sweep callers when a contract moves): is every caller updated or aware, and does the new behavior hold under each one's assumptions? Matters most where no CI battery catches the ripples. *(blocker)*
10. **Glossary conformance** — bring code and the project's `GLOSSARY.md` closer together. Does a new symbol, comment, log phrase, doc heading, or option name reuse the established term, or coin a synonym/paraphrase for a concept the glossary already names? Did the diff introduce a cross-cutting concept that deserves a glossary row (or a topic doc) and didn't get one? Did it rename or change a concept such that an existing row is now stale? Name the existing term to adopt, or the row to add/fix. Cheap when the diff already touches the naming; do not block a correct change purely on vocabulary. *(advisory; blocker at a seam)*
11. **Change-narrating comments** — a comment that describes the diff or the conversation that produced the code rather than the code as it stands: "with X removed" where no X appears, "now using Y instead", "as we discussed", "added for the Z flow". It narrates a before/after the committed source doesn't contain, so the next reader hits "why mention X when no X is here?" (`software-aesthetic.md` § Comments). Such comments are legitimate only in code presented for discussion, planning, or alignment — never in committed source; flag every one for deletion. *(blocker)*

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

Correctness bar, replacing execution simulation, judged per role. Agent instructions and topic docs: each kept rule is load-bearing (`AGENTS.global.md` § Load-bearing instructions), no trigger promises detail its target lacks, and worked examples that stop a weaker agent reasoning around a rule are preserved. Reader-facing docs (README, manual, tutorial): every claim matches the current artifact — commands run, paths exist, options are spelled as implemented — and the content serves the named audience's first read.

## Approval bar

The changed paths read as near-provably correct (for prose-only, the non-code correctness bar), and the diff does not worsen the structure it touches. Be direct and demanding — do not soften a structural blocker into a suggestion.
