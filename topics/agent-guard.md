# Agent git discard guardrail

> The prevention half of the shared-workdir discard defense: a
> PATH-level `git` shim that refuses work-discarding commands while a
> live `.agentctl/active` peer shares the workdir. A guardrail against
> the careless command, not a sandbox.

Topic: `agent-guard`

Motivation: an agent ran `git reset --hard origin/master` "so I can land
my amend against the right commit" in a shared workdir and wiped another
agent's unsaved hour. The discard ban (AGENTS.md) is the rule; this is the
mechanical backstop for when an agent skips the rule. It is prevention
only — the recovery half (a passive worktree snapshot into a git object so
a lost worktree is recoverable) is a separate, not-yet-built partner.

## Components

- `scripts/agent-guarded` — launcher. `agent-guarded <cmd> [args]`
  synthesizes a shim dir whose `git` symlinks to `agent-guard-git`,
  prepends it to PATH, and exports `AGENT_GUARD=1` plus
  `AGENT_GUARD_REAL_GIT` (the true git), then execs the command. Marking
  at the launch chokepoint — rather than heuristically detecting "am I an
  agent" — makes the guard reliable by construction and transitive: env
  inheritance flows through every subshell, script, and grandchild the
  harness spawns, the coverage a per-harness PreToolUse hook lacks.
- `scripts/agent-guard-git` — the shim, resolved as `git`. Parses past
  leading global options, classifies the subcommand, and either refuses
  (live peer present) or execs the real git unchanged.

## Contracts

- **Binds at launch.** The shim only exists if the harness was started
  through `agent-guarded` (or an env that sets `AGENT_GUARD` + the shim
  PATH). An agent already running in a bare session cannot wrap itself, so
  the in-session obligation is only: at session start in a shared-workdir
  project, if `AGENT_GUARD` is unset, warn once and continue.
- **Gate is the env var, not identity.** Anyone in a guarded context — the
  agent or the user typing manually — hits the shim. `AGENT_GUARD= git …`
  is the deliberate override (and, being identical to the bypass, is why
  the prose never claims prevention, only friction).
- **Peer detection mirrors AGENTS.md:** `find .agentctl/active -maxdepth 1
  -type f -mmin -70`, skipping entries that start with `DONE` and the
  agent's own session file. Zero live peers ⇒ allow (solo work is not
  endangering anyone).

## Classified as discarding

reset `--hard`/`--merge`; `clean` (any); `restore` unless `--staged`-only;
`checkout`/`co` with `-f`/`--force`/`--`/`.`; `stash drop`/`clear`. `co` is
matched because the shim sees the literal token before git expands the
alias. Scope is worktree/index discard only — push/force-push (the gated
remote action) and branch-ref deletion are different concerns, untouched.

## Known gaps (accepted, not bugs)

- `git checkout <file>` without `--` is not caught: lexing cannot tell a
  pathspec from a branch name, and a per-call `rev-parse` was rejected as
  not worth it. Countered by advising the explicit `git checkout -- <path>`
  / `git restore <path>` form (AGENTS.md); a bare form is the agent's
  fault.
- Protection is only as good as `.agentctl/active` hygiene. A peer that
  never wrote an active entry (the convention exempts read-only/interview
  sessions) or crashed mid-write is invisible to the guard — and is
  precisely the victim who can't be protected. That is the peer's risk.
- Absolute-path (`/usr/bin/git`), `command git`, and env-stripped calls
  bypass entirely, by design. The threat model is the careless command,
  not an adversary; closing these would mean seccomp/namespace territory,
  a different and far heavier project.

## Deployment

- `~/bin/agent-guarded` → `scripts/agent-guarded` (PATH-installed).
- `~/local.sh` wires `AGENT_GUARD` into agent contexts only, never general
  shells:
  - `tms` (the agent tmux funnel) wraps the command in `agent-guarded` and
    marks the session. tmux 2.7 has no `new-session -e`, so it runs
    `tmux start-server` then `set-environment -g AGENT_GUARD 1` before
    `new-session`, so manual shell panes opened in the session inherit it.
  - `reyep` sets `AGENT_GUARD=1` in the yepanywhere server's env, so
    YA-spawned login shells inherit it.
  - A guarded-context block prepends the shim to PATH whenever
    `AGENT_GUARD` is set, capturing the real git first — so a manual
    `git` typed in an agent pane is guarded too. General shells leave
    `AGENT_GUARD` unset and are untouched.
