# Session management

This is the always-loaded, binding global policy. Do not routinely load the
slow-path packets under `AGENTS/`: they retain rationale, examples, and rare
mechanics for matching named sections. This file wins on conflict.

A routed file read before compaction is not thereby protected. After compaction
or resume, obey this file's current read trigger at the next governed action
boundary even if summarized history says the file was read earlier. Unless a
boot-loaded harness/model/effort supplement states an evidence-backed cadence,
skip that refresh only when the harness is verified to reconstruct the exact
current routed packet in model context.

Session continuity is primarily resume-by-session-id plus live state:
worktree, active sessions, `tasks/*.md`, run metadata, and artifacts. `/hi` is
an optional explicit resume tool; do not invoke it merely because context
compacted or instructions were reinjected. Recover prior context only on a
greeting or explicit resume signal; a fresh specific request is independent.

`tasks/*.md` records private direction, coordination, acceptance notes, and
unfinished state. `tasks/ROOT` names the default handoff used only for a bare
`/hi` or boot with no specified scope; it does not select which artifact active
work maintains. Change it only when explicitly establishing a new default
bare-boot target. Prefer committed `topics/` for knowledge that would help a
collaborator. Use `tasks/` only when that test fails or material must stay
private. When committing an incomplete shared artifact, commit an honest
status/cutoff with it so the artifact cannot mislead; private task state alone
is insufficient. A project that tracks `tasks/` instead follows its tracked-task
convention.

For implementation/bugfix work, search existing `tasks/*.md` and cite relevant
files in planning and conclusion. Task files should point to related topics.
On believed completion, append a dated status with commit(s), one line of
evidence, and inline-subtask statuses. Judge each task file independently.

Dated task/tactical/journal progress entries name the contributing model using
the `Contributing-model:` short form. Topic docs do not. Prefer a real session
id to hand-counted effort statistics.

## Handoff audience

A handoff or persistent plan writes for exactly the user and a fresh agent of
similar capability with no shared context. Preserve the compiled understanding:
load-bearing constraints, ruled-out paths and why, the crux, and unfinished
state. Restate context unless a specific cited artifact is one the receiver will
actually open. Do not waste an `Audience:` line restating this rule. Outward
reports retain their own reader model.

When a resumed handoff starts with `/goal X`, process that line as a separate
user turn immediately preceding the remaining handoff, which is the following
request.

A handoff that relies on a durable advisor-type co-session records its logical
metadata path and every serving incumbent's verified canonical durable harness
resume id immediately after the optional `/goal X` line. When a public address
or provider-native handle differs, the local address records each available
identity. If the durable id is not yet recoverable, record that fact and the
best durable address instead. An instruction to consult the advisor also
carries a stable intake id. `topics/handoffs.md` owns the repeatable syntax,
session-id check, deduplication, completeness-review packet, and treatment of
advisor claims.

Before creating or updating a handoff, read `topics/handoffs.md` (repo-local,
else global). Maintain the handoff already governing the work only at
significant milestones that make its state or next step materially false, not
between routine edit/build/test actions. When no artifact governs material
unfinished work, that topic chooses between a project gap and private
`tasks/auto-handoff-<slug>.md`, while non-blocking candidate improvements stay
in the owning topic's `.sketches.md` companion or an established plan;
`tasks/ROOT` is irrelevant to this choice.

## Active sessions

On the first planning-to-act step in a shared workdir, register
`.agentctl/active/<real-resumable-session-id>`. Recover the provider's actual id
using its supplement; never invent an id where transcript/provider state can
recover one. Line 1 is a present-tense gist; optional line 2 is
`scope: <paths/globs>`. Refresh at milestones, after ten minutes of continuous
work, and at least hourly. On completion, line 1 begins `DONE`.

Pure read-only/interview sessions may skip registration. At caution points,
recheck active peers rather than carrying an old belief:

```bash
agentctl others <session-id>
```

Exit 0 means alone; nonzero names peers. `agentctl alone <id> -b "<status>"`
waits for project-wide solitude, then registers the caller; scope does not
narrow that wait. Steward sessions add `tending:` and claim through
`agentctl tending <id>` before clearing/servicing a queue.

Read `topics/agentctl.md` before changing or diagnosing active-session/run
semantics, `agentctl`, staleness/sweep behavior, launch-depth guards, or plugin
contracts. Detailed file schema and examples remain there and under “Active
sessions” in [AGENTS/session.md](AGENTS/session.md).

## Resume source priority

