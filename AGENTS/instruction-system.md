# Instruction and project-knowledge details

> Slow-path rationale for instruction authority, routing, project knowledge, glossary placement, and language-policy loading.

Consult the matching named section while authoring or reorganizing agent
instructions, topics, glossaries, or routed policy. `AGENTS.global.md` retains
the binding rules and wins on conflict.

## Authority and instruction files

`~/agents/AGENTS.global.md` is the authoritative global instructions file;
global policy changes belong here first. Harness-global `AGENTS.md` or
`CLAUDE.md` install paths may symlink to it. The repo-local `AGENTS.md` is
instead this checkout's project boot, so launching here does not inject the
global source twice. Keep shared helper scripts under `~/agents/` and `~/bin/`
in sync. When global instructions or those scripts change, make a brief commit
on `~/agents` `master`.

`~/agents` in these instructions means this checkout's root; substitute
the actual path if loaded from elsewhere.

`~/agents/AGENTS.user.md` is a personal supplement — read it alongside
this file every session.

After reading this file and `~/agents/AGENTS.user.md`, read the
provider-specific supplement for your harness when present:
- Codex / OpenAI Codex: `~/agents/AGENTS.codex.md`
- Claude: `~/agents/AGENTS.claude.md`
- GitHub Copilot CLI (`COPILOT_CLI=1`) or a YA Claude Gateway child marked
  `YEP_COPILOT_API=1`: `~/agents/AGENTS.copilot.md`
- Grok / xAI: `~/agents/AGENTS.grok.md`

Harness/backend supplements carry scoped mechanics and behavior patches —
session-log locations, resume identifiers, provider skill paths, launcher
quirks, and backend-specific safeguards — and may route capability and
recorded-model supplements such as `AGENTS.frontier.md`, `AGENTS.opus.md`, and
`AGENTS.sol.md`. Cross-provider policy stays here. If the relevant supplement
is missing or unreadable, report once and continue.

Symlinks and hardlinks to the same target are the same loaded
source for provider-supplement routing.

`~/agents/topics/agent-instructions.md` (and its `.evidence.md`
ledger) carry the reasoning behind these instructions and the
rules for writing new ones. Read it before writing or editing any
agent instruction in any project — whenever the user asks for an
"AGENTS instruction/note/advice/rule", a "global rule", or a
"project(-level) rule" — and on demand when unsure how to safely
follow a rule or when proposing an improvement (welcome from work
in any project, not only inside `~/agents`). Evidence-ledger
conventions are in `~/agents/topics/evidence-ledger.md`.

### Point to authored instruction text

When authoring or editing instruction text — `AGENTS.global.md`, `AGENTS.md`,
supplements, topic docs, glossary rows, skills — identify each important
edit in the reply by project-relative path and the line where the rewritten
range begins (`path:line`). Prefer a browseable read-range tool result for each
rewritten range when the harness supports one; the user is reviewing what was
written, not necessarily a before/after diff. Keep the summary brief and do not
repeat the exact text inline when the range is available. If the current text
cannot be made browseable, paste it verbatim. Mechanically regenerated output
is exempt; text you composed is not.

### Instruction routing

When the user labels a rule, persist it (do not leave it only in chat):
- `global rule` -> `~/agents/AGENTS.global.md`
- `project-level rule` -> repo-local `AGENTS.md`

### Load-bearing instructions

When editing agent instructions, propose cutting entries that don't steer
behavior beyond what a capable agent does by default. Preferences,
project-specific context, and deliberate counters to defaults are
load-bearing; restatements of standard tool mechanics or defaults are not.
Add explicit rules to prevent known project-specific failures; avoid
prompt debt that just replaces ordinary engineering judgment.

The same bar applies to rationale: "good because" prose that doesn't
sharpen the decision surface moves to the relevant `.evidence.md` ledger
(create one if needed) rather than padding the rule or being deleted.

Non-frontier agents occasionally edit these projects, so keep redundancy —
worked examples, and the rationale behind counterintuitive rules — that
stops a weaker agent reasoning its way around a rule, even where a frontier
agent would not need it.

### Project-level instructions

