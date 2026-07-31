# Backward compatibility

> Observable compatibility breaks and shims are recorded here so future
> changes can check whether a surface has already made a contract decision.

Topic: `backward-compat`

## Decisions

- 2026-07-05 `agentctl` active-session stdout — changed `active`,
  `others`, `tending`, and `alone` default non-TTY/agent output from prose to
  ACLI JSONL; agent-first output is the contract from `topics/agent-cli.md`.
  Exit codes and `.agentctl/active` side effects stay compatible; `--pretty`
  gives indented JSON rather than restoring the old prose, because a text shim
  would keep the unstructured output path alive.
- 2026-07-31 research-program discovery — a program root now needs a
  `Research program:` line in its `research/<program>/GLOSSARY.md`; bare
  presence of that file no longer declares one. Breaks any program glossary
  written under the 2026-07-30 rule, which falls back to the project-wide
  advisor until the line is added; no shim, because detection-by-presence
  collides with `topics/glossary.md` telling every subtree to create a
  `GLOSSARY.md` as soon as local jargon recurs — the two rules cannot both
  hold, and a one-day-old convention is cheaper to migrate than to alias.
