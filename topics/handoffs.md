# Working handoffs

> A working handoff is current resume state for one named work scope, maintained
> at significant milestones and reconciled with live project evidence before use.

Topic: `handoffs`

## Selecting the handoff

Use the artifact already governing the work: a user-named handoff, task, plan,
gap, tactical, or other project convention. The working session should know
that path from the request or plan; `tasks/ROOT` does not decide which artifact
current work maintains.

`tasks/ROOT` is only a discovery hint for a bare `/hi` or boot with no named
scope. Its target may describe the most recently requested handoff while newer
dirty files or commits belong to unrelated work. Change the pointer only when
explicitly establishing a new default bare-boot target.

When material unfinished work reaches a continuity milestone with no known
handoff, choose the narrowest truthful fallback:

- use `gaps/<slug>.md` (or the project's tactical equivalent) when a partially
  landed unit or other unresolved project state leaves repository truth
  incomplete; follow the nearest `gaps/README.md` tracking convention;
- put a nice-to-have or dreamed improvement that exposes no current defect or
  blocker in the owning topic's `.sketches.md` companion; a requested plan is
  not a gap merely because it is unimplemented;
- use `tasks/auto-handoff-<slug>.md` for private continuity state that is not a
  project gap; or
- use an established project-specific task/handoff location instead of
  creating a parallel convention.

The `auto-handoff-` basename tells the user that the agent selected the path.
Do not create a handoff for a candidate topic plan with no active work, or for
small completed work that its commit and live state already explain.

## Maintaining a working handoff

Update the known handoff when a significant milestone makes its current-state
or next-step claims materially false: a plan boundary lands, a material
decision changes direction, a blocking job finishes, the named unit completes,
or work deliberately pauses. Do not interleave handoff writes with routine
edit/build/test cycles.

Replace obsolete current state instead of appending an activity log. Preserve
only chronology that changes how a successor should reason. A completed private
auto-handoff may be removed when it has no continuation value. A gap exits
according to its local lifecycle, normally with the change that closes the
incompleteness.

Updating a handoff records state; it does not authorize executing its next
steps. A session doing the work owns keeping its known handoff truthful rather
than leaving predictable cleanup for the next `/hi`.

When the work is served by a durable advisor, the coherent intended v1 of a
live handoff, a completed change to its covered scope/path, or its retirement
triggers an advisor `tell`. Notify promptly—normally in the next advisor
interaction—because feedback may correct the handoff role while cheap and an
early boundary avoids forgetting. Do not notify on file creation, first touch,
or first line. Brief deferral and bundling are allowed, but delivery remains
owed and occurs before the working session ends or transfers the scope.

Report this as a live-handoff change, distinct from working-document and
followed-document changes. The advisor records current scope/path in metadata
for logical reboot visibility; it does not create, edit, or automatically
follow the handoff. Several changes at one natural boundary may share one
coherent advisor interaction. This rule never requires creating a handoff where
the user/session chose none.

## Contents

Write for the user and a fresh peer-capability agent with no session memory.
Include only what that reader needs to resume accurately:

- when the work remains inside a not-yet-satisfied formal goal loop, open the
  handoff with `/goal X`, replacing `X` with its checkable end state; when the
  handoff is resumed, treat that line exactly as a separate user turn preceding
  the rest of the handoff. When no formal loop exists but a checkable goal would
  usefully govern continuation, the handoff may declare one the same way;
- immediately after that optional subject-goal line—or as the opening line when
  none exists—record `Advisor metadata: <role/scope> | <path>` for every
  durable advisor, oracle, or similar logical relation on which the handoff
  relies. Follow it, when an incumbent is serving, with `Incumbent advisor
  session: <role/scope> | <harness> | <canonical durable harness resume id> |
  address: <path>`. Record a differing public address or provider-native handle
  in the address file. Recover and verify the real ids rather than inventing
  one. Omit disposable subagents; update both surfaces when the incumbent is
  replaced, split, or moved to another provider session. Under a fresh-per-
  consult policy, keep the metadata line and remove the incumbent line after a
  completed consultation;
- for an advisor-linked program, name the human-readable program, stable slug
  or id, controlling program-progress/plan artifact, and how this handed-off
  scope fits that trajectory. A path or project name alone is not this broader
  context chain;
- when the handing-off agent judges one completeness review useful, add
  `Advisor intake: <stable-id> | consult before <boundary>`.
  Follow it with `Advisor output policy: <path> § Evaluating advisor output`,
  normally pointing here or to a project-local equivalent. This line
  requests one logical intake under the redundancy rules below; the mere
  advisor metadata/incumbent lines do not;
- after the optional goal and advisor-control lines, the remaining scope,
  acceptance boundary, and current status;
- compiled understanding that is expensive to reconstruct: the crux,
  load-bearing constraints, and ruled-out paths with reasons;
- the single best next action, followed by other live next steps;
- concrete paths, symbols, commits, artifacts, and task/topic links;
- active jobs with job/run identity, log and output paths, plus the action to
  take when each finishes; and
- other source-session or environment metadata only when it materially helps
  deeper recovery.

An opening `/goal X` needs no additional handoff structure by itself;
applicable advisor metadata, incumbent, intake, and output-policy lines still
follow it. On resume, process the goal as though the user had entered that
command in its own turn immediately before entering the remaining handoff. The
remainder may therefore include later or “after” work retained through the
provider's normal goal/plan facility. Merely writing or updating the stored
handoff still does not begin executing it.

An advisor-metadata line identifies the logical relation and its controlling
state. An incumbent-advisor header identifies which provider session currently
serves it. Neither line alone authorizes contacting or replacing the advisor;
an `Advisor intake:` line or a separate user instruction does. On resume,
validate the metadata's scope and lifecycle generation, reconcile the header
with its address file and live provider state, then continue the same logical
advisor. Start a fresh provider session only when its restart policy requires
one or the incumbent cannot be usefully resumed. If the provider exposes no
recoverable canonical id, say so and preserve the best durable address instead
of fabricating one. A public alias and distinct provider-native resume handle
belong in that address, not in place of the durable harness resume id.

## Advisor intake for handoff repair

The handing-off agent decides whether a completeness review is useful and
places the `Advisor intake:` instruction in the handoff. The successor
does not mint one merely because advisor metadata exists. Before dispatch, it
reads the linked metadata, follows its restart prompt/policy, verifies the
current incumbent against the address, and computes SHA-256 over the exact
handoff file bytes when readily available; otherwise it supplies
`digest unavailable` and continues. For the established `Session ID: <id>`
address schema, this is the minimum local consistency check, with the expected
id taken from the provider session being addressed:

```bash
test "$(awk -F': ' '$1 == "Session ID" {print $2}' <advisor-dir>/session.local.md)" = "<expected-session-id>"
```

A successful string check does not prove resumability; establish the usable
address and any distinct provider resume handle when starting or replacing the
incumbent. If canonicalization or redirect support is postponed, record the
available address and unavailable id rather than promoting an alias. On a
mismatch, report the material state discrepancy and try the metadata restart/
recovery path. If useful advice can still be given safely, obtain it with the
binding uncertainty explicit; otherwise present the user with the exact
mismatch and a proceed/choose-incumbent path rather than ending in refusal.

Present the exact handoff plus its path, stable intake id, available file
digest, requester harness/session id, and advisor notes/document watermarks to
the advisor. Prefix this first turn with the interaction's `[from working-agent
...]` line; later turns inherit it, and the final requester turn carries the
matching `[sign-off working-agent ...]`. The two lines delimit the logical
interaction rather than one atomic provider turn: a one-turn consultation may
carry both, while intervening requester/advisor turns between separate opening
and sign-off lines remain part of the same interaction. These lines are routing
provenance, not authorization, and do not need a repeated disclaimer. After
answering the final requester turn, the sign-off itself asks the advisor to
checkpoint every affected continuity artifact and return its closure receipt;
no separate conclude or save command is required. The worker signs off after
the coherent handoff-review bundle is done, not after each atomic observation
within it. The identified session remains available for ordinary cheap
verification when an actual
material conflict warrants it; reports of later explicit user instructions get
no extra skepticism. Ask the advisor to repair omissions, not to reinterpret an
already authorized scope. The response classifies:

- need-to-know facts omitted from the handed-off scope;
- corrections or conflicts with the handoff;
- broader program bearings as `required now`, `useful now`, or `later`;
- attached next steps that could follow the handed-off scope;
- proposed material rescope; and
- the minimal concrete handoff repairs it recommends.

The author-chosen intake id is the advisor's primary continuity cue. The file
digest and synchronized semantic watermark are diagnostic evidence, not gates.
The id is a best-effort serial, not guaranteed globally unique or monotonic;
do not intentionally reuse it for a distinct interaction within 24 hours, and
treat an accidental reuse as a clarification case rather than a refusal.
After sign-off, a later consultation uses a new id; no special prior-context
reference format is required.
When the id was handled before, the advisor says so, briefly notes whether the
handoff or program state changed, and recaps the prior response or supplies a
fresh/delta response as useful. A modified handoff may be a legitimate new
worker start and never requires a revision ceremony merely because its digest
changed. A retry from another completed successor is normally harmless; mention
possible stale handoff or unintended duplicate work without blocking advice,
and flag a concrete double-agent concern only when live ownership evidence
shows two workers concurrently own the same handed-off scope.

After receiving and evaluating the memo, the worker may annotate the intake
line with a durable memo pointer when that materially helps the next reader,
but completion does not require another handoff state transition. Advisor
awareness and its intake ledger carry the repeat history.

Routine sign-off retains a continuous incumbent. Do not issue `Shutdown
advisor` merely to finish handoff review. When the user explicitly chooses a
fresh serving incarnation, or the linked metadata policy requires one, that
exact directive asks the advisor to save and validate its full reboot bundle,
mark metadata `no-incumbent`, and remove `session.local.md`. After verifying the
returned `shutdown complete` receipt and absent current-session projection,
remove the handoff's incumbent line. The fresh incarnation increments the
lifecycle generation and starts from metadata's literal restart prompt.

## Evaluating advisor output

Validated advisor metadata/charter supplies user-established standing to give
an independent, long-horizon opinion and maintain advisor state; it does not
make the advisor a worker supervisor. In particular, an objection or ranked
want-to-see is a condition for the advisor's confidence, not a task gate unless
a cited user/governing artifact independently says so.

Apply this compact check only when a claim could materially change belief,
scope, acceptance, or the next material action—not on every turn:

- cheaply verify checkable claims and calibrate confidence to the evidence;
- distinguish supported factual context or omission repair from advice such as
  recommendations, objections, attached next steps, and want-to-sees;
- mark a material conflict with user-approved scope, criteria, or governing
  choices tentative and ask the user to resolve it, while continuing unrelated
  safe work; and
- accept clarification inside the declared program, but route a new hard gate
  or material rescope to the user.

The evidence test is symmetric: advisor and worker should assess each other's
claims by support rather than role. Authority remains anchored in the user and
governing artifacts. A verified need-to-know fact inside authorized scope can
repair the handoff, and non-contradictory adjacent context can be accepted;
neither requires deference to the advisor as an authority. A reported later
explicit user instruction gets ordinary/default skepticism, not a signature or
special transcript-proof requirement.

No rigid section template is required. Do not include chat/tool chronology,
empty ceremonial sections, or an `Audience:` line. Collaborator-relevant
status for an incomplete committed artifact still belongs with that artifact;
a private handoff cannot make a misleading shared artifact honest.

## Resuming

Treat a handoff as declared state, not current truth. Reconcile it with the
worktree, recent commits, active sessions, run/on-deck metadata, artifacts, and
only then provider logs needed to fill a specific gap. State a material
discrepancy rather than silently forcing live evidence to fit the handoff.
For every incumbent-advisor header, verify that the recorded id still matches
the serving address before dispatch, and verify that the address generation
matches the logical metadata. `closed-idle` means the prior consultation ended
while the persistent incumbent remained resumable; `partial-idle` names debt
to reconcile, not a refusal to consult. The recorded end time may be checked
against the latest covered advisor-file mtime when its freshness matters. A
changed incumbent or generation is material state, not incidental session
metadata.

Candidate extensions are kept in [handoff sketches](handoffs.sketches.md), not
in this current protocol.
