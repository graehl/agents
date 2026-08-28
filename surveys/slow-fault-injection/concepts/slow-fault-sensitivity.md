# Slow-fault sensitivity and recovery maps

> Read-backed digest (cluster A, trust `single-source`; closest direct method
> match to the proposed degradation-injection experiment).

**Paper.** Lu et al., “One-Size-Fits-None: Understanding and Enhancing
Slow-Fault Tolerance in Modern Distributed Systems,” NSDI 2025
([USENIX page](https://www.usenix.org/conference/nsdi25/presentation/lu),
[PDF](https://www.usenix.org/system/files/nsdi25-lu.pdf),
[local extract](../related-work/extract/lu2025-one-size-fits-none/lu2025-one-size-fits-none.md)).

## Method

The study evaluates Cassandra, HBase, HDFS, etcd, CockroachDB, and Kafka. Its
pipeline separates initialization, warmup, fault injection, and recovery and
varies network packet loss, network delay, filesystem delay, severity,
location, duration, workload, and hardware resource limits. Network controls
and a FUSE filesystem inject faults outside the systems. Repeated trials and
confidence intervals distinguish stable effects from run noise.

## Evidence

Slow-fault tolerance is not monotonic or transferable across systems. Narrow
severity changes can cause qualitatively different outcomes; a milder fault can
be worse when a stronger fault triggers re-election or failover. Followers can
be more damaging locations than leaders, additional CPU can worsen relative
degradation, and workload shape changes the result. Delay recovery is often
quick, while loss can produce longer recovery; some trials retain backlog or
bursty catch-up after injection stops.

Aggregate latency is a poor sole oracle because a severely slow interval may
complete fewer requests and therefore contribute fewer latency samples.
Throughput/goodput and phase-separated latency are both needed.

The paper also proposes Adaptive Data-driven Resilience (ADR), which traces
selected variables and update frequencies, adapts high-percentile thresholds,
and triggers mitigation. In the evaluated HBase and CockroachDB integrations it
reports 2.8% overhead and average 65% degradation reduction.

## Decision edge and limits

This work largely occupies systematic slowdown sweeping and recovery mapping.
YA differs in its internal and browser-side injection points and in reusing one
aspect for local metrics and counterfactual optimization. ADR assumes developers
already know what to trace and is a mitigation design, not the injection
framework itself.
