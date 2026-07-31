# At — scheduled agent sessions

> An `at/` queue pairs hand-editable prompt sources, which may be committed,
> with a clone-local activation store that alone decides what runs; every
> mutation goes through `scripts/at-queue`.

Topic: `at`

This is a filesystem protocol for low-volume, agent-operated scheduling. It
does not pretend that instructions alone provide a wall-clock daemon. A helper
or YA scheduler may provide punctual wakeups over the same store, but ordinary
sessions service it correctly without one.

## Source and activation are separate

Two artifacts, and the split is the safety property:

- **Source** — `<project>/at/<job>.md`, the reusable opening prompt. Ordinary
  Markdown, hand-editable, and trackable if the owner wants it reviewed.
- **Activation** — `<project>/.yep/at-activation.json`, holding schedule,
  enabled state, the approved prompt hash, and run records.

**Activation must never be tracked.** Because it is clone-local and untracked,
`git pull` cannot write it, so no repository content can schedule agent work —
not by policy but by construction. `at-queue` refuses to read or write a
tracked activation file rather than trusting the rule to hold.

The source stays free: an agent may create *and* activate a job with no
external API and no human UI step. What it cannot do is make that activation
travel to another clone through Git.

Activation lives under `.yep/` because that is the established clone-local
directory (YA keeps its own approvals there) and because it sits outside the
queue directory the owner may deliberately track.

## The helper is mandatory

All activation reads and writes go through `scripts/at-queue`. Hand-editing
`at-activation.json` is forbidden: the file is machine-owned, and a bare write
can lose a concurrent update. `at-queue` warns when it loads a file it did not
write (non-canonical formatting), so a hand edit is noticed rather than merely
prohibited.

If neither the project-local nor the `~/agents` helper is present and
executable, **skip the probe entirely**. Do not hand-roll the claim: an
unlocked read-modify-write is exactly what the helper exists to prevent, and a
missed catch-up is cheaper than a double launch.

```text
at-queue activate --root R --job NAME --run-after RFC3339
at-queue pause|resume --root R --job NAME
at-queue claim --root R --session ID --harness H --owner-pid PID
at-queue done --root R --job NAME (--run-after RFC3339 | --park) [--status S]
at-queue list --root R
```

`claim` exits 0 with the claimed job, 3 when nothing is claimable; a refused
operation exits 4 with a JSON `error`. Full CLI contract and post-conditions:
`topics/helper-scripts.md`.

## Ownership and location

An entry at `<project>/at/<job>.md` belongs to `<project>` and opens its runner
with that project root as the working directory. In particular,
`~/agents/at/<job>.md` belongs to `~/agents`; it is not a machine-global queue
that every other project session scans.

Ordinary session startup checks only the current project. An explicit
multi-project invoker may inspect several known project queues, but resolves
and preserves each queue's own project root. When two paths resolve to the same
project, canonicalize them and inspect it once.

`at/` is git-excluded by default. Apply the global creation-only convention:
add the exclusion to the repository-local Git exclude only while creating
`at/`; never use `.gitignore`, and never restore a missing exclusion on an
existing directory. The owner may deliberately track the prompt sources. That
permission never extends to the activation file.

## Job file

The basename of `<job>.md` is the job identity. Reuse the same file for a
periodic job; use a new, collision-free basename for a distinct job. A job is
small, human-editable Markdown:

```markdown
---
name: mastery-review
scope:
  - user/MASTERY.md
---

Review one currently due mastery entry. ...
```

`name` and `scope` are recommended. Provider, model, or permission-mode fields
may be added when the launcher needs them; absent launch fields inherit the
ordinary project/session defaults. The Markdown body is the object-level
opening prompt.

**No schedule field.** `run_after` is activation state and lives only in the
activation store. A source file carrying a schedule is a source file that
schedules work by being copied.

The job may state a recurrence rule in ordinary language because its runner,
not a parser, chooses the next appropriate instant and passes it to
`at-queue done --run-after`. A job that specifies no rescheduling is parked by
`--park` after one completed invocation.

## Probe and claim

At the start of each ordinary new or resumed session, once per process launch:

1. Resolve the current project root.
2. If `<project>/at/` does not exist, stop without creating it.
3. Run `at-queue claim`, passing the project root, canonical resumable session
   id, harness, and the PID of a process that will outlive the claim.
4. On exit 0, launch the runner with the owning project root as its working
   directory, passing the exact source path and the acknowledgement duty.

