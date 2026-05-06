# Session management

Session state is saved in `last-session.md`. Use `/bye` to save a
summary before ending work. Use `/hi` to recover context only when the
user greets you, explicitly resumes prior work, or otherwise signals that
they want session recovery. When a fresh user turn is already a specific
request and does not explicitly ask for `/hi` or prior-session recovery,
treat it as an independent request by default: do not read or cite
`last-session.md` merely because it exists.

local (git ignored) .md files in `tasks/` track per-feature progress and
architectural decisions — read the active task file when resuming.
Upon believed completion of a task, append a dated completion status note at
the end of the task file listing the relevant git commit(s) and one line of
evidence for believing the work complete. If the task file contains inline
subtasks, make this a formal section listing status for each inline subtask.
It is permissible to judge each task file in isolation; agents need not recurse
into linked non-inline subtask files.

For implementation or bugfix work, search for related `tasks/*.md` files when
that directory exists. Cite the relevant task file(s) in planning and again
when concluding the request, so longer-running follow-up inventory stays
visible without forcing every small request to create a task. When task files
exist, they should define or cross-reference the relevant `topics/*.md`
topic(s) when practical.

## Resume source priority

Explicit automated handoff instructions or context compression as the first
turn mean `bye` was not previously run before creating the handoff (unless
actually seen at end of transcript). The previous session may be accessible
by a link/session id present in a handoff; browse that session (as if to
compress context or summarize) to ensure you are caught up; sometimes
sessions pursue multiple unrelated tasks in series so you can first scan for
obvious commit/topic change boundaries and closely read only the last two
such sections.

When resuming after a disconnected session, crashed browser/client, full
agent restart, or context compaction that may have dropped live details,
presume `last-session.md` is stale unless the user explicitly says the prior
agent ran `/bye` after the disconnect. The same applies when `last-session.md`
is older than live worktree files, recently modified task/subtask files,
active job state, or artifact metadata. In those stale-summary cases, recover
from live state first: the worktree, newest relevant task/subtask files,
`.agentctl`/run metadata, saved artifacts, and only then the platform-wide
session JSONL logs for the dead ancestor session. In repos with `tasks/`,
sort task files by mtime and read the newest relevant entries even when
`tasks/` is untracked or ignored by git; task files are live working state,
not necessarily repository history. For Codex, check recent
`~/.codex/sessions/**/*.jsonl` entries; for Claude, check the matching
project logs under `~/.claude/projects/**/*.jsonl`. Use `last-session.md`
only as a historical hint after those sources, not as primary truth.

# Verification and retrieval

When a task depends on a claim about the contents of a software project,
verify it against the repository before relying on it. Treat user and agent
assumptions as hypotheses until checked. ripgrep (`rg`) is available.

# Authority and instruction files

`~/agents/AGENTS.md` is the authoritative global instructions file. Repo-local
`AGENTS.md` / `CLAUDE.md` symlinks or copies may point here, but global policy
changes belong in this file first.

Likewise, shared helper scripts under `~/agents/` and `~/bin/` should be kept
in sync when they intentionally mirror each other. When those global
instructions or helper scripts are modified, make a brief commit directly on
`~/agents` `master` so the authoritative copy has a clear history.

**User-specific supplement**: `~/agents/AGENTS.user.md` contains personal
preferences specific to this user. Read it alongside this file at the start
of every session — it is not optional.

## Skills path aliasing

In this environment, `~/agents/skills` and `~/.codex/skills/user` may be two
paths to the same underlying directory (hard-link/bind-like aliasing). Always
treat `~/agents/skills` as the canonical edit target.

Do **not** "sync" these paths by converting one side to symlinks. That can
create self-referential loops (for example `skills/foo -> skills/foo`) and
break skill loading with "Too many levels of symbolic links".

Before any migration or sync operation, verify whether they are the same
inode: `stat -c '%d:%i %n' ~/agents/skills ~/.codex/skills/user`

## Instruction routing

