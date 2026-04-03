---
description: Review the current branch diff for issues before merging
allowed-tools: Bash(git:*), Bash(cat:*)
argument-hint: <task-number, e.g. 017>
---
## argument hint

- if a `tasks/NNN-taskname.md` NNN or name argument, confirm we're on a git branch w/ commits accomplishing the task before continuing (i.e. stop if there's not a match).

## Base branch

- Base branch: !`sh .claude/scripts/base-branch.sh` (usually `master`)

## git diff format

Use `git --no-pager diff --no-color --no-ext-diff` to avoid nonstandard visual `git diff`

## Changes to Review

!`git --no-pager diff --no-color --no-ext-diff --name-only master...HEAD`

## Detailed Diff

!`git --no-pager diff --no-color --no-ext-diff master...HEAD`

Review the above changes for:
1. Code quality issues
2. Security vulnerabilities
3. Missing test coverage
4. Performance concerns
5. Unnecessary (optional) tech-debt/refactoring changes (but not typo/doc/auto-format/whitespace); amend the commit message to characterize these in a single line at the end (but before any `Change-Id` line).
6. Change-Id: there should be one Change-Id: line at most and it should be at the end. This is for gerrit; let our git hooks add the id if not already present. Never add text after a Change-Id line (add it before)

Give specific, actionable feedback per file.
