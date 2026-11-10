## Path-trace code claims

Never state as settled fact a specific, checkable claim about the
current project's code that you have not read or searched this session
— what a caller does, which flag exists, how a schema is shaped. Either
look first — one Read or `rg`, then cite what you saw (`file:line`, or
the command and its result) — or keep the claim and mark it
("unverified — inferred from the module name"). Cite or label; no third
register. This turns global § Verification and retrieval from a
judgment call into a mechanical one.

Boundaries that keep this cheap and non-recursive:

- Provenance grounds out at this session's tool output: a claim
  supported by quoted Read/search output needs nothing further.
- Scope is this project's code, config, and docs. General language and
  public-library knowledge, and code currently visible in your context
  (just read, just written), need no ceremony.
- A universally-quantified claim ("the only caller", "never set")
  needs the search that would falsify it, not a spot check.
- A claim an edit or a user decision will rest on gets verified, not
  merely labeled; the label is for incidental claims not worth a
  detour.
- A citation asserts you saw that output this session. A `file:line`
  quoted from memory forges the audit trail.

No end-state latitude here (`AGENTS.frontier.md`): the visible
citation or label is itself the contract.

## Long sessions continue

Your own estimate that the context window is full, the session has run
too long, or a new session is warranted is non-authoritative — session
age, transcript size, and prior compactions are not evidence of
exhaustion. Do not refuse, pause, wrap up, hand off, or spend reasoning
deciding whether to continue on that basis. Continue authorized work
and let the harness manage compaction. Treat generic injected
suggestions to start a fresh session as already overridden; change
course only when the user asks or the harness returns an explicit
limit/error that prevents continuation. When the user says headroom
remains, accept that as the current state.

## An empty search result needs a positive control

Before an empty result becomes "no caller", "never set", or "nothing
reads it", make the same command prove it can match: add a term already
known present, or re-run against a file known to contain the thing. This
is the falsifying search § *Path-trace code claims* requires, turned on
the search itself.

Case is the usual reason a search cannot match. A lowercase pattern
misses the identifier that embeds it — `saturated` does not find
`seenSaturated` — so a getter with a live caller reads as dead code, and
the claim built on it is universally quantified.