After disconnect, restart, compaction, or crash, keep any already-known work
scope; compaction alone does not trigger `/hi`. For a named resume, use the
named handoff/task. Only a bare `/hi` or boot with no scope reads `tasks/ROOT`
first as a discovery hint. Then reconcile against live state: worktree and
recent commits; `.agentctl/active/`; run/on-deck state; artifacts; then provider
logs needed to fill a specific gap. A recent relevant task/auto-handoff or
`*.bearings.md` can orient when the first hint is missing, broken, or unrelated.

If a first-turn handoff/context-compression message gives a session link/id,
inspect that session, scanning boundaries and reading the last two sections
closely.

## Scheduled session prompts

Once at the start of each ordinary new/resumed project session, cheaply check
that project's existing `at/` for due `*.md` prompts. Do not create `at/` to
probe, probe `~/agents/at/` from another project, or repeat this in an at-launched
runner.

Claim only through executable project `scripts/at-queue`, else
`~/agents/scripts/at-queue`. Pass project root, canonical session id, harness,
and an owner PID that outlives the claim; use the exact source path returned.
If neither helper exists, skip rather than hand-roll a claim.

Before invocation, read project `topics/at-scheduling.md`, else
`~/agents/topics/at-scheduling.md`.
The source file is inert; the helper-owned, clone-local activation store is what
schedules it. Never hand-edit that store. Any YA/multi-project scheduler must
call the helper and derive cwd from the owning `at/` directory. Slow-path
activation/acknowledgement mechanics are in `topics/at-scheduling.md`.

# Verification and retrieval

Verify project claims against the repository. Before voicing a specific,
cheaply checkable fact about the user's system/tool/config—path, default, flag,
schema—check it instead of presenting memory or agreement as fact. Treat user
preferences and direct observations as authoritative; treat causal guesses as
hypotheses.

When entering unfamiliar code, first map relevant modules/callers in project
vocabulary, then drill down. Before a wide change, audit, or edit to an
uninspected file, read the full file or full relevant module/section, not
isolated snippets that hide callers and guards.

## Delegation

Delegation is optional judgment unless a higher instruction requires/forbids
it. Keep planning, the core investigation trace, and final synthesis in the
parent. Never send implementation to a lesser model than the session's.

Delegation is flat, depth 1: a leaf reports to its creator and does not spawn.
Useful shapes are independent fan-out, a sequential fold over bulky homogeneous
items, and a standing advisor/oracle. Re-engaging the same leaf is allowed.
Do not fold away reasoning the parent must own.

A task journal starts untracked in `tasks/journals/`. Most journals feed a
commit message then are discarded. Publish none automatically. A durable one
is condensed/redacted and reviewed into `topics/journals/` or a `journals/`
directory beside its plan. Journals also record dated requirement/spec changes,
marked user-directed or agent-derived.

## Standalone bug-report intake

For a new/unrelated defect report, read `topics/handling-bug-reports.md` before
deciding whether this tree needs change. Credibly accept that the observation
occurred while checking whether the exact defect exists here now. A correction
inside active implementation is part of that feedback loop, not standalone
intake. Diagnose without implementing when the user asked only for diagnosis.

# Authority and instruction files

`~/agents/AGENTS.global.md` is the authoritative global source; global policy
changes land here first. Harness-global `AGENTS.md`/`CLAUDE.md` paths may
symlink to it. This checkout's root `AGENTS.md` is only its project boot.
`~/agents` means this checkout root. Keep shared helpers under `~/agents/` and
`~/bin/` synchronized and make a brief local commit on `master` when changing
global instructions/helpers.

For YA-launched sessions, trust present `YEP_AGENT_HARNESS`,
`YEP_AGENT_INITIAL_MODEL`, `YEP_AGENT_INITIAL_EFFORT`, and
`AGENTCTL_SESSION_ID` values as launcher-recorded facts. Use the harness marker
for supplement routing; initial model and effort remain launch facts after a
mid-session change. Query provider state or logs only for a required fact that
no present marker supplies.

Read `AGENTS.user.md` every session. Then read the matching harness supplement
when present:

- Codex: `AGENTS.codex.md`
- Claude: `AGENTS.claude.md`
- Copilot CLI or YA Copilot backend: `AGENTS.copilot.md`
- Grok/xAI: `AGENTS.grok.md`

Harness supplements own session ids/logs, skill paths, launcher quirks, and
backend safeguards, and may route model supplements. Cross-provider policy
stays here. Report a missing/unreadable applicable supplement once and
continue. Symlink and hardlink aliases to the same source route identically.

Before writing/editing any agent instruction, global/project rule, supplement,
skill, glossary row, or instruction topic, read
`topics/agent-instructions.md` and its evidence ledger; follow
`topics/evidence-ledger.md` for ledger changes. Optional pre-compression
clarification is grouped by activation concern under `AGENTS/`.

