# Change and delivery details

> Slow-path rationale and mechanics for gated actions, shared-worktree edits, commits, and implementation quality.

Consult the matching named section before a gated or destructive action, a
history rewrite, an ambiguous shared-worktree edit, or when a compact commit or
quality rule needs its worked mechanics. `AGENTS.global.md` retains the binding
rules and wins on conflict.

## Big-effect command gate

Big-effect commands fall in two tiers.

**Full gate record** — for irreversible or shared-state actions: push,
force push, deploys, migrations, dependency upgrades, destructive
filesystem commands, and file edits that wholly replace user-written
content. Stop and produce the record below before running one.

**Light check** — for local commits and amends (especially doc-only): no
formal record, just a one-line confirmation that the staged scope is
intended and, for an amend, that prior commit-message content is
preserved. A local commit is cheaply reversible, so the full ceremony is
not worth it. Amending an already-pushed commit is still local (light
check); the force-push it then requires gets the full record.

Exception to both tiers: recently created scratch/log/tmp files the user
has not been shown — a filename appearing in an approval does not mean the
user knows the file.

The full gate record:
1. State the action and why it is gated.
2. List required checks as bracketed tags, each stating the current fact
   that satisfies or blocks it, e.g. `[wip] unrelated work present;
   command is path-limited to README.md`.
3. For multi-step gated operations, prefix each later action with the
   matching tag(s).
4. Show the exact command.
5. Quote exact policy only for destructive, forceful, ambiguous, or
   unusually risky actions, or on request.
6. Do not proceed if any required check is missing or ambiguous.

**Force-push form.** A justified, gated force push uses `git push
--force-with-lease --force-if-includes`, never bare `--force`/`-f`. The
lease refuses the push when the remote branch moved since your last
fetch — catching work a peer pushed that you would otherwise clobber —
and `--force-if-includes` (git ≥2.30) keeps a stray fetch from silently
refreshing the lease ref out from under that check. Drop to bare
`--force` only when the lease form genuinely cannot express the intent,
and say why in the gate record. Mechanics and the explicit-ref lease
form are in `topics/commits.md`.

**Pre-push attribution scan (`[no-attrib]`).** Every push, PR
creation, or publish-script invocation carries a `[no-attrib]` check
in its gate record: scan the outgoing commit messages — and any
message argument the publish command takes — for AI-attribution
markers before running it:

```bash
git log --format='%H %B' @{u}..HEAD |
  rg -i 'co-authored-by|generated with|noreply@|🤖'
```

These shapes cover the trailers and banners agent harnesses inject
(Claude, Copilot, Codex, Gemini, …) without matching vendor names in
ordinary prose — and without matching the mandated
`Contributing-model:` trailer (§ Commits), which is sanctioned
provenance and is never stripped. No match (rg exits 1) satisfies
the check. Inspect
each hit — prose merely mentioning a marker passes. Every real
marker is stripped before the push proceeds — every
`Co-Authored-By:` trailer regardless of the author it names, and
every generated-with banner. Stripping is mandatory, not a
keep-or-strip decision to escalate. Strip by the exact SHA the
scan's `%H` column names — amend a marked tip; for a deeper commit
use the SHA-targeted message filter in `topics/commits.md` — never a
blind pattern sweep over the range, and run the whole chain under
the rewrite lock (§ Amends). A marker discovered on already-pushed
history gets stripped there too — amend/reword, then the gated
force-push form; when that history sits on a shared or default
branch others pull from, the strip still happens but waits for the
explicit user go the shared-branch force-push ban requires.
`scripts/pre-push-no-attrib`, installed machine-locally as a repo's
`pre-push` hook, refuses marked pushes mechanically (trailer-block
parsing, so prose mentions pass); where present it backstops this
check, but the scan stays required — hook installs don't travel with
clones. With no upstream configured, substitute the range
actually being pushed.

When a review step is part of the same request as a push or deploy,
sequence as: review → fix → push. Do not push first and review after.

The bracketed-tag style is encouraged for other self-imposed gates; it is
required only for the full gate record.

## Shared-workdir discard ban

In a shared workdir, never run repo-wide work-discarding commands —
`git reset --hard`, `git clean`, broad `git checkout`/`git restore` of
tracked paths, or scripted equivalents that overwrite the worktree. When
unstaged user or peer edits may exist this is the wrong tool, not merely a
gated one. In particular do not reach for it to line up or repair a mistaken
commit, amend, merge, rebase, cherry-pick, pull, or push-prep step — "so I
can land my amend against the right commit" is exactly how a peer's
unsaved hour gets destroyed.

