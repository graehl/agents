# Agent Instructions

Reusable operating instructions, topic docs, skills, and small helper tools for
coding agents that work inside real project directories.

This repo is not an app framework and not a prompt pack of slogans. It
is a working policy layer for agents that inspect local files, share dirty
worktrees, run commands, launch long jobs, write commits, and need the next
session to recover what happened without trusting stale chat context.

The central idea is simple: durable instructions belong in the repository, not
only in the current conversation. A future agent can read committed files,
verify the live worktree, and act from the same contracts the previous agent
used.

The core policy is subagent-agnostic: it takes no position on whether tasks
are completed by a single agent, delegated subagents, or autonomous swarms,
but it is best-effort safe when multiple agents operate concurrently. It does
not depend on skills, provider supplements, or any particular launcher: the
same instructions have been exercised in at least the Codex, Claude Code,
opencode, and Grok Build harnesses. The
shared-worktree
accommodations are plain filesystem conventions: active-session files for
awareness of other agents, pre-edit rereads and path-limited edits for edit
safety, and gates around operations that can affect shared state. The shared
worktree is a deliberate trade of isolation for observability — interrupted
work stays visible, integration is continuous, and the whole state is readable
in one place — with the conventions buying the safety back. Skills are
optional automation on top; the framework still stands with zero skills
installed.

## Who This Is For

Use this repo as a reference if you run coding agents in filesystem-first
projects and care about:

- preserving unrelated user or peer work in dirty checkouts;
- running independent agents or subagents in one worktree without assuming a
  shared supervisor;
- resuming after disconnects, compaction, or handoff;
- separating private task state from committed project knowledge;
- loading topic-specific instructions only when triggered, so agent boot does
  not leave the context half full;
- keeping research claims, runs, and artifacts traceable;
- making commits and reviews explain motivation as well as diff mechanics;
- giving strong agents room for judgment while still blocking known failure
  modes.

It is deliberately opinionated. You should adapt it before dropping it into a
different workflow, especially where your project has different rules for
branches, commits, shared workdirs, or private notes.

## Start Here

| Path | Purpose |
| --- | --- |
| `AGENTS.global.md` | Installable global operating contract: session entry, worktree safety, edit discipline, commits, topics, glossary, and interaction rules. |
| `AGENTS.supplemental.md` | Optional slow-path clarification preserving the fuller global protocol; never installed or read as routine boot. |
| `AGENTS.md` | Project boot for developing this instruction repository; deliberately distinct from the global install source. |
| `AGENTS.codex.md`, `AGENTS.claude.md`, `AGENTS.grok.md` | Harness-specific mechanics such as session identifiers, log locations, and launcher quirks. |
| `AGENTS.frontier.md`, `AGENTS.weak.md` | Capability-tier latitude and extra reminders; load-bearing policy still belongs in `AGENTS.global.md`. |
| `AGENTS.anthropic.md`, `AGENTS.opus.md`, `AGENTS.sol.md` | Model-family behavior patches selected from the harness-recorded model id. |
| `RESEARCH.md`, `RESEARCH.supplemental.md` | Compact research binding rules plus optional templates, rationale, and edge cases. |
| `research-advisor.md` | Handoff protocol for the long-lived, normally project-wide skeptical research-advisor session. |
| `advisor/charter.md` | Durable global mandate and operating behavior loaded into every research-advisor session. |
| `RUNS.md`, `RUNS.supplemental.md` | Compact run-operation binding rules plus optional templates, rationale, and rare mechanics. |
| `feature-branch.md` | Optional branch-per-feature workflow for projects that opt into it. |
| `GLOSSARY.md` | Project vocabulary that agents should reuse in docs, code, UI copy, and commits. |
| `TOPICS.md`, `topic-definitions.md` | Topic vocabulary and curated general-domain definitions used when naming project concerns. |
| `topics/` | Committed cross-cutting contracts and rationale: debugging, testing, agent instructions, run provenance, UI verification, and more. |
| `topics/handoffs.md` | Selection, contents, milestone maintenance, and live-state validation for working handoffs. |
| `ideas/` | Durable seeds for possible projects unrelated to this repository; preservation without implementation commitment. |
| `skills/` | Optional workflows layered on the core policy; highlights below. |
| `agentctl`, `agentctl.py`, `agentctl_plugins/` | A dependency-free process manager with active-session participation, run state, optional plugins, and foreground local/SSH GPU-capacity watching. |
| `scripts/` | Small helper scripts, including guarded git launchers, scheduled-prompt claiming, on-deck queue scaffolding, and commit-message formatting checks. |
| `code-map/` | Developer-facing maps of this repo and selected related repos. |
| `tests/` | Regression coverage for `agentctl` behavior. |