## Point to authored instruction text

When reporting authored instruction text, identify each important range by
project-relative `path:line` where it begins. Prefer a browseable read range;
otherwise paste the composed text verbatim. Keep the summary brief. Mechanically
generated output is exempt.

## Instruction routing

Persist labeled rules:

- `global rule` → `~/agents/AGENTS.global.md`
- `project-level rule` → repo-local `AGENTS.md`

## Load-bearing instructions

Keep only text that changes capable-agent behavior: user preferences,
project-specific context, deliberate counters to defaults, and rules preventing
observed failures. Move rationale that does not sharpen a decision surface to
the evidence ledger. Preserve examples/redundancy that stop weaker agents
reasoning around counterintuitive rules. A routed main file retains its trigger,
action, and persistence span; supplemental clarification never becomes the
only place a binding rule exists.

## Project-level instructions

Before first tool use in any repo this session—also after pivoting to a foreign
repo—fully read, when present:

1. root `AGENTS.md`;
2. `AGENTS.local.md`;
3. `CLAUDE.md`;
4. any README named by those as instruction source; and
5. every project-owned `PROGRAM.md`, located after reading the instruction
   files above.

Program charters are concise project orientation; fully read all of them rather
than assuming a root charter lists every subprogram. Exclude vendored/external
repositories. An existence probe/slice and task files do not satisfy these
reads. Do not reread on later returns in the same session. Report an
unreadable/broken file once.

When an unfamiliar subdirectory's purpose, placement rules, or local
conventions remain unclear, read the nearest `README.md` in that directory or
its ancestor path before guessing. This is an on-demand fallback, not a startup
sweep of every README; scoped instruction precedence above remains unchanged.

A self-contained foreign-repo task is often better launched with that repo as
cwd; otherwise carry context and perform the same reads here. Project
instructions are final inside that project; `AGENTS.local.md` is its private
final amendment. Global policy governs outside it. Report material precedence
conflicts rather than silently resolving them. A committed project
`AGENTS.md` stands alone.

### Local instruction file backups

Before editing/deleting an instruction file not safely recoverable from Git
(especially untracked or dirty `AGENTS.local.md`), snapshot it under
`.backups/<timestamp>/<relative-path>`.

## Optional supplements

Resolve triggered companions at repo root first, then `~/agents/`. Report a
missing one once and continue. Re-read the binding main at the governed action
boundary after compaction/resume unless the harness verifiably reconstructs
that exact current packet or a boot-loaded scoped supplement explicitly sets an
evidence-backed cadence; summarized recollection is insufficient.
`AGENTS/` detail is optional and this main wins. Routed RESEARCH/RUNS packets
are binding for their named conditions; their short indexes own routing and
win on packet conflict.

- `RESEARCH.md` — before substantive research/experimentation, paper/report,
  field-survey/prior-art/direction-ranking, significance/comparison, or
  research-advisor work. It is a short router. Compaction-durable high-value
  routes are:
  - research paper/log/program/result-table/progress-report work →
    `RESEARCH/artifacts.md`;
  - field survey, prior art, direction ranking, or a material advisor decision
    → `RESEARCH/direction.md`;
  - a newly wired experimental result, train/eval/gate summary, comparison, or
    significance claim → `RESEARCH/evidence.md`; and
  - an untuned elaborate arm, multi-difference attribution, or closure of a
    substantial weak/surprising line → `RESEARCH/judgment.md`.
- `RUNS.md` — before using local accelerators or launching, monitoring, waiting
  for, or summarizing tracked/long-running jobs. It is a short router:
  - Python that may import an accelerator stack or GPU-capacity allocation →
    `RUNS/resources.md`;
  - an important saved output, in-flight record, or row-wise transformed
    dataset → `RUNS/provenance.md`; and
  - a session-outliving launch, foreground wait, monitor/summary, or run-policy
    failure reconstruction → `RUNS/monitoring.md`.
- `feature-branch.md` — when project instructions name it or the repo plainly
  uses feature branches; otherwise stay branch-agnostic.
- `AGENTS/` — optional slow-path detail only for a matching named section or a
  rare ambiguity. Do not load the directory indiscriminately:
  - handoff/session registration/resume/scheduled prompt → `AGENTS/session.md`;
  - unfamiliar-code investigation/delegation/standalone defect →
    `AGENTS/investigation.md`;
  - instruction/topic/glossary/language-policy authoring →
    `AGENTS/instruction-system.md`;
  - gated or destructive action/shared-worktree edit/commit/quality mechanics
    → `AGENTS/change-delivery.md`; and
  - a named interaction or tool-use edge case → `AGENTS/interaction-tools.md`.

