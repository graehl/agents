# Instruction-repository boot

This checkout authors the reusable agent policy whose installable global source
is `AGENTS.global.md`. Load that file before this one unless the harness already
supplied it. A harness-global `AGENTS.md` or `CLAUDE.md` must target
`AGENTS.global.md`, not this project file; keeping those roles distinct prevents
the global policy from being injected again as project context in this repo.

## Design objective

This repository treats `AGENTS.global.md` and its routed supplements as an
empirical control surface for global agent context. Compliance is not an end in
itself. Keep an instruction only when observed cost/productivity or a credible
failure mode supports the belief that it helps agents pursue user aims—most
importantly by reducing catastrophic, unrecoverable mistakes—or that it points
toward a repeatedly successful tactic.

Continuously seek a smaller compaction-protected token burden without spending
more reliability than the saved context is worth. Prefer measured ablation by
model, harness, project, and request class over a universal intuition about
which text is necessary. Put corrections for demonstrated model or harness
maladaptations in the narrowest applicable supplement, and revisit them as
defaults improve rather than allowing permanent prompt debt.

The current strategy is a small compaction-protected routing layer: bind a
scoped mandate in global or project `AGENTS.md` to read—or precisely locate the
applicable parts of—a concise next-tier packet such as `RUNS.md`, `RESEARCH.md`,
or a `topics/` document immediately before its governed action. The routing
should remain effective across time and compaction without treating rereads as
free or prescribing one cadence for every agent. The capability/tendency model
in `topics/agent-instructions.md` governs how refresh and protection may vary by
harness, model, effort, request class, stakes, and evidence. This is an
aspiration rather than a free guarantee: fidelity, retrieval cost,
protected-token burden, and available task context remain explicit tradeoffs.

## Project-unrelated ideas

When the user asks to preserve a clever, fun, or possible-new-project idea that
does not govern this repository, read `ideas/README.md` and save one tracked
`ideas/<slug>.md` seed. Its presence preserves the idea; it does not approve,
schedule, or authorize implementation. Keep `topics/` limited to context that
governs this project.

## Working in this repository

- Before editing agent-facing instructions, read
  `topics/agent-instructions.md` and its `.evidence.md` ledger. Read
  `topics/agent-instructions.testing.md` when behavior or loading changes.
- Put reusable cross-project policy in `AGENTS.global.md` or its routed
  supplements. Keep this file limited to the authoring and installation rules
  specific to this checkout.
- Preserve trigger, apply, and persistence spans when compressing instructions.
  Optional clarification may move to a supplemental file; the governing main
  file must retain the trigger and the binding rule.
- Treat existing evidence-ledger entries as append-only historical records.
- Installation changes must be reversible: preserve every pre-existing target
  before replacing it, and make uninstall restore its recorded kind, content,
  link target, and mode.
