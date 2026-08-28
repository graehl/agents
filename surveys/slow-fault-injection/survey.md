# Slow-fault and degradation injection

> **Mode:** grounded field survey. **Coverage cutoff:** 2026-08-28.
> The survey asks how prior work injects graded degradation, chooses injection
> points and schedules, observes cascades and recovery, and spans server and
> browser async boundaries. `[G]` marks a fetched and read primary source;
> `[R]` marks a metadata-verified primary source read through web retrieval but
> not retained as a local extract.

## Decision summary

The proposed **degradation-injection** discipline is mostly a synthesis of
established methods, not a new fault-injection method. The closest direct
overlap is *One-Size-Fits-None*: it sweeps delay and packet-loss severity,
location, workload, duration, and hardware limits across six distributed
systems, then measures steady-state degradation and recovery. It finds narrow,
system-specific danger zones, non-monotonic responses, workload dependence,
and residual effects after injection stops
([slow-fault sensitivity](concepts/slow-fault-sensitivity.md)) [G]. Fine-grained
delay points, guided search, deterministic delay/error simulation, and
perturbation-based optimization attribution also already exist separately.

What remains different is an engineering combination: one YA-owned aspect at
application async/queue boundaries, used for both observation and controlled
degradation, spanning provider runtime through server fan-out and relay to
browser reconciliation/rendering. The located work does not demonstrate that
same cross-layer hook or a browser-to-server performance/recovery map. That is
a plausible implementation gap, not a strong research-novelty claim. The
survey's falsification search and dimension map are in
[frontier.md](frontier.md).

The literature also changes the proposed analysis. Uniform slowdown and two
saturation curves are useful probes, but they do not identify a causal owner by
themselves. Start with one fault at a time; sweep severity closely enough to
find non-monotonic danger zones; distinguish injection, recovery, and residual
phases; record goodput and queue state rather than only aggregate tail latency;
then validate an optimization with a paired on/off intervention. Compound or
adversarial schedules come after the single-boundary map.

## Grounding and coverage

Fourteen primary papers were checked. Twelve have retained full-text Markdown
extracts under `related-work/extract/` and read-backed concept digests. Two
historical/fine-grained anchors, Limplock and Chronos, are `[R]`: their primary
papers were inspected through web retrieval, but their author hosts did not
yield a reproducible local extract. Detailed synthesis is therefore based on
the twelve `[G]` papers.

Search began from the seed's named lineages (Limplock/fail-slow, LDFI,
FoundationDB, Coz, metastability), followed backward and forward citations, and
then reframed around `transient delay injection`, `fine-grained slow fault`,
`Node.js delay injection`, `browser event race perturbation`, `slow-fault
recovery`, and `metastable failure characterization`. The browser/full-stack
claim received a separate falsification search. The search is focused rather
than exhaustive: it covers the closest method families needed to assess the YA
idea, not every chaos-engineering tool, storage fault injector, or concurrency
testing system.

Citation metadata and fetch state live in
[`related-work/papers.yaml`](related-work/papers.yaml). Concept pages link both
the primary source and the retained local extract.

## The discipline being situated

The user-directed proposal in `topics/perf.md` puts a common instrumented
aspect at worker queues and async boundaries on both server and browser. The
aspect reports timing/queue metrics and can add latency, cap throughput, raise
I/O errors, or crash its worker. Random exploration is the first implementation;
later passes use observed sensitivity to select individual and composed
degradations. The objective is not merely to provoke an exception: it is to map
how local degradation becomes user-visible latency, throughput collapse,
incorrect ordering, or slow/nonexistent recovery.

Reliable ordered transports narrow the semantics. Added service time or queue
delay may change interleavings, but an injector should preserve each boundary's
normal ordering unless reordering is explicitly the tested fault. Crash/resume
tests a documented durability prefix and eventual recovery. Storage errors are
a separate axis from storage delay. These distinctions matter because papers
that inject omission, exceptions, or reordered schedules do not automatically
validate a graded performance experiment.

## Prior-art map

### A. Slow faults already have a measurement discipline

Limplock's central result is that a single “limping” device can collapse a
scale-out system rather than merely reduce the affected node's contribution
[R]. The later FAST study assembled 101 fail-slow incidents from 12
institutions, spanning storage, network, CPU, and memory; it distinguishes
permanent, transient, partial-slowdown, and transient-stop behavior and records
fault conversion and cascading effects
([production fail-slow evidence](concepts/fail-slow-evidence.md)) [G]. These
papers establish the fault class, but do not supply a reusable application
async-boundary framework.

*One-Size-Fits-None* is the strongest overlap. Its harness runs initialization,
warmup, injection, and recovery phases while varying fault type, severity,
location, duration, workload, and host limits over Cassandra, HBase, HDFS,
etcd, CockroachDB, and Kafka [G]. The injector is external (`tc`/network
controls and a FUSE filesystem), so its points are coarser than the proposed YA
aspect. Its experimental lessons transfer directly:

