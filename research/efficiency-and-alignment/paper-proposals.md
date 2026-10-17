# Paper proposals

## conditional-reuse

Status: promoted by the user's request for a short theoretical paper.
Governing form: theorem-or-bound paper.

Reader promise: a computer science or mathematics master's-level reader can
check why a model close to an efficiency frontier can still implement a
consequential conditional deviation.

Central result: a Boolean circuit computing the legitimate function can be
reused with a conjunction trigger and an exclusive-or output gate. The added
gate count is linear in trigger length, while passive detection can require
exponentially many samples. The result is an elementary construction, not a
novel algorithm or an empirical claim about transformers.

Matched baseline: a minimum-size circuit implementing the exact legitimate
function in the same fixed gate basis. The cost of an imperfect or unknown
baseline is not needed for the counterexample.

Scope: resource accounting and finite testing, with a fictional sponsored
recommendation example. No practical research companion, training experiment,
deployment, or paper submission is planned or authorized.

The [paper](papers/conditional-reuse/index.qmd) owns the argument. Its evidence
ceiling is the stated circuit model and sampling assumptions. Transfer to
fixed transformer architectures remains outside the proved claim.

The user-directed extension adds attacker-triggered and ordinary-use policies,
output-only and weights-access reviewers, and committed training trajectories
with random replay. Audit methods may be known to the attacker; audit random
choices remain private. Training draws are reproducible from their separate
seed. Elementary coverage, distribution-overlap, and transition-sampling
bounds extend the argument without claiming a universal neural concealment
method or provably sound sublinear verification of arbitrary training.
