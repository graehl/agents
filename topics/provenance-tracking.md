# Provenance tracking

Topic: `provenance-tracking`

A run-launcher / job-tracking system needs to answer:

- *What run produced this output file?*
- *What were this run's inputs, and what runs produced them?*
- *If I want to regenerate this output, what do I need to rerun?*
- *What's been touched (script edited? config swapped?) since the last good run?*

This topic specifies the contract the system implements to answer those
questions. `agentctl` is the reference implementation.

Relationship to `topics/agentctl.md`: provenance tracking is an aspect of
`agentctl`, currently implemented by the `aim` plugin. The `agentctl` topic
documents the process manager and plugin hook API; this topic documents the
cross-cutting provenance contract that sits on top of those hooks. Keep
launcher lifecycle details in `agentctl.md`; keep run-record schema,
sidecar/back-pointer behavior, input ancestry, propagation facts, and
reproducibility boundaries here.

## Why this design

Properties that fall out of the design choices below — useful when judging
whether to extend the system or to introduce something parallel.

- **No workflow DSL.** Agents (or humans) drive orchestration imperatively;
  the runs DB is the durable propagation graph. Workflow languages
  (Snakemake, Make, Airflow, Nextflow, Luigi, dbt) impose strong opinions
  and none fits every research/run case — declining the DSL avoids that
  fight. Reproducibility lives in shell scripts or task files, written in
  a language everyone already speaks.
- **Programs stay naive.** Wrapper-side declaration via
  `agentctl start --input KEY=PATH ...` is the baseline and works for any
  program in any language. A library compliance path is planned for
  cooperating programs (task 002, deferred) but never required.
- **Schema compatibility with existing tooling.** Run dumps are byte-for-byte
  `aim-text-dump-v1`, the same format produced by export-from-live-Aim
  tooling. `import_aim_text.py` and similar consumers work unchanged. The
  plugin never imports the Aim SDK — dumps are JSON, period.
- **One-deep ancestry, walk the rest.** Each run record stores a flat,
  queryable pointer to each input's producing run (`source_run_id`,
  `source_dump`); deeper traces are graph queries against the dump tree.
  Cost is O(N+M) per run for N inputs and M outputs — never exponential.
- **Filesystem-discoverable back-pointers.** `<output>.meta.json` sidecars
  use the same adjacent-to-file convention as the existing `.meta.md` /
  `.log` / `.running.md` family. A fresh agent or human recognizes the
  pattern without onboarding.
- **Plugin architecture sized to the actual extraction.** 9 hooks, all
  optional. The Aim plugin is the first concrete implementation that proved
  the surface; future plugins for different metadata stores or
  domain-specific verbs slot in without touching base.
- **Two-tier: tracked vs trivial.** `--no-aim` opts out of dump writing
  cleanly. `agentctl` remains useful as a tracked-launch tool with state
  recovery for short-lived/janitorial commands without paying the dump cost
  — and as an agent-permission boundary (one trusted binary in PATH instead
  of raw shell exec).
- **Deterministic synthetic identity.** The `aim_run_hash` field is
  `md5(run_id)[:24]` — same width as a real Aim hash, deterministic from
  `run_id`, collision-safe within agentctl-generated dumps. No SDK
  round-trip required to produce records.
- **Reproducibility-grade fingerprinting where it matters.** Scripts are
  always sha256-fingerprinted (small, cheap, edits are exactly what matters
  for "did I change this between runs?"). Inputs and outputs are sha256
  opt-in (large weights tensors are expensive). Git branch + commit
  captured at launch.

## Bounded scope (non-goals stated up front)

- **No workflow DSL.** Agents (or humans) orchestrate steps imperatively —
  `agentctl start` per step, `--depends-on` for declared ordering, the runs
  DB is the durable propagation graph. We are not building Snakemake.
- **No automated dependency discovery.** A step that doesn't declare its
  inputs is a graph leaf — fine for trivial commands. We don't strace, we
  don't intercept opens, we don't parse `--K=V` heuristically.
- **No deterministic replay.** True bit-for-bit reproducibility is the
  containerization problem (nix/docker). We capture enough provenance to
  rerun by hand and to debug *why* outputs differ.
- **No per-program library coupling required.** Wrapper-side declaration
  via `agentctl start --input KEY=PATH ...` is the baseline and works for
  any program. A library for cooperating programs is planned (task 002,
  deferred) but never required.

## Authority model

