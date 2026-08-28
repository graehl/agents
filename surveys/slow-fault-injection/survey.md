# Field map: slow-fault / degradation injection testing

> Prior art for stress-testing concurrent and distributed systems by
> artificially degrading (not crashing) components — added latency, reduced
> throughput — at instrumented async boundaries, with guided rather than
> purely random exploration of the degradation space.

**Grounding mode: ungrounded (recall-only), persisted at user direction
2026-08-28.** Every claim below is model recall as of a January 2026
knowledge cutoff. No source was fetched or read; venues, years, and author
lists may be wrong; no claim is graded above single-source. The
research-survey invariant says ungrounded output is never persisted — this
file exists anyway because graehl explicitly asked for a placed ungrounded
seed. Treat it as a search plan, not reference material, until a grounded
pass replaces this banner. `concepts/`, `related-work/`, and the
survey-scoped `GLOSSARY.md` are deliberately absent: those tiers require
fetch+read.

## The discipline being situated

graehl's (independently derived) proposal: every worker queue and async
boundary in a system — server-side queues, websocket paths, and
browser-side JS components/event handlers alike — carries an instrumented
aspect that both reports metrics and accepts artificial degradation (added
latency, capped throughput). Stress testing then explores degradation
settings — random-first, since that build is easy, graduating to
cascade-sensitivity analysis (which boundary's small degradation
propagates to user-visible harm?) and composed adversarial scenarios.

Scope refinements (2026-08-28): delays are preferred over packet drops —
loss injection is out of scope while all transports are reliable and
in-order, and matters only where a custom non-TCP-semantic reliability
layer converts loss into reordering. Inducing *reordering* is an explicit
intent of the variable/random slowdowns; direct reorder injection is
reserved for channels whose out-of-order retransmit/accept discipline
already admits it. This narrows the relevant prior art: cluster A's
loss/partition nemeses are motivation, not method — the delay attacks are
the transferable part.

Crash/resume is definitely in scope, framed as the normal path:
distributed systems routinely auto-restart crashed queue workers and even
queue servers, so crash injection tests promised recovery, not an exotic
fault. Client crash/resume always; server crash/recovery where data is
persistent, against a relaxed durability contract — journaled-filesystem
approximate write atomicity where the tail may be lost, since nothing
waits for a truly committed write (which storage hardware may not honor
anyway). The recovery invariant is a consistent recent prefix, not zero
loss.

Degradation also includes an injected *storage failure rate* — I/O
operations erroring at a controllable rate, distinct from both slowness
and crash — and an injected *crash probability*, motivated by janky
end-user OS/browser/hardware platforms where client crashes are a base
rate to engineer for, not a tail case; this makes the crash/resume axis a
per-aspect knob rather than only a composed scenario. Recall-only prior art: Linux device-mapper fault targets
(dm-flakey, dm-delay, dm-dust), SQLite's VFS-level systematic I/O-error
injection in its test harness, CharybdeFS (FUSE fault injection,
ScyllaDB), and the filesystem-reaction literature — IRON file systems
(Prabhakaran et al., ~SOSP 2005), latent-sector-error field studies
(Bairavasundaram et al.). Recall-only prior-art pointer for that axis: the crash-consistency
testing lineage — ALICE (Pillai et al., ~OSDI 2014, application-level
crash vulnerabilities on journaled filesystems), CrashMonkey/B3 (~OSDI
2018), and fsync-failure studies (~ATC 2020) — plus cluster D's
simulators, which already treat process kill/restart as a first-class
injected event.

The non-random exploration requirement has a second motivation beyond
search efficiency: coverage must include massive correlated *adversarial*
degradation — remote-exploit DoS flooding, crash storms — which random
sampling essentially never composes, and the invariant tested there is
sensible eventual recovery once the assault stops. That is precisely the
metastable-failures concern (cluster C: degradation-triggered feedback
loops that persist after the trigger clears), so cluster C is method for
this axis, not just motivation.
Operational statement: `topics/perf.md § Degradation injection`.

## Clusters (all recall, uncited-in-the-verified-sense)

### A. Chaos engineering / system-level fault injection

Netflix Chaos Monkey and the chaos-engineering literature (Basiri et al.,
~2016, IEEE Software) established injecting faults into production-like
systems; commercial tools (Gremlin) and Kubernetes-native ones (Chaos
Mesh, LitmusChaos) include latency attacks, usually via network-level
`tc netem`. Jepsen's nemesis injects partitions and delays at the network
boundary. **Closest deployed analogue:** Envoy/Istio per-route fault
injection — declarative delay and abort percentages at every service
boundary — which is the user's "aspect" at service granularity, but
network-boundary-only and unguided.

### B. Guided exploration of the fault space

Lineage-Driven Fault Injection (LDFI; Alvaro et al., ~SIGMOD 2015, the
Molly system; productionized at Netflix ~SoCC 2016) uses the provenance of
a successful outcome to pick exactly the fault combinations that could
break it — the strongest precedent for "cascade sensitivity analysis
guiding settings explored" rather than random fuzz. Filibuster
(Meiklejohn et al., ~2021) systematically explores service-level fault
injections in microservice test suites. These target crash/omission
faults more than graded slowness.

### C. Slow faults as a distinct, worse fault class

