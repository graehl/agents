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
