---
slug: session-turn-eventual-send
noticed: 2026-09-02
where: scripts/session-turn, YA provider-host sessionTurn admission
---

**Gap:** `session-turn send` cannot opt into queuing a turn for a busy
recipient. During YA workflow file release, two sends to a live Codex
recipient returned `outcome: busy`, `accepted: false`, `Provider session is
not idle`, and exit 11. That establishes rejection on the observed host path,
not a universal limitation of every harness transport.

**Agreed direction** (user-directed, 2026-09-07): add an option on `send`
for **eventual send**; flag spelling remains open. Preserve immediate busy
rejection without the option. Opted-in callers must learn whether the turn
was queued or started. Queueing a follow-up does not steer the running turn.
Define durable acceptance, later execution/terminal receipt, retries and
deduplication, plus behavior when the recipient dies before starting it.

**Safety prerequisite for automated peer nudges** (user-directed,
2026-09-02): the user must be certain that the YA provider host atomically
accepts for the existing live session or refuses `not alive`. Never use a
native resume-and-send fallback: it can fork the YA session. Absent-worker
resume must also be disabled for this use. Current client protocol-3 assembly
adds launch/recovery information; verify the host's live-only behavior and
expose it explicitly rather than treating a pre-send liveness check as atomic.
These restrictions govern automated nudges, not a blanket change to all
existing `session-turn` callers.

If automatic agentctl-to-session delivery is later added, resolve the target
harness/provider ID explicitly and mark the body as peer input. An ordinary
user-turn transport supplies no peer wrapper or authorization boundary by
itself. A notice never carves, releases a claim, or authorizes another task.

The former mixed gap was `gaps/agentctl-nudge-blocking-peer.md`. Its independent
claim-wait dialogue portion is implemented in `agentctl_coordination.py` and
documented in [agentctl](../topics/agentctl.md#claim-clearance-dialogue): default
waiting with flushed notices, `--no-wait`, `--deaf`, pause/resume/cancel, and
whole-wait archival without acknowledgments. That mechanism neither calls
`session-turn` nor depends on eventual send. This gap retains only the transport
work; its presence does not authorize implementation.

Contributing-model: 6-Astra
