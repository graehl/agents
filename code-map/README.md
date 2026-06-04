# Code Map

## Orientation

`~/agents` is a policy-and-tooling repository for filesystem-first coding
agents. A new developer should understand three flows first: global
instruction loading from `AGENTS.md` plus provider supplements; skill
lifecycle through `skills/<name>/SKILL.md`; and `agentctl` run tracking,
where `./agentctl` launches `agentctl.py`, writes `.agentctl/` runtime state,
and lets `agentctl_plugins/aim.py` write provenance records under
`runs/aim/`.

## Module Index

| Path | Responsibility | Inputs / Outputs | Key Callers / Callees | Evidence |
|---|---|---|---|---|
| `AGENTS.md` | Authoritative global operating contract: session recovery, task/topic use, edit discipline, commits, glossary, and tool conventions. | Inputs: user/project requests, repo state, companion docs. Outputs: behavioral constraints for agents and commit/topic policy. | Provider supplements (`AGENTS.codex.md`, `AGENTS.claude.md`) and skills rely on these rules. | verified: `sed -n '1,140p' AGENTS.md`; `cat AGENTS.user.md`; `cat AGENTS.codex.md` |
| `AGENTS.user.md` | User-specific preferences and active-project hints. | Inputs: personal project aliases and ML explanation preferences. Outputs: narrower defaults layered after `AGENTS.md`. | Read alongside global instructions by session policy. | verified: `cat AGENTS.user.md` |
| `AGENTS.codex.md`, `AGENTS.claude.md`, `AGENTS.weak.md` | Provider- or capability-scoped instruction supplements. | Inputs: provider runtime mechanics. Outputs: session-id/log-path guidance and model-specific amendments. | Loaded by agent/harness conventions after `AGENTS.md`. | verified: `rg --files`; `cat AGENTS.codex.md` |
| `GLOSSARY.md` | Project vocabulary table. | Inputs: curated rows plus topic-doc ledes. Outputs: terms reused in docs, commits, and reports. | Contribution rules live in `topics/glossary.md`. | verified: `cat GLOSSARY.md`; `cat topics/glossary.md` |
| `topics/*.md` | Cross-cutting concern docs, not module maps. | Inputs: concern contracts and invariants. Outputs: topic ledes for glossary, `Topic:` trailer namespace, and verification riders. | `AGENTS.md` routes significant work and commits through relevant topic docs. | verified: `rg --files`; `cat topics/agentctl.md topics/provenance-tracking.md topics/agent-instructions.md topics/glossary.md` |
| `skills/*/SKILL.md` | Reusable workflows such as `hi`, `bye`, `review`, `ship`, `harsh-review`, `doubt`, `rep`, `wish`, `start-task`, and `code-map`. | Inputs: user skill trigger. Outputs: scoped workflow instructions and optional provider configs under `skills/*/agents/`. | Consumed by Codex skill loading; `skills/code-map` produced this report. | verified: `find skills -maxdepth 3 -type f -print`; `cat skills/code-map/SKILL.md` |
| `tasks/*.md` | Git-ignored active-work scratchpads and handoff notes. | Inputs: per-feature direction and unfinished state. Outputs: private resume context, not durable project-facing conclusions. | Read on resume/implementation; omitted from public map details because task files are private live state. | verified: `ls -lt tasks` |
| `./agentctl` | Shell wrapper that selects Python >= 3.10 and sets `AGENTCTL_ROOT` to the invocation project. | Inputs: CLI args, `AGENTCTL_PYTHON`, project-local envs, active conda, PATH. Outputs: `exec` into `agentctl.py`. | Calls `agentctl.py`; lets one global checkout operate in many project roots. | verified: `sed -n '1,220p' agentctl` |
| `agentctl.py` | Dependency-free local job manager. Owns parser, plugin loading, process lifecycle, `.agentctl/` state, GPU waits/watch, status/list/tail/note/cleanup/wait/stop/restart verbs. | Inputs: CLI args and optional `agentctl_plugins/*.py` hooks. Outputs: `.agentctl/jobs/*/current.json`, `.agentctl/runs/*/*`, logs, metadata, child env. | Imports `artifact_meta` in `write_meta`; calls hooks from `agentctl_plugins/aim.py`; tested by `tests/test_agentctl.py`. | verified: `sed -n '1,260p' agentctl.py`; `rg -n "^(def|class) |argparse|subparsers|if __name__|main\\(" agentctl.py ...` |
| `agentctl_plugins/aim.py` | Default `agentctl` plugin that writes Aim-format text dumps and output back-pointer sidecars without importing the Aim SDK. | Inputs: `agentctl` state and hooks. Outputs: `runs/aim/<experiment>/manifest.jsonl`, `runs/<ref>.json`, `texts/<ref>/meta.markdown.md`, `<output>.meta.json`. | Registered by `agentctl.py` plugin loader; uses `import agentctl` helpers. | verified: `sed -n '1,380p' agentctl_plugins/aim.py`; `cat topics/provenance-tracking.md` |
| `artifact_meta.py` | Metadata sidecar builder and provenance lookup helper. | Inputs: output paths, setup/results/machine keyvals, declared inputs, Aim read roots. Outputs: `.meta.md`, `.running.md`, analysis-summary updates, input ancestry excerpts. | Called by `agentctl.py:write_meta`; searched by downstream scripts and tests. | verified: `sed -n '1,220p' artifact_meta.py`; `sed -n '220,620p' artifact_meta.py`; `sed -n '990,1130p' artifact_meta.py` |
| `tests/test_agentctl.py` | Stdlib-only end-to-end tests for `agentctl`, the Aim plugin, sidecars, restart, and cleanup behavior. | Inputs: copied `agentctl` files in temp workspaces. Outputs: pass/fail summary. | Exercises wrapper root selection, tracked/untracked runs, propagation, plugin failure tolerance, and marker cleanup. | verified: `sed -n '1,160p' tests/test_agentctl.py`; `sed -n '580,790p' tests/test_agentctl.py` |
| `scripts/commit-msg-fmt`, `scripts/commit-msg-lint` | Commit-message helper scripts. | Inputs: commit-message text. Outputs: formatting or lint diagnostics. | Support commit policy in `AGENTS.md`. | verified: `find agentctl_plugins scripts tests topics -maxdepth 2 -type f -print`; `rg -n ... scripts` |

