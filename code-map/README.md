# Code Map

## Orientation

`~/agents` is a **policy-and-tooling repository for filesystem-first coding
agents** — not an app or framework. Its center of gravity is prose: a layered
instruction contract (`AGENTS.md` + provider supplements), a `topics/*.md`
contract library, a `GLOSSARY.md`, and a `skills/` workflow set. A small
dependency-free Python layer (`agentctl.py`, `artifact_meta.py`, the `aim`
plugin) gives agents local job tracking and run provenance.

Three flows orient a new reader fastest:

1. **Instruction loading** — how an agent assembles its operating contract
   from `AGENTS.md`, `AGENTS.user.md`, and a provider supplement.
2. **`agentctl` run lifecycle** — `./agentctl` → `agentctl.py` launch/child/
   status verbs writing `.agentctl/jobs/` and `.agentctl/runs/` state, with
   `aim`-plugin provenance dumps.
3. **The agent activity register** — `.agentctl/active/<session-id>`, a
   *convention-only* coordination file (written by agents per `AGENTS.md`,
   read by the `/others` skill), distinct from `agentctl.py` job state.

Distinguish the two `.agentctl` worlds: **job state** (`jobs/`, `runs/`) is
owned by `agentctl.py`; the **active register** (`active/`) is owned by the
agent-instructions convention and touched by no Python here.

## Module Index

