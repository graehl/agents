# Tool surprises — sketches

Candidate futures, not current guidance (`topics/topic-doc-format.md`
§ Companions).

## Command-invocation telemetry wrapper (reactivated 2026-08-18)

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

**Why it was postponed.** Transcript scraping
(`scripts/tool-surprises`) yields the fail→fix signal for Claude
sessions with zero runtime overhead and no new mandate touching every
command. A mandatory wrapper adds per-command latency and failure
surface, needs per-harness deployment, and duplicates data the Claude
transcripts already hold.

**Why it is active again.** The Codex loader can recover direct
`exec_command` exits, but newer `functions.exec` scripts commonly emit
only a nested call's `r.output`. In a 30-day sample on 2026-08-18,
5,093 of 6,340 custom scripts in `~/agents` and 35,838 of 47,527 in Yep
Anywhere had opaque nested command status. The surrounding `Script
completed` reports JavaScript completion, not the nested command's exit
code. Retrospective mining therefore undercounts Codex shell failures
materially.

Evaluate a harness-level result-serialization change before imposing a
wrapper: retaining each nested call's exit code would repair the
existing log source without adding a second mandatory command path. A
shared wrapper remains the fallback if harness telemetry cannot expose
that status, and live in-session detection remains a separate reason to
adopt it. Do not spend boot-instruction context telling every Codex
agent to print `r.exit_code` solely for retrospective analytics.

## Codex patch-context instruction candidate (surveyed 2026-08-18)

Thirty-day, same-target fail→success results after discounting unrelated
later patches:

| Harness / project | Sessions | Calls | Anchor failures | Recovered | Sessions hit |
|---|---:|---:|---:|---:|---:|
| Codex / `~/agents` | 45 | 7,491 | 69 | 64 | 25 |
| Codex / Yep Anywhere | 190 | 63,727 | 277 | 276 | 79 |
| Claude / `~/agents` | 58 | 8,269 | 38 | 37 | 12 |
| Claude / Yep Anywhere | 148 | 36,219 | 97 | 89 | 43 |

The Codex pattern crosses a general instruction repository and an
application repository, so a Yep Anywhere-only patch would be
mis-scoped. A strict pass over raw Codex patch-verification errors also
found that most failures already followed a same-file shell call (60 of
65 in `~/agents`, 262 of 280 in Yep Anywhere). Before the next
successful patch call, 52 of 54 and 213 of 216 intervening shell calls,
respectively, mentioned that same file. Requiring only a reread *after*
failure describes the common recovery; it does not prevent the first
miss.

**Candidate hierarchy.** Keep the cross-tool invariant in
`AGENTS.global.md § Edit anchors: copy, don't compose`: exact-match edit
source and context come from current file output, and another writer or
formatter invalidates that evidence. Put the patch-tool projection in
`AGENTS.codex.md`: construct each `apply_patch` hunk by copying exact,
minimal current context rather than composing whitespace or surrounding
lines. This is a proposal for a later instruction-authoring pass, not
current guidance. Measure the same counts after adoption before keeping
or expanding the boot text.

## Codex stale-handle candidates (surveyed 2026-08-18)

Handle-aware matching found 26 `write_stdin` failures across 18 Yep
Anywhere sessions and 12 `wait` failures across 12; none recovered on
the same process or cell. `~/agents` added one `write_stdin` failure.
This is distinct from ordinary command nonzero exits.

Eleven of the 12 stale `wait` calls followed an already-terminal result
for the same cell. A narrow `AGENTS.codex.md` candidate is therefore:
a terminal `wait` result consumes that cell id; do not wait on it again.
Verify the remaining event before deciding whether the instruction needs
an exception or more detail.

The `write_stdin` group is not the same agent mistake. One representative
sequence received a live process id from `exec_command`, then the first
poll returned `Unknown process id` without a terminal result. Prefer a
harness/tool repair that retains and returns a process's terminal status
for a bounded period (or an explicit expired-result state) instead of a
boot instruction that asks the agent to predict the race.

## Yep Anywhere screenshot-path guidance gap (surveyed 2026-08-18)

Codex recorded 53 `view_image` missing-path failures across 38 Yep
Anywhere sessions; 31 later reached the same path successfully. A
representative trace followed the project's Playwright fallback shape:
it passed a relative `.artifacts/...` output to
`pnpm --filter @yep-anywhere/client exec playwright`, then tried to read
that path from the repository root. `pnpm --filter ... exec` ran the
command in the client package, so the capture landed under
`packages/client/.artifacts/...` instead.

This is project guidance, not a Codex or global boot-rule gap. Revise the
fallback recipes in Yep Anywhere's `CLAUDE.md § Browser Control (UI
Testing)` and `topics/ui-testing.md § Recommended automation` to derive
an absolute artifact directory from the repository root before invoking
the filtered package command. Re-run the survey afterward; do not add a
general instruction compensating for a misleading project recipe.
