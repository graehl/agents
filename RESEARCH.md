# RESEARCH supplement

This file is loaded when research-task indicators are present. It captures
research method, documentation discipline, and branch/task research workflow.

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

For a paper-specific related-work catch-up, prefer a companion artifact folder
next to the paper: `research/<paper-name>/related-work/` for
`research/<paper-name>.md`. Put a small fetch/extract script there that
recreates the PDF/HTML/markdown extraction cache for cited papers. The generated
markdown/text output is a valuable `rg` search target for finding method,
threat-model, limitation, and table sections before reading them carefully.
Commit the script and lightweight notes when useful; normally ignore downloaded
PDFs, model caches, and generated extraction outputs unless the project
explicitly wants vendored sources.

Do not let extracted markdown become citation-orphaned text. The related-work
script should also create a lightweight metadata manifest for every paper key,
morally equivalent to a BibTeX entry plus source URL: stable key, title,
authors, venue or preprint server, year/date, DOI/arXiv/OpenReview/ACL/etc.
identifier when available, PDF URL, fetched/extracted timestamp, and extraction
tool/version. Prefer one repo-readable file such as `papers.bib`, `papers.yaml`,
or per-paper markdown front matter that can be regenerated alongside the
extracts. The paper can still hand-format citations, but the artifact folder
must preserve enough metadata for a future agent to reconstruct exact
bibliography entries without re-searching the web.

When the candidate related-work list grows beyond about eight papers, tier the
artifact folder and fetch/extract script. Fully extract the high-value tier:
papers with suspected proposal overlap, directly applicable methods, or likely
threat-model lessons. Leave peripheral/background papers on demand until a
comprehensive pass needs them. Make the tiering explicit in the paper or
companion notes, because `rg` over generated markdown/text only searches papers
that have actually been extracted; expand the extraction tier before claiming
coverage across the whole bibliography.

### Field surveys and frontier mapping

Two companion templates cover field-survey work:
- `survey-field.md` — building and maintaining a field map for a survey
  paper/presentation, or prior-art reconnaissance on a subtopic.
- `research-frontier.md` — void-mapping and capstone-question suggestion
  built on top of a field map.

Load them (repo root first, then alongside this file in `~/agents/`) when
the task is to survey a field, gather prior art before planning a solution,
or rank unexplored research directions. If a triggered file is missing,
report once and continue.

Field surveys are standalone, cross-branch reference material under
`surveys/<field-slug>/`, not branch-scoped `research/` artifacts. When a
`surveys/<field-slug>/` covering a paper's field exists, the paper's
related-work should **reference and extend that shared survey's
`related-work/` extraction artifacts** rather than maintain a private
duplicate. Keep a per-paper `research/<paper-name>/related-work/` only when
no `surveys/` subdir covers the field, or for the paper-specific
overlap tier (suspected proposal-overlap papers) that does not belong in a
general field survey. A paper that draws on a survey should cite the
`surveys/<field-slug>/` path so a future agent can find the shared map.

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
  research log until they produce a legitimate publication-facing insight.
- The paper is a record of findings, not process — strip debugging/testing narrative
  from claim-bearing sections. Exception: a correctness demonstration that is
  itself a finding (replicable, meaningful to an unfamiliar reader) may appear in
  the paper.
- **`tasks/` files are the private control plane for research investigations** —
  in-progress, parked, or planned work items live in `tasks/NNN-*.md`. They are
  not committed to the branch and are not public. Durable conclusions belong in
  the paper or an appropriate committed `topics/` doc once they are more than
  private direction-setting.
- Working research-paper drafts may temporarily include a brief plan note or
  related-task pointer when it improves navigation for active collaborators. Mark
  such text as draft/navigation scaffolding and keep it short; do not let it carry
  the actual investigation detail, which belongs in `tasks/` and the research log.
  The final/submission-prep phase must remove these task references so the paper
  stands alone. The precise pre-submittal cleanup gate can be defined later for
  each project.
- When a task governs a research paper, keep the task file as a summary and
  control plane: point to the paper, summarize the current framing or acceptance
  state, and note what session learnings should be synced into the paper when
  applicable. Do not duplicate whole paper sections into the task file; that
  creates two divergent sources of truth.
