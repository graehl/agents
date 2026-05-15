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

## Verifying instruction changes

A reading pass finds rules that *look* wrong; it misses rules that only
misfire when practiced. Before finalizing an instruction change — and
especially after compressing or rewording existing rules — run a
trace-simulation pass:

1. Triage (cheap): pick the rules most likely to misfire — those that fire
   often, overlap with other rules, hedge, or create perverse incentives.
2. Simulate (bounded): for each, construct 2-3 concrete scenarios and play
   the rule forward. Does following it literally produce a worse outcome
   than not having it?
3. Keep only changes that survive their traces; fix the ones that fail.

This is the falsification discipline applied inward: "what realistic
situation makes this rule backfire?" Compression is the highest-risk case —
a reword can invert a rule's logic while still reading fine on the page,
and the inversion surfaces only in a trace.

Past trace passes and what they caught are recorded in the companion
ledger `agent-instructions.evidence.md` — consult it when proposing an
instruction change, not routinely.

When a trace exposes that the rule's gap is only safe because a frontier
agent infers around it, prefer adding redundancy (a worked example, or the
rule's rationale) over leaving the gap, since non-frontier agents also edit
these projects.
