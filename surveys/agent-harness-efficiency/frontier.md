# Frontier: agent harness efficiency

Mode: grounded, 2026-09-30, on top of [survey.md](survey.md). Depth:
**analysis only**, meaning a ranked void map and candidates with no drafted
proposals. The user plans to move experimentation into a `draft` program
later. Revisit dates are unscheduled reminders, not `at/` entries.

## Provisional claim inbox

### Codex's same-model advantage is trained tool fit

- **Claim.** GPT-5.x beats neutral harnesses by 5–22 points on
  Terminal-Bench only inside Codex because the models are post-trained on
  Codex's tool shapes: `apply_patch`, shell tool, and code-mode `exec` for
  Sol and Astra.
- **Evidence.** The operator-run deltas (survey §B1) plus OpenAI's
  "trained to excel at this diff format". The mechanism has only been
  demonstrated on small models (§D1).
- **Confounds.** Codex also differs in loop, compaction and delegation, and
  the one tie (GPT-5-Codex +0.9) cuts against a pure tool-fit story.
- **Cheapest discriminating check.** Same GPT model, same neutral harness,
  toggling only the edit tool. pi with and without pi-lovely-codex is almost
  exactly that. Revisit 2026-12.

### Claude Code's Terminal-Bench 2.0 deficit was an environment artifact

- **Claim.** The deficit came from KillShell's missing `ps` dependency
  (Z.ai).
- **Evidence.** Supported by the 2.1 rerun: Claude Code +12.1, Terminus 2
  +0.9.
- **Open.** Terminus 2 was never rerun under Z.ai's other fixes. Revisit
  when an operator-run board pairs harnesses again.

### No average native premium on a contamination-controlled suite

- **Claim.** `arjmandi2026harnessormodel` finds none, for either Opus 4.8
  or GPT-5.5.
- **Limits.** Single author, 80 tasks; one repo-versus-contest interaction
  flagged as post hoc; the Opus billing is unresolved.
- **Relevance.** This is the strongest counterweight to the Terminal-Bench
  reading. Revisit on replication.

### Context overhead from a large skill menu is about zero

- **Claim.** `song2026skillshadowing` finds wrong-skill selection, not
  length, explains the drop at 202 skills.
- **Relevance.** This decides whether this host should trim skills catalogs
  (1.3k–7.1k tokens) or filter them.
- **Cheapest check.** Hold the catalog's selection fixed and pad its length.
  Revisit 2026-12.

## Void map

Axes: harness (native / neutral-minimal / Copilot / pi + extension / native
through `copilot-api`) × model (Opus/Sonnet 5.x, Sol, Astra, Grok 4.x) ×
metric (fixed context / success / billed $ per solve). Cells for current
models:

| harness \ model, metric | Claude 5.x success | Claude 5.x $/solve | Sol/Astra success | Sol/Astra $/solve | Grok success |
|---|---|---|---|---|---|
| native CLI | filled (Terminal-Bench 2.1/4.0, AA index) | filled (Terminal-Bench 2.1, AA) | filled (Terminal-Bench 3.0/4.0, AA) | filled | filled (Grok Build, Terminal-Bench 3.0/4.0) |
| neutral minimal (Terminus 2 / mini-SWE-agent) | filled (Terminal-Bench 2.1, Opus 4.7 / Fable 5) | filled | untried for Sol/Astra | untried | untried |
| Copilot CLI / VS Code agent | untried (stale: LiveSWEBench 3.7) | untried | untried | untried | untried |
| pi (± lovely-codex) | untried | untried | untried (GPT-5 pentest only) | untried | untried |
| native harness via `copilot-api` | untried | untried (cache survival unmeasured) | not possible: Codex needs `/v1/responses` | — | — |
| Claude Code driving a foreign model | tried-failed for open models (Harbor: 4–6× cost) | tried-failed | untried for GPT | untried | untried |

Fixed context is filled for all five installed harnesses by the local
capture, except VS Code agent mode and Grok Build.

## Capstone candidates (ranked)

1. **Same-model harness A/B for Sol and Astra: Codex versus pi versus pi
   with lovely-codex versus Copilot CLI.**
   - Measure billed cost per solve on a fixed Terminal-Bench 2.1 subset or
     private tasks.
   - Impact: high. It decides the user's harness for the models used most,
     and it tests the tool-fit claim above.
   - Tractability: high. Every harness is installed, and pi and Codex both
     accept the same model.
   - Novelty confidence: high. Tracks A, B and D found no Sol or Astra
     cross-harness pair, and the only pi-versus-Codex result is GPT-5
     pentest.
   - Prior art checked: arXiv `"Codex" AND pi`, `native harness`,
     `cross-harness`; Terminal-Bench, AA and HAL boards; pi.dev packages.
2. **Instruction-prefix ablation across harnesses.**
   - Compare the 15.6k compiled boot against a trimmed boot on fixed tasks,
     measuring success, tokens and billed cost.
   - Impact: high for this repository, whose design objective asks for
     measured ablation by model and harness; see
     `gaps/instruction-guidance-evolution-testbed.md`.
   - Tractability: medium, needing enough runs to beat 2–6 points of run
     noise.
   - Novelty confidence: medium. AGENTS.md studies cover repository context
     files, not a global behavioral policy.
   - Prior art checked: `"AGENTS.md"`, `"context files"`, `"system prompt"
     AND "coding agent"`.
3. **Copilot transport probe.**
   - Bound the server-side prompt through reported versus local usage, and
     check cache-read survival through the fork's Anthropic passthrough.
   - Impact: medium; tractability: trivial once the quota resets (script
     exists).
   - Novelty confidence: high for this specific proxy.
   - Prior art checked: VS Code #254959 and #312940, openclaw #60174.
4. **Claude Code driving Sol or Astra through the gateway versus Codex.**
   - This measures the foreign-harness penalty for GPT.
   - Impact: medium; tractability: high. Harbor's open-model result predicts
     a penalty. Novelty confidence: high.
