# Deterministic fault and delay simulation

> Read-backed digest (cluster D, trust `single-source` for the FoundationDB
> design report).

**Paper.** Zhou et al., “FoundationDB: A Distributed Unbundled Transactional
Key Value Store,” SIGMOD 2021
([PDF](https://www.foundationdb.org/files/fdb-paper.pdf),
[local extract](../related-work/extract/zhou2021-foundationdb/zhou2021-foundationdb.md)).

## Mechanism

FoundationDB runs production logic inside a deterministic discrete-event
simulator. Network, disk, time, randomness, process failures, latency, and
`BUGGIFY` branches are controlled by the simulation. Swarm testing varies
configuration and fault scenarios; the seed reproduces a failure exactly.

## Evidence

The paper describes this simulator as central to developing and validating the
database. It can accelerate long histories, inject rare faults and delays, kill
and restart processes, and exercise unusual tunable values without a separate
mock implementation of the database logic.

## Decision edge and limits

The design is strong precedent for pervasive controlled hooks, seeded scenario
records, and crash/recovery as a normal test path. The paper explicitly warns
that simulation is not reliable for performance issues. Its determinism also
depends on FoundationDB's Flow runtime; YA cannot inherit that guarantee by
adding delay hooks to ordinary Node and browser execution.
