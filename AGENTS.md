# Session management

Session state is saved in `last-session.md`. Use `/bye` to save a
summary before ending work, and `/hi` at the start of a new session to
pick up context. `/hi` and `/bye` — that's the whole ritual. Task files in `tasks/` track per-feature progress and
architectural decisions — read the active task file when resuming.

## Global authority

`~/agents/AGENTS.md` is the authoritative global instructions file. Repo-local
`AGENTS.md` / `CLAUDE.md` symlinks or copies may point here, but global policy
changes belong in this file first.

Likewise, shared helper scripts under `~/agents/` and `~/bin/` should be kept in
sync when they intentionally mirror each other. When those global instructions or
helper scripts are modified, make a brief commit directly on `~/agents` `master`
so the authoritative copy has a clear history.

### Instruction Routing

When the user says something is a `global rule`, `project-level rule`, or `branch
rule`, treat that as an instruction about where the rule must be persisted unless the
user says otherwise:
- `global rule` -> write it to `~/agents/AGENTS.md`
- `project-level rule` -> write it to the repo-local `AGENTS.md`
- `branch rule` -> write it to the branch main task file in `tasks/NNN-<branch>.md`

If the user uses that phrasing, do not leave the rule only in chat state; persist it in
the corresponding authoritative file.

### Confirmation threshold

When the user gives a clear affirmative reply to a proposed approach or policy,
such as `yes`, `yes that's correct`, `sounds good`, or `ok`, treat that as
alignment and proceed. Do not keep re-checking whether we are "on the same page"
unless there is a concrete unresolved ambiguity, a new risk introduced by later
findings, or a choice whose consequences materially changed.

## Task and branch structure

Each **main task** (a significant feature, experiment, or refactor) gets its own
git branch named after the task (e.g., `logit-vs-merge-lora` for task 002). A main
task also owns two companion documents in `research/`:

- `research/<branchname>.md` — the **research paper / design doc**: hypotheses,
  setup, results tables, key findings, open questions. Written to be readable by a
  future agent or human without the full conversation history.
- `research/<branchname>.log.md` — the **running log**: timestamped notes,
  intermediate results, dead ends, decisions. Less polished, more complete.

The main task file itself should explicitly track the branch's acceptance criteria,
implementation steps, and current state, not merely act as a subtask index.

### Research log conventions

Log entries go at the **top** of the file (newest first). Each entry should be
human-readable prose. For experiments or training runs, record **both** the
semantic description (what it is and why) **and** the actual shell command run,
so a future reader can reproduce it without reverse-engineering flags from config
files. Put the command in a fenced code block immediately following the description:

```markdown
### Retrain v2c (seed=999, same config as v2b)

Equal-strength partner to v2b for a clean ensemble test. Same r=16, alpha=32,
rslora, 15ep — only seed differs (999 vs 123).

```bash
CUDA_VISIBLE_DEVICES=0 conda run -n edge python train-lora.py \
  -m Qwen/Qwen3-0.6B --system "Translate Chinese to English." \
  -Q chi.dev -R eng.dev \
  --lora-rank 16 --lora-alpha 32 --rslora 1 \
  --num-train-epochs 15 --seed 999 \
  -o untracked/0.6B-chieng-lora-r16-v2c
\`\`\`
```

If a command was not recorded at the time and must be reconstructed, note that
explicitly: `(reconstructed from adapter_config.json / task notes — not verified
as the verbatim original)`.

Do NOT log commands that were never actually run, or future plans disguised as
past runs. The log is a factual record.

Keep research-log analysis/commentary minimal. Prefer a short factual interpretation after
the commands and bottom-line results, and update the log whenever the branch paper's
headline conclusion changes so the two remain consistent.

For run/experiment entries, include a brief factual preface before the command saying what
the run is and why it is being done, then a brief factual coda after the command with the
bottom-line result or interpretation. Do not leave raw commands unexplained, but do not
expand the preface/coda into long narrative analysis.

When a paper table cites a numbered or short-named run reference (for example `R17`,
`pm-tau01`, or similar), the research log entry for that run should place the same ref
immediately next to a one-line summary and point at the saved `*.meta.md` artifact when
available. The log should make it easy to go from paper ref -> run summary -> metadata
without scanning prose blocks.

### Research paper conventions

The research paper should stay pruned, current, and accurate throughout the work so it
remains the human-readable branch summary rather than an append-only dump of stale notes.

Results tables in `research/<branchname>.md` **must** include:
- The **split** (dev / test / dev-subset) and **N** (number of examples) used for scoring.
  A table row without these is uninterpretable after time passes.
- Example header: `HF results, chi.dev head-20 (N=20, dev subset), MetricX-24 hybrid-large:`
- If the same table mixes splits or Ns, add a column for them.
- When showing tables to the user in chat, prefer layouts that remain legible in a terminal
  while still being valid Markdown tables. Favor short headers, compact wording, and only
  the columns needed for the current decision.
- When comparing methods across multiple corpora and models, widen the table with additional
  corpus columns and add additional row blocks for each model. It is acceptable to render
  this as one table with repeated model-identifying rows, spacing rows, or separator rows,
  as long as the direct comparison remains legible in plain Markdown.
