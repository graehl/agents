---
name: review
description: Review the current branch diff for issues before merging
allowed-tools: Bash(git:*), Bash(cat:*)
argument-hint: <task-number, e.g. 017>
---
## argument hint

- if a `tasks/NNN-taskname.md` NNN or name argument, confirm we're on a git branch w/ commits accomplishing the task before continuing (i.e. stop if there's not a match).

## Base branch

Use `~/agents/skills/ship/base-branch.sh` to resolve the review base branch.
Contract:
- use the repo's remote default branch when `origin/HEAD` is configured
- otherwise use whichever of `main` or `master` exists
- fail if neither or both exist without a remote default

If the helper cannot be executed, returns an empty value, or names a branch
that does not exist, ask the user which branch to diff against before
continuing.

## git diff format

Use `git --no-pager diff --no-color --no-ext-diff` to avoid nonstandard visual `git diff`

Review the above changes for:
1. Code quality issues
2. Security vulnerabilities
3. Missing test coverage
4. Performance concerns
5. Unnecessary (optional) tech-debt/refactoring changes (but not typo/doc/auto-format/whitespace); amend the commit message to characterize these in a single line at the end (but before any `Change-Id` line).
6. Change-Id: there should be one Change-Id: line at most and it should be at the end. This is for gerrit; let our git hooks add the id if not already present. Never add text after a Change-Id line (add it before)

Before reviewing, resolve the base branch and run:
- `git --no-pager diff --no-color --no-ext-diff --name-only <base>...HEAD`
- `git --no-pager diff --no-color --no-ext-diff <base>...HEAD`

Give specific, actionable feedback per file.
