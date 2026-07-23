# Handling bug reports

> Standalone bug-report intake verifies whether reported behavior still
> exists, uses a failed reproduction as a search hint rather than an
> abstention trigger, distinguishes the exact report from related defects,
> and changes behavior only after demonstrating a current failure.

Topic: `handling-bug-reports`

## Trigger and boundary

Apply this topic when a session- or topic-opening user message resembles
a standalone report of a new or unrelated defect: unexpected behavior,
an error or trace, a regression, a screenshot showing something wrong,
or a request to make an observed failure stop. No special bug-report
syntax is required.

A complaint about the result of an implementation effort already in
progress does **not** automatically restart this protocol. Treat it as
credible new evidence and refinement within the current feedback loop.
A test, investigation, classification, or focused subtask remains
available when naturally useful; nothing here requires or prohibits
those actions. The distinction is that the instructions do not mandate
a full intake process for every correction. If a message introduces a
genuinely unrelated defect, make it a separate intake when taking up
that topic.

## Evidence posture

A user's direct observation is strong evidence that the behavior
occurred in the system they saw. It does not by itself establish that
the same behavior exists in the current checkout, configuration, data,
or runtime state. Preserve both facts: do not dismiss the observation
because a local attempt passes, and do not patch current code merely
because the report names a plausible defect.

A bug report is therefore a search input, not a pre-proved patch
requirement. Before editing behavior:

1. Search the current implementation, tests, configuration, and
   relevant history for the reported behavior and equivalent concepts.
2. Attempt a faithful reproduction, recording the material revision,
   inputs, state, configuration, environment, and event sequence.
3. If the literal reproduction passes, audit its fidelity and use the
   report as a bounded search hint: derive the suspected violated
   invariant, form ranked falsifiable hypotheses, and probe nearby cases
   that distinguish stale behavior, an inaccurate reproducer, and a
   related current defect.
4. Stop only when the evidence supports one of the classifications
   below, not merely because the first reproduction attempt passed.

Use the cheapest faithful signal: a failing test at the real seam, CLI
or API invocation, rendered interaction, captured-trace replay,
performance baseline, or a repeated probabilistic trigger. Follow
[`debugging`](debugging.md) for hypothesis and feedback-loop discipline
and [`testing`](testing.md) for the regression test.

## Classify before changing behavior

State explicitly which conclusion the evidence supports:

- **The described defect reproduces on the current target.** Name the
  conditions. Capture the failure in a regression signal, then fix it
  and show that signal passing.
- **The described defect does not reproduce, but a related current
  defect does.** Say both. Test and fix the defect actually
  demonstrated; do not present it as reproduction of the original
  report.
- **The defect existed on the reported target but is already fixed on
  the current target.** Show the old failure, the current pass, and the
  intervening change when identifiable. Do not make a duplicate fix.
- **No defect was demonstrated.** Report what was searched and probed
  and make no change solely to satisfy the bug-fix framing. An optional
  test, documentation, cleanup, or usability improvement is a proposal,
  explicitly not expected to produce a material behavioral difference.

If the report asks for a remedy and a current defect is demonstrated,
proceed directly from the failing regression signal to the fix. If the
user asked only for diagnosis, stop at the evidence-backed diagnosis;
the bug-report protocol does not expand the requested authority.

When investigation instead finds that the requested capability already
exists, follow `AGENTS.md` § *"Add X" when X already exists*: point to
the existing mechanism and do not build a duplicate.

## Reporting contract

Lead the result with the classification, not with an edit summary.
Identify the target and conditions for every reproduction claim.
Never let “a test failed” imply that the test represented the user's
exact report when it covered only a related case.

Use direct formulations:

- `The reported defect reproduced on <target> under <conditions>.`
- `The reported defect did not reproduce; <related defect> did.`
- `The defect reproduced at <old target> and passes on <current target>.`
- `I did not reproduce a defect; <evidence> does not justify a change.`

## Remote reports

A remote report should identify the exact source commit SHA-1. Reproduce
against that revision without moving a shared worktree's HEAD, inspect
the intervening commits, and then demonstrate the result on current
HEAD. Without the reported SHA-1, label the historical comparison
under-specified; still investigate current HEAD rather than treating
the missing revision as an abstention trigger.
