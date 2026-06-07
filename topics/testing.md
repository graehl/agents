# Topic: testing

> Vertical-slice TDD: one test → minimal code to pass → next test.
> Tests verify behavior through public interfaces and survive
> internal refactor; mocking is for system boundaries, not internal
> collaborators.

Topic: `testing`

## Contracts

- **Vertical slices, not horizontal.** One test → minimal code to
  pass → next test. Writing all tests first then all implementation
  produces tests of *imagined* behavior and of the *shape* of things
  (signatures, data structures) rather than of actual user-facing
  behavior.
- **Behavior through public interfaces.** A good test reads like a
  capability specification ("user can checkout with valid cart")
  and survives internal refactor. If renaming an internal function
  breaks it, the test was coupled to implementation, not behavior.
- **Mock at system boundaries only.** Network, filesystem, clock,
  external services — yes. Internal modules — no; that couples the
  test to today's structure and masks integration bugs.
- **Non-exact-matchable behavior gets a soft check.** When the output
  has no single correct value (generation, translation, layout, model
  output), the check's oracle is a stated property or rubric, not a
  string match — see [`soft-checks`](soft-checks.md). Don't skip verification because
  the output isn't pinnable; pick the cheapest adequate oracle.

## Invariants

- **Red before green; never refactor while red.** Each cycle is
  write-failing-test → watch fail → minimal code to pass → watch
  pass. Refactor only after green.
- **Only enough code for the current test.** Do not anticipate
  future tests; let each cycle teach you what the next test should
  cover.
- **Test names use project glossary vocabulary** so the test reads
  as a capability statement, not a paraphrase.

## Known edge cases

- You cannot test everything. Confirm with the user which behaviors
  matter most; focus testing effort on critical paths and complex
  logic, not every edge case.
- Coverage gaps the structure prevents from being closed (no
  correct seam) are findings — record them in the commit message's
  `Known coverage gaps:` section rather than papering over with a
  shallower test that gives false confidence.
