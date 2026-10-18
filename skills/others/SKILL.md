---
name: others
disable-model-invocation: true
description: Show what other agents are doing in this project — own .agentctl/active status (or that the agent is lurking), peers currently active, recently DONE work, and stale entries that may be orphaned. Use when the user invokes /others, asks "who else is here", "what other agents are running", or similar.
---

# /others — see what other agents are doing here

Report this Git project's self entry, active peers, stale entries, work DONE in
the last day, and sessions awaiting whole-project solitude.

Resolve the Git root with `git rev-parse --show-toplevel`; outside a Git
project, say so and stop. From that root run:

```bash
agentctl active --minutes 0 --done
```

This read-only command includes swept archives and awaiting entries. It
resolves identity itself: use `self: true` / `[yours]`, without searching logs
or exposing an unmasked id. No self row means lurking; do not register merely
to report. If identity is unresolved, report that uncertainty.

Group the returned rows:

- Self: the row marked `self`, if any.
- Active peers: non-self, non-DONE, younger than 70 minutes.
- Stale: non-self, non-DONE, at least 70 minutes old. Age is not proof of death.
- DONE in the last 24 hours: status starts with `DONE`, age under 24 hours.
- Awaiting: rows from `awaiting`, younger than 70 minutes; these do not block.

Number rows for follow-up references. Show id, age, status, and any scope or
tending declaration. Show empty groups as none. Summarize large histories
rather than dumping them; inspect an individual entry only when its details
matter to the user's question.

For coordination or unavailable-helper fallback, read
`~/agents/topics/agentctl.md` § Other coordination uses and § Active-sessions
file schema. This reporting skill does not sweep, retire, or take over claims.
