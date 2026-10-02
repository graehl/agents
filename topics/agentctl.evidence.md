# agentctl — evidence ledger

Companion to `topics/agentctl.md`; conventions in
`topics/evidence-ledger.md`. Append-only.

## 2026-07-02 tending marker: machine-level GPU awareness deferred

The `tending:` header line and `agentctl tending` verb are per-project
by design (`.agentctl/` is project-rooted). graehl explicitly deferred
the wider idea — making all GPU users on a machine mutually aware
across projects, e.g. a machine-level tending registry keyed by
project+session so "will this GPU be re-claimed on someone's next
wake?" is answerable across checkouts — as "for now this is not
relevant to my needs." Revisit only if cross-project GPU contention
actually shows up: the failure the marker solves (two stewards racing
one on-deck queue) is per-project, and GPU oversubscription across
projects is already bounded by agentctl's resource gating at launch.

## 2026-07-02 tending design decisions

- The marker lives inside `.agentctl/active/<sid>` as a header line,
  not a parallel `tending/` dir. A tending session is a real peer (it
  appends on-deck status logs and launches jobs), unlike `awaiting/`
  whose whole point is *not* counting as a peer — that asymmetry is why
  awaiting got its own dir and tending does not. A second registry
  sharing the same identity, window, and sweep could also disagree
  with the first.
- `until <deadline>` is informative, not parsed or enforced; entry
  staleness (the 70-min window) is the enforcement. Enforcing it buys
  little: a crashed steward ages out within the window anyway, and a
  live one past deadline writes its final report and DONE per the
  steward skill.
- `on_deck.py eligible` *warns* about another fresh tending session,
  never refuses: taking over from a crashed-but-not-yet-stale steward
  must stay possible, and the pending→launched status flip on entries
  bounds the double-launch race. It also does not auto-register the
  caller as tending — the on-deck authoring skill runs `eligible` for
  validation, so auto-registering would mark directors as stewards and
  poison the signal. Registration stays explicit (steward skill step 1
  / `agentctl tending <id>` claim).
- `wait`/`watch`/`wait-gpu` mtime-touch the caller's active entry each
  poll (self-throttled to 300s, content never written, launch-depth
  guarded). Found while designing tending: `refresh_active_register`
  ran only on launches, so a session obeying the RUNS.md 55-min
  blanket wait cap that launched nothing between waits crossed the
  70-min window while demonstrably alive — a false absence that would
  have defeated both the peer check and the tending check. The 70-min
  window ≈ the ≤60-min steward wake cadence (55-min wait cap, 3600s
  fallback heartbeat) plus slack; the touch is what makes that
  arithmetic hold through long foreground blocks.

## 2026-08-16 watched launches need a durable completion owner

- On commit `a909383`, a scratch `start --watch` run launched a payload that
  slept and exited 0. Sending SIGTERM only to the `start --watch` frontend let
  the payload finish, but left no `exit-status.json`; the next `status` refresh
  produced `finished returncode=unknown`. The direct cause was the
  `args.watch` branch bypassing `_run-child`, so the observer alone owned the
  `Popen` handle and terminal-status write.
- The user asked to improve the compaction-surviving monitoring trigger, make
  `agentctl` detect the intent, or otherwise prevent the failure. The chosen
  invariant makes every start use `_run-child`; `--watch` only attaches to that
  durable run. A regression terminates the frontend, confirms the payload
  survives, and requires the later wait to return 0 with an exit-status
  sidecar.

Contributing-model: 5.6-Sol

## 2026-09-07 claim waits stream notices independently of session turns

- **User direction:** separate opt-in `session-turn send` eventual delivery
  from claim-clearance waits that emit notices while remaining blocked. The
  user approved separate per-wait notice files, archive-only cleanup, and no
  explicit acknowledgments. During implementation they requested waiting by
  default, `--deaf` for waiting without notices, and coordination instructions
  explaining when `--no-wait` is appropriate.
- **Storage decision:** `.agentctl/coordination/<wait-id>/` separates immutable
  notices from both participants' active records. The initial sender-owned
  active-record idea was a convenience, not a user preference. A stable outer
  transaction lock serializes publication and archival; a separate observer
  lock prevents concurrent observers claiming through one wait ID. Only the
  waiter's heartbeat controls staleness. No receipt directory is needed because
  cleanup retires whole waits and replay after interruption is acceptable.
- **Behavioral evidence:** `tests/test_agentctl_coordination.py` exercises the
  real CLI through live stdout pipes, checking notice visibility before exit,
  continued blocking, claim acquisition only after release, pause/replay,
  duplicate suppression, concurrent senders and owner updates, competing
  waiters, deaf rejection, stale/DONE behavior, and publication racing archive.
  The first integration test failed on the missing wait options before the
  implementation. Existing clear, active, alone, completion, and wrapper
  regressions pass with immediate-verdict callers using `--no-wait`.
