# Session management

Session continuity is primarily resume-by-session-id plus live state
(active sessions, `tasks/*.md`, run metadata). `/hi` and `/bye` are an
optional manual save/restore pair, mainly worth reaching for when a
session is too full or corrupted to resume normally. Recover prior
context only on a greeting or explicit resume signal — a fresh, specific
request is independent.

`tasks/*.md` files track per-task direction, coordination, acceptance
notes, and unfinished session state. Whether `tasks/` is git-ignored is
the customization point: ignored (the default here) means task files are
private working state — never commit them and stay branch-agnostic;
tracked means the feature-branch workflow (committed task files, branch
per task). The active root task is named by `tasks/ROOT` (a one-line
pointer holding its filename); update it when a new root task begins —
rarely. Prefer
opening or updating a committed `topics/` doc for durable conclusions,
contracts, and project-facing knowledge. Create or extend a task file
when private direction-setting, handoff state, or an active-work
scratchpad would make the work easier to resume or coordinate. Read the
active root task when resuming. On believed completion, append a dated
status note with the relevant commit(s) and one line of evidence; if the
task file has inline subtasks, make it a section listing each subtask's
status. Judge each task file in isolation — no recursing into linked
subtask files.

For implementation or bugfix work, search `tasks/*.md` when that directory
exists, and cite the relevant file(s) in planning and conclusion. Task
files should cross-reference relevant `topics/*.md`.

## Active sessions

On the first planning-to-act step in a shared workdir, write
`.agentctl/active/<session-id>` with a short present-tense status line.
Create `.agentctl/active/` if missing — autocreate is mandatory, not
optional courtesy. Update at each milestone, after 10+ min of
continuous work, or at the 60-min heartbeat cap — whichever comes
first. On completion start the file with `DONE`, preferably
`DONE: <one-line summary>`. Readers must treat files starting with `DONE`
(`DONE*`) as complete. Pure read-only or interview sessions: skip.

File schema: line 1 is the present-tense gist (self-contained,
readable on its own). Line 2 may declare scope as `scope: <paths>` —
a space- or comma-separated list of project-root-relative paths,
each either a plain path or a path with a trailing `**` (e.g.
`packages/client/**`), for tool-detected overlap with peers. Glob
patterns beyond trailing-`**` need a glob-aware consumer and are
noise to prefix-match readers; reach for them only when narrowing
by suffix or pattern is genuinely the point. Anything beyond line
2 is free content at agent discretion (plan notes, considered
approaches, longer status). Brief readers stop after line 2.

Active sessions are a separate artifact — task-file status, run logs,
and commit status do not satisfy this. Always attempt to discover
the provider's real resumable session id before falling back to a
personal tag — the provider supplement carries the discovery
snippet for each harness. A personal tag is a last resort; do not
skip the discovery attempt for convenience. Once chosen, reuse
the same id or tag across compaction or resume.

Check for active peers with `find .agentctl/active -maxdepth 1
-type f -mmin -70`. Older files that do not start with `DONE` are
stale/crashed.

`agentctl` maintains your entry automatically. It adopts your
session id from `AGENTCTL_SESSION_ID`, else a harness-provided var
your supplement names (Claude: `CLAUDE_CODE_SESSION_ID`), so no
manual step is needed. On `start`/`smoke`/`restart` it refreshes
mtime and appends a free-text launch note, creating the entry with
a placeholder line 1 if absent (overwrite it). It never rewrites
your line 1 or `scope:` line 2, never touches a `DONE`-prefixed
entry, and never lets a launched job adopt your identity (an
internal launch-depth counter, so jobs cannot masquerade as your
session).

To author or re-scope your entry without launching a job, use the
run-free `agentctl active` verb (no job, dump, or log) — e.g. to
declare intended-edit scope for peer overlap detection:

    agentctl active "wiring the active verb" agentctl.py topics/agentctl.md