The motivation literature: Limplock (Do et al., ~SoCC 2013) shows one
limping component (e.g. a degraded NIC) cascading into cluster-wide
stalls; "Fail-Slow at Scale" (Gunawi et al., ~FAST 2018) catalogs
real-world fail-slow hardware; "Gray Failure" (Huang et al., ~HotOS 2017)
names the differential-observability problem; metastable failures
(Bronson et al., ~HotOS 2021, with an OSDI follow-up) show
degradation-triggered feedback loops that persist after the trigger
clears. Together: slowness injection finds failure modes crash injection
cannot, which is the core argument for the user's discipline.

### D. Built-in degradation knobs at every marked point

FoundationDB's simulation testing with `BUGGIFY` macros — code points
that deliberately misbehave (including delays) only under deterministic
simulation — is the nearest thing to "every async has an instrumented
aspect that can be made slow," proven over years of finding rare bugs.
TigerBeetle's VOPR simulator and Antithesis (deterministic-hypervisor
testing, by ex-FoundationDB people) generalize the approach. These are
crash-and-delay simulators for one codebase/deterministic runtime, not a
cross-stack instrumentation discipline.

### E. Concurrency schedule perturbation (single machine)

Injecting delays at synchronization points to shake out interleavings:
ConTest noise injection (IBM, Edelstein et al., ~2002), CHESS systematic
scheduling (Musuvathi et al., ~OSDI 2008), PCT randomized priority
scheduling with probabilistic bug-finding guarantees (Burckhardt et al.,
~ASPLOS 2010), rr's chaos mode, Microsoft Coyote. This is the
multithread-one-machine ancestor of the discipline: delay injection as
schedule fuzzing, sometimes with principled (not random) schedules.

### F. Sensitivity/causal measurement via perturbation

Coz causal profiling (Curtsinger & Berger, ~SOSP 2015) measures "what if
component X were faster" by slowing everything else — literally the
measurement dual of degradation injection, and evidence the
perturb-to-attribute logic is sound. Pivot Tracing (Mace et al., ~SOSP
2015) installs dynamic instrumentation aspects that report metrics across
component boundaries — the metrics half of the user's aspect, without the
degradation half.

### G. Performance fuzzing (input side)

SlowFuzz (~CCS 2017) and PerfFuzz (~ISSTA 2018) fuzz *inputs* to find
algorithmic slowdowns. Dual to the discipline: they search input space
for slowness, the discipline searches component-degradation space for
cascade fragility.

### H. Browser/JS async perturbation — candidate void

Known adjacent art: DevTools CPU/network throttling (global and coarse),
test-framework fake timers, Playwright/Puppeteer network-interception
delays, and web event-race detection (EventRacer lineage, Petrov/Raychev
et al., ~PLDI 2012). I recall no established framework for per-component
/ per-event-handler degradation aspects in browser code, let alone one
unified with server-side aspects under one sensitivity-guided explorer.
**Candidate void only:** recall cannot rule out that it exists, and the
research-survey rule requires a recorded falsification search before any
void becomes a capstone claim.

## Analysis methods and strategies (ungrounded)

Construction is deliberately the easy half — one global "how bad" knob,
random per-boundary slowdowns, random subsets relaxed back to normal —
and random fuzz is the right starting point. Analysis is the hard half:

- **Dual saturation probes.** First questions: raise offered load /
  request rate / data size at fixed capacity, and dually, slow every
  component uniformly until the fixed offered load is barely
  sustainable. Both walk to the saturation boundary from opposite
  sides. Queueing theory puts the latency knee near utilization 1; the
  Universal Scalability Law (Gunther, ~2007) fits
  contention/coherence penalties to such curves. Map where the knee is
  and which user-visible metric hits it first.
- **Hysteresis / recovery curves.** Sweep stress up then back down and
  plot both directions. A hysteresis loop — the system not returning
  promptly once stress is relieved — is the metastability signature,
  in cluster C's trigger/sustaining-effect vocabulary. Also plot
  recovery time versus stress episode duration and depth.
- **Flail attribution.** The stated goal beyond graphing: identify
  which components make things worse — amplify stress (retry storms,
  timeout-triggered rework, unbounded queue growth, GC/allocator
  pressure) or lengthen recovery after relief. Method sketch: fix a
  standard stress episode and measure time-to-normal; then clamp one
  component's stress response (cap its queue, disable its retries,
  freeze its timeouts) and re-measure — the recovery-time delta is
  that component's flail contribution. This is Coz-style what-if
  attribution (cluster F) applied to the recovery transient rather
  than steady-state throughput.
- **Remediation art once flail is attributed** (recall-only): overload
  control and load shedding (SEDA lineage, admission control, recent
  overload-control systems ~Breakwater), retry budgets and jittered
  exponential backoff from SRE practice, circuit breakers.

## Positioning (ungrounded synthesis)

Each ingredient is individually precedented: degradable knobs at marked
points (D), latency injection at service boundaries (A), guided
exploration (B), slowness as the fault class worth testing (C),
perturbation-based attribution (F). The apparent unclaimed combination is
*uniform instrumented aspects across the full stack including browser-side
handlers, where the same aspect serves metrics and degradation, explored
under cascade-sensitivity guidance*. Cluster H is where novelty most
plausibly survives a grounded pass; clusters B/D are where it most
plausibly dies.

## Grounding next steps

1. Fetch/read anchors: LDFI, Limplock, Coz, FoundationDB testing
   write-ups, metastable-failures papers; verify all recalled citations.
2. Falsification search for cluster H (browser-side degradation
   injection): try "fault injection web frontend", "latency injection
   JavaScript event handler", event-loop instrumentation literature.
3. Scaffold `related-work/` via `related-work init` and replace this
   banner with a grounded coverage statement.
