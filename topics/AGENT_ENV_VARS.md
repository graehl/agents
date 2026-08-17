# Agent environment variables

> The launcher, harness, session, agentctl, and guard environment variables
> understood by `~/agents`, including their effects and transfer across child
> process boundaries.

Topic: `AGENT_ENV_VARS`

## Scope and notation

This is the canonical inventory for purpose-built environment variables that
`~/agents` publishes, reads, routes on, or deliberately removes. It also records
YA compatibility outputs whose names affect those contracts. It is not an
inventory of every operating-system, provider, model, or YA configuration
variable. YA's operator inputs remain cataloged in its
`topics/ya-env-vars.md`; provider-specific tuning remains in the provider's own
documentation.

The child-boundary columns use these terms:

- **inherit** — copied unchanged from the invoking environment;
- **set** — supplied when the corresponding option or facility is active;
- **replace** — the boundary supplies its own value even when one was inherited;
- **increment** — parsed as an integer, with invalid input treated as zero, then
  increased by one; and
- **remove** — absent from the child even when the caller had it.

`agentctl start` and `smoke` do not have a general environment denylist. They
start from the complete ambient environment, fill missing keys from
`agentctl.env`, set their run context, apply `--source-env`, apply explicit
`--env KEY=VALUE`, and finally run plugin `on_start` hooks. A source script can
add or replace values but, under the current overlay implementation, cannot
remove a value inherited before it. The detached `_run-child` wrapper and its
payload receive the same resulting environment. Consequently **inherit** also
means “available to the payload”; it does not mean that agentctl persists the
value in run state. Project-env metadata records key names, never values.

## Agent, launcher, and session contract

| Variable | Publisher / effect | Sensitive | `agentctl` launched command | `session-turn` native child | Status |
|---|---|---:|---|---|---|
| `AGENT_LAUNCHER` | Launcher identity; `yepanywhere` routes `AGENTS.ya.md`. | no | inherit | remove | canonical |
| `AGENT_LAUNCH_HARNESS` | Harness family selected at launch. | no | inherit | replace with target harness | canonical |
| `AGENT_LAUNCH_MODEL` | Explicit model selected at initial launch; not current-model state after a switch. | no | inherit | remove | canonical |
| `AGENT_LAUNCH_EFFORT` | Explicit effort selected at initial launch; not current-effort state after a switch. | no | inherit | remove | canonical |
| `AGENT_LAUNCH_ROUTE` | Route inside the harness, currently `claude-gateway`; distinguishes transport from harness and backend. | no | inherit | remove | canonical reader contract; YA publisher migration pending |
| `AGENT_LAUNCH_BACKEND` | Explicit backend implementation, currently `copilot-api`; routes backend-specific instructions without inferring from URL, port, vendor, or model. | no | inherit | remove | canonical reader contract; YA publisher migration pending |
| `AGENTCTL_SESSION_ID` | Canonical durable harness/session id used by active-session coordination and helper defaults. YA may publish it through its Bash bridge. | no | inherit; `AGENTCTL_LAUNCH_DEPTH>0` prevents the job from acting as that agent | replace with target YA id, else target provider id | established consumer-owned name |
| `AGENT_SESSION_WAKE_URL` | Opaque session-specific POST endpoint used by the agentctl completion-wake plugin. | capability endpoint | inherit into wrapper and payload | remove | canonical reader contract; YA publisher migration pending |
| `AGENT_SESSION_WAKE_TOKEN` | Bearer credential authorizing a wake turn for one session. Never log or persist it. | **yes** | inherit into wrapper and payload; completion plugin reads it | remove | canonical reader contract; YA publisher migration pending |
| `AGENT_BROWSER_DEBUG_BROKER_URL` | Endpoint for the explicitly granted remote-browser diagnostics broker. | no; may carry a public TLS trust anchor | inherit into wrapper and payload | remove | proposed canonical name; YA migration pending |
| `AGENT_BROWSER_DEBUG_CALLER_TOKEN` | Provider-host-boot caller factor used together with a separately pasted per-tab grant. Never log or persist it. | **yes** | inherit into wrapper and payload | remove | proposed canonical name; YA migration pending |
| `AGENT_GUARD` | Nonempty means the PATH-level Git discard guard is active; also makes ACLI output compact by default. | no | inherit | inherit | canonical guard marker |
| `AGENT_GUARD_REAL_GIT` | Absolute real-Git path used by the guard shim. | no | inherit | inherit | guard implementation detail |
| `AGENT_GUARD_SHIMDIR` | Optional location where `agent-guarded` creates its Git shim. | no | inherit | inherit | guard launcher input |