This sets line 1 to the banner and line 2 to `scope: agentctl.py
topics/agentctl.md`, preserving any free content below; with no
path args it leaves an existing `scope:` line in place. A leading
`DONE` in the banner marks completion. The launch-depth guard still
applies, so a launched job cannot author your entry. This is a
convenience over hand-writing the file, not a new requirement — the
file remains an ordinary text artifact you may edit directly.

## Resume source priority

A handoff or context-compression message as the first turn means `/bye`
did not run before the handoff. If it carries a link/session id, browse
that session to catch up — scan for commit/topic boundaries and read
the last two sections closely.

When resuming after a disconnect, crash, restart, or compaction,
recover from live state first: worktree, the active root task
(`tasks/ROOT` names it if present, else newest `tasks/*.md` by
mtime, even if git-ignored), `.agentctl/active/`, run metadata,
artifacts, then provider session logs. With no `tasks/ROOT`, a
recently modified `*.bearings.md` is a useful "what is this even
doing" orientation fallback. A `last-session.md` newer than that
live evidence may be offered as an optional restore step; never
treat it as authoritative.

# Verification and retrieval

Verify claims about a project against the repo before relying on them;
treat user and agent assumptions as hypotheses until checked. `rg` is
available.

When entering an unfamiliar area of code, build a higher-level map
first — relevant modules and callers in the project's glossary
vocabulary — before drilling into a specific function. Deep
inspection follows the map, not the other way around.

# Authority and instruction files

`~/agents/AGENTS.md` is the authoritative global instructions file;
global policy changes belong here first, even when a repo-local
`AGENTS.md` / `CLAUDE.md` symlinks or copies it. Keep shared helper
scripts under `~/agents/` and `~/bin/` in sync. When global instructions
or those scripts change, make a brief commit on `~/agents` `master`.

`~/agents` in these instructions means this checkout's root;
substitute the actual path if loaded from elsewhere.

`~/agents/AGENTS.user.md` is a personal supplement — read it alongside
this file every session.

After reading this file and `AGENTS.user.md`, read the provider-specific
supplement for your harness when present:
- Codex / OpenAI Codex: `~/agents/AGENTS.codex.md`
- Claude: `~/agents/AGENTS.claude.md`
- Grok / xAI: `~/agents/AGENTS.grok.md`

Provider supplements carry harness mechanics only: session-log locations,
provider resume identifiers, provider skill paths, and launcher quirks.
Cross-provider policy stays here. If the relevant supplement is missing or
unreadable, report once and continue.

Symlinks and hardlinks to the same target are the same loaded
source for provider-supplement routing.

`~/agents/topics/agent-instructions.md` (and its `.evidence.md`
ledger) carry the reasoning behind these instructions. Read on
demand — when unsure how to safely follow a rule, or when
proposing an improvement (welcome from work in any project, not
only inside `~/agents`). Evidence-ledger conventions are in
`~/agents/topics/evidence-ledger.md`.

## Instruction routing

When the user labels a rule, persist it (do not leave it only in chat):
- `global rule` -> `~/agents/AGENTS.md`
- `project-level rule` -> repo-local `AGENTS.md`

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

## Optional supplements

Companion docs hold split-out, opt-in policy:
- `RESEARCH.md` — research method; load before substantive
  research/experimentation work (notebooks, train/eval, significance
  claims, paper/report drafting). Also names the survey-field and
  research-frontier templates.
- `RUNS.md` — run-operation / `agentctl` policy; load before
  launching/monitoring/summarizing long-running jobs.
- `feature-branch.md` — branch-per-feature workflow; load when the
  project's `AGENTS.md` names it or the repo plainly uses feature
  branches. Default policy is branch-agnostic without it.

Resolve companion docs at the repo root first, then `~/agents/`. If a
triggered file is missing, report once and continue. Keep reusable
cross-project guidance global (in `~/agents/`) unless it depends on a
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

When a review step is part of the same request as a push or deploy,
sequence as: review → fix → push. Do not push first and review after.

The bracketed-tag style is encouraged for other self-imposed gates; it is
required only for the full gate record.

# Ancillary workdir hygiene

