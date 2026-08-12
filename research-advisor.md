# RESEARCH ADVISOR — logical continuity and object-session routing

This protocol governs the object-level research session and the transport to a
durable logical advisor that may outlive any provider session or model.
`advisor/charter.md` governs how the advisor reasons and responds. Load this
protocol when a `RESEARCH.md` invocation condition fires or graehl
operationally addresses or refers to “the advisor.” The advisor is treated as
always at hand even though its serving session is resumed or started only on
demand.

## Scope and continuity

The default unit is one research program. Discover program roots by the
`Research program:` declaration in `research/<program>/GLOSSARY.md`
(`RESEARCH/artifacts.md` § Research programs); a glossary without one scopes
vocabulary only, so no subdirectory forks an advisor by merely existing. A
program advisor uses:

- `research/<program>/advisor/metadata.md` for logical identity, program
  binding, lifecycle, and restart control;
- `research/<program>/advisor/notes.md` for its compact current assessment;
- `research/<program>/advisor/docs/state.md` for its followed-document list
  and last-review state;
- `research/<program>/advisor/intake.md` for handled interaction/revision and
  handoff-intake deduplication records;
- `research/<program>/advisor/session.local.md` for its machine-local
  current-incarnation transport, model, and effort;
- `research/<program>/advisor/sessions/` for completed session logs.

The directory basename is the stable program slug. Every paper, report, log,
and supporting artifact below the program root belongs to that program unless
the program glossary says otherwise.

Root-level standalone papers and cross-program synthesis use the project-wide
fallback under `research/advisor/` with the same layout. A project-wide advisor
may follow multiple root-level threads; it does not absorb a program merely to
share context.

Below, `<advisor-dir>` means that resolved program directory or project-wide
fallback. The logical reboot bundle is
`<advisor-dir>/{metadata.md,notes.md,docs/state.md,intake.md}`; the current
incarnation is `<advisor-dir>/session.local.md`; cold transcript provenance is
under `<advisor-dir>/sessions/`. Handoffs record the exact metadata path rather
than asking a successor to repeat scope discovery.

Create the advisor directory on first actual handoff, not merely because a
project has a `research/` directory. The logical advisor is the stable
program-to-advisor relation named in `metadata.md`; a provider session is one
generation-fenced incarnation. The default policy is one continuous, growing
session, consulted infrequently at the invocation conditions, rather than a
clean reviewer per packet. A program may deliberately choose fresh per consult
or another policy in metadata.

The continuous transcript remains valuable working memory, but logical
continuity is the durable bundle: metadata, compact semantic notes, document
cursor, intake ledger, and available post-watermark transcript. This permits a
failed compaction, lost resume handle, or deliberate model/provider migration
without silently creating an unrelated advisor. The advisor maintains
`notes.md`, in whatever compact structure best preserves its current
understanding, as a self-contained statement of current scope state. It is not
a copy of the transcript, a persona prompt, or another chronological research
log.

The durable state files have distinct roles:

- `metadata.md` controls identity, declared scope, artifacts, lifecycle
  generation, exact session title, literal restart prompt, and policies;
- `docs/state.md` is the mechanical read cursor: which documents were resolved,
  at what repository revision, plus fingerprints for dirty or untracked text;
- `notes.md` is the semantic state: the advisor's synthesized understanding of
  the program after reading through that cursor, including its present progress
  assessment and ranked outstanding proof requests; and
- `intake.md` is the append-only operational ledger that makes retries and
  repeated handoff presentations idempotent.

Keep one fact in one owning artifact. `metadata.md` points to the other files
but does not copy their content; integrity receipts may project their current
digests/watermarks without restating their claims;
`docs/state.md` contains no program assessment, decision, objection, or proof
request; `notes.md` contains no transport address; `intake.md` records the
packet/memo provenance rather than another program summary; and
`session.local.md` contains no durable policy. The only deliberate projections
are the logical advisor id, lifecycle generation fence, and cross-file
watermark/digest needed to detect a stale or split-brain write.

