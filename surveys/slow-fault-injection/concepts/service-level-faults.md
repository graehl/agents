# Service-level fault injection

> Read-backed digest (cluster B, trust `single-source`).

**Paper.** Meiklejohn et al., “Service-Level Fault Injection Testing,” SoCC
2021
([PDF](https://christophermeiklejohn.com/publications/filibuster-socc-2021.pdf),
[local extract](../related-work/extract/meiklejohn2021-filibuster/meiklejohn2021-filibuster.md)).

## Mechanism

Filibuster instruments RPC clients and servers in a style aligned with
distributed tracing. It reuses functional tests, observes the service graph and
actual calls, and systematically injects exceptions or timeout behavior at
those boundaries. Dynamic reduction avoids scenarios made redundant by the
observed topology and determinism assumptions; the relevant exponent becomes
the maximum branching factor rather than the total call-edge count.

## Evidence

The evaluation reproduced every bug in its microservice corpus and demonstrates
that developer/local testing can exercise resilience paths without a complete
production chaos environment. The method includes delayed responses and
timeouts, but the primary outcome is resilience correctness.

## Decision edge and limits

Filibuster is the closest “common aspect at every service boundary” precedent.
It supports instrumenting the real call path and pruning from observed
execution. It does not cover internal application queues, browser rendering,
continuous performance sensitivity, or recovery after a graded overload.