When the user says something is a `global rule`, `project-level rule`, or
`branch rule`, treat that as an instruction about where the rule must be
persisted unless the user says otherwise:
- `global rule` -> write it to `~/agents/AGENTS.md`
- `project-level rule` -> write it to the repo-local `AGENTS.md`
- `branch rule` -> write it to the branch main task file in
  `tasks/NNN-<branch>.md`

If the user uses that phrasing, do not leave the rule only in chat state;
persist it in the corresponding authoritative file.

## Load-bearing instructions

When writing or editing instructions for agents (AGENTS.md,
AGENTS.local.md), propose deletions and simplifications for entries that
don't bear load — rules that don't steer behavior beyond what a capable
coding agent (frontier models like ChatGPT 5.x or Opus 4.x, and local
open-weights models only a little behind) already does by default. Use your
own knowledge of default agent behavior as the baseline. Preferences,
project-specific context, and counters to defaults the user wants to override
are load-bearing; restatements of standard tool mechanics or documented
defaults the model would already follow are not.

## Project-level instructions

Before running tools in a repository for the first time in a session, check
for project-scope instruction files. At minimum look for `AGENTS.md`,
`AGENTS.local.md`, and `CLAUDE.md` in the repo root, and any `README.md`
they explicitly name as an instruction source. Do not assume task files or
prior session state substitute for this check.

When launched in a project root:
- If `AGENTS.md` exists (regular file or symlink), resolve and read it as
  project-level instructions.
- If `AGENTS.local.md` exists, read it as a supplementary amendment to the
  project-level instructions.
- If either is unreadable or a symlink is broken, report once and continue
  with global instructions.

Project docs are supplementary by default. If they materially conflict and
precedence is unclear, ask the user.

Committed project instructions such as repo-local `AGENTS.md` should stand
alone for future agents and reviewers. Project-local/private amendments such
as `AGENTS.local.md` may be brief deltas against global instructions instead
of repeating the full policy.

### Local instruction file backups

Before editing or deleting an agent instruction file whose current contents
are not safely recoverable from git, first save a snapshot under
`.backups/<YYYYmmdd-HHMMSS>/<relative-path>` in the same workspace or nearest
repo. This applies especially to ignored or untracked local instruction files
such as `AGENTS.local.md`, and also to tracked instruction files with
uncommitted local changes that you might otherwise overwrite.

## Research and run supplements

Research-method and run-operation policies are split into companion docs:
- `RESEARCH.md`
- `RUNS.md`

Treat reusable research-method guidance and run-operation / `agentctl`
tracking policy as generally global. Persist those rules in
`~/agents/RESEARCH.md` or `~/agents/RUNS.md` unless the rule depends on a
particular repository's data, scripts, artifact schema, or paper-specific
decisions.

Activation triggers:
- Load `RESEARCH.md` before substantive work when the repo or request
  indicates research/experimentation (e.g., `research/`, `tasks/`,
  notebooks, train/eval scripts, significance requests, or
  research-paper/log updates).
- Load `RUNS.md` before launching/monitoring/summarizing jobs when the repo
  or request indicates run operations (e.g., `.agentctl/`, `*.running.md`,
  `write_artifact_meta.py`, long-running jobs, watchdogs, background jobs,
  or GPU scheduling/utilization).

Resolution order for companion docs:
1. repo root (`./RESEARCH.md`, `./RUNS.md`)
2. global alongside this file (`~/agents/RESEARCH.md`, `~/agents/RUNS.md`)

If a triggered file is missing, report once and continue.

# Big-effect command gate

Before running any big-effect command — including nontrivial commits,
amending a non-trivial commit, push, force push, file edits that entirely
replace previous user-written content, deploy commands, database migrations,
dependency upgrades, or destructive filesystem commands (exception: recently
created scratch/log/tmp files the user has not been shown; a filename
appearing in an approval does not mean the user knows the file; the user
knows files organized per agreed naming schemes or tracked in git) —

1. Stop before executing the command.
2. Quote the applicable AGENTS instruction.
3. State why this command is big-effect.
4. List the required checks for this command.
5. Verify each check against current repo/session state.
6. Show the exact command that would be run.
7. Do not proceed if any required check is missing or ambiguous.

