# Yep Anywhere Launcher Supplement

Read this after `~/agents/AGENTS.global.md`, `~/agents/AGENTS.user.md`, and the
harness supplement whenever `AGENT_LAUNCHER=yepanywhere`. Yep Anywhere (YA) is
the local supervisor that starts, resumes, and streams provider sessions. This
file owns what YA publishes into a session it launched and the behavior that
depends on YA being the launcher. Harness mechanics stay in the harness
supplement; cross-launcher policy stays in the global file.

## Markers present at launch

| Marker | Meaning |
|---|---|
| `AGENT_LAUNCHER` | `yepanywhere` |
| `AGENT_LAUNCH_HARNESS` | harness family YA launched: `claude`, `codex`, `gemini`, `grok`, `opencode`, or `pi` |
| `AGENT_LAUNCH_MODEL` | the model YA selected explicitly; absent when YA asked for the provider default |
| `AGENT_LAUNCH_EFFORT` | the effort YA selected explicitly; absent when YA asked for the provider default |
| `YEP_COPILOT_API` | `1` only when a Claude Gateway launch reached an Anthropic-compatible Copilot backend; routes `AGENTS.copilot.md` |

Model and effort are launch history. A live model or effort switch leaves them
unchanged, so they answer what this session started as, never what it is
running now.

## Markers delivered through the Bash bridge

These arrive once YA knows the canonical session id, through the `BASH_ENV`
file rather than the agent process environment. They appear in ordinary Bash
calls and are absent from the agent process's own `/proc/self/environ`; an
early absence on a new session is normal, and a resume can carry the id from
the start.

| Marker | Meaning |
|---|---|
| `AGENTCTL_SESSION_ID` | canonical YA session id — the resumable id to register and to pass to `agentctl` |
| `YEP_SESSION_WAKE_URL`, `YEP_SESSION_WAKE_TOKEN` | this session's wake capability; YA-owned outputs, never operator inputs. Never log the token |
| `YEP_BROWSER_DEBUG_AGENT_URL`, `YEP_BROWSER_DEBUG_CALLER_TOKEN` | short-lived browser-diagnostic broker credentials, useful only with a separately pasted tab grant. Never log the token |

## Why the agent-facing names carry no product prefix

YA strips inherited `YEP_*` and `YA_*` from the environment it hands a provider
child on purpose: its own configuration is not the agent's, and a leaked value
changes tooling behavior inside the project. Anything meant for the agent
therefore lives in the unprefixed `AGENT_` namespace, or is published
explicitly by name after that filter.

Do not restore a product prefix on an agent-facing marker. `YEP_AGENT_HARNESS`,
`YEP_AGENT_INITIAL_MODEL`, and `YEP_AGENT_INITIAL_EFFORT` were set on the
provider worker but filtered back out one process later, so no Claude session
ever saw them between their introduction and 2026-08-17.

## The server supervising you

The YA server that launched this session also supervises every other live
session on the host, so restarting or reloading it — a restart helper, a
maintenance-port reload, killing its process tree — destroys in-flight work,
including this turn. Treat that as a user action: state `needs restart: <what>`
and continue. To exercise a server change first, start an isolated instance on
another port and profile instead.
