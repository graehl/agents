# Perf measurement discipline

> Discipline for performance measurement runs: mandatory cleanup and
> survivor checks for every spawned process, host contention/variance
> baselining before trusting numbers, host-class-keyed ratchet
> accumulators, and record conventions for parameterized
> client/server perf runs.

Topic: `perf`

Binds whenever a session launches processes to measure performance —
benchmark scripts, ratchet suites, load simulations, profiling — on
a host it does not exclusively own, which is the default: dev hosts
carry live servers the user relies on, peer agents, and the user's
own processes. A *ratchet* here is a committed pass/fail threshold a
measured metric must stay inside. A repo-local `topics/perf.md` (or
a named suite topic, e.g. ya's `performance-regression-suite.md`)
refines this doc for its project.

## Cleanup is part of the measurement

A perf run is finished when its numbers are recorded **and** every
process it spawned is dead and verified dead. Worked incident
(2026-08-08, ya `tasks/066-perf-regression-survey.md`): a perf
survey left orphaned measurement processes; the production :3400
server became unusably slow until the user manually restarted it.
The numbers were fine; the session still degraded the host for its
owner.

- **Tag everything you spawn, in argv.** Launch isolated server
  instances, dev servers, headless browsers, watchers, load
  generators, and fixture writers with a distinctive marker the
  sweep can match. The marker must be argv-visible — an explicit
  `--run-id <id>` argument, a dedicated port range, an app-data
  path under the suite dir — because `pgrep -f` matches command
  lines only. A `PERF_RUN_ID` environment variable does not appear
  in argv (checkable only via `/proc/<pid>/environ`), so an env
  marker supplements the argv one, never replaces it.
- **Manifest at launch, not reconstruction after.** Record pid,
  pgid, port, and role in a run-local manifest as each process
  starts. Launch each scenario in its own process group (`setsid`)
  so teardown starts with `kill -- -<pgid>`; prefer a cgroup or
  systemd scope (`systemd-run --user --scope`) where available,
  since a process group is not a complete descendant boundary —
  browser helpers re-daemonize out of it. Either way the post-run
  marker sweep, not the group kill, is the authoritative survivor
  check.
- **Teardown runs on failure paths.** Crashed scenarios are the main
  orphan source; drivers trap `EXIT`/`INT`/`TERM` and kill their
  process groups there too.
- **Sweep before, verify after.** Before a run, and again before
  ending the session or claiming completion, run `perf-sweep
  <marker>` (spec: `~/agents/topics/helper-scripts.md`; fall back to
  `pgrep -f <marker>` where it is not installed). It reports
  survivors and their unmarked group-mates and exits 0 only when
  nothing matches; reap with `--kill` (add `--kill-group` to take
  each survivor's whole group). An orphan you cannot kill is
  reported, not shrugged off.
- **Kill only by marker.** Never `pkill node` / `pkill chrome`-style
  sweeps on a shared host — peers and production run the same
  binaries. This is the shared-workdir discard ban's process-space
  analogue.
- **Production is out of bounds.** The live server/app a user relies
  on is never measured in place, restarted, or killed to tidy up (a
  restart is a big-effect state change — evidence first). If your
  run degraded it, say so immediately rather than silently fixing
  it.

Debris the sweep finds is a finding, not just mess. When teardown
claimed a clean exit yet the next sweep still catches survivors,
name the source before reaping: a harness teardown bug, or a
lifecycle defect in the measured system itself — a server that
orphans its helpers on shutdown is a real measurement result, and it
goes to the measuring agent's attention (a `gaps/` entry or task
note), not silently into the kill. `GROUPMATE:` and `src=env`
lines — processes that inherited a survivor's group or the marker
environment but carry no argv marker — are the usual tell that the
measured system, not the driver, spawned the debris. `perf-sweep`
exits nonzero whenever debris existed, even after a clean reap, so a
driver that gates the next run on exit 0 cannot overlook it.

## Host baseline: contention and variance

Establish two facts before treating a local number as comparable
evidence, and record both with the run:

- **Contention** — who else is on the host now: live production
  servers, peer agents (`.agentctl/active`), GPU jobs, browsers;
  loadavg vs. core count, free memory. Record a one-line co-tenancy
  summary and before/after load per run.
- **Variance** — same-configuration spread: ≥3 repetitions of a
  representative scenario at one SHA; ratchet margins derive from
  that measured spread (ya's suite sizes margins for an estimated
  ≥99.9% unchanged-run pass rate), never from optimism.

A run under contention the calibration did not include is
diagnostic-grade, not ratchet-grade: a ratchet failure there means
"re-run under calibration conditions" first and "regression" only
second. Flag such runs in the record instead of accumulating them
as comparable.

## Optimization work measures itself

Every perf-motivated change records its own before/after under the
project's suite convention (`AGENTS.global.md § Feature validation` scoped
to perf). Reworking a facility whose gain was measured re-runs that
facility's benchmark — updating the benchmark to compile is not
re-running it. Worked incident: ya's 064 review arc reworked
several measured 062 facilities with strong correctness evidence
and no perf re-assessment; the 066 survey later found persistent
session-detail losses hiding behind endpoint-flat comparisons.

