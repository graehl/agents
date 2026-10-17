# Program Efficiency and alignment

Understand what model efficiency can and cannot establish about alignment.
The central concern is conditional reuse: a small decision rule can redirect
knowledge and reasoning already needed for legitimate tasks. This writing
program develops concise arguments with explicit resource accounting for
readers with graduate-level computer science or mathematics training.

The current scope is a theoretical paper, including training-trajectory audit
limits, optimizer-state influence, and executable checks of mathematical
models. Scalar simulations and proof checking support the arguments; neural
attack efficacy and statistical concealment remain separate research questions.
The [current paper](ROOT.md) is the main reading entry;
the [interpretability survey](../../surveys/interpretability/survey.md)
provides broader background.

## Program instructions

Before developing or revising a conjecture, proof, mathematical model, or its
simulation in this program, read [theorem development](topics/theorem-development.md).
Fix the attacker's permissions and the auditor's observations before proving
a bound; distinguish a proof, an executable check, and a formally verified
statement. Revisit the model when a counterexample changes those assumptions.

Keep methodology and ideation guidance, including Lean or other proof-assistant
use, scoped here while it is being tried. Record consequential successes,
failures, and costs in the topic's evidence companion, with mathematical
artifacts beside the paper. Propose general guidance only after a performance
record in this program supports the particular procedure being promoted.
