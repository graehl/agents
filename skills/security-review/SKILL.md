---
name: security-review
description: Security-only audit of release snapshots against the project's stated security stance. Use for /security-review, $security-review, or a requested security review; reads optional topics/security.md, keeps .security-review plus security-review/ range records, and reports concrete compromise paths rather than general correctness or hardening advice.
---

# Security review

Audit only security compromises against the project's stated stance. Retain
frozen-range resolution, range-keyed records, a serial fold, and independent
second-opinion discipline, but do not run structural, aesthetic, or general
correctness checklists. A correctness defect is in scope only when it yields a
concrete security impact.

## Security stance

At each review point, read the project-root `topics/security.md` from that
snapshot in full when it exists. Do not create it merely to run this review.
Treat its protected assets, threat actors and capabilities, trust boundaries,
guarantees, accepted risks, and explicit non-goals as the controlling stance
for that snapshot unless a higher-precedence project instruction or the user
says otherwise. Record whether the file existed and, when it did, its SHA-256
for that review point in both records.

When the topic is absent, infer no maximal-hardening policy. Recover only
security promises stated elsewhere in the project and the concrete trust
boundaries the reviewed system exposes. Conventional security expectations may
make an evident boundary legible, but a preference for stronger defense is not
a finding.

Every finding identifies:

- the stance clause, project promise, or trust-boundary contract being broken;
- the attacker-controlled input or capability and required preconditions;
- the path from that input to the sensitive effect;
- the resulting confidentiality, integrity, availability, or authority impact;
- end-state evidence at the affected review point.

Investigate or omit an item missing that chain. Do not report generic hardening,
style, maintainability, performance, or correctness advice; an unreachable
theoretical weakness; or a risk the stance explicitly accepts. A silent
expansion beyond an accepted risk's stated boundary is still a finding.

While tracing security paths, you may freely file concrete non-security quality
defects you encounter under the project's normal gap convention. This is
capture, not a second audit: do not search for them, widen review coverage to
classify them, or include them in the security accumulator or verdict.
Deduplicate and follow the project's gap format. At the end of a completed
review, name every gap filed during it after the verdict link.

## Upstream freshness

When the review end is selected by a moving ref — a bare invocation, bare
`since`, or a range ending at HEAD or a branch tip — sync before freezing
endpoints; an end the user pinned to an explicit SHA reviews as requested. The
upstreams are the remote branches project instructions name for keeping the
reviewed branch current (e.g. `~/ya` tracks main on both its kzahel and graehl
remotes), else the branch's configured `@{u}`; with neither, skip this step.
Fetch them (a failed fetch is reported and reviews the local tree), then:

- up to date or strictly ahead: proceed;
- behind with a clean fast-forward — one fetched head descends from local HEAD
  and contains every other named upstream head, no active peer sessions, and
  the worktree does not block it: `git merge --ff-only <that head>`, then
  review the updated tree;
- behind otherwise — local commits not upstream, upstream heads with no single
  fast-forward target, active peers, or a worktree refusal: stop and ask
  whether to merge, rebase, or review locally, unless the request already
  chose. Reviewing locally audits the tree as it stands, and the response
  names the upstream(s) it is behind.

## Range, review points, and scope

Resolve what to review first. The selected Git range runs from the parent of the
first selected change to the final selected endpoint. No argument reviews the
security state at `HEAD`, using the preceding release tag as its change-map
baseline when one exists. A single commit (`security-review SHA1`) audits the
snapshot at that commit. An inclusive start — "SHA1 to SHA2" or "from SHA1 on"
— includes SHA1, so its change map is `SHA1^..SHA2` (or `SHA1^..HEAD`). "Since
SHA1" treats SHA1 as the baseline and maps `SHA1..HEAD`. A bare `since` takes
its baseline from line 1 of `.security-review`; when the marker is missing or
its commit no longer exists, say so and ask for a baseline rather than choosing
one.

Immediately resolve both endpoints to full SHAs and hold them fixed. Form the
artifact range key `<base12>..<end12>` from their 12-character abbreviations.
Record the full SHAs in each artifact. A moving ref may select an endpoint but
never appears in an artifact key or replaces the frozen end.

The audited units are **review points**, not commits: every project release tag
whose peeled commit lies on the ancestry path in `(base, end]`, plus the frozen
end. If the end is tagged, that is one review point rather than two. Use the
project's established release-tag convention; if several tag families make
release identity materially ambiguous, ask which family governs. Record each
tag name and peeled commit SHA. Multiple tags for one release commit are one
review point with all names retained.

Audit the complete tree at each review point. Intervening commits and their
messages are only a map for locating changed attack surfaces and understanding
intent. A vulnerability introduced and removed between review points is not a
finding. A compromise present in a tagged release remains historically relevant
even if a later point fixes the code; report it as released-and-resolved and
ask whether persistent consequences such as exposed data, forged authority, or
credential rotation remain. Never propose a code fix already present at the
latest reviewed state.

Coverage is the requested review-point set. Review every selected point, or
stop with an explicit named coverage gap and resume path. When the set is too
large to reason about comfortably in one context, use the serial fold below;
never substitute a self-selected high-risk subset and call the audit complete.

## Review marker

Line 1 of `.security-review` at the repository root is the full-SHA
high-water-mark through which requested review points have been delivered and
closed contiguously. Bare `since` reads only line 1; later lines may record the
date, range, or latest reviewed release names.

