---
slug: agentctl-stop-from-inside-run
noticed: 2026-11-10
where: agentctl.py terminate_state, stop and restart
---

**Gap:** `agentctl stop <job>` or `restart <job>` issued by a process of the
run it names is killed by its own signal before it records anything. The run
stays recorded `running`, its GPU leases are not released, and `restart`
never relaunches. It completes only when the caller has left the run's
process group and the run is not a systemd service unit; in the other three
arrangements (same group, or a service unit with the caller inside or
outside the group) the signal reaches the caller. Reproduced by a strict
review on throwaway jobs; the behaviour predates the review.

**Noticed while:** the automatic strict review of
`1b63f83accc8..50a69f1ad81d`.

**Fix sketch:** when the caller belongs to the run, record `stopped` and
release the leases before delivering the signal, or hand the stop to a
process outside the run (`systemd-run --user --scope`, or a detached child
that has left the group) and wait for nothing. Test each of the four
arrangements.
