# Optimizer-memory proofs and checks

The manuscript supplies proofs, with no novelty claim. All numerical values
are deterministic evaluations of the scalar models, not neural experiments.
The reference code is `../checks/optimizer_memory.py` (relative to this file).

## Model fidelity

The budget counts changed transitions. Step rejection is tested on every
actual weight increment, including the intervention, not just sampled steps.
Frozen gradients, arbitrary state resets, bounded gradient substitution, and
nonlinear honest feedback are separate models. A zero gradient is supplied;
the optimizer is not skipped. Adam counters are trusted, and the exact
bias-corrected calculation is separate from the uncorrected approximation.
No claim establishes that the constructed gradients arise from realistic
smuggled data or that scalar displacement predicts neural behavioral harm.

For the Adam dynamic program, the initial first moment is zero and the
second moment is positive, avoiding 0/0 during an idle prefix with epsilon
zero. A reset may replace both moments independently. Segment gains are
attainable by scaling their ratio; an all-step gradient-consistency test
would invalidate that unrestricted intervention model. The maximum is over
all legal start positions and includes a possible idle prefix.

## Reproduction

From the repository root:

```bash
/usr/bin/python3 research/efficiency-and-alignment/papers/conditional-reuse/checks/optimizer_memory.py
```

Standard-library Python only; no accelerator, dataset, stochastic search or
package install is involved. The output includes the source SHA-256. Exact
rational checks cover 180 momentum reset-optimum cases, 12 Nesterov impulse
cases, and 6,561 finite scalar propagation cases. Momentum optima are checked
against enumeration of every reset schedule for horizons through nine.
Adam's dynamic program is checked against exhaustive schedules through eight
steps and budgets through three. Direct Adam recurrences are compared to the
closed form, including bias correction, at four absolute starting steps.
These finite checks can expose errors but do not prove unrestricted claims.

The checked 100-step, unit-cap momentum optima at coefficient 0.9 are
9.999734386, 19.896924496, 43.921167270, and 65.132155990 for budgets one,
two, five, and ten. For bias-corrected Adam with betas (0.9, 0.999), epsilon
zero and arbitrary moment resets, the corresponding computed optima for
budgets one, two and five are 11.166009548, 21.478524720, 44.848711274.
Maximizing reset times are (22), (17,57), and (7,25,44,63,82), respectively.
The optimization is exact as a finite model; these evaluations use floating
point and are not certified real-arithmetic comparisons of near ties.

For the RMSProp suppression example, alpha 0.99, horizon 100, and a maximum
half-sized legitimate update need second-moment ratio 9.195997079; direct
iteration yields endpoint deviation 58.772944370 from the steady reference.
The nonlinear SGD example with delta 0.1 and cap one reaches 99.1 after
100 updates, while the reference remains zero and only one step is invalid.

## Verification status

Readable proofs were rederived by an independent agent from the model
specification. This caught the need for distinct Nesterov impulse conventions
and Adam bias correction, and supplied the nonlinear-gradient counterexample.
No Lean or other proof-assistant verification has been performed. The local
tool probe found neither `lean` nor `lake` on PATH. The scoped methodology
and performance record live in the program's `topics/theorem-development.md`.