# Commits

Composing commit messages: aim for a <=65 char subject, and manually wrap
body prose at 71 columns. Prefer bullet lists in the commit body when items
are numerous or complex; prose when the content is short and simple.

## Commit messages

Trivial commits get a short message (possibly subject-only).

For non-trivial commit messages:
* Format is a narrative session-summary synthesis of the motivation and
  decision => change
* Exclude credentials/secrets from commit contents and message
* Include main user decision points from session log of work committed
* Exclude unrelated side discussions but include approaches ruled out for
  non-obvious reasons
* Standard subject line (scannable headline for `git log --oneline`)
* Briefly indicate whether the test suite is known to pass after the commit
  (in commit-as-you-go or split commits this is not always the case)
* Explain the existence of significant diffs esp. creations of >3 lines
  length or significant-effect edits of any kind if not already mentioned
  or implied somewhere in the commit message; checking that what is said in
  the message appears compliant is not enough; we want every change at least
  broadly described (besides trivial: whitespace/formatting, comments, fully
  file-local var renames/refactors, etc)

For ALL amends of non-trivial commits:
* commit messages specifying amendment are to be amendments or additions to
  the existing well-crafted and valuable commit message.
* NEVER describe just the amendment in the amended commit message even though
  the amending change may be trivial. ALWAYS preserve the existing commit
  message info (the amendment can simply edit the part of the message
  corresponding to what was changed; if it's a change to a minor detail then
  no message change at all is needed)
* example of FORBIDDEN amend commit messages: 'moved X to Y.hpp' when X is
  created in this commit; instead don't mention it or better find if the old
  Z.hpp where X used to live is mentioned as the site for X and correct that
  minimally.
* the amended commit message must be true of the commit contents by the
  original non-trivial commit message standards!

All commit messages: manually wrap body prose at 71 columns. This keeps
fixed-width formatting intentional and avoids Gerrit double-wrapping.
Exceed 71 only for unavoidable long tokens/strings, not to reduce raggedness
or avoid a short neighboring line. Do not link to git-ignored content e.g.
`tasks/`; no `Co-Authored-By`.

Manual wrapping is a visual formatting rule, not greedy fill: preserve
bullets, hanging indents, aligned continuations, short tables, quoted blocks,
and ASCII diagrams, even when that leaves a non-full line before the target.

* Before committing, ALWAYS make an additional final commit message global
  improvement check for coherency and conformance w/ checklist. This is
  equivalent to a kind of brief review for coverage; every impactful item in
  the diff must be covered by some motivating or summary implying existence
  of some similar diff chunk. In this final edit, consider (rereading the
  draft message) splitting into independent impl. parts, or impl. and then
  research finding parts (if this is a research project).

### Commit topic series threading

When a commit is part of a related series, append a `Topic: <string>`
trailer at the bottom of the body. The topic string is the basename of the
relevant committed `topics/<topic>.md` file when one exists; inspect
`ls topics/*.md` to see the project topic namespace. A topic series shares
the exact same topic string across all commits: commit #1 sets the canonical
text, later commits copy it verbatim so `git log --grep "Topic: ..."` finds
the chain. Switch topic strings only when it's obviously time for a new one.
Topic should also be easy to cross-reference from related `tasks/*.md` files.
Standalone commits with no task spec. and no expected follow-up: no topic
trailer.

### Amend vs. second commit after a correction

If the user contradicts or corrects a commit that has NOT yet been pushed to
the upstream default branch (`origin/main` or `origin/master`, whichever
exists), always `git commit --amend` (or `git commit --amend --no-edit` for
trivial fixups) so the branch history stays clean and the corrected state is
the canonical record. A second stand-alone commit for a one-line correction
adds noise and can leave a misleading intermediate state in history.

### Recent pushed oopsies on personal GitHub

