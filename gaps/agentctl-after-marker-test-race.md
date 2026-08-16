---
slug: agentctl-after-marker-test-race
noticed: 2026-08-16
where: tests/test_agentctl.py test_start_after_marker_without_sidecar_does_not_launch_payload
---

**Gap:** the test writes an external `.running.md` marker, arms a helper that
deletes it after 0.2 s, then launches `agentctl start --after <artifact>`. On a
host where the launcher needs longer than 0.2 s to reach dependency resolution
(bash wrapper plus interpreter start), the marker is already gone, so `start`
exits 1 with "--after target not found" and the assertion about the payload not
running never gets exercised. It fails reproducibly here at pristine `HEAD`,
independent of any working-tree change, so the suite carries one standing red
that hides a real regression in the same area.

**Noticed while:** running the suite to validate the cross-repo environment pin
in the tracked-run admission guard.

**Fix sketch:** make the marker's disappearance follow the launch instead of
racing it — hold the marker until `start` has recorded the job as `waiting`
(poll the state file, or have the helper wait on a file the launcher writes),
then delete it. Raising the sleep only moves the race to a slower host.