Reusable cross-project policy belongs in `~/agents/` unless dependent on a
specific repo's data/scripts/schema.

# Big-effect command gate

Use a **full gate record** before push/force-push/deploy/migration/dependency
upgrade, destructive filesystem action, or wholesale replacement of
user-written content. Local commits/amends use a **light check**: confirm staged
scope and, for amend, preservation of prior message. New scratch/log/tmp files
not shown to the user are exempt.

The full record, before action:

1. state action and why gated;
2. list bracketed checks with current facts/blocks;
3. prefix later multi-step actions with matching tags;
4. show the exact command/action;
5. quote policy only for destructive/forceful/ambiguous/unusually risky cases
   or on request; and
6. stop on any missing/ambiguous required check.

A justified force push uses
`git push --force-with-lease --force-if-includes`, never bare force. Pin the
lease to an expected SHA when appropriate. A force push of shared/default
history still requires explicit user go. Full mechanics: `topics/commits.md`.

Every push, PR, or publish action includes `[no-attrib]` and scans outgoing
messages plus publish arguments:

```bash
git log --format='%H %B' @{u}..HEAD |
  rg -i 'co-authored-by|generated with|noreply@|🤖'
```

No match passes. Inspect prose hits; strip every real `Co-Authored-By` trailer
or generated-with banner by its named SHA. `Contributing-model:` is sanctioned
and remains. A marked pushed commit is rewritten and lease-force-pushed; shared
history waits for explicit go. Use the advisory rewrite lock for multi-command
strips. `scripts/pre-push-no-attrib` may backstop but never replaces the scan.
With no upstream, scan the actual outgoing range.

When review and publish are one request: review, fix, then publish.

# Shared-workdir discard ban

Never use repo-wide work-discard or head-moving commands in a shared workdir:
`git reset --hard`, `git clean`, broad checkout/restore, backward reset,
`git switch`, `gh pr checkout`, bypassed hooks, bare stash, or staging sweeps
such as `git add -A`/`git add .`. Never capture peer/user dirty work in a commit.
Never force-push shared/default history without explicit user authorization.

A requested stash is path-scoped:
`git stash push -m '<why>' -- <paths>`. Restore with `apply` and verify before
any separately authorized drop; never `pop` or clear. Review branches/PRs with
diffs or a dedicated worktree, not by moving shared HEAD.

Repair history/index while preserving the worktree: inspect status/reflog, make
a path-scoped temporary commit/stash, use a separate worktree, or revert
forward. A discard command runs only when the user explicitly requests that
exact operation after being warned, and is narrowed to named paths. Use
`git restore -- <path>`/`git checkout -- <path>` with `--`.

Shared projects should launch through `agent-guarded`. If `AGENT_GUARD` is
unset, warn once. Contract and deployment: `topics/agent-guard.md`.

# Never reach system-wide

Never use `/` as an operation's scope/root (`find /`, `grep -r /`, `du /`)
without explicit permission. A specific absolute path is fine.

# Ancillary workdir hygiene

Put scratch/ancillary worktrees on durable storage, preferably a sibling of the
primary worktree, never reboot-cleared `/tmp`/tmpfs. Before transferring back,
verify source/destination branches match and make the source a committed unit
(or narrowly stash first); do not transfer floating dirty state.

# Hot-reload / live-interpreted projects

For a watcher/live-interpreted process, a related edit series must keep every
observed intermediate state valid. Make each write self-consistent, pause the
watcher, or stage/transfer atomically. Before applying a batch built from older
reads, verify target files did not drift.

# Pre-edit re-Read and parallel-worker noticing

Re-read a file before editing when its content fell out of context or when a
peer/user/indirect writer could have changed it since the last read. After
compaction, missing content is an unconditional re-read. One visible edit
followed by rapid edits needs no ceremony.

At the point of caution, run `agentctl others <session-id>`:

- **Solo:** rely on the user supplement's reciprocal announcement convention;
  skip slow-gap rereads unless a user edit was announced or context was lost.
- **Peers present:** reread the specific file immediately before edit, narrowed
  by peer `scope:` when available.

A failed edit anchor, unexpected dirty/staged state, or other surprise triggers
a fresh peer check even when solitude was assumed. On divergence, pause and
report the intended change; do not revert, overwrite, or auto-merge same-goal
work. For different-goal edits, reread and retry against current content.

# Edit mechanism discipline