| Path | Responsibility | Inputs / Outputs | Key Callers / Callees | Evidence |
|---|---|---|---|---|
| `AGENTS.md` | Authoritative global operating contract: session recovery, activity register, task/topic use, edit discipline, commits, glossary, gates, tool conventions. | In: user/project requests, repo state, companion docs. Out: behavioral constraints, commit/topic policy. | Provider supplements and skills build on it. | verified: `wc -l AGENTS.md` (≈32KB) |
| `AGENTS.user.md` | Personal supplement (active-project hints, ML explanation prefs) layered after the global contract. | In: graehl-specific defaults. Out: narrower per-user policy. | Read alongside `AGENTS.md` each session. | verified: `cat AGENTS.user.md` |
| `AGENTS.codex.md`, `AGENTS.claude.md`, `AGENTS.weak.md` | Provider/capability supplements: session-id discovery, log paths, weak-model amendments. Harness mechanics only. | In: provider runtime facts. Out: id/log guidance. | Loaded after `AGENTS.md` by harness routing. | verified: `cat AGENTS.claude.md` |
| `README.md`, `RESEARCH.md`, `RUNS.md`, `feature-branch.md` | Repo intro + opt-in companion policy (research method, run ops, branch-per-feature). | In: triggering work mode. Out: scoped extra rules. | `AGENTS.md` "Optional supplements" loads on trigger. | verified: `cat README.md` |
| `GLOSSARY.md` | Single prescriptive vocabulary table. | In: curated rows + topic ledes. Out: reused terms. | Rules in `topics/glossary.md`. | verified: `cat GLOSSARY.md` |
| `TOPICS.md`, `topic-definitions.md` | Topic-granularity guidance and curated jargon namespace. | In/Out: vocabulary calibration. | Consulted when creating/assessing topics. | verified: `rg --files` |
| `topics/*.md` (31 files) | Cross-cutting concern docs (contracts, invariants), method docs (`debugging`, `testing`, `prototyping`), and companions (`.evidence.md`, `.bearings.md`, `.testing.md`). Basenames = `Topic:` trailer namespace. | In: concern contracts. Out: ledes, trailer vocabulary, verification riders. | `AGENTS.md` routes significant work/commits through them. | verified: `ls topics/` |
| `skills/*/SKILL.md` (11 skills) | Reusable workflows: `hi`, `bye`, `start-task`, `ship`, `review`, `harsh-review`, `doubt`, `rep`, `wish`, `others`, `code-map`. | In: user skill trigger. Out: scoped workflow steps. | Invoked by harness skill loader. | verified: per-skill `name:`/`description:` read |
| `skills/others/SKILL.md` | Reads `.agentctl/active/` to report own status, live peers, recent DONE, stale entries. | In: register files + mtimes. Out: peer summary. | Pure reader of the convention `AGENTS.md` defines. | verified: `rg -n 'find .agentctl\|DONE\|mmin' skills/others/SKILL.md` |
| `tasks/*.md` | Git-ignored active-work scratchpads / handoff state. | In: per-feature direction. Out: private resume context. | Read on resume; not durable project authority. | verified: `ls tasks` (git-ignored) |
| `./agentctl` | Shell wrapper: pick Python ≥3.10, set `AGENTCTL_ROOT` to invocation dir, `exec agentctl.py`. | In: argv, `AGENTCTL_PYTHON`, local envs, conda, PATH. Out: exec into `agentctl.py`. | Lets one global checkout drive many project roots. | verified: `cat agentctl` |
| `agentctl.py` (2754 LOC) | Dependency-free local job manager: parser, plugin loader, process lifecycle, `.agentctl/` job state, GPU waits, and `start`/`smoke`/`status`/`tail`/`note`/`cleanup`/`watch`/`wait`/`wait-gpu`/`stop`/`restart` verbs. Does **not** manage `.agentctl/active/`. | In: argv, optional `agentctl_plugins/*.py` hooks. Out: `.agentctl/{jobs,runs}/...`, logs, metadata, child env. | Imports `artifact_meta` in `write_meta`; calls `aim` hooks; tested by `tests/test_agentctl.py`. | verified: `rg -n '^def (start\|run_child\|status\|main\|build_parser)' agentctl.py` |
| `agentctl_plugins/aim.py` (383 LOC) | Default plugin: Aim-format text dumps + output back-pointer sidecars, no Aim SDK import. | In: agentctl state/hooks. Out: `runs/aim/<exp>/manifest.jsonl`, `runs/<ref>.json`, `texts/<ref>/...`, `<output>.meta.json`. | Loaded by `agentctl.py` plugin loader; `import agentctl` helpers. | verified: `rg -n '^def ' agentctl_plugins/aim.py` |
| `artifact_meta.py` (1072 LOC) | Metadata sidecar builder + provenance lookup (`build_meta_markdown`, `find_aim_run_record`, `find_aim_run_text`, `stat_artifact`). | In: output paths, key/vals, declared inputs, read roots. Out: `.meta.md`/`.running.md`, summary updates, ancestry excerpts. | Called by `agentctl.py:write_meta`; searched by downstream/tests. | verified: `rg -n '^def (build_meta_markdown\|find_aim_run_record)' artifact_meta.py` |
| `tests/test_agentctl.py` (783 LOC) | Stdlib-only end-to-end tests for wrapper root selection, runs, Aim dumps, sidecars, propagation, plugin tolerance, restart, cleanup. | In: copied agentctl files in temp dirs. Out: pass/fail. | The current vertical test slice for the Python layer. | verified: `wc -l tests/test_agentctl.py` |
| `scripts/commit-msg-fmt`, `scripts/commit-msg-lint` | Commit-message format/lint helpers supporting `AGENTS.md` commit policy. | In: commit text. Out: formatting/diagnostics. | Standalone helper scripts. | verified: `ls scripts/` |

## Flow Slices

### Instruction Loading

1. `AGENTS.md` defines global session, register, edit, topic, glossary,
   commit, gate, and tool policy.
2. `AGENTS.user.md` layers graehl-specific project/explanation preferences.
3. The provider supplement (`AGENTS.claude.md` for this harness) adds
   session-id discovery and transcript log paths — mechanics only.
4. Triggered companions (`RESEARCH.md`, `RUNS.md`, `feature-branch.md`) and
   relevant `topics/*.md` load on demand.

