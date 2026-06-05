---
name: start-task
description: Scaffold a new root task — create the task file and point tasks/ROOT at it.
argument-hint: "<short-description, e.g. auth-refactor>"
---

# Existing tasks
!`ls tasks/*.md 2>/dev/null | sort -t/ -k2 -n | tail -5`

# Customization point
!`git check-ignore -q tasks && echo "tasks/ is git-ignored → private working state (default: no commit, no branch)" || echo "tasks/ is tracked → feature-branch workflow (commit task file; branch per task)"`

# Instructions
1. Treat `$ARGUMENTS` as the desired task slug; normalize to lowercase
   kebab-case.
2. Ensure `tasks/` exists. Next task number = highest `tasks/NNN-*.md` + 1,
   zero-padded to three digits (start at `001` if none).
3. Create `tasks/NNN-<slug>.md` from scratch (do not rely on any sample).
4. Ask me for any missing background, constraints, and acceptance criteria;
   if I already gave enough, proceed without re-asking.
5. Fill the task file with at least: a title, `## Status`, `## Background`,
   `## Acceptance Criteria`, `## Current State`, `## Plan`, `## Risks`, and
   `## Subtasks` (the required table and three summary lines).
6. Point the active-root-task pointer at the new file:
   `printf '%s\n' NNN-<slug>.md > tasks/ROOT` (see `AGENTS.md` § Session
   management). If `tasks/ROOT` already names a different, unfinished task,
   say so and confirm before redirecting it.

Whether `tasks/` is git-ignored is the customization point:
- **Ignored (default for these projects):** task files and `tasks/ROOT` are
  private working state — do **not** commit them, and do **not** create or
  switch branches unless I explicitly ask.
- **Tracked:** the feature-branch workflow applies — add `## Branch` with
  `<slug>` to the task file, create and switch to branch `<slug>` (if it
  already exists, stop and ask whether to reuse it), and commit the new task
  file as the branch's first commit.