Beyond discarding, the same ban covers shared-worktree git moves that
capture or disrupt others' work, absent an explicit user request:
staging others' changes into your commit (`git add -A`/`git add .`, and
bare `git stash` — both sweep up everyone's dirty files; scope with a
pathspec), bypassing hooks (`git commit --no-verify`), moving the
worktree's HEAD out from under peers (`git switch`, `gh pr checkout`, or
any backward `git reset` — even soft/mixed to reorganize your own commits;
see *Amends*), and force-pushing a shared or default branch.

Stashing: dirty files are not presumed yours — "stash my changes" means
the named, path-scoped form `git stash push -m '<why>' -- <paths>`,
as safe as editing those files, never bare `git stash`. Restore with
`stash apply` and verify before any `drop`; `stash pop` auto-drops your
only backup the moment the merge textually succeeds, so it has no place
in a shared workdir. `stash drop`/`clear` are discard commands under
this ban. Reviewing or inspecting
a branch or PR never requires moving HEAD — use `gh pr diff`, `git
--no-pager diff main...BRANCH`, or a dedicated `git worktree add`, not
a checkout.

To repair history or index state, preserve the worktree and take a
non-discarding path: inspect status/reflog, make a temporary commit of
your own changes (or a pathspec-scoped stash, never bare `git stash`),
use a separate worktree, or revert with a new commit.
Run a discard command only when the user explicitly requests that exact
operation after being told it can delete uncommitted shared work, and even
then narrow it to named paths.

When discarding worktree changes to a path, use the explicit `git checkout
-- <path>` / `git restore <path>` form, never `git checkout <path>` — `--`
keeps git from mistaking a pathspec for a branch. Shared-workdir projects
should launch harnesses via `agent-guarded`, which shims `git` to refuse
these commands while a live `.agentctl/active` peer exists; if `AGENT_GUARD`
is unset, warn once that the launch is unguarded. Contract, bypass surface,
and deployment: `topics/agent-guard.md`.

## Never reach system-wide

No operation that takes `/` as its scope/root (`find /`, `grep -r /`, `du
/`, …) without explicit user permission — scope every action to the
task's real paths. A specific absolute path (`/home/…`, `/tmp/…`) is fine:
this bans `/` as an operation's root, not the leading slash of normal paths.
Unprompted whole-system reach is a judgment failure even when read-only and
harmless.

## Ancillary workdir hygiene

When working in an ancillary worktree or scratch checkout, do not
put it on reboot-cleared storage (`/tmp`, tmpfs); use durable
storage — a sibling directory of the primary workdir, on the same
filesystem, is a good default. Before transferring content back to the primary workdir,
verify source and destination branches match, and stash or
formally commit (or amend) first — a committed state is the only
safe transfer unit. Do not rely on default agent caution here.

## Hot-reload / live-interpreted projects

When a project's running process re-reads source on save (dev server,
nodemon, watcher-driven build, live REPL/notebook session), a related
series of edits must not leave the live tree in a state that crashes
that process between writes. The watcher observes each write; the
contract covers the sequence of observed states, not only the final
one.

Choose any mechanism that satisfies the contract — make each
intermediate state self-consistent, pause/stop the watcher across the
batch, stage and transfer together. Before applying a batch built
against earlier reads, verify the target files have not drifted from
those reads.

## Pre-edit re-Read and parallel-worker noticing

Re-Read a file before the next Edit when, since your last Read, a peer
agent or a direct user edit could plausibly have intervened — across a
context compaction, a multi-turn exchange, or returning to a file you
Read earlier. One Read then several rapid Edits is fine; this covers the
slower gaps. (Re-reading because compaction dropped the content from your
window is a separate, unconditional need — you can't edit text you can't
see.)

Branch on peer presence, re-checked at the point of caution — not on a
belief formed earlier in the session. Peers finish, so a "peers present"
reading goes stale, and the per-file re-Read ceremony below keeps being
charged long after you are actually solo. The check is one cheap command,
not a fact to carry: `find .agentctl/active -maxdepth 1 -type f -mmin -70`
answers "any peers here?" in one call, and `agentctl others <session-id>`
answers it by exit code (0 alone, nonzero peers present) with your own
entry excluded, so the re-check needs no parsing — prefer it. (Or the
user just says a peer joined.)
- Solo (no fresh non-self entry, none announced): the only path left is a
  direct user edit, covered by the reciprocal convention (AGENTS.user.md
  — the user announces joins and mid-impl hand-edits). Skip the slow-gap
  re-Read; re-Read only on an announcement or post-compaction content
  loss.
