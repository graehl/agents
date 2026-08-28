# Lineage-guided fault selection

> Read-backed digest (cluster B, trust `single-source`).

**Paper.** Alvaro, Rosen, and Hellerstein, “Lineage-driven Fault Injection,”
SIGMOD 2015
([PDF](https://people.ucsc.edu/~palvaro/molly.pdf),
[local extract](../related-work/extract/alvaro2015-ldfi/alvaro2015-ldfi.md)).

## Mechanism

LDFI records the data/control lineage supporting a successful outcome, reasons
backward to combinations of failures that could cut every support, encodes that
condition for a SAT solver, executes a candidate fault scenario, and adds the
new lineage before repeating. The search spends executions on combinations
that could matter to the stated correctness goal rather than sampling every
message or process independently.

## Evidence

The evaluated implementation often used an order of magnitude fewer
executions than random fault injection and found seven bugs across fourteen
systems. Its completeness result is bounded by the explored input, failure
model, and deterministic/synchronous abstraction.

## Decision edge and limits

LDFI is a strong precedent for replacing random compound faults with causally
guided candidates. Its native fault model is crashes and message loss, and its
oracle is a correctness outcome. For degradation injection, observed queue and
phase dependencies could play the role of lineage, but graded severity,
continuous metrics, and recovery introduce state not covered by the original
bounded guarantee.
