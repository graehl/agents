# Metastable failures and recovery

> Read-backed digest (cluster C, trust `multi-source`; conceptual model,
> incident evidence, and causal characterization).

**Papers.** Bronson et al., “Metastable Failures in Distributed Systems,”
HotOS 2021
([PDF](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf),
[local extract](../related-work/extract/bronson2021-metastable/bronson2021-metastable.md));
Huang et al., “Metastable Failures in the Wild,” OSDI 2022
([PDF](https://www.usenix.org/system/files/osdi22-huang-lexiang.pdf),
[local extract](../related-work/extract/huang2022-metastable-wild/huang2022-metastable-wild.md));
Farahbakhsh et al., “Characterizing Metastable Faults and Failures,” 2026
([arXiv](https://arxiv.org/abs/2606.00942),
[local extract](../related-work/extract/farahbakhsh2026-characterizing-metastability/html/2606.00942.md)).

## Model and evidence

The HotOS paper separates a trigger from a sustaining effect. A load spike,
capacity loss, or cache disturbance can move the system into a region where
retries, slow error paths, queueing, work amplification, or resource imbalance
keep it unhealthy after the trigger clears. Recovery may require explicit load
shedding, state reset, or capacity beyond what steady state appeared to need.

The OSDI study examines 22 incidents from 11 organizations and classifies
triggers and amplification along workload and capacity axes. It establishes
that the phenomenon is operational rather than merely theoretical and that
vulnerability varies by operating region.

The 2026 paper models a metastable fault as a destabilizing cycle among
individually stabilizing components. It derives vector fields over queues and
resources from executions and emphasizes scheduling: destabilizing transitions
can repeatedly win even when stabilizing actions exist.

## Decision edge and limits

Degradation experiments must include a post-injection phase, residual queue and
resource state, and a concrete recovery invariant. Attribution should test
cycle-breaking interventions and schedule competition rather than assign each
component an independent “flail score.” These papers characterize dynamics;
they do not provide the proposed cross-stack YA injection implementation.
