# Topic: soft-checks

> When an output has no single correct value, the check's oracle is a
> stated property or rubric, not a string match. Pick the cheapest
> adequate oracle (computable predicate over model judge), keep the
> failing cases as a regression set, and never leak the target answer to
> a generator under test.

Topic: `soft-checks`

A **soft check** is a check whose pass/fail comes from evaluating a
stated invariant over an output, rather than comparing the output to an
exact expected value. It is the verification tier between a hard
assertion (the property reduces to code — see [`testing`](testing.md)) and pure
human eyeball (taste). It is the routine, almost-mandatory mode whenever
the thing under test *generates* rather than *computes*: machine
translation and other model outputs, prompt debugging, codegen, layout
([`ui-verification`](ui-verification.md)).

## Contracts

- **The oracle, not the value.** A soft check is defined by its oracle.
  Two kinds: a **property check** — a computable predicate over the
  output (counts, ranges, a parseable field, a structural relation) —
  and a **rubric check** — a model/judge scoring the output against
  stated criteria. Use the cheapest oracle that is adequate: if the
  property reduces to code it is a property check; reach for a rubric
  check only for what code cannot decide.

- **Golden only for deterministic producers.** A compliant example
  output is a safe fixture (a snapshot test) *only* when the thing under
  test computes its output deterministically — it cannot see the golden
  and bend toward it. For a generator (a model, a prompt), providing the
  target answer invites gaming: the generator pattern-matches the
  example instead of satisfying the property. Specify the properties or
  criteria and keep the answer out of the prompt. The tell: *is the
  artifact-under-test produced by the thing the check could leak to?*

- **Rubric criteria are concrete and independently gradeable.** A judge
  oracle is fallible — it passes wrong outputs when lenient, and a
  generator can learn to satisfy its letter. Enumerate gradeable
  criteria ("revenue projection uses ≥5 years of history", "summary
  introduces no entity absent from the source"), not vibes ("looks
  good"). Noisy criteria produce noisy loops.

## Invariants

- **Keep failing cases as a regression set.** The durable artifact is
  the small set of input cases that exercised the invariant, re-run on
  every change — not the one debug run that found the bug. This is the
  soft-check form of the [`debugging`](debugging.md) regression-test contract: the
  seam is the invariant, the cases are the coverage.

- **Metamorphic relation when no absolute exists.** When you cannot
  state an absolute property of one output, assert a *relation* between a
  perturbed input and its output — paraphrase / casing / terminology
  invariance for MT, idempotence, monotonicity under a known change. The
  relation is the oracle; this is often the only soft check available
  for generation, and the native one for translation.

- **Soft checks supplement exact checks, never replace them.** Where an
  exact assertion or computable predicate is available, use it; the soft
  check covers only the un-codeable remainder. Don't rubric-check what a
  property check can pin — that trades a reliable oracle for a fallible
  one.

## Known edge cases

- Some properties are genuinely human-only (taste, voice, final call).
  Those stay human eyeball — do not force a rubric onto them, which only
  produces a check that passes while the thing is actually wrong.

- A rubric check run by the same model that generated the output can
  share its blind spots. Prefer an independent oracle (a different
  model, or explicit computable criteria) when the stakes justify it,
  and say "judge-only, modest confidence" when they don't.