- Peers present: re-Read the specific file just before editing it. That
  is the fast, file-specific, up-to-date overlap check — cheaper and more
  current than a lock, and it surfaces a peer's change directly. Narrow
  by the peer's `scope:` line when present: only files within their claim
  need it.

Surprise is itself a trigger. An edit op failing unexpectedly (an
`old_string` that no longer matches), or git dirty / staged / commit
content you did not produce, means your model of the tree is stale — run
the peer-check before proceeding, even when you believed you were solo.
This catches a peer, or your own drift, without an announcement, so the
solo skip never rests on memory alone.

On detected divergence, pause and report what you were about to change;
do not revert, overwrite, or auto-reconcile. Same goal as a peer: leave
the worktree intact. Different goal: retry the Edit against the new
content.

## Edit mechanism discipline

For any change that could or should be an ordinary edit, the
structured edit tool (`Edit`/`apply_patch`) is the mechanism. Never
substitute `sed`/`perl`/`python`/here-doc in-place rewrites for a
normal edit in order to dodge an approval prompt, a permission mode
(e.g. 'Ask'), or a temporarily blocked edit tool. Choosing a more
error-prone mechanism to slip past a gate is forbidden — the gate
exists precisely for the change you are trying to make. A blocked
edit tool means the edit needs approval or a fix, not a quieter route
around it.

If the normal edit tool cannot be used — permission mode, a sandbox
or environment error, a broken helper — first try to solve it
head-on: request the edit through the prompt, or fix the environment
fault. If it cannot be solved head-on, raise it to the user once and
stop; this is exactly the execution-context limitation you state
plainly (see *Execution-context limits*), not one you engineer
around with riskier tooling. A giant `perl -0pi -e q~...~` block
replacement of a multi-line function — brittle, unverifiable, silent
on a whitespace drift — is never the right answer to "the edit tool
asked for permission."

Shell text transforms remain the right tool when they genuinely are:
mechanical rewrites fanned across many files, `clang-format-diff`,
codemods. The line is intent — a bulk transform that is awkward as
hand-edits is fine; a single targeted edit re-expressed as a shell
substitution to avoid a prompt is not.

### Edit anchors: copy, don't compose

`old_string` is a verbatim substring of the file, not a description of
the region. Every part of it is literal — indentation, trailing spaces,
and the position of every line break. Compose it from what you expect
the file to say and the edit fails; the usual retry re-composes the same
guess and fails again.

- **Copy from text you can currently see verbatim.** *Pre-edit re-Read*
  above covers peer and user edits; the gap it leaves is a write you
  made indirectly — a subagent, a formatter, a codemod, a script —
  whose result you never read. Re-Read before anchoring there. Your own
  prior `Edit` needs no re-Read: its `new_string` is visible verbatim.
- **Never re-indent an anchor or start one mid-line.** A Read's
  soft-wrapped display is not the file's line structure. An anchor that
  begins at a wrap point, or whose leading whitespace you supplied
  rather than copied, cannot match — and switching spaces for a tab on
  the retry is a guess, not a diagnosis.
- **Anchor on the smallest span that is unique, not the largest you can
  reproduce.** A 40-line anchor is 40 chances to mis-copy, not more
  safety.
- **On "Found N matches", extend the anchor upward** to the nearest
  unique line — the enclosing `it("...")`, `describe`, `function`, or
  heading. Adding more of the identical body just re-fails.
- **Escape sequences in source (`\0`, `\n`, `\t`, `\\`) are two
  characters in the file; emit two.** A literal control byte compiles
  and behaves identically, so tests stay green, but it makes the file
  binary to `rg`/`grep` — which then silently skips it, leaving a hole
  in every later search — and breaks every later anchor that spells the
  escape correctly.
- **After a second failure on one file, stop varying the anchor:** Read
  the exact line range and copy from it.

## Reader-facing summaries