Do not create a parallel `state-understanding.md`. After every successful
followed-document synchronization, reconcile `notes.md` against what was read
and advance its understanding watermark even when no conclusion changes. This
makes a successor's startup test explicit: if the document cursor is newer than
the notes watermark, the compact understanding is stale and must be reconciled
before advising.

The durable default advisor behavior is `~/agents/advisor/charter.md`. A project
may add `research/advisor/charter.md` as a project-wide amendment, and a program
may add `research/<program>/advisor/charter.md`. Amendments are loaded broadest
to narrowest; they supplement rather than silently replace the global charter.

Route work on a document below a program root to that program's advisor. Route
work that names a program to the matching program root even when the immediate
artifact is outside it. Use the project-wide fallback only for root-level
standalone work or genuinely cross-program decisions. If scope is ambiguous,
list the discovered program glossaries and choose from those stable slugs
rather than inventing another advisor directory.

## Establishing the logical advisor

At first use, consciously choose and record the human program name, stable
program id/slug, declared program root, advisor scope, governing overall
progress/plan, and advisor metadata site. Normally the declared program's
`advisor/` directory is the only appropriate site. Use the project-wide
fallback only for genuinely root-level or cross-program work, and record why
that broader site is correct. Choose an exact session title derived from the
program name, normally `Advisor — <Program name>`; generic startup-prompt text
is not an acceptable durable title.

Create `<advisor-dir>/metadata.md` from this minimum control schema:

```markdown
# Advisor metadata

Schema version: 1
Logical advisor ID: <stable id>
Program name: <human-readable name>
Program ID: <stable slug or id>
Program root: <project-root-relative path or project-wide>
Advisor scope: <precise program responsibility>
Scope revision: <monotonic integer>
Scope provenance: <user decision or non-contradictory clarification source>
Governing progress/plan: <path(s)>
Metadata path: <project-root-relative metadata.md path>
Metadata site rationale: <why this program or fallback site is correct>
Exact session title: Advisor — <Program name>
Lifecycle generation: <monotonic integer>
Lifecycle state: active | no-incumbent | retired
Predecessor: <logical id/generation/session, or none>
Replacement reason: <reason, or none>
Charter stack: <global then project/program amendments>
Semantic notes: <notes.md path>
Document state: <docs/state.md path>
Intake ledger: <intake.md path>
Session archives: <sessions/ path and tracking/availability policy>
Consultation policy: <triggers/cadence; normally long-lived and infrequent>
Restart policy: <resume-continuous | fresh-per-consult | other explicit policy>
Model/effort policy: <preference or migration rule; current values are local>
Restart prompt version: <integer>
Restart prompt SHA-256: <digest of the literal block below>

## Restart prompt

<literal prompt supplied to every fresh incarnation>
```

The literal restart prompt names the logical advisor id, program name and
scope, exact metadata path, and expected session title. It instructs the new
incarnation to validate the metadata generation and acquire exclusive
ownership; load the charter stack, notes, document state, intake ledger, and
available post-watermark transcript; reconcile all fold/document/intake debt;
avoid continuity writes from a retired or fenced generation; and report its
binding and current transport facts. Binding uncertainty does not suppress a
useful read-only advisory response: label it, preserve state, and offer the user
a concrete proceed/select-incumbent path. Store the prompt itself, not a
description of how to reconstruct it. Update its version and digest whenever
its text changes.

An advisor may clarify or amplify scope inside the declared program and record
that gradual evolution by advancing `Scope revision` with provenance. A
material widening, contraction, or transfer of authority is proposed to the
user and recorded only after resolution; advice alone does not authorize it.

Validated metadata and charter are sufficient user-established standing for
ordinary consultation and advisor-owned continuity writes; they do not make
the advisor a supervisor of object-level work. Its objections, recommendations,
and want-to-sees express its assessment. A want-to-see is a condition for the
advisor's confidence unless a cited user/governing artifact independently makes
it a worker gate.

