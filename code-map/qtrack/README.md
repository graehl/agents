# Code Map: qtrack

## Orientation

`/home/graehl/qtrack` is not a conventional application repo; it is a
machine-translation baseline tracking repository whose dominant assets are
language-pair data/config snapshots, apex templates, historical run logs, and
score ledgers. The small script layer turns those tracked assets into runnable
experiments: `scripts/run.sh` orchestrates qtrack runs, `scripts/create-apex-from-template.pl`
instantiates a task apex, `scripts/generate-assets.pl` builds per-run assets,
`scripts/generate-new-apex.pl` applies modern training settings, and
`scripts/scan-scores` / `scripts/scan-customizer-stats` append result rows.

This report is a read-only calibration of the `code-map` skill against a
data-heavy repository. It records static/source traversal only; no qtrack shell
workflow script was executed.

## Module Index

| Path | Responsibility | Inputs / Outputs | Key Callers / Callees | Evidence |
|---|---|---|---|---|
| `scripts/run.sh` | Top-level qtrack workflow: update related repos, create apexes/assets, run Sherpa experiments, collect scores/weights, and create reproducibility branches. | In: repo paths, task lists, run type flags, optional run name. Out: `logs/<year>/<month>/`, `apexes/<lp>/<year>/<month>/`, `results/*.txt`, `data/weights/**`, git branches. | Calls `common.sh`, `create-apex-from-template.pl`, `generate-assets.pl`, `generate-new-apex.pl`, `scan-scores`, `scan-customizer-stats`, CT/XMT tooling, and git. | verified: `sed -n '1,760p' scripts/run.sh` |
| `scripts/common.sh` | Shared shell logging and fatal-error helpers. | In: message text. Out: timestamped info lines or process exit. | Sourced by `run.sh`. | verified: `sed -n '1,220p' scripts/common.sh` |
| `scripts/create-apex-from-template.pl` | Replaces template placeholders in `<lp>.apex-template` to create a concrete apex for a run. | In: base dir, language pair, run name, run type, optional prior system, stdin apex template. Out: apex text on stdout. | Called by `run.sh:prepare_lp()`. Reads `results/<lp>.txt` for `<BESTWEIGHTS...>` resolution. | verified: `sed -n '1,180p'` |
| `scripts/generate-assets.pl` | Builds run-local assets for one language pair. | In: base qtrack dir, language pair, experiment name. Out: `<name>.assets/<lp>/` plus policy files and source/target/task asset copies. | Called by `run.sh` when an apex references `<NAME>.assets`; feeds `generate-new-apex.pl`. | verified: `sed -n '1,220p'` |
| `scripts/generate-new-apex.pl` | Applies `training-settings.yml` to an apex, normalizes settings names, expands NMT trainer options, resolves file-piece includes, and writes a modernized `.new.apex`. | In: apex file and assets dir. Out: `<apex>.new.apex` plus generated basis files when multiple file pieces apply. | Called by `run.sh` after asset generation; uses `scripts/Tiny.pm` / `YAML::Tiny`. | verified: source reads of parser, settings, and writer functions |
| `scripts/Tiny.pm` | Vendored small YAML reader/writer implementation. | In: YAML strings/files. Out: Perl data structures or YAML text. | Used by `generate-new-apex.pl` as `YAML::Tiny`. | verified: `rg` function inventory |
| `scripts/scan-scores` | Extracts DEV/TEST BLEU and Q2 speed rows from completed experiment directories. | In: experiment name and optional test set. Out: score-row text for `results/<lp>[.<set>].txt`. | Called by `run.sh:run_lp()` for each detected eval set. | verified: `sed -n '1,220p'` |
| `scripts/scan-customizer-stats` | Extracts customizer memory/time/grammar/tmpdir stats. | In: run name and optional `--print-header`. Out: stats table rows. | Called by `run.sh` for customized systems. | verified: `sed -n '1,220p'` |
| `scripts/qtrack-helper.sh` | Operator helper for selecting old baselines/retunes and checking whether templates reference qtracked weights. | In: command such as `report_last` or `suggest_next`. Out: suggested task flags or status lines. | Reads `results/*.txt` and `apexes/<lp>/<lp>.apex-template`. | verified: `sed -n '1,220p'` |
| `scripts/find_nnmodel_apex.sh` | Backtracks neural-model references in apex templates to likely source apex files. | In: optional task-name filter. Out: per-task model/apex lookup report. | Reads `apexes/*/*.apex-template` and model paths. | verified: `sed -n '1,160p'` |
| `scripts/consolidate.py` | Copies external model/training assets into `/lwdata2/mt-models/for-qtrack` and rewrites templates to stable paths. | In: `--template` path. Out: rewritten template plus copied asset trees. | Standalone migration/consolidation helper; uses `subprocess.run(shell=True)`. | verified: `sed -n '1,260p'` |
| `apexes/<lp>/<lp>.apex-template` | Reproducible experiment template per language pair/task. | In: placeholders like `<NAME>`, `<LP>`, `<TYPE>`, `<BESTWEIGHTS...>`. Out: concrete apex under `apexes/<lp>/<year>/<month>/<name>.apex`. | Consumed by `create-apex-from-template.pl`; updated by qtrack branch commits. | verified: representative `apexes/eng-ger/eng-ger.apex-template` |
| `data/common`, `data/<src>-SRC`, `data/<trg>-TRG`, `data/<lp>` | Shared, language-side, and task-specific asset/config pools. | In: tokenizers, rules, filtering specs, policies, dev/test/rc files, weights. Out: copied run assets under `<name>.assets/<lp>/`. | Consumed by `generate-assets.pl` and referenced from apex templates. | verified: `find data ...`, representative reads |
| `data/common/training-settings.yml` | Concept-grouped settings overlay for modernized apexes. | In: include/exclude selectors and `apex-settings`. Out: apex setting changes and generated basis files. | Parsed by `generate-new-apex.pl:readTrainingSettings()`. | verified: representative read |
| `data/weights/<lp>/<year>/<month>/` | Stored final weights from successful qtrack runs. | In: `weights.file.final*` copied from experiments. Out: qtracked weight references for future baselines/retunes. | Written by `run.sh:store_final_weights_files()`; read by template placeholders. | verified: `run.sh` source and file inventory |
| `results/*.txt` | Score ledger per language pair/task/test set. | In: rows from `scan-scores` and manual notes. Out: baseline/retune history and `<BESTWEIGHTS...>` lookup source. | Read by `create-apex-from-template.pl` and `qtrack-helper.sh`; appended by `run.sh`. | verified: representative `results/eng-ger.txt` |
| `logs/<year>/<month>/` | Historical run logs and phase sentinels. | In: qtrack run output, repo status reports, git diffs, `*.DONE` phase markers. Out: resumable run state and reproducibility evidence. | Written by `run.sh` phases. | verified: `git ls-files` counts and `run.sh` source |