When working in an ancillary worktree or scratch checkout, do not
put it on reboot-cleared storage (`/tmp`, tmpfs); use durable
storage — a sibling directory of the primary workdir, on the same
filesystem, is a good default. Before transferring content back to the primary workdir,
verify source and destination branches match, and stash or
formally commit (or amend) first — a committed state is the only
safe transfer unit. Do not rely on default agent caution here.

# Hot-reload / live-interpreted projects

When a project's running process re-reads source on save (dev server,
nodemon, watcher-driven build, live REPL/notebook session), a related
series of edits must not leave the live tree in a state that crashes
that process between writes. The watcher observes each write; the
contract covers the sequence of observed states, not only the final
one.

Choose any mechanism that satisfies the contract — make each
intermediate state self-consistent, pause/stop the watcher across the
batch, stage and transfer together. Before applying a batch built
against earlier reads, verify the target files have not drifted from
those reads.

# Pre-edit re-Read and parallel-worker noticing

Re-Read a file before the next Edit when enough time has passed
since your last Read of it for a parallel worker to plausibly have
intervened — across a context compaction, a multi-turn user
exchange, or when returning to a file you Read earlier in the
session. One Read followed by several rapid Edits to the same file
is fine and efficient; this rule covers the slower gaps.

Detecting peer-agent intervention is cheap now that
`.agentctl/active/` is the agreed convention: `find
.agentctl/active -mmin -70` answers "any peers in this tree?" in
one call. The remaining intervention path is a direct user edit,
which the re-Read itself surfaces. On detected divergence, pause
and report what you were about to change; do not revert, overwrite,
or auto-reconcile. Same goal as a peer: leave the worktree intact.
Different goal: retry the Edit against the new content.

# Edit mechanism discipline

For any change that could or should be an ordinary edit, the
structured edit tool (`Edit`/`apply_patch`) is the mechanism. Never
substitute `sed`/`perl`/`python`/here-doc in-place rewrites for a
normal edit in order to dodge an approval prompt, a permission mode
(e.g. 'Ask'), or a temporarily blocked edit tool. Choosing a more
error-prone mechanism to slip past a gate is forbidden — the gate
exists precisely for the change you are trying to make. A blocked
edit tool means the edit needs approval or a fix, not a quieter route
around it.

If the normal edit tool cannot be used — permission mode, a sandbox
or environment error, a broken helper — first try to solve it
head-on: request the edit through the prompt, or fix the environment
fault. If it cannot be solved head-on, raise it to the user once and
stop; this is exactly the execution-context limitation you state
plainly (see *Execution-context limits*), not one you engineer
around with riskier tooling. A giant `perl -0pi -e q~...~` block
replacement of a multi-line function — brittle, unverifiable, silent
on a whitespace drift — is never the right answer to "the edit tool
asked for permission."

Shell text transforms remain the right tool when they genuinely are:
mechanical rewrites fanned across many files, `clang-format-diff`,
codemods. The line is intent — a bulk transform that is awkward as
hand-edits is fine; a single targeted edit re-expressed as a shell
substitution to avoid a prompt is not.

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

The message has two usually-aligned purposes: orienting a reviewer now, and
letting a later reader (`git blame`, a `bisect` bug-hunt) validate a diff
hunk against the stated intent and result. Both are served by describing
purpose and outcome — enough that an agent told to achieve this message would
produce a similar diff, and that every group of files in the diff is
explained by something in the text. Neither is served by a journal of how the
change was reached: omit iteration narrative, superseded approaches that left
no trace in the tree, and added-then-reverted churn.

Consider splitting unrelated changes into independent commits (e.g.
implementation vs. research finding).

### Amends

When amending: keep the subject; treat the message as additive or
corrective (do not erase prior content); describe only what changed
relative to `HEAD~1`. Prefer amend over a correction commit while
local; never amend after a PR has been opened elsewhere. Full
procedure in `topics/commits.md`.

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
  `GLOSSARY.md` (contribution rules in `~/agents/topics/glossary.md`);
  keep single-use facilities close to their use.
- Keep run logs greppable: tag every line of a phase with the phase name
  (`WARMUP: ...`), rather than bracketing a span (`[start WARMUP]` /
  `[end WARMUP]`) or relying on indentation.

