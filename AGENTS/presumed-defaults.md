# Presumed frontier defaults

> Rules removed from the boot on the presumption that current frontier
> models follow them unprompted, kept verbatim so each can be restored.

No session reads this file routinely. It is the audit list for the trial
recorded in `topics/frontier-capability-review.md`: restore a passage to
`AGENTS.global.md` when a session trace shows the behavior it asked for was
missed, and delete it here once restored or judged unnecessary.

Removed 2026-11-10 from `AGENTS.global.md`.

## From § Verification and retrieval

When entering unfamiliar code, first map relevant modules/callers in project
vocabulary, then drill down. Before a wide change, audit, or edit to an
uninspected file, read the full file or full relevant module/section, not
isolated snippets that hide callers and guards.

## From § Code quality: Anti-slop implementation

Do not add permissive fallbacks, softened preconditions, broad exception
swallowing, or proceed-on-partial-state behavior merely to make the current
trace pass. Establish required preconditions or fail clearly unless recovery is
part of the documented contract.

The boot keeps the paragraph that followed, on tolerant parsing in throwaway
orchestration, with the durable-script bar restated in its last sentence.
Fuller rationale: `AGENTS/change-delivery.md` § Anti-slop implementation.

## From § Code quality: Fix the invariant, not the symptom

Name the violated contract behind a visible defect and fix its owning
mechanism. Block special cases, suppressions, regex cleanup, CSS overrides, or
caller workarounds that hide only one projection. When similar fixes already
exist, treat duplication as a finding: keep the best invariant owner and remove
shadow fixes unless layers have distinct deliberate contracts. UI/layout and
software-structure details live in `topics/ui-verification.md`,
`topics/functional-layout.md`, and `topics/software-aesthetic.md`.

Fuller rationale: `AGENTS/change-delivery.md` § Fix the invariant, not the
symptom.

## Removed from `AGENTS.opus.md`

Both were written for Opus 5 incidents in August and September 2026. Global
policy already covers each: project-entry reads bind on a pivot to another
repository and the push gate stops on an ambiguous target; § Matching
processes by pattern holds the safe search forms.

### Request verbs resolve from instruction files, not repo scanning

"This request verb is ambiguous/undefined here" is a
universally-quantified claim — it needs the search that would falsify
it. Before declaring a big-effect verb (`push`, `publish`, `deploy`,
`release`) ambiguous or choosing its target, confirm the full boot
list of `AGENTS.global.md` § Project-level instructions was read this
session for the repo being acted on — copy the list from that
section, do not recall it — then cite where the verb is defined, or
state that the read files do not define it. Already-read files are
not re-read.

### Process searches self-match

Check the command text before running any process search: if the pattern
you are searching for appears in the command, the command matches
itself. Rewrite it rather than running it and reading the result.
Knowing the trap does not substitute for the check, and frontier
end-state latitude does not discharge it. `AGENTS.global.md` § Matching
processes by pattern holds the safe forms.

A poll whose match count never drops is self-matching until shown
otherwise. Never explain an anomalous duration from process-search
output alone — confirm the work through output size, exit status, or the
destination file.