Before using tools in a repo for the first time in a session — at
launch or when work pivots into another project mid-session — read its
root `AGENTS.md`, `AGENTS.local.md`, `CLAUDE.md`, any `README.md` they
name as an instruction source, and every project-owned `PROGRAM.md` found
after those instruction reads. The duty
binds to the repo being acted on, not the launch cwd; the harness
injects nothing for a foreign repo, so these reads are the only way
its rules load. Copy this list rather than recalling it — a
mid-session entry has been observed probing `ls AGENTS.md CLAUDE.md
GLOSSARY.md`, dropping `AGENTS.local.md`, then calling a request verb
"ambiguous" that the unread file defined. An existence probe or a
sliced excerpt does not satisfy the read; files already read this
session are not re-read on later returns. Task files do not
substitute for this. If a file is unreadable or a symlink is broken,
report once and continue.

Every project-owned program charter is deliberately part of project
orientation. Locate and fully read all of them; a root charter may list
significant subprograms for navigation, but that optional list is not a
discovery index. Exclude vendored dependencies and nested external repositories.

When a request targets a project other than the one this session was
launched in, weigh where the work lands best: a fresh agent launched
with the target project as its working directory boots with that
project's instruction stack loaded automatically — generally the
better vehicle for a self-contained task. When this session's prior
context materially informs the work, prefer a context-carrying fork,
or act here after completing the boot reads above. The duty is
identical on every path; a target-cwd launch merely makes it
automatic.

Project instructions are the final word for work inside that project;
`AGENTS.local.md` is its private final amendment. Global instructions
govern actions outside the project. Report material conflicts with unclear
precedence rather than resolving them silently. A committed repo `AGENTS.md`
should stand alone; `AGENTS.local.md` may be a brief delta against global
policy.

#### Local instruction file backups

Before editing or deleting an agent instruction file whose contents are
not safely recoverable from git (especially untracked files like
`AGENTS.local.md`, or tracked files with uncommitted changes), first
snapshot it under `.backups/<YYYYmmdd-HHMMSS>/<relative-path>`.

### Optional supplements

Companion docs hold split-out, opt-in policy:
- `RESEARCH.md` — a short router for substantive research/experimentation;
  binding concern packets live under `RESEARCH/`. Shared field surveys live
  under `~/agents/surveys/<field>/` (`survey.md` map + per-concept
  `concepts/<short>.md` digests) and should be searched before extracting a
  field afresh.
- `RUNS.md` — a short run-operation / `agentctl` router; binding resource,
  provenance, and monitoring packets live under `RUNS/`.
- `feature-branch.md` — branch-per-feature workflow; load when the
  project's `AGENTS.md` names it or the repo plainly uses feature
  branches. Default policy is branch-agnostic without it.

Resolve companion docs at the repo root first, then `~/agents/`. If a
triggered file is missing, report once and continue. Keep reusable
cross-project guidance global (in `~/agents/`) unless it depends on a
specific repo's data, scripts, or schema.


## Project organization

### Convention-owned private directories

When a project convention says a directory is git-excluded by default, add its
path to the repository-local exclude file (`git rev-parse --git-path
info/exclude`, commonly `.git/info/exclude`) **only in the same operation that
creates the directory**, never to `.gitignore`. If the directory already
exists, do not add or restore the exclusion unless the user explicitly asks:
the project owner may have removed it deliberately in order to track the
contents. Creating children or later maintaining the convention is not another
occasion to enforce the default.

### Project topics

For git projects, maintain committed topic docs for cross-cutting contracts:
shared invariants, integration boundaries, and system-level concerns, not
module notes or changelogs. A topic doc holds the repo's evolved truth —
contracts, invariants, knowledge state — and may also carry live plans or
ephemera, so long as they are cleared when addressed rather than accreted;
permanence is not what separates a topic from `tasks/` (§ Session management),
collaborator value is.

Each `GLOSSARY.md` defines a topic scope. The project-root glossary owns
`topics/*.md` (or the alternate `docs/topics/*.md`); a scoped glossary owns
the `topics/*.md` collection beside it. Every named glossary term is
topic-like, including one whose `topic / refs` cell points to an already
located proposal, draft, handoff, or other canonical doc. Resolve that doc
before creating anything. If none exists, create a formal topic doc in the
owning glossary's collection. Create a collection when first needed, not
proactively.

Choose the broadest active glossary scope that naturally owns the concern,
while defaulting creation to the current project. A subtree/program remains
the right owner when a parent-scope doc would mostly use qualified local names
or paths. Promote to a parent glossary only when the concern's real utility
widens across child scopes, and promote to `~/agents` only for clearly reusable
general agent workflow or explicit user direction. Read `~/agents/TOPICS.md`
when creating or assessing a topic's granularity, scope, or durable landing
site.

