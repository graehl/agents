---
slug: agentctl-nudge-blocking-peer
noticed: 2026-09-02
where: agentctl.py (`alone`, active-entry header), scripts/session-turn
---

**Gap:** `agentctl alone` waits for solitude and nothing more. A session
blocked on a peer's wildcard `scope:` has no agentctl way to tell that
peer someone is queued and for what; a peer cannot even be addressed,
because an `active/` entry holds only the gist and `scope:` while
`session-turn` needs `<harness> <provider-session-id>`. Claude Code
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
