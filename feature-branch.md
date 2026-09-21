# Feature-branch supplement

This file is loaded only when a project opts in — its `AGENTS.md` names
this supplement, or the repo plainly uses a branch-per-feature (or
branch-per-task) workflow. Document-directory names do not select a branching
workflow. Without
this supplement the global instructions stay branch-agnostic and default
agent git behavior applies; the user does not use feature branches by
default.

It restores the branch-scoped rules that `AGENTS.global.md` omits and
points at the touchpoints that already assume a branch.

## Branch-scoped instruction routing

The global `## Instruction routing` maps `global rule` and
`project-level rule` only. When this supplement is active, add a third:

- `branch rule` -> the branch's governing gap or explicitly named handoff

A *branch rule* is direction that holds only for the current feature
branch — narrower than project-level, so it lives with that branch's governing
work artifact and retires when the branch merges.

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

- `_RESEARCH/workflow.md` — branch-derived paper/log names are fallbacks
  when the program has not declared canonical paths.
- `skills/ship` — squash-merges the current feature branch into one commit
  for upstream.