Seams: global rules → `AGENTS.md`; provider mechanics → `AGENTS.<provider>.md`;
personal prefs → `AGENTS.user.md`; concern contracts → `topics/<name>.md`.
Evidence: verified: `cat AGENTS.md AGENTS.user.md AGENTS.claude.md`.

### Agentctl Launch And State

1. `./agentctl` resolves code root vs. project root, picks Python ≥3.10,
   sets `AGENTCTL_ROOT`, and `exec`s `agentctl.py`.
2. `main()` (`agentctl.py:2730`) loads plugins, special-cases `start`/`smoke`
   parsing around `--`, dispatches to a verb via `build_parser()`
   (`:2463`).
3. `start()` (`:1078`) resolves GPU waits, `--after` gates, inputs/outputs,
   script fingerprints, env, and pre-launch state; writes
   `.agentctl/runs/<job>/<run-id>/state.json` and mirrors
   `.agentctl/jobs/<job>/current.json`.
4. `run_child()` (`:1364`) waits on dependencies, writes launch metadata,
   runs the payload, records `exit-status.json`, stats outputs, merges
   `propagate.json`, and calls plugin finish hooks.
5. `status()` (`:1497`) / `print_status_state()` (`:1552`) read current state
   and refresh it from process/exit sidecars.

Seams: start options in `add_start_options()` (`:2241`); launch assembly in
`start()`; child completion in `run_child()`; status render in
`print_status_state()`.
Evidence: verified: `rg -n '^def (start|run_child|status|main|build_parser|add_start_options)' agentctl.py`.

### Provenance Dump And Sidecars

1. `agentctl.py:_load_plugins()` imports every non-underscore
   `agentctl_plugins/*.py`; hooks may extend args, mutate state/env, write
   metadata, react to notes, and repair restart args.
2. `aim.py:register_args()` adds `--no-aim`, `--experiment`, `--tag`.
3. `on_start()` sets `state["aim"]`, experiment, tags, a synthetic
   `aim_run_hash`, and child `AIM_*` env vars.
4. `agentctl.py:write_meta()` builds `.meta.md` via
   `artifact_meta.build_meta_markdown()`, then gives `on_meta_built()` a
   chance to write the dump.
5. `aim.py:on_finish()` writes `<output>.meta.json` back-pointers for
   declared outputs that exist.
6. `artifact_meta.find_aim_run_record()` / `find_aim_run_text()` relocate runs
   later from metadata and configured read roots.

Seams: the hook list is the provenance boundary; sidecar schema →
`aim.py` + `topics/provenance-tracking.md`; markdown render → `artifact_meta.py`.
Evidence: verified: `rg -n '^def ' agentctl_plugins/aim.py`;
`cat topics/provenance-tracking.md`.

### Agent Activity Register (convention-only)

1. `AGENTS.md` "Agent activity register" tells an agent to write
   `.agentctl/active/<session-id>` on first planning-to-act in a shared
   workdir — line 1 a present-tense gist, optional line 2 `scope: <paths>`,
   `DONE`-prefixed on completion.
2. The session id is the provider's real resumable id; `AGENTS.claude.md`
   gives the discovery snippet (transcript filename stem under
   `~/.claude/projects/<hash>/`).
3. The `/others` skill (`skills/others/SKILL.md`) reads the directory,
   classifying files by mtime and `DONE`-prefix into self / live peers /
   recent DONE / stale.
4. No Python in this repo creates or parses these files — `agentctl.py`'s
   `--active` flag is an unrelated alias for `--running-only` job filtering.

Seams: register schema → `AGENTS.md`; reader classification → `skills/others`;
id discovery → provider supplement. The register is *not* job state.
Evidence: verified: `find .agentctl/active -maxdepth 1 -type f`;
`rg -n 'active' agentctl.py` (only `--running-only` alias).

### Topic And Glossary Maintenance

1. `topics/*.md` define cross-cutting contracts/ledes; basenames are the
   `Topic:` trailer namespace.
