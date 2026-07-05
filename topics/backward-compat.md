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
