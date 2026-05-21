# Topic: prototyping

> Throwaway code that answers one specific question. One command to
> run, no persistence, no polish, state surfaced after every action,
> deleted or absorbed when done — with the answer captured durably.

Topic: `prototyping`

## Contracts

- **Throwaway from day one, and marked as such.** Locate the
  prototype next to the module or page it is exploring for, but
  name it so a casual reader sees it is not production. Obey the
  project's existing routing and task-runner conventions; do not
  invent new top-level structure for a prototype.
- **One command to run.** Whatever the project's existing task
  runner supports (`pnpm <name>`, `python <path>`, `bun <path>`,
  …). The user must be able to start it without thinking.
- **No persistence by default.** State lives in memory. If the
  question explicitly involves a database, use a scratch DB or
  local file named so it self-identifies as wipe-on-cleanup.
  Persistence is what the prototype is *checking*, not what it
  depends on.
- **Surface the state.** After every action (logic prototype) or on
  every variant switch (UI prototype), print or render the full
  relevant state so the user sees what changed.

## Invariants

- **Skip the polish.** No tests, no error handling beyond what
  makes the prototype runnable, no abstractions. The point is to
  learn fast and delete.
- **The answer is the keepable artifact.** Capture the question
  and its answer durably in whichever channel fits: an ADR bullet
  in the relevant topic doc's `## Design decisions`, an entry in
  that topic's `.evidence.md` ledger (experiment / probe /
  negative result), a task-file note, or the commit message that
  deletes or absorbs the prototype. Then delete the prototype, or
  fold the validated decision into production code.

## Known edge cases

- **The question decides the shape.** "Does this state / business
  logic feel right?" → tiny interactive terminal app that walks the
  state machine through cases hard to reason about on paper. "What
  should this look like?" → several radically different UI
  variations on one route, switchable via a URL search param or a
  floating bottom bar. Picking the wrong branch wastes the
  prototype; if genuinely ambiguous and the user is unreachable,
  default by surrounding code (backend → logic; page or component
  → UI) and state the assumption at the top of the prototype.