## Fresh runners when policy allows

Where project policy authorizes cloud workers (AWS or similar) or
CI (e.g. GitHub Actions), prefer them for ratchet-grade numbers: a
freshly provisioned guest with no peer agents or production
tenants, and one instance type or runner class is one host class.
"Fresh" is a guest-level guarantee only — hosted runners and most
cloud VMs share physical hosts, and on GitHub-hosted runners
noisy-neighbor variance is routine, not an edge case: CodSpeed
(a stable-runner vendor, but measuring) reports ~2.7% coefficient
of variation across 100 runs vs. ~0.6% on tuned bare metal, enough
that a 2% pass/fail gate false-alarms roughly 45% of the time. So
calibrate variance per runner class exactly as for a local host,
size margins accordingly, and reserve tight ratchets for
dedicated/bare-metal instance types or self-hosted runners.
Scraping perf data from CI runs into the accumulator is a
sanctioned pattern — key it by runner class. The local shared host
stays right for back-to-back A/B on one change, phase attribution
and profiling, and smoke checks — relative same-session comparisons
a fresh runner would only slow down.

## Accumulator keying: host class, then host

Perf accumulators and ratchet targets group by **host resource
class**: an explicit recorded string derived from the facts that
determine performance — CPU model and core count, memory size,
storage type, GPU when relevant, pinned runtime (e.g. Node major).
Numbers compare, and targets bind, only within one class. The
particular host is additionally logged per run for diagnostics
(hostname plus the raw facts) so a one-machine anomaly stays
traceable — but the ratchet key is the class, never the hostname.
CI runner labels/instance types are classes the same way.

## Run-record conventions (parameterized, client-server)

- One JSON object per run, appended to JSONL: run id, timestamp,
  measured-tree SHA plus dirty flag (content-address the harness
  itself, as ya's suite does, so unrelated worktree edits cannot
  relabel a measurement), fixture identity, scenario and
  scale-point parameters, universe, host class plus host
  diagnostics, raw samples per metric (not only aggregates), and
  correctness-check outcomes — fast-but-wrong is not a baseline, so
  a run failing correctness checks carries flagged numbers.
- **Universes stay separate.** Server-side and client-local
  (browser) measurements are distinct ratchet universes with
  different variance profiles; a client metric depends on both the
  client and server hosts, so its record names both.
- Committed vs. local: ratchet targets live in a small committed
  file keyed by (universe, scenario, metric, host class); raw JSONL
  results are local or CI artifacts, not committed. Durable
  conclusions go to a topic doc, per-regression handoffs to
  `gaps/`/tactical files — ya's split
  (`topics/performance-regression-suite.md` +
  `gaps/perf-regressions-survey.md`) is the model.
- Query layer — unevaluated candidates, not binding policy: DuckDB
  (reads JSONL natively) or SQLite for ad-hoc analysis; Bencher,
  Conbench, or github-action-benchmark for a hosted dashboard with
  regression alerts. None has been tried in these projects; the
  binding conventions are the record schema and keying above, which
  any of these can sit on. In agentctl-tracked projects, launch
  measurement runs through `agentctl start` so argv/cwd/git
  provenance comes free.
