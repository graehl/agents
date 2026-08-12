# Research workflow and continuity

> Rules, templates, and rationale for on-deck work, subtasks, checkpoints, direction roots, paths, and resume.

Read this packet before queueing, resuming, checkpointing, or autonomously
selecting research work. `RESEARCH.md` is the router and wins on conflict.

## Binding rules

### Workflow and continuity

#### On-deck research runs

`on-deck/` is the executable projection of research triage into guarded
single-step runs, not the paper/log/task. Every entry points to its governing
artifact; steward records raw run facts while interpretation lands in the
paper, log, task, or topic. See `topics/on-deck.md`.

#### Subtasks and commit checkpoints

Commit paper/log updates and source checkpoints when meaningful findings or
subtask states land. Private task and working-handoff files remain private
unless the user explicitly asks otherwise. Stage only known work; do not infer
ownership from timestamps or sweep unrelated files. Global shared-worktree and
commit rules govern any ambiguity.

Each main task file maintains a `## Subtasks` list covering file-backed and
inline work, with status, last worked, likely next, and user-confirmed
completion. The detailed table template and branch search command appear below
under “Main task file: subtask tracking section.”

#### Research direction root (`research/ROOT.md`)

When present, `research/ROOT.md` records established user direction about
fruitful projects for autonomous research/tending. Read it before choosing such
work. Routine detail/progress may update it; reversing which projects are
fruitful requires explicit user consent.

#### Research document paths and resume

Derive paper/log names from the Git branch. A branch paper requires a
corresponding main task file; report a missing one. “Update the research
paper/log” means the branch-derived file unless the governing task names
another.

On explicit `/hi` or resume of research work:

1. resolve the named handoff/task, or for bare `/hi` the default discovery hint,
   under “Resume source priority” in [AGENTS.global.md](../AGENTS.global.md);
2. reconcile it with live state;
3. skim `research/ROOT.md` when present;
4. skim the branch paper/current framing;
5. read the governing task's Subtasks section and listed in-progress subtask
   files; and
6. read the newest research-log entries.

Do not run this checklist for a fresh specific request without a resume signal.

## Retained detail and examples

### Subtasks and commit checkpoints

**Subtasks** (NNN-name.md files with `## Branch: <branchname>` header) live in the
same branch as their parent task. They do NOT get their own research/ documents —
all findings go in their task file sections. The parent task's research/ documents
should reference subtask conclusions once resolved.

Not every subtask gets its own file. Minor items may be tracked inline in the main
task file's subtask list and worked on without a dedicated NNN-name.md. The user
will explicitly ask to create a subtask file when one is warranted.

**Rule**: never merge back to main repeatedly for subtasks. Complete or park all
subtask work in the branch, then merge once when the main task is done.

**Commit checkpoints**: commit to the research branch whenever a meaningful checkpoint
is reached — a subtask (inline or explicit) is satisfactorily resolved, an interesting
subtask is newly identified, or a significant finding is recorded. These commits do not
require explicit permission; use judgment and proceed if confident. It is polite to note
"committing now" or ask first when the scope is ambiguous.

### On-deck research runs

For GPU-heavy research programs, `on-deck/` is the executable projection of
research triage into guarded single-step runs, not a replacement for the
research log or task file. Each entry should point back to the governing task,
research log, progress-report triage row, or topic next-step; the steward runs
checks and records raw facts, while research interpretation still lands in the
paper/log/task as appropriate. See `topics/on-deck.md`.

**What to commit**:
- `research/<branchname>.md` and `research/<branchname>.log.md` — always commit when
  updated; these are the persistent record of the work.
- Source code changes — commit at checkpoints as above.
- Private `tasks/` and working-handoff files — do NOT commit. These are live
  working state shared among agents via the filesystem directly. Exception:
  only if the user explicitly asks to include them.

### Main task file: subtask tracking section

Every main task file (`tasks/NNN-<branchname>.md`) must contain a **Subtasks**
section that serves as the authoritative list of all work under this branch:

```markdown
## Subtasks

| NNN | Name | File | Status |
|-----|------|------|--------|
| 003 | first-subtask | tasks/003-first-subtask.md | In Progress |
| 004 | second-subtask | tasks/004-second-subtask.md | Not Started |
| —   | small inline check | (inline) | Not Started |

**Last subtask completed** (user confirmed): _(none yet)_
**Last subtask worked on**: 003-first-subtask
**Likely next**: small inline check, then 004-second-subtask
```

Rules for maintaining this section:
- List every subtask, whether it has its own file or is tracked inline.
- Update `Last subtask completed` only when the user explicitly confirms satisfaction.
- Update `Last subtask worked on` and `Likely next` at a significant continuity
  milestone when either field becomes materially false; do not interleave this
  bookkeeping with routine edit/run/check cycles.
- To find all subtask files for a branch:
  `rg -t md -l "Branch: <branchname>" tasks/`

### Research direction root (`research/ROOT.md`)

`research/ROOT.md` (when present) records the **current user direction** on
which project(s) are fruitful — the standing triage that governs autonomous
research and tending work (the "autoresearch" / "tend" context). It is a
recommended resume-context read: skim it before starting or continuing that
work so effort lands on a project the user still considers worth pursuing.

Create or edit it as the record evolves, but it encodes an **established**
direction: routine updates (adding detail, recording progress against the
existing priorities) need no permission, while reversing or replacing which
projects count as fruitful requires explicit user consent — not a unilateral
agent edit.

### Research document paths (derive from git branch name)

The git branch name IS the key. Given branch `logit-vs-merge-lora`:
- Research paper: `research/logit-vs-merge-lora.md`
- Research log:   `research/logit-vs-merge-lora.log.md`
- Main task file: `tasks/NNN-logit-vs-merge-lora.md` (where NNN is the task number)

If on a branch where `research/<branchname>.md` exists, there MUST be a corresponding
`tasks/NNN-<branchname>.md` main task file. If it is missing, alert the user.

When a fresh agent is asked to "update the research log" or "update the research paper",
it should run `git branch --show-current` to get the branch name, then write to
`research/<branchname>.log.md` or `research/<branchname>.md` respectively.

When resuming a session with `/hi`:
0. If `research/ROOT.md` exists, skim it for the current fruitful-project
   direction (see above) before choosing what to resume.
1. Recover the active root task and live state per `AGENTS.global.md` § Resume
   source priority (`tasks/ROOT`, `.agentctl/active/`, run metadata) — not a
   session summary.
2. Skim `research/<branchname>.md` (paper) for current framing, findings, and
   tables; if the governing task mentions a different paper path, skim that
   paper too.
3. Read the active root task — check its Subtasks section and any summary of
   what needs to be synced into the paper.
4. Read any in-progress subtask files it lists.
5. Check `research/<branchname>.log.md` for the most recent session's notes

Do not run this checklist for a fresh, specific request that lacks an explicit
`/hi` or resume signal; follow the AGENTS.md session-opening rule instead.
