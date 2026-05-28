# Session management

Session state lives in `last-session.md`. `/bye` saves a summary; `/hi`
recovers context — but only on a greeting or explicit resume signal. A
fresh, specific request is independent: do not read or cite
`last-session.md` just because it exists.

Git-ignored `tasks/*.md` files track per-feature progress and decisions;
read the active one when resuming. On believed completion, append a dated
status note with the relevant commit(s) and one line of evidence; if the
task file has inline subtasks, make it a section listing each subtask's
status. Judge each task file in isolation — no recursing into linked
subtask files.

For implementation or bugfix work, search `tasks/*.md` when that directory
exists, and cite the relevant file(s) in planning and conclusion. Task
files should cross-reference relevant `topics/*.md`.

## Resume source priority

A handoff or context-compression message as the first turn means `/bye`
did not run before the handoff. If it carries a link/session id, browse
that session to catch up — scan for commit/topic boundaries and read the
last two sections closely.

When resuming after a disconnect, crash, restart, or compaction, presume
`last-session.md` is stale unless the user says `/bye` ran after the
disconnect — and stale regardless when it is older than live worktree/task
files, job state, or artifacts. Recover from live state first: worktree, newest `tasks/*.md`
(by mtime, even if git-ignored), `.agentctl`/run metadata, artifacts, then
session logs (`~/.codex/sessions/**/*.jsonl` or
`~/.claude/projects/**/*.jsonl`). Use `last-session.md` only as a last
historical hint.

# Verification and retrieval

Verify claims about a project against the repo before relying on them;
treat user and agent assumptions as hypotheses until checked. `rg` is
available.

When entering an unfamiliar area of code, build a higher-level map
first — relevant modules and callers in the project's glossary
vocabulary — before drilling into a specific function. Deep
inspection follows the map, not the other way around.

# Authority and instruction files

`~/agents/AGENTS.md` is the authoritative global instructions file; global
policy changes belong here first, even when a repo-local `AGENTS.md` /
`CLAUDE.md` symlinks or copies it. Keep shared helper scripts under
`~/agents/` and `~/bin/` in sync. When global instructions or those
scripts change, make a brief commit on `~/agents` `master`.

`~/agents/AGENTS.user.md` is a personal supplement — read it alongside this
file every session.

The instructions live in the `~/agents` checkout (git origin
`github.com/graehl/agents`), which also holds companion docs explaining the
reasoning behind the policy and the evidence for it — e.g.
`topics/agent-instructions.md` and its `.evidence.md` ledger. These are not
loaded routinely; read one on demand only when unsure how to safely follow
a rule, or when proposing an improvement to it. Suggesting instruction
improvements is always welcome, from work in any project, not only when
working inside `~/agents`. You may append to a topic's `.evidence.md`
companion (the topic's evidence ledger and your own notes on the
topic). The convention — what to append, when, how, the append-only
and not-routinely-loaded constraints — is in
`~/agents/topics/evidence-ledger.md`.

## Skills path aliasing

`~/agents/skills` and `~/.codex/skills/user` may alias the same directory;
treat `~/agents/skills` as the canonical edit target. Do not "sync" them
into symlinks — that creates self-referential loops that break skill
loading. Check first:
`stat -c '%d:%i %n' ~/agents/skills ~/.codex/skills/user`.

## Instruction routing

When the user labels a rule, persist it (do not leave it only in chat):
- `global rule` -> `~/agents/AGENTS.md`
- `project-level rule` -> repo-local `AGENTS.md`
- `branch rule` -> branch main task file `tasks/NNN-<branch>.md`

## Load-bearing instructions

When editing agent instructions, propose cutting entries that don't steer
behavior beyond what a capable agent does by default. Preferences,
project-specific context, and deliberate counters to defaults are
load-bearing; restatements of standard tool mechanics or defaults are not.
Add explicit rules to prevent known project-specific failures; avoid
prompt debt that just replaces ordinary engineering judgment.

Non-frontier agents occasionally edit these projects, so keep redundancy —
worked examples, and the rationale behind counterintuitive rules — that
stops a weaker agent reasoning its way around a rule, even where a frontier
agent would not need it.

## Project-level instructions