- When a new model or corpus is added to an existing comparison table, add explicit `TBD`
  placeholders where the not-yet-run numbers belong so the intended comparison surface is
  visible before all runs are complete.
- Keep the paper pruned to informative direct comparisons and the actual hill-climbing /
  decision story. Methods or conditions that are no longer part of that story should be
  removed from the paper and archived to the research log with a short note saying they
  were removed from the paper and why.
- Important paper numbers should carry a human-invisible correlation marker such as an HTML
  comment (`<!-- ref: R17 -->`) so a future reader can align the paper table entry with the
  corresponding research-log run record and saved artifacts.

**Statistical significance**: when reporting that method A is better than method B,
use bootstrap resampling over per-example scores to establish significance:
- * = p < 0.05, ** = p < 0.01 (two-tailed, 10,000 bootstrap iterations)
- Report: mean_A, mean_B, diff(A−B), p-value, and % of bootstrap samples where A wins
- Do NOT claim ordering without significance markers — N=20 is almost never sufficient
- **Minimum eval N = 40** (head-20 is only a smoke-test during development, never for conclusions)
- Prefer N ≥ 200 for pilot conclusions; use the full split for final results
- LoRA fine-tuning: always train on at least the full dev set (≥1 epoch over all dev examples)

When editing a branch research paper (`research/<branchname>.md`), show the full diff
afterward, eliding only long unchanged stretches if needed to keep the displayed output
within roughly one 70-line screen. Focus the displayed diff on the modified output.

For head-N pilot or smoke-test evaluations, compare against prior full runs by reusing
saved hypothesis outputs or saved per-example score files whenever possible, rather than
re-running old baselines from scratch. Prefer evaluation paths that gracefully handle any
number of lines or expose a `--head` flag so small-slice comparisons remain directly
comparable to earlier full-split runs.

### GPU access for Python ML commands

When working in an ML repo that uses local accelerators, default to running Python
commands with GPU-visible permissions whenever the script might import `torch`,
`transformers`, `unsloth`, `vllm`, TensorRT helpers, or related ML code. This includes
commands that look lightweight such as `--help`, because some scripts import the full
runtime before parsing arguments.

Do not infer "this machine has no GPU" from a sandboxed failure like `torch.cuda` or
`unsloth` accelerator detection returning false. Treat that first as a likely sandbox
GPU-visibility issue. If there is any realistic chance the command will touch the ML
stack, rerun it with GPU-capable permissions instead of continuing with a sandboxed
Python path.

Before launching a GPU job, first confirm whether the GPU appears idle. If GPU use is
already present unexpectedly, warn but proceed when estimated free VRAM still looks
sufficient for the planned job, since this resource is assumed to be single-user. Only
block or change the plan when current use makes the launch materially risky.

### Implicitly authorized routine operations

Do not stop to ask for permission for operations that are already implicitly authorized
by an agreed research or engineering task and that a careful Linux expert would consider
reasonably safe. This includes using GPUs, editing or removing git-tracked files in the
repo, creating files anywhere in the project, editing or removing files the agent
created, running project code or ad-hoc analysis scripts, monitoring processes, killing
processes the agent launched, ordinary shell process composition such as
redirection/backgrounding/`tee`, and similar routine execution needed to carry out the
plan. Do not demand explicit approval for long command prefixes when the underlying
action is already clearly authorized.

### Research artifact metadata

For important saved research outputs, use the output artifact as the anchor:

- `<out>` — primary artifact
- `<out>.meta.md` — compact provenance and summary
- `<out>.log` — full stderr/runtime log

The naming relationship is strict: `.meta.md` and `.log` are formed directly from the
exact output filename. When a run has one primary output, redirect stderr to `<out>.log`.

Always look for `*.meta.md` first. If `write_artifact_meta.py` is on `PATH`, prefer using
it. Otherwise, agents may write the metadata manually using the same structure so later
agents can also parse it.

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

**Dev vs test set discipline**:
- **Dev set**: use freely for model selection, hyperparameter tuning, blend weight search,
  early-stopping decisions, and all iterative exploration. Report dev results as "dev performance."
- **Test set**: run once, after all selection decisions are finalized, to measure generalization.
  Never use test results to choose between methods — that turns test into a second dev set and
  invalidates it as a generalization estimate.
- If dev and test rankings diverge consistently, treat it as a real signal: the model or
  pipeline may be overfitting to dev (too many epochs, too strong LoRA scale, or too many
  blend-weight candidates explored — each candidate counts as a parameter tuned on dev).
- A sweep over K blend weight candidates on dev effectively has K × (dev size) degrees of
  freedom; the resulting "best" may not generalize. Verify with held-out dev subsets or
  accept that test divergence is informative, not a "bad slice."