Before writing records, create root-level `security-review/`. Keep the marker
and directory untracked by adding any missing `.security-review` and
`/security-review/` patterns to `$(git rev-parse --git-common-dir)/info/exclude`,
never the committed `.gitignore`.

Advance the marker to the frozen end when the review closes every requested
review point in an unbroken extension from the prior marker, including an
overlap-and-extend re-review whose base precedes it. A review that begins after
an uncovered release point or lies wholly behind the marker leaves it unchanged.
The marker never jumps an unaudited requested release snapshot.

## Review records and serial fold

Every non-empty review persists the same left-fold. Before touching a range
record, list fresh active sessions and stop if another session claims the same
range key or either canonical file. Otherwise register
`agentctl active "SECURITY-REVIEW: <range>" "security-review/<range>.accum"
"security-review/<range>.verdict.md"`, then list again. On a race, the oldest
claim wins (canonical session id breaks an exact mtime tie); losers mark their
entry `DONE` and leave the files untouched. Refresh a long-running claim and
mark it `DONE` only after delivery or an explicit stop.

A review uses:

- `.security-review` — the contiguous-delivery marker.
- `security-review/<range>.accum` — the working review. Its header records full
  endpoints, per-point security-stance sources/hashes, ordered review points,
  `folded-through`, coverage, and any prior backup pair. Its body carries
  evidence and findings under `open`, `released-and-resolved`, and
  `dismissed`, sufficient for a fresh agent to resume.
- `security-review/<range>.verdict.md` — the final findings for exactly the
  frozen range and review-point set, with honest coverage.

Fold one review point per pass: read the accumulator, inspect that snapshot and
the change map since the previous point, carry still-open findings forward,
record released-and-resolved compromises without proposing a landed code fix,
advance `folded-through`, and repeat. A small range may complete in one pass but
still writes its accumulator.

Before freezing a new target for bare `since`, look for an unfinished
`security-review/<marker12>..<end12>.accum` whose full base equals the marker
and which has no verdict. Resume its frozen target rather than retargeting to a
newer `HEAD`; if several qualify, name them and ask which to resume. A
single-snapshot review remains allowed during a fold and uses its own files.

### Same-range second opinion

When both canonical files already exist, acquire the advisory claim, choose the
next free integer `N` from filenames alone, and mechanically move the pair to
`security-review/<range>.prior-N.accum` and
`security-review/<range>.prior-N.verdict.md`. Verify both backups exist, then
start a fresh accumulator naming their paths. Do not open, grep, summarize, or
otherwise inspect either prior file until the independent review has recorded
its provisional verdict. If only one canonical file exists, stop rather than
overwrite incomplete history.

At **Time to reconcile now**, read the immediately previous pair and reconcile
each prior finding against the reviewed snapshots and current stance. Preserve
valid findings, add new ones, and record a concrete reason for every dropped or
reclassified item in the accumulator. The canonical verdict contains the clean
merged result without prior/current annotations. The session response briefly
notes valid findings missed by the independent pass and valid new findings.

Finalize over the latest reviewed snapshot and any historically tagged
compromises. Before communicating a finding, write the verdict with full frozen
range, per-point stance sources/hashes, review points, coverage,
blocker/advisory findings,
released-and-resolved items, or an explicit no-findings result. Only then may
the marker advance. Retain all range files as uncommitted review history.

The response links `security-review/<range>.verdict.md` using that
project-relative path as link text and does not duplicate findings inline. If
the verdict cannot be written, do not claim delivery or advance the marker.

## Security pass

For each review point, map changed trust boundaries before drilling into files.
Sweep callers, configuration, deployment surfaces, serializers, and policy docs
outside the diff when they participate in the same security path. Then trace
only applicable compromise classes:

1. authority or identity accepted without the stance's required authentication,
   authorization, scoping, freshness, or revocation;
2. attacker-controlled data reaching an interpreter, query, command, path,
   template, URL fetch, parser, or deserializer with unintended authority;
3. protected data or secrets disclosed, retained, logged, cached, or crossed
   into a weaker trust domain;
4. integrity or availability lost through confused-deputy behavior, unsafe
   defaults, partial security state, races, rollback, replay, or resource
   exhaustion within the stated threat model;
5. a required isolation, cryptographic, dependency, update, provenance, or
   fail-closed mechanism weakened or bypassed;
6. implementation, configuration, documentation, and `topics/security.md`
   disagreeing about the end-state guarantee.

Simulate a concrete adversarial input through each plausible path and inspect
the protection's negative tests. Tests that cover only benign behavior are not
evidence for the security contract. If exploitability depends on an unknown,
name and verify it when cheap; otherwise an advisory may retain that precise
uncertainty only when the rest of the compromise chain is concrete.

Classify a demonstrated reachable compromise within the stated threat model as
a **blocker**. Classify a bounded, lower-impact or explicitly uncertain stance
violation as an **advisory** only when it still has a concrete attacker-to-impact
path. Do not fill categories that have no hit.

## Approval bar

The latest requested release state has no demonstrated blocker against the
stated stance, every requested review point has honest coverage, and any
released-and-resolved compromise names its potentially persistent consequence.
A no-findings verdict means only that this scoped review found no compromise; it
is not a certification that the project is secure.