If a pushed commit to the user's `github.com/graehl` remote is discovered
within days to be wrong, and there are no downstream forks/consumers
depending on that erroneous commit, prefer `git commit --amend` plus a
force-push/overwrite so the bad state disappears rather than accumulating
noise-fix history. Exception: do not rewrite once the branch/commit has
already been submitted as a PR elsewhere; in that case, keep history stable
and repair forward unless the user explicitly says otherwise.

## Pre-commit gate

Before running `git commit` for a non-trivial change:

1. Recite (in your scratchpad or thinking block) the key commit-message
   requirements from the AGENTS.md Commits section — this demonstrates
   actual engagement with the rules and makes compliance verifiable rather
   than merely claimed.
2. Decide whether the change is trivial or non-trivial.
3. If non-trivial, list the session requirements and implementation decisions
   that another agent would need to recreate an equivalent change (but not
   fully specifying exact explanatory documentation, comments, UI, or usage
   text).
4. Draft the commit message per the checklist.
5. Check that every item from step 3 appears in the message.
6. Only then run `git commit`.
7. No `Co-Authored-By` — the user is the author.

# Code quality

## Anti-slop implementation

Do not turn implementation or debugging work into a maze of permissive
fallbacks just to make the current trace succeed. Unrequested recovery,
precondition softening, broad exception swallowing, warning-and-continuing,
skipping required work, or proceeding with partial state are acceptable only
when they preserve the documented contract and are part of the requested
behavior. If the requested outcome needs a missing precondition, establish
that precondition explicitly or fail with a clear, actionable error; do not
silently reinterpret bad inputs or bypass required checks to keep moving.

Prefer repairing the model of the problem over adding output-forcing patches.
A chain of "if this input condition then force that output condition" clauses
is a design smell unless each branch follows from an explicit domain rule.
Before adding a special case, name the invariant or contract it preserves,
check whether a simpler representation would make the branch unnecessary, and
test the contract boundary instead of only replaying the observed debugger
trace. Future maintainers should be able to prove the behavior from
principles and local contracts, not reconstruct accumulated exceptions.

## Feature validation

When adding or enabling a feature that can affect runtime, memory use, model
quality, or experimental conclusions, plan an explicit on/off comparison
unless the effect is mechanically obvious and low risk. Scope the comparison
to the blast radius: a smoke-scale timing check is enough for narrow
plumbing, while research-facing training, decoding, scoring, scheduling, or
data-selection changes need a recorded contrastive run or a clear task note
explaining why the comparison is postponed.

## Avoid redundant compute

For compute-intensive implementation paths, treat redundant computation as a
design bug to avoid up front. Reuse cached, prefetched, or intermediate work
that has already been paid for, and repair only the rows, systems, shards, or
states that actually need repair. Pure discovery and housekeeping scripts are
exempt unless they become performance-critical. If an obvious reuse path is
left out for expedience, mark it as temporary with a task note and a planned
on/off timing comparison.

## Ideal coding

- Use precomputation or verifiable 'proofs' (e.g. exhaustive enough testing)
  of library contracts when possible to achieve n*lg n or better performance
  on tasks that feel they should be simple. It's shameful to make something
  quadratic or worse that need not be. However, easily scannable/verifiable
  code is also important. It's an aesthetic tradeoff that depends on how hot
  the path could become in practice. Further, an understanding of whether
  memory or compute is the bottleneck is needed when proposing even O(n)
  added per-input scratch space to improve past O(n * lg n) time.
- Everything you change should become a polished 'gem' limited primarily by
  prudent (and courteous to collaborators) avoidance of scope creep /
  sweeping refactors. Prefer the shortest conventional readable option that
  correctly expresses the contract. Clever low-level tricks are permitted
  when they meaningfully improve size or speed, especially in hot code, but
  document the reason. This is a strong aesthetic preference.
- Do favor styles that allow useful work by lesser programmers in referring
  to popular conventions in domain and programming terminology, patterns,
  etc. but do not sprinkle obvious "strategy pattern" type comments
  everywhere — unwanted and ugly. Part of the name of something can allude
  to known terms/patterns. Lesser programmers copy/paste. While we favor
  reusability-ready code, general facilities invented for one use need to
  live close in the source to their use.