`metadata.md`, `notes.md`, `docs/state.md`, and `intake.md` are the ordinary
logical-reboot bundle and follow the project's durable research-document
tracking policy. `sessions/` is optional cold provenance: it may repair
post-watermark debt or recover exact wording, but an ordinary reboot must not
depend on replaying pre-watermark archives. Only `session.local.md`, backups,
temporary siblings, and a live lease are current-incarnation scratch state.

## Start, resume, repair, and succession

When legacy advisor state lacks `metadata.md`, first ask the still-resumable
prior advisor for its proposed program binding and scope, current assessment of
program progress, and ranked outstanding proof requests. Reconstruct and repair
the logical bundle in place when the program binding and provenance are
verifiable, the semantic state is usable, and no competing incarnation exists.
An evolved schema is not by itself a reason to discard continuous context.

Start a successor only when required by recorded policy or when the incumbent
is unresumable, retired/fenced, irreconcilably wrong-scope, missing/corrupt in
its semantic state, missing transcript across material fold debt, or one of
multiple incumbents that cannot be put in a verified order. Before the
successor starts, archive the available provider transcript or lossless export
under `sessions/`, fold the contiguous available debt, fence the old
generation, and increment `Lifecycle generation` in metadata. Publish the
successor address only after it has loaded and validated that generation. A
different provider or model may serve the same logical advisor; preserve the
logical id and record the migration as a new generation. A live model/effort
change within one still-resumable session may stay in the same generation, but
its later advice retains the changed provenance.

Use a chronological archive filename and preserve the native format rather
than rewriting the exchange into a cleaner story. If no transcript export is
available, archive the best available session handoff and label it as a
summary. `notes.md` must remain sufficient to start the successor without
replaying every archive; archives recover provenance, exact prior wording, and
post-watermark drift that compact state may have lost.

`<advisor-dir>/session.local.md` is the local projection used to resume the
current incarnation. On first creation, exclude that exact path through the
repository-local Git exclude unless it is already ignored; never commit it.
Keep this schema:

```markdown
Logical advisor ID: <metadata.md logical id>
Lifecycle generation: <metadata.md generation>
Advisor scope: <project-root-relative research scope>
Exact session title: <provider-visible title>
Harness: <provider/harness resume command>
Session ID: <canonical durable harness resume identifier, or unavailable>
Session address: <public URL or other durable address, or unavailable>
Provider resume ID: <distinct provider handle, same, or unavailable>
Current model: <verified current model, or unknown>
Model evidence: <source and observation time>
Current effort: <verified current effort, or unknown>
Effort evidence: <source and observation time>
Resumability: verified | unverified | failed
Consultation state: open | closed-idle | partial-idle
Consultation ended at: <ISO-8601 timestamp or none>
Verified at: <ISO-8601 timestamp>
```

Do not report launcher-recorded initial model/effort as current after a live
change; label initial-only evidence explicitly or use `unknown`. After the
advisor's first turn, and whenever its provider session, model, or effort
changes, the advisor reports these facts; the object-level owner verifies and
safely updates this file. Once an expected session id is established, the
consulting worker checks the local projection before dispatch with:

```bash
test "$(awk -F': ' '$1 == "Session ID" {print $2}' <advisor-dir>/session.local.md)" = "<expected-session-id>"
```

This checks the recorded durable harness id; initial establishment or
replacement also requires evidence that its address and any distinct provider
resume handle are usable. YA normally puts this durable id at the end of its
public session URL. A backend whose canonical id or redirect is not yet
implemented records the available address and `Session ID: unavailable`; do
not silently promote an alias or backend-native handle. The object-level
session or user controls lifecycle. The local projection records that decision;
it does not create a standing router. At consultation close, write this
projection last. Its filesystem mtime, or the latest mtime among advisor files
covered by the receipt, is acceptable evidence for the recorded end time; a
later write makes that closure timestamp stale rather than invalidating prior
advice.