`claim` grades every job before taking one and reports why each was skipped
(`paused`, `not due`, `already running`, `prompt source is missing`, or a
prompt changed since activation), so one blocked job never hides the rest. A
normal startup probe takes at most one job.

An at-launched runner does not perform the startup probe, which is what
prevents recursive launch chains. An explicit user request, a bounded
multi-project helper, or YA may also trigger a probe and may service more than
one job under an explicit concurrency bound.

No session-start scheme wakes while no session starts. It provides eventual
catch-up only. A punctual scheduler is a separate concern and must not keep one
provider process or polling loop alive per job.

### A changed prompt blocks its own claim

Activation records the SHA-256 of the prompt bytes it approved. If the source
differs at claim time, the job is skipped with `re-activate to approve` rather
than run. This matters most for a tracked `at/`, where a collaborator's commit
can change what a scheduled job says; approving is a deliberate `activate`.

## Exclusion without a heartbeat

Two mechanisms, deliberately distinct — conflating them is what forces
liveness ceremony into a lock:

**A lock, held for one write.** `at-queue` serializes activation writes with an
atomic `mkdir` of `at-activation.json.lock`. `mkdir` rather than `flock`
because these queues live on NFS, where directory creation is atomic but
flock's auto-release is not dependable. The critical section spans a single
read-modify-write, never a job's run, which is what makes an age-based break
sound: a lock older than 30 seconds cannot be a live holder, only debris.

**A run record, held for the run.** A claim records the runner's session,
harness, host, and process-start identity (PID plus `/proc` start ticks plus
boot id). A later claim asks "is that exact process incarnation still alive?" —
answerable at any instant with no periodic write. If it is gone, the run was
abandoned and the job is claimable again.

There is therefore no heartbeat and no phase ladder. `kill -0 <pid>` alone
never proves ownership because PIDs are reused; start ticks are what
distinguish a live process from its successor, so a claim that cannot record
them warns that it is not provably exclusive.

## Mandatory runner acknowledgement

Before its final response, the runner must call `at-queue done` with an
explicit disposition — `--run-after <next instant>` or `--park`. The helper
clears the run record, stamps the outcome, and re-approves the current source
bytes in one locked write, so there is no ordering for a caller to get wrong
and no half-applied acknowledgement to recover from.

`done` refuses without a disposition rather than guessing. A failed
object-level task reschedules only when the job specified or the user directs a
retry; otherwise record the failure and park it. Automatic retry after an
uncertain result is more dangerous than a visible miss because it can duplicate
external effects.

A runner that dies without calling `done` leaves a run record whose process is
provably gone, so the job simply becomes claimable again at its existing
schedule. That is the intended failure mode: at-most-once per due instant, with
a visible retry, rather than a stuck lock needing adjudication.

## Exactly-once session creation

The claim protocol prevents two *simultaneous* launches. It cannot by itself
prevent a duplicate when a launcher created a session but the caller crashed
before recording it. Where the launcher accepts an idempotency key, derive it
from the canonical queue path, job basename, and claimed prompt SHA-256; a
retry with that key must resolve to the original occurrence rather than create
another. Without such a launcher contract, this protocol deliberately prefers
visible at-most-once behavior over a duplicate run.

## Safe job updates

Re-read a source immediately before changing it. Preserve the object prompt and
prior completion facts. For a non-trivial rewrite, build and validate a
complete sibling temporary file and atomically rename it over the job; keep a
recoverable backup when the update could replace user-authored content.

Activation controls invocation, not authorship. A user may edit or cancel a
source at any time; the claim-time hash comparison turns that edit into a
visible block, never a silently overwritten file.

## Relationship to YA routines

An `at/` job and a YA routine now share one shape — reusable source plus
server- or clone-local activation:

```text
routine source + YA activation -------> occurrence -> safe session dispatch
at/<job>.md    + at-activation.json --> occurrence -> safe session dispatch
```

YA is a **helper over this convention, not its owner**. It may discover `at/`
sources, display schedules and run history from `at-queue list`, provide the
punctual wakeups a session-start probe cannot, and offer run/pause actions —
all by invoking `at-queue`, never by reimplementing the lock in a second
language.

YA's rule that repository content must not activate a routine
(`~/ya/topics/routines.md`) remains YA's, and applies to what YA dispatches:
it may batch drift warnings and block *its own* executions until a user
confirms. It does not gate the CLI probe, and it does not need to — untracked
activation already makes a pulled repository unable to schedule anything.

Do not turn `at/` into a second prompt library or invent a cron grammar for it.
Recurrence stays agent-chosen per completion until promoted to a YA routine.
