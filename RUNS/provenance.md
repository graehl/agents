# Run artifacts and provenance

> Rules, schemas, and rationale for in-flight markers, durable run records, saved outputs, and row-wise transforms.

Read this packet before launching tracked work that produces an important saved
output, defining its in-flight record, or accepting a row-wise transformed
dataset. `RUNS.md` is the router and wins on conflict.

## Binding rules

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
The exact template and explicit cleanup forms appear below under the second
“In-flight job tracking (`.running.md`)” heading.

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
`*.meta.md` template and one-level input inheritance rules appear below under
the second “Research artifact metadata” heading.

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


## Retained detail and examples

### Research artifact metadata

For important saved research outputs, use the output artifact as the anchor:

- `<out>` — primary artifact
- `<out>.meta.md` — compact provenance and summary (written by agent-managed
  launch plumbing such as `agentctl`, not by payload scripts)
- `<out>.log` — full stderr/runtime log
- `<out>.running.md` — launch record written by the agent at job start; deleted on clean completion

#### In-flight job tracking (`.running.md`)

**The agent writes `.running.md` immediately when launching a background job.** Scripts
are not responsible for creating or deleting it. This file survives crashes and lets a
resumed agent discover in-flight or interrupted work without reading shell history.

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

**On session resume after a crash:**
1. `ls untracked/*.running.md` (or wherever jobs are launched) to find candidates.
2. For each: `kill -0 <pid>` — if alive, job is still running; tail the log for progress.
   If dead and no `.meta.md` exists, the job was killed mid-run — tail the log for
   partial results and record them informally in the research log.
3. If `.meta.md` exists alongside `.running.md`, the job completed but cleanup was
   skipped — delete the `.running.md`.

**Cleanup:** ordinary operation should not require a manual cleanup step: the
launching agent, or `agentctl` when it owns the launch, removes `.running.md`
after a clean completion. If a reboot, crash, or interrupted cleanup leaves
stale markers and you need a "where were we?" pass, run
`agentctl cleanup-running` with no arguments: it scans the workspace, reports
`running` / `completed` / `interrupted`, and only removes markers that are
clearly completed via adjacent `.meta.md` or `.meta.json`. To delete a known
marker explicitly, run `agentctl cleanup-running <out>` or pass the marker
path directly, `agentctl cleanup-running <out>.running.md`. Payload scripts
should not be expected to create `.meta.md` or clean up `.running.md`; they
produce outputs and may optionally write cooperative run declarations such as
`$AGENTCTL_RUN_DIR/propagate.json`.

`agentctl start --after <job-or-output>` may depend on either an `agentctl`
job or an output path following this `.running.md` convention. The queued job
is visible as `waiting`, but its payload is not launched and output metadata is
not written until all dependencies complete cleanly. Use this only when the
follow-on is mechanically determined; if the next step depends on interpreting
the completed `.meta.md` or output contents, wait and inspect before launching.

Prequeueing the mechanically-determined successor at launch time (eval
after train, decode after cache) is cheap insurance against an agent
dead-stop: if nothing consumes the completion promptly, the GPU still
runs the planned chain and only reporting waits. `--after` gates on
clean exit, but exit 0 is not semantic success: when the successor
should not run on a degenerate result (metrics out of range, truncated
or empty output), put that check in a small standalone guard script
that the successor payload runs first — exit nonzero fails the
successor and stops the chain — rather than shell-quoting a compound
test into the agentctl command line. Results needing real
interpretation still follow the wait-and-inspect rule above.

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

### Run records and provenance

When a project tracks runs through `agentctl`, the canonical run record is the
JSON dump under `runs/aim/<experiment>/runs/<run-id>.json`, using the
`artifact_meta.find_aim_run_record/text` lookup path. Refer to that record
rather than reconstructing run history from logs or `.meta.md` content alone: the
dump carries the structured argv/cwd, declared inputs and outputs, the script
fingerprint, git branch+commit, and any producer-tagged propagation facts.

Output files produced under tracked runs get a `<output>.meta.json` sidecar next
to them, containing `agentctl_run_id` and `run_dump` pointing back at the
producing record. When you encounter an unfamiliar file, check for this sidecar
before assuming it's untracked — following `run_dump` gives you the full
provenance one read away.

