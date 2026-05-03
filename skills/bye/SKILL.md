---
name: bye
description: Save a session summary and stop. Use when wrapping up a work session.
disable-model-invocation: true
allowed-tools: Bash(cat:*), Bash(find:*), Bash(ls:*), Bash(git:*), Write, Read
---

# Current state
- Branch: !`git branch --show-current`
- Uncommitted changes: !`git status --short`
- Recent commits this session: !`git log --oneline -5`

# Instructions

1. Interpret arguments:
   - Default (`/bye`, `bye`, or no explicit argument): overwrite
     `last-session.md` with the current work segment only. If a prior `/bye`
     happened earlier in this same chat and the user kept working without
     `/hi`, treat that prior `/bye` as a session boundary, as if the later work
     began from a fresh `/hi`. Do not preserve older `last-session.md` content
     merely because it exists.
   - Append (`/bye append`, `bye append`, or an equivalent explicit request):
     read the existing `last-session.md` first, then write a cumulative handoff
     that combines still-relevant prior summary content with the new work.
2. Read the active task file if one was being worked on (check tasks/*.md
   for any with Status: In Progress). Also search for related task files when
   `tasks/` exists, and cite them in `## Branch/Task Structure` and relevant
   next-step bullets.
3. Capture source-session metadata for the current agent/provider when
   available. Include a lightweight `## Source Session` section in
   `last-session.md` with session ID, provider, model, and a provider JSONL
   log path or logdir/glob hint for deeper transcript/debug detail. Make the
   session ID the stable grep key when possible, e.g. `grep -R <session-id>
   ~/.codex/sessions/**/*.jsonl` or search the matching Claude project logs
   under `~/.claude/projects/**/*.jsonl`. If a value is not available, write
   `unknown` rather than omitting the section.
4. Inspect `.agentctl/jobs/*/current.json` when present and capture the known
   jobs still marked `running`.
5. Write (project-root) `last-session.md` with exactly these sections:
   - `# Last Session`
   - `## Source Session`
   - `## Branch`
   - `## What We Did`
   - `## Commits Made This Session`
   - `## What's In Progress`
   - `## Immediate Next Steps`
   - `## Running Agentctl Jobs`
   - `## Branch/Task Structure`
   - `## Working Tree State`
   - `## Environment`
6. In `## Running Agentctl Jobs`, list each known running `agentctl` job with:
   - job name
   - serial and run id when present
   - log path
   - output/artifact path when present
   - the intended next step after that job completes
   Derive that next step from the current task/research plan, not from vague
   chat memory. Write it so a resumed agent can launch or monitor the successor
   action without rereading the whole conversation.
   If there are no known running `agentctl` jobs, write `None`.
7. `## Running Agentctl Jobs` is the persisted handoff for unfinished
   `agentctl` work. Keep it factual and current; do not list finished/stopped
   jobs there.
8. This file is consumed by `/hi`; treat it as the canonical resume handoff.
9. Write only the canonical summary content described above; do not append
   chat logs, tool traces, or unrelated scratch notes.
10. Keep entries concise and factual. Use bullets or numbering as appropriate.
11. In `## Immediate Next Steps`, put the single best next action first. If a
   running `agentctl` job blocks that action, say so and point to the relevant
   item in `## Running Agentctl Jobs`.
12. Include concrete file paths and commit hashes where relevant.
13. If a section has nothing to report, write `None`.
14. Stop after writing `last-session.md`.
