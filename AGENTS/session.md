# Session continuity details

> Slow-path rationale and mechanics for session state, handoffs, active-session coordination, resume, and scheduled prompts.

Consult the matching named section when creating a handoff, coordinating an
active session, resuming work, or processing a scheduled prompt.
`AGENTS.global.md` retains the binding rules and wins on conflict.

## Session management

Session continuity is primarily resume-by-session-id plus live state
(active sessions, `tasks/*.md`, run metadata). `/hi` is an optional explicit
recovery operation, mainly worth reaching for after a disconnect or corrupted
resume; compaction alone does not invoke it. Recover prior context only on a
greeting or explicit resume signal — a fresh, specific request is independent.

`tasks/*.md` files track per-task direction, coordination, acceptance
notes, and unfinished session state. Whether `tasks/` is git-ignored is
the customization point: ignored (the default here) means task files are
private working state — never commit them and stay branch-agnostic;
tracked means the feature-branch workflow (committed task files, branch
per task). The default scope-less boot handoff is named by `tasks/ROOT` (a
one-line pointer holding its filename); it does not choose what current work
maintains. Update it only when explicitly establishing a new bare-boot target.
Prefer a committed `topics/` doc for durable conclusions, contracts,
and project-facing knowledge, and reach for a git-ignored `tasks/` file
**last** — one test decides: would committing this plausibly help a repo
collaborator? If yes, commit it durably. `tasks/` is the parking spot
for what fails that test — *our* session management of no collaborator
interest: private direction-setting, coordination, an active-work
scratchpad, and save/resume of plans or progress that only we will pick
back up — plus anything that must stay private (auth, secrets,
confidential context) and so cannot be committed at all. **But** when you
commit an *incomplete* shared artifact, its resumable status (what is
done, what is pending, the coverage/grounding cutoff) passes the test —
an uncommitted status would let the partial result mislead — so commit
that status *with the artifact* (a status banner, cutoff line, or
"what's left" section), never only in `tasks/`. (In the tracked-`tasks/`
variant those files are themselves the committed collaborator artifact,
so the last-resort test does not apply.) Read the
selected task when resuming. On believed completion, append a dated
status note with the relevant commit(s) and one line of evidence; if the
task file has inline subtasks, make it a section listing each subtask's
status. Judge each task file in isolation — no recursing into linked
subtask files.

For implementation or bugfix work, search `tasks/*.md` when that directory
exists, and cite the relevant file(s) in planning and conclusion. Task
files should cross-reference relevant `topics/*.md`.

Dated progress entries — a `tasks/*.md` or `docs/tactical/` status or
plan note, a journal append — name the contributing model, in the same
short form as the `Contributing-model:` commit trailer (§ Commits), so
effort can be fairly attributed when several models or sessions touch
one task. Topic docs carry no model identity. Prefer recording the
session id over hand-counted effort stats (turns, user chars):
transcripts make those mechanically derivable later, while live counts
are unreliable across compaction and multi-session commits.

### Handoff audience

A handoff or persistent plan — a `tasks/*.md` file, a `.bearings.md`, or any
ad-hoc "write me a handoff/plan" doc — has exactly
two readers: the user, and a fresh agent of similar capability. Never
write down to a lesser reader. "Similar capability" means peer skill with
zero shared context: the receiver can re-derive reasoning from the same
artifacts but was not in the room, so it carries none of this session's
working memory. Use this model to decide what the handoff contains; do
not recite it inside one — an `Audience:` line that names these readers
recites the rule instead of applying it, wasting the opening on meta the
readers don't need.

Both halves of that cut against the default tendency to flatten a handoff
into basic narration:

- Preserve the compiled understanding the session paid for — ruled-out
  hypotheses, the load-bearing constraint, "don't try X, it dead-ends at
  Y," the actual crux. It is the highest-value, least-recoverable content
  and the first thing a flattened handoff drops.
- Restate context by default. Omit it only to the extent it lives in
  specific pointed-to material the receiver will actually open (a named
  doc, a cited code section, a linked prior report) — not merely because
  a peer could in principle reconstruct it from the repo.

This governs resume/handoff artifacts. Outward-facing reports keep their
own reader model — e.g. `topics/progress-report.md` writes for a
non-delving manager or peer org — so do not apply this pin to them.

When the work uses a durable advisor/oracle co-session that is resumed and
grown rather than recreated for each review, the handoff records its serving
logical relation and incumbent. Immediately after an optional `/goal X` line,
record `Advisor metadata: <role/scope> | <path>`, followed when one is serving
by `Incumbent advisor session: <role/scope> | <harness> | <canonical durable
harness resume id> | address: <path>`. Record a differing public address or
provider-native handle in the address file. Verify the real ids, update the
line on replacement or provider-session change, and omit disposable subagents.
A fresh-per-consult policy retains the metadata line but removes the incumbent
line after closure. Full intake, resume, and unavailable-id handling is in
`topics/handoffs.md`.