- neighboring severities can lead to radically different outcomes;
- milder faults can be worse when stronger faults trigger failover;
- a follower or non-obvious location can hurt more than the nominal leader;
- hardware headroom and workload shape change the response; and
- recovery can leave queued work, bursty catch-up, or other residual effects.

It also shows a measurement trap: a severely slow interval may emit fewer
latency samples and therefore look deceptively benign in an aggregate tail.
Goodput/throughput and phase-separated latency are both required
([slow-fault sensitivity](concepts/slow-fault-sensitivity.md)) [G].

### B. Injection-point selection and search are established

Lineage-driven fault injection (LDFI) reasons backward from a successful
outcome's supports and asks a solver for crash/omission combinations capable of
cutting all of them. Repeated forward executions refine the lineage. Under its
bounded deterministic model, this replaces blind enumeration with relevant
fault combinations and found bugs in the evaluated distributed systems
([lineage-guided faults](concepts/lineage-guided-faults.md)) [G]. It is a
precedent for sensitivity-guided search, but its faults and correctness oracle
are not graded performance degradation.

Filibuster brings systematic fault injection to RPC calls exercised by ordinary
microservice tests. It instruments call boundaries in a tracing-like style and
uses the observed service graph to reduce redundant exception/timeout tests
([service-level faults](concepts/service-level-faults.md)) [G]. This is close to
the “one aspect” idea at service granularity. It does not cover internal queues,
browser rendering, or performance optimization.

Sieve studies 48 real fail-slow hardware bugs and locates a more specific
selection rule: synchronized and timeout-protected I/O points are unusually
vulnerable. Static analysis instruments those points, then delays one point per
test; its evaluation reproduced 34 of the 48 known bugs and found six unknown
bugs, two confirmed by developers
([fine-grained slow points](concepts/fine-grained-slow-points.md)) [G]. Chronos
similarly combines fine-grained transient delay with deep-priority fuzzing and
reports 27 timeout bugs [R]. Together they substantially preempt novelty in
“instrument many internal boundaries and guide which delays to try.”

### C. Cascades require recovery-state and cycle analysis

Metastability separates a trigger from a sustaining feedback loop. Retry load,
slow error paths, cache loss, work amplification, and imbalanced capacity can
keep a system overloaded after the original disturbance is gone
([metastable recovery](concepts/metastable-recovery.md)) [G]. The OSDI incident
study analyzes 22 incidents at 11 organizations and classifies load/capacity
triggers and workload/capacity amplification [G]. This is direct support for
measuring hysteresis and time-to-recovery, rather than stopping the experiment
when the injected delay ends.

The 2026 characterization sharpens “flail attribution.” It models metastable
faults as destabilizing cycles among components that may each appear locally
stabilizing, and reconstructs queue/resource vector fields plus scheduling
choices from executions [G]. An intervention that disables one retry or caps
one queue can break a cycle, but its observed benefit depends on the competing
stabilizing and destabilizing transitions. The analysis should therefore look
for causal cycles and schedule dominance, not assign independent scalar blame
to every component.

### D. Perturbation for optimization already exists

Coz's causal profiler predicts the benefit of speeding a line or function by
virtually speeding it up: it pauses other threads while the selected code runs,
then relates the perturbation to developer-defined throughput or latency
progress points. The paper reports 17.6% average overhead and validates several
predictions with real optimizations
([causal perturbation](concepts/causal-perturbation.md)) [G]. It is the closest
precedent for using a perturbation control surface to prioritize optimization.

This precedent also marks a limit. Slowing one asynchronous boundary is not in
general the algebraic inverse of speeding it up: thresholds may trigger
failover, batching may improve, ordering may change, or a queue may enter a
different state. A YA slowdown map is excellent for finding fragility and
candidate owners. Exact speedup predictions require a Coz-like relative
perturbation or, more simply, the actual optimization measured on/off under the
same scenario.

### E. Deterministic and event-loop injection cover most implementation pieces

FoundationDB runs production logic in a deterministic discrete-event simulator
whose network, disk, time, randomness, faults, and unusual `BUGGIFY` branches
are controlled by a seed. Swarm testing varies configurations and faults, and a
failure is exactly reproducible
([deterministic simulation](concepts/deterministic-simulation.md)) [G]. This is
strong precedent for one test hook carrying delay/error behavior through a
large codebase. The paper explicitly says the simulator is not reliable for
performance results, and its reach depends on FoundationDB's deterministic
runtime architecture.

For JavaScript, NACD dynamically instruments Node core async APIs using
`Proxy`/`Reflect`, then injects random 0–500 ms delays around async functions,
callbacks, and promises while preserving connected callback order. On 23 race
benchmarks it had the best reproduction ratio in 78% of cases and averaged 2.5
runs to first failure
([JavaScript delay injection](concepts/javascript-delay-injection.md)) [G]. It
is server-side Node correctness testing, excludes timers and unmodeled
third-party APIs, and leaves browser support as future work.