- Since error handling, logging, and other defensive/boilerplate items are
  distracting, especially focus on a concise "get these things checked and
  right" once positioning of such gates. You can rely on exceptions.
  Correctly reducing overall code size/reading burden by placing these logs
  etc once per input execution (or once at load time) does require a global
  view or even grep for such logs. Observe the structure of run logs for
  potential reductions in logging code and also interpretability/elegance of
  the log flow with agent search/inference in mind, e.g. nested indents
  mirroring subtasks are nice if used everywhere but hard to line-search for
  correctly so cannot be the only signal (open and close brace type
  conventions for logs are not in widespread currency). Therefore some
  context info can be repeated across multiple lines in spite of it
  compromising on an otherwise essential aesthetic: things are most elegantly
  defined (and run-logged) only once.
- Tradeoffs of fundamental elegant/polished gem aesthetic are allowed in the
  direction of both human and agent new-maintainer immediate
  legibility/searchability; needless runtime inefficiency is not in the case
  of planned future large runs' hotspots.

# Project organization

## Project topics

For git projects, create and commit a `topics/` directory unless local
project instructions say otherwise. Use committed `topics/*.md` docs to
explain why important subsystems or cross-cutting aspects should be correct
in relation to the whole system. The `topics/*.md` basenames define the
project topic namespace used by `Topic:` commit trailers; inspect
`ls topics/*.md` to discover the available topic names.

**Scope and granularity**: topics map to *concerns* — cross-cutting
contracts, shared invariants, integration boundaries, security or
performance properties — not to modules or directories. A topic that only
describes one module's internals with no external consumer is probably a
README section. Topic count is useful as developer onboarding, casual commit
review orientation, and a forcing function for periodic global-consistency
checks.

For granularity calibration and a domain-organized vocabulary of well-scoped
topic names, read `~/agents/TOPICS.md`. Do this when creating a new topic,
assessing whether an existing one is correctly scoped, or running a periodic
global-consistency pass. It is not required reading on every task.

Most projects carry tech debt: architectural concerns that are real,
load-bearing, and simply unwritten. Catch-up topic creation is appropriate
whenever you need to state a contract between a topic you are writing and an
adjacent concern that has no doc yet — write the missing stub rather than
leaving the cross-reference dangling.

**Content**: a topic doc is not a change log. It names contracts, invariants,
assumptions, dependencies, known edge cases, and representative change types.
When work discovers a contract relied upon across concerns, add or update a
concise note in the relevant topic doc even if the implementation change
itself is small.

**Epistemic labeling**: an unlabeled claim means "plausible architectural
claim, not specifically verified." Add an inline HTML comment only when the
absence of a label would mislead a reader about confidence:
- `<!-- verified: SHA abcdef0 -->` — confirmed by test, bisect, or audit
- `<!-- assumed -->` — design intent or working hypothesis, unverified

`<!-- assumed -->` annotations are natural review targets. Do not use
"last updated" dates — they create false confidence. When a commit directly
weakens a `<!-- verified -->` claim it touches, downgrade it to
`<!-- assumed, see SHA ... -->` rather than leaving a stale marker. Apply
this check only to the specific invariant the diff touches, not to the whole
topic doc.

**Active use — debugging and significant planning**: before touching any
code in response to a bug, scan `topics/` filenames for the affected concern
and read the relevant doc. Do not chase a log trace or debugger observation
directly to a fix — that path produces patches that silence the symptom
while violating a contract the trace never showed. Contracts and invariants
in the topic doc tell you what *must* be true and therefore where the
violation must actually live. Form a hypothesis that satisfies those
invariants, then verify it against the trace — not the other way around.
Follow cross-references outward (grep, links) as needed. Before committing
to a significant or risky implementation plan, do the same: topic contracts
limit the design space and name external consumers that are required test
targets. A full pass over all topics for global consistency is a separate
periodic ritual, not a per-task step.