The route and backend values are intentionally enumerated strings rather than
one boolean per product. `AGENT_LAUNCH_HARNESS=claude`,
`AGENT_LAUNCH_ROUTE=claude-gateway`, and
`AGENT_LAUNCH_BACKEND=copilot-api` describe three different facts. The more
specific names avoid an ambiguous `AGENT_SESSION_ID` collision with
provider-native, broker, or tool-owned session identifiers.

## Harness-native markers recognized here

These names are owned by their harnesses, not by `~/agents`. They are listed
because ACLI detection, active-session fallback, instruction routing, or fresh
native-child cleanup depends on them.

| Variable | Effect in `~/agents` | `agentctl` launched command | `session-turn` native child |
|---|---|---|---|
| `CLAUDE_CODE_SESSION_ID` | Fallback active-session id and queued-anchor transcript id; also identifies an agent caller to ACLI. | inherit; ignored for active registration at launch depth > 0 | remove |
| `CLAUDECODE` | Claude Code presence/nesting marker; identifies an agent caller to ACLI. | inherit | remove |
| `CLAUDE_CODE_*` | Any nonempty member identifies an agent caller to ACLI; individual provider knobs otherwise retain their provider-defined meaning. | inherit unless another launch layer replaces it | inherit except the exact session-id name above |
| `CODEX_THREAD_ID` | Codex thread presence identifies an agent caller to ACLI; it is not treated as the canonical active-session id. | inherit | remove |
| `PI_CODING_AGENT` | Pi's boolean agent marker; identifies an agent caller to ACLI. | inherit | remove |
| `COPILOT_CLI` | `1` routes the native GitHub Copilot CLI supplement. | inherit | remove |
| `CI` | Nonempty selects compact ACLI output as a defensive convention. | inherit | inherit |

## agentctl inputs and child run context

| Variable | Effect | `agentctl` launched command |
|---|---|---|
| `AGENTCTL_ROOT` | Selects the invocation project. The shell wrapper resolves it (or the current directory) and exports the absolute project root. | replace with resolved project root |
| `AGENTCTL_PYTHON` | Optional explicit Python ≥3.10 interpreter for the wrapper. | inherit unchanged after interpreter selection |
| `AGENTCTL_NO_PROC_SESSION_ID` | Nonempty disables fallback recovery of a resume id from ancestor process arguments. | inherit; launch depth independently suppresses job registration |
| `AGENTCTL_LAUNCH_DEPTH` | Distinguishes an agent from a job or nested job for active-session upkeep and wake arming. | increment |
| `AGENTCTL_JOB` | Slugged job name for the current run and provenance helpers. | replace, then overridable by `--source-env` / `--env` |
| `AGENTCTL_RUN_ID` | Unique current run id used by provenance helpers. | replace, then overridable by `--source-env` / `--env` |
| `AGENTCTL_RUN_DIR` | Absolute current run-state directory; cooperative declarations write `propagate.json` here. | replace, then overridable by `--source-env` / `--env` |
| `AGENTCTL_MODE` | Launch verb mode (`start` or `smoke`). | replace, then overridable by `--source-env` / `--env` |
| `AGENTCTL_HEADLINE_FILE` | Path where the payload may publish its current run headline. | replace, then overridable by `--source-env` / `--env` |
| `AGENTCTL_PARENT_RUN_ID` | On entry, identifies an enclosing run for the recorded `parent_run`; the child receives the current run id so a nested launch links back to it. | replace with current run id, then overridable by `--source-env` / `--env` |
| `AGENTCTL_OUTPUT` | Primary declared output path exposed to the payload. | set when a primary output exists; otherwise an ambient value is currently inherited |
| `AGENTCTL_INPUT_FILE` | Resolved path supplied by `--input-file`. | set with that option; otherwise an ambient value is currently inherited |
| `AGENTCTL_STEP_ID` | Optional external provenance step identifier read by `artifact_meta.py`; agentctl does not assign it. | inherit |
| `AGENTCTL_AIM_READ_ROOTS` | Path-separator list of additional read-only Aim dump roots used during provenance migration. | inherit |
| `AIM_EXPERIMENT` | Aim experiment selected by the tracking plugin. | plugin replaces for tracked runs; inherited for `--no-aim` |
| `AIM_RUN_NAME` | `<job>/<run-id>` name supplied to payloads that write a live Aim run. | plugin replaces for tracked runs; inherited for `--no-aim` |
| `CUDA_VISIBLE_DEVICES` | GPU visibility supplied by `--gpus`. | replace with `--gpus` value; otherwise inherit |
| `PYTHONUNBUFFERED` | Makes payload logs promptly observable. | default to `1` only when absent; later sources/explicit env may replace |
| `PYTHONPATH` | The shell wrapper makes the shared agentctl Python modules importable to payloads. | append the `~/agents` code root when absent from the path |
| `MPLCONFIGDIR` | Avoids an unwritable/noisy Matplotlib cache under restricted launches. | default to `<project>/.agentctl/mplconfig` when unset and creatable |
| `BASH_ENV` | Non-interactive Bash startup file. YA uses it for late session publication. | inherit and therefore source in Bash payloads | 