- **Published intake/split recipes must NOT reference private paths** such as `/private-mount`
  or other local-only mounts. Paper-facing recipes must point at public sources,
  checked-in scripts, or explicitly named non-public prerequisites instead.
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

### Reporting eval conditions precisely

When summarizing a research run, eval result, or claimed "gate", report the
data conditions explicitly rather than relying on branch-local shorthand such as
"dev200 gate" or "same-pool" alone.

At minimum, state:
- train corpus / split / head-N (or full-N) actually used for fitting
- epoch ceiling and whether early stopping or schedule exhaustion determined the
  final checkpoint
- early-stopping / model-selection corpus, including exact split, head-N, and
  whether it was fixed-explicit or derived from train
- decode / evaluation corpus, including exact split, head-N, and whether it is
  the same pool as the early-stopping set or a disjoint slice
- score/reference corpus when separate from the decode inputs
- overlap status among train, early-stop, and eval sets, especially when any
  quoted result comes from the same pool used for checkpoint selection

For quick train-smoke checks, say explicitly that the decode/eval examples came
from the training split and that such numbers are only correctness-smoke
evidence, not generalization evidence.

For head-N pilot or smoke-test evaluations, compare against prior full runs by reusing
saved hypothesis outputs or saved per-example score files whenever possible, rather than
re-running old baselines from scratch. Prefer evaluation paths that gracefully handle any
number of lines or expose a `--head` flag so small-slice comparisons remain directly
comparable to earlier full-split runs.

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

**Research-line closure before moving on**:
- After a substantial experiment line produces a surprising or weakly-positive signal, do
  not immediately jump to the next high-level research-plan item. First exhaust the
  reasonable closure tests that explain whether the previous investment paid off, failed
  for a code/configuration reason, or only beat an insufficient baseline.
- For combination-only gains, compare against embarrassing null baselines with the same
  decode/selection budget, such as random same-norm adapter perturbations or random
  one-step experts. A learned adapter that cannot improve on its own only earns credit in
  a blend or system-combination result if it beats those random-direction controls across
  enough seeds or validation-selected candidates.
- Treat this closure work as part of the result, not a detour: record the null baselines,
  bug checks, and plausible failure explanations before declaring the line exhausted or
  moving to the next paper-level project.

**Post-run option audit**:
- When post-run analysis of logs raises a possible mishap, inefficiency, anomaly, or
  suboptimal behavior, grep the relevant tool's `--help` output for the symptom terms
  and nearby concepts before assuming the behavior is fixed. The log does not need to
  show an outright bug; terms such as "reload", "sync", "batch", "patience",
  "checkpoint", "cache", "offload", "wrap", "timeout", or "floor" may indicate an
  existing controllable knob.
- Use context-aware searches over help text so the matched option and its neighboring
  descriptions are visible. Prefer an agent-friendly non-wrapped help mode when
  available because it saves tokens and avoids follow-up wider-context reads to
  reconstruct wrapped option descriptions.
- Summaries should name any relevant existing options and recommend the smallest
  follow-up run or setting change that would distinguish "tool limitation" from
  "unexamined option/configuration".

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
| 004 | decoder-tuning | tasks/004-decoder-tuning.md | Not Started |
| —   | retrain v2c (seed=999) | (inline) | Not Started |

**Last subtask completed** (user confirmed): _(none yet)_
**Last subtask worked on**: 003-prompt-consistency-refactor
**Likely next**: retrain v2c, then 004-decoder-tuning
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
2. Skim `research/<branchname>.md` (paper) for current framing, findings, and
   tables; if the governing task mentions a different paper path, skim that
   paper too.
3. Read the main task file matching the branch name — check its Subtasks section
   and any summary of what needs to be synced into the paper.
4. Read any in-progress subtask files listed in last-session.md
5. Check `research/<branchname>.log.md` for the most recent session's notes

Do not run this checklist for a fresh, specific request that lacks an explicit
`/hi` or resume signal; follow the AGENTS.md session-opening rule instead.
