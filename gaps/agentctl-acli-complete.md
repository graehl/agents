---
slug: agentctl-acli-complete
noticed: 2026-07-26
where: agentctl.py build_parser / parse_start_command
---

**Gap:** agentctl, the flagship ACLI consumer, does not wire
`maybe_complete` (or `maybe_repl`), so it offers no `--acli-complete`
protocol despite building its parsers with `acli_args.ArgumentParser`.
Both constructions now pass `capabilities=()` so `--help` does not
falsely advertise `complete`; the capability line contract is
"advertise only what is wired" (`topics/agent-cli.md`).

**Noticed while:** adding the capability line / help footer to
`acli.args` for the almanac testbed — the new default `("complete",)`
would have made agentctl's help lie.

**Fix sketch:** call `acli_args.maybe_complete(parser)` (and optionally
`maybe_repl`) in agentctl's main before parsing and before any side
effect; verbs, flags, and `choices` complete for free. Then restore the
default capabilities and add `exit_codes` for the help footer. Check
the dynamically built `parse_start_command` parsers and plugin
`register_args` hooks stay side-effect-free under a completion probe.
