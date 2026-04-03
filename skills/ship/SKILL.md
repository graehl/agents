---
name: ship
description: Squash-merge current feature branch into a single commit for Gerrit, deriving the message from the task file.
disable-model-invocation: true
allowed-tools: Bash(git:*), Bash(cat:*)
argument-hint: <task-number, e.g. 017>
---

# Context
- Current branch: !`git branch --show-current`
- Upstream-base branch: !`git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's|origin/||' || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' || echo master`
  (usually `master`)
- Commits on branch vs main: !`git log --oneline master..HEAD`
- Task file content: (read tasks/$ARGUMENTS-*.md)
- merge-base branch: (common ancestors of the current and upstream-base); we will create a single commit for upstream from our changes since merge-base
- User pushes upstream (not claude!).

# Instructions
0. `git fetch origin`; if `origin/upstream-base` has moved from our merge-base and a rebase or merge would have conflicts, *STOP* and ask permission to rebase + fix conflicts.
1. Read `tasks/*$ARGUMENTS*.md` (glob the number prefix) and confirm we are in a local branch where we've implemented it. If not, *STOP*. If we are in the right branch, and state is dirty, commit all changes in the local branch (amend if trivial and we already have a local commit).
2. Generate the upstream commit message:
   - Subject: one-line summary of what the task accomplished; include (possibly revised for creep) the task description but not any `NNN-` prefix; if there are JIRA tickets referenced in the description (e.g. `AIP-2345`) then the commit message should start with that.
   - Body: key architectural decisions, relevant background
   - Omit implementation checklists and step-by-step progress but call out in one line any major code changes that are not directly in service of the task e.g. 'Also, refactor XXX.hpp.'
3. Verifying that our local branch `branchname` state is clean (*STOP* if not), create `branchname-review` where we will craft a single commit for upstream; forcibly rename `branchname-review` to `branchname-review.bak` if it exists and create (and switch to) `branchname-review`, i.e. overwrite it with a single backup. Then `git reset --soft` to the merge-base so we can make the commit.
4. Run `git commit` with the generated message; exclude the tasks/ files or any claude-related artifacts (the task file is committed in my local branch but should not hit the shipped branch)
5. Show me the generated message and follow on with any code review comments/questions for me (do not include these in the commit message)
6. At this point we are in `branchname-review` with a single commit added to the upstream base branch. Do NOT push — I will `git push` to Gerrit myself