## Flow Slices

### Baseline Run Orchestration

1. `scripts/run.sh` parses task flags (`--baseline`, `--retune`,
   `--rerescore`, `--reeval`, release modes, `--learnnmt`) and normalizes comma
   lists into task sets.
2. It creates or resumes a run name, records `logs/running.log`, checks related
   repo paths, pulls/updates CT/XMT/XMT-externals, and refreshes binaries when
   requested.
3. For each task, `prepare_lp()` creates a concrete apex, creates run assets,
   applies modern training settings, and writes a per-task log with recent repo
   commits.
4. `run_lp()` submits the apex to Sherpa, verifies completion markers, extracts
   score rows, stores final weights, records system paths, and touches per-task
   `DONE` markers.
5. After all tasks complete, `run.sh` writes git diff files, creates branches in
   related repos, stages qtrack results/apexes/weights/logs, and optionally
   pushes reviewable changes.

Seams: task selection and phase control in `run.sh`; apex content in
`apexes/<lp>/<lp>.apex-template`; scoring extraction in `scan-scores`; weight
storage in `store_final_weights_files()`.

Evidence: verified by source reads of `run.sh`, `scan-scores`, and
representative `results/eng-ger.txt`.

### Apex Instantiation

1. `run.sh:prepare_lp()` chooses the destination apex path and finds the prior
   baseline system for non-baseline run types.
2. It pipes `apexes/<lp>/<lp>.apex-template` into
   `create-apex-from-template.pl`.
3. `create-apex-from-template.pl` substitutes run placeholders and resolves
   `<BESTWEIGHTS...>` by scanning `results/<lp>.txt` for the best or latest
   matching baseline row.
4. The generated apex is sanity-checked for a section matching
   `[<name>.<lp>.<type>]`.

Seams: placeholder syntax in templates; score-ledger row format in
`results/*.txt`; best-weight resolution logic in `create-apex-from-template.pl`.

Evidence: verified by source reads of `create-apex-from-template.pl` and
`apexes/eng-ger/eng-ger.apex-template`.

### Asset And Modern Apex Generation

1. `generate-assets.pl` copies `data/common`, source-language assets,
   target-language assets, and task-specific assets into
   `<name>.assets/<lp>/`.
2. It rewrites policy files so asset paths point at the generated assets
   directory.
3. `generate-new-apex.pl` reads the concrete apex, preserving section/parameter
   order while normalizing old setting names such as `hadoop_cluster`.
4. `readTrainingSettings()` applies included `apex-settings` from
   `training-settings.yml`, optionally composing multi-piece config files via
   generated `basis:` files.
5. `writeApex()` suppresses inherited duplicate settings and writes the
   modernized apex.

Seams: concept-grouped setting overlays in `data/common/training-settings.yml`;
asset copy rules in `generate-assets.pl`; inheritance and include/exclude logic
in `generate-new-apex.pl`.

Evidence: verified by source reads and representative `data/common/training-settings.yml`.

### Score And Stats Capture