- **`runs/aim/<experiment>/runs/<ref>.json`** is the canonical branch
  record for tracked runs. The dump format is `aim-text-dump-v1`. Projects
  may commit these dumps as reviewable authority or ignore them as local
  runtime provenance; project-local instructions decide.
- **Live `.aim/`** (when present) is a rebuildable materialized view
  produced by downstream tooling like `import_aim_text.py` from the dumps.
  Live disagrees with text → repair from the text, never the other way.
- **`<output>.meta.json` sidecars** are filesystem-discoverable
  back-pointers from outputs to their producing run record. Tiny (~6
  fields), produced at run completion.
- **One-deep ancestry rule.** Each run record inlines a *bounded snapshot*
  of each input's producer (enough to rerun the producer by hand). It does
  NOT recurse into the producer's own inputs. Walking deeper is a graph
  query against the dump tree.

## Storage layout

```
<project-root>/
├── .agentctl/                          # runtime job state, gitignored
│   ├── jobs/<job>/current.json         # pointer to the latest state for <job>
│   └── runs/<job>/<run-id>/
│       ├── state.json                  # canonical run state (full schema below)
│       ├── exit-status.json            # completion record
│       ├── headline.txt                # one-line agent headline
│       └── run.log                     # stdout+stderr capture
│
├── runs/aim/<experiment>/              # canonical run dumps, gitignored or committed
│   ├── manifest.jsonl                  # one entry per run in this experiment
│   ├── runs/<ref>.json                 # full run record
│   └── texts/<ref>/meta.markdown.md    # human-readable meta snapshot
│
└── <any-output-path>.meta.json         # back-pointer sidecar next to every declared output
```

Output sidecars use the `.meta.json` adjacent-to-file convention to match
the existing `.meta.md` / `.log` / `.running.md` family — a fresh agent
recognizes the pattern without onboarding.

## CLI surface

### Implemented

| Flag | Effect |
|------|--------|
| `--input KEY=PATH` (repeatable) | Declare input + translate to `--KEY=PATH` appended to argv |
| `--input-raw KEY=PATH` (repeatable) | Declare input only, no argv translation |
| `--input-hash KEY=PATH` (repeatable) | Like `--input` plus compute sha256 of the file at launch (opt-in because hashing large weight tensors is expensive) |
| `--output KEY=PATH` (repeatable) | Declare output + write `<path>.meta.json` sidecar at completion |
| `--output-hash KEY=PATH` (repeatable) | Like `--output` plus compute sha256 at completion (cost is paid after the user command finishes) |
| `--script PATH` | Override the heuristic script-detection. Useful when argv has no script-shaped argument (`bash -c '...'`), the heuristic picks the wrong file, or the run hides behind a multi-word launcher (`pixi run script.py`, `conda run -n env python ...`, `nohup ...`). |
| `--propagate-json '{...}'` | Static producer-flagged facts (JSON object) for quoting at the next consumer's input record. Stored in `state.propagate`, folded into each output's `.meta.json` sidecar under `propagate`. Cooperative protocol: programs may write run-time-computed facts to `$AGENTCTL_RUN_DIR/propagate.json` during execution; agentctl merges that file at completion (runtime values override static). |
| `--no-aim` | Skip writing the aim-format dump (run becomes a graph leaf) |
| `--no-meta` | Skip the human-readable launch `.meta.md` (sidecar `.meta.json` is independent) |
| `--experiment NAME` | Group dumps under `runs/aim/<NAME>/` (default: `<job>`) |
| `--tag TAG` (repeatable) | Add tag to run identity |

### Env contract

| Variable | Set by | Read by |
|----------|--------|---------|
| `AGENTCTL_JOB`, `AGENTCTL_RUN_ID`, `AGENTCTL_MODE`, `AGENTCTL_HEADLINE_FILE`, `AGENTCTL_OUTPUT` | Parent agentctl `start` | The user's program (informational) |
| `AGENTCTL_RUN_DIR` | Parent agentctl `start` | The user's program. Programs that want to flag runtime facts for propagation write JSON to `$AGENTCTL_RUN_DIR/propagate.json`; agentctl reads it at completion. |
| `AGENTCTL_PARENT_RUN_ID` | Parent agentctl `start` (set to its own `run_id`) | Child agentctl invocations during this run; they record `state.parent_run = $AGENTCTL_PARENT_RUN_ID` so the dump record carries the link. Inherited automatically — no flag needed for nested-agentctl chains. |

