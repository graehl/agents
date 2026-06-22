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

#### First-contact public-facing sections

For the first public-facing section of a research paper, report, or
presentation, model a reader who has none of the live conversation context.
Before accepting the opening framing, check:

- Does the opening state the main result or claim before mechanism detail?
- Can a reader understand the task without knowing internal run names?
- Are condition names literal enough to decode from the table alone?
- Are all abbreviations, glossary terms, and project-specific labels expanded
  or briefly glossed on first use?
- Does the first table avoid implementation/debug-only columns?
- Are table columns defined immediately below the caption when they are not
  ordinary field-wide terms?
- Are cost columns clearly stage vs. cumulative, or omitted until needed?
- Are estimates labeled as estimates?
- Are diagnostic, parser-audit, or instrumentation-only runs separated from
  scored experimental conditions?
- Does the text say what is measured, what is not measured, and what is
  pending?
- Would a reader know which comparison is the main claim?
- Would a skeptical reader know which controls or baselines are missing?

Diagnostic, parser-audit, or instrumentation-only runs do not belong in the
main result table unless they are scored under the same output contract as the
main conditions. Mention them separately as audit evidence.

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

### Progress reports

Projects with sizable research scope should periodically emit a dated
`research/progress-YYYY-MM-DD.md` instalment — a plan-change and triage
report written for a manager or peer research org consuming the stream of
reports without delving into the repo. Spec and rationale:
`topics/progress-report.md` ("progress report" / "research progress
report"). Key contract: each instalment implicitly contains its
predecessors (brief restatement for a new reader, details by reference to
older reports/topics), states conditions in newcomer-legible expanded
form, ends every thread with an explicit pursue/hold/park triage verdict,
and is frozen once disseminated (corrections go in the next instalment).

### Field surveys and frontier mapping

Three companion files cover field-survey work, in pipeline order:
- `literature-search.md` — the **retrieval method**: citation snowballing from
  trusted anchors (paper-DB relevance/citation scores), with keyword search
  filtered by a known-labs/authors prior for the freshest, not-yet-cited work.
  Finds the papers the other two organize and rank.
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
- **One typed column per quantity; caveats go in footnotes, never in the cell.**
  A column is homogeneous down its length (all tokens, all seconds, all the same
  metric); a table is heterogeneous across columns. So a metric request means one
  column per quantity — "tokens and time" is **two** numeric columns, not one cell
  holding `1234 tok / 5.6s`. Manual decoration is always allowed regardless of a
  column's type — it annotates the number rather than replacing it: **bold** the
  best value, a `±ci` confidence interval on the number, or stat-sig markers in a
  comparison (the common research convention is `*`/`**`/`***` for p<.05/.01/.001,
  `†` for a noted exception), plus footnote refs. These form a small fixed set, so
  a query treating the table as a database strips them to recover the bare value;
  free prose has no such closed vocabulary and cannot be stripped, which is the
  operational reason it must move to a footnote rather than sit in the cell. (A
  per-cell unit recap like `5.6s` is itself such a strippable token, so it breaks
  nothing — but it's stylistically discouraged: carry the unit in the header and
  leave cells bare. The searching-agent-friendly rule that favors self-describing
  *log lines* doesn't transfer, since a cell's header sits right beside it; recap
  only earns its noise for a table whose cells are quoted out of context.) When a
  number needs words — an outlier, an OOM-truncated run, a
  not-comparable condition — write a Markdown footnote (`[^r17]`) inline, freely,
  the moment you notice it: as cheap and local as cramming the cell (drop the
  marker, append one line) but the column stays clean and no table rewrite is
  forced. Make no column-vs-footnote decision mid-build — footnote always works.
  Defer the only structural choice to one pass *after* the table, its captions, and
  all explanatory/analysis prose are written: revisit then and extract or promote
  footnotes where it improves readability and renderer compatibility (e.g. dense
  parallel notes lifted into a mostly-empty comment column). The two errors to
  avoid are both about the cell: prose fragments crammed into a numeric cell, and —
  over-correcting — deleting legitimate commentary to force a numbers-only table.
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

**Hypothesis-mode communication**: When discussing experiments not yet
run, the user states hypotheses bald, without "probably" / "might" /
"need to test" framing — the unrun status is shared common ground.
Translate, don't restate: when recording such a claim (paper, log,
task file), render it as a hypothesis ("we expect X", "X would imply
Y"); the translation IS the hedge. Skip "needs testing" / "we haven't
measured this yet" replies — they only restate shared ground.

What this rule does NOT suppress: substantive disagreement. If
existing evidence or background knowledge makes the hypothesis
probably wrong (contradicts a known result, fails a quick check
against published findings, conflicts with data already in front of
you), say so promptly — do not meekly record the claim as a
hypothesis to test. The distinction: "needs testing" replies waste
time on shared common ground; "probably wrong because X" is the
pushback the user wants immediately.

**Truth over momentum**: In research, the desired output is what
actually works or is actually true — including null results,
falsified hypotheses, and "doesn't work" findings. Those are
successful experiments, not setbacks to spin. Reserve language like
"promising" / "encouraging" / "on the right track" for cases where
the evidence supports it, not for cases where the user has invested
recent effort and would feel rewarded by it. Report what is, not
what would feel like progress.

**Favor ambition**: Prefer experiments that resolve live uncertainty
over experiments that confirm what we are already nearly sure of. A
run with a known-likely outcome wastes compute and time; design
probes that could plausibly surprise, that distinguish between
competing hypotheses, or that move the frontier of what is known.
"Let's first verify X" is the wrong default when X is already well
established — skip the redundant confirmation and aim higher.

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

### Result-sanity preview

Before presenting any newly wired
experiment/eval/benchmark/scorer/decode/parser/extraction result
as meaningful, do a cheap output-contract sanity preview,
including for prototypes and pilots.

Check, as applicable: item counts and empty/malformed outputs;
producer format vs. consumer format (`txt`, JSONL, auto,
extracted field); one aligned example per new condition showing
input, expected target when one exists, produced output, and the
exact payload consumed by the scorer/downstream tool; and
condition order plus item/row mapping for promptsets, multi-policy
outputs, concatenations, extractions, or joins.

When reporting a new result, quote the preview unless the path is
unchanged. Treat results as provisional until it passes; if it
fails, fix the path and explicitly supersede contaminated numbers.
Never present new-wiring scores whose consumed examples could be
wrappers, record objects, prompt echoes, parser markers,
diagnostic text, or shifted rows.

For outputs with no exact reference (generation, MT, model judgments),
the scorer is a soft-check oracle — a property/metric or rubric over a
kept case set, with metamorphic relations (paraphrase / terminology
invariance) the native form for translation. See `topics/soft-checks.md`
for the oracle-choice and no-leak-to-generator rules.

### Build the strongest cheap baseline early

In every experiment arm, build and tune the strongest cheap/simple baseline
*before* judging an elaborate approach — not as a checkbox row but as the
first real effort. The search pays out two ways regardless of how the arm
breaks, so a "we lost to baseline" result is information, not a setback:

- The baseline may simply be the win — a cheap, reliable technique that
  already matches or beats the elaborate method is worth shipping precisely
  because it is cheap and reliable, and it advances the deployable curve now
  while the fancy method is still speculative.
- A strong baseline debugs the elaborate method. If you only compare against
  a *weak* baseline you mis-read a small positive delta as success and never
  diagnose. A strong one forces the diagnosis and names the fix: "losing to
  baseline → need more data," or "→ need at least the smoothing/regular-
  ization that lets us match baseline before any added mechanism can show
  through."

Recurring corollary: across arms, a cheap calibrated/external component
(a selector, a fixed routing recipe, a direct first pass) often beats a
cleverer model-internal mechanism at deployable scale. Expect it; do not
treat each instance as a surprise.

Triage guardrail when this becomes a named theme in a report or paper:
over-claiming a unifying theme is harmless *only as long as it does not
color per-thread triage*. Triage each arm on its own cost and likelihood;
a repeated theme is a story for the reader, not extra evidence, and earns
an arm no triage weight.

### Attributing a surprising change across multiple differences

When a surprising (usually bad) result follows a departure from baseline that
changed several things at once and you have no one-at-a-time ablation: first
resort is to **just run the one-thing-at-a-time ablation, or a progression from
baseline** — if the runs are cheap or the effect is large enough to measure
quickly, do not spend tokens reasoning about attribution you could cheaply
measure. The rest of this applies only when the controls are expensive enough
that careful between-run thought earns its tokens. There, "underperformance
usually has one main cause" is a useful *prior for where to probe first* — not a
conclusion; it is Bayes-valid only under two structural conditions, so step away
from it when either cracks:

- separability — the causes' effects on the metric are ~additive (no
  interaction): `delta = delta_A + delta_B + delta_AB` with `delta_AB ~ 0`.