When a working handoff covers work served by this advisor, record the exact
`metadata.md` path in its `Advisor metadata:` line and copy the verified
harness, scope, canonical id, and `session.local.md` path into its repeatable
`Incumbent advisor session:` line from `topics/handoffs.md`. Update both
surfaces when the provider session changes. Under a fresh-per-consult policy,
fence the serving generation and mark metadata `no-incumbent`, then remove
`session.local.md` and the incumbent line after verified closure while
retaining the logical metadata line. The next consult increments the generation
and marks it active before starting its fresh provider session.

On the first handoff, use this protocol to establish metadata before starting
the provider session. Its first transaction creates `notes.md` with an initial
progress assessment and ranked proof requests, using a `none` fold
watermark if no turn has yet been folded; `docs/state.md` with the initial
followed set and completed-review state; and `intake.md` with its schema header.
For a program advisor, the program's `GLOSSARY.md` is the first required
followed document. Start or resume every advisor turn with this ordered bundle:

1. `~/agents/advisor/charter.md`;
2. optional project-wide and program charter amendments;
3. the resolved `metadata.md`;
4. the resolved `notes.md`;
5. the resolved `docs/state.md`;
6. the resolved `intake.md`; and
7. the current interaction turn: initial packet or focused follow-up.

On its first response in an incarnation, the advisor states the logical id,
generation, program name/scope, metadata path, exact session title, harness,
canonical session id, current model and effort with evidence, and resumability
status. A binding mismatch blocks conflicting continuity writes, not advice:
state the uncertainty and obtain user resolution before treating the response
as folded durable state.

The advisor applies any followed-document changes requested by the packet, then
synchronizes every path in `docs/state.md`—committed, staged, unstaged, and
untracked deltas included—and reconciles `notes.md` through that completed
document state before reviewing the claim or decision. The object session names
the narrow set of evolving documents needed for the program; it does not
default to the entire `research/` tree.

## Serial ownership and locking

Serial advising is the expected mode. Before processing a packet, the advisor
registers an active-session scope covering its advisor directory and checks for
another live session claiming the same scope. If one exists, route the packet to
that session or avoid a competing continuity write. A non-owner may still
inspect and respond provisionally with the ownership uncertainty visible.
Immediately before writing any continuity artifact or archiving a session,
repeat the peer check, re-read the target, and verify that the logical
id/generation in metadata, session projection, lease, and target projection
still match. A fenced older generation does not write even if its provider
session later resumes; it can still advise read-only.

This active-session convention detects ordinary collisions but is not an atomic
lock: two launches can both pass a check before either registers. A launcher or
session router that automates advisor dispatch must therefore acquire one
atomic, scope-keyed, stale-recoverable lease before resuming or creating an
advisor. Hold it for one delivered advisor-turn transaction, including
note/archive writes, and release it while the advisor awaits the next
object-level turn. Until that lease exists, a detected
collision prevents automatic state merging, not a provisional advisory reply.
Surface the owners and let the user select/fence one when routing cannot
resolve it.
Before implementing such automation, specify its owner record and recovery:
logical advisor id/generation, harness/session or occurrence id, host, PID plus
process-start identity, claim/heartbeat time, phase, and the evidence required
to retire a stale lease. PID liveness alone is insufficient. This generation
fence prevents both simultaneous split brain and an old incarnation's later
ABA-style resurrection after a successor has published.

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
call. Its author assigns a stable id for the research scope and claim/decision;
the id is not derived from the packet hash. Clarification, rebuttal,
advisor-requested evidence, and rapidly evolved prototype results continue as
turns or explicit revisions under that id, including across provider-session
resumptions. The object-level researcher or user decides whether and how long
to continue the discussion. Treat the id as a best-effort serial, not a global
uniqueness or monotonicity claim. Honor a reuse within 24 hours as a likely
continuation/retry while the interaction remains open; requesters should not
intentionally assign it to a distinct interaction during that window. After a
real or synthetic sign-off, a later request uses a new id and may reference the
prior interaction naturally.