agentctl deliberately leaves harness/session markers intact and relies on
`AGENTCTL_LAUNCH_DEPTH`, rather than masking the ambient identity, to stop jobs
from registering as agents. It also leaves wake and browser-debug capabilities
in the payload environment today. The detached wrapper needs the wake pair for
completion delivery; the payload's inheritance is recorded here as current
behavior, not as a claim that every payload needs those capabilities.

## YA compatibility and private names

Current YA builds still publish several agent-consumed outputs under `YEP_*`.
Readers accept these spellings during a reader-first migration, but they are
compatibility aliases, not naming precedent. YA normally filters inherited
`YEP_*` / `YA_*`; the rows below reach a provider only through an explicit
allowlist, provider overlay, or late Bash bridge.

| Legacy/current YA name | Canonical replacement or disposition | Effect here | `agentctl` launched command | `session-turn` native child |
|---|---|---|---|---|
| `YEP_CLAUDE_GATEWAY=1` | `AGENT_LAUNCH_ROUTE=claude-gateway` | Transitional instruction-route fallback. | inherit | remove |
| `YEP_COPILOT_API=1` | `AGENT_LAUNCH_BACKEND=copilot-api` | Transitional Copilot-supplement fallback. | inherit | remove |
| `YEP_SESSION_WAKE_URL` | `AGENT_SESSION_WAKE_URL` | Transitional agentctl wake fallback. | inherit into wrapper and payload | remove |
| `YEP_SESSION_WAKE_TOKEN` | `AGENT_SESSION_WAKE_TOKEN` | Transitional bearer credential; never log or persist. | inherit into wrapper and payload | remove |
| `YEP_BROWSER_DEBUG_AGENT_URL` | `AGENT_BROWSER_DEBUG_BROKER_URL` | Current YA browser-debug CLI input until publisher/reader migration. | inherit into wrapper and payload | remove |
| `YEP_BROWSER_DEBUG_CALLER_TOKEN` | `AGENT_BROWSER_DEBUG_CALLER_TOKEN` | Current browser-debug caller credential; never log or persist. | inherit into wrapper and payload | remove |
| `YEP_AGENT_HARNESS` | removed; use `AGENT_LAUNCH_HARNESS` | Pre-2026-08-17 launch marker that never reached its intended agent reader. | inherit if an old launcher supplied it | remove |
| `YEP_AGENT_INITIAL_MODEL` | removed; use `AGENT_LAUNCH_MODEL` | Pre-2026-08-17 invisible launch marker. | inherit if present | remove |
| `YEP_AGENT_INITIAL_EFFORT` | removed; use `AGENT_LAUNCH_EFFORT` | Pre-2026-08-17 invisible launch marker. | inherit if present | remove |
| `YEP_ORIGINAL_BASH_ENV` | keep private | YA bridge pointer to the caller's prior Bash startup file; not agent-facing semantic state. | inherit | remove |
| `YEP_PROVIDER_HOST_RUNTIME_DIR` | keep private | Explicit `session-turn` provider-host discovery directory, mainly for controlled installations/tests. | inherit | remove |

For wake/browser capabilities, a complete canonical pair wins; otherwise a
complete legacy pair is accepted without mixing names. For route/backend facts,
a present canonical marker controls routing and the legacy alias is considered
only when the canonical variable is absent. The migration order is reader first,
then dual-publish or canonical-publish with legacy aliases, then removal after
consumers have moved. The YA implementation work and its compatibility/test
surfaces are tracked in `~/ya/gaps/agent-facing-env-markers.md`.

## Fresh native session boundary

`session-turn` native fallback copies the caller environment because unrelated
operator and tool configuration may still be required by the target provider.
It removes only caller identity, launch-route/backend facts, Bash bridge state,
session wake/browser capabilities, and provider-native identity markers, then
sets the target's `AGENTCTL_SESSION_ID` and `AGENT_LAUNCH_HARNESS`. It preserves
`AGENT_GUARD` so the fresh target retains the shared-worktree Git guard.

This is a fresh-session boundary, unlike agentctl's same-task payload boundary.
A new harness must not inherit the caller's backend supplement selection or a
capability addressed to the caller session.
