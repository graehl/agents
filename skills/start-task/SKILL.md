---
name: start-task
description: Scaffold a new root task (point tasks/ROOT at it) and create a feature branch.
disable-model-invocation: true
argument-hint: "<short-description, e.g. auth-refactor>"
---

# Existing tasks
!`ls tasks/*.md 2>/dev/null | sort -t/ -k2 -n | tail -5`

# Instructions
1. Treat `$ARGUMENTS` as the desired task slug. Normalize it to lowercase
   kebab-case if needed, and use that slug for both the task filename suffix
   and the branch name.
2. Ensure `tasks/` exists. Determine the next task number by finding the
   highest-numbered `tasks/NNN-*.md` file and adding 1. Zero-pad to three
   digits. If no task files exist yet, start at `001`.
3. Create `tasks/NNN-<slug>.md` from scratch. Do not rely on
   `tasks/000-sample.md`.
4. Ask me for any missing background, constraints, and acceptance criteria.
   If I already gave enough context, proceed without re-asking.
5. Fill the new main task file with the current branch-task structure rather
   than old Claude-era sections. Include at least:
   - a title
   - `## Branch` with `<slug>`
   - `## Status`
   - `## Background`
   - `## Acceptance Criteria`
   - `## Current State`
   - `## Plan`
   - `## Risks`
   - `## Subtasks` with the required table and the three summary lines
6. Point the active-root-task pointer at the new file:
   `printf '%s\n' NNN-<slug>.md > tasks/ROOT` (git-ignored; see
   `AGENTS.md` § Session management). This step is independent of any
   branch.
7. Create and switch to branch `<slug>`. If that branch already exists, stop
   and ask whether to reuse it or choose a different slug.
8. Commit the new task file as the first commit on the new branch.
