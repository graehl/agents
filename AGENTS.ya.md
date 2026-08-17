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

YA normally delivers these once it knows the canonical session id, through the
`BASH_ENV` file rather than the agent process environment. They appear in
ordinary Bash calls and are absent from the agent process's own
`/proc/self/environ`; an early absence on a new session is normal, and a resume
can carry the id from the start. Current builds publish `AGENTCTL_SESSION_ID`
plus the two legacy `YEP_*` pairs. The canonical pair rows are reader contracts
for the pending publisher migration, not claims that current YA publishes them.

| Marker | Publication / meaning |
|---|---|
| `AGENTCTL_SESSION_ID` | current canonical YA session id — the resumable id to register and to pass to `agentctl` |
| `AGENT_SESSION_WAKE_URL`, `AGENT_SESSION_WAKE_TOKEN` | canonical wake target; prefer the complete pair when published; never log the token |
| `YEP_SESSION_WAKE_URL`, `YEP_SESSION_WAKE_TOKEN` | current YA compatibility outputs for the canonical wake pair |
| `AGENT_BROWSER_DEBUG_BROKER_URL`, `AGENT_BROWSER_DEBUG_CALLER_TOKEN` | canonical browser-debug target; prefer the complete pair when published; never log the token |
| `YEP_BROWSER_DEBUG_AGENT_URL`, `YEP_BROWSER_DEBUG_CALLER_TOKEN` | current YA compatibility outputs for the canonical browser-debug pair |

The wake values are YA-owned outputs, never operator inputs. Browser-debug
credentials are useful only with a separately pasted tab grant. A complete
canonical pair wins; do not combine one canonical value with one legacy value.

## Namespace transition

YA strips inherited `YEP_*` and `YA_*` from the environment it hands a provider
child on purpose: its own configuration is not the agent's, and a leaked value
changes tooling behavior inside the project. Canonical agent-facing values use
`AGENT_*`. Current product-prefixed session outputs survive only because YA
explicitly injects or allowlists them; they remain compatibility aliases while
`~/ya/gaps/agent-facing-env-markers.md` tracks the publisher migration.

Do not use those aliases as naming precedent. `YEP_AGENT_HARNESS`,
`YEP_AGENT_INITIAL_MODEL`, and `YEP_AGENT_INITIAL_EFFORT` were set on the
provider worker but filtered back out one process later, so no Claude session
ever saw them between their introduction and 2026-08-17. The complete variable
inventory and child-boundary behavior is in `topics/AGENT_ENV_VARS.md`.

## The server supervising you

The YA server that launched this session also supervises every other live
session on the host, so restarting or reloading it — a restart helper, a
maintenance-port reload, killing its process tree — destroys in-flight work,
including this turn. Treat that as a user action: state `needs restart: <what>`
and continue. To exercise a server change first, start an isolated instance on
another port and profile instead.