Before using tools in a repo for the first time in a session, read its
root `AGENTS.md`, `AGENTS.local.md`, `CLAUDE.md`, any `README.md` they
name as an instruction source, and `GLOSSARY.md` if present. Task
files do not substitute for this. If a file is unreadable or a symlink
is broken, report once and continue.

Project instructions are the final word for work inside that project;
`AGENTS.local.md` is its private final amendment. Global instructions
govern actions outside the project. Report material conflicts with unclear
precedence rather than resolving them silently. A committed repo `AGENTS.md`
should stand alone; `AGENTS.local.md` may be a brief delta against global
policy.

### Local instruction file backups

Before editing or deleting an agent instruction file whose contents are
not safely recoverable from git (especially untracked files like
`AGENTS.local.md`, or tracked files with uncommitted changes), first
snapshot it under `.backups/<YYYYmmdd-HHMMSS>/<relative-path>`.

## Research and run supplements

Companion docs hold split-out policy:
- `RESEARCH.md` — research method; load before substantive work when the
  repo or request indicates research/experimentation (`research/`,
  `tasks/`, notebooks, train/eval scripts, significance requests).
- `RUNS.md` — run-operation / `agentctl` policy; load before
  launching/monitoring/summarizing jobs (`.agentctl/`, `*.running.md`,
  long-running jobs, watchdogs, GPU scheduling).
- `survey-field.md`, `research-frontier.md` — field-survey and
  research-frontier templates; load when the task is surveying a field,
  gathering prior art, or void-mapping/capstone suggestion. This trigger
  is independent of `RESEARCH.md`.

Resolve companion docs at the repo root first, then `~/agents/`. If a
triggered file is missing, report once and continue. Keep reusable
research/run guidance global (in `~/agents/`) unless it depends on a
specific repo's data, scripts, or schema.

# Big-effect command gate

Big-effect commands fall in two tiers.

**Full gate record** — for irreversible or shared-state actions: push,
force push, deploys, migrations, dependency upgrades, destructive
filesystem commands, and file edits that wholly replace user-written
content. Stop and produce the record below before running one.

**Light check** — for local commits and amends (especially doc-only): no
formal record, just a one-line confirmation that the staged scope is
intended and, for an amend, that prior commit-message content is
preserved. A local commit is cheaply reversible, so the full ceremony is
not worth it. Amending an already-pushed commit is still local (light
check); the force-push it then requires gets the full record.

Exception to both tiers: recently created scratch/log/tmp files the user
has not been shown — a filename appearing in an approval does not mean the
user knows the file.

The full gate record:
1. State the action and why it is gated.
2. List required checks as bracketed tags, each stating the current fact
   that satisfies or blocks it, e.g. `[wip] unrelated work present;
   command is path-limited to README.md`.
3. For multi-step gated operations, prefix each later action with the
   matching tag(s).
4. Show the exact command.
5. Quote exact policy only for destructive, forceful, ambiguous, or
   unusually risky actions, or on request.
6. Do not proceed if any required check is missing or ambiguous.

The bracketed-tag style is encouraged for other self-imposed gates; it is
required only for the full gate record.

# Ancillary workdir hygiene

When working in an ancillary worktree or scratch checkout, do not
put it on reboot-cleared storage (`/tmp`, tmpfs); use durable
storage — a sibling directory of the primary workdir, on the same
filesystem, is a good default. Before transferring content back
to the primary workdir,
verify source and destination branches match, and stash or
formally commit (or amend) first — a committed state is the only
safe transfer unit. Do not rely on default agent caution here.

# Commits

Subject <=65 chars and scannable for `git log --oneline`. Wrap body prose
manually at 71 columns — a visual rule, not greedy fill: preserve bullets,
hanging indents, aligned continuations, short tables, and ASCII diagrams
even when that leaves a short line. Exceed 71 only for unavoidable long
tokens. Use body bullets when items are numerous or complex, prose when
short. No `Co-Authored-By`; no links to git-ignored content (e.g.
`tasks/`).

## Commit messages

Trivial commits get a short, possibly subject-only message.

Non-trivial messages are a narrative synthesis of motivation and
decision => change:
- Exclude credentials/secrets from contents and message.
- Include the main user decision points from the session.
- Exclude unrelated side discussions, but include approaches ruled out for
  non-obvious reasons.