## Flow Slices

### Instruction Recovery

1. `AGENTS.md` defines global session, edit, topic, glossary, commit, and
   tool-use policy.
2. `AGENTS.user.md` adds graehl-specific active-project and explanation
   preferences.
3. Provider supplements such as `AGENTS.codex.md` add harness mechanics:
   real session id lookup and provider log paths.
4. On resume, the `hi` skill checks whether `last-session.md` is stale, then
   prefers live worktree/task/job/session-log state when needed.

Seams: edit global rules in `AGENTS.md`; provider-only mechanics in
`AGENTS.codex.md` or `AGENTS.claude.md`; user-specific preferences in
`AGENTS.user.md`.

Evidence: verified: `cat AGENTS.user.md`; `cat AGENTS.codex.md`;
`cat /home/graehl/.codex/skills/user/hi/SKILL.md`.

### Skill Lifecycle

1. A reusable workflow lives in `skills/<name>/SKILL.md`, with optional
   provider configuration in `skills/<name>/agents/`.
2. For new or changed skills, the system `skill-creator` guidance supplies
   the structure and validation expectation.
3. `skills/code-map/SKILL.md` defines this report's required sections,
   evidence labels, and traversal workflow.
4. Git-ignored task files can capture private calibration status until the
   report type is stable enough for a glossary row or helper template.

Seams: update the skill body for workflow behavior; add optional helper
scripts under the skill only after repeated reports prove the need; record
private active decisions in task files rather than in the public map.

Evidence: observed: `python3 /home/graehl/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/graehl/agents/skills/code-map` returned `Skill is valid!` during calibration; verified: `cat skills/code-map/SKILL.md`.

### Agentctl Launch And State

1. `./agentctl` resolves the install directory as code root, resolves the
   invocation directory or `AGENTCTL_ROOT` as project root, picks Python >=
   3.10, and `exec`s `agentctl.py`.
2. `agentctl.py:main()` loads plugins, special-cases `start`/`smoke` parsing
   around `--`, then dispatches to a verb function.
3. `agentctl.py:start()` resolves GPU waits, `--after` gates, inputs,
   outputs, script fingerprints, env, and pre-launch state; it writes
   `.agentctl/runs/<job>/<run-id>/state.json` and mirrors
   `.agentctl/jobs/<job>/current.json`.
4. Non-watch launches re-enter through `_run-child`; `run_child()` waits on
   dependencies, writes launch metadata, runs the payload, records
   `exit-status.json`, stats outputs, merges `propagate.json`, and calls
   plugin finish hooks.
5. Status verbs read current state and refresh it from process/exit sidecars.

Seams: parser options live in `add_start_options()` and `build_parser()`;
launch state assembly is in `start()`; child completion is in `run_child()`;
status rendering is in `status()` / `print_status_state()`.

Evidence: verified: `sed -n '1070,1475p' agentctl.py`;
`sed -n '2240,2760p' agentctl.py`; `cat topics/agentctl.md`.

### Provenance Dump And Sidecars

1. `agentctl.py:_load_plugins()` imports every non-underscore
   `agentctl_plugins/*.py`; plugins can extend args, mutate state/env, write
   metadata, react to notes, and repair restart args.
2. `agentctl_plugins/aim.py:register_args()` adds `--no-aim`,
   `--experiment`, and `--tag`.
3. `on_start()` sets `state["aim"]`, `experiment`, tags, synthetic
   `aim_run_hash`, and child `AIM_*` env vars.
