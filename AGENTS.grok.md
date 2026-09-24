## Session Identity

Primary mechanism: the launcher-injected `$AGENTCTL_SESSION_ID`. It is
harness-agnostic — a launcher such as yepanywhere (YA) exports it per
command through a `BASH_ENV` bridge that the `agentctl` bash wrapper
sources regardless of provider — so it works for Grok with no
Grok-specific discovery snippet. Check an ordinary Bash call, not only
the agent process environment. If it is set, use it verbatim as the
session id for `.agentctl/active/<session-id>` and skip any further
lookup; `agentctl` adopts the same var first, so its `active/` entry and
yours name the same file.

YA uses Grok's native session id (UUIDv7 directory name under
`~/.grok/sessions/`) as the canonical YA session id, so the env var
matches the transcript directory when YA launched this session.

When `AGENT_LAUNCHER=yepanywhere`, do not search transcripts for a
substitute. If `$AGENTCTL_SESSION_ID` is still unset after a Bash check
in an already-running session, report a YA host publication defect.

If no launcher is present (hand-launched Grok) and the var is unset,
recover the id only from provider/process evidence tied to this live session.
The newest directory under `~/.grok/sessions/<urlencoded-cwd>/` is a discovery
candidate, not proof of identity. Report unresolved identity rather than
inventing a tag or registering another session's id.

## Session Logs

Grok stores each session at
`~/.grok/sessions/<urlencoded-cwd>/<session-id>/` (`GROK_HOME` overrides
`~/.grok`). `updates.jsonl` is the conversation log. When
`AGENTS.global.md` says to search provider session logs, search there,
excluding your own `$AGENTCTL_SESSION_ID` directory. A YA-launched
session still must not use that search to recover its own id.
