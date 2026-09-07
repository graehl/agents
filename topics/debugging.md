# Topic: debugging

> Disciplined diagnosis builds a faithful agent-runnable feedback loop
> before changing behavior, uses ranked falsifiable hypotheses for new
> diagnoses, tags temporary instrumentation for cleanup, and writes the
> regression test at the correct seam — or records its absence.

Topic: `debugging`

## Contracts

- **Feedback loop before patching.** No fast, deterministic,
  agent-runnable pass/fail signal for the bug → no behavior-changing
  patch, not no investigation. Build the best faithful signal (failing
  test at the right seam, curl / CLI invocation, headless browser
  script, replay of a captured trace, throwaway harness, property /
  fuzz loop, bisection or differential harness) before editing behavior.
  Iterate on the loop itself for speed, sharpness, and determinism
  before iterating on the code. A failed literal reproduction is not a
  stop condition: audit its fidelity and follow
  [`handling-bug-reports`](handling-bug-reports.md) when the investigation
  began with a standalone report. When the thing under test *generates*
  rather than computes (a model, a prompt, an MT system), the loop is a
  soft check — a property or rubric oracle over a kept set of cases, see
  [`soft-checks`](soft-checks.md) — not an exact-match assertion.
- **Ranked falsifiable hypotheses before any new-diagnosis probe.** 3–5
  hypotheses, each stating its prediction ("if X is the cause then
  changing Y will make the bug disappear"). Surface the ranked list
  as an interruptible checkpoint; the user often re-ranks instantly.
  Single-hypothesis generation anchors on the first plausible idea.
- **Active feedback continues the existing loop.** A user complaint
  about implementation already in progress is new evidence and
  refinement, not an automatic fresh diagnosis. Tests, investigation,
  classification, and focused subtasks remain available when naturally
  useful; this contract creates no process requirement merely because
  feedback named a defect.
- **Regression test at a correct seam, or record the gap.** The
  seam exercises the real bug pattern as it occurs at the call
  site. No such seam → the absence is the finding, recorded as a
  structural coverage gap; a too-shallow test is worse than no test.

## Resource pressure

For slow, stalled, or intermittently buggy interactions, check system resource
pressure alongside the application path, early enough to capture a live stall
and before stopping at an unexplained cause. Passing focused tests, successful
delivery, or eventual completion do not rule out contention.

Check the affected host and process/container: available memory and limits,
active swap-in/out or paging, CPU contention, and disk I/O wait; inspect pressure
metrics and OOM events where available. Use a short sampled observation to
distinguish ongoing pressure from accumulated counters, and identify competing
processes when pressure appears. Swap occupancy alone does not establish
thrashing. Extend to other resources when the symptom warrants it.

Match evidence to the incident's timestamp. If it has subsided, look for
retained metrics and relevant system/application logs; current healthy readings
cannot rule out earlier pressure, and current pressure cannot prove the past
cause. Report what was checked and whether pressure is supported, ruled out
for the observed interval, or remains unknown because historical evidence or
host access is unavailable. Do not manufacture certainty or require an
indefinite investigation when evidence is missing. This diagnostic check does
not authorize killing processes or changing resource limits.

## Invariants

- **Greppable debug tags.** Every debug log line carries a unique
  prefix (`[DEBUG-a4f2]`) so cleanup is one grep. "Log everything
  and grep" is an anti-pattern: untagged "just-this-once" logs
  survive across commits.
- **One variable per probe.** Each probe maps to one hypothesis
  prediction. Prefer debugger / REPL inspection over logs when the
  environment supports it.
- **Measure before fixing performance.** Baseline (timing harness,
  profiler, query plan) first, then bisect.
- **Non-deterministic bugs need a higher reproduction rate, not a
  clean repro.** Loop the trigger, parallelize, narrow timing
  windows, inject sleeps until the rate is workable. A 50%-flake
  bug is debuggable; 1% is not.

## Known edge cases

- When the bug only reproduces in an environment you cannot access,
  ask for access, a captured artifact (HAR file, log dump, recording
  with timestamps), or permission to add temporary production
  instrumentation. Continue history, static, and test investigation,
  but do not claim reproduction or make a behavioral patch unless an
  independently demonstrated current defect supplies the loop.
- The correct hypothesis goes in the commit message so the next
  debugger learns. Structural recommendations (no good seam,
  tangled callers, hidden coupling) are made *after* the fix is in
  — you know more once the fix exists than when you started.