**Pre-commit trigger**: before finalizing a nontrivial commit message, read
the topic docs relevant to the changed aspect and confirm whether the commit
needs a `Topic:` trailer. If the change touches an important cross-cutting
contract and no relevant topic doc exists, create or update one (prefer
adding a section to an existing related topic over a new file unless the
concern is genuinely orthogonal). Explicitly check whether any claim the
diff directly touches is now false or weakened; update or downgrade its
epistemic marker rather than leaving a silent contradiction. Add a note when
the change alters the correctness argument, exposes a new edge case, or
leaves a risk unresolved. Use the topic to design tests: what violation
would falsify the contract? Build targeted tests around that boundary.

# Language tooling

## C++

When reformatting C/C++ changes, use clang-format only on modified lines:
  git diff -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i
Do not run clang-format on entire files. You can use clangd to check your
edits to a C/C++ source file (if a `.clangd` is present at project root).

## Python

Use `ruff check --fix` and `ruff format` rather than separate
black/isort/flake8 invocations. Add type hints to function signatures. Prefer
`uv` or `pixi` for environment and dependency management. Avoid `shell=True`
in subprocess calls with any user-influenced content. In ML code, make device
placement explicit rather than assuming CUDA availability.

# Interaction style

## Confirmation threshold

A clear affirmative means alignment — proceed without re-checking unless a
genuinely new ambiguity or risk has emerged.

## Terse-reference ambiguity

When a terse user instruction or query seems redundant under shared common
knowledge, first consider whether an alternate interpretation is more likely,
especially whether a pronoun or elliptical reference points back a few turns
in the real engaged conversation. Prefer user/system instruction content over
tool outputs, pasted logs, or other bulky artifacts when resolving that
reference.

## Speech-recognition noise

When user text has sparse punctuation and includes likely mischosen words,
treat speech-recognition errors as a possible noise source. Decipher the turn
with near-homonyms and deficient language-model word choices in mind before
deciding the user meant the literal transcript.

When you do silently disambiguate a likely speech-recognition error or other
transcript noise (typos, missing punctuation, dropped words), briefly restate
what you understood the user to mean before acting on it — typically as the
opening of your next sentence, paraphrased rather than quoted, e.g. "Got it —
you want X, not Y." Do this whenever a literal reading would be a different
task than the one you're proceeding with. The user's choice not to interrupt
is implicit confirmation, which is far better than just "right" + diving in:
they get a free chance to correct a misread before you spend effort on the
wrong interpretation. Keep the restatement to one short sentence; do not
quote the original transcript back at them.

## "Don't forget" reminders

When the user says `don't forget X` (or similar phrasing), briefly check
whether `X` is already present in the governing global/project/branch
instructions or is only an inferred expectation from the current plan. Report
back succinctly:
- where it was already covered, quoting or paraphrasing the closest governing
  phrasing when practical
- or that it was not explicit and should be added if the user appears to
  want it

When helpful, also say whether `X` would have been independently likely from
the existing instructions and current task direction, or whether the reminder
was surprising enough that an explicit rule is warranted. Do this with
judgment; do not overclaim access to a counterfactual inner state.

## Planning rationale

When the user gives planning or sequencing directions, assume there is often
an implicit claim or justification behind "A before B" that is worth
surfacing. Briefly ponder and suggest the most likely rationale for the
ordering or choice, especially when that rationale would sharpen the plan,
expose a hidden tradeoff, or help the user correct/generalize an unspoken
intuition. Keep this brief and tentative rather than leading: the goal is to
elicit or refine the user's real reasoning, not to force agreement or create
confirmation bias.

## Agreement and disagreement quality

When agreeing or disagreeing with the user on a substantive technical claim,
briefly paraphrase the claim as understood and give the checked crux of the
reasoning. Prefer a compact argument sketch that an expert can verify over
credibility-seeking phrases. If the crux has not been checked, say that
directly and label the agreement or disagreement as tentative. Do not add
plausible but unverified reasons merely to make alignment sound stronger;
low-quality "because..." clauses waste the user's time by forcing them to
debug the agent's reasoning.

## Asynchronous questions

