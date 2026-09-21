# Run artifacts and provenance

> Rules, schemas, and rationale for in-flight markers, durable run records, saved outputs, and row-wise transforms.

Read this packet before launching tracked work that produces an important saved
output, defining its in-flight record, or accepting a row-wise transformed
dataset. `RUNS.md` is the router and wins on conflict.

## Binding rules

For a tracked launch or saved-output lookup, read Research artifact metadata
through Run records and provenance. Row-wise transforms instead activate
Verified provenance for row-wise text transforms and its normative topic;
also read launch rules when launching the transform. The manual templates
below load only for manual marker/metadata authoring or interpretation.

### Research artifact metadata

Anchor an important saved output with:

- `<out>` — primary artifact;
- `<out>.meta.md` — compact human provenance/summary for legacy or manual runs;
- `<out>.log` — full runtime log; and
- `<out>.running.md` — crash-resilient in-flight record, removed after clean
  completion.

#### In-flight job tracking (`.running.md`)

The launching agent or `agentctl` writes the marker immediately; payload
scripts do not own it. Record at least status, PID, start time, cwd/full command,
log, and output. On resume, find markers, use `kill -0` and the log to classify
live versus interrupted work, and treat an adjacent completed metadata sidecar
as stale-marker cleanup. `agentctl cleanup-running` is the canonical sweep.
Use “Manual in-flight marker template” below only when authoring a marker
without launcher support. `agentctl cleanup-running <out>` or an exact marker
path handles explicit cleanup; payload scripts do not own marker removal.

`agentctl start --after <job-or-output>` is for a mechanically determined
successor. Prequeueing eval-after-train is encouraged when exit status is a
sufficient gate. If semantic validity matters, make the successor run a small
standalone guard first; if interpretation is required, wait and inspect instead.

#### Run records and provenance

For tracked `agentctl` work, the canonical record is the JSON run dump under
`runs/aim/<experiment>/runs/<run-id>.json`. Follow an output's
`<output>.meta.json` back-pointer before reconstructing provenance from logs.
The record owns argv/cwd, declared inputs and outputs, script fingerprint, Git
state, and producer propagation.

Declare an input or output at its durable path, not at a fast scratch replica
the payload happens to read or write. Scratch carries only regenerable bytes
(`_RUNS/resources.md`), so a record naming only the replica stops resolving as
soon as that copy is evicted or its host is replaced. When the payload must be
handed the replica path for speed, relocate the artifact and repoint the record
before treating the run as complete.

The default tracked form is also a source-admission gate. It requires a Git
checkout with a committed `HEAD`. `--source-scope non-doc` (the default) rejects
tracked/index changes repo-wide except `*.md` and `runs/aim/**` bookkeeping;
`--source-scope all` includes Markdown. Both reject any non-ignored untracked
`*.py` and verify that the detected or explicit entry script, `agentctl.env`,
each `--source-env` file, and recognized environment controls are byte-identical
to files recoverable from the recorded commit. A selected `.md` script/control
is still fingerprinted. A selected Pixi environment must have both `pixi.toml`
and `pixi.lock`.

Before launch, commit every changed path covered by the chosen scope, every
non-ignored untracked Python source, and every selected script/environment
control. This is the minimal source commit guarantee; a default-scope task or
status Markdown edit need not join it. Queued work repeats the check after its
waits and before the payload starts. A later commit is accepted when its diff
from the recorded commit changes only out-of-scope Markdown/bookkeeping; the
record remains tied to the original source commit. A SHA-256 for bytes absent
from Git is diagnostic evidence of the non-reproducible submission, not
permission to run it.

This is an admission-time observation, not an immutable execution tree. The
source record says `execution_guarantee: admission-time-only` and
`execution_tree: mutable-shared-worktree`: after the last pre-launch check,
the payload runs from the invoking checkout, so a later peer edit or lazy file
read can observe different bytes. Work requiring commit-isolated execution
must invoke `agentctl` from a separately materialized, protected checkout.

This makes an exact Git checkout the normal remote staging unit. An rsynced
source tree without `.git`, or one changed after checkout, cannot launch a
tracked experiment. Named data inputs may remain outside Git, but declare them
with `--input`/`--input-hash` and follow their project-specific provenance
contract. `--no-aim` bypasses this source gate and is therefore unsuitable for
evidence-producing work.

The checkout rule governs source-controlled bytes, not realized runtime state.
Derived environments such as `.pixi/` may remain unchecked-in when a standard
Git ignore/exclude rule hides them and the manifests/locks that define them are
committed. Likewise, intermediate data and artifacts may remain unchecked-in
under their ordinary declared-input/output and sidecar provenance. The
untracked-Python tripwire applies only to non-ignored/non-excluded paths.

Machine context is best-effort and nonblocking: the record may include
hostname, architecture, kernel, OS/distro, Python executable/version, GPU
name/UUID/driver/memory, and cloud-init AMI/instance/region fields. Hardware,
image, distro, and OS differences remain ordinary reproduction qualifications,
not launch failures.

Prefer `agentctl start ... -- <command>` for launches that may need audit or
reproduction. Use the default tracked form for research outputs; use
`--no-aim` only for genuinely trivial runs that need launcher/process handling
but no durable run record.

