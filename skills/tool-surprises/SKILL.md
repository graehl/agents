---
name: tool-surprises
description: Mine a project's harness session logs for recurring tool-invocation failure patterns — a failed call followed by a similar successful one marks a tool contract the agent re-derived by retry — then rank them and propose remediations (tool option, helper script, instruction fix, or environment fix). Use when the user invokes /tool-surprises, asks what commands or tools keep failing, mentions "tool surprises", or asks for command-crafting error analysis.
---

# /tool-surprises — mine session logs for failing command patterns

Reports recurring tool-invocation failures across a project's past
sessions and turns the systematic ones into remediation candidates.
The unit of interest is the fail→fix pair: a failed call followed in
the same session by a similar call that succeeded means the agent
corrected its model of the tool by retry, at token cost. The same
pair recurring across sessions is an error-analysis candidate — the
tool is hard to use, the instructions are missing a line, or the
environment is broken. Background and promotion criteria:
`topics/tool-surprises.md`.

## Workflow

1. **Resolve the project root**: the named `--project`, else
   `git rev-parse --show-toplevel`, else cwd.

2. **Run the helper** (canonical source `~/agents/scripts/tool-surprises`):

   ```bash
   ~/agents/scripts/tool-surprises --project "$root" --harness claude
   ~/agents/scripts/tool-surprises --project "$root" --harness codex
   ```

   Run either line for one harness or both for a cross-harness survey.
   Useful knobs: `--days N` to bound the window, `--min-fails`
   (default 2), `--limit` (default 20; dropped rows are counted in
   the summary), `--full` for untruncated examples and model/session
   lists, `--include-gated` to include user-interrupt/approval rows.
   In a Codex summary, a nonzero
   `custom_exec_scripts_with_opaque_command_status` coverage count
   means nested shell exits were not serialized; report shell-failure
   totals as lower bounds rather than guessing from output text.

3. **Discount the false-positive classes** before reporting. A
   nonzero exit is not always a surprise:

   - answer-by-exit-code verbs (`agentctl others`/`alone`, `rg`/
     `grep` with no match) — the exit code is the answer;
   - lint/test tools whose nonzero exit is them working (a
     `commit-msg-lint` rejection is a caught draft, not a stumble);
   - deliberate probes (`ls` of maybe-missing paths, existence
     checks with `2>/dev/null` fallbacks);
   - harness gates and user interrupts (excluded by default).

   `recovered=0` patterns are usually one of these — or an
   unresolved gap; read the example to tell which.

4. **Classify each real pattern's remediation**:

   - **tool** — hard to invoke correctly: add/point to an explicit
     option, a named composite verb, or a helper script
     (`topics/agent-cli.md` conventions);
   - **instruction** — a wrong or missing agent model of the tool:
     a line in the narrowest applicable file (harness or model
     supplement, language topic, or `AGENTS.global.md`), authored
     under `topics/agent-instructions.md` discipline — propose it,
     with the pattern counts as evidence, rather than editing in the
     same breath;
   - **environment** — missing binary or wrong PATH: setup fix or a
     host note where the governing doc assumes the tool exists;
   - **accept** — tolerated by design; the per-session bar is
     `AGENTS.global.md § Anti-slop implementation` (second surprise
     from the same tool ends tolerance — this skill is that rule's
     systematic detector).

5. **Report**: the summary line (calls, failures, sessions), a
   compact table (fails / recovered / sessions / tool / signature /
   class), and one recommendation per surviving pattern with its
   example fail→fix pair. Name what was discounted and why.