## Run state schema (`.agentctl/runs/<job>/<run-id>/state.json`)

Flat dict of canonical fields. Plugins write under their own keys. Subset
shown; full set documented inline in `agentctl.py:start()`.

```json
{
  "job": "step1",
  "run_id": "20260508T040459Z",
  "launch_name": "step1-0001",
  "serial": 1,
  "mode": "start",
  "status": "finished",
  "started_at": "2026-05-08T04:04:59Z",
  "finished_at": "2026-05-08T04:04:59Z",
  "returncode": 0,
  "pid": 1512853,
  "pgid": 1512853,
  "argv": ["bash", "-c", "...", "--data=/tmp/in.bin"],
  "cwd": "/abs/path",
  "log_path": "...",
  "output_path": "/tmp/out.bin",
  "meta_path": "/tmp/out.bin.meta.md",
  "context_note": "...",
  "depends_on": [],
  "git_branch": "...",
  "git_commit": "...",
  "inputs":  { /* see below */ },
  "outputs": { /* see below */ },
  "script":  { /* see below */ },
  "aim": true,
  "aim_run_hash": "61ee963e8aa0049289d46d58",
  "aim_dump_record": "/abs/path/runs/aim/exp/runs/<rid>.json",
  "experiment": "chain-test",
  "tags": ["agentctl"]
}
```

### `inputs` (per declared input)

```json
"inputs": {
  "config": {
    "path":      "/abs/path/configs/foo.json",
    "realpath":  "...",                              // iff differs (symlink)
    "size":      12345,
    "mtime":     "2026-04-15T22:18:03Z",
    "sha256":    "...",                              // iff --input-hash
    "is_dir":    false,                              // iff true
    "raw":       false,                              // iff --input-raw (no argv translation)

    // Source identity (always present when the input has a producer sidecar):
    "source_run_id":       "20260415T221803Z",
    "source_dump":         "runs/aim/exp/runs/<ref>.json",

    // Automatic one-deep recap, best-effort from the producer's dump:
    "source_experiment":   "exp",
    "source_command_text": "python build_config.py --target=A",
    "source_origin":       "/abs/path/configs/foo.json",   // drift if != path

    // Producer-flagged propagation (verbatim, schema set by producer):
    "source_facts":        { "loss": 0.234, "checkpoint": "epoch-12" }
  }
}
```

All `source_*` keys are flat for aim queryability (`run.params.inputs.<KEY>.source_run_id == "X"`,
`source_experiment == "Y"`, etc.). The recap fields are best-effort: if the
producer's dump can't be read or doesn't have a particular field, it's
omitted. We deliberately do *not* inline the producer's own
inputs/outputs/script-details — those are one DB-read away via
`source_dump`. Walking deeper is a graph query against the dump tree.

`source_facts` is reserved for arbitrary JSON the producer flagged for
quoting at the next consumer. Producer-side support for writing this field
into the sidecar is implemented by `--propagate-json` and
`$AGENTCTL_RUN_DIR/propagate.json` (see Propagation protocol below); the
consumer side reads it verbatim when present.

### `outputs` (per declared output)

At launch, only `path` is set. At completion (in `run_child`), the file is
stat'd and `size`/`mtime` are filled in; the aim plugin's `on_finish`
writes the back-pointer sidecar and records its path.

```json
"outputs": {
  "result": {
    "path":    "/abs/path/output.bin",
    "size":    98765432,                            // at completion
    "mtime":   "...",                                // at completion
    "sha256":  "...",                                // iff --output-hash
    "is_dir":  false,                                // iff true
    "sidecar": "/abs/path/output.bin.meta.json",     // iff sidecar successfully written
    "status":  "missing"                             // iff file did not exist at completion
  }
}
```

### `script`