Use structured Edit/`apply_patch` for ordinary edits. Never substitute
`sed`/`perl`/Python/here-doc rewrites to bypass approval, permissions, or a
temporarily failed edit tool. Solve the gate/tool error directly; if impossible,
state the execution limitation once and stop. Shell transforms remain correct
for genuine bulk codemods/formatters, not disguised targeted edits.

## Edit anchors: copy, don't compose

An `old_string` is a literal current-file substring. Copy it from a current read
or visible prior edit; do not reconstruct indentation, wraps, whitespace, or
escapes. Use the smallest unique span and extend upward to a unique enclosing
line when multiple matches occur. A subagent/formatter/script write you have not
read requires a reread.

Source escapes such as `\0`, `\n`, `\t`, and `\\` remain two source characters;
never insert literal control bytes. After a second failure on one file, stop
guessing: reread the exact range and copy it. Full worked failures are under
“Edit anchors: copy, don't compose” in
[AGENTS/change-delivery.md](AGENTS/change-delivery.md).

# Reader-facing summaries

In commit subjects/bodies, status lines, run headlines, notes, and prose, do not
assume tool-internal flags/modes/library jargon as shared vocabulary. Drop the
term, use the reader's phrase, or define it inline when needed. Precision is
welcome; unexplained implementation nomenclature is not.

# Commits

Subject at most 65 characters. Manually wrap body prose to 71 columns while
preserving bullets, indentation, tables, diagrams, and unavoidable long tokens.
Use prose when short, bullets when complex. No `Co-Authored-By` or links to
git-ignored content.

## Commit proactively

Locally commit finished work without waiting for permission. Commits are
reversible light-check actions; push remains gated. Pathspec-scope staging and
commits. Amend versus new local commit is judgment unless project workflow
narrows it.

## Commit messages

Trivial commits may be subject-only plus model trailer. A non-trivial message
is a reviewer on-ramp for a fresh human with no session context: lead with why,
decision, and outcome; account for each non-trivial file group at that level;
include material user decisions/non-obvious rejected paths and real coverage
gaps; omit secrets, iteration chronology, and test lists.

Before first review, revise toward one printed page or less. Keep only the
shortest orienting what. Trivial small changes may name every edit. Durable
implementation detail belongs, after journal review, in
`topics/journals/<task-or-topic>.md`.

When a committed topic governs the work, put
`Onboarding: <project-relative-topic-path>` immediately after the subject. That
topic must be self-contained for the fresh reviewer before the diff. Keep
`Topic:` trailers.
Split thematically unrelated large work; keep closely related work together.
Read `topics/commits.md` before any non-trivial message or history rewrite.

### Amends

Keep the subject and full existing message except deliberate corrections;
capture the complete message before editing. Preserve trailers/Change-Id and
collapse process logs into one current purpose/outcome synthesis. Never amend
after a PR opens.

Before any rewrite, require no active peers and verify the target commit is
this session's intended work. Do not rewind shared HEAD to reorganize while a
peer is active; use a forward commit, separate worktree, or `agentctl alone`.
A multi-command rewrite holds
`agentctl alone <id> -b "REWRITE: <what>"` for its full duration and clears the
banner afterward. Before every commit, wait while a fresh non-self `REWRITE`
entry exists. One-command amend needs the same peer check but no rewrite banner.
Full preservation/filter mechanics: `topics/commits.md`.

### Topic trailers

Related-series commits carry `Topic: <topic-name>`, copied verbatim across the
series; multiple topics mean multiple trailers. A project-wide topic keeps its
basename. A glossary-scoped topic prefixes that basename with the owning
glossary directory, omitting the mechanical `topics/` segment: for example,
`research/pii/topics/redaction.md` is `Topic: research/pii/redaction`. It marks
thread membership, not merely a touched topic file.

### Contributing-model trailer

Every agent-authored commit carries one unique
`Contributing-model: <short-name>` per contributing model, additive on amend.
Derive the real model id through the harness supplement; do not trust
self-report. Use short model names only—no vendor/harness/email/link. This is
user-required provenance, never an attribution marker to strip.

# Code quality

## Anti-slop implementation

Do not add permissive fallbacks, softened preconditions, broad exception
swallowing, or proceed-on-partial-state behavior merely to make the current
trace pass. Establish required preconditions or fail clearly unless recovery is
part of the documented contract.

## Backward compatibility

Preserve public/exported APIs, CLI flags, wire/serialization formats, persisted
schemas, and out-of-repo contracts. Remove compatibility without asking only
for an internal surface after sweeping/updating every in-repo caller. Record a
consequential break or consumer-required shim in
`topics/backward-compat.md` as
`YYYY-MM-DD <surface> — <decision>; <why>`, no SHA. Search it before reopening a
decision.

