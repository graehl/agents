# Topic: testing

> Proportionate verification of software and durable scripts: weigh initial
> correctness evidence and lasting regression protection against test cost,
> and retain only coverage that earns its ongoing expense.

Topic: `testing`
Governs: planning or implementing durable scripts or software, or choosing, writing, running, retaining, or reviewing tests

## Cost, scope, and retention

These are defaults across projects; explicit project test, release, and
commit policies take precedence. Choose checks by the failures they could
expose, their likelihood and consequences, and the cost of writing, debugging,
running, and maintaining the checks. Reasoned judgment suffices; do not require
expensive measurements to justify a small verification decision.

Establishing that the requested behavior works and retaining regression
coverage are separate decisions. A temporary test can earn its development
cost and still be removed before landing. Retain it only when future failure
detection justifies recurring execution and maintenance, including fixtures,
startup, retries, and failure triage. Agents may avoid, remove, or consolidate
low-value tests without separate permission unless project policy requires them.

Prefer focused integration checks through real boundaries over assertions
that mirror implementation or mock wiring. Use the smallest boundary that can
expose the failure; integration does not mean a full application or live
external service. Small unit tests remain useful for subtle logic and state
transitions. Neither test count nor coverage percentage alone establishes value.
Rare failures with severe consequences can justify costly retained coverage.

Run applicable static checks and focused behavioral checks. Broaden when shared
behavior, configuration, unresolved failures, or uncertain impact leave
meaningful risks outside focused coverage, or project gates require it.
Committing or ending a work slice alone does not require a full suite. Reuse
passing results while intervening changes cannot affect what they verified;
honor stricter project rules for evidence reuse. Report material verification
limits. A direct manual check can suffice for a simple change; a new automated
test or test-first sequence is not required for every implementation.

Do not delete a failing test merely to obtain green results. Diagnose the
failure and judge its contract. When removing coverage, account for the failure
it could catch and whether other checks preserve it or its value is low; no
replacement is required for a trivial assertion. Preserve project-required
coverage and useful detection of consequential failures.

## Temporary tests and review evidence

When a temporary test has useful review or reproduction value and the project
allows separate commits, consider committing it with the implementation, then
removing it in a separate commit. The removal message identifies the evidence
commit and test path, what was established, and why continued retention is not
worth its cost. Do not create a two-commit ritual for trivial checks. A project's
single-commit review policy overrides this option; it never authorizes extra
review commits or removal of project-required tests.

When reviewing such a change, inspect the historical test and the removal
rationale: a test added and removed inside the range disappears from its net
diff. Judge initial verification and continuing regression protection
separately; historical evidence does not provide ongoing coverage. Require
additional retained tests for a concrete worthwhile risk, not merely because
the final tree lacks a test for every changed path.

## Test construction

- **Use test-first work when useful.** When using it, take one behavior
  through failing test → minimal implementation → passing test before the
  next. For a regression check, demonstrate that it rejects the unfixed or
  bypassed behavior. Do not write a speculative battery against an imagined
  implementation.
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
- **Test names use project glossary vocabulary** so the test reads
  as a capability statement, not a paraphrase.

## Behavioral integration smoke

Before relying on changed behavior, exercise the real entrypoint and affected
execution mode at the smallest useful scale. Choose a case that activates the
change and state an expected effect that would be absent if its implementation
were omitted or bypassed. Check that the test rejects that failure, using the
previous version, a disabled configuration, or a bounded deliberate bypass as
appropriate. Merely accepting an option, logging its value, returning success,
or testing a helper in isolation does not establish integration.

For training and optimization changes, hold inputs, initialization and random
state fixed between controls; account for remaining numerical noise. Exercise
the actual option-to-batch-to-loss-to-update path for a few steps. Assert the
relevant loss, gradient, parameter update, routing or output relation; check
save/reload when the change crosses checkpoint persistence. A zero learning
rate, inactive margin or zero-initialized residual may legitimately hide an
effect: construct an activating case rather than accepting an insensitive
smoke. Verify the disabled setting recovers the baseline when that is part of
the contract.

The exact final weights and quality score need not be predictable. This check
establishes that the mechanism operates; it does not require a tiny run to
improve a downstream metric. Judge benefit separately through the matched
comparisons and output review in [soft-checks](soft-checks.md). Keep checks
proportionate: a direct manual check can suffice for a simple change; no large
test harness or quality study is implied by this smoke requirement.

## Known edge cases

- Focus on consequential behavior and complex logic. Ask which behaviors
  matter most only when an unresolved priority changes the verification plan.
- Coverage gaps the structure prevents from being closed (no
  correct seam) are findings — record them in the commit message's
  `Known coverage gaps:` section rather than papering over with a
  shallower test that gives false confidence.
