---
slug: agentctl-dual-path-artifacts
noticed: 2026-09-10
where: agentctl.py input/output declaration; artifact_meta sidecar writing; _RUNS/provenance.md
---

**Gap:** an input or output has exactly one path in a run record, so a run that
legitimately reads or writes through a fast scratch replica has to choose
between two wrong answers. Cite the replica and the record rots the moment
scratch is evicted or its host is replaced. Cite the durable home and the
record disagrees with the argv the payload actually ran, which is the one thing
the record is supposed to reproduce. `_RUNS/resources.md` now requires the
durable citation, so today's compliant runs deliberately record a path the
payload never opened.

**Noticed while:** planning the migration of the `gra` host to a new instance,
where instance-store `/scratch` does not survive and draft run records that
name `/scratch` paths would have to be relocated and repointed by hand.

**Fix sketch:** let a declaration carry both paths — a runtime path handed to
the payload and a durable path recorded as the artifact's identity — rather
than forcing one to stand in for the other. `--output-arg` is the existing
precedent for one value serving two roles, so the shape is likely
`KEY=runtime-path@durable-path` or a paired option, with the sidecar written
beside the durable copy. Completion should verify the durable copy exists and
hashes equal to the runtime one before the run is recorded clean; a missing or
divergent durable copy is a run failure, not a warning, or the dual form just
relocates the rot. Inputs need the mirror image: record the durable source
while reading the replica, and refuse the run if the two disagree.

An accepted alternative is to keep one path and make relocation an explicit
post-run verb that rewrites the record and its sidecars together. That is
cheaper to build and worse to operate, because nothing forces it to happen.
