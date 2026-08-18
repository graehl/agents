# Tool surprises

> A tool surprise is a tool invocation that failed because the calling
> agent's model of the tool — flags, output form, schema, preconditions —
> was wrong; the tool-surprises skill and helper mine harness session
> logs for recurring surprise patterns and rank them for a real fix
> (tool option, helper, instruction, or environment).

Topic: `tool-surprises`

## The signal

Within one session, a failed call followed by a similar successful call
means the agent re-derived the tool's contract by retry, paying tokens
and latency. File-edit recoveries also match the target path when the
transcript exposes one, so an unrelated later edit does not count as the
fix. That adjacency recurring across sessions is the error-analysis
candidate this topic exists for: either the tool is hard to use (fix the
tool: an explicit option, a composite verb, a helper — see
`topics/agent-cli.md`), the agents' model of it is wrong (fix the
narrowest applicable instruction file), or the environment breaks an
assumption a governing doc makes (fix the setup or the doc).

Patterns with no recovery are ambiguous: tolerated-by-design nonzero
exits, deliberate probes, or unresolved gaps. The example pair
distinguishes them; the skill's workflow names the false-positive
classes to discount (answer-by-exit-code verbs, linters doing their
job, probes, harness gates).

The per-session decision — when an agent may tolerate an unexpected
output form versus stop and fix its understanding — is owned by
`AGENTS.global.md § Anti-slop implementation`. That rule's
second-surprise trigger is informal and per-agent; this topic's mining
is its systematic, retrospective complement.

## Data sources and coverage

Claude harness transcripts live at
`~/.claude/projects/<munged-root>/*.jsonl`, where the munged root is the
project path with `/` replaced by `-` (a `.` variant is also probed).
`tool_result` blocks with `is_error` mark failures; Bash failures carry
`Error: Exit code N` plus output, so exit codes are recoverable without
any runtime wrapper.

Codex rollouts live under `~/.codex/sessions/**/*.jsonl`. The miner
selects the project from `session_meta.payload.cwd`, records the model
from `turn_context`, and parses both rollout forms:

- direct `exec_command` / `apply_patch` calls, including terminal results
  retrieved through `write_stdin`; and
- newer `functions.exec` scripts, including patch-tool attribution and
  terminal results retrieved through `wait`.

Direct command results expose `Process exited with code N`. Most nested
`exec_command` calls inside `functions.exec`, however, serialize only
`r.output`; a surrounding `Script completed` does not prove that nested
command exited zero. The miner does not infer status from payload text.
Codex summaries therefore report
`custom_exec_scripts_with_opaque_command_status` beside direct-call and
terminal-event counts. Treat Codex shell-failure totals as a lower bound
when that coverage count is nonzero. This observed loss activates the
telemetry alternative in
[tool-surprises.sketches.md](tool-surprises.sketches.md).

For either harness, the current session is excluded unless
`--all-sessions`. Claude `is_error` and Codex nonzero exits still
conflate answer-by-exit-code verbs with genuine failures — hence the
manual discount step.

## Components

- `scripts/tool-surprises` — ACLI miner for Claude and Codex. Flags:
  `--project`, `--harness`, `--days`, `--limit`, `--min-fails`,
  `--all-sessions`, `--include-gated`, plus the standard output flags.
  Emits a `summary` row then `pattern` rows (tool, signature, error
  class, fails, recovered, sessions, example fail→fix pair). Codex
  summaries also carry coverage diagnostics. Exit codes: 0 report
  emitted, 2 usage, 4 no transcript directory.
- `skills/tool-surprises/SKILL.md` — the reporting workflow: run,
  discount false positives, classify remediation, report with
  evidence. Instruction changes it motivates go through
  `topics/agent-instructions.md` discipline rather than being applied
  inline.
