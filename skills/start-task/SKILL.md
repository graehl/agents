---
name: start-task
description: Scaffold a new task and create a feature branch.
disable-model-invocation: true
argument-hint: "<short-description, e.g. auth-refactor>"
---

# Existing tasks
!`ls tasks/*.md 2>/dev/null | sort -t/ -k2 -n | tail -5`

# Instructions
1. Determine the next task number by finding the highest-numbered
   file in tasks/ and adding 1. Zero-pad to three digits.
2. Create `tasks/NNN-$ARGUMENTS.md` from tasks/000-sample.md
3. Ask me for background, constraints, and acceptance criteria
4. Fill in the Claude sections (current state, files, steps, risks)
5. Create branch `task/NNN-$ARGUMENTS`
6. Commit the new task file as the first commit on the branch.

