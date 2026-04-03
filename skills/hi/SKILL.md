---
name: hi
description: Pick up where the last session left off by reading the session summary.
disable-model-invocation: true
allowed-tools: Bash(cat:*), Bash(git:*), Read
---

# Instructions

1. Read (project root or cwd) `last-session.md`
2. Read the task file mentioned or in progress (check tasks/*.md)
3. Check current branch and git status to verify state matches
   what the summary expects
4. Report:
   - What was accomplished last time
   - What's in progress
   - What the recommended next step is
5. Ask me how to proceed — do not start working automatically
