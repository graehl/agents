# Agent Instructions

Reusable operating instructions for coding agents in filesystem-first software
and research projects.

This is not an app or framework. It is a compact policy bundle for agents that
work inside real project directories, inspect local files, respect dirty
worktrees, run commands, track jobs, and leave durable evidence for the next
session.

## Start Here

- `AGENTS.md` - global operating contract for developer agents.
- `RESEARCH.md` - research, eval, and paper discipline.
- `RUNS.md` - long-running jobs, GPU use, and run provenance.
- `TOPICS.md` / `topic-definitions.md` - topic vocabulary and curated jargon.
- `skills/` - reusable workflows for handoff, review, task start, and shipping.

Private machine-local preferences live outside public committed instructions;
in this setup, that means `AGENTS.user.md`.

## Why These Instructions?

`AGENTS.md` is written for continuity across agent sessions. It tells agents
to:

- verify project claims against the repo;
- preserve unrelated WIP in dirty trees;
- route global, project, and branch rules to durable files;
- write commits that preserve motivation and decisions;
- use task files and topic docs as working memory;
- record provenance for research and long-running runs.

It can also stand alone as a repo-local `AGENTS.md` or `CLAUDE.md`.

## Roles

- **Developer:** inspect first, edit narrowly, verify, commit cleanly.
- **Researcher:** maintain experiment logs, eval splits, artifact provenance,
  and paper-facing claims for intellectually honest, reproducible public
  results.
- **Run operator:** launch, monitor, and summarize agent-driven jobs so
  long-running work survives handoff.

The common assumption is a real filesystem working tree: source, tasks, logs,
artifacts, and git history are available for agents to inspect.
