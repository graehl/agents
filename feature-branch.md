# Feature-branch supplement

This file is loaded only when a project opts in — its `AGENTS.md` names
this supplement, or the repo plainly uses a branch-per-feature (or
branch-per-task) workflow. Tracked `tasks/` (not git-ignored) is the
signal this applies; git-ignored `tasks/` is the default, where task
files stay private and uncommitted and work is branch-agnostic. Without
this supplement the global instructions stay branch-agnostic and default
agent git behavior applies; the user does not use feature branches by
default.

It restores the branch-scoped rules that the global `AGENTS.md` omits and
points at the touchpoints that already assume a branch.

## Branch-scoped instruction routing

The global `## Instruction routing` maps `global rule` and
`project-level rule` only. When this supplement is active, add a third:

- `branch rule` -> the branch's main task file `tasks/NNN-<branch>.md`

A *branch rule* is direction that holds only for the current feature
branch — narrower than project-level, so it lives with that branch's task
file and retires when the branch merges.

## Worktree transfers across branches

Reinforces `# Ancillary workdir hygiene`: before transferring content
between worktrees, verify the source and destination branches match —
moving uncommitted work onto the wrong branch is an easy footgun. A
committed (or stashed) state is still the only safe transfer unit. The
global rule already requires the committed-state part; this adds the
branch-match check for multi-branch work.

## Touchpoints that already assume a branch

These need no change when this supplement is active — they are branch-aware
already, and become relevant only under a branch workflow:

- `RESEARCH.md` `## Task and branch structure` — each main task owns a
  git branch and `research/<branchname>.md` + `.log.md` companions keyed
  to the branch name.
- `skills/start-task` — scaffolds the task file and creates/switches to
  the feature branch.
- `skills/review` — diffs the current branch against its resolved base
  (`skills/ship/base-branch.sh`) before merge.
- `skills/ship` — squash-merges the current feature branch into one commit
  for upstream.