Machine-local supplements such as `AGENTS.local.md` or `AGENTS.user.md` are
intentionally private in this setup. Public instructions should stand alone
without relying on those files.

## Install

Clone the checkout at `~/agents` when possible. The global corpus defines
`~/agents` as its canonical root, and routed supplements and topic docs use
that spelling. Then inspect or install every supported harness:

```bash
cd ~/agents
scripts/install-agents status
scripts/install-agents install
scripts/install-agents status
```

Select one or several harnesses with repeated or comma-separated
`--harness` values; the default is `all`. Accepted names are `codex`,
`claude`, `pi`, `opencode`, `grok`, and `copilot` (with `grok-build`,
`claude-code`, and `copilot-cli` aliases).

The current user-level destinations are:

| Harness | Global instructions | Skills |
| --- | --- | --- |
| Codex | `~/.codex/AGENTS.md` | `~/.agents/skills` |
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills` |
| Pi | `~/.pi/agent/AGENTS.md` | `~/.pi/agent/skills` |
| OpenCode | `~/.config/opencode/AGENTS.md` | `~/.agents/skills` (auto-discovered) |
| Grok Build | `~/.grok/AGENTS.md` | `~/.grok/skills` |
| GitHub Copilot CLI/TUI | `~/.copilot/copilot-instructions.md` | `~/.agents/skills` |

Instruction targets point directly to `AGENTS.global.md`. An absent skill root
becomes one symlink to `skills/`; an existing directory keeps unrelated skills
and receives one link per repository skill. Roots already resolving to this
checkout are left alone.

Re-running `install` reconciles repository skill additions and retirements.
For a retired skill, it removes only an alias the installer created and restores
the exact pre-install object recorded for that path. `status` reports an
installed retired alias until this refresh is run.

Use `--home` for an isolated rehearsal before touching a real profile:

```bash
mkdir -p ~/.cache
test_home=$(mktemp -d ~/.cache/agents-install-test.XXXXXX)
scripts/install-agents install --home "$test_home"
scripts/install-agents status --home "$test_home"
scripts/install-agents uninstall --home "$test_home"
```

Each install writes a readable manifest and filesystem snapshots under
`~/.local/state/agents-install/backups/`. It records absent paths, regular
files, directories, symlinks (including broken ones), inode/link metadata,
and a non-mutating snapshot of `~/AGENTS.md` when present. `uninstall` restores
the prior kind, content, link target, and mode of paths the installer replaced;
it refuses to overwrite a path changed after installation. Backups remain
after uninstall.

The installer never creates or modifies `~/AGENTS.md`, and it deliberately has
no hardlink mode. A hardlink to a Git-controlled file can retain the old inode
when checkout or pull replaces that path, silently freezing stale policy.
Symlinks follow the named `AGENTS.global.md` across Git updates.

## Skill Highlights

| Skill | Why it is interesting |
| --- | --- |
| `skills/wish/` | Pursues an unattended goal against an explicit done-condition and quoted evidence, while refusing verifier-gaming shortcuts. |
| `skills/harsh-review/` | Runs a deliberately strict structural and correctness audit: deleting reframes, spaghetti, leaky abstractions, and logic that breaks on a concrete input. |
| `skills/code-map/` | Produces a regenerable developer map of modules, flow slices, contracts, seams, blind spots, and refresh commands. |
| `skills/doubt/` | Re-solves a disputed conclusion independently before comparing with the earlier answer to find the first consequential divergence. |
| `skills/dream/` | Consolidates a doc project by pruning contradiction/staleness and distilling facts established in recent sessions but never written down. |
| `skills/others/` | Reports the active-agent state in the current project: self entry, active peers, recently DONE work, and stale sessions. |
| `skills/rep/` | Repeats or self-paces a prompt across wakeups; useful as a workaround when an agent harness lacks built-in loop capability. |
| `skills/on-deck/` | Adds guarded single-step research/run jobs to a project's `on-deck/` queue. |
| `skills/steward/` | Fills idle GPU capacity from eligible on-deck entries, with `/rep steward` as the repeated form. |

## What the Rules Preserve

**Continuity.** Sessions are recoverable from a named working handoff and live
state: worktree, active sessions, task files, run metadata, artifacts, and only
then old chat logs. Bare `/hi` can use `tasks/ROOT` as a discovery hint; routine
compaction does not invoke a manual save/restore ritual.

**Shared-workdir safety.** Agents must not reach for broad discard commands to
repair their own history or line up an amend. The default posture is to inspect
status, notice active peers, reread files before delayed edits, preserve
unrelated work, and use path-limited edits.

**Durable knowledge.** Private `tasks/*.md` files can hold active direction and
handoff notes. Committed `topics/*.md` files hold project-facing contracts,
rationale, invariants, and evidence that should survive a branch or session.

**Explicit gates.** Pushes, deploys, migrations, dependency upgrades,
destructive commands, and wholesale replacement of user-authored content require
a written gate record before action. Local commits get a lighter check.

**Verification over assertion.** Agents are told to verify project claims
against the repo, build a map before drilling into unfamiliar code, and test the
contract a change could violate rather than only the line it touched.

**Lean but load-bearing instructions.** The goal is not to script every move.
Rules should prevent concrete failures a capable agent might still make; prompt
debt is treated as a maintenance cost.

## Common Adoption Paths

- **One project, one agent:** start with `AGENTS.global.md`, then trim sections that
  do not apply. Keep a project-local supplement for branch, test, and deploy
  rules.
- **Shared dirty worktree:** keep the active-session convention, discard ban,
  pre-edit reread rule, path-limited edit habit, and big-effect gate. Those are
  the high-value safety pieces.
- **Research or eval repo:** add `RESEARCH.md`, `RUNS.md`,
  `topics/provenance-tracking.md`, `topics/on-deck.md`, and `agentctl` so
  experiments, queued GPU fillers, claims, and artifacts have a recoverable
  record.
- **Instruction-design work:** read `topics/agent-instructions.md` and
  `topics/instruction-ablation.md`. This repo treats instruction quality as a
  hypothesis to test, not as a belief proven by sounding careful.
- **Skills:** copy or adapt only the skills you actually invoke. A skill
  should encode a reusable workflow, not a general preference.

## Boundaries

These files assume an agent can read and write a real working tree, run local
commands, and inspect git state. They are less useful in a chat-only setting or
in a locked environment where the agent cannot verify the filesystem.

The repo also does not claim that more instructions automatically make agents
better. Some rules are present because weaker or non-frontier agents still work
in these projects; others exist because a specific failure already happened.
When a rule no longer steers behavior, the project prefers cutting it over
preserving it as ceremony.

The project is built for strong-agent workflows, primarily GPT-5.5+ and Opus
4.7+. It has also steered weaker agents, including Qwen3.6-27B and Grok Build,
on tasks within their reach.