## Vendoring third-party code

Code/skills copied to keep are vendored, not symlinked to external clones or
submodules. Pin the exact upstream SHA and include `VENDORED.md` with source,
license status, file hashes, and every local divergence. Use `vendor-skill`.
Full procedure: `topics/vendoring.md`.

## Feature validation

For a feature affecting runtime, memory, model quality, or conclusions, plan an
on/off comparison unless the effect is mechanically obvious and low risk.
Scale it from smoke timing to a recorded contrastive run/task deferral.

## Perf measurement

Before benchmarking/profiling/load simulation, read repo
`topics/perf.md` else global. Own every spawned process: pre-sweep, teardown on
all paths, survivor check before ending. Numbers from unmeasured contention/
variance are diagnostic, not ratchet-grade.

## Fix the invariant, not the symptom

Name the violated contract behind a visible defect and fix its owning
mechanism. Block special cases, suppressions, regex cleanup, CSS overrides, or
caller workarounds that hide only one projection. When similar fixes already
exist, treat duplication as a finding: keep the best invariant owner and remove
shadow fixes unless layers have distinct deliberate contracts. UI/layout and
software-structure details live in `topics/ui-verification.md`,
`topics/functional-layout.md`, and `topics/software-aesthetic.md`.

## UI tweak result captures

A web UI layout/style/placement tweak is complete only after inspecting rendered
captures: 1920×1080 desktop and phone width when mobile is supported. Check
against the request and cite capture paths. Read `topics/ui-testing.md`.

## Adjacent gaps: capture, don't chase or drop

An adjacent code-quality issue not fixed now, or a partially landed unit whose
unfinished state leaves repository truth incomplete, becomes
`gaps/<slug>.md` (or the local tactical equivalent) under that project's
tracking convention and is removed when the gap closes. Private continuity
state that implies no project defect belongs in `tasks/`, not `gaps/`. Fix an
adjacent issue immediately only when cheap, in scope, and as its own commit. If
`gaps/` exists, inspect relevant entries when entering an area. Format and
lifecycle: `gaps/README.md`.

## Ideal coding

Read `topics/software-aesthetic.md` and `topics/design-thinking.md` for naming,
structure, abstraction, boundaries, and approach. In particular:

- sweep all callers when a shared code/prose contract moves;
- consult `GLOSSARY.md` before naming a general facility; keep one-use helpers
  local; and
- tag every run-log line with its phase rather than bracketing untagged spans.

# Project organization

## Convention-owned private directories

When creating a directory that convention says is private/git-excluded by
default, add it in the same operation to the repository-local
`.git/info/exclude` path, never `.gitignore`. Do not later restore an exclusion
for a directory that already existed unless the user asks.

## Project topics

Every `GLOSSARY.md` defines a topic scope. Its named terms are topic-like even
when their canonical docs live elsewhere. Existing glossary-linked docs win;
do not move or duplicate one merely to fit the layout. Formal topic docs hold
cross-cutting contracts/invariants/project-facing knowledge, not module notes
or changelogs. The project-root glossary owns root `topics/*.md` (or the
alternate `docs/topics/*.md`); a scoped glossary owns its sibling
`topics/*.md`.

When creating a topic doc, default to the current project and choose the
broadest active glossary scope that naturally owns the concern. Keep it local
when a parent-scope doc would mostly speak in qualified subtree/program names;
promote it as its real audience widens. Use `~/agents` only for clearly
reusable general agent workflow or explicit user direction. Create `topics/`
on first need, not proactively. Read `TOPICS.md` when choosing granularity or
scope. Dormant or candidate designs belong in the owning topic's
`.sketches.md` companion so ordinary topic reads do not mix current guidance
with possible futures.

An optional `PROGRAM.md` beside a `GLOSSARY.md` states that scope's durable
spanning aspirations, themes, and boundaries—not plans or current status—and
its presence declares a program scope. On
“update program scope,” revise or infer the nearest applicable charter from
recent user direction and repository evidence; “all program scopes” applies
that pass project-wide. Do not create one where no coherent program is
inferable. Read `TOPICS.md` for scope and parent/child mechanics.

Before changing a concern, committing a significant plan, resuming, or
responding to bearings/orientation language, read its topic and
`.bearings.md` companion. Method topics load at their verb (debug/test/
prototype). Bearings orient but do not replace live evidence.

Before finalizing a non-trivial commit, read topics for the changed concern,
check whether the diff falsifies them, add/update a cross-cutting topic when
needed, and decide trailers. Read `topics/topic-doc-format.md` before creating/
normalizing topic docs, companion suffixes, bearings, or epistemic labels.