4. `agentctl.py:write_meta()` builds `.meta.md` through
   `artifact_meta.build_meta_markdown()` and gives plugins
   `on_meta_built()` a chance to write dumps.
5. `agentctl_plugins/aim.py:on_finish()` writes `<output>.meta.json`
   back-pointers for declared outputs that exist.
6. `artifact_meta.find_aim_run_record()` and `find_aim_run_text()` locate
   runs later from metadata and configured read roots.

Seams: the plugin hook list is the process/provenance boundary; sidecar
schema changes belong in `agentctl_plugins/aim.py` and
`topics/provenance-tracking.md`; markdown rendering changes belong in
`artifact_meta.py`.

Evidence: verified: `sed -n '840,1140p' agentctl.py`;
`sed -n '1,380p' agentctl_plugins/aim.py`;
`sed -n '220,620p' artifact_meta.py`; `cat topics/provenance-tracking.md`.

### Topic And Glossary Maintenance

1. `topics/*.md` files define cross-cutting contracts and ledes; topic
   basenames are the `Topic:` trailer namespace.
2. `GLOSSARY.md` keeps one sorted term table; topic-linked rows derive from
   topic ledes, while vernacular rows are curated.
3. `topics/glossary.md` owns contribution and regeneration rules.
4. Tasks can point to topics, but tasks do not replace topic docs for durable
   project-facing knowledge.

Seams: edit topic contracts in `topics/<name>.md`; edit glossary contribution
rules in `topics/glossary.md`; update `GLOSSARY.md` rows when vocabulary
becomes stable.

Evidence: verified: `cat GLOSSARY.md`; `cat topics/glossary.md`;
`rg --files`.

## Contracts And Seams

- `agent-instructions`: `AGENTS.md` is the global authority; local/project
  files may narrow it, and task files are not durable project-facing
  authority. Evidence: verified: `cat topics/agent-instructions.md`.
- `agentctl`: `.agentctl/runs/<job>/<run-id>/state.json` and
  `.agentctl/jobs/<job>/current.json` are canonical runtime status; plugins
  are optional hooks and loader failures warn without breaking the base.
  Evidence: verified: `cat topics/agentctl.md`.
- `provenance-tracking`: `runs/aim/` dumps and `<output>.meta.json`
  sidecars form the provenance graph; no workflow DSL or automatic dependency
  discovery is assumed. Evidence: verified: `cat topics/provenance-tracking.md`.
- `glossary`: `GLOSSARY.md` is a single sorted table; topic-linked rows derive
  from topic ledes; scoped sub-glossaries are placed by enclosing use.
  Evidence: verified: `cat topics/glossary.md`.
- Testing seam for `agentctl`: `tests/test_agentctl.py` is the current
  vertical slice and should catch changes to wrapper root selection, Aim dumps,
  input/output declarations, propagation, plugin loading, restart, and marker
  cleanup. Evidence: verified: `sed -n '1,160p' tests/test_agentctl.py`;
  `sed -n '580,790p' tests/test_agentctl.py`.

## Blind Spots

- This map did not execute `tests/test_agentctl.py`; it is a static traversal
  plus a prior observed skill validation. Treat runtime behavior claims as
  source-verified, not freshly test-observed.
- Dynamic plugin behavior is represented by the hook surface and the one
  concrete `aim` plugin. The generality of the hook surface remains partly
  assumed until another plugin uses it.
- `tasks/` and `.agentctl/` are git-ignored live state; their current contents
  can change between refreshes and are not durable project-facing authority.
- `find ... -type f` showed `__pycache__` files under some directories; they
  are runtime byproducts and intentionally omitted from the module index.
- Provider-specific skill loading is inferred from local skill files and
  Codex instructions; this report did not inspect an external skill registry.

## Reproduce / Refresh

Run from `/home/graehl/agents`:

```bash
rg --files
find skills -maxdepth 3 -type f -print
find agentctl_plugins scripts tests topics -maxdepth 2 -type f -print
cat README.md
sed -n '1,140p' AGENTS.md
cat GLOSSARY.md
cat skills/code-map/SKILL.md
cat topics/agentctl.md topics/provenance-tracking.md topics/agent-instructions.md topics/glossary.md
sed -n '1,220p' agentctl
sed -n '1,260p' agentctl.py
sed -n '840,1140p' agentctl.py
sed -n '1070,1475p' agentctl.py
sed -n '2240,2760p' agentctl.py
sed -n '1,380p' agentctl_plugins/aim.py
sed -n '1,220p' artifact_meta.py
sed -n '220,620p' artifact_meta.py
sed -n '990,1130p' artifact_meta.py
sed -n '1,160p' tests/test_agentctl.py
sed -n '580,790p' tests/test_agentctl.py
rg -n "^(def|class) |argparse|subparsers|if __name__|main\\(" agentctl.py artifact_meta.py agentctl_plugins scripts tests
```