- Flag known uncovered areas or risks. Default presumption: work
  is at least manually smoke-tested; automated coverage is evident
  from the diff. Do not enumerate which tests were run or passed —
  that is busywork; the diff and CI carry it.
- Use a `Known coverage gaps:` labeled section near the end of
  the body (before trailers) when there are gaps worth flagging.
  Prose or short bulleted list, whichever fits. Be specific about
  the structural gap; omit the section entirely when empty.
- Broadly describe every non-trivial change — especially >3-line creations
  and significant-effect edits. Trivial changes (whitespace, comments,
  file-local renames) need no mention.

Consider splitting unrelated changes into independent commits (e.g.
implementation vs. research finding).

### Amends

For ALL amends of ALL commits:
- Leave the subject unchanged.
- Write the message as an additive or corrected update; do not erase prior
  content except to fix what is now incorrect.
- Describe only what changed relative to `HEAD~1`, not changes from the
  previous patchset. Forbidden: "preserved Z" when Z was already described;
  "moved X to Y.hpp" when X is created in this commit.
- An amended message must meet non-trivial standards if the original
  commit was non-trivial.
- Show the edited message as a diff, and confirm no prior content was
  dropped or replaced except as a deliberate correction.

When the user corrects a commit not yet pushed to the upstream default
branch, amend it (`--amend --no-edit` for trivial fixups) rather than
adding a noisy second correction commit. When a commit already pushed to
the user's personal GitHub is found wrong within days and has no
downstream forks/consumers, prefer amend + force-push over accumulating
fix history — but not once it has been submitted as a PR elsewhere; then
repair forward.

### Topic trailers

A commit in a related series gets one or more `Topic: <string>` trailers.
The string is the basename of the relevant `topics/<topic>.md` (`ls
topics/*.md` for the namespace); all commits in a series copy it verbatim
so `git log --grep` finds the chain. Use multiple `Topic:` lines for a
commit spanning topics. The trailer marks thread membership, not merely
that the diff touched a `topics/` file: a standalone commit with no task
spec and no expected follow-up gets no trailer even if it edits a topic
doc, while the commit that starts a thread gets one as #1.

# Code quality

## Anti-slop implementation

Do not pile on permissive fallbacks to make the current trace succeed.
Unrequested recovery, precondition softening, broad exception swallowing,
warn-and-continue, or proceeding on partial state are acceptable only when
they preserve the documented contract and are part of the requested
behavior. If the outcome needs a missing precondition, establish it
explicitly or fail with a clear, actionable error — do not silently
reinterpret bad input or bypass checks.

## Feature validation

When adding or enabling a feature that affects runtime, memory, model
quality, or experimental conclusions, plan an explicit on/off comparison
unless the effect is mechanically obvious and low risk. Scope it to the
blast radius: a smoke-scale timing check for narrow plumbing; a recorded
contrastive run (or a task note deferring it) for research-facing changes.

## Ideal coding

See `~/agents/topics/software-aesthetic.md` for the full shared aesthetic —
naming, comments, structure, abstraction, and input/output contracts. The
points below are either not in that doc or are worth repeating here:

- Before introducing a new general facility, consult
  `topics/shared-primitives.md`; keep single-use facilities close to their
  use.
- Keep run logs greppable: tag every line of a phase with the phase name
  (`WARMUP: ...`), rather than bracketing a span (`[start WARMUP]` /
  `[end WARMUP]`) or relying on indentation.

# Project organization

## Project topics

For git projects, maintain committed `topics/*.md` docs explaining why
important cross-cutting concerns must hold relative to the whole system.
Their basenames are the `Topic:` trailer namespace (`ls topics/*.md`).
Create `topics/` when first needed, not proactively.

Topics map to *concerns* — cross-cutting contracts, shared invariants,
integration boundaries, security/performance properties — not to modules
or directories; a doc describing one module with no external consumer is a
README section. A topic doc is not a changelog: it names contracts,
invariants, assumptions, dependencies, and known edge cases. For
granularity calibration and a topic-name vocabulary, read
`~/agents/TOPICS.md` when creating or assessing a topic.

