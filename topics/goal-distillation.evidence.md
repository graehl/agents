# goal-distillation — verification evidence

Field observations, mechanism findings, and the agent's own notes on
goal-conditioned agents and the `/goal`-style loop — the training-time
companion to [`goal-distillation.md`](goal-distillation.md) and the
inference-time [`wish`](../skills/wish/SKILL.md) skill. Convention:
`topics/evidence-ledger.md`. Not loaded routinely; consult when working on
the topic. Append new entries at the top; do not rewrite prior ones.

## 2026-05-29 — Codex `/goal` mechanism: persistence is orchestration, not an attention slot

A gpt5.5 session in `~/ya`, given a Codex `/goal` objective ("explain the
/goal feature and whether it is tuned to have any attention bearing on
'keep going for the goal'"), reported the mechanism by introspecting its
own runtime state. Captured as a worked example of how a built-in goal
loop actually carries the goal — i.e. what `wish` hand-rolls in a contract
file, Codex does in the runtime.

What the agent could **observe** in-session:
- `/goal` creates **persistent external goal state**, and the runtime
  **reinjects a structured `<goal_context>` on continuation turns** —
  objective, continuation behavior, completion-audit rules, and
  `update_goal` mechanics. That is what gives it operational bearing: the
  objective stays alive across turns and completion/block accounting is
  required, not optional.

What the agent explicitly would **not** assume:
- That there is any "magic attention token" / durable embedding-memory
  slot. Transformer attention is still over tokens in the current context;
  all persistence comes from **orchestration** — stored goal state,
  injected instructions, continuation scheduling, tool state. There may be
  hidden role/control delimiters, but not a model-generated token that
  stores "the goal meaning" for later.

Plain "the goal is X" vs `/goal`, per the same session:
- Plain text: remembered only as context — vulnerable to drift/truncation,
  no lifecycle.
- `/goal`: parsed, persisted, reinjected, coupled to completion/block
  rules. If the model was trained/evaluated on this scaffold it follows it
  better — but that is *learned behavior + structured orchestration*, not
  an embedding-memory slot.

Why it matters here:
- This is direct corroboration of the design premise behind `wish` and
  `goal-distillation`: the goal contract / reinjected `<goal_context>` is
  the **conditioning channel**, and the "follows it better if trained on
  the scaffold" point is exactly the trained-disposition transfer thesis.
  The `wish` contract file is the portable, prompt-level emulation of what
  Codex's runtime injects automatically.
- It also bounds an overclaim we should avoid: do not describe `wish`'s
  goal-mode declaration as giving the model a persistent memory handle. It
  is a per-turn re-statement that must be re-injected (re-read each cycle)
  to persist — same as `/goal`.

Epistemic status <!-- assumed -->: single-session introspection by gpt5.5,
not official docs. The agent checked OpenAI's public docs and found Codex
described as a long-horizon agentic system but **no public documentation
of `/goal` internals** — so the `<goal_context>` structure is inferred
from the live runtime, credible but unverified against a spec.

Repo-specific aside (from the same `~/ya` session): Yep Anywhere treats
Claude `/goal` as provider-native command text passed through unchanged
(`topics/claude.md`, `providers/claude.ts`), and its Codex provider has
`supportsSlashCommands = false` — so YA is not locally emulating a Codex
`/goal`.