2. `GLOSSARY.md` keeps one sorted table; topic-linked rows derive from ledes,
   vernacular rows are curated.
3. `topics/glossary.md` owns contribution/regeneration rules; `TOPICS.md`
   calibrates topic granularity.
4. Tasks may point to topics but never replace them for durable knowledge.

Seams: contracts → `topics/<name>.md`; vocabulary rules → `topics/glossary.md`;
rows → `GLOSSARY.md`.
Evidence: verified: `cat GLOSSARY.md topics/glossary.md`.

## Contracts And Seams

- `agent-instructions`: `AGENTS.md` is the global authority; local/project
  files narrow it; task files are not durable authority.
  Evidence: verified: `cat topics/agent-instructions.md`.
- `agentctl`: `.agentctl/runs/<job>/<run-id>/state.json` and
  `.agentctl/jobs/<job>/current.json` are canonical job status; plugins are
  optional hooks whose loader failures warn without breaking the base.
  Evidence: verified: `cat topics/agentctl.md`.
- `provenance-tracking`: `runs/aim/` dumps + `<output>.meta.json` sidecars
  form the provenance graph; no workflow DSL or auto dependency discovery.
  Evidence: verified: `cat topics/provenance-tracking.md`.
- `glossary`: `GLOSSARY.md` is one sorted table; topic-linked rows derive from
  ledes; scoped sub-glossaries sit at the narrowest enclosing dir.
  Evidence: verified: `cat topics/glossary.md`.
- Activity-register contract (no dedicated topic doc): `.agentctl/active/`
  files are present-tense status, `DONE`-prefixed when complete, classified
  by 70-min staleness. Owned by `AGENTS.md` prose + `/others`, not Python.
  Evidence: verified: `rg -n 'Agent activity register' AGENTS.md`;
  `cat skills/others/SKILL.md`.
- Python test seam: `tests/test_agentctl.py` is the vertical slice guarding
  wrapper root selection, Aim dumps, I/O declarations, propagation, plugin
  loading, restart, and marker cleanup.
  Evidence: verified: `wc -l tests/test_agentctl.py`.

## Blind Spots

- This map is static traversal; it did **not** run `tests/test_agentctl.py`.
  Runtime behavior claims are source-verified, not freshly observed.
- The plugin hook surface is exercised by only one concrete plugin (`aim`);
  its generality beyond that is partly assumed.
- `tasks/` and `.agentctl/` are git-ignored live state; contents drift between
  refreshes and carry no durable project authority. The `active/` listing
  captured here is a momentary snapshot.
- Skill *invocation* mechanics live in the harness, not this repo; only the
  `SKILL.md` bodies are inspected.
- `__pycache__/` byproducts are intentionally omitted from the index.

## Reproduce / Refresh

Run from `/home/graehl/agents`:

```bash
rg --files
ls topics/ skills/
for d in skills/*/; do rg -n '^name:|^description:' "$d/SKILL.md" | head -2; done
cat README.md AGENTS.md AGENTS.user.md AGENTS.claude.md GLOSSARY.md
cat topics/agentctl.md topics/provenance-tracking.md topics/agent-instructions.md topics/glossary.md
cat agentctl skills/others/SKILL.md skills/code-map/SKILL.md
wc -l agentctl.py artifact_meta.py agentctl_plugins/aim.py tests/test_agentctl.py
rg -n '^def (start|run_child|status|print_status_state|main|build_parser|add_start_options|watch|wait_job|stop|restart)\b' agentctl.py
rg -n '^def ' agentctl_plugins/aim.py
rg -n '^def (build_meta_markdown|find_aim_run_record|find_aim_run_text)\b' artifact_meta.py
find .agentctl/active -maxdepth 1 -type f          # convention register, not job state
rg -n 'active' agentctl.py                          # confirms --active is a --running-only alias
```
