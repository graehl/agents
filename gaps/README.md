# gaps/ — durable capture of adjacent, deferred defects

`gaps/` holds one file per noticed-but-not-fixed-now code-quality defect —
a UI glitch, a lint warning, a failing or flaky test, a small structural
wart — that is *adjacent* to the current work rather than part of it. The
point: a defect an agent noticed must not evaporate into a chat comment
that dies with the session. It becomes a committed, greppable entry the
next session or the user trips over.

This is the durable-capture half of *"capture adjacent gaps; don't chase
or drop them"* (`AGENTS.md`). The other half is the fix-in-place exception:
when the fix is cheap *and* in scope (the seam is already open), just fix
it as its own commit — no gap file needed.

## Why committed, and why its own directory

- **Committed, unlike `tasks/`.** `tasks/` is private, git-ignored working
  state; a gap is durable backlog that should survive a fresh clone and be
  visible to peers. So `gaps/` is tracked.
- **Not `topics/`.** A topic doc is a lasting cross-cutting contract; a gap
  is transient — it exists only until fixed, then it is removed.
- **Not `on-deck/`.** On-deck entries are executable, guarded run-queue
  items a steward launches. A gap has no launch command and no
  scheduler, and never grows one: gaps are addressed by a frontier
  agent in active dialog — or a subsession it chooses and manages —
  never by queueing or launching a fixer process, because the user
  needs visibility into what actions sessions take in response to
  commands. Tending on-deck does not itself put unrelated gaps in scope.

## Reading

Glance at `gaps/` when starting work in an area — a filed gap is known
context, and its fix may now be in scope (then fix and remove it as its
own commit). Capture without this read side is write-only memory.

## Lifecycle

- **Create** `gaps/<slug>.md` when you notice an adjacent defect you are
  deliberately not fixing now (out of scope for the current change).
  Check existing entries first; extend the file covering the same
  defect rather than filing a duplicate.
- **Remove** `gaps/<slug>.md` in the same commit that fixes the gap. Do not
  archive it — git history is the record, and the commit message narrates
  the closure.
- **Remove when moot** — a gap obsoleted by other work (code deleted,
  premise falsified, fixed independently) exits by its own small commit
  naming the reason. Without this exit the empty-`gaps/` target becomes
  unreachable and the directory rots like the scattered TODOs it
  replaces.

## Entry format

Light by design — a gap is low-ceremony. Reference code by symbol or path,
never a bare line number (a committed doc outlives the line).

```markdown
---
slug: <kebab-case>
noticed: <YYYY-MM-DD>
where: <symbol or path>
---

**Gap:** what is off — the symptom, and the invariant it violates if known.
**Noticed while:** the task that surfaced it (marks it adjacent, not core).
**Fix sketch:** the seam or approach, or "unknown — needs diagnosis".
```
