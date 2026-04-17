# Banner

Immediately say "Global AGENTS understood" after reading all of this.

# Session management

Session state is saved in `last-session.md`. Use `/bye` to save a
summary before ending work, and `/hi` at the start of a new session to
pick up context. `/hi` and `/bye` — that's the whole ritual. Task files in `tasks/` track per-feature progress and
architectural decisions — read the active task file when resuming.

### Resume source priority

When the user provides an extract, handoff, or `continues` resume log from a previous agent session, treat that as evidence that the source session did not successfully run `/bye`. This overrides the normal resume instructions for `last-session.md`: in that situation, `last-session.md` is presumed stale by default and should not be treated as the primary source of truth. Prefer the provided extract or handoff, plus current branch/task state and live artifacts/jobs, over `last-session.md` unless there is explicit evidence that the previous session did in fact update it by completing `/bye` afterward.

## Global authority

`~/agents/AGENTS.md` is the authoritative global instructions file. Repo-local
`AGENTS.md` / `CLAUDE.md` symlinks or copies may point here, but global policy
changes belong in this file first.

Likewise, shared helper scripts under `~/agents/` and `~/bin/` should be kept in
sync when they intentionally mirror each other. When those global instructions or
helper scripts are modified, make a brief commit directly on `~/agents` `master`
so the authoritative copy has a clear history.

### Skills path aliasing (important)

In this environment, `~/agents/skills` and `~/.codex/skills/user` may be two paths
to the same underlying directory (hard-link/bind-like aliasing). Always treat
`~/agents/skills` as the canonical edit target.

Do **not** "sync" these paths by converting one side to symlinks. That can create
self-referential loops (for example `skills/foo -> skills/foo`) and break skill
loading with "Too many levels of symbolic links".

Before any migration or sync operation, verify whether they are the same inode:
`stat -c '%d:%i %n' ~/agents/skills ~/.codex/skills/user`

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

A clear affirmative means alignment — proceed without re-checking unless a
genuinely new ambiguity or risk has emerged.

### "Don't forget" reminders

When the user says `don't forget X` (or similar phrasing), briefly check whether
`X` is already present in the governing global/project/branch instructions or is
only an inferred expectation from the current plan. Report back succinctly:
- where it was already covered, quoting or paraphrasing the closest governing
  phrasing when practical
- or that it was not explicit and should be added if the user appears to want it

When helpful, also say whether `X` would have been independently likely from the
existing instructions and current task direction, or whether the reminder was
surprising enough that an explicit rule is warranted. Do this with judgment; do
not overclaim access to a counterfactual inner state.

### Planning rationale

When the user gives planning or sequencing directions, assume there is often an
implicit claim or justification behind "A before B" that is worth surfacing.
Briefly ponder and suggest the most likely rationale for the ordering or choice,
especially when that rationale would sharpen the plan, expose a hidden tradeoff,
or help the user correct/generalize an unspoken intuition. Keep this brief and
tentative rather than leading: the goal is to elicit or refine the user's real
reasoning, not to force agreement or create confirmation bias.

### Asynchronous questions

Socratic or genuine clarifying questions are allowed when they can improve the
shared understanding of the work, but they must be treated as asynchronous by
default. Do not let such questions stall execution for more than about 30
seconds while awaiting a reply. Assume many of them will go unanswered; if the
question is still worth posing, ask it briefly and continue working. When
helpful, tag the question with a short project-style codename prefix such as
`ORBIT:` or `KEPLER:` so the user can quickly recognize it as an optional
reasoning probe rather than a hard blocker. Do not standardize on one fixed
keyword forever; choose a brief topical codename that fits the question. A
later user reply may still be answering such a codename-tagged question; do not
reject that interpretation merely because of delay. Only treat the reply as
unrelated when the surrounding context makes the intended referent clearly
different.

### Search conventions

`rg` (ripgrep) is installed and should be the default text-search tool. Use
type filters when they help narrow the search, e.g. `rg -t md "pattern" .` to
find text in project Markdown files.

### Project-scope instructions before tools

Before running tools in a repository for the first time in a session, check for
project-scope instruction files in that workspace. At minimum, look for repo-local
`AGENTS.md` / `CLAUDE.md` and any project `README.md` they point to, duplicate, or
explicitly name as an instruction source. Do not assume task files or prior session
state are sufficient substitutes for this initial project-scope instruction check.

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

Log entries go at the **top** (newest first). For each experiment: brief preface
(what and why), the actual command in a fenced block, brief coda with the result.
Update the log whenever the paper's headline conclusion changes.

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

When a paper table cites a numbered or short-named run reference (for example `R17`,
`pm-tau01`, or similar), the research log entry for that run should place the same ref
immediately next to a one-line summary and point at the saved `*.meta.md` artifact when
available. The log should make it easy to go from paper ref -> run summary -> metadata
without scanning prose blocks.

### Research paper conventions

Results tables in `research/<branchname>.md` **must** include:
- The **split** (dev / test / dev-subset) and **N** (number of examples) used for scoring.
  A table row without these is uninterpretable after time passes.
- Training and decode comparisons must also report **wall time**; decode rows must report
  **batch width** whenever more than one request/example was translated concurrently.
  Many methods are attempted speedups, so a result is incomplete unless a future reader can
  place it on the time/performance Pareto frontier.
- Example header: `HF results, chi.dev head-20 (N=20, dev subset), MetricX-24 hybrid-large:`
- For multi-corpus/multi-model comparisons, widen the table; repeated model-identifying
  rows or separator rows are fine as long as direct comparison stays legible.
- When a new model or corpus is added to an existing comparison table, add explicit `TBD`
  placeholders where the not-yet-run numbers belong so the intended comparison surface is
  visible before all runs are complete.
- Stale methods/conditions no longer part of the decision story should be removed from the
  paper and archived to the research log with a note.
- Important paper numbers should carry a human-invisible correlation marker such as an HTML
  comment (`<!-- ref: R17 -->`) so a future reader can align the paper table entry with the
  corresponding research-log run record and saved artifacts.

**What belongs in the paper vs. log vs. task files**:
- Debugging steps, failed commands, environment troubleshooting, and routine
  "plumbing works" sanity checks belong exclusively in `tasks/` files and the
  research log — never in the research paper.
- The paper is a record of findings, not process — strip debugging/testing narrative.
  Exception: a correctness demonstration that is itself a finding (replicable,
  meaningful to an unfamiliar reader) may appear in the paper.
- **`tasks/` files are the canonical location for all research investigations** —
  in-progress, parked, or planned work items live in `tasks/NNN-*.md`. They are
  not committed to the branch and are not public.
- **Research papers must NOT reference `tasks/` files** (non-public). Task files
  may cite the paper; the paper must stand alone.
- **Include a `## Future Work` section** for high-level directions meaningful to
  an unfamiliar reader. Routine follow-ups stay in `tasks/` only.

**Eval split sizing defaults**:
- **Smoke / reject-bad**: `head-20` to `head-50`; no conclusions from these.
- **Pilot / hillclimbing**: dev set; grow slice size as needed for significance.
- **Default test evaluation**: use the first 1,000 lines of the test split (`head-1000`).
  Any improvement detectable only beyond 1,000 test pairs is unlikely to be practically
  meaningful; do not spend compute proving marginal differences at full scale.
- **Final paper revision only**: run the full test split (e.g. 3,334 pairs) once, after
  all method selection is finalized, to confirm the headline result holds at full scale.
  Never use full-test numbers to choose between methods.

**Statistical significance**: when reporting that method A is better than method B,
use bootstrap resampling over per-example scores to establish significance:
- * = p < 0.05, ** = p < 0.01 (two-tailed, 10,000 bootstrap iterations)
- Report: mean_A, mean_B, diff(A−B), p-value, and % of bootstrap samples where A wins
- **Minimum eval N = 200** for any conclusion; head-20/head-50 are smoke-tests only
- Use the full split for final results

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

**PyTorch CUDA allocator — prevent memory over-reservation:**
Always set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.5`
before any PyTorch job — without it the caching allocator holds large VRAM slabs between
jobs, preventing concurrency. `env.sh` sets this; always `source env.sh` or export
explicitly before `nohup` jobs. (The typo `PYTORCH_ALLOC_CONF`, missing `CUDA_`, is silently ignored.)

### GPU utilization and parallelism policy

The GPU is non-shared and must be kept busy with planned work at all times —
without being asked and without churning the repo.

**Keep-busy rule**: Whenever a job finishes (or while one runs and a slot is
free), immediately queue or launch the next planned job. Never leave the GPU
idle between planned jobs. Use `wait <PID>` wrappers with a brief sleep buffer
(~90 s) between sequential jobs to let GPU memory fully release.

**Parallelism rule** — two independent jobs must run simultaneously whenever:
- the running job uses **< 50% of total VRAM**, AND
- a second planned job also fits in remaining VRAM with ≥ 10% headroom.

A single job is acceptable only when it uses **≥ 80% of VRAM** (or ≥ 80%
sustained utilization per `nvidia-smi utilization.gpu`). The 50–80% band is
the trigger zone: find and launch a second job from the plan without asking.

**Operationally**:
1. After any job launch or completion, run `nvidia-smi` and check VRAM.
2. If VRAM < 50%: immediately identify the next independent planned job that
   fits in free VRAM (≥ 10% headroom) and launch it without asking.
3. Two jobs are "independent" if they write to different output directories and
   neither reads the other's in-progress output.
4. Prefer the next *planned* job from the task/research queue; only propose new
   experiments if the queue is exhausted.
5. When chaining via `wait <PID>`, check whether any queued job can be promoted
   to run now in parallel with the current job.
6. When a run finishes, immediately show the user a brief highlight: headline
   result, key metric(s), and 1–2 sample output comparisons. Do not wait to be
   asked.
7. **Verify GPU is in use after every job launch.** After starting a background
   job (direct or via a `nohup` wrapper), wait ~30 s and run `nvidia-smi` to
   confirm VRAM rose as expected. If the GPU stays at 0 MiB, the job silently
   failed — investigate the log immediately and relaunch. Never assume a
   background job succeeded without this check.
8. **Use VRAM-polling waits between chained jobs**, not fixed sleeps.
   Before launching the next job in a chain, poll until VRAM drops below a
   safe threshold (e.g. `while [ $(nvidia-smi --query-gpu=memory.used
   --format=csv,noheader | tr -d ' MiB') -gt 3000 ]; do sleep 15; done`).
   Fixed sleeps are unreliable because child/worker processes can hold GPU
   memory well past the parent's exit.

### Implicitly authorized routine operations and return-from-sidebar liveness

After a sidebar, immediately resume with the previously agreed next step (or its
successor if the sidebar changed the plan). Treat any plan previously proposed and
not contradicted as approved; ask only when two alternatives have meaningfully
different outcomes and comparable expected value. Offer to run independent forks
in parallel when feasible.

Full GPU access is always permitted.

Editing project files always permitted.

Standard (this project) git operations (besides checking in private/.gitignore files eg tasks/), 
standard command-execution plumbing/housekeeping - shell/tee/timeout/kill(processes you launched) - 
always permitted.


### Research artifact metadata

For important saved research outputs, use the output artifact as the anchor:

- `<out>` — primary artifact
- `<out>.meta.md` — compact provenance and summary (written at job completion)
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

**Cleanup:** `artifact_meta.cleanup_running(output)` in Python, or
`write_artifact_meta.py ... --cleanup-running` from the CLI.
`hf-translate.py` calls `cleanup_running` automatically at its normal exit.
For `train-lora.py` and other scripts that don't write `.meta.md`, the agent
cleans up manually after recording results in the research log.

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
- To find all subtask files for a branch:
  `rg -t md -l "Branch: <branchname>" tasks/`

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

For `agentctl` and other long-running waits, do not say `in agentctl wait.`
unless the wait/watch command is still live in this turn and you are actively
using its output as the current control point. If the environment will not
reliably wake you on completion, do not use that phrase.

A resolved wait is not a resting state. Once the watched job finishes or the
relevant idle condition is met, immediately consume that completion and launch
or attach the next already-approved successor in the same turn before giving a
status update.

### Wait watchdog discipline

In this Codex environment, a live PTY does **not** automatically create a new
assistant turn when fresh output appears. Therefore, a bare `agentctl watch`
process is not a sufficient wait primitive by itself. Likewise, a tmux pane
that merely prints status to the screen is useful for the human operator but
does not by itself create a fresh user-input event for the local CLI.

When work is gated on a long-running job, the default wait primitive is:
- the built-in `agentctl wait/watch --heartbeat ...` path first; prefer this
  over ad hoc shell sleep loops when all you need is bounded-latency liveness
  output
- a foreground watchdog process that emits a timestamped poll at least every
  300 seconds and includes `agentctl status`/`list` plus `nvidia-smi`
- explicit PTY polling by the agent at least every 300 seconds while the wait
  is active
- when Codex itself is running inside tmux, a second helper from another shell
  or pane that periodically injects a benign key into the Codex pane so the
  local CLI receives a real tty input event; default to `C-l` unless there is
  a concrete reason to use a different key sequence

Use the helper `~/agents/agent-wait-watchdog` (mirrored as
`~/bin/agent-wait-watchdog`) when you need an external poll block that combines
`agentctl` state with `nvidia-smi`, not as the first-line substitute for the
built-in `agentctl` heartbeat. When Codex is running inside tmux and prolonged
quiescence would be harmful, pair the normal `agentctl` wait/watch path with
`~/agents/agent-tmux-nudge` (mirrored as `~/bin/agent-tmux-nudge`) targeting
the Codex pane. This helper is for synthetic tty input, not for on-screen
dashboards.

Never claim to be waiting on a job after the watchdog or watch PTY has already
resolved. Re-check live state first.

Do not use GPU-idle thresholds for a short sidecar watch if another intended
GPU job is still running. For sidecars, watch the job to completion only; keep
GPU-idle watches for the gating job whose successor truly needs the GPU clear.

If a watched job is no longer running, or the GPU is idle unexpectedly, or an
already-approved successor can now be launched, the wait state is over and must
be consumed immediately in the same turn.

Synthetic heartbeat turns delivered through the current yepanywhere session are
not new semantic user requests. Treat them as liveness nudges for the current
plan. The default text may be `yepanywhere heartbeat`, but session-specific
overrides may use a different configured phrase. On receiving one, immediately:
- re-check the live wait/watch/job/GPU state, including explicit polling of any
  active unified-exec PTY that backs an `agentctl` watch or other foreground wait
- continue the already-approved next step if one exists
- emit a short verified in-session status line even when still waiting, so the
  heartbeat causes visible observable output in the active session/CLI rather
  than only silent internal revalidation
- keep the response terse unless there is a blocker, completion, or new result

Temporary observability rule for `yepanywhere heartbeat`: when a heartbeat turn
causes any action that may become visible in the active CLI session (for
example a status line, a wait/liveness note, or a command-launch preface),
prefix the first such visible output with the code word `PULSE:` so the user
can tell it was heartbeat-related rather than an unrelated spontaneous turn.

### Failure postmortems

When troubleshooting your own failure to comply with instructions, explicitly
cite the AGENTS sections that were likely governing or distorting the mistaken
behavior. This may require post-hoc reconstruction rather than direct access to
the exact activations that produced an earlier turn; say so plainly when
uncertain. Prefer section headers and short quoted phrases over vague
summaries, for example `Long-running commands`, `Wait watchdog discipline`, or
repo-local wait-state rules.

# C++
When reformatting C/C++ changes, use clang-format only on modified lines:
  git diff -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i
Do not run clang-format on entire files.
You can use clangd to check your edits to a C/C++ source file (if a .clangd is present at project root)

# Commits

Composing commit messages: aim for a <=65 char subject, and strictly enforce a 72-column line wrap for the body.
Use `fixup! <subject>` for fold-into-later follow-up commits; do not use `squash!` unless explicitly requested.
For commits made on research branches, include newly resolved findings or newly discovered findings in the commit message whenever that is part of the checkpoint.

**Amend vs. second commit after a correction**: if the user contradicts or
corrects a commit that has NOT yet been pushed to `origin/master`, always
`git commit --amend` (or `git commit --amend --no-edit` for trivial fixups)
so the branch history stays clean and the corrected state is the canonical
record. A second stand-alone commit for a one-line correction adds noise and
can leave a misleading intermediate state in history.

**Push to origin/master only in high-confidence, mechanical scenarios** —
e.g., a passing-test engineering checkpoint where the content is clearly
non-sensitive. Never autonomously push research documents, config changes,
or anything that could contain non-public information without explicit user
confirmation. Once pushed, a corrected amend becomes an unwanted force-push
or requires a second commit — either outcome is worse than waiting.

**Recent pushed oopsies on personal GitHub**: if a pushed commit to the user's
`github.com/graehl` remote is discovered within days to be wrong, and there are
no downstream forks/consumers depending on that erroneous commit, prefer
`git commit --amend` plus a force-push/overwrite so the bad state disappears
rather than accumulating noise-fix history. Exception: do not rewrite once the
branch/commit has already been submitted as a PR elsewhere; in that case, keep
history stable and repair forward unless the user explicitly says otherwise.

# Explanation style: "remind me" / "refresher"

When the user says **"remind me"** or **"refresher"** before a concept or technique,
deliver a self-contained paragraph or short textbook-style section with these properties:

- **Computation-focused**: lead with the core equation, algorithm step, or worked
  micro-example (small concrete numbers). Do not open with historical background.
- **Worked example**: include at least one small numerical or pseudocode illustration
  that a reader can trace by hand in under two minutes.
- **Mnemonic anchors**: give the acronym expansion on first use and the primary
  discoverer's last name + year (e.g., "RSLoRA (Rank-Stabilized LoRA, Kalajdzic 2023)").
- **Assumes deep ML background**: do not explain SGD, attention, tokenization, or other
  standard field concepts unless the reminder is specifically about them. Skip motivation
  sentences the user already knows.
- **Related concepts**: briefly name the 1–3 most closely related techniques the user
  likely knows, so they can cross-reference their own memory (e.g., "contrasts with
  plain LoRA in that…", "same family as DoRA but without…").
- **Length**: one to three paragraphs maximum; tighter is better.
