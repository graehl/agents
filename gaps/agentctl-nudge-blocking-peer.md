---
slug: agentctl-nudge-blocking-peer
noticed: 2026-09-02
where: agentctl.py (`alone`, active-entry header), scripts/session-turn
---

**Gap:** `agentctl alone` waits for solitude and nothing more. A session
blocked on a peer's wildcard `scope:` has no agentctl way to tell that
peer someone is queued and for what. The active-entry header does not
declare a harness, while `session-turn` needs
`<harness> <provider-session-id>`. Claude Code
sessions now have an instructed hand nudge over the harness's native
session messaging (`AGENTS.claude.md § Peer coordination over native
session messaging`), which a script cannot call and Codex lacks, so the
coordination contract has a same-harness-only path and no
harness-agnostic one.

**Noticed while:** siting that Claude preference after observing two
YA-launched gateway sessions negotiate a scope carve unprompted over
`ListAgents`/`SendMessage`.

**Fix sketch:** a `nudge <peer-id>` verb, invoked at most once per wait
by `alone --nudge-after <seconds>`, sending over `session-turn` a body
whose first line names the sending session, its claimed paths, and the
wait. The peer decides; a nudge never carves or drops a claim. Three
prerequisites:

- A `harness:` header line in `active/` entries, written from
  `AGENT_LAUNCH_HARNESS` at registration, so an entry is addressable.
- A `session-turn --no-resume` mode. The client forces `resumeIfAbsent`
  on under host protocol 3 (`scripts/session-turn`, request assembly),
  and a nudge must not revive an expired session. Whether the YA host
  honors the flag set false is unverified. A refused send on an absent
  worker then doubles as the liveness check.
- A self-identifying body, because `session-turn` delivers raw text as
  an ordinary user turn with no wrapper; without the first line the
  receiver reads the nudge as its user.

**Blocked until** (user-directed, 2026-09-02): the user is certain the
YA provider host can deliver a turn atomically as send-to-live-session
or fail `not alive`. Only the provider-mediated path qualifies: an
ordinary native resume-and-send forks the YA session, so a nudge that
falls back to native resume is worse than no nudge. `session-turn`'s
native fallback therefore has to be off for this verb, not merely the
absent-session resume.

## Peer-written notices and busy recipients

User-directed question, 2026-09-07. Contributing-model: 6-Astra.

The user requested checking whether peers may leave coordination comments
in another session's active record, with at least Linux-safe atomic delivery,
possibly through an `agentctl` verb. This also needs a delivery path when the
recipient is in foreground activity rather than idle.

Current evidence:

- `topics/agentctl.md` permits free content below the header and says brief
  readers stop at that header. It does not define peer-writable notice fields,
  sender identity, required notice reads, acknowledgment, or delivery semantics.
  `claim:`/`carve:` notes are written in the caller's own entry, not a mailbox.
- `agentctl.py`'s `write_active_entry` and `clear`'s `write_own` preserve the
  body by reading it, then writing a fixed `<session-id>.tmp` and replacing the
  destination. These paths have no interprocess lock around the read/modify/
  replace operation. Atomic rename alone does not prevent a concurrent owner
  update from losing a peer's appended notice; concurrent writers also share
  the temporary filename. The existing header/body preservation test is
  sequential, not evidence of safe concurrent delivery.
- During YA workflow file release, two `session-turn send codex` attempts
  against the live recipient returned `outcome: busy`, `accepted: false`,
  `Provider session is not idle`, and exit 11. The observed provider-host path
  did not queue the notice. This establishes rejection of these submissions,
  not that all harness delivery paths reject busy recipients.

Resolve the design before recommending hand-written peer comments:

- Define whether notices belong inside the active record or in a separate
  inbox. If sharing the record, every cooperating owner/peer writer must use
  one Linux-safe locking protocol covering the whole update and temporary-file
  lifecycle. A separate inbox may avoid replacing owner-controlled state.
  State behavior for readers, crashes, and unsupported platforms explicitly.
- Define sender/recipient and notice identity, acknowledgment/removal, retry
  deduplication, and the observation point where a busy recipient reads pending
  notices. Distinguish persisted/queued, delivered, and acted-on; writing a
  comment does not wake a model or prove it was read.
- Do not let a peer notice refresh the recipient's apparent liveness, revive a
  DONE/stale session, replace its banner/scope, or release its claims. Preserve
  notices across legitimate owner updates and settle archive/sweep behavior.
- Decide whether busy `session-turn` delivery should durably queue instead,
  with explicit acceptance/receipt semantics, or whether an agentctl notice
  complements its existing live-session delivery. Keep the no-native-fallback
  and no-implicit-resume constraints above for automated nudges.

Closure needs concurrent owner-update/peer-write tests (including two senders),
crash/retry and duplicate-delivery cases, no false liveness refresh, and a busy
recipient eventually observing a notice without a competing native resume.
This entry records the question and observed gap; it does not authorize a
coordination implementation or another session's task execution.