For a multi-stage workflow, prefer one durable run per atomic stage when the
stages have distinct outputs or semantic gates: train, decode, score,
bootstrap, and export are separate records rather than one shell-wrapped
pipeline. Prequeue only mechanically determined successors; when the next
stage depends on interpreting the result, wait and inspect it first. Supply a
runtime estimate when the duration is reasonably predictable so status and
handoff records expose the expected horizon.

Stable non-secret project launch defaults may live in tracked
`agentctl.env`. Ambient variables override it, then `--source-env`, then
explicit `--env KEY=VALUE`. Never put secrets there. When one output path must
both reach the payload as `--KEY=PATH` and be declared for provenance, use
`--output-arg KEY=PATH`; plain `--output` is provenance-only.

Bare `agentctl` assumes PATH lookup; fall back to `~/agents/agentctl`, not
`./agentctl` from an arbitrary project. Full schemas and algorithms live in
`topics/provenance-tracking.md` and `topics/agentctl.md`. The legacy
`*.meta.md` template and one-level input inheritance rules are under “Manual
metadata schema”; read it only when authoring or interpreting that format.
When configuring launch defaults, read `topics/agentctl.md` § Contracts for
the declarative format, `${AGENTCTL_ROOT}`, and project-env override flags.

#### Verified provenance for row-wise text transforms

A batch translation, paraphrase, or other row-wise rewrite carries stable
source identity in each output row when the format permits: dataset/document,
an explicit base-qualified row locator, source text and hash, Unicode-codepoint
input/output lengths, and `AGENTCTL_RUN_ID`. A keyed sidecar is acceptable only
with exact membership, order, and hash validation; row position alone is not
provenance.

When a tokenizer is already loaded, also record token counts, immutable
tokenizer revision, and special-token convention. Independently resolve a
sample (all rows when cheap) against the source, record the checked count, and
save length-ratio outliers. Acceptance uses a policy frozen before the batch;
same-batch fitting is exploratory only. The normative envelope and check are
`topics/verified-provenance.md` and
`run_quality.length_ratio.LengthRatioPolicy`.
Do not save integer token-ID sequences in the envelope. Log the configured
length-ratio coverage and save outlier pairs; anomalies are review signals,
not automatic rejection.

### Manual in-flight marker template

Minimal structure:

```markdown
# In-Flight Job: <out-name>

- status: running
- pid: <PID>
- started: <ISO timestamp>
- log: <path to stdout/stderr log>
- trainlog: <path to structured trainlog, if separate>
- out: <output dir or file path>

## Command
\`\`\`bash
cd <cwd>
<full command>
\`\`\`
```

### Manual metadata schema

The naming relationship is strict: `.meta.md` and `.log` are formed directly from the
exact output filename. When a run has one primary output, redirect stderr to `<out>.log`.

For new tracked runs, prefer the `agentctl` run record and the output
`<out>.meta.json` back-pointer. For legacy or manually managed artifacts,
`*.meta.md` remains a useful compact human summary; if writing one manually,
use the same structure so later agents can parse it.

Use short relative paths inside `*.meta.md`, interpreted relative to that metadata file.

Canonical `*.meta.md` structure:

```markdown
# Run Metadata: <artifact name or short title>

## Output
- out: [<out>](relative/path)
- log: [<out>.log](relative/path)

## Command
```bash
cd <working-directory-used-for-the-run>
<actual command line used to generate the artifact>
```

## Setup
- split: `<split>`
- N: `<N, if known>`
- metric: `<metric, if any>`
- model: `<model, if useful>`
- method: `<method summary, if useful>`

## Result
- <key>: `<value>`

## Machine
- <key>: `<value>`
- <key>: `<value>`

## Related
- <label>: [<path>](relative/path)

## Inputs
### `<code>`
- path: [<path>](relative/path)
- meta: [<path>.meta.md](relative/path)
- (`<code>.output`) out: [<path>](relative/path)
- (`<code>.result`) score-summary: `<headline result>`
- (`<code>.machine`) <key>: `<value>`

## Notes
- <free-form note>
```

Section semantics:
- `## Command` is required when a command generated the artifact. Include the explicit
  `cd ...` and the actual command that was run, not a reconstruction.
- `## Result` is for headline outcomes a human will compare first.
- `## Machine` is for compact machine-generated run stats or parsed summaries that are
  still small enough to keep in the metadata file.
- `## Related`, `## Inputs`, and `## Notes` are optional.
- Under `## Inputs`, use one `### <code>` block per input. Short codenames should be
  explicit when helpful (for example via `--input train=path/to/out`), otherwise derived
  from the filename.
- Inherited input metadata is **one level deep only**. Inline only selected top-level facts
  from the input's own `*.meta.md` (typically `Output`, `Result`, and `Machine`) and prefix
  them with the input codename such as `(<code>.result)`. Do **not** recursively inline the
  input's own `## Inputs`.
- The inherited restatement must not introduce additional `##` headings; reserve `##` for the
  current artifact's top-level sections so simple `^## ` header scans remain reliable.

When updating a research log, link directly to the saved output or its `*.meta.md`.
If a linked artifact is missing later, search first for the corresponding `*.meta.md`,
then by naming convention or distinctive command/log lines.
