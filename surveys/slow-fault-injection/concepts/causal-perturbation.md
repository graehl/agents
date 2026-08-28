# Causal perturbation for optimization

> Read-backed digest (cluster C, trust `single-source`).

**Paper.** Curtsinger and Berger, “Coz: Finding Code that Counts with Causal
Profiling,” SOSP 2015
([arXiv](https://arxiv.org/abs/1608.03676),
[local extract](../related-work/extract/curtsinger2015-coz/html/1608.03676.md)).

## Mechanism

Coz asks what program-wide progress would result if a selected line or
function were faster. It creates a virtual speedup by pausing other threads
while the selected code executes, varies the virtual speedup, and measures the
effect at developer-chosen throughput or latency progress points. The
experiment targets causal optimization potential rather than sampled time.

## Evidence

The paper reports 17.6% average profiling overhead, identifies optimization
opportunities conventional profilers miss, and validates several predictions
with actual code changes. It also exposes code where speeding a locally costly
region does not improve the named end-to-end outcome.

## Decision edge and limits

Coz supports perturbation as an optimization-prioritization instrument and the
need for an explicit progress oracle. A YA slowdown experiment is not an exact
inverse: asynchronous thresholds, queues, failover, batching, and ordering can
change the operating regime. Use slowdown sensitivity to find candidates, then
measure the actual optimization on/off or construct an opposing intervention.
