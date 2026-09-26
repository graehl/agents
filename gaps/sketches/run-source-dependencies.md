---
slug: run-source-dependencies
noticed: 2026-09-24
where: agentctl.py source admission; topics/provenance-tracking.md
---

**Outcome:** a tracked run records the in-repo files it actually depends on,
so its Git SHA reproduces it without requiring a clean worktree. Today
admission rejects any in-scope tracked drift and any non-ignored untracked
Python, because it cannot tell which files the run reads
([provenance-tracking](../../topics/provenance-tracking.md) § Bounded scope).
With a dependency list, only those files must match the recorded commit.

**Approach:**
- Explicit: the launcher or payload declares a dependency path list
  (e.g. `--source-dep PATH`, or a cooperative `declared.json` field), stored in
  the run record and readable in dry-run form before launch.
- Traced: an optional audit mode runs the payload under `strace -f -e
  trace=open,openat,execve` (truss/dtruss elsewhere), keeps the in-repo paths
  it opened, and records them. A traced list from a smoke can seed the
  declared list for the full run.
- Admission then checks cleanliness and commit recoverability for the listed
  paths only, keeping the current whole-scope check as the fallback when no
  list exists.

- Loading phase (user, 2026-09-26): the declared files need to stay fixed
  only for a brief loading phase at payload start, until the process has
  imported or read them, not for the whole run or the whole queue wait. The
  admission check and the delayed-launch check cover the listed files. The
  run then signals, or agentctl infers, the end of loading; edits to those
  files after that point do not affect the run and are not violations.

**Interim:** `--source-guard record` (or `AGENTCTL_SOURCE_GUARD=record` in a
project `agentctl.env`) records whole-scope violations in the run record
instead of refusing or aborting. The draft PII project uses it because its
shared checkout is edited throughout long queued chains. Once dependency lists
and the loading phase exist, record mode should become unnecessary for such
projects.

**Open decisions:** lazily imported modules and data read late in a long run
escape a smoke trace; tracing overhead on GPU jobs; whether a declared list
that misses a file read at runtime should fail the run or only mark the record;
how the end of the loading phase is signalled (payload marker file, first GPU
allocation, or a fixed timeout).
