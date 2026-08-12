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
  blocker in the owning topic's candidate-improvement or `## Sketches`
  section; a requested plan is not a gap merely because it is unimplemented;
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

## Contents

Write for the user and a fresh peer-capability agent with no session memory.
Include only what that reader needs to resume accurately:

- when the work remains inside a not-yet-satisfied formal goal loop, open the
  handoff with `/goal X`, replacing `X` with its checkable end state; when the
  handoff is resumed, treat that line exactly as a separate user turn preceding
  the rest of the handoff. When no formal loop exists but a checkable goal would
  usefully govern continuation, the handoff may declare one the same way;
- immediately after that optional subject-goal line—or as the opening line when
  none exists—repeat this header for every durable advisor, oracle, or similar
  co-session that is deliberately resumed and grown across interactions:
  `Incumbent advisor session: <role/scope> | <harness> | <canonical resumable
  session id> [| address: <path>]`. Recover and verify the real provider
  id rather than inventing one. Omit disposable subagents and fresh-per-review
  sessions; update the header when the incumbent is replaced, split, or moved
  to another provider session;
- after the optional goal and incumbent-session lines, the remaining scope,
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
applicable incumbent-advisor headers still follow it. On resume, process the
goal as though the user had entered that command in its own turn immediately
before entering the remaining handoff. The remainder may therefore include
later or “after” work retained through the provider's normal goal/plan
facility. Merely writing or updating the stored handoff still does not begin
executing it.

An incumbent-advisor header identifies which accumulated co-session is serving
the work; it does not authorize contacting or replacing that advisor. On
resume, reconcile the header with its address file and live provider state,
then continue the same session. Start a fresh advisor only when the governing
lifecycle deliberately replaces the incumbent or the recorded session cannot
be usefully resumed. If the provider exposes no recoverable canonical id, say
so and preserve the best durable address instead of fabricating one.

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
the serving address before dispatch; a changed incumbent is material state,
not incidental session metadata.

## Sketches

If bare `/hi` repeatedly fails to discover important simultaneous work, consider
a plain `tasks/OPEN` manifest naming `tasks/ROOT` plus other open tasks. Do not
introduce `tasks/open/` merely for categorization: nested files would escape
existing `tasks/*.md` discovery, while a symlink set would add cleanup and stale
membership failure modes. Adopt either form only with observed misses and a
defined writer, freshness signal, and retirement lifecycle.