Prefix only the first delivered turn of an interaction:

```text
[from working-agent <harness> <canonical-durable-session-id>; interaction <interaction-id>]
```

Later turns inherit it. End the requester's final turn with the matching
`[sign-off working-agent <harness> <canonical-durable-session-id>; interaction
<interaction-id>]`; a one-turn consultation may carry both lines. The envelope
is claimed routing provenance and a post-sign-off return address, not
cryptographic authentication or an authorization token. Do not add the usual
subagent/non-user authorization disclaimer. If the advisor must report a
material correction or emergency after sign-off, label it `post-sign-off
notice` and address that harness/session. Otherwise a later request starts a
new interaction envelope with a new id.

`working-agent` tells the advisor to scrutinize material progress/completion,
result-interpretation, and inferred-user-intent claims for advocacy or
self-reinforcement. A factual update that the user explicitly said X, including
a later superseding instruction, gets ordinary/default skepticism and is
accepted normally. The identified session/log is merely the usual cheap
verification option when an actual material conflict independently warrants
it, not a special proof burden.

Consultations are serial by default. If another party enters while one
requester interaction is open and its origin is ambiguous, state the confusion
and ask the entrant to begin its own `[from working-agent ...]` envelope; do not
silently attribute or merge its messages, but preserve safe provisional help.
On the next activation, an interaction with no sign-off and no activity for
more than 24 hours receives an explicit advisor-authored `[synthetic sign-off
...; inactive >24h]` in `intake.md`. Mark it synthetic, never requester-authored;
a later return opens a new interaction envelope with a new id.

Before dispatch, finalize the packet and normally compute its SHA-256. Record
in `intake.md` the stable interaction id, handled time/status, requester,
handoff or packet path, digest when available, advisor incarnation, and prior
memo or durable pointer. A semantic/document watermark is optional context for
explaining a changed response. Prior completed records are append-only.
Missing optional provenance is `unavailable`; it does not suppress advice.

The stable interaction id is the primary repeat cue within its origin and time
context, not proof of global uniqueness. If the packet digest and semantic
watermark also match, return or recap the cached memo. If either changed, say
the interaction was seen before and provide a fresh or delta response as
useful; do not demand a revision ceremony. An ambiguous reuse asks for
clarification without suppressing advice. A completed duplicate delivered by
another successor is not by itself a double-agent incident; report concurrent
ownership only when live session/lease evidence establishes it.
`topics/handoffs.md` adds handoff-specific completeness-repair fields.

Use this compact append-only record shape; a later status or closure appends a
linked record:

```markdown
## <interaction-id> · <packet-sha256-or-unavailable> · <status> · <ISO-8601 time>

Requester: <harness> · <canonical durable session id or unavailable>
Requester sign-off: open | received <ISO-8601 time> | unavailable
  | synthetic <ISO-8601 time> after >24h inactivity
Advisor incarnation: <logical id>/<generation> · <provider session id>
Source: <handoff/packet path> · SHA-256 <digest or unavailable>
Status: received | answered | closed | interrupted | superseded
Response: <exact memo or durable path>
Related record: <prior/newer record or none>
```

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

## Semantic-state reconciliation

In addition to the transcript fold watermark, `notes.md` carries:

```markdown
Document understanding synchronized through: <docs/state.md Observed at timestamp> · <full HEAD SHA>
```

Use `none · none` before the first completed document review. After resolving
and reading the followed set, atomically write `docs/state.md` first. Then
compare every live claim, evidence status, criterion, objection, alternative,
and pending adjudication in `notes.md` with the synchronized documents. Update
the semantic summary where the documents changed its meaning and advance the
marker to the exact observation timestamp and SHA recorded in `docs/state.md`.
When changes are formatting-only or otherwise semantically inert, advance only
the marker rather than manufacturing narrative churn.