In any summary written for a reader — commit subjects and bodies, status
lines, run-log headlines, notes, and prose — do not import tool-internal
jargon as if it were shared vocabulary. A term that names a library's
internal mode, a flag, or an implementation detail raises a question the
rest of the sentence has usually already answered; either drop it or define
it in-line, and prefer the phrase the reader already understands over the
one that is precise only to whoever wrote the code. Worked instance: a
commit subject "consensus (pairwise) not paired self-chrF" — here "paired"
named a scoring library's element-wise mode and only prompted "what is
paired?"; "self-chrF (vs all-pairs consensus)" carried the whole point.
This is reader-facing wording discipline, not a ban on precision: define the
internal term when the reader needs it, just do not assume it.

## Commits

Subject <=65 chars and scannable for `git log --oneline`. Wrap body prose
manually at 71 columns — a visual rule, not greedy fill: preserve bullets,
hanging indents, aligned continuations, short tables, and ASCII diagrams
even when that leaves a short line. Exceed 71 only for unavoidable long
tokens. Use body bullets when items are numerous or complex, prose when
short. No `Co-Authored-By`; no links to git-ignored content (e.g.
`tasks/`).

### Commit proactively

Checkpoint your own finished work in a local commit rather than leaving
it uncommitted and waiting for permission — local commits are
light-check, reversible, and strengthen resume-from-live-state. Push
stays gated; in a shared worktree, pathspec-scope every commit (never
`git add -A`) so you capture only your own work, not peer or user WIP.
Whether to amend the previous commit or add a new one is a judgment
call — permitted either way while unpushed, mandated in neither
direction. A project may narrow this: a single-commit-per-ticket review
workflow can require amend and gate any additional commit on explicit
permission, and that project rule governs there.

### Commit messages

Trivial commits can be subject-only (the `Contributing-model:`
trailer still applies). A non-trivial message is a reviewer on-ramp:
write for a fresh human about to inspect the diff, with none of the
implementation conversation in mind. Lead with why, the resulting decision,
and outcome; account for every non-trivial file group at that level. Include
main user decisions and non-obvious rejected approaches, exclude secrets and
unrelated iteration churn, and use `Known coverage gaps:` for meaningful
uncovered risks. Do not enumerate tests run; the diff and CI carry that.

Before first review, make a brevity pass toward one printed page or less.
Remove action-by-action "did X, then Y" detail and keep only the shortest what
that orients the reviewer; a trivial small-scope change may still name every
change. If implementation detail deserves a durable record but would crowd
the message, condense it under the journal publication rules (§ Delegation)
into `topics/journals/<task-or-topic>.md`; otherwise discard it.

When work is largely governed by a committed `topics/<name>.md` doc, start
the body just after the subject with that doc's relative path as the
onboarding path for new readers. That topic must be self-contained for the
fresh human reviewer before they inspect the changes: it cannot rely on the
session or implementation being familiar. Keep `Topic:` trailers for
series/search membership, and prefer expanding the topic doc for lasting
context over lengthening the message.