Eval scripts should output per-example scores (one float per line) so bootstrap
comparisons can be run without re-invoking the model. The eval script should also
support accepting two hypothesis files in one call (single model load) and running
the bootstrap comparison internally. `mbrs_txt.py` supports this via:
  `--compare HYP_B`           score two hyp files + bootstrap in one call
  `--pre-scored A.scores B.scores`  bootstrap from pre-computed score files (no model)
  per-line scores are always printed as `score\thyp` after the summary line

**Subtasks** (NNN-name.md files with `## Branch: <branchname>` header) live in the
same branch as their parent task. They do NOT get their own research/ documents —
all findings go in their task file sections. The parent task's research/ documents
should reference subtask conclusions once resolved.

Not every subtask gets its own file. Minor items may be tracked inline in the main
task file's subtask list and worked on without a dedicated NNN-name.md. The user
will explicitly ask to create a subtask file when one is warranted.

**Rule**: never merge back to main repeatedly for subtasks. Complete or park all
subtask work in the branch, then merge once when the main task is done.

**Commit checkpoints**: commit to the research branch whenever a meaningful checkpoint
is reached — a subtask (inline or explicit) is satisfactorily resolved, an interesting
subtask is newly identified, or a significant finding is recorded. These commits do not
require explicit permission; use judgment and proceed if confident. It is polite to note
"committing now" or ask first when the scope is ambiguous.

**What to commit**:
- `research/<branchname>.md` and `research/<branchname>.log.md` — always commit when
  updated; these are the persistent record of the work.
- Source code changes — commit at checkpoints as above.
- `tasks/` files and `last-session.md` — do NOT commit. These are live working state
  shared among agents via the filesystem directly. Exception: only if the user
  explicitly asks to include them.

**Before committing**: check `git status` and compare untracked/modified file timestamps
against the current and recent sessions. If any source files look like they were created
or meaningfully edited during this work (scripts, notebooks, config files, etc.), ask the
user whether to include them. Handle the response as follows:
- User says **include with this commit**: stage and include.
- User says **no / ignore**: add to `.gitignore` (don't ask again).
- User says **unrelated but add anyway**: add in a **separate commit** with a message
  noting the file's likely purpose and that it was a forgotten/stray file.

### Main task file: subtask tracking section

Every main task file (`tasks/NNN-<branchname>.md`) must contain a **Subtasks**
section that serves as the authoritative list of all work under this branch:

```markdown
## Subtasks

| NNN | Name | File | Status |
|-----|------|------|--------|
| 003 | prompt-consistency-refactor | tasks/003-prompt-consistency-refactor.md | In Progress |
| 004 | trtllm-lora-debug | tasks/004-trtllm-lora-debug.md | Not Started |
| —   | retrain v2c (seed=999) | (inline) | Not Started |

**Last subtask completed** (user confirmed): _(none yet)_
**Last subtask worked on**: 003-prompt-consistency-refactor
**Likely next**: retrain v2c, then 004-trtllm-lora-debug
```

Rules for maintaining this section:
- List every subtask, whether it has its own file or is tracked inline.
- Update `Last subtask completed` only when the user explicitly confirms satisfaction.
- Update `Last subtask worked on` and `Likely next` at the end of each work session
  (i.e., during `/bye`).
- To find all subtask files for a branch, grep:
  `grep -rl "Branch: <branchname>" tasks/`

### Research document paths (derive from git branch name)

The git branch name IS the key. Given branch `logit-vs-merge-lora`:
- Research paper: `research/logit-vs-merge-lora.md`
- Research log:   `research/logit-vs-merge-lora.log.md`
- Main task file: `tasks/NNN-logit-vs-merge-lora.md` (where NNN is the task number)

If on a branch where `research/<branchname>.md` exists, there MUST be a corresponding
`tasks/NNN-<branchname>.md` main task file. If it is missing, alert the user.

When a fresh agent is asked to "update the research log" or "update the research paper",
it should run `git branch --show-current` to get the branch name, then write to
`research/<branchname>.log.md` or `research/<branchname>.md` respectively.

When resuming a session with `/hi`:
1. Read `last-session.md` → active branch name, active task numbers, next step
2. Read `research/<branchname>.md` (paper) for experimental context
3. Read the main task file matching the branch name — check its Subtasks section
4. Read any in-progress subtask files listed in last-session.md
5. Check `research/<branchname>.log.md` for the most recent session's notes

# Long-running commands 
If a command times out:
- Clearly say "Command timed out after X minutes"
- Show the last 100 lines of output
- Show the exact command that was run
- Ask me if I want to increase the timeout or change flags

When running builds or tests, always redirect full output to a log file
(e.g., `make 2>&1 | tee /tmp/build.log`) and show only the tail.
Never discard output with bare `| tail`.


# C++
When reformatting C/C++ changes, use clang-format only on modified lines:
  git diff -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i
Do not run clang-format on entire files.

You can use clangd to check your edits to a C/C++ source file (if a .clangd is present at project root)

Composing commit messages: aim for a <=65 char subject, and strictly enforce a 72-column line wrap for the body.
Use `fixup! <subject>` for fold-into-later follow-up commits; do not use `squash!` unless explicitly requested.
For commits made on research branches, include newly resolved findings or newly discovered findings in the commit message whenever that is part of the checkpoint.