- **Instruction trace: choose other work:** an agent seeking only the current
  conflict verdict uses `clear --no-wait`; it does not enter an unwanted wait.
  An agent intending to edit when possible uses the default, observes notices,
  and keeps the exit-0 claim prerequisite.
- **Instruction trace: dialogue without permission laundering:** an owner
  posts "push my changes" or "you can edit now". The typed peer event grants
  neither authorization nor clearance. The waiter may pause to converse; it
  still needs its own successful claim before editing and user authority for
  the proposed external action.
- **Instruction trace: interruption and cleanup:** the waiter pauses, sees a
  replay after resuming, and does not acknowledge individual notices. Explicit
  cancellation retires its wait; a killed process ages into stale. Sender
  notices cannot keep an abandoned wait or either active entry live.
  The monitoring packet explicitly recognizes a peer notice as an observation
  point for claim waits, so its general foreground-wait discipline does not
  prevent the intended pause for dialogue.
- **Remaining work:** `gaps/session-turn-eventual-send.md` replaces the mixed
  `gaps/agentctl-nudge-blocking-peer.md` for provider delivery. Historical
  references to the old filename remain historical; automatic peer turns
  retain the no-native-fallback/no-implicit-resume prerequisite.

Contributing-model: 6-Astra

## 2026-10-02 multi-job wait, per-run GPU use, advisory VRAM leases

- **Anchoring user direction:** the user asked whether agentctl could list
  running jobs and wait on a set of them "such that if a wait-for is sent
  just as a job finished, the 'finished' status satisfies without a 'no job
  running' error", as a cross-session GPU coordination facility. Already
  true for one job (`wait_job` reads persisted `current.json`); extended to
  several (`wait a b`, `a,b`, `--any`). The user then asked for per-run GPU
  detection with CPU/GPU resident memory in the default running list, and a
  "fractional" lease: "specify an amount of vram needed for run to be
  useful"; "relative specs (50% etc) are fine too - don't round so as to
  block two 50% from being placed"; leases stated as advisory; a slower
  accurate measurement; and recent nvidia-smi samples per run so the list
  can show a smoothed max-favoring figure by default. Cross-project job
  discovery was explicitly left as a sketch ("i am typically only using gpu
  within a single project").
- **Reversal of the 2026-07-02 deferral:** that entry deferred machine-level
  GPU awareness. The lease store is host-scoped by user direction because a
  project-local lease cannot stop a second project from double-booking the
  device; job discovery stays project-local.
- **Exactness:** 0.5 is exact in binary, so `50%` twice was never the
  risk; base-10 shares such as `33.3333333%` and the unattributed driver
  overhead were. Amounts parse as `Fraction` from the decimal text. A
  design subtracting `memory.used` from the total would refuse the second
  `50%` whenever any overhead exists (600 MiB on the test fake; this host
  read 0 MiB idle).
- **Behavioral evidence:** `tests/test_agentctl.py` covers multi-wait
  all/any/unknown, exact admission arithmetic, a third lease queuing behind
  two `50%` leases and launching after one ends, release on `stop`, and the
  wrapper's sample history feeding `vram_max10m=` and `vram_peak=`.
  Replacing `GpuCommitment.fits` with `True` failed both lease tests. Real
  96 GB-GPU smoke (torch, systemd user-service backend): a 3 GiB allocation was
  attributed as `vram=gpu0:3.5G` with `ram=1.1G`, lease `gpu0:9.6G` from
  `10%` of 97887 MiB, `10%`+`90%` admitted exactly, `91%` waited. After the
  payload shrank to 1 GiB: `vram=gpu0:1.5G vram_max10m=gpu0:3.5G`, and the
  GPU line committed 3.5G against the 2G lease. `list --live` took 0.29 s
  end to end; `--gpu-sample 2` took 2.5 s.
- **Observed gap, fixed:** `stop` on a leased run kills the wrapper before
  its `finally` releases the lease; the dead-holder record lingered until
  the next admission. `stop` now removes the stopped run's leases.
- **Coexistence observed:** during the smoke an unrelated `VLLM::EngineCore`
  process appeared on the same GPU; outside the lease system it counts only
  as `unleased=` use, which is the advisory contract.
- **Full-suite baseline:** 171 passed, 3 failed. Two fail identically on
  clean `f23c02c` (session-id recovery under this harness's environment);
  the third, `test_start_after_marker_without_sidecar_does_not_launch_payload`,
  passes alone and is the known 0.2 s marker race
  (`gaps/agentctl-after-marker-test-race.md`).

Contributing-model: opus-5.5