EventRacer instruments WebKit event traces and detects browser event races; its
evaluation reports 75 harmful races across 21 Fortune 100 sites
([browser event control](concepts/browser-event-control.md)) [G]. It proves
that browser event boundaries can be instrumented at scale, but it detects
ordering conflicts rather than injecting component-local performance
degradation. The located browser-side work therefore narrows but does not fill
the full-stack YA combination.

## What is different in the envisioned YA optimization

The individual ideas are not new:

| YA ingredient | closest grounded precedent | remaining difference |
|---|---|---|
| sweep delay severity/location/workload and observe recovery | One-Size-Fits-None [G] | YA uses app-owned async boundaries and user-visible browser outcomes |
| instrument one common boundary abstraction | Filibuster, FoundationDB [G] | same observer/injector across server, wire/relay, and browser |
| choose promising internal slow points | Sieve, Chronos [G/R] | YA can use runtime queue/phase metrics in addition to static I/O patterns |
| guide combinations rather than sample blindly | LDFI, Filibuster [G] | optimization/recovery oracle rather than only correctness failure |
| infer which work is worth optimizing by perturbation | Coz [G] | asynchronous distributed/browser path and recovery transient |
| shake JavaScript scheduling with delays | NACD, EventRacer [G] | browser performance/cascade mapping, not only event-race reproduction |
| test lingering overload after disturbance | metastability literature [G] | project-local, full user journey with a shared control plane |

The likely contribution is therefore a **YA-specific, full-stack causal
instrument**: a single scenario can perturb provider intake, server processing
and fan-out, transport/relay, client reconciliation, and render commit while
using the same phase clocks to report both local queue behavior and final user
latency. It becomes more useful than an ordinary benchmark because it asks
counterfactual questions inside one revision. It becomes more useful than an
ordinary fault injector because it carries the perturbation to a visible
browser outcome and recovery phase.

That integration could be generally instructive if it reveals a reusable
boundary contract or a browser-specific cascade absent from the located work.
On present evidence it should be described as implementation novelty and a
measurement synthesis, not as a new algorithm or unexplored research field.

## Experimental recipe implied by the literature

1. **Name the scenario and phases.** Record seed, revision, workload, host
   capacity, warmup, injection interval, recovery interval, and the exact
   boundary configuration.
2. **Use one fault at a time first.** Select representative boundaries from
   queue, synchronization, timeout, and high-rate paths. Establish a clean
   baseline before compound faults.
3. **Sweep severity, not just presence.** Probe closely around the first knee
   and preserve non-monotonic results. Test more than the nominal owner/leader.
4. **Keep fault semantics typed.** Distinguish wait-before-service,
   service-time inflation, throughput release/cap, error, crash, and explicit
   reorder. Preserve normal ordering by default.
5. **Measure useful work and state.** Record goodput, phase-specific latency,
   queue depth/wait, error/correctness outcomes, resource pressure, recovery
   time, and residual backlog/memory. Do not infer health from aggregate p99
   alone.
6. **Search for interactions only after the map exists.** Use lineage,
   observed queue dependencies, or cycle hypotheses to choose pairs and
   adversarial schedules. Random compound sampling remains a smoke test, not a
   coverage argument.
7. **Validate optimization causally.** Use an opposing intervention or the
   actual optimization on/off under the identical seeded scenario. A slowdown
   sensitivity ranks candidates; it does not by itself predict the gain.
8. **Check recovery explicitly.** Stop the perturbation and wait for a stated
   invariant: correct recent state, bounded backlog, restored goodput/latency,
   and no oscillation.

## Limits

- The corpus is anchored in distributed storage, microservices, Node, and web
  event-race work. It is not an exhaustive survey of chaos products, Linux
  kernel fault facilities, storage crash consistency, or browser test tools.
- Most evaluated systems use synthetic or benchmark workloads. Transfer to
  YA's long interactive sessions and real browsers requires local measurement.
- The full-stack/browser gap is a negative search result, not proof of absence.
  New systems or papers may use different vocabulary.
- None of the located papers validates that every async boundary should be
  instrumented. Sieve and Filibuster instead support selective points and
  dynamic reduction; YA should earn broader coverage incrementally.

## Primary-source index

The read-backed pages are:

- [production fail-slow evidence](concepts/fail-slow-evidence.md) [G]
- [slow-fault sensitivity](concepts/slow-fault-sensitivity.md) [G]
- [lineage-guided faults](concepts/lineage-guided-faults.md) [G]
- [service-level faults](concepts/service-level-faults.md) [G]
- [fine-grained slow points](concepts/fine-grained-slow-points.md) [G]
- [metastable recovery](concepts/metastable-recovery.md) [G]
- [causal perturbation](concepts/causal-perturbation.md) [G]
- [deterministic simulation](concepts/deterministic-simulation.md) [G]
- [browser event control](concepts/browser-event-control.md) [G]
- [JavaScript delay injection](concepts/javascript-delay-injection.md) [G]

Reference-only anchors: Do et al., *Limplock* (SoCC 2013) and Chen et
al., *Chronos* (IEEE S&P 2024) [R]. Their citation metadata and source links are
kept in the manifest; no detailed result in this survey depends on an
unretained extract.
