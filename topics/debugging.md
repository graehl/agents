# Topic: debugging

> Disciplined diagnosis: build a fast deterministic feedback loop
> before hypothesising, generate ranked falsifiable hypotheses, tag
> debug instrumentation `[DEBUG-xxxx]` for one-grep cleanup, and
> write the regression test at a correct seam — or record the
> seam's absence as the finding.

Topic: `debugging`

## Contracts

- **Feedback loop first.** No fast, deterministic, agent-runnable
  pass/fail signal for the bug → no debugging. Build one (failing
  test at the right seam, curl / CLI invocation, headless browser
  script, replay of a captured trace, throwaway harness, property /
  fuzz loop, bisection or differential harness) before hypothesising.
  Iterate on the loop itself for speed, sharpness, and determinism
  before iterating on the code.
- **Ranked falsifiable hypotheses before any probe.** 3–5
  hypotheses, each stating its prediction ("if X is the cause then
  changing Y will make the bug disappear"). Surface the ranked list
  as an interruptible checkpoint; the user often re-ranks instantly.
  Single-hypothesis generation anchors on the first plausible idea.
- **Regression test at a correct seam, or record the gap.** The
  seam exercises the real bug pattern as it occurs at the call
  site. No such seam → the absence is the finding, recorded as a
  structural coverage gap; a too-shallow test is worse than no test.

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
  stop and ask — for access, a captured artifact (HAR file, log
  dump, recording with timestamps), or permission to add temporary
  production instrumentation. Do not proceed without a loop.
- The correct hypothesis goes in the commit message so the next
  debugger learns. Structural recommendations (no good seam,
  tangled callers, hidden coupling) are made *after* the fix is in
  — you know more once the fix exists than when you started.