Topic-doc format: an H1 stating the topic, then a `> ` blockquote
lede (one or more `> ` lines, no other content between H1 and lede,
multi-line `> ` lines space-joined when consumed), then optional
metadata (e.g., a `Topic: <name>` trailer) and body sections. The
lede is the canonical one-sentence definition consumed by
`GLOSSARY.md`. The agent may auto-edit existing topic docs to bring
them into this format without separate confirmation — synthesize a
missing lede from the doc's first body paragraph, move stray
trailers — provided the edit preserves body content faithfully.

Topic-doc companions: structured ancillaries ride alongside the main
topic doc as `topics/<name>.<suffix>` — either a `.<suffix>.md` file
or a `.<suffix>/` directory, depending on the convention. The main
topic doc stays free-form prose; concerns with their own structure
live in suffixed companions rather than dedicated sections of the
main doc. Current suffixes: `.evidence.md` (verification ledger,
append-only — see `topics/evidence-ledger.md`); `.runs/` (curated
run records — see `topics/runs-ledger.md`); `.bearings.md`
(orientation — see below).

`topics/<name>.bearings.md` is a nested outline of plan items. Each
non-leaf node carries `> why: <one line>` so the chain of "why we
opened this" reconstructs by reading parent → child whys; `> why:`
is required where non-obvious, optional on self-evident leaves.
Status markers per node: `[ ]` planned, `[*]` active, `[~]`
paused/blocked, `[x]` done; optional `★` for high-value. The
active backtrace is the chain of `[*]` from root to deepest active
leaf — a single highlighted spine through the tree.

Epistemic labeling: an unlabeled claim means "plausible, not verified".
Add an inline HTML comment only when its absence would mislead:
`<!-- verified: SHA abcdef0 -->` (confirmed by test/bisect/audit) or
`<!-- assumed -->` (unverified design intent). When a commit weakens a
verified claim it touches, downgrade that claim's marker rather than
leaving it stale. Do not use "last updated" dates.

Active use: before touching code for a bug, before committing to a
significant plan, or when entering a topic's area for the first time
in a session (including on resume), read the relevant topic doc and
its `.bearings.md` companion if present. The topic doc's contracts
tell you what must be true and therefore where a violation must
live — form a hypothesis that satisfies the invariants, then check
it against the trace, not the reverse. The bearings file gives
current orientation: synthesize it against live state (recent
commits, WIP, task notes), not a verbatim recap. Additional
bearings-read triggers: user says `bearings`, `orient`, `lost`, or
states a recollection of where work stands; the user's stated
recollection enters the discussion as an LTM-hunch candidate even
when outdated. After such a discussion, update the bearings file
and commit alongside the work. A full consistency pass over all
topics is a separate periodic ritual.

Some `topics/` entries are method/discipline docs rather than contract
docs — e.g. `debugging.md`, `testing.md`, `prototyping.md`. Load them
at the verb-trigger (before starting to diagnose a bug, before
designing or extending the test strategy, before building a prototype),
not only when the noun-shaped "relevant topic doc for the change" rule
fires by concern.

Before finalizing a non-trivial commit message, read the topic docs for
the changed concern and decide whether a `Topic:` trailer is needed. If the
change touches a cross-cutting contract with no topic doc, create or update
one (prefer a section in a related topic over a new file). Check whether
the diff falsifies or weakens any claim it touches, and design boundary
tests around the contract it could violate.

## Project glossary

`GLOSSARY.md` is the project glossary: a shared, prescriptive
vocabulary for talk, planning, code, UI copy, and commits in the
repo. Read on first repo use alongside `AGENTS.md` so terms stay
in attention. When naming a code symbol, UI element, doc heading,
or commit topic — or when prose starts spelling out in several
words something one term could carry — check the glossary first
and reuse an existing term rather than introducing a synonym or
paraphrase. When a user phrase or pasted log drifts from a glossary
term, prefer the glossary's wording. If `GLOSSARY.md` has fallen
out of context (deep in a long session, post-compaction), `rg` it
before proposing a new row or claiming a term is absent.

A glossary row is not a pending topic doc — most rows are vernacular
forever. A row becomes a `topics/<name>.md` only when it meets the
cross-cutting-concern bar in `~/agents/TOPICS.md`.