This ordering makes interruption detectable: if `docs/state.md` advances but
the notes marker does not, the next activation must perform the missing
reconciliation before it treats compact notes as current. Matching markers mean
the advisor deliberately considered the synchronized document state; they do
not imply that every statement in the documents is correct or endorsed.

Near its watermarks, `notes.md` maintains a dated current assessment of program
progress: what is established, provisional, blocked, or unproven; the strongest
evidence and missing gates; and the advisor's confidence. It also maintains a
ranked `Want-to-sees` section for deliverables, gates, or discriminating
observations the advisor has requested but has not received proof of. Every
item carries a stable id, current rank, requested proof, the decision it would
change, what it discriminates, an objective closure criterion, status, and
originating interaction/revision. Reordering, weakening, satisfying,
withdrawing, or reopening an item records the evidence or reason; a new
incarnation does not reset the list.

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

Use the interaction envelope above for every delivered packet. Its harness and
session id identify the requester and provide a possible return address after
sign-off; they neither grant authority nor require a repeated prefix on later
turns in the same interaction.

`Conclude advisor interaction <interaction-id>/<revision>` is the normal
leave-call message and carries the matching requester sign-off. It asks the
advisor to reconcile the current followed
documents; fold every contiguous transcript turn through the interaction;
update the program-progress assessment and ranked proof requests in `notes.md`;
complete the intake record; write `session.local.md` last as `closed-idle` or
`partial-idle` with the consultation end time; return a closure receipt; and
release its live lease/active ownership while remaining resumable. Do not
forcefully terminate the provider session as a substitute for this fold.

The closure receipt states logical id/generation/session, current model/effort
and evidence, metadata/notes/document/intake paths plus resulting watermarks or
digests, folded-through turn, remaining debt, consultation state and its end
timestamp/mtime evidence, and whether the session remains the incumbent. The
working session verifies the receipt against files and runs the established
session-id Bash check. Under a fresh-per-consult policy, only after this
verification does it remove `session.local.md` and the handoff's incumbent
line; the durable logical bundle remains.

If the advisor hangs or disappears after interaction, the working session
first attempts resume and requests the same close. Once provider and active/
lease evidence establish that no serving advisor can complete it, the worker
may recover continuity in place: archive available transcript, fold only
verbatim or otherwise verifiable conclusions through a contiguous point,
record the interrupted intake and remaining debt, and repair lifecycle and
transport projections. It must not invent an advisor assessment, close an
unproven proof request, or overwrite a live owner. If the remaining state is
not safely reconstructable, fence the generation and start a successor under
the restart rules.

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
The object session must not present its own assessment as the advisor's when
transport is unavailable. It may still give a clearly labeled working-session
assessment and the exact forwardable packet, plus an explicit user choice to
proceed without advisor delivery.
For handoff completeness repair, use `topics/handoffs.md` § Advisor intake for
handoff repair rather than translating a normal challenge memo ad hoc.

## Return and durable notes

Return the memo without laundering it into the object session's preferred
story. Quote or link the advisor memo first; place any object-session rebuttal
or updated interpretation after it as a separate response.

Evaluate every advisor claim under `topics/handoffs.md` § Evaluating advisor
output, not only claims emitted during handoff repair. Verified facts and
non-contradictory adjacent context may repair omissions autonomously; material
conflicts with user-authorized scope remain tentative until the user resolves
them, and advice never supplies authorization for rescope.

`ask` packets and automatic pre-decision triggers hold the material decision
until the advisor has answered the current revision or graehl explicitly
proceeds without it. Reversible prototype work may occur inside the open
interaction and return as evidence. A `tell` packet is non-blocking, but only
reversible preparation should outrun an unreturned challenge on the same
decision.

The advisor updates compact notes and archives completed transcripts according
to its charter. Ordinary interaction traffic remains in its continuous
transcript.
