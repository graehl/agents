---
name: ship
description: Squash-merge current feature branch into a single commit for Gerrit, deriving the message from the task file.
disable-model-invocation: true
allowed-tools: Bash(git:*), Bash(cat:*)
argument-hint: <task-number, e.g. 017>
---

# Context
- Current branch: !`git branch --show-current`
- Upstream-base branch: use `~/agents/skills/ship/base-branch.sh`
  Contract:
  - prefer the remote default branch from `origin/HEAD`
  - otherwise use whichever of `main` or `master` exists
  - if the helper fails, returns empty, or names a missing branch, ask the user
- Commits on branch vs base: after resolving the base branch, inspect
  `git log --oneline <base>..HEAD`
- Task file content: (read tasks/$ARGUMENTS-*.md)
- merge-base branch: (common ancestors of the current and upstream-base); we will create a single commit for upstream from our changes since merge-base
- User pushes upstream (not claude!).

# Instructions
0. Resolve the upstream-base branch with `~/agents/skills/ship/base-branch.sh`.
   If the helper cannot be executed, returns an empty value, or names a branch
   that does not exist, ask the user which base branch to use.
1. `git fetch origin`; if `origin/upstream-base` has moved from our merge-base and a rebase or merge would have conflicts, *STOP* and ask permission to rebase + fix conflicts.
2. Read `tasks/*$ARGUMENTS*.md` (glob the number prefix) and confirm we are in a local branch where we've implemented it. If not, *STOP*. If we are in the right branch, and state is dirty, commit all changes in the local branch (amend if trivial and we already have a local commit).
3. Generate the upstream commit message:
   - Subject: one-line summary of what the task accomplished; include (possibly revised for creep) the task description but not any `NNN-` prefix; if there are JIRA tickets referenced in the description (e.g. `AIP-2345`) then the commit message should start with that.
   - Body: key architectural decisions, relevant background
   - Omit implementation checklists and step-by-step progress but call out in one line any major code changes that are not directly in service of the task e.g. 'Also, refactor XXX.hpp.'
4. Verifying that our local branch `branchname` state is clean (*STOP* if not), create `branchname-review` where we will craft a single commit for upstream; forcibly rename `branchname-review` to `branchname-review.bak` if it exists and create (and switch to) `branchname-review`, i.e. overwrite it with a single backup. Then `git reset --soft` to the merge-base so we can make the commit.
5. Run `git commit` with the generated message; exclude the tasks/ files or any claude-related artifacts (the task file is committed in my local branch but should not hit the shipped branch)
6. Show me the generated message and follow on with any code review comments/questions for me (do not include these in the commit message)
7. At this point we are in `branchname-review` with a single commit added to the upstream base branch. Do NOT push — I will `git push` to Gerrit myself
