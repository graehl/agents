# Topic: ml-scaling

> Scaling posture for ML systems: v1 targets correct, efficient
> single-configuration training; distributed/multi-GPU training and
> memory-hierarchy (CPU/disk) offload are stretch goals reached through a
> preserved seam, not infrastructure built into the first version.

Topic: `ml-scaling`

## v1 target vs. stretch goals

- **v1 target.** Correct, and efficient on the hardware it already uses —
  no needlessly quadratic-or-worse work, running on the simplest platform
  that fits the problem. Not full-distributed-ready infrastructure.
- **Stretch goals, explicitly not v1.** Seamless transition to multi-GPU /
  multi-node training; handling larger data and models by respecting the
  memory-storage hierarchy — spilling GPU → CPU memory, and CPU → disk,
  when capacity is the binding constraint.

v1 should reach the stretch goals *incrementally later*, never by a
rewrite. That is a **seam** requirement, not an infrastructure one: v1
avoids the cheap-to-avoid lock-in that would foreclose the transition, and
otherwise stays minimal. When keeping a seam open is itself expensive,
defer it and record the deferral rather than paying for it now. This is the
general seam / reversibility discipline of [`design-thinking`](design-thinking.md)
applied to the scaling axis — not a license to pre-build for scale, which
cuts against the same YAGNI stance.

## "Scalable" is a bundle, not a scalar

"Scalable" is vague until decomposed into the measurable quantity the
decision actually turns on:

- **strong-scaling efficiency** — speedup vs. device count at a fixed
  problem size;
- **weak-scaling efficiency** — throughput held per device as the problem
  grows with the device count;
- **capacity ceiling** — largest model/dataset that fits at fixed hardware;
- **offload reach** — how far down the GPU → CPU → disk hierarchy state can
  spill before the run stops fitting.

Name the one you mean; "make it scalable" on its own does not specify a
target.
