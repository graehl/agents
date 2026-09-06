---
slug: instruction-guidance-evolution-testbed
noticed: 2026-09-06
where: topics/instruction-ablation.sketches.md
---

**Gap:** the instruction corpus has no outcome-tested mechanism for learning
how to write and evolve guidance. Incident-driven additions accumulate while
we cannot distinguish useful shared themes, model/defect-specific repairs, and
inert prompt cost. Existing ablation, longitudinal-benchmark, and differential
diagnosis proposals have not implemented this capability.

**Noticed while:** the user requested Astra-oriented instruction reductions,
then specified the larger ambition: find guidance themes recurring in
successful trajectories and project back to a minimal reasonable seed that
can evolve guidance toward both testbed fitness and appropriate scoped wins.

**Fix sketch:** the linked
[guidance-evolution design](../topics/instruction-ablation.sketches.md)
defines the mutable authoring/working guidance, external objective,
fixed-point candidates, seed minimization, pinned real-project and synthetic
testbeds, controls, fitness, and held-out adaptation. The present
[reduction proposals](../topics/agent-instructions.sketches.md#astra-and-shared-instruction-reductions)
are judgment-based candidate interventions, not discovered fixed points.

**Deferred by user:** wait for a later model and an explicit experiment
budget. This gap authorizes no run, worktree preparation, paid call, model
launch, or scheduled re-evaluation. A model release alone does not authorize
spending. This entry is the root of a larger effort, not a claim that its full
research objective fits one work session.

**First future unit:** one frozen fixture, effective-guidance manifest, sealed
grader, cost recorder, and reproducible same-guidance replay. Verify that
future Git objects, hidden tests, and personal global boot cannot leak into
the solver; retain all trajectory versions and failures. Complete this unit
before sizing or implementing a broad search.

**Closure evidence:** reproducible held-out adaptation trajectories comparing
seeds and authoring policies; per-model/per-defect with/without effects;
downstream quality and cost with uncertainty; and a defensible disposition of
candidate stable themes and minimal seeds. A null or failure to find a common
seed is a valid result. Building a harness or writing an attractive seed alone
does not close the empirical gap.

**Distributed extension:** the same sketch describes a git-history aggregator
for human-steered successful collaborations and donated blind-evolution runs.
Record revision prompts and before/after trees to expose co-evolution; compare
whole forks without requiring a meta/non-meta partition. Score boot and total
size, count the runner, and search fresh for minimal successful added guidance
at each frontier harness/model/default-prompt step. Forking a claimed best is
part of the proposed social process; independent confirmation and attribution
to human steering remain separate from contribution credit.
