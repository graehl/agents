# Agentctl sketches

> Dormant candidate extensions to `agentctl`; none is current behavior until
> promoted into `agentctl.md` and implemented.

Topic: `agentctl`

## Language-aware source selection

The current `--source-scope non-doc` is intentionally repo-wide: broad enough
to be safe, but coarser than the payload's actual dependency closure. A future
extension could combine an explicit source list with a conservative
language-aware crawler rooted at the selected entry script, then record the
resolved file set in `source_snapshot` for delayed revalidation.

Do not add language values to `--source-scope`; that option names the current
`non-doc|all` path policy. A separate surface and its fallback behavior need
design only after real repo-wide false invalidations make the added crawler
worth its language/toolchain complexity.

## Host-wide job discovery and waits

GPU leases are already host-scoped (`agentctl.md` § GPU use and VRAM
leases), but job state is not. `list` and `wait` see only the invocation
project's `.agentctl/`, so a session cannot list or wait on another
project's runs on the same machine. Two shapes would close that without
moving the per-project authority:

- **Activity pointers:** each launch touches a host-level pointer
  (`~/.local/state/agentctl/projects/<hash>` naming the project root).
  `list --host` and `wait PROJECT:JOB` resolve through the pointers to the
  owning project's ordinary state files. There is no second copy that
  could disagree, and a stale pointer is just a project with no live
  runs.
- **Redundant host index:** the wrapper also mirrors a compact row per run
  into a host store. This makes discovery a single read, but the index can
  disagree with the per-project ground truth and needs its own liveness
  rule.

Prefer the pointers unless a measured host-wide listing cost argues for
the index. Lease records already carry `project_root`/`job`/`run_id`, so
`list` could name a foreign leaseholder today. Defer until the user
routinely runs GPU work from more than one project at once; as of
2026-10-02 they typically use the GPU from a single project.

## GPU lease queue order

Lease admission has no order: any waiter whose amount fits is admitted,
so a large request can starve behind a stream of smaller ones. Strict
FIFO fixes starvation but idles capacity that a small job could use
(no backfill). A middle form admits a later waiter only when the oldest
blocked waiter could not fit even with that waiter absent. Waiters would
publish a pending record (spec, `queued_at`, live holder) beside the
leases. Build it when starvation is observed, not before.

## Machine-scoped activity on foreign workers

Local `.agentctl/active/` cannot expose a session operating in another clone
or on an AWS worker. A future fleet plugin could preserve the existing local
contract instead of inventing a distributed lock: run the ordinary active
registry on each foreign machine, qualify every observation by a stable machine
identity, and query those registries over the same SSH boundary used by
`fleet-watch`.

The final useful claim is the remote host plus the items held there. A row
would contain the machine identity (cloud provider/region/instance id when
available), harness/session id, local status and age, remote project root,
claimed remote paths, and explicitly claimed machine resources such as GPU ids
or named jobs. Before the item vocabulary exists, an optional exploratory stage
could claim `remote-host:<machine>:*` and measure whether whole-host awareness
catches real misses without creating mostly false conflicts. Keep it only if
that probe supplies value, and label it visibly as whole-host scope rather than
fine-grained coordination.

The foreign machine computes freshness against its own clock and returns that
result; the caller must not compare raw mtimes across hosts. Unreachable means
`unknown`, never `alone`. Credentials and SSH arguments remain caller input
and are not copied into the activity record.

A machine-local registry is sufficient for a first implementation boundary;
the final claim still combines that host with its held paths/resources. This
can detect two sessions using the same worker, filesystem, GPU, or job namespace
without requiring a global AWS registry, cross-host consensus, or automatic
fencing. A fleet view may aggregate rows for awareness, but each machine-local
registry remains the authority for that machine. Logical advisors can retain a
later semantic notice of a missed false start; that is useful continuity
evidence, not live resource ownership.
