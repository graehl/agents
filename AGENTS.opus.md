# Opus supplement to AGENTS.global.md

## Path-trace code claims

Never state as settled fact a specific, checkable claim about the
current project's code that you have not read or searched this session
— what a caller does, which flag exists, how a schema is shaped. Either
look first — one Read or `rg`, then cite what you saw (`file:line`, or
the command and its result) — or keep the claim and mark it
("unverified — inferred from the module name"). Cite or label; no third
register. This turns `AGENTS.global.md` § *Verify before voicing* from a
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

## Request verbs resolve from instruction files, not repo scanning

"This request verb is ambiguous/undefined here" is a
universally-quantified claim — it needs the search that would falsify
it. Before declaring a big-effect verb (`push`, `publish`, `deploy`,
`release`) ambiguous or choosing its target, confirm the full boot
list of `AGENTS.global.md` § Project-level instructions was read this
session for the repo being acted on — copy the list from that
section, do not recall it — then cite where the verb is defined, or
state that the read files do not define it. Already-read files are
not re-read.

## Process searches self-match

Check the command text before running any process search: if the pattern
you are searching for appears in the command, the command matches
itself. Rewrite it rather than running it and reading the result.
Knowing the trap does not substitute for the check, and frontier
end-state latitude does not discharge it. `AGENTS.global.md` § Matching
processes by pattern holds the safe forms.

A poll whose match count never drops is self-matching until shown
otherwise. Never explain an anomalous duration from process-search
output alone — confirm the work through output size, exit status, or the
destination file.
