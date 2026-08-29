# Degradation injection

> Stress-test discipline where named worker queues and async boundaries —
> server-side and browser-side alike — carry an instrumented aspect that
> both reports metrics and accepts artificial degradation (added latency,
> capped throughput, injected storage-failure rate, injected crash
> probability), mapped one fault at a time before sensitivity-guided and
> composed adversarial scenarios (field terms: fault injection, latency
> injection, slow faults).

Topic: `degradation-injection`

User-directed trial (2026-08-28), promoted so perf-improvement
sessions actually apply it; evaluate and retire or keep after use.
Measurement hygiene — process cleanup, host baselining, ratchet
keying — stays in [perf](perf.md), which this discipline inherits.

When improving or stress-testing a concurrent or distributed system —
including a web app's server queues, websocket paths, and browser-side
components/event handlers — give every worker queue and async boundary
an instrumented aspect that both reports metrics and accepts
artificial degradation: added latency, capped throughput, an injected
I/O failure rate at storage aspects, and an injected crash
probability — the janky end-user OS/browser/hardware platform is a
real deployment target, not a tail case. Then:

- **Choose injection sites from a system theory.** Slowdown hooks do
  not replace architectural and code reading. For an overall-UX
  performance bug report, first trace the user-visible path and choose
  boundaries whose queueing, fan-out, batching, storage, or rendering
  work could plausibly govern the symptom. A test-only site may be
  added speculatively to validate or falsify that theory before an
  ordinary profile proves it hot; record the theory, predicted
  downstream metric or phase, and realized perturbation. A site whose
  dose sweep has no predicted end-to-end effect is negative evidence,
  not a hotspot merely because it was instrumented.
- **A small observed share is a floor conditioned on scenario and
  scale, not a ceiling.** A dose sweep or end-to-end attribution
  measures a site's share of one workload mix at one scale point; it
  caps neither the site's share of a single user-visible operation
  (a site diluted to a few percent of the mix can own half of one
  operation) nor its share where a scaling parameter grows. In an
  interactive application the latency of every user-driven action
  matters, so a single-workload share systematically undervalues
  sites that govern individual actions. Triage with scenario
  identification as an explicit intermediate step: a low-share site
  with an obvious cheap fix enters as a speculative candidate; before
  selecting it for improvement, identify the reachable scenario(s) it
  bottlenecks — name the driving parameter (data size, session
  length, message rate) and why real or adversarial-but-reachable use
  attains that regime — then rank candidates by the importance and
  likelihood of those scenarios, not by aggregate share. A scenario
  handcrafted so the site is the bottleneck
  is validation apparatus, not impact evidence, until that regime is
  shown reachable. When the fix lands, record its effect on both the
  demonstration scenario and the original observed suite — an
  off-one-operation percentage is not aggregate recovery; Amdahl
  still caps the mix at the site's measured share there. Worked
  incident (2026-08-29, ya
  `gaps/perf-sprint-system-observed-followups.md`): injection sites
  jointly under 20% of an aggregate scenario contained one owning
  49–57% of a single server operation and one whose older-page
  prepend ran a 1.27 s long task at real transcript scale; fixes
  selected per-operation cut that scroll path's p95 from 200–233 ms
  to ~17 ms.
- **Use external resource pressure where process boundaries suffice.**
  Source hooks are unnecessary for some useful sweeps. A helper can
  occupy and continually touch a declared amount of physical memory,
  or consume a declared CPU/core share; prefer kernel or container
  controls such as memory high/max limits, CPU quotas, and CPU sets
  when they can constrain the target process tree directly. On one
  machine, put separately launched server and browser process trees in
  separate control groups so server and client pressure can be varied
  independently. Otherwise use an isolated pressure host, or run the
  client on another host through an SSH tunnel/remote forward. Record
  both the configured knob and realized RAM, reclaim/swap/pressure, CPU
  occupancy, and throttling. Deliberate pressure is an experimental
  input, not permission to treat unmeasured ambient contention as a
  ratchet-grade run.
- **Map cascade sensitivity.** Degrade one boundary at a time, sweep
  severity closely enough to expose non-monotonic danger zones, and
  measure useful work plus injection, recovery, and residual phases.
  Boundaries whose small degradations cascade are both optimization
  candidates and fragile points under load; confirm the optimization
  itself on/off, because slowdown is not generally the inverse of
  speedup across queues, thresholds, batching, or failover.
- **Start random, graduate to guided.** The easy build is the right
  start after architecture and code reading define a plausible site
  set: one global "how bad" knob and random choices of one boundary and
  severity. Add random subsets only after the single-boundary map;
  sensitivity ranking, observed queue dependencies, and causal-cycle
  hypotheses then guide composed scenarios. The explored set must
  still include massive
  *correlated, adversarial* scenarios — remote-exploit DoS flooding,
  crash storms — which random sampling essentially never composes.
  There the pass criterion is sensible eventual recovery once the
  assault stops, not graceful service during it.
- **First analyses: dual saturation probes, then cycle attribution.**
  The opening questions are dual walks to the saturation boundary:
  what happens as load / request rate / data size increases, and what
  happens when everything slows until offered load is barely
  sustainable. Graphs are not the goal — the goal is identifying
  which parts of the system amplify stress or lengthen recovery once
  stress is relieved. Attribute that behavior with paired
  interventions over the same seeded scenario and inspect
  destabilizing cycles among queues/resources rather than assigning
  independent scalar blame. Analysis strategies: the survey's
  `Experimental recipe implied by the literature` section.
- **Output system-observed-performance code hotspot pointers.** A
  useful analysis result is a ranked set of pointers to code regions
  or compilation units where a projected marginal speed or memory
  improvement changes an externally observed system metric: latency,
  goodput, queue growth, recovery time, or residual memory. These are
  causal optimization candidates, not raw CPU-usage hot spots. Each
  pointer should name the scenario, affected metric, evidence, owning
  code, and likely intervention: usually a manual code edit, and where
  supported, targeted compiler-optimization markup or compilation-unit
  settings. Validate the actual change on/off before claiming its
  projected value.
- **Delays, not drops.** With reliable in-order transports (the
  current stack), packet-loss injection exercises a layer that is not
  there; message delay is the perturbation of choice. Loss becomes
  interesting only where a custom non-TCP-semantic reliability layer
  turns it into reordering.
- **Reordering is a first-class intent.** Variable/random per-message
  slowdowns are meant to induce reordering wherever ordering is not
  guaranteed. Apply *explicit* reorder injection only in channels known
  to admit out-of-order delivery — an out-of-order retransmit/accept
  discipline — not in in-order channels.
- **Crash/resume is in scope — it is the normal path.** Distributed
  systems pretty much always auto-restart crashed queue workers and
  even queue servers, so crash injection exercises a recovery path the
  system already promises to take, not an exotic fault. Client
  crash/resume is always a test axis. Where persistent data exists,
  add database-style server crash/recovery — tested against the
  actual durability contract, not an imagined one: a journaled
  filesystem giving approximately atomic writes, where losing the
  last message(s) is acceptable because nothing waits for a *really*
  committed write (and storage hardware may not deliver true commit
  even when asked). The recovery invariant is a consistent recent
  prefix, not zero loss.
- **One hook, three uses.** Keep the degradation knob inside the same
  instrumented aspect that reports metrics, so it serves profiling,
  stress tests, and regression suites without parallel plumbing. The
  browser analogue: wrap component event handlers so a test build can
  delay them like any server queue.

Grounded prior-art map and YA novelty check:
[`surveys/slow-fault-injection/`](../surveys/slow-fault-injection/survey.md).