An optional `PROGRAM.md` beside a `GLOSSARY.md` is that scope's concise charter:
the durable aspirations, themes, and boundaries that explain why its topics
belong together. It is not a plan, progress report, topic index, or activity
log. A nested charter narrows or specializes its parent without restating it.
Read it for scope choice and program-wide orientation. At project entry, read
every project-owned charter, not only the root one. A root charter may point to
significant children but need not maintain an exhaustive index.

“Update program scope” selects the nearest applicable glossary scope, reads an
existing charter or infers the probable one from recent user direction,
glossary terms, canonical topic docs, and repository evidence, then creates or
revises `PROGRAM.md`. “Update all program scopes” discovers existing charters
and glossary scopes whose artifacts support a coherent spanning program, and
applies the same reconciliation independently. Do not manufacture a charter
for a mere vocabulary scope with no inferable program, and do not let the
latest tactical activity silently narrow a durable aspiration.

Read the relevant topic doc and its `.bearings.md` companion if present
before touching code for a bug, committing to a significant plan, entering
a topic's area for the first time in a session, resuming, or responding to
user words like `bearings`, `orient`, `lost`, or a stated recollection of
where work stands. Use the topic contracts to
form the hypothesis, then check it against the trace. Bearings are
orientation, not complete state; synthesize them with live evidence.

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

Read `topics/topic-doc-format.md` (repo-local first, else
`~/agents/topics/topic-doc-format.md`) when creating or normalizing topic
docs, using companion suffixes (`.evidence.md`, `.runs/`, `.bearings.md`,
`.testing.md`, `.sketches.md`), maintaining bearings outlines, or applying
epistemic labels.

### Alternate directory layouts

A repo may keep these conventions under `docs/`: `docs/topics/` in
place of the project-wide root `topics/`, and `docs/tactical/` in place of
`tasks/` and/or `gaps/`. When the root form is absent and the `docs/` form
exists, use the `docs/` form wherever these instructions name the root one —
same duties, read-triggers, and root topic-name namespace — rather than
creating a parallel root directory. Scoped glossaries still own their sibling
`topics/` collections. Content routed to `docs/tactical/` is committed (the
tracked variant of `tasks/`) and follows the local files' format where it
differs from the formats given here.

### Project glossary

`GLOSSARY.md` is the project's shared, prescriptive vocabulary
for talk, planning, code, UI copy, and commits. Before interpreting or changing
a file at a newly entered project work site, locate its nearest-enclosing
glossary and the active chain outward through the project glossary. A targeted
`rg` or row read is sufficient for awareness; defer a full read until broad
vocabulary is relevant. On a glossary read, ensure its sibling `PROGRAM.md`,
when present, has been read this session. When naming a symbol, UI element,
doc heading, or commit topic — or when prose starts spelling out what one term
could carry — reuse glossary terms instead of introducing synonyms. When a
user phrase or pasted log drifts from a glossary term, prefer the glossary's
wording.

In new-reader-accessible docs, briefly spell out project-specific terms at
first use when they could be mistaken for ordinary English. A term lives in
the broadest active glossary scope that naturally contains its uses, while a
nearer row overrides the same term in its subtree. Consult the active glossary
chain before naming or paraphrasing there. The project glossary is the default
creation ceiling; `~/agents/GLOSSARY.md` is the outer scope only for clearly
general agent-workflow vocabulary or explicit user direction.

When a user phrase is ambiguous and the resolution would change
action, emit an interruptible checkpoint with the inferred meaning
plus 1–2 alternatives. On resolution, propose a glossary row
flagged `<!-- unconfirmed: YYYY-mm-dd -->`. When the user
explicitly introduces a distinction ("by X I mean Y, not Z"), add
the row immediately. When a row is clearly general-domain —
recognizable outside this project — surface it once as a
candidate for `~/agents/topic-definitions.md` or
`~/agents/TOPICS.md`; do not edit those global files autonomously.

Read `topics/glossary.md` before adding, regenerating, sorting, or
promoting glossary rows, creating scoped sub-glossaries, resolving
ambiguous terms, or deciding whether a vernacular row should become a
topic doc. Create `GLOSSARY.md` when the project has more than one topic
doc or when project jargon starts recurring; not proactively.

## Language tooling

Language-specific tooling is loaded on demand, not inline here. Before
editing a file in one of these languages, or when first working in a
project that uses it, read the matching doc if present — repo-local
`topics/<lang>.md` first, else `~/agents/topics/<lang>.md`:

- C / C++ — `cpp.md`
- Python — `python.md`
- TypeScript / JavaScript — `typescript.md`
