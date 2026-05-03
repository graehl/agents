---
name: hi
description: Pick up where the last session left off, preferring live state and prior agent logs when the summary may be stale.
disable-model-invocation: true
allowed-tools: Bash(cat:*), Bash(find:*), Bash(git:*), Bash(ls:*), Bash(rg:*), Bash(sed:*), Bash(stat:*), Bash(tail:*), Read
---

# Instructions

1. Decide whether `last-session.md` is likely fresh enough to trust:
   - If the user provided a handoff/extract/continues log, says the previous
     session disconnected, crashed, full-restarted, or context-compacted in a
     way that may have dropped live details, or otherwise implies `/bye`
     probably did not run, presume `last-session.md` is stale.
   - Also treat it as stale when live task files, `.agentctl` jobs, artifact
     metadata, or git state are clearly newer than it.
   - Concrete stale/missing `/bye` signs include: no `last-session.md`; mtime
     older than recent task/worktree/artifact/job updates; missing expected
     `# Last Session` / `## Running Agentctl Jobs` structure; listed jobs that
     do not match `.agentctl`; no mention of currently running jobs; no mention
     of recently modified task files; or user language indicating a disconnect,
     browser crash, full restart, context compaction, or "last session did not
     save/commit".
   - In stale-summary cases, recover from current worktree/task state, live
     `.agentctl`/artifact metadata, and then platform-wide JSONL session logs
     before using `last-session.md`. Treat `tasks/` files as live state even
     when untracked or ignored by git.
2. For stale-summary recovery, inspect the platform-wide logs for the dead
   ancestor session when practical. This is primarily needed when
   `last-session.md` is not fresh relative to worktree state, task mtimes, live
   jobs, or artifact metadata:
   - Codex: recent `~/.codex/sessions/**/*.jsonl` files, usually selecting by
     timestamp and current working directory references.
   - Claude: matching project logs under `~/.claude/projects/**/*.jsonl`
     (project path is usually encoded in the directory name).
   - Summarize only the relevant recent actions, running jobs, and next-step
     cues; do not bulk-load unrelated long histories.
3. If `last-session.md` still appears authoritative, read the project-root or
   cwd copy written by `/bye` and prefer its exact section headings as the
   source of truth.
4. Validate the file shape before trusting details:
   - first heading must be `# Last Session`
   - all required `##` sections from `/bye` must be present
   - required sections include `## Running Agentctl Jobs`
   - if missing or contaminated, report mismatch and fall back to
     branch/task files, `.agentctl/jobs/*/current.json`, artifact metadata,
     agent JSONL logs, and git state as primary truth
5. Read the task file mentioned or in progress. If `tasks/` exists, sort
   `tasks/*.md` by modification time and inspect the newest relevant subtasks;
   do this even when `tasks/` is not part of the git repository.
5a. If `RESEARCH.md` exists and the repository/task indicates research workflow
    (for example `research/` or `tasks/` layout), read `RESEARCH.md`.
5b. If `RUNS.md` exists and there are active/pending job indicators (for
    example `.agentctl/` or `*.running.md`), read `RUNS.md`.
6. Check current branch and git status to verify state matches
   what the summary expects
7. Report:
   - What was accomplished last time
   - What's in progress
   - What the recommended next step is
   - Which `agentctl` jobs are still known/running, and for each the
     persisted next step to take after it completes
8. If `## Running Agentctl Jobs` says `None`, say so explicitly. If it lists
   jobs, treat that section as the canonical persisted handoff for pending
   `agentctl` work and cross-check against `.agentctl/jobs/*/current.json`
   before trusting it. In stale-summary mode, do not let a stale `None`
   override live `.agentctl` state or newer run metadata.
9. Ask me how to proceed — do not start working automatically
