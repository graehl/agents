# Agent Instructions Theory

Topic: `agent-instructions`

This repo's main correctness claim is that committed global instructions give
future agents enough stable, searchable policy to behave consistently across
projects without relying on stale chat state.

## Contracts

- `AGENTS.md` is the authoritative global policy file.
- Local project instructions may add narrower rules, but global policy changes
  belong here first.
- Correctness topics are defined by committed `topics/*.md` basenames, and
  related commit series use matching `Topic:` trailers.
- Task files may track work, but they are not the durable source of global
  correctness arguments.

## Invariants

- Instruction changes should be load-bearing: they should steer behavior that
  a capable agent would otherwise plausibly get wrong.
- A rule that introduces process cost should identify the failure mode it
  prevents.
- Topic and theory names should stay searchable from commits, tasks, and
  instruction text.
- Theory docs should explain why contracts are believed, not accumulate a
  chronological list of every change.

## Contract Notes

- The topic namespace depends on `ls topics/*.md`, so agents have one
  committed place to inspect both the topic name and its correctness model.
- The `agent-instructions` topic spans commit policy, task cross-references,
  and theory docs because all three determine how future agents recover the
  intended policy from repository state.
