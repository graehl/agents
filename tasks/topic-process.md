---
title: Topic population process
status: proposal
---

# Topic population process

Two distinct approaches for populating and maintaining `topics/` docs
in any project.

## 1. Incremental checklist (as-you-go)

Run mentally before each nontrivial commit. Already partially encoded
in AGENTS.md pre-commit trigger; this is the refined version.

- Scan `topics/` filenames for the concern being changed.
- If a relevant topic doc exists: check whether any claim the diff
  directly touches is now false or weakened; update or downgrade its
  epistemic marker (`<!-- verified -->` → `<!-- assumed, see SHA -->`).
- If no relevant topic doc exists and the change crosses subsystem
  boundaries: stub one — name the contract, external consumers, known
  edge cases. A stub beats a dangling cross-reference.
- If the change introduces a cross-cutting concern absent from
  `TOPICS.md`: add the topic name there.
- Append a `Topic:` trailer to the commit message.

Open question: hook vs. reminder? A pre-commit hook enforces it but
adds friction to every commit. A reminder in AGENTS.md is bypassable
but lower cost. Current choice: AGENTS.md reminder only.

## 2. Code archaeology (bulk, deferred)

Reading an entire codebase to write topics/ from scratch is expensive
and session-spanning. Tentative process when wanted:

1. **Module index pass** — one paragraph per source file/module:
   what it does, what it promises callers, what it assumes.
   Save to a scratch JSONL artifact (not committed).
2. **Cross-reference pass** — find modules that share contracts or
   invariants; group into candidate topic names.
3. **Topic drafting pass** — write `topics/<name>.md` per group,
   naming the contract and external consumers.
4. **Discard** intermediate index; commit only the topic docs.

Concern: the intermediate index may be large and span context
windows. Format options:
- Per-module stub files in a scratch dir (survives handoff)
- Single structured JSONL artifact with stable module keys
- Per-directory summary files committed temporarily

Do not execute this approach without a concrete target codebase and a
format decision for the intermediate index.

## 3. topic-definitions.md companion

`topic-definitions.md` alongside `TOPICS.md` provides one-line
definitions for every named topic. It is a **human orientation aid**,
not an agent-maintained artifact — agents already know these terms
from pretraining and need only `TOPICS.md` for topic-name lookup.

Regenerate it on demand with a prompt like:
> "Regenerate topic-definitions.md from the current TOPICS.md"

Do **not** treat it as a source of truth or require agents to keep it
in sync. When `TOPICS.md` grows new entries, regenerate the whole file
rather than patching incrementally.
