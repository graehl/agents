---
slug: atomic-write-helper-duplicates
noticed: 2026-11-10
where: scripts/handoff-age `_write_atomically`, scripts/build-boot `_write_atomic`
---

**Gap:** several scripts each carry a private write-to-scratch-then-rename
helper. The 2026-11-10 strict review counted six, also naming
`scripts/install_agents/core.py`, `agentctl_coordination.py`, and
`almanac/cli.py`. They differ in whether they keep the file mode, follow a
symlink, or sync before the rename, so a fix to one (the symlink case in
`handoff-age`) does not reach the others.
**Noticed while:** adding `scripts/handoff-age`.
**Fix sketch:** one shared helper beside the `acli` library with the union of
the needed guarantees (same-directory scratch, mode kept, symlink resolved),
then replace each private copy and delete it.