One sorted table: `| term | definition | topic / refs |`. Rows whose
`topic / refs` column links a `topics/<name>.md` are autopopulated
from that doc's `> ` lede (see `## Project topics`); other rows are
curated and preserved verbatim on regeneration, including
`<!-- unconfirmed -->` markers. Contribution and regeneration rules
belong in the project's `topics/glossary.md`; `GLOSSARY.md` itself
stays free of build instructions for readers.

Scoped sub-glossaries: a term lives in the `GLOSSARY.md` at the
narrowest enclosing directory; create the file if missing. Freely
promote a row to a parent's `GLOSSARY.md` as the term's scope
widens; the root `GLOSSARY.md` is the terminal scope. Before
naming or paraphrasing in a subtree, consult the nearest-enclosing
`GLOSSARY.md`. Scope is declared by file placement, not by a path-
pattern rule (subsystem cutpoints vary too much across projects).
Sub-glossaries hold pure vernacular; topic-doc autopopulation feeds
the root only.

When a user phrase is unclear and the resolution would change action,
emit an interruptible checkpoint with the inferred meaning plus 1–2
alternatives. Continue at normal pace when the fork is minor or
cheaply reversible; hold for the reply when proceeding with the wrong
branch would waste significant work. On resolution, propose a
glossary row flagged `<!-- unconfirmed: YYYY-mm-dd -->` until the
user prunes or confirms it. When the user explicitly introduces a distinction ("by
X I mean Y, not Z"), add the row immediately. When a row is clearly
general-domain — a term recognizable outside this project's
specifics — surface it once as a candidate for
`~/agents/topic-definitions.md` or `~/agents/TOPICS.md`; do not edit
those global files autonomously.

Create `GLOSSARY.md` when the project has more than one topic
doc or when project jargon starts recurring; not proactively.

# Language tooling

## C++

Reformat only modified lines, never whole files:
`git diff -U0 HEAD -- '*.c*' '*.h*' | clang-format-diff -p1 -i`. Use
`clangd` to check edits when a `.clangd` is present.

## Python

Use `ruff check --fix` and `ruff format` (not black/isort/flake8). Add type
hints to signatures. Prefer `uv` or `pixi` for environments. Avoid
`shell=True` with user-influenced content. Make device placement explicit
in ML code.

# Interaction style

## Confirmation threshold

A clear affirmative means alignment — proceed without re-checking unless a
genuinely new ambiguity or risk emerges.

## Execution-context limits

If your current execution context has limitations (observability, ability
to execute certain commands, access to state the user can see, etc.),
solve for them yourself — spawning login shells, using alternative
mechanisms, or clearly stating the limitation once — rather than pushing
repeated check-ins or friction back to the user. Defaulting to telling
the user "run this command yourself" is not an acceptable first-line
solution.

## Terse-reference ambiguity

When a terse instruction seems redundant under shared knowledge, consider
whether it points back a few turns — a pronoun or elliptical reference.
Prefer user/system instruction content over tool outputs or pasted logs
when resolving the referent.

## Terse instructions contradicting recent work

When a terse input maps to work already done this session, surface the
contradiction inline (`X looks done — did you mean Y?`) and pause for
redirect; do not silently switch items.

## Speech-recognition noise

User text with sparse punctuation and odd word choices may be
speech-recognition noise; read it with near-homonyms and likely dropped
words in mind before taking the literal transcript as the task. When you
silently disambiguate, restate what you understood in one short paraphrased
sentence before acting (e.g. "Got it — you want X, not Y"), so the user can
correct a misread for free.

## "Don't forget" reminders

When the user says `don't forget X`, check whether `X` is already in
governing instructions or only inferred from the current plan. Reply
briefly: where it is covered (quoting the closest phrasing), or that it is
not and should perhaps be added.

## Planning rationale

When the user gives sequencing directions ("A before B"), there is often an
implicit justification. Briefly and tentatively surface the likely
rationale when it would sharpen the plan or expose a hidden tradeoff;
continue unless the answer is a real blocker.

## Agent-chosen implementation branches

When the user explicitly leaves an implementation branch to the agent
("your call", "up to you"), call out the chosen branch and a brief reason —
at the decision point if it happens during planning, and in commit messages
and status summaries for completed work. This applies only to choices the
user made salient, not every routine decision.

## Agreement and disagreement quality

On substantive technical or research claims — including wording the user
asks to record in docs, commits, or task artifacts — do not merely
acknowledge or execute. Give the shortest useful crux-level feedback:
agreement, disagreement, or uncertainty; whether you checked it; and, when
following a direction anyway, whether that is because instructed or because
it independently seems right. Do not pad alignment with unverified
"because" clauses.

Before concurring with a significant or dubious claim that is not about the
user's own intent, preference, or observation, take a second epistemic
step: echoing a confirming claim is easier than generating a disconfirming
one. Use background knowledge to name adjacent ways the claim could be
false or overstated, use those to choose probes, and run targeted searches
for the probes — not just for supporting evidence, especially on the web.
If you accept a claim without that disconfirming pass (low stakes,
instructed wording, or out of scope), say so rather than presenting
concurrence as verified.

## Epistemic treatment of user statements

User preferences and direct observations are authoritative as stated. Only
clearly speculative user claims ("maybe it's because...") warrant
uncertainty labeling and verification before you build on them; when the
mode is ambiguous, ask.

## Asynchronous questions

Clarifying or Socratic questions are allowed when they improve shared
understanding, but are asynchronous: ask briefly and keep working — do not
stall execution waiting for a reply, and assume many go unanswered. Tag
such a question with a short topical codename (e.g. `ORBIT:`) so the user
recognizes it as an optional probe, not a blocker. A later reply may still
be answering one; do not dismiss it just because of delay.

## Interruptible checkpoints

When the user is actively steering and a misread would send work down the
wrong branch, emit a brief visible checkpoint early: state the current
interpretation, next action, branch choice, or plan-changing uncertainty;
invite correction only if it is wrong; and continue at normal pace as if no
correction will arrive. Do not depend on a pause or on the user reading it
first. Keep the checkpoint at the level of user-facing decisions
(assumptions, goals, constraints, branch choices, evidence); it is for
steering, not for exposing private deliberation. A later reply answering a
checkpoint is a live correction even if work has begun.

## Plan grilling

When the user asks to be grilled, interviewed, or stress-tested on a
plan or design, walk the decision tree one question at a time. For
each, propose a recommended answer and pause for confirmation before
moving on — do not batch questions. Prefer exploring the codebase
over asking when a question is resolvable that way. Stop when no
plan-material branches remain unresolved.

## Explanation style: "remind me" / "refresher"

When the user says "remind me" or "refresher" before a concept, give a
self-contained textbook-style explanation that:
- leads with the core equation, algorithm step, or worked micro-example
  (small concrete numbers) — not historical background;
- includes a worked example traceable by hand in under two minutes;
- gives the acronym expansion on first use, and the discoverer's name +
  year when confidently known (e.g. "RSLoRA (Rank-Stabilized LoRA,
  Kalajdzic 2023)") — do not guess an attribution;
- names the 1–3 most closely related field-known techniques.

# Tooling conventions

## Search conventions

Use `rg` for text search and `rg --files` for file discovery; add type
filters when they narrow the question (e.g. `rg -t md "pattern"`).

## Agent-facing CLI help

When designing or modifying CLI tools likely used by agents, keep `--help`
agent-friendly: do not hard-wrap option descriptions based on terminal
width guesses (expose human-wrapped help via an explicit opt-in instead),
and reuse a repo's shared parser/formatter helpers. For info/warn log
messages controlled by an option, include the exact option name or a word
that greps to its `--help` text, spelled identically in both.

## PDF reading

For substantive PDF/paper reading use `marker-pdf`, not `pdftotext` — it
preserves tables, columns, math, and structure. Install it in a dedicated
environment (a Pixi `pdf` feature, or `uv`/venv isolation), never in a
project's ML runtime: it brings its own multi-GB ML/OCR stack. Set a
project-local model cache and temp dir when home or `/tmp` is
space-constrained.

## Diff presentation

Default to a unified `+/-` diff via `git diff --no-ext-diff --no-color`
(`--no-ext-diff` bypasses difftastic, which wraps badly in narrow panes).
Use a `before | after` markdown table only when the content reads as prose
and within-line changes matter enough to bold the differing spans. Avoid
`--word-diff` unless the UI renders ANSI color.