Split thematically unrelated changes into independent commits. Open-ended
commit latitude ("make as many commits as you want", "commit at your own
pace", "split however you like") means unrelated large themes should land
separately; closely related changes still belong together.

Read `topics/commits.md` before writing a non-trivial commit message,
amending, splitting or otherwise rewriting history, deciding correction
commit vs. amend, or relying on topic-trailer, Gerrit, coverage-gap, or
message-preservation mechanics.

#### Amends

When amending, keep the subject, preserve existing message content except
deliberate corrections, and prefer amend over a local correction commit;
never amend after a PR has opened. In a shared worktree, first check active
peers; with any active peer, no history rewrite at all — not amend, not
rebase, and not a `git reset` that rewinds the branch to split, squash, or
reorder what you believe is your tip commit. The scope is peer presence,
not `HEAD` ownership: a peer may commit at any moment, so no `HEAD` check
closes the race — the rewind can land below a freshly-landed commit you
don't own and silently orphan or absorb it. Make a follow-up commit, use a
separate worktree, or block with `agentctl alone`. With no active peer,
verify `HEAD` is the intended commit and is your own current-session work;
then splitting it with `git reset` + recommits is as free as amending.
Repair bad history without discarding the worktree. Full procedure,
including Gerrit `Change-Id` and message-preservation mechanics, lives in
`topics/commits.md`.

**Advisory rewrite lock.** A multi-command history rewrite — an amend
chain, rebase, split, or attribution strip — must stay solo for its
whole duration, not just at its first command: take the floor with
`agentctl alone <session-id> -b "REWRITE: <what>"`, whose `REWRITE`
banner prefix on your active entry is the lock, and clear it by
rewriting your banner (or `DONE`) when the chain ends. The respect
side binds every session: before any commit, even a routine one,
check for a fresh non-self entry whose line 1 starts with `REWRITE`
(`find .agentctl/active -maxdepth 1 -type f -mmin -70 -exec grep -l
'^REWRITE' {} +`); one present means history is mid-surgery — wait
for it to clear rather than committing into the moving range. A
single one-command amend keeps the lighter rule above (peer check, no
lock). Banner schema: `topics/agentctl.md`.

#### Topic trailers

A commit in a related series gets one or more `Topic: <string>` trailers.
Use the basename of the relevant `topics/<topic>.md`, copy it verbatim
across the series, and use multiple trailers when a commit spans topics.
The trailer marks thread membership, not merely that the diff touched a
topic doc; details live in `topics/commits.md`.

#### Contributing-model trailer

Every commit an agent authors carries a `Contributing-model: <name>`
trailer — an intentional abbreviation of the model name
(`claude-fable-5` → `Fable`, `claude-opus-5` → `Opus 5`,
`gpt-5.6-sol` → `5.6-Sol`); vendor or harness names (`Pi`,
`Copilot`), emails, and links are not welcome. Recover the id per
the harness supplement's transcript check; models misreport their
own names. One trailer per contributing model, additive across
models and sessions, never duplicated. This is deliberate,
user-mandated provenance for fair effort attribution — not an
AI-attribution marker: the `[no-attrib]` scan does not match it,
and it is never stripped. Details: `topics/commits.md`.

## Code quality

### Anti-slop implementation

Do not pile on permissive fallbacks to make the current trace succeed.
Unrequested recovery, precondition softening, broad exception swallowing,
warn-and-continue, or proceeding on partial state are acceptable only when
they preserve the documented contract and are part of the requested
behavior. If the outcome needs a missing precondition, establish it
explicitly or fail with a clear, actionable error — do not silently
reinterpret bad input or bypass checks.

### Backward compatibility

Default to preserving observable contracts — exported/public APIs, CLI
flags, wire and serialization formats, persisted schemas, anything an
out-of-repo caller depends on. Drop a compatibility shim without asking
only when the surface is internal and you have swept and updated all
in-repo callers; otherwise ask. Don't add new back-compat scaffolding
speculatively.

Record a consequential or non-obvious decision — a deliberate break of
an observable contract, or a shim kept because a specific consumer
needs it — in the project's `topics/backward-compat.md` (create on
first need), one entry per decision:
`YYYY-MM-DD <surface> — <decision>; <why>`. Routine internal removals
with all callers swept need no entry. No SHA in the entry: commit it
with the change it records, and `git blame`/`git log` on the ledger
recovers the exact commit when you need provenance. Grep the ledger for
the surface before asking a compat question you may have already
answered; append when you take a new one.

### Vendoring third-party code

When copying someone else's skill/script/subtree into a repo to keep
(rather than co-develop), **vendor** it — copy the files in and commit
them — over a submodule or a symlink to an external clone; the latter is
machine-local state that breaks a plain clone and dodges review of code an
agent executes. Pin to the **exact upstream commit SHA** (not a branch or
tag) and write a `<dest>/VENDORED.md` recording upstream URL/subpath/SHA,
license (or that none exists), per-file hashes, and a **Local changes**
section documenting every divergence from upstream — that section is the
only record a re-sync won't overwrite. Use `vendor-skill` (`~/bin`, spec
in `topics/helper-scripts.md`) so the SHA-pin and provenance are
automatic. Full rationale and procedure: `topics/vendoring.md`.

### Feature validation

When adding or enabling a feature that affects runtime, memory, model
quality, or experimental conclusions, plan an explicit on/off comparison
unless the effect is mechanically obvious and low risk. Scope it to the
blast radius: a smoke-scale timing check for narrow plumbing; a recorded
contrastive run (or a task note deferring it) for research-facing changes.

### Perf measurement

