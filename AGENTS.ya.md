# Yep Anywhere Launcher Supplement

Read this after `~/agents/AGENTS.global.md`, `~/agents/AGENTS.user.md`, and the
harness supplement whenever `AGENT_LAUNCHER=yepanywhere`. Yep Anywhere (YA) is
the local supervisor that starts, resumes, and streams provider sessions. This
file owns what YA publishes into a session it launched and the behavior that
depends on YA being the launcher. Harness mechanics stay in the harness
supplement; cross-launcher policy stays in the global file.

## Launch, route, and backend markers

| Marker | Meaning |
|---|---|
| `AGENT_LAUNCHER` | `yepanywhere` |
| `AGENT_LAUNCH_HARNESS` | harness family YA launched: `claude`, `codex`, `gemini`, `grok`, `opencode`, or `pi` |
| `AGENT_LAUNCH_ROUTE` | canonical route inside the harness; `claude-gateway` when present |
| `AGENT_LAUNCH_BACKEND` | canonical explicitly identified backend; `copilot-api` when present |
| `AGENT_LAUNCH_MODEL` | model YA selected explicitly; absent when YA asked for the provider default |
| `AGENT_LAUNCH_EFFORT` | effort YA selected explicitly; absent when YA asked for the provider default |
| `YEP_CLAUDE_GATEWAY=1` | current YA fallback for `AGENT_LAUNCH_ROUTE=claude-gateway` when the canonical route marker is absent |
| `YEP_COPILOT_API=1` | current YA fallback for `AGENT_LAUNCH_BACKEND=copilot-api` when the canonical backend marker is absent; routes `AGENTS.copilot.md` |

Model and effort are launch history. A live model or effort switch leaves them
unchanged, so they answer what this session started as, never what it is
running now. Route identifies how the harness reaches a model; backend
identifies the implementation behind that route. Do not collapse those facts
into one boolean or infer them from URL, port, model, or vendor.

Current YA builds publish the two `YEP_*` compatibility outputs above rather
than their canonical replacements. Readers accept both during migration;
prefer `AGENT_LAUNCH_ROUTE` and `AGENT_LAUNCH_BACKEND` when present.

## Markers delivered through the Bash bridge

YA may publish `AGENTCTL_SESSION_ID` and session capabilities late through
`BASH_ENV`; check an ordinary Bash call, not the agent process environment.
An early absence on a fresh session is normal. Before using or diagnosing
wake/browser credentials or child-environment propagation, read the matching
sections of `topics/AGENT_ENV_VARS.md`, including YA late publication and
compatibility names. Prefer complete canonical pairs; never mix a canonical
and legacy value or log a token. Browser access also needs the separate tab
grant; wake values are YA-owned outputs, not operator inputs.

## Namespace transition

Agent-facing names use `AGENT_*`. Accept only the compatibility aliases in
`topics/AGENT_ENV_VARS.md`; do not use `YEP_*`/`YA_*` as naming precedent.
That topic owns filtering and migration details.

## The server supervising you

The YA server that launched this session also supervises every other live
session on the host, so restarting or reloading it — a restart helper, a
maintenance-port reload, killing its process tree — destroys in-flight work,
including this turn. Treat that as a user action: state `needs restart: <what>`
and continue. To exercise a server change first, start an isolated instance on
another port and profile instead.