1. `run_lp()` locates evalresult files for each completed system and test set.
2. `scan-scores` chooses dev/test/lcBLEU/Q2 values from tuning, rescore, and
   eval directories, filling `XX.XX` sentinels when data is missing.
3. `run_lp()` validates that scores contain the run name and, for non-customized
   systems, rejects rows containing `XX`.
4. Score rows are appended to `results/<lp>[.<set>].txt` only if the run name is
   not already present.
5. Customized systems route to `scan-customizer-stats` and
   `results/<lp>.stats`.

Seams: `scan-scores` row formatting; `results/*.txt` headers and run-name
deduplication; customizer stats schema.

Evidence: verified by `scan-scores`, `scan-customizer-stats`, `run.sh`, and
representative `results/eng-ger.txt`.

### Asset Consolidation

1. `consolidate.py --template <path>` scans a template for path-valued
   settings.
2. Parameters are classified into `BACKUP`, `TRAINING`, and `IGNORE` sets.
3. Known model/config/training paths are copied into
   `/lwdata2/mt-models/for-qtrack/<template-prefix>/<param>/...`.
4. The template is rewritten to stable copied paths after commands complete.

Seams: the parameter classification sets in `consolidate.py`; destination root
constant; shell command construction.

Evidence: verified by source read of `scripts/consolidate.py`.

## Contracts And Seams

- Qtrack's durable truth is split by artifact family: templates under
  `apexes/`, assets under `data/`, scores under `results/`, logs under `logs/`,
  and operational logic under `scripts/`. This differs from app repos where a
  module index mostly names code files. Evidence: verified by `git ls-files`
  counts: `data` 5297, `logs` 5018, `apexes` 3194, `results` 1776,
  `scripts` 13.
- `results/*.txt` row format is load-bearing: it is both human score history
  and machine input for `<BESTWEIGHTS...>` template resolution. Evidence:
  verified by `create-apex-from-template.pl` and representative
  `results/eng-ger.txt`.
- `run.sh` is intentionally high-effect: it can pull repos, compile/update
  binaries, submit Sherpa jobs, write qtrack artifacts, create branches, commit,
  and push. A code-map refresh should not execute it casually. Evidence:
  verified by `run.sh` source.
- `training-settings.yml` centralizes modern settings overlays across many
  language pairs. The include/exclude logic is a key edit seam because it lets
  one conceptual setting section apply to source-side, target-side, or
  task-specific assets. Evidence: verified by `generate-new-apex.pl` and
  representative training-settings read.
- `scripts/consolidate.py` has intentionally external side effects into
  `/lwdata2/mt-models/for-qtrack`. Treat it as an operator migration tool, not
  a harmless analyzer. Evidence: verified by source read.

## Blind Spots

- No qtrack scripts were executed. The report is static traversal only.
- There are no root `AGENTS.md`, `AGENTS.local.md`, `CLAUDE.md`, `README.md`,
  or `GLOSSARY.md` files visible in this checkout during the quick check.
- The first raw `rg --files` output was enormous, so traversal intentionally
  narrowed away from exhaustive `data/`, `results/`, `apexes/`, and `logs/`
  listings. Representative files were read instead.
- External CT/XMT/XMT-externals behavior, Sherpa execution, `/lwdata2`
  filesystem effects, and git branch/push side effects were not observed.
- `scripts/Tiny.pm` is treated as a vendored YAML parser; its internals were
  inventoried but not behaviorally audited.

## Reproduce / Refresh

Run from `/home/graehl/qtrack` with login-shell startup disabled if the current
sandbox cannot write `/home/graehl/.condarc`:

```bash
git status --short --branch --untracked-files=all
rg --files -g '!data/**' -g '!results/**' -g '!apexes/**' -g '!logs/**'
find scripts -maxdepth 2 -type f -print | sort
find data -maxdepth 2 -type f \( -name 'README*' -o -name 'filtering_spec' -o -name 'training.spec' -o -name 'training-settings.yml' -o -name 'policy.yml' \) -print | sort | head -120
find apexes -maxdepth 2 -type f -name '*template*' -print | sort | head -80
rg -n "^(sub|def|class) |^use |^import |^from |argparse|OptionParser|GetOptions|if __name__|main\(|^function " scripts
sed -n '1,760p' scripts/run.sh
sed -n '1,430p' scripts/generate-new-apex.pl
sed -n '1,260p' scripts/consolidate.py
sed -n '1,220p' scripts/generate-assets.pl
sed -n '1,180p' scripts/create-apex-from-template.pl
sed -n '1,220p' scripts/scan-scores
sed -n '1,220p' scripts/scan-customizer-stats
sed -n '1,220p' scripts/qtrack-helper.sh
sed -n '1,160p' scripts/find_nnmodel_apex.sh
sed -n '1,80p' data/common/training-settings.yml
sed -n '1,140p' apexes/eng-ger/eng-ger.apex-template
sed -n '1,60p' results/eng-ger.txt
git ls-files | awk -F/ '{count[$1]++} END {for (k in count) print count[k], k}' | sort -nr
```