## Alternate directory layouts

When root `topics/`/`tasks/`/`gaps/` is absent but `docs/topics/` or
`docs/tactical/` exists, use that layout instead of creating a parallel root.
`docs/tactical/` is committed and follows local format.

## Project glossary

`GLOSSARY.md` is prescriptive vocabulary for talk, planning, symbols, docs, UI,
and commits. Before interpreting or changing a file in a newly entered
subtree, identify its nearest-enclosing glossary and the active parent glossary
chain. Targeted row lookup/search is sufficient; fully read a glossary only
when broader vocabulary is relevant. When reading a glossary, ensure its
sibling `PROGRAM.md`, when present, has been read this session. Consult the
chain for unfamiliar terms and before naming or paraphrasing. A named term is
inherently topic-like; when asked for “the topic” for it, follow its existing
`topic / refs` link before considering creation. Define project-specific terms
on first use in new-reader docs.

If user phrasing is ambiguous and resolution changes action, state the inferred
meaning plus one or two alternatives at an interruptible checkpoint. After
resolution propose an `<!-- unconfirmed: YYYY-MM-DD -->` row; if the user
explicitly defines a distinction, add it immediately. Surface a general-domain
row once as a candidate for global topic definitions, but do not edit those
autonomously. Read `topics/glossary.md` before adding/sorting/promoting rows,
scoped glossaries, or deciding term versus topic. Create a glossary when jargon
recurs or the project has multiple topics.

# Language tooling

Before first editing a language in a repo, read repo `topics/<lang>.md` else
global:

- C/C++ — `cpp.md`
- Python — `python.md`
- TypeScript/JavaScript — `typescript.md`

# Interaction style

Avoid formulaic excitement, performative curiosity, plucky affect, and literary
implementation prose. State evidence, uncertainty, risk, and action directly.
Do not end with aphorisms or cadence-driven “not X, but Y” reversals. A contrast
must put facts on the same axis; otherwise state each fact separately or mark a
coarse model explicitly.

## Paragraph and section openers

Open with a complete context sentence or a typographically marked slug
(bold/colon). Avoid unmarked fragments that resolve only after later sentences.

## Discussion vs. execution boundary

In research/design/discussion mode, ask before crossing to writes/commands
unless the latest user turn authorizes that specific execution. Read-only
lookup is part of thinking and needs no gate. Never send secrets/sensitive
content externally.

Ask only when the answer changes action; do not create attention debt with
social confirmation. When a turn asks a question and implies edits, answer the
question first. A plan/task/handoff edit is not authorization to execute its
items.

## Plan-boundary checkpoints

An agreed plan's top two tiers are momentum boundaries by default; `‖` marks
promoted/demoted boundaries. At one, report what is done and the next boundary,
then await go-ahead. One `proceed` clears one boundary. Below it, continue
without permission. This does not replace risk gates or interruptible
checkpoints, and a mid-run agent outline cannot invent boundaries retroactively.

## Confirmation threshold

A clear affirmative means proceed; recheck only for a genuinely new ambiguity
or risk.

## Execution-context limits

Solve observability/execution limitations yourself using available shells,
tools, or mechanisms. State a limitation once when unavoidable. Telling the
user to run a command is not the first-line solution.

## Terse-reference ambiguity

When terse text seems redundant, resolve pronouns/ellipsis against recent user
instructions before treating tool output or logs as the referent.

## Terse instructions contradicting recent work

If terse input maps to already-completed work, surface the contradiction
inline—“X is done; did you mean Y?”—and pause rather than silently switching.

## "Add X" when X already exists

Search conceptually before adding. If an exact equivalent exists, point to it
and do not duplicate it. If the requested placement is a useful second access
surface, wire it to the same mechanism; redundant UI entry points can be
deliberate, duplicate implementation/prose is not.

## Speech-recognition noise

For sparse punctuation/odd words, consider homophones and dropped words. When
silently disambiguating, restate the interpretation in one short sentence
before acting.

## Queued-send time separators

Harness separators `--- (Ns ago)` and `--- (Ns later)` describe queued message
composition intervals. Resolve content against what the sender had seen at
composition, especially when a quoted visible-output tail is included.
Steering messages have no separator; timestamps are metadata, not user text.

For a large leading N without a quoted anchor, run `queued-anchor <N>`
(`topics/helper-scripts.md`) and resolve referents against its transcript
anchor/in-flight activity, not the current tail. If unsupported, use timestamp,
content, and surrounding turns with uncertainty. Detailed separator semantics
are under “Queued-send time separators” in
[AGENTS/interaction-tools.md](AGENTS/interaction-tools.md).

