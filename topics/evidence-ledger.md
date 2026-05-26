# Evidence ledger convention

> An optional, append-only `<topic>.evidence.md` companion to a
> topic doc — agent-owned space for notes that help maintain
> accurate knowledge and good behavior on the topic.

Topic: `evidence-ledger`

## License — what to append

Append:
(a) incident reports when the user explicitly attributes a failure
    to an instruction or to behavior under one;
(b) trace-simulation catches and clarifying examples hit while
    consulting an instruction;
(c) the agent's own observations, hypotheses, or beliefs that help
    maintain accurate knowledge and good behavior on the topic.

Append-only; do not rewrite prior entries. (a) is expected when
triggered; (b) and (c) are licensed at the agent's discretion. The
companion is not loaded routinely — it is the agent's space, not the
user's review surface — so brevity matters less than capture.

## Adding entries

The trigger is always: "would this help me or another agent maintain
accurate knowledge and good behavior on this topic later?" If yes,
append; if no, don't. Bullets are fine; paragraphs when context
matters. Date-stamp entries that benefit from chronology.

## Use cases

- **Justification anchor for a topic-doc claim** — when the topic
  doc states something the user (or a future agent) might later
  question, log the trail: code path, test run, conversation
  excerpt, or empirical observation that backs it. Trigger: writing
  a non-obvious claim with no inline citation.
- **Decision / branch choice** — when the agent picks an
  implementation branch, term, format, or convention, log the
  choice plus brief reason. Future agents pick up the trail rather
  than re-deriving.
- **Experiment, probe, or negative result** — record runs and their
  artifacts in `<topic>.runs/` (see `topics/runs-ledger.md`), not
  here. Use evidence.md only for qualitative notes around a run —
  surprise, updated hypothesis, model change — that don't belong as
  a run artifact.
- **Anchoring user instruction** — selectively, quote a user
  message that established or modified a topic-doc claim where the
  provenance would otherwise be lost. Not every user message — only
  ones that shaped lasting content.
- **Unresolved question / open item** — something noticed but not
  resolved this session; serves as backlog for revisit.
- **Mental model / analogy** — an internal frame the agent finds
  useful for reasoning about the topic; helps a future agent load
  the same model fast.
- **Drift observation** — when a topic-doc claim seems to no
  longer match code or behavior; flags for verification before the
  doc itself is updated.
