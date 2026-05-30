# Topic: testing-rider

> An optional `topics/<name>.testing.md` companion that specifies how to
> check a change to that topic's concern before committing it: the
> cheap always-run checks and the expensive optional ones, which are
> mandatory, and what counts as passing.

Topic: `testing-rider`

A topic doc names the contracts and invariants a concern must uphold. The
`.testing` rider says **how you verify a change does not break them** —
turning "be careful editing this" into a named, repeatable check. It is
the per-topic analogue of a test suite: a contract doc without a rider
relies on each editor re-deriving how to validate; a rider makes the
check explicit and inheritable by weaker agents.

This is a companion convention alongside `.evidence.md`,
`.bearings.md`, and `.runs/` (see `AGENTS.md § Project topics`). It is
**optional** — most topics will not have one — and is read at a
**verb-trigger**, not routinely.

## Contract

- **Trigger.** Before committing a change to a topic's concern (code or
  the topic doc itself), check for `topics/<name>.testing.md`. If it
  exists, run the checks it marks mandatory and report the result in the
  commit or status; skip the optional ones with a one-line reason.
- **Content.** A rider lists checks cheapest-first, each tagged
  **mandatory** (always run; a change is not done until it passes) or
  **optional/deferred** (run when the change is significant enough or
  compute is available). Each check states what passing looks like.
- **Not a duplicate of `testing.md`.** The `testing.md` topic is the
  project's general TDD discipline. A `.testing` rider is specific to
  *one* topic's concern — what to run when *that* contract might have
  been weakened.
- **Honesty about cost.** A rider may say its real validation is
  expensive and deferred; that is a valid state, recorded rather than
  pretended-away. The mandatory tier should stay cheap enough to
  actually run every time.

## Why optional, not mandatory-everywhere

Forcing a rider on every topic would manufacture inert files — the
celebratory-ritual failure mode. Add one only where the check is
non-obvious or the contract is easy to silently break. A topic whose
"how to check" is just "run the repo's tests" needs no rider.

## First instances

- [`agent-instructions.testing.md`](agent-instructions.testing.md) — how
  to check an instruction-corpus change: trace-simulation (mandatory,
  cheap) and the [`instruction-ablation`](instruction-ablation.md)
  outcome measurement (optional, deferred, expensive).