Bare `agentctl` invocations throughout this doc assume PATH lookup; when
`command -v agentctl` fails, invoke it via `~/agents/agentctl` (the canonical
absolute path — `./agentctl` will not work from arbitrary project CWDs).

Put stable, non-secret launch defaults that must survive local/remote path
differences in a tracked project-root `agentctl.env`. It is a declarative
`KEY=VALUE` file rather than a sourced shell script; `${AGENTCTL_ROOT}` expands
to the invocation-project root. For example:

```text
PII_EVAL_HOME=${AGENTCTL_ROOT}/untracked/pii-eval
```

Project values only fill missing ambient variables. `--source-env` and then
explicit `--env KEY=VALUE` take precedence. Use `--no-project-env` for an
intentional clean-room launch or `--project-env PATH` to select a different
declarative file. Do not put credentials or other secrets in a tracked project
environment file. Run provenance records its path, SHA-256, and key names,
without recording values; `restart` preserves the original selection.

When `agentctl` is on `PATH`, prefer `agentctl start ... -- <command>` for any
launch you might later need to reproduce, audit, or trace. Two tiers:

- **Tracked launch** (default): writes the full dump + meta sidecars; the run is
  reachable via the runs DB and via filesystem-discoverable back-pointers.
  Declared inputs (`--input KEY=PATH`) get sidecar lookup so the run record
  shows what produced each input one-deep.
- **Trivial launch** (`agentctl start --no-aim ...`): records nothing under
  `runs/aim/`, no sidecars. Useful when the value is just having a tracked
  launcher and an agent-permission boundary (one trusted binary in PATH instead
  of raw shell exec) without paying the dump cost. Per project-local
  run-record policy, trivial janitorial commands do not need Aim records.

Keep multi-stage work as a sequence of those records when stage boundaries
produce independently useful artifacts or require a validity decision. A
monolithic shell command hides which stage failed and makes provenance and
selective restart needlessly coarse. Use `--after` for a successor whose gate
is mechanical; otherwise inspect the predecessor before submitting the next
record. Add `--runtime-estimate` when a useful estimate is available.

When one output path must both reach the payload as `--KEY=PATH` and be
declared for provenance, use `agentctl start ... --output-arg KEY=PATH`. It
performs both operations from one value. Do not repeat the path once in
agentctl's options and again after `--`: the copies can diverge, and agentctl's
plain `--output` is deliberately provenance-only. Keep plain `--output` for
payloads whose output is positional, internally determined, or named by some
other argument.

For the full schema and algorithms (input source resolution, output sidecar
writing, propagation protocol, plugin contract), see
`topics/provenance-tracking.md`. For the agentctl plugin/hook surface
specifically, see `topics/agentctl.md`.

### Verified provenance for row-wise text transforms

Any scripted batch translation, paraphrase, or other text rewrite must carry
stable source identity inside each output row when the format permits it:
dataset/document identity, an explicit `line_1based` or `row_0based` locator,
the source text and hash, Unicode-codepoint input/output lengths, and
`AGENTCTL_RUN_ID`. Prefer this inline envelope over a positional mapping. A
legacy keyed sidecar is acceptable only with exact membership, order, and hash
checks; line position alone is not provenance.

When the transform already has a tokenizer loaded, include source and output
token counts with the tokenizer's immutable revision and special-token
convention; do not save the integer token-ID sequence. Codepoint and token
ratios are complementary for cross-script transforms.

Independently resolve a sample (all rows when cheap) against the original
source and log the checked count. For every such batch, and especially before
accepting an expensive transform, log the configured length-ratio coverage
summary and save the actual source/output pairs that fall outside it for
review. Acceptance uses a policy frozen for the operation/language direction,
not one fitted on the batch under review; same-batch fitting is exploratory and
cannot detect a coherent batch-wide misalignment. Length anomalies are review
signals, not automatic rejection. Use the standard `row-transform/v1`
envelope and reciprocal-symmetric empirical check
in `topics/verified-provenance.md`; the shared implementation is
`run_quality.length_ratio.LengthRatioPolicy`.