### Active sessions

On the first planning-to-act step in a shared workdir, write
`.agentctl/active/<session-id>` with a short present-tense status line.
Create `.agentctl/active/` if missing. Recover the provider's real
resumable session id and key the entry by it — the provider supplement
names the mechanism (env var, else this session's transcript). Do that
work: a hand-picked personal tag is a last resort only where the
provider exports no id *and* has no recoverable transcript. A fabricated
id is not carried in env across calls and diverges from the real id a
resume or sibling shell uses, so it is never DONE-marked and lingers as
a false live peer.

Line 1 is the gist; line 2 may be `scope: <paths>`, with plain
paths or separator-anchored globs (`/**` subtree, `*.ext`; full schema in
`topics/agentctl.md`). Update at milestones, after 10+ min of
continuous work, or at the 60-min heartbeat cap. On completion start line
1 with `DONE`, preferably `DONE: <one-line summary>`. Pure read-only or
interview sessions may skip this.

Check for active peers with `find .agentctl/active -maxdepth 1 -type f
-mmin -70`, ignoring entries whose line 1 starts with `DONE`. Task notes,
run logs, and commit status do not satisfy active sessions. `agentctl
active "<banner>" [paths...]` is the run-free convenience for writing your
own entry; `agentctl active` lists fresh non-DONE entries. Prefer two
verbs over carrying a peer belief: `agentctl others <session-id>` answers
"am I alone?" by exit code (0 alone, nonzero peers) with your own entry
excluded — use it as `agentctl others <id> && <solo-only step>`, re-run
at the point of caution rather than trusting a stale reading (see
*Pre-edit re-Read and parallel-worker noticing*); `agentctl alone <id>
-b "<status>" [scope...]` blocks until every other peer is gone (for an
intentionally project-serial step, e.g. a whole-project amend/rebase),
then registers your entry. Neither verb narrows to `scope:` overlap; a
waiting `alone` is visible to browsers but never counts as a peer.

A steward-type session — one that will keep launching queued work when
it wakes (e.g. `/steward` between hourly rounds) — adds a `tending:`
line to its entry while such launches stay armed, and checks `agentctl
tending <session-id>` before clearing a queue: exit 0 also claims
tending, nonzero names the session already tending it, so two stewards
never race one queue (schema and mechanics in `topics/agentctl.md`).

Read `topics/agentctl.md` before changing active-session semantics,
diagnosing `.agentctl` run state, modifying `agentctl`, or relying on
details of the `active`/`others`/`tending`/`alone` verbs, staleness
window, sweep, launch-depth guard, or plugin contract.

### Resume source priority

If a first-turn handoff or context-compression message carries a link/session
id, browse that session to catch up — scan for commit/topic boundaries and read
the last two sections closely.

After a disconnect, crash, restart, or compaction, retain any already-known
work scope. For a named resume use the named artifact. Only a bare `/hi` or
scope-less boot reads `tasks/ROOT` first, as a possibly stale discovery hint.
Then reconcile against live state: worktree and recent commits,
`.agentctl/active/`, run and `on-deck/` state, artifacts, then provider logs
needed to fill a specific gap. A recent relevant task, auto-handoff, or
`*.bearings.md` can orient when the first hint is missing or unrelated.

### Scheduled session prompts

Once at the start of each ordinary new or resumed project session, cheaply
probe that project's `<project>/at/` for a due `*.md` prompt when the directory
exists. Do not create `at/` merely to check it, and do not also probe
`~/agents/at/` from another project: an `at/` entry belongs to the project
containing it and runs with that project root as its working directory.
An at-launched runner skips this startup probe, preventing recursive launch
chains.

Claiming goes through the project-local `scripts/at-queue` when executable,
else `~/agents/scripts/at-queue`: pass the project root, canonical resumable
session id, harness, and the PID of a process outliving the claim, then use the
exact source path it returns. The helper is mandatory, not a convenience — if
neither exists, skip the probe rather than hand-rolling an unlocked claim.

A prompt under `at/` is inert source; what schedules it is the clone-local
activation store the helper owns, which is never tracked, so pulling a
repository cannot start agent work. Never hand-edit that store. Before invoking
a job, load and follow `topics/at-scheduling.md` from the project root when
present, else `~/agents/topics/at-scheduling.md`; its activation split, claim
protocol, and runner acknowledgement (`at-queue done`) govern whether a job may
run.

A session-start probe is catch-up, not a wall-clock scheduler. An explicit
multi-project helper or YA may provide punctual wakeups over the same store,
invoking `at-queue` rather than reimplementing it, and must derive each job's
working directory from its owning `at/`, never from the helper's caller.
