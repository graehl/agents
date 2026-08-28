# Perf sketches

> Candidate performance-measurement and optimization designs that are not
> current guidance.

## Code-growth-regularized load-capacity loop (user-proposed 2026-08-28)

**Proposal.** Try an unguided generate–measure–retain loop with the goal:
“optimize this for the same externally observed performance at `+X%` offered
load.” Here *unguided* means that the loop receives no code-hotspot pointers;
the system-level measurement oracle still supplies its acceptance signal. The
goal condition must include the maintenance cost of growing the codebase, not
treat code growth as a free way to buy capacity.

Evaluate candidates lexicographically:

1. correctness, ordering, and recovery invariants pass;
2. the candidate at `+X%` load matches the baseline's latency distribution,
   useful goodput, rejection/abandonment behavior, and recovery at current
   load;
3. the candidate does not regress current-load behavior or exceed stated
   resource ceilings; and
4. among passing candidates, prefer the lowest codebase-maintenance cost and
   require that cost to remain within an explicit budget.

Do not use raw lines added as the complete cost model; that rewards dense or
obscure code. Charge at least for net production-code growth, new dependencies,
public APIs/configuration/schema, duplicated mechanisms, branching and
cross-module coupling, and additional operational states. Credit deletion and
simplification only when the same checks still pass. Tests, documentation, and
evidence remain hard completeness requirements; account for their maintenance
cost separately so the loop cannot improve its score by omitting validation.

A server's main latency/goodput objective is per-request and intentionally
excludes one-time startup resources, so price those resources on separate
axes. The specification assigns declared weights to load time (start to ready)
and load memory (peak startup memory plus resident/process-tree memory at
readiness), measured for both baseline and candidate. Give these terms very low
weight for a long-lived server once repeated load cycles show that they are
genuinely fixed and bounded; they matter, but normally amortize over many
requests. During request service, also record peak resident memory, quiescent
memory after the workload drains, and resident-memory growth per completed
request or repeated load cycle. The last two distinguish bounded caches from
“never free memory” accelerations that a short per-request benchmark would
reward. Growth with requests is not startup overhead and does not receive the
low startup weight.

Keep a hard server resident-memory budget in addition to the weighted startup
costs and growth measurements. Enforce it throughout startup, request service,
and recovery with an OS/container process-tree limit such as a cgroup memory
ceiling, or on an isolated worker with a controlled physical-memory
reservation; a post-hoc RSS assertion alone is insufficient. Host-wide memory
pressure must never be introduced on a shared machine.

These terms prevent the loop from treating unbounded caching or precomputing
an excessive state space as free acceleration. A candidate that crosses the
hard memory limit or shows unbounded post-request growth fails even if its
throughput improves; one below the limit still pays its declared startup-time
and startup-memory costs when candidates are compared.

### YA long-session client condition

For YA, make session length an explicit sweep axis and weight the growth curves
of client performance and resources, not only their value at one short session
length. Measure at least append-to-visible latency, interaction and scroll
responsiveness, frame-time and missed-frame distributions, browser process-tree
resident memory, JavaScript heap, and quiescent memory after activity settles.
A fixed client startup cost may remain low-weight; a slope that grows with turns
does not.

Run this condition in a browser launched and owned by the performance harness,
so the suite controls its profile, fixture, lifecycle, measurement interfaces,
and process-tree accounting without perturbing the user's browser. Complete
history is a correctness invariant: every old turn exposed by the baseline
must remain scrollable, displayable, ordered, and content-identical at every
tested session length. Virtualization or lazy materialization may optimize the
implementation, but truncating old turns or shortening the measured history is
a failed candidate, not a performance improvement. The harness should scroll
back through sampled old turns and verify their content rather than inferring
retention from an internal count.

Provide a gather-and-replay path for representative joint client/server session
fixtures. Capture causally ordered provider and server-message logs, recorded
user interactions anchored to the UI state that enabled them, and expected
visible-state checkpoints. Replay the trace through the server and harness-owned
browser, preserving event dependencies and ordering while allowing intentional
timing/degradation changes; exact recorded wall-clock timing is an input profile,
not the causal contract. Collect server request/queue/resource metrics and
client frame time, interaction response, streaming updates, scrolling, and
historical-turn materialization in the same run. Sanitize captured content and
keep raw private-session traces out of committed fixtures.

Do not represent the interaction trace as a timed recording of raw key, mouse,
coordinate, or wheel events. Capture and replay above raw input, after the
browser/application has interpreted it as a semantic action such as submitting
a prompt, selecting a session, or scrolling to a turn; the exact stable
boundary remains to be chosen. Gate each replayed action on an observed screen
or application-state predicate. The time taken to reach that predicate is
performance data, not a fixed sleep to hide, and failure to reach it is a
recorded replay divergence.

Accept that replay can desynchronize: candidate server completion times and
client/server message sequences may diverge from the recording. Record replay
match coverage, the first consequential divergence, missing/extra/reordered
events, and timing drift rather than silently repairing the trace or discarding
the run. Retain its performance measurements, but label claims after a causal
divergence as diagnostic or conditionally comparable. The desynchronization
risk is worth accepting because representative session behavior supplies
client/server performance evidence that synthetic short traces miss.

Run the loop as a control for guided optimization. Compare trials and wall
time to reach the target, retained change size and maintenance cost, final load
headroom, and the kinds of edits found. This tests whether system-observed code
hotspot pointers actually make the search more efficient or merely explain
changes that an unguided loop would discover anyway.

Wake conditions: a project has an isolated, repeatable end-to-end performance
suite with a correctness oracle, sufficient variance calibration, and an
automated way to build and compare candidate edits without touching a live
service.