# Project organization

## Project topics

For git projects, maintain committed `topics/*.md` docs explaining
cross-cutting concerns that must hold relative to the whole
system. Basenames are the `Topic:` trailer namespace (`ls
topics/*.md`). Create `topics/` when first needed, not
proactively.

Topics map to *concerns* — cross-cutting contracts, shared
invariants, integration boundaries, security/performance
properties — not to modules or directories. A doc describing one
module with no external consumer is a README section. A topic doc
names contracts, invariants, assumptions, dependencies, and edge
cases; it is not a changelog. For granularity calibration and a
topic-name vocabulary, read `~/agents/TOPICS.md` when creating or
assessing a topic.

Format of a topic doc (H1 + `> ` lede + `Topic:` trailer + body),
companion-suffix vocabulary (`.evidence.md`, `.runs/`,
`.bearings.md`, `.testing.md`), bearings-outline glyphs, and
epistemic-labeling markers all live in
`topics/topic-doc-format.md`.

**Active use**: before touching code for a bug, before committing
to a significant plan, or when entering a topic's area for the
first time in a session (including on resume), read the relevant
topic doc and its `.bearings.md` companion if present. The topic
doc's contracts tell you what must be true and therefore where a
violation must live — form a hypothesis that satisfies the
invariants, then check it against the trace, not the reverse.
Synthesize bearings against recent live evidence (dirty files,
recent topic edits, task files, run records, git history, live
`.agentctl` state) — the bearings file is not the whole state.
Additional read triggers: user says `bearings`, `orient`, `lost`,
or states a recollection of where work stands.

Some `topics/` entries are method/discipline docs (e.g.
`debugging.md`, `testing.md`, `prototyping.md`); load them at the
verb-trigger (before diagnosing, before designing tests, before
building a prototype), not only when the noun-shaped concern-doc
rule fires.

Before finalizing a non-trivial commit message, read the topic
docs for the changed concern and decide whether a `Topic:` trailer
is needed. If the change touches a cross-cutting contract with no
topic doc, create or update one (prefer a section in a related
topic over a new file). Check whether the diff falsifies or
weakens any claim it touches, and design boundary tests around the
contract it could violate.

## Project glossary

`GLOSSARY.md` is the project's shared, prescriptive vocabulary
for talk, planning, code, UI copy, and commits. Read on first
repo use alongside `AGENTS.md`. When naming a code symbol, UI
element, doc heading, or commit topic — or when prose starts
spelling out in several words what one term could carry — check
the glossary first and reuse an existing term rather than
introduce a synonym or paraphrase. When a user phrase or pasted
log drifts from a glossary term, prefer the glossary's wording.
If `GLOSSARY.md` has fallen out of context (deep session,
post-compaction), `rg` it before proposing a new row.

In any new-reader-accessible doc, briefly spell out a glossary
term at first use when the term is project-specific or could be
mistaken for ordinary English. Do not expand obvious general-
domain terms or terms whose definition is supplied by adjacent
context.

Most glossary rows are vernacular forever; a row becomes a
`topics/<name>.md` only when it meets the cross-cutting-concern
bar in `~/agents/TOPICS.md`.

**Scoped sub-glossaries**: a term lives in the `GLOSSARY.md` at
the narrowest enclosing directory; create the file if missing.
Promote a row to a parent's `GLOSSARY.md` as the term's scope
widens; the root is the terminal scope. Before naming or
paraphrasing in a subtree, consult the nearest-enclosing
`GLOSSARY.md`.

When a user phrase is ambiguous and the resolution would change
action, emit an interruptible checkpoint with the inferred meaning
plus 1–2 alternatives. On resolution, propose a glossary row
flagged `<!-- unconfirmed: YYYY-mm-dd -->`. When the user
explicitly introduces a distinction ("by X I mean Y, not Z"), add
the row immediately. When a row is clearly general-domain —
recognizable outside this project — surface it once as a
candidate for `~/agents/topic-definitions.md` or
`~/agents/TOPICS.md`; do not edit those global files autonomously.