Before running local performance measurements — benchmarks, ratchet
suites, load simulations, profiling — read `topics/perf.md`
(repo-local first, else `~/agents/topics/perf.md`). Two duties bind
even if the read is deferred: every process the run spawns is yours
to kill and verify gone (sweep before, teardown on failure paths,
survivor check before session end — orphaned measurement processes
have made a user's live server unusable), and a number from a host
whose contention and variance you have not measured is diagnostic,
not ratchet-grade.

### Fix the invariant, not the symptom

A request to "change this thing I see and don't like" — a visible defect, a
screenshot annotation, "make this stop happening" — names a *symptom*, which
is a projection of an underlying code/organization invariant. Fix at the
invariant, not the projection: before patching, name the contract the symptom
violates (what must be true that currently isn't), then fix there.

Block the brittle local patch — a special-case, an extra conditional, a CSS
override, regexp-scrubbing generated output into shape, suppressing the
output, hide-at-this-width, a permissive fallback —
that makes *this* symptom vanish without restoring the contract; it just
recurs at the next projection. Tells you are patching, not fixing: the
third-plus fix in one area hits a different surface symptom of the same
constraint; the fix special-cases an instance rather than changing the shared
mechanism; a new element is rendered *beside* a container instead of as an
instance of it, so it can't inherit the container's contract (see
`~/agents/topics/software-aesthetic.md` § Structure).

Worked instances. A UI "wrong across rounds" → derive the invariant +
current falsifier and make it the judge, not the screenshots
(`~/agents/topics/ui-verification.md` § *Closing a spec-vs-behavior gap*;
fit/overlap layout is a measured allocator, not breakpoint tiers,
`~/agents/topics/functional-layout.md`). A "make this trace stop erroring" →
establish the missing precondition or fail clearly, don't soften or swallow
it (*Anti-slop implementation* above).

**Duplicate fixes.** Multi-author trees collect independent fixes for one
defect, each author patching their own projection — a second guard on one
invariant, a caller workaround shadowing a callee fix. In any review, a
fix resembling one already in the tree is a finding, not a coincidence:
usually neither sits at the owning invariant, or one is dead. Name the
best fix site, keep that one fix (whichever author's), remove the rest;
deliberate layered defense with per-layer contracts is not a duplicate.

### UI tweak result captures

A request to tweak, fix, or restyle a web app's UI — layout, spacing,
control/toolbar placement, flow — is confirmed only by rendered browser
captures of the result: 1920×1080 desktop, plus a phone width when the
project targets mobile. Capture after the change lands, actually look at
each image, and check it against the request before claiming success —
the capture exists to catch your own wrong spatial/aesthetic guess,
which otherwise ships mis-spaced layouts as "done". Cite capture paths
in the final response. Mid-implementation captures are optional.
Protocol and mechanics: `topics/ui-testing.md`, repo-local first, else
`~/agents/topics/ui-testing.md`.

### Adjacent gaps: capture, don't chase or drop

A code-quality defect you notice adjacent to your work — a UI glitch,
lint, a failing or flaky test, a small structural wart — but are not
fixing now because it is out of scope must not evaporate into a chat
comment that dies with the session. Record it as a committed
`gaps/<slug>.md` entry (create `gaps/` when first needed), and remove that
file in the commit that fixes the gap. Fix in place instead only when the
fix is cheap *and* in scope — the seam is already open — and then as its
own commit, not folded into unrelated work. The capture has a read
side: when the repo has `gaps/`, glance at it when starting work in
an area — a filed gap is known context there, and its fix may now be
in scope. Format, lifecycle, and the distinctions from `tasks/`,
`topics/`, and `on-deck/` live in `gaps/README.md`.

### Ideal coding

See `~/agents/topics/software-aesthetic.md` for the full shared aesthetic —
naming, comments, structure, abstraction, and input/output contracts — and
`~/agents/topics/design-thinking.md` for how to approach a change (reframe
before patching, map before drilling, caller sweeps, scope discipline). The
points below are either not in those docs or are worth repeating here:

- When a change moves a shared facility's contract (signature, semantics,
  errors, performance), sweep call sites beyond the diff and confirm each
  caller's assumptions still hold. Same duty for prose: a section other
  docs cite or a read-trigger points at is a shared facility.
- Before introducing a new general facility, consult
  `GLOSSARY.md` (contribution rules in `~/agents/topics/glossary.md`);
  keep single-use facilities close to their use.
- Keep run logs greppable: tag every line of a phase with the phase name
  (`WARMUP: ...`), rather than bracketing a span (`[start WARMUP]` /
  `[end WARMUP]`) or relying on indentation.
