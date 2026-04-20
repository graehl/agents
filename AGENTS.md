# Banner

Immediately say "Global AGENTS understood" after reading all of this.

# Session management

Session state is saved in `last-session.md`. Use `/bye` to save a
summary before ending work. Use `/hi` to recover context only when the
user greets you, explicitly resumes prior work, or otherwise signals that
they want session recovery. Independent sidequests do not require `/hi`,
though `last-session.md` can still be checked as an optional time-saving
hint. `/hi` and `/bye` — that's the whole ritual. Task files in `tasks/`
track per-feature progress and architectural decisions — read the active
task file when resuming.

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

### Load-bearing instructions

When writing or editing instructions for agents (AGENTS.md,
AGENTS.local.md), propose deletions and simplifications for entries
that don't bear load — rules that don't steer behavior beyond what a
capable coding agent (frontier models like ChatGPT 5.x or Opus 4.x,
and local open-weights models only a little behind) already does by
default. Use your own knowledge of default agent behavior as the
baseline. Preferences, project-specific context, and counters to
defaults the user wants to override are load-bearing; restatements of
standard tool mechanics or documented defaults the model would already
follow are not.

### Confirmation threshold

A clear affirmative means alignment — proceed without re-checking unless a
genuinely new ambiguity or risk has emerged.

### User shorthand

`YA` / `yepanywhere` refers to the user's client: `github.com/graehl/yepanywhere`.

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

### Diff presentation

When showing the user a diff, default to a standard unified `+/-` diff via
`git diff --no-ext-diff --no-color` (the `--no-ext-diff` bypasses any
configured external driver such as difftastic; column-1 markers scan well
without ANSI color).

Use a markdown table with `before | after` columns only when both apply:
the content reads as prose (e.g. two NLP/model runs on the same input) and
within-line changes matter enough to justify hand-constructing the table
with **bold** around the differing spans.

Avoid difftastic side-by-side output — it wraps illegibly in narrow UI
panes. Avoid `--word-diff` (`[-del-]{+add+}` markers) until the UI renders
ANSI color, since without color the mid-line markers are hard to scan.

### Project-scope instructions before tools

Before running tools in a repository for the first time in a session, check for
project-scope instruction files in that workspace. At minimum, look for repo-local
`AGENTS.md` / `AGENTS.local.md` / `CLAUDE.md` and any project `README.md` they point to, duplicate, or
explicitly name as an instruction source. Do not assume task files or prior session
state are sufficient substitutes for this initial project-scope instruction check.


## Project-level instruction files

When launched in a project root:
- If `AGENTS.md` exists (regular file or symlink), resolve and read it as
  project-level instructions.
- If `AGENTS.local.md` exists, read it as a supplementary amendment to the
  project-level instructions.
- If either file is unreadable or a symlink is broken, report it once and
  continue with global instructions.

Project docs are supplementary by default. If they materially conflict and
precedence is unclear, ask the user.

## Research and run supplements

Research-method and run-operation policies are split into companion docs:
- `RESEARCH.md`
- `RUNS.md`

Activation triggers:
- Load `RESEARCH.md` before substantive work when the repo or request indicates
  research/experimentation (e.g., `research/`, `tasks/`, notebooks, train/eval
  scripts, significance requests, or research-paper/log updates).
- Load `RUNS.md` before launching/monitoring/summarizing jobs when the repo or
  request indicates run operations (e.g., `.agentctl/`, `*.running.md`,
  `write_artifact_meta.py`, long-running jobs, watchdogs, background jobs, or
  GPU scheduling/utilization).

Resolution order for companion docs:
1. repo root (`./RESEARCH.md`, `./RUNS.md`)
2. global alongside this file (`~/agents/RESEARCH.md`, `~/agents/RUNS.md`)

If a triggered file is missing, report once and continue.

# C++
When reformatting C/C++ changes, use clang-format only on modified lines:
  git diff -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i
Do not run clang-format on entire files.
You can use clangd to check your edits to a C/C++ source file (if a .clangd is present at project root)

# Commits

Composing commit messages: aim for a <=65 char subject, and strictly enforce a 72-column line wrap for the body.
Prefer bullet lists in the commit body when items are numerous or complex; prose when the content is short and simple.
Do not add `Co-Authored-By` trailers crediting an AI assistant — the human is the author.
## Instruction synthesis

**Maintainer**, here, means the human reviewer or a future agent
(possibly you) re-reading this commit to understand or re-derive the
change.

For non-trivial commits, include a concise excerpt or synthesis of the
originating instruction (or motivating observation, when the change
wasn't user-prompted) that is feasible to land in the committed
changes. Summarize the motivating request and key implementation
direction so a Maintainer could paste the message, add their own
adjustments, and recreate something close to the intended result. Prune
digressions, secrets, and low-signal chat detail; do not aim for a
verbatim or exhaustive transcript.

The subject line is the conventional scannable headline result — keep
it scannable in `git log --oneline`. The synthesis lives
in the body. The 72-column body wrap applies to synthesis prose as
well.

**Exemption**: skip the synthesis for mechanical or small + self-evident
changes — formatter passes, typo fixes, version bumps, trivial renames
with no substantive user direction. The conventional one-line message
alone is sufficient there.

**Research projects** follow a different commit-organization rule:
separate commit kinds — implementation changes versus research/plan-doc
changes (findings, paper edits, plan updates). Do not mix the two in
one commit; implementation typically lands first, with the findings or
plan commit that uses it as a separate follow-up. Commit as you go to
avoid accumulating a mixed checkpoint. (Each kind's synthesis body
naturally carries what's load-bearing — the user direction for impl,
the finding or plan rationale for the doc.)

**Series threading**: when a commit is part of a related series, append
a `Topic: <string>` trailer at the bottom of the body. The topic string
is freeform (descriptive phrasing fine; not constrained to a short
UPPERCASE codename). A series shares the exact same topic string across
all commits — "first in wins": commit-1 sets the canonical text, later
commits copy it verbatim so `git log --grep "Topic: ..."` finds the
chain. Switch topic strings only when it's obviously time for a new
one. Standalone commits with no expected follow-up: no trailer.

To avoid accidentally reusing a topic for an unrelated series, keep a
project-level `topics.md` log at the repo root and append each new
topic string to it when the series begins. The log is appended to
whether or not it's tracked in git — tracking is a project-collab-style
decision (commit it for shared/team repos where topic discipline is
mutual practice; leave it untracked on solo repos if preferred).
Format is freeform (not a traditional ChangeLog) — typically a
bulleted list with optional one-line notes. Scan `topics.md` before
opening a new series.

**Amend vs. second commit after a correction**: if the user contradicts or
corrects a commit that has NOT yet been pushed to the upstream default branch
(`origin/main` or `origin/master`, whichever exists), always `git commit
--amend` (or `git commit --amend --no-edit` for trivial fixups) so the branch
history stays clean and the corrected state is the canonical record. A second
stand-alone commit for a one-line correction adds noise and can leave a
misleading intermediate state in history.

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
