# RESEARCH ADVISOR — object-session handoff and routing

This protocol governs the object-level research session and the transport to a
long-lived, separately resumable advisor. `advisor/charter.md` governs how the
advisor reasons and responds. Load this protocol when a `RESEARCH.md` invocation
condition fires or graehl operationally addresses or refers to “the advisor.”
The advisor is treated as always at hand even though its session is resumed or
started only on demand.

## Scope and continuity

The default unit is one project:

- one advisor session covers the project's whole `research/` tree;
- its compact current assessment lives in `research/advisor/notes.md`;
- its followed-document list and last-review state live in
  `research/advisor/docs/state.md`;
- its machine-local transport address lives in
  `research/advisor/session.local.md`;
- completed advisor-session logs live in `research/advisor/sessions/`;
- separate papers and branches still use that project-wide advisor.

Create the advisor directory on first actual handoff, not merely because a
project has a `research/` directory. The advisor's continuous transcript is the
v1 working memory: resume the same session rather than starting a clean reviewer
for each packet. The advisor maintains `notes.md`, in whatever compact structure
best preserves its current understanding, as a self-contained statement of
current project state. It is not a copy of the transcript, a persona prompt, or
another chronological research log.

The durable default advisor behavior is `~/agents/advisor/charter.md`. A project
may add `research/advisor/charter.md` as a project-wide amendment. An explicitly
distinct research program may further add
`research/<program-slug>/advisor/charter.md`. Amendments are loaded broadest to
narrowest; they supplement rather than silently replace the global charter.

A distinct research program may override the default with its own advisor
session and `research/<program-slug>/advisor/{notes.md,docs/,sessions/}`. Make
that split only after deciding that the program's evidence stream and research
narrative are independent enough that shared advising adds more contamination
or context load than useful cross-program memory. The slug defaults to the
basename of the program's principal `research/<name>.md` paper. If there is no
natural paper basename, the object-level agent chooses a concise stable slug.
Record the override, slug, and scope at the top of its `notes.md`. A paper,
directory, or branch existing is not by itself an override.

Route a packet to the most specific existing `advisor/notes.md` whose declared
scope covers the active program; otherwise use the project-wide advisor. Do not
infer a distinct-program advisor from unrelated files under the program
directory.

When an advisor session is deliberately replaced or can no longer be usefully
resumed, archive its available provider transcript or lossless export under
`sessions/` before starting the successor. Use a chronological filename and
preserve the native format rather than rewriting the exchange into a cleaner
story. If no transcript export is available, archive the best available
session handoff and label it as a summary. `notes.md` must remain sufficient to
start the successor without replaying every archive; archived sessions are for
recovering provenance, exact prior wording, and drift that the compact state may
have lost.

`notes.md` follows the project's normal tracking policy for research documents.
The project may commit or locally retain the much larger `sessions/` archives;
state that choice in `notes.md`, and never make its current assessment depend on
an archive unavailable to the next intended reader. Provider resume locators
are machine-local session metadata, not committed research notes.

`<advisor-dir>/session.local.md` is the durable address the object-level
research session or user uses to resume the advisor. On first creation, exclude
that exact path through the repository-local Git exclude unless it is already
ignored; never commit it. Keep this minimal schema:

```markdown
Advisor scope: <project-root-relative research scope>
Harness: <provider/harness resume command>
Session ID: <canonical resumable identifier>
Reported at: <ISO-8601 timestamp>
```

After the advisor's first turn, and whenever its provider session changes, the
advisor reports its harness and canonical session id; the object-level owner
verifies and safely updates this file. Lifecycle—continue, close, replace, or
split—remains controlled by the object-level research session or user. The
address records that decision; it does not create a standing router.

On the first handoff, use this protocol to start the advisor. Its first
transaction creates `notes.md` with its initial scope and assessment, using a
`none` fold watermark if no turn has yet been folded, and `docs/state.md` with
the initial followed set and completed-review state. Start or resume every
advisor turn with this ordered bundle:

1. `~/agents/advisor/charter.md`;
2. optional project-wide and distinct-program charter amendments;
3. the resolved `notes.md`, when it exists;
4. the resolved `docs/state.md`, when it exists;
5. the current interaction turn: initial packet or focused follow-up.

The advisor applies any followed-document changes requested by the packet, then
synchronizes every path in `docs/state.md`—committed, staged, unstaged, and
untracked deltas included—before reviewing the claim or decision. The object
session names the narrow set of evolving documents needed for the program; it
does not default to the entire `research/` tree.

## Serial ownership and locking

Serial advising is the expected mode. Before processing a packet, the advisor
registers an active-session scope covering its advisor directory and checks for
another live session claiming the same scope. If one exists, route the packet to
that session or wait; do not start a competing advisor. Immediately before
writing `notes.md` or archiving a session, repeat the peer check and re-read the
target.

This active-session convention detects ordinary collisions but is not an atomic
lock: two launches can both pass a check before either registers. A launcher or
session router that automates advisor dispatch must therefore acquire one
atomic, scope-keyed, stale-recoverable lease before resuming or creating an
advisor. Hold it for one delivered advisor-turn transaction, including
note/archive writes, and release it while the advisor awaits the next
object-level turn. Until that lease exists, a detected
collision stops rather than merging two advisors' state after the fact.
Before implementing such automation, specify its owner record and recovery:
harness/session or occurrence id, host, PID plus process-start identity,
claim/heartbeat time, phase, and the evidence required to retire a stale
lease. PID liveness alone is insufficient.

The charter governs safe note replacement and session archiving. The router
must ensure its backup/temporary paths are ignored or locally excluded before
the advisor's first state update.

## Invocation and deduplication

`RESEARCH.md` owns the automatic invocation conditions. When several conditions
describe the same decision/evidence state, send one packet naming all relevant
reasons, not one packet per bullet.

An operational user mention of “advisor” also invokes it:

- information, a claim, or “the advisor should know X” is a `tell`;
- a question, request for judgment, or “what does the advisor think?” is an
  `ask`;
- discussion of the advisor mechanism, charter, files, or routing is meta-level
  design and does not recursively invoke it.

The initial packet opens an advisor interaction, not a one-shot remote procedure
call. Assign the interaction a stable id for its research scope and
claim/decision. Clarification, rebuttal, advisor-requested evidence, and rapidly
evolved prototype results may continue as turns or evidence revisions under
that id, including across provider-session resumptions. The object-level
researcher or user decides whether and how long to continue the discussion; the
router may keep, resume, or split provider sessions at its discretion.

Reuse the interaction id plus revision when retrying delivery. The advisor
treats an already completed revision as idempotent and returns its prior memo
only when both the turn and synchronized followed-document state are unchanged.
Changed evidence, a followed-document delta, a changed decision, or an explicit
request to reconsider gets a new revision in the same interaction. Keep the
latest handled interaction/revision for each live program in compact notes so a
successor can deduplicate without replaying settled archives.

## Fold-in debt

`notes.md` carries this fold watermark:

```markdown
Last session folded in: <ISO-8601 timestamp or none>
Folded through: <session archive or stable label> · <interaction-id>/<turn>, or none
```

Any advisor transcript material after the watermark is **fold-in debt**: a
newer session log, or later turns in the same session. Debt is allowed while an
interaction remains live; do not rewrite compact notes after every turn. At a
natural interaction close, fold its durable conclusions, objections, and
adjudications into `notes.md` and advance the watermark even when no conclusion
changed. A long interaction may checkpoint earlier when context or resumability
would otherwise be at risk.

The watermark covers one contiguous prefix of the advisor transcript, not
independent per-interaction acknowledgements. Advance it only after considering
every turn through that point. If interactions interleave, preserve an older
still-open interaction as pending state rather than skipping it to fold a newer
one.

