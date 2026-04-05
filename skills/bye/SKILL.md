---
name: bye
description: Save a session summary and stop. Use when wrapping up a work session.
allowed-tools: Bash(cat:*), Bash(git:*), Write, Read
---

# Current state
- Branch: !`git branch --show-current`
- Uncommitted changes: !`git status --short`
- Recent commits this session: !`git log --oneline -5`

# Instructions

1. Read the active task file if one was being worked on (check tasks/*.md
   for any with Status: In Progress)
2. Write (project-root) `last-session.md` with exactly these sections:
