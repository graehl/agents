# Session management

Session state is saved in `last-session.md`. Use `/bye` to save a
summary before ending work, and `/hi` at the start of a new session to
pick up context. `/hi` and `/bye` — that's the whole ritual. Task files in `tasks/` track per-feature progress and
architectural decisions — read the active task file when resuming.

## Task and branch structure

Each **main task** (a significant feature, experiment, or refactor) gets its own
git branch named after the task (e.g., `logit-vs-merge-lora` for task 002). A main
task also owns two companion documents in `research/`:

- `research/<branchname>.md` — the **research paper / design doc**: hypotheses,
  setup, results tables, key findings, open questions. Written to be readable by a
  future agent or human without the full conversation history.
- `research/<branchname>.log.md` — the **running log**: timestamped notes,
  intermediate results, dead ends, decisions. Less polished, more complete.

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

### Research paper conventions

Results tables in `research/<branchname>.md` **must** include:
- The **split** (dev / test / dev-subset) and **N** (number of examples) used for scoring.
  A table row without these is uninterpretable after time passes.
- Example header: `HF results, chi.dev head-20 (N=20, dev subset), MetricX-24 hybrid-large:`
- If the same table mixes splits or Ns, add a column for them.

**Statistical significance**: when reporting that method A is better than method B,
use bootstrap resampling over per-example scores to establish significance:
- * = p < 0.05, ** = p < 0.01 (two-tailed, 10,000 bootstrap iterations)
- Report: mean_A, mean_B, diff(A−B), p-value, and % of bootstrap samples where A wins
- Do NOT claim ordering without significance markers — N=20 is almost never sufficient
- Prefer N ≥ 200 for pilot conclusions; use the full split for final results

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