Auto-detected at launch from `argv` (heuristic: first non-interpreter arg
that's an existing file; fall back to argv[0]). Always sha256-fingerprinted
because scripts are typically small and edits are exactly what
reproducibility cares about.

```json
"script": {
  "path":   "/abs/path/do.translate.sh",
  "size":   1234,
  "mtime":  "...",
  "sha256": "abc..."
}
```

## Dump schema (`runs/aim/<experiment>/runs/<ref>.json`)

Matches `aim-text-dump-v1` — the same shape produced by
`scripts/export_aim_text.py` so dumps written here can be imported via
`scripts/import_aim_text.py` without modification. Top-level structure:

```json
{
  "identity":  {"agentctl_run_id": "...", "experiment": "...", "run_name": "...", "tags": [...]},
  "metrics":   [],
  "params":    { /* see below */ },
  "ref":       "20260508T040459Z",
  "schema":    "aim-text-dump-v1",
  "source":    {"aim_repo": ".", "aim_run_hash": "<24-hex>", "exported_at": "..."},
  "texts":     [{"name": "meta.markdown", "path": "texts/<ref>/meta.markdown.md"}]
}
```

`params` mirrors run state, organized by domain:

```json
"params": {
  "agentctl":   {"job", "mode", "run_id", "headline_file", "output", "step_id"},
  "command":    {"argv": [...], "cwd", "text"},
  "inputs":     { /* same as state.inputs, with flat source_* recap keys */ },
  "machine":    {"git_branch", "git_commit", "pid", "started_at"},
  "meta":       {"format": "artifact_meta.md", "path"},
  "notes":      ["Created by agentctl at launch; ..."],
  "output":     {"log_path", "meta_path", "path", "title"},
  "outputs":    { /* same as state.outputs (declaration; completion stats land here too if dump is reread) */ },
  "related":    {"agentctl-state": "<state.json path>"},
  "request_plan": [],
  "result":     {},
  "script":     { /* same as state.script */ },
  "setup":      {"job", "launch_status", "run_id"}
}
```

The synthetic `aim_run_hash` is `md5(run_id)[:24]` — same width as a real
Aim hash, deterministic from `run_id`, collision-safe within
agentctl-generated dumps. `agentctl_run_id` is the truly authoritative
identifier and the citation key per `~/d/specs/aim-authority.md`.

## Sidecar schema (`<output>.meta.json`)

The back-pointer half of the system. Discovered via filesystem walk
(`<output>.meta.json` next to any declared output). Minimal fields:

```json
{
  "agentctl_run_id": "20260508T040459Z",
  "aim_run_hash":   "61ee963e8aa0049289d46d58",
  "experiment":     "chain-test",
  "run_dump":       "runs/aim/chain-test/runs/20260508T040459Z.json",
  "output_key":     "result",
  "produced_at":    "2026-05-08T04:04:59Z"
}
```

The `run_dump` field is a project-relative path when the dump lives under
the project root, absolute otherwise. The sidecar contains everything a
downstream consumer needs to walk to the producer's full record.

## Algorithms

### Input source resolution

For each `--input KEY=PATH` (or `--input-raw`):

1. Resolve PATH to absolute (no symlink follow yet); record `path`.
2. If a symlink: also record `realpath` (after follow).
3. Stat: record `size`, `mtime`. If directory: `is_dir: true`, recursive
   size, newest mtime in tree.
4. If `--input-hash`: compute sha256.
5. Look for sidecar at `<path>.meta.json`:
   - If found and valid: read `agentctl_run_id` and `run_dump`. Record as
     `source_run_id` and `source_dump` (flat keys).
   - If the sidecar carries a `propagate` field: copy verbatim into
     `source_facts` (arbitrary JSON the producer flagged for quoting).
   - Best-effort open `run_dump`: pull `source_experiment`,
     `source_command_text`, `source_origin` into the input record.
     Skipped silently if the dump is unreadable (e.g. moved, corrupted) —
     the identity keys are still present.
6. If no sidecar: input is a graph-leaf source (preexisting / produced by
   non-agentctl-tracked means); only `path/size/mtime` recorded.

All recap is **one-deep by design**. Walking further (e.g. "what produced
this run's inputs?") is a separate graph query against the dump tree, never
recursive inlining.

### Propagation protocol <!-- assumed -->

For facts the producer wants quoted at the next consumer (e.g. final loss,
selected hyperparameter, computed checkpoint id) — useful when aim's
visualization tools don't follow graph edges to look up upstream facts and
you want grouping/filtering on producer-derived values to work in the
consumer's own dump.

Producer side:
- A flag like `--propagate-json '{"loss": 0.234}'` sets static facts at
  launch, OR
- The program writes `$AGENTCTL_RUN_DIR/propagate.json` during execution
  (computed values from the run); the aim plugin's `on_finish` reads it
  and folds it into the output sidecar's `propagate` field.

Sidecar shape (extended):

```json
{
  "agentctl_run_id": "...",
  "aim_run_hash":   "...",
  "experiment":     "...",
  "run_dump":       "...",
  "output_key":     "...",
  "produced_at":    "...",
  "propagate":      { "loss": 0.234, "checkpoint": "epoch-12" }
}
```

Consumer side (already implemented): `resolve_input_source` reads the
`propagate` field verbatim into `inputs.<KEY>.source_facts`. No schema
imposed; the producer is responsible for choosing what to quote.

### Output declaration and sidecar writing

At launch:
1. Declared outputs are recorded with just `path` (file may not exist yet).
2. The first declared output (or the bare `--output PATH` form) sets the
   primary `output_path` for `.meta.md` linkage.

At completion (`run_child` after `proc.wait()`):
1. For each declared output: stat the file. Record `size`, `mtime`,
   `is_dir`. If missing, record `status: missing` and skip sidecar.
2. Call `on_finish` plugin hook. The aim plugin writes
   `<path>.meta.json` next to each existing output, with the back-pointer
   fields above.
3. Persist final state.

### Script detection

At launch, scan `argv`:
1. Skip args starting with `-` (flags).
2. Skip args whose basename matches a known interpreter (`bash`, `sh`,
   `zsh`, `python`, `python3`, `perl`, `node`, `ruby`, `Rscript`).
3. The first remaining arg that's an existing file is the script.
4. Fallback: argv[0] (if it exists as a file).
5. Always sha256-fingerprint (small files, cheap, very high reproducibility
   value).

User can override with `--script PATH` when the heuristic picks
wrong, when no candidate exists (e.g. `bash -c '...'`), or when a
multi-word launcher hides the actual code (e.g. `pixi run script.py`,
`conda run -n env python ...`).

## Composability

### One-deep, walk the rest

Each run record inlines a small flat recap of each input's producer
(`source_run_id`, `source_dump`, plus the best-effort `source_experiment`,
`source_command_text`, `source_origin`). It does NOT inline ancestors of
those inputs. To trace deeper:

```
this run → inputs.<KEY>.source_dump → load that record → its inputs.<KEY>.source_dump → ...
```

This avoids the exponential blowup that would happen if every run
recursively inlined its full ancestry. Each level is a single dump-file
read.

### Many-to-many is additive, not exponential

A step with N inputs records N flat source recaps. A step with M outputs
writes M sidecars. The cost scales as O(N+M) per run, not O(N×M) or worse.

### Nested agentctl <!-- assumed -->

When an all-in-one script wants per-internal-step records without rewriting
into separate top-level `agentctl start` calls, it can recursively invoke
`agentctl start sub-step-N -- inner-prog ...`. The plan:

1. Outer `agentctl start outer ...` sets `AGENTCTL_PARENT_RUN_ID=<outer-id>`
   in env.
2. Child `agentctl start ...` reads `AGENTCTL_PARENT_RUN_ID` and records
   `state.parent_run = <outer-id>`.
3. Each child gets its own dump record. Outer's record points at children
   via `state.children = [...]` (assembled during outer's lifetime).

DB query "what's inside run X?" becomes trivial. No DSL required.

### Trivial / leaf runs

`agentctl start --no-aim ... -- some-cmd` writes nothing under `runs/aim/`
and writes no sidecars. The run is a graph leaf. Useful when:
- The launch is genuinely trivial (one-off janitorial command)
- The agent benefits from agentctl as a launcher / permission boundary
  without paying the dump cost
- Per project-local run-record policy: trivial commands don't need Aim
  records

## Reproducibility scope

Captured automatically:
- Git branch + commit at launch
- Script path + sha256 (at launch)
- All declared inputs' size/mtime (and sha256 if `--input-hash`)
- All declared outputs' size/mtime at completion (and sha256 if
  `--output-hash`)
- Full argv + cwd + command text

Deliberately not captured (in v1):
- **Env vars.** Projects typically specify env explicitly (via shell
  scripts, conda/venv/pixi activation, or `--env KEY=VALUE`); auto-capture
  rarely earns its keep. May become important if nested-flow scenarios
  emerge that need to inherit parent env, but agent-driven orchestration
  hopefully sidesteps the need entirely. Addable later via a hook if a
  concrete case justifies it.
- Kernel version, GPU model, library versions. Out of scope; could be
  added to `params.machine` cheaply if needed.
- Process tree, syscalls, opened files. Out of scope.
- Bit-for-bit input/output equality. Use `--input-hash` / `--output-hash`
  for content fingerprints; bit-for-bit replay is the
  containerization/nix problem.

## Conventions

### `<file>.meta.json` family

Sidecars use the existing `.meta.md` / `.log` / `.running.md` adjacent-file
convention. A fresh agent or human dropping into a directory recognizes
the pattern instantly. The directory-clutter cost is real but standard
remediation (extension filtering) handles it.

### `runs/aim/` vs `research/aim/`

`runs/aim/` is the current canonical dump root. `research/aim/` is searched
as a back-compat fallback by `artifact_meta.find_aim_run_record` /
`find_aim_run_text`. New writes always go to `runs/aim/`. Migration of
existing `research/aim/` artifacts is per-project (see
`tasks/003-d-migration.md`).

Projects decide whether `runs/aim/` is committed or ignored. Research repos
may treat it as git-reviewed text authority; operational repos may treat it
as disposable local provenance. `AGENTCTL_AIM_READ_ROOTS` may specify a
pathsep-separated read-only root list during migrations or unusual layouts.
Writes remain single-target and canonical.

### KEY extensibility

`--input KEY=PATH` keys are user-chosen labels. The dict-of-keys structure
(rather than a fixed enum or positional list) lets each project invent
labels meaningful in its domain (`lora_adapter`, `validation_universe`,
`train_split`) without us pre-defining a vocabulary or shipping schema
changes.

### `aim_run_hash` is synthetic

Derived as `md5(run_id)[:24]`. Same width as a real Aim hash so the schema
field stays valid, but reproducible from `run_id` so collisions within
agentctl-generated dumps are impossible. Real Aim hashes (assigned by the
SDK) live in a separate space; in dumps that mix both, treat
`agentctl_run_id` as authoritative.

## Plugin contract

The provenance system is implemented as the `aim` plugin (see
`topics/agentctl.md` for the plugin loader and hook surface). Hooks the
`aim` plugin uses:

- `register_args` — adds `--no-aim` / `--experiment` / `--tag`
- `default_output_path` — supplies `<run_dir>/run` when user doesn't pass `--output`
- `on_start` — sets `state.aim`, `state.experiment`, `state.tags`,
  `state.aim_run_hash`; injects `AIM_EXPERIMENT` / `AIM_RUN_NAME` env
- `on_meta_built` — writes the dump record + manifest + meta-text snapshot
- `on_status_print` — adds `aim=<hash>` to status one-liner
- `on_finish` — writes per-output `<path>.meta.json` sidecars
- `on_note` — updates the dump record's `analysis-summary` and notes
- `on_restart` — reconstructs declared inputs/outputs/experiment/tags

A second plugin (e.g. for a different metadata system) could provide
parallel implementations of these hooks; the base is plugin-agnostic.

## What's next <!-- assumed -->

Concrete planned work, in rough order of priority:

1. Compliance library (task 002) — Python module + JSON sidecar protocol
   for cooperating programs to declare their own I/O without wrapper-side
   listing.
2. Env auto-capture, *if* nested-flow scenarios end up needing parent-env
   inheritance and agent-driven orchestration doesn't obviate it.
3. Per-output propagate (different `propagate` blocks per declared output
   instead of one shared block per run) — only if a real case shows up
   where outputs of the same run need different facts attached.

Each is a small extension; none requires re-architecture.

## Status

<!-- verified: smoke test 2026-05-08 -->
Verified end-to-end in `~/agents`:

- Two-step chain: step 1 produces output → step 2 declares step 1's output
  as input → step 2's record contains flat `source_*` recap keys (run_id,
  dump, experiment, command_text, origin) pointing back at step 1's dump.
- `--input-hash` / `--output-hash`: sha256 computed at launch / completion
  respectively; visible in `state.inputs.<KEY>.sha256` and
  `state.outputs.<KEY>.sha256`.
- `--script PATH`: explicit override fingerprints the named file regardless
  of argv shape.
- `--propagate-json '{...}'`: static facts flow through to each output's
  `.meta.json` sidecar under `propagate`, then into the next consumer's
  `inputs.<KEY>.source_facts`.
- `$AGENTCTL_RUN_DIR/propagate.json`: cooperative file written by the
  program during execution is merged into `state.propagate` at completion
  (overrides static values), then propagates as above.
- Nested agentctl: child invocation under a tracked outer run records
  `state.parent_run = <outer-run-id>`; verified via `AGENTCTL_PARENT_RUN_ID`
  env propagation.