Format, regeneration, and the design rationale for these
conventions live in `topics/glossary.md`. Create `GLOSSARY.md`
when the project has more than one topic doc or when project
jargon starts recurring; not proactively.

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

Avoid formulaic excitement, performative curiosity, or plucky affect; state
observations, uncertainty, risk, and next action directly. This governs style,
not substance: genuine investigation, probing, and clarifying questions are
unaffected.

## Discussion vs. execution boundary

When a conversation is in research, design, or discussion mode, treat
the move to execution (web fetches, file writes, code changes, commands)
as a meaningful checkpoint: ask before crossing it unless the user's
most recent turn already authorized that specific step.

A question is a real gate only when the answer would change the action.
"Want me to do X?" when X is clearly right and low-risk is social hedging,
not a gate — it creates attention debt without giving the user meaningful
control. State what you are doing instead; reserve the question form for
genuine branch points where a wrong assumption would waste significant work.

## Plan-boundary checkpoints

A *plan boundary* is a plan node designated as a momentum checkpoint:
by default the top two tiers of an agreed `.bearings.md`/task plan,
with deeper nodes promotable and shallow ones demotable by marking
them `‖`. The agent maintains these markers; the user does not type
glyphs.

- **At a boundary:** state what is done, name the next boundary, and
  await go-ahead. One queued "proceed" clears one boundary, so each
  pause should be worth a blind greenlight.
- **Below a boundary** (discovered sub-steps, leaves): keep momentum
  and do not solicit permission; state direction inline and continue.

This governs momentum pauses only: the big-effect command gate still
applies at any tier, and the interruptible-checkpoint rule can still
pause below a boundary when a wrong assumption would waste significant
work. A boundary set counts only when agreed before an unattended run;
an agent-invented mid-run outline does not manufacture boundaries.

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

## Queued-send time separators

A harness may inject `--- (Ns ago)` ahead of the first chunk of
a queued user turn, and `--- (Ns later)` between chunks. The
leading "Ns ago" counts seconds from composition to the moment
this prompt was rendered — no separate anchor like "previous
turn end" is named, since flush-time anchors break under
autonomous-multi-turn and deferred-queue-during-turn flows where
a chunk's submit can predate the most recent turn. The
inter-chunk "Ns later" counts seconds from the previous chunk's
submit time. Steering messages carry no separator.

A large N on the leading separator means composition predates
prompt-render by that much; the chunk may have been queued
through one or more agent turns. Read the chunk's content to
judge whether it continues, refines, or shifts from the
preceding context.

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

## Agent-chosen implementation paths

When the user explicitly leaves an implementation path to the agent
("your call", "up to you"), call out the chosen path and a brief reason —
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

## Doubt triggers

On `/doubt` or when the user says they doubt, distrust, are
unconvinced by, or want a clean re-check of a conclusion, load
`skills/doubt/SKILL.md` and run a doubt pass. The target is the
conclusion just applied unless the user names another. The
trigger does not override execution, tool-use, or big-effect
gates.

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

On "grill me" / "interview me" / "stress-test this plan", see
`topics/plan-grilling.md`: one branch at a time, recommend an
answer, pause for confirmation.

## External systems and vendor guidance

When writing setup or operator docs that include vendor-specific steps:
- Only present paths the vendor actually supports on the plan being
  recommended. Omit uncertain options entirely; a confident hedge is
  worse than an omission — readers will follow it and lose time.
- Do not assert specific UI navigation paths (labels, menu structure)
  from training data. Vendors relabel and rearrange without notice. For
  live guidance, ask the user to describe what they see; for committed
  docs, describe intent rather than exact labels.
- When updating a step for a vendor UI change, just update the label.
  Do not add parentheticals explaining old terminology to hypothetical
  readers of stale material.

## Explanation style: "remind me" / "refresher"

On "remind me X" / "refresher on X", see
`topics/explanation-style.md`: worked micro-example first, acronym
expansion on first use, named prior art, no historical lead-in.

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
