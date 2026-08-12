# Agentctl sketches

> Dormant candidate extensions to `agentctl`; none is current behavior until
> promoted into `agentctl.md` and implemented.

Topic: `agentctl`

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
