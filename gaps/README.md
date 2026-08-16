# gaps/ — unresolved project incompleteness

`gaps/` holds one file per unresolved project incompleteness: a
noticed-but-not-fixed-now code-quality defect, or a partially landed single unit
whose current repository state is incomplete or misleading. The point is that
such state must not evaporate into chat. In this repository gaps are committed
and greppable; another project may choose different tracking while preserving
the same semantic boundary.

This is the durable-capture half of *"capture adjacent gaps; don't chase
or drop them"* (`AGENTS.global.md`). The other half is the fix-in-place exception:
when the fix is cheap *and* in scope (the seam is already open), just fix
it as its own commit — no gap file needed.

A nice-to-have or dreamed improvement that exposes no current defect or blocker
belongs in the owning topic's candidate-improvement or `## Sketches` section.
Private resume state that implies no project defect belongs in `tasks/`. The
single-purpose meaning of this directory is unresolved project incompleteness,
not every unimplemented plan or missing handoff.

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

## Scoped gaps directories

Like `topics/`, a glossary/program scope may own a sibling `gaps/`, created
on first need — `surveys/llm-intelligence/gaps/` for example. Choose the
owning scope as for a topic doc; the project root is the default. This root
README governs every scoped directory — do not copy it. A `gaps/` directory's
presence marks live backlog in that subtree. When the owning scope has a
`PROGRAM.md`, the goals a gap claims are impaired are that charter's.

## Reading

Glance at the enclosing scopes' `gaps/` directories, nearest first, when
starting work in an area — a filed gap is known context, and its fix may
now be in scope (then fix and remove it as its own commit). Capture without
this read side is write-only memory.

## Lifecycle

- **Create** `gaps/<slug>.md` when you notice an adjacent defect you are
  deliberately not fixing now, or when a partially committed unit needs an
  honest visible account of what remains. Check existing entries first; an
  observation duplicative of or close enough to an existing entry extends
  that file rather than filing a duplicate.
- **Choose useful granularity.** `TOPICS.md`'s landing-site principles apply —
  one home plus pointers, name the retrieval trigger — at a finer grain than
  topics. A gap file is either a **triage pool** (one running file at a
  topical scope holding less-investigated, vague noticed items until a pass
  triages them into a working plan or promotes one to its own file) or a
  **session unit** (a small specific proposal sized for one working session,
  carrying the claim that program — or project — goals stay impaired until it
  clears). Promotion out of a pool is the normal way old material becomes a
  new file. A capability-gated `.sketches.md` companion beside the owning
  formal topic and its gap link both ways; do not create an alternate
  `*.gaps.md` discovery namespace or require routine scans of every topic
  companion.
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
