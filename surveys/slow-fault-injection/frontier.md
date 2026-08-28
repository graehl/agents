# Frontier check: full-stack degradation injection

> Falsification record for the narrow claim that one application-owned
> observation/injection aspect spans server and browser async boundaries and is
> used to map performance cascades, recovery, and optimization targets.

## Claim tested

The seed proposed a possible void: per-boundary degradation injection across a
complete server-to-browser path, with the same hook reporting local metrics and
accepting delay/throughput/error/crash perturbations, followed by
sensitivity-guided exploration.

The claim was deliberately split into dimensions before searching. Otherwise
several adjacent systems could look novel only because they use different
names.

| system/paper | layer | injected behavior | objective | point selection | recovery map | same metrics/injection hook |
|---|---|---|---|---|---|---|
| One-Size-Fits-None | network + filesystem around distributed stores | loss, network delay, filesystem delay | degradation and recovery | factorial sweep | yes | no |
| Filibuster | RPC/service boundary | exceptions and timeouts | resilience correctness | observed service graph | no | tracing-style instrumentation, but not performance metrics |
| Sieve | internal synchronized/timeout I/O | long delay | fail-slow bug reproduction | static analysis + context | limited | no |
| Chronos | fine-grained distributed-system calls | transient delay | timeout bugs | deep-priority fuzzing | limited | no |
| LDFI | distributed data/control lineage | crash and omission | correctness | backward causal lineage | no | no |
| FoundationDB simulation | deterministic runtime abstractions | latency, errors, crashes, unusual branches | correctness | seeded swarm testing | some restart paths | common simulation controls, but unreliable for performance |
| Coz | lines/functions in multithreaded programs | relative virtual speedup | optimization impact | progress-point experiments | no | profiling control, not fault/recovery injection |
| NACD | Node core async APIs | random callback/promise delay | event-race reproduction | runtime API model | no | no performance map; server-side only |
| EventRacer | browser event trace | none; detects order conflicts | race detection | dynamic trace/filtering | no | no injection |
| metastability papers | distributed components/queues | incident triggers or modeled schedules | sustained failure/recovery | causal cycle analysis | central | analytic, not a reusable injection aspect |
| proposed YA instrument | provider→server→wire/relay→browser | delay, rate cap, I/O error, crash; reorder only explicitly | user-visible performance, correctness, recovery, optimization targeting | single-point map then runtime/cycle guidance | central | yes, by design |

## Falsification search

Searches used the primary-source indexes and citation graphs around the table,
plus the reframings:

- `browser latency injection event handler performance testing`
- `JavaScript async delay injection race detection`
- `full stack fault injection browser server`
- `frontend chaos engineering latency injection`
- `event loop perturbation browser`
- `fine grained transient delay distributed system`
- `causal profiling asynchronous distributed system`

The search found browser race tracing (EventRacer), Node async delay injection
(NACD), coarse browser/network throttling, service-level fault injection, and
distributed slow-fault harnesses. It did not find a read-backed system filling
all of the proposed layer, objective, recovery, and shared-hook cells.

## Verdict

The broad “degradation injection” method is not a frontier. Nearly every
ingredient is occupied, and *One-Size-Fits-None* is already a systematic
slow-fault sensitivity and recovery study. “Instrument every async boundary”
is also weakened as a novelty claim by Sieve, Chronos, FoundationDB, and NACD.

The narrower cross-layer combination remains open in this focused search:

1. application-owned points from server internals through browser render work;
2. one hook serving observation and injected degradation;
3. a user-visible performance and recovery oracle; and
4. perturbation results carried into actual optimization validation.

This is best treated as a **project-specific integration gap**. A stronger
research claim would require a broader systematic review of browser/frontend
testing and a demonstrated finding that depends on the cross-layer design.

## What would falsify even the narrow claim

- A system that instruments both backend and browser application async points,
  injects graded local slowdown/rate limits, and reports end-to-end performance
  and recovery from the same scenario.
- A browser-focused causal profiler whose intervention semantics cross a remote
  service boundary and validate predicted optimizations.
- Evidence that an existing tracing/fault framework can express the proposed
  YA experiment without new boundary semantics, leaving only configuration.

Until one is found, use “located gap” or “engineering synthesis,” not “novel
method.”
