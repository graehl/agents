---
slug: agentctl-run-id-experiment-collision
noticed: 2026-10-05
where: agentctl.py run_id / start (collision suffix loop); aim plugin dump path
---

**Gap:** `run_id()` has one-second resolution. `start` suffixes a colliding id
only when `.agentctl/runs/<job>/<run-id>` already exists, so collisions within
one job are prevented. The canonical record is per experiment, however:
`runs/aim/<experiment>/runs/<run-id>.json`. Two different jobs started in the
same second under one experiment get the same id. The later launch overwrites
the earlier job's dump, and both share the md5-derived `aim_run_hash`.
`topics/agentctl.md` § plugin metadata asserts run ids are unique, which this
falsifies. Per-job `state.json` survives, so the loss is the canonical record,
not all provenance.

**Noticed while:** queueing five-stage ASR evaluation chains with
`--launch-wait 0` in the draft repo. Stages queued back to back shared ids, for
example `ar-catchup-off-calibrate-v1` and `ar-catchup-off-dev-v1` both received
`20261005T192456Z` under `speech-recognition/ar/incumbent-ablations`.
Workaround: pass a distinct `--run-id` per stage.

**Fix sketch:** allocate ids so they are unique across every record namespace
the launch will write: suffix while either the job run dir or the experiment's
dump path exists, and reserve the dump path atomically (exclusive create) so
two concurrent launches cannot both pass the check. Add a test that starts two
jobs in one experiment within one second and asserts distinct ids, dumps and
`aim_run_hash` values.
