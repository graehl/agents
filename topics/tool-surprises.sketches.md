# Tool surprises — sketches

Candidate futures, not current guidance (`topics/topic-doc-format.md`
§ Companions).

## Command-invocation telemetry wrapper (postponed 2026-08-18)

**Proposal.** Route every agent shell command through a thin wrapper —
or a harness hook — that appends one JSONL record per invocation to a
standard location: project, harness, model, session id, argv, exit
code, duration. Fail→success adjacency then becomes computable
token-free, uniformly across harnesses, with no transcript parsing.
Candidate schema:

```json
{"ts": "...", "project": "...", "harness": "claude", "model": "...",
 "session": "...", "argv": ["git", "push"], "exit": 1, "ms": 240}
```

Plausible wiring: extend `agent-guarded` or the YA `BASH_ENV` bridge;
store under `~/.local/state/agents/tool-log/` or per-project
`.agentctl/`.

**Also considered and set aside.** A standard hand-maintained
surprise-report location (project, model, tool, relevant options and
inputs, expected output, remediation applied): costly and
context-distracting to maintain per incident; the wrapper or the log
scrape recovers most of the same facts for free.

**Why postponed.** Transcript scraping (`scripts/tool-surprises`)
already yields the fail→fix signal for Claude sessions with zero
runtime overhead and no new mandate touching every command. A
mandatory wrapper adds per-command latency and failure surface, needs
per-harness deployment, and duplicates data the transcripts already
hold.

**What would change the answer.** Scraping proving too lossy (exit
codes or argv unavailable in some harness's logs); wanting
cross-harness aggregation where per-harness loaders cost more than one
shared wrapper; or wanting live in-session surprise detection rather
than retrospective mining.
