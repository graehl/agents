# At — scheduled agent sessions

> An `at/` queue is a project-owned, mtime-indexed set of future
> session-opening prompts whose runners claim once, execute in the owning
> project, and acknowledge by rescheduling or parking the prompt.

Topic: `at`

This is a filesystem protocol for low-volume, agent-operated scheduling. It
does not pretend that instructions alone provide a wall-clock daemon. A future
helper or YA scheduler may implement the same protocol, but ordinary sessions
can service it correctly without one.

## Ownership and location

An entry at `<project>/at/<job>.md` belongs to `<project>` and opens its runner
with that project root as the working directory. In particular,
`~/agents/at/<job>.md` belongs to `~/agents`; it is not a machine-global queue
that every other project session scans.

Ordinary session startup checks only the current project's `at/`. An explicit
multi-project invoker may inspect several known project queues, but resolves
and preserves each queue's own project root. When two paths resolve to the
same project and queue, canonicalize them and inspect it once.

`at/` is git-excluded by default. Apply the global creation-only convention:
add the exclusion to the repository-local Git exclude only while creating
`at/`; never use `.gitignore`, and never restore a missing exclusion on an
existing directory. The owner may deliberately track the queue.

## Job file

The basename of `<job>.md` is the job identity. Reuse the same file for a
periodic job; use a new, collision-free basename for a distinct job. A job is
small, human-editable Markdown:

```markdown
---
run_after: 2026-08-01T09:00:00Z
created_at: 2026-07-30T18:00:00Z
scope:
  - user/MASTERY.md
---

Review one currently due mastery entry. ...
```

`run_after` is required for an active job and uses RFC 3339 with an explicit
timezone. `created_at` and `scope` are recommended. Provider, model,
permission-mode, expiry, or source-routine fields may be added when the
launcher needs them; absent launch fields inherit the ordinary project/session
defaults. The Markdown body is the object-level opening prompt.

The job may state a recurrence rule in ordinary language because its runner,
not a parser, chooses the next appropriate instant. If it does not specify
rescheduling, one completed invocation retires it by the year-3000 mtime
sentinel described below.

## Due index and wakeups

For an active job, the file's mtime should equal `run_after`. The in-file value
is authoritative; mtime is only the cheap index that prevents every startup
from reading every future job.

At the start of each ordinary new or resumed session, once per process launch:

1. Resolve the current project root.
2. If `<project>/at/` does not exist, stop without creating it.
3. Inspect top-level `*.md` entries whose mtime is not later than now, oldest
   first. A normal startup probe invokes at most one job.
4. Acquire the per-job lock, then re-read and validate `run_after` and the
   prompt. A due-looking mtime never overrides a future or invalid in-file
   value.
5. Launch the runner with the owning project root as its working directory and
   pass the exact job and lock paths plus the runner-acknowledgement duty.

Continue past locked, invalid, or no-longer-due candidates until one job is
invoked or the bounded candidate set is exhausted; one stale lock must not
starve unrelated jobs.

An at-launched runner does not perform the startup probe. An explicit user
request, a bounded multi-project helper, or YA may also trigger a probe and may
service more than one job under an explicit concurrency bound.

No session-start scheme wakes while no session starts. It provides eventual
catch-up only. A future independent scheduler owns punctual wakeups; it must
not keep one provider process or polling loop alive per job.

## Per-job lock and handoff

Several sessions may discover the same due mtime. Exclusion is therefore a
per-job directory lock:

```text
<project>/at/.locks/<job>.lock/
  owner.md
```

Create `.locks/` when initializing `at/`, or as operational state if an older
queue lacks it; doing so does not authorize changing the queue's Git exclusion.
Acquire `<job>.lock/` with one plain atomic `mkdir` of that final directory.
Do not use `flock`, a check-then-create lock file, `mkdir -p` for the final
component, or `mv -n` as the exclusion primitive. A failed `mkdir` means
another invoker owns or left the lock; skip the job.

Immediately record in `owner.md`:

- the canonical resumable invoker session id;
- host and PID when available;
- claim time;
- phase (`claimed`, `launching`, or `runner`);
- the SHA-256 of the exact job bytes claimed;
- once known, the runner session or durable occurrence id.

After acquiring the lock, re-read the job and compute its hash. If it moved,
changed, became future-scheduled, or became invalid, record the reason and
release only the lock this invoker created; never run the stale candidate.

The invoker retains the directory lock across session creation. The launched
runner's first protocol action is to verify the job hash and update `owner.md`
to name its own resumable session id and phase `runner`. The lock remains for
the entire run. Its purpose is not mutual exclusion around file editing alone;
it prevents another startup probe from launching the still-due prompt before
the runner has acknowledged its disposition.

## Mandatory runner acknowledgement

Before its final response, the runner must leave the prompt non-due and verify
that state. The order is part of the contract:

1. Record a concise completion/failure fact in the job without erasing its
   reusable prompt.
2. If the job specifies recurrence, choose the next instant, update
   `run_after`, set the file mtime to exactly that future instant, and verify
   both values.
3. Otherwise mark it completed, set `run_after: null`, set its mtime to
   `3000-01-01T00:00:00Z`, and compare the stored mtime to that exact request.
   A filesystem may silently clamp it. If so, record the actual stored
   `parked_mtime` in the job and accept it only when it is still safely in the
   future; the cleared `run_after` remains the semantic defense when that
   filesystem horizon eventually arrives.
4. Only after successful verification remove `owner.md` and `rmdir` the
   per-job lock.

If the filesystem refuses a future timestamp, clamps it to a value that is not
future, or any acknowledgement step cannot be verified, keep the lock and
report the job as blocked. Do not release it and leave the file due.

A failed object-level task follows the same rule: reschedule only when the job
specified or the user directs a retry; otherwise record the failure and park
it. Automatic retry after an uncertain result is more dangerous than a visible
miss because it can duplicate external effects.

## Stale and ambiguous locks

Never steal or remove a lock merely because it is old. First inspect
`owner.md`, the named invoker/runner session, the prompt, and any recorded
result:

- a live or uncertain owner keeps the lock;
- a provably dead owner with proof that no runner was created may have its lock
  removed and the still-due job retried;
- if session creation may have succeeded but its durable id was not recorded,
  leave the job blocked for manual adjudication.

Exactly-once session creation across the final case requires the launcher to
accept an idempotency key. When available, derive it from the canonical queue
path, job basename, and claimed prompt SHA-256; a retry with that key must
resolve to the original occurrence rather than create another. Without such a
launcher contract, this protocol deliberately prefers visible at-most-once
behavior over a duplicate run.

## Safe job updates

Re-read a job immediately before changing it. Preserve the object prompt and
prior completion facts. For a non-trivial rewrite, build and validate a
complete sibling temporary file and atomically rename it over the job; keep a
recoverable backup when the update could replace user-authored content.

The lock controls invocation, not authorship. A user may edit or cancel a job
at any time. An invoker detects such a change by the mandatory post-lock
re-read/hash; it never overwrites the newer version to preserve its claim.

## Relationship to YA routines

An `at/` job is one authorized occurrence. A YA routine is reusable
project-owned source plus server-local activation and recurrence. A future YA
routine tick may materialize an occurrence equivalent to an `at/` job, and a
YA launcher may service `at/`, but it must keep these identities separate:

```text
routine source + activation -> occurrence -> safe session dispatch
at/<job>.md -----------------> occurrence -> safe session dispatch
```

Do not turn `at/` into a second prompt library or invent a cron grammar for it.
Periodic `at/` jobs remain agent-rescheduled until promoted to a YA routine.
