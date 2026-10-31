---
slug: run-source-dependencies
noticed: 2026-09-24
where: agentctl.py source admission; topics/provenance-tracking.md
---

**Outcome:** a tracked run records the in-repo files it actually depends on,
so its Git SHA reproduces it without requiring a clean worktree.

**Implemented (2026-10-31):** declared lists (`--source-dep`,
`--source-deps-file`), a static scan (`--source-deps-scan`: Python imports
via `ast`, shell references and extra patterns by regex), dependency-only
admission and delayed-launch checks, and the loading phase (marker file or
timeout). The contract lives in [agentctl](../../topics/agentctl.md),
"Declared source dependencies". A cooperative `declared.json` field was not
added: the payload writes that file at exit, too late to gate admission.

**Remaining approach — traced audit:** an optional mode runs the payload
under `strace -f -e trace=open,openat,execve` (truss/dtruss elsewhere),
keeps the in-repo paths it opened, and records them. A traced list from a
smoke can seed the declared list for the full run, and catches what the
static scan cannot: dynamic imports and runtime-computed paths.

**Open decisions:** lazily imported modules and data read late in a long
run escape a smoke trace; tracing overhead on GPU jobs; whether a declared
list that misses a file read at runtime should fail the run or only mark the
record.