Socratic or genuine clarifying questions are allowed when they can improve
the shared understanding of the work, but they must be treated as
asynchronous by default. Do not let such questions stall execution for more
than about 30 seconds while awaiting a reply. Assume many of them will go
unanswered; if the question is still worth posing, ask it briefly and
continue working. When helpful, tag the question with a short project-style
codename prefix such as `ORBIT:` or `KEPLER:` so the user can quickly
recognize it as an optional reasoning probe rather than a hard blocker. Do
not standardize on one fixed keyword forever; choose a brief topical codename
that fits the question. A later user reply may still be answering such a
codename-tagged question; do not reject that interpretation merely because of
delay. Only treat the reply as unrelated when the surrounding context makes
the intended referent clearly different.

## Explanation style: "remind me" / "refresher"

When the user says **"remind me"** or **"refresher"** before a concept or
technique, deliver a self-contained paragraph or short textbook-style section
with these properties:

- **Computation-focused**: lead with the core equation, algorithm step, or
  worked micro-example (small concrete numbers). Do not open with historical
  background.
- **Worked example**: include at least one small numerical or pseudocode
  illustration that a reader can trace by hand in under two minutes.
- **Mnemonic anchors**: give the acronym expansion on first use and the
  primary discoverer's last name + year (e.g., "RSLoRA (Rank-Stabilized
  LoRA, Kalajdzic 2023)").
- **Related concepts**: briefly name the 1–3 most closely related
  field-known techniques.

# Tooling conventions

## Search conventions

Use `rg` for repository text search and `rg --files` for file discovery. Add
type filters when they narrow the question, e.g. `rg -t md "pattern" .` for
project Markdown files.

## Agent-facing CLI help

When designing or modifying command-line tools likely to be used by agents,
make their `--help` output agent-friendly. Do not hard-wrap option
descriptions by default based only on `TERM` or terminal column guesses;
agent invocations may still present as ordinary color terminals. If
traditional human-wrapped help is useful, expose it through an explicit
width/env setting or other opt-in path. Prefer shared parser/formatter
helpers when a repo already has them, so option UI conventions stay
consistent across tools. Non-wrapped help is more efficient for agents to
parse because it saves tokens and avoids follow-up wider-context reads to
reconstruct wrapped option descriptions.

For info/warn log messages whose behavior is controlled by an option, include
the exact option name when practical, or at least a greppable word that
appears in that option's `--help` text. Prefer spelling the log term the
same way in logs and help text, without avoidable hyphen/underscore variants,
so post-run analysis can connect symptoms back to controllable knobs.

## PDF reading

For substantive PDF reading, use `marker-pdf` from a dedicated Python
environment. Do not install it into a project's ML runtime environment:
marker brings its own ML/OCR dependency stack and multi-GB model cache. In
Pixi projects, add a separate feature/environment such as `pdf`; in non-Pixi
projects, use a dedicated venv or `uvx`/`uv tool`-style isolation. Set a
project-local marker/surya model cache and temp directory when the default
home cache or `/tmp` may be space-constrained.

Do not use `pdftotext` for paper reading. Marker is the default extractor
for papers because it preserves tables, columns, math, and section structure
much better. Treat it as the practical lightweight alternative to GROBID:
comparable purpose for structured academic-paper extraction, but without the
heavier Docker service setup.

## Diff presentation

When showing the user a diff, default to a standard unified `+/-` diff via
`git diff --no-ext-diff --no-color` (the `--no-ext-diff` bypasses any
configured external driver such as difftastic; column-1 markers scan well
without ANSI color).

Use a markdown table with `before | after` columns only when both apply: the
content reads as prose (e.g. two NLP/model runs on the same input) and
within-line changes matter enough to justify hand-constructing the table with
**bold** around the differing spans.

Avoid difftastic side-by-side output — it wraps illegibly in narrow UI
panes. Avoid `--word-diff` (`[-del-]{+add+}` markers) until the UI renders
ANSI color, since without color the mid-line markers are hard to scan.
</parameter>
</invoke>