---
name: hi
description: Pick up where the last session left off by reading the session summary.
disable-model-invocation: true
allowed-tools: Bash(cat:*), Bash(find:*), Bash(git:*), Bash(ls:*), Read
---

# Instructions

1. Read (project root or cwd) `last-session.md` written by `/bye`
   and prefer its exact section headings as the source of truth.
2. Validate the file shape before trusting details:
   - first heading must be `# Last Session`
   - all required `##` sections from `/bye` must be present
   - required sections include `## Running Agentctl Jobs`
   - if missing or contaminated, report mismatch and fall back to
     branch/task files, `.agentctl/jobs/*/current.json`, and git state as
     primary truth
3. Read the task file mentioned or in progress (check tasks/*.md)
4. Check current branch and git status to verify state matches
   what the summary expects
5. Report:
   - What was accomplished last time
   - What's in progress
   - What the recommended next step is
   - Which `agentctl` jobs are still known/running, and for each the
     persisted next step to take after it completes
6. If `## Running Agentctl Jobs` says `None`, say so explicitly. If it lists
   jobs, treat that section as the canonical persisted handoff for pending
   `agentctl` work and cross-check against `.agentctl/jobs/*/current.json`
   before trusting it.
7. Ask me how to proceed — do not start working automatically