- skew — effect sizes are unequal, so one term usually dominates.

Distrust the single-cause story when any of these hold (signature in parens):

- Interaction / synergy — metric moves only with both present, AND-gate; neither
  alone is "the" cause (joint != sum of singles).
- Saturation — a cause near a floor/ceiling caps and hides another's real
  marginal effect until it is relieved (metric pinned at an extreme).
- Comparable magnitudes or many simultaneous changes — no reason one dwarfs the
  rest; with many similar-scope changes a lone dominator is unlikely (order
  statistics).
- Sign cancellation — one change helps while another hurts, so the net
  understates two large opposing effects; "one main cause of the net" is then a
  category error (net smaller than the changes' scope implies).
- Regime dependence — a cause helps in one slice and hurts in another; the
  aggregate is a blend with no context-free main cause (subgroup numbers
  disagree).

Scope note: a *limiting factor / binding constraint* (one stage binds, so
changing others does nothing) is deliberately absent — it explains a *missing*
expected difference (the dual problem), and when it does yield an observed one
the per-cause harms are usually additive, so it is not a separability failure
here.

Operational rule: use the prior to aim the *first* control (one leave-one-out,
or add-one-to-baseline, for the suspected dominant cause), then let the residual
adjudicate. If that cause explains most of the gap, the prior earned it; if a
large residual remains — or the residual flips sign — finish the factorial
before attributing. Two binary factors are four cells; additivity lets three
determine the fourth, but a confounded pair (baseline + full departure only)
never identifies the parts, however separable the truth is. One clean
leave-one-out earns its keep even when the observed gap looks modest: checking A
alone can reveal B is opposite-signed — a help masking a larger hurt — which the
net hid.

Two discipline riders. Keep straight *what* you are attributing: one cause can be
the main driver of the harmful component while the net is a two-effect story (a
help plus a larger hurt) — "usually one cause" can be true for one and false for
the other. And until the deciding cell is run, treat any interaction as an open
question, not a risk: an imagined failure mode is not evidence, and uncertainty
about an untested interaction is symmetric.

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

For machine translation (MT) evals, apply the global result-sanity preview
using MT-specific alignment: verify source/reference/hypothesis counts,
inspect at least one aligned source/ref/hyp example per new condition, and
confirm the scored hypothesis is plain translated text rather than JSONL
wrappers, prompt echoes, parser markers, diagnostic text, or shifted rows.

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

### On-deck research runs

For GPU-heavy research programs, `on-deck/` is the executable projection of
research triage into guarded single-step runs, not a replacement for the
research log or task file. Each entry should point back to the governing task,
research log, progress-report triage row, or topic next-step; the steward runs
checks and records raw facts, while research interpretation still lands in the
paper/log/task as appropriate. See `topics/on-deck.md`.

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
1. Recover the active root task and live state per `AGENTS.md` § Resume
   source priority (`tasks/ROOT`, `.agentctl/active/`, run metadata) — not a
   session summary.
2. Skim `research/<branchname>.md` (paper) for current framing, findings, and
   tables; if the governing task mentions a different paper path, skim that
   paper too.
3. Read the active root task — check its Subtasks section and any summary of
   what needs to be synced into the paper.
4. Read any in-progress subtask files it lists.
5. Check `research/<branchname>.log.md` for the most recent session's notes

Do not run this checklist for a fresh, specific request that lacks an explicit
`/hi` or resume signal; follow the AGENTS.md session-opening rule instead.
