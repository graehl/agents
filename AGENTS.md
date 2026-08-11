# Instruction-repository boot

This checkout authors the reusable agent policy whose installable global source
is `AGENTS.global.md`. Load that file before this one unless the harness already
supplied it. A harness-global `AGENTS.md` or `CLAUDE.md` must target
`AGENTS.global.md`, not this project file; keeping those roles distinct prevents
the global policy from being injected again as project context in this repo.

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
