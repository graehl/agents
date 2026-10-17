# Theorem-development evidence

## 2026-10-17 — First optimizer-audit investigation

Contributing-model: 6-astra

User-directed scope: “the paper program should specify all this for now while
we work it out (incl lean or other methodology/ideation advice). we will promote
to general after we have a record of performance in this paper program.” The
existing program was extended; no general theorem-proving instructions were
added. Methodology efficacy is unmeasured.

The initial paper had a random-replay counting bound but no bound connecting
one bad transition to eventual change. The user supplied the missing question:
all-step cheap restrictions, momentum, and sparse interventions. The
[new analysis](../papers/conditional-reuse/sections/_37-optimizer-memory.qmd)
and its [reproduction record](../papers/conditional-reuse/sections/_37-optimizer-memory.repro.md)
preserve the resulting proofs and numerical checks.

Observed contributions during derivation and independent proof review:

- Specifying the intervention object separated velocity resets from bounded
  gradient substitutions, and exposed different Nesterov gains.
- Separating rejection from clipping prevented applying a geometric-tail
  bound to an unbounded hidden velocity behind clipped parameter steps.
- Checking the actual Adam recurrence exposed bias correction as material:
  the steady-state geometric factor is not a finite-time upper bound. The
  corrected segment formula also revealed that delaying a reset can help.
- Seeking a counterexample with honest gradient feedback showed that even
  plain SGD can propagate one bounded corruption into linear-in-horizon
  divergence. A weight-step cap alone cannot justify the desired sampling
  guarantee. A separate stability argument supplies a sufficient condition.
- Exact small-case enumeration checked the momentum optimum and residual
  recurrence; direct floating recurrences checked Adam and RMSProp formulas.
  None of these checks demonstrates neural realizability or semantic harm.

The working agent and an independent mathematical reviewer checked the main
derivations. This is not a controlled comparison of the new instructions with
ordinary reasoning, and no incremental human/agent time was measured. Lean
and Lake were not available on the inspected PATH; no formal proof was run.
The first candidate for later formalization is residual propagation, after its
statement stabilizes, rather than a claim about real-model behavioral safety.

Instruction trace checks: a formatting-only paper edit does not trigger the
mathematics procedure; a new Adam bound does trigger the model and recurrence
checks; a passing Lean proof of a changed definition still requires statement
review. A failed connection may be recorded without forcing formalization.
One successful lemma does not authorize global promotion. These traces check
the rules' interpretation, not their empirical productivity.