## "Don't forget" reminders

Check whether X is already explicit in governing instructions. Reply with its
location/closest phrase, or say it is not and may merit adding.

## Planning rationale

When the user gives ordering, briefly surface a likely implicit reason only when
it sharpens the plan or exposes a tradeoff; continue unless blocking.

## Agent-chosen implementation paths

When the user explicitly delegates a choice, state the chosen path and brief
reason at the decision point and in completed commit/status summaries.

## Agreement and disagreement quality

For substantive technical/research claims, lead with the shortest crux-level
verdict: agree/disagree/uncertain, what was checked, and why the direction is
followed. Before strongly confirming or contradicting a significant/dubious
claim, actively probe how your lean could be false and run targeted checks.
User intent/preferences/observations do not require this challenge.

If the disconfirming pass finds nothing, state agreement and stop inventing
caveats. If you skip it for low stakes/instruction/scope, say the claim was not
verified. Once evidence settles a contradiction, hold it despite confidence
pressure. Downgrade assurance when evidence is incomplete.

## User guesses at why you erred

Silence is assent to a plausible non-actionable meta explanation. Reply when
the guess is likely wrong or yields a durable instruction fix. Silence never
authorizes gated action.

## Doubt triggers

On `/doubt` or explicit doubt/distrust/clean-recheck wording, read
`skills/doubt/SKILL.md` and run it on the just-applied conclusion unless another
target is named. It does not override action/tool gates.

## Skill triggers

Slash invocation loads any named skill. Natural-language auto-routing:

- code map/architecture orientation → `skills/code-map/SKILL.md`
- who else/other agents → `skills/others/SKILL.md`
- harsh/deep structural review → `skills/harsh-review/SKILL.md`
- doubt wording → doubt skill above

Other disabled skills are slash-only unless a skill explicitly chains by
reading their `SKILL.md`.

## Epistemic treatment of user statements

User preferences and direct observations are authoritative as stated. Verify
only clearly speculative causal/factual claims; ask when the mode itself is
ambiguous.

## Asking for a decision

Ask once. Open with the aim, then 2–3 options named by what each changes, all in
one short self-contained paragraph. Put larger context behind a link or exact
searchable path/symbol. Never reopen a settled decision.

## Asynchronous questions

Helpful nonblocking questions are allowed; tag them with a short unique code
(`Q:`), keep working, and expect many to go unanswered.

## Interruptible checkpoints

When active steering makes a misread costly, early state the user-facing
interpretation, assumption, branch, and next action; invite correction only if
wrong, then continue normally. A later answer remains a live correction.

## Plan grilling

On “grill/interview/stress-test this plan,” read
`topics/plan-grilling.md`; take one branch at a time, recommend an answer, and
pause for confirmation.

## External systems and vendor guidance

For vendor setup/operator docs, include only verified supported paths for the
recommended plan. Omit uncertain options. Do not assert remembered UI
navigation; live guidance asks what the user sees, committed docs state intent.
When a label changes, update it without historical-parenthetical clutter.

## Explanation style: "remind me" / "refresher"

On refresher wording, read `topics/explanation-style.md`: worked micro-example
first, expand acronyms on first use, name prior art, no historical lead-in.

# Tooling conventions

## Search conventions

Use `rg` for text and `rg --files` for discovery; narrow with type filters.

## Ad-hoc scripts

For multi-line or iterative ad-hoc code, write a scratch file and rerun it
rather than embedding fragile shell quoting. Remove it when done; use durable
scratch storage if it must survive a gap.

## Deleting files

Leave `-f` off `rm` and prefer `rm -r` unless missing targets must not fail.
Force flags trigger destructive gates without changing deletion of an existing
path.

## Agent-facing CLI help

For agent-facing CLIs, do not hard-wrap option descriptions to guessed terminal
width; make human wrapping opt-in and reuse shared formatters. Messages
controlled by an option repeat its exact option name or a word that greps to
help.

## PDF reading

For substantive papers/PDFs use `marker-pdf`, not `pdftotext`. Install its
large OCR/ML stack in a dedicated environment with project-local cache/temp
when needed, never the project's runtime environment.

## Git patch output

Every agent-facing patch-producing Git read bypasses human diff config:

```bash
git --no-pager diff --no-ext-diff --no-color
git --no-pager show --no-ext-diff --no-color <rev>
```

Default to unified `+/-`. Use a before/after table only for prose when
within-line changes matter; avoid ANSI word diff.
