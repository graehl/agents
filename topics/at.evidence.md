# at — evidence and decisions

Append-only notes supporting the `at/` scheduled-session protocol.

## 2026-07-30 — the lock is the manual runner's in-flight state

- The first draft separated pending/running/history state as if a program
  would enforce it. The user pointed out that v1 is instruction-operated:
  periodic rescheduling and completed-job retirement are responsibilities of
  the prompted runner itself.
- The directory lock therefore spans discovery, runner creation, and the
  entire object-level run. The runner removes it only after it has verified
  either the next scheduled mtime or the completed-job parking mtime. This
  ordering closes the ordinary duplicate window: a second startup may have
  observed the old due mtime, but it cannot invoke while the lock remains; if
  it acquires after unlock, its mandatory re-read observes the non-due job.
- A crash leaves a visible lock rather than guessing whether session creation
  or object-level work happened. Age alone never proves it safe to retry.
- A same-name concurrent `mkdir` probe on the NFS filesystem hosting
  `~/agents` produced one success and one `File exists` failure, confirming the
  final-component directory creation supplies the required single winner in
  the current environment.

## 2026-07-30 — year-3000 mtime is filesystem-dependent

- A scratch-file probe under `/home/graehl/agents` (reported by `stat -f` as
  NFS) round-tripped `3000-01-01T00:00:00Z` exactly:
  epoch `32503680000`.
- The same probe under `/home/graehl/ya` (XFS) returned success from `touch`
  but silently stored `2038-01-19T03:14:07Z`, epoch `2147483647`.
- Consequence: checking only that `touch` succeeded, or only that the result is
  future, can falsely claim an exact year-3000 acknowledgement. The protocol
  compares the stored value with the request, records a future clamp when one
  is unavoidable, and clears active `run_after` so the clamp horizon cannot
  reactivate completed work.
- **Superseded 2026-07-31.** With the schedule moved out of the filesystem
  index entirely (below), nothing writes a sentinel mtime and this whole class
  of clamp failure is unreachable. Kept as the reason the mtime index was not
  worth repairing.

## 2026-07-31 — activation leaves the source file

- **Requirement (graehl).** Agents must be able to create *and* activate a job
  with no YA API call and no manual operation of the YA interface. YA is a
  helper over a convention external to it, so it cannot enforce its own
  "pulling a repository must never start agent work" rule here.
- **Rejected: dropping that property.** It does not have to be enforced by YA
  to hold. Moving activation to a clone-local untracked file
  (`.yep/at-activation.json`) makes `git pull` *physically unable* to schedule
  work — pull only writes tracked paths. The guarantee becomes structural, and
  agents keep unrestricted local create+activate. YA's rule stays scoped to
  what YA dispatches: batch drift confirmations that block YA's own executions,
  per `~/ya/topics/routines.md`.
- **The one thing that must be mechanized.** "Never track the activation file"
  fails silently and is reintroduced by an ordinary `git add -A`, so `at-queue`
  checks it (`git ls-files --error-unmatch`) and refuses. Contrast the
  hand-edit ban, whose worst case is one lost scheduling record: that is a
  mandate plus a canonical-formatting warning. Mandate what is merely racy;
  mechanize what is a safety boundary — the same split as
  AGENTS.global.md § Edit mechanism discipline (mandate) versus `agent-guarded`
  (mechanism).
- **The helper mandate is also the YA integration.** One implementation of the
  protocol that YA shells out to, rather than a second copy in TypeScript
  drifting from this one. Its cost is a CLI surface wide enough that nobody
  needs to hand-edit: `activate`, `pause`/`resume`, `claim`, `done`, `list`.
- **Lock: same primitive, shorter critical section.** `mkdir` is kept over
  `flock` because these queues live on NFS (`~/agents` is nfs4), where
  directory creation is atomic but flock auto-release is not dependable. What
  changed is span — the lock now covers one read-modify-write of the activation
  file, never a job's run. That is what makes an age-based stale break sound,
  since no legitimate holder lasts seconds.
- **Consequence: heartbeat and phase are deleted, not implemented.** The
  2026-07-30 design held the lock across the entire run, which made "how long
  is too long?" unanswerable and forced `heartbeat_at`, a `phase` ladder, and
  owner adjudication. Splitting the lock (one write) from the run record (PID +
  `/proc` start ticks + boot id) answers liveness exactly, at any instant, with
  no periodic write. A harsh review found both fields were written once and
  never updated, with `topics/at.md` resting liveness proof on the heartbeat —
  the reframe removes the defect rather than fixing it.
- **Rejected: optional `--owner-pid`.** Without recorded start ticks a claim
  carries no liveness evidence and single-winner silently degrades to nothing,
  so the flag is required and an unreadable `/proc` entry warns rather than
  passing quietly.
- **Rejected: activation under `at/`.** The owner may deliberately track `at/`
  (that permission predates this change and is worth keeping for reviewable
  prompts), which would put activation back in Git's reach.