Before a successor relies on `notes.md`, fold every available debt session or
turn. If a provider session cannot be resumed, archive its transcript first so
the successor can pay the debt. Pre-watermark sessions remain cold provenance
and need no replay.

## Followed documents

`<advisor-dir>/docs/state.md` is the one authoritative followed-document list
and last-review ledger for that advisor. Its list contains project-root-relative
paths or anchored globs, with a reason where inclusion is not obvious. Direct
paths to canonical project documents are preferred; no symlink farm is
required.

A document or symlink placed under `docs/` has no implicit status. If useful,
list a regular document there or the symlink's resolved target in `state.md`;
the advisor reads and diffs the listed source. This preserves one discovery
rule and avoids treating an unchanged symlink as evidence that its target is
unchanged.

The object session proposes the narrowest additions or removals needed to keep
the advisor current on the active program. Evolving papers, logs, topic docs,
and research plans normally belong in the followed set. A one-off artifact may
remain only an evidence link in its packet. Do not bulk-add the whole
`research/` tree merely for completeness. If two programs need substantially
different followed sets and trajectories, give them distinct advisor
directories rather than adding selection rules inside one `state.md`.

## Natural-language commands

`Tell advisor <X>` or `tell the advisor <X>` means: assemble the smallest
faithful packet containing X and its live research context, deliver it to the
designated session, and continue reversible object-level work. Bring the
challenge memo back at the next natural boundary; do not imply that silence
means agreement.

`Ask advisor <Q>` or `ask the advisor <Q>` means: assemble and deliver a packet
centered on Q, then obtain the advisor's answer before crossing the decision
boundary named by the question. The object session may continue the resulting
discussion under the same interaction. Do not answer in the advisor's voice
from the object session.

Use available session-control transport to resume the designated advisor. If
the current harness cannot address the harness/session pair recorded in
`session.local.md`, say once that delivery did not occur and emit the exact
packet, marked `UNDELIVERED`, for forwarding; never fabricate an advisor
response.

## Object session → advisor packet

Keep the initial packet short—normally at most 350 words excluding direct
evidence links. Omit inapplicable fields rather than padding them.

```markdown
## Advisor packet: <project>/<thread>/<interaction-id>/<revision>

Mode: tell | ask
Question: <only for ask, or the decision to review>
Claim / decision: <one sentence>
Current status: <object session's evidence status and confidence>
Prior commitments: <predictions or decision criteria recorded before the result>
Followed-document changes: <paths/globs to add or remove, or none>
Evidence: <direct artifact, run, diff, paper, or result-table links>
Alternatives: <live alternatives actually considered, including stop/incumbent>
Interpretation / next step: <what the object session now thinks follows>
```

Separate observation from interpretation. Link to the evidence instead of
pasting logs or retelling the whole discussion. Preserve a missing
pre-registered prediction as `none recorded`; do not reconstruct one after
seeing the result. Do not send the advocacy transcript unless the advisor asks
for a specific passage needed to diagnose drift. Add a document to the followed
set when its future deltas matter to the advisor's trajectory; otherwise leave
it as a direct evidence link. Follow-up turns cite the interaction id and send
only the question, objection, or evidence delta; do not reserialize the initial
packet.

## Advisor review

The global charter and optional amendments govern the advisor's review,
challenge-memo format, independence, compact-state maintenance, and succession.
The object session must not simulate that review when transport is unavailable.

## Return and durable notes

Return the memo without laundering it into the object session's preferred
story. Quote or link the advisor memo first; place any object-session rebuttal
or updated interpretation after it as a separate response.

`ask` packets and automatic pre-decision triggers hold the material decision
until the advisor has answered the current revision or graehl explicitly
proceeds without it. Reversible prototype work may occur inside the open
interaction and return as evidence. A `tell` packet is non-blocking, but only
reversible preparation should outrun an unreturned challenge on the same
decision.

The advisor updates compact notes and archives completed transcripts according
to its charter. Ordinary interaction traffic remains in its continuous
transcript.
