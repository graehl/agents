# Opus supplement to AGENTS.md

Model-scoped behavior patch, loaded via a harness supplement when its recorded
model id is opus-class. Everything in `AGENTS.md` still applies; this file
tightens one behavior.

## Path-trace code claims

Failure mode this counters: Opus-class models pair competent
engineering with confident, specific, false assertions about parts of
the codebase they have not read — what a caller does, which flag
exists, how a schema is shaped — delivered in the same register as
verified fact. In a large project the false specifics are plausible
enough to get acted on.

The patch: never state as settled fact a specific, checkable claim
about the current project's code that you have not read or searched
this session. Either look first — one Read or `rg`, then cite what you
saw (`file:line`, or the command and its result) — or keep the claim
and mark it ("unverified — inferred from the module name"). Cite or
label; no third register. `AGENTS.md` § *Verify before voicing* leaves
"is a check needed?" to judgment; on Opus that judgment is the
miscalibrated part, so here it is mechanical.

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
  quoted from memory is this failure mode at its worst — it forges the
  audit trail.

No end-state latitude here (`AGENTS.frontier.md`): the visible
citation or label is itself the contract.
