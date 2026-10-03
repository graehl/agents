---
slug: pstack-concepts
noticed: 2026-10-03
where: topics/acli.md; topics/testing-rider.md; topics/handling-bug-reports.md; skills/harsh-review/SKILL.md; topics/explanation-style.md; user/MASTERY.md
---

**Source:** Lauren Tan's (poteto) pstack, canonical upstream
`github.com/cursor/plugins` path `pstack/` at `9511e60` (2026-10-03);
harness-neutral mirror `github.com/backnotprop/pstack`. Local cache:
`~/.cache/checkouts/github.com/cursor/plugins/pstack`. Below, pstack
skill names are paths under its `skills/`. This sketch borrows concepts
only. Copying any skill text would be vendoring
([vendoring](../../topics/vendoring.md)).

**Outcome:** routine project steps become rerunnable tools whose output
is mostly a verdict, so agents spend turns and tokens on judgment, and
the user's reading time goes to the current approach, its alternatives
and its warning signs. Eight threads follow. Each gives what pstack
offers, what `~/agents` already has, and the proposed move.

## 1. Project verify tools, with a ladder of judgment checks

- *pstack:* `create-verification-skill` writes a project-local
  `verify-<app>` skill with Launch / Doctor / Drive / Evidence / Cleanup
  sections plus a `features/` map (one file per user-facing feature,
  each ending in an observable proof state). The skill must run end to
  end once before it counts as delivered. `maintain-verification-skill`
  keeps the map honest. Read-only subagents read source per feature;
  then one coordinator drives every feature live. Each pass ends
  `clean`, `changed` or `blocked`. `principle-prove-it-works` and
  `principle-explain-the-number` cover outputs and measurements.
- *Here:* a [testing-rider](../../topics/testing-rider.md) says how to
  check a change to one topic's concern. UI work has
  [ui-verification](../../topics/ui-verification.md). Nothing gives a
  project one `verify` entry point.
- *Proposal:* a per-project `scripts/verify` acli tool with tiers.
  `verify` (cheap, deterministic, seconds) prints one verdict line plus
  any exceptions. `verify --deep` adds slower deterministic suites.
  Above those sit agent-run judgment tiers, named in the project's
  instructions rather than built into the tool: soft-check review
  ([soft-checks](../../topics/soft-checks.md)), live drive of a feature
  map, then harsh-review. Each tier runs only when the tiers below it
  pass and the change class warrants it. Doctor (is this instance worth
  driving?) becomes a `verify doctor` verb.

## 2. Lasting project tools whose output is exceptions and a bottom line

- *pstack:* `principle-build-the-lever`: any non-trivial edit,
  analysis or check produces a script, codemod or generator. "Applying
  this principle produces a file." `principle-encode-lessons-in-structure`
  and `correct` give a mechanism order: architecture, then types, then
  a lint whose error names the fix, then a test, and prose rules last.
  `correct` keeps a rule-to-enforcer table in the agent instructions.
- *Here:* [acli](../../topics/acli.md) is the output contract, and
  global § Multiple-use helper tools defaults retained helpers to
  `scripts/`. Nothing yet pushes agents to *create* such a tool when a
  manual check recurs, and no instruction states the output budget:
  quiet on success, full detail only for what needs judgment.
- *Proposal:* add a quiet-success profile to acli. Default output is
  the verdict plus exceptions. Traces that need judgment are written to
  a named file and their path is printed. The tool's help lists the
  evidence it does *not* check, so the agent knows what is left for it
  to examine. Trigger: the second time a session hand-runs the same
  check sequence, it builds the tool. Consider `correct`'s
  rule-to-enforcer table as a column in the evidence ledger.

## 3. Hash-bound beliefs about project state (not in pstack)

- *pstack:* closest are `recall` (reconstruct state from transcripts
  plus shared records, then verify against live `git`/`gh`) and
  `show-me-your-work` (an append-only TSV decision log whose evidence
  column holds pointers, audited against the transcript at the end).
  Neither binds a claim to the inputs it was derived from.
- *Here:* run provenance hashes inputs and outputs
  ([provenance-tracking](../../topics/provenance-tracking.md)), and
  [auditable-agent-traceability](auditable-agent-traceability.md)
  covers action audit. Neither covers "where is X implemented?" or "is
  the training run healthy?".
- *Proposal:* an acli `belief` tool. `belief record <key> --claim TEXT
  --inputs <paths|git-rev|run-id> [--check CMD]` stores the claim with
  hashes of its inputs (git blob ids for tracked files, mtime+size
  then sha256 for large outputs, a run record's hash). `belief get
  <key>` returns the claim marked `fresh`, `stale (inputs changed: …)`
  or `unverifiable`. `belief recheck` re-runs `--check` only for stale
  entries. A fresh belief saves rediscovery. A stale belief names the
  input that changed, which is cheaper than a full re-search. Open:
  storage (untracked `.agentctl/beliefs/` vs committed), and whether
  code-location beliefs should key on a symbol (via `code-map`) rather
  than a file.

## 4. Spend some tokens keeping the user educated

- *pstack:* `teach` runs `how` and `why`, gives the smallest complete
  answer first, then builds diagrams one part at a time. It bans quizzes
  and pacing theater. `show-me-your-work` closes with an "Attention"
  section written by a reviewer from a different model family: weak
  evidence, skipped verification, risky choices. All of it is on
  demand; nothing teaches as a side effect of ordinary work.
- *Here:* [explanation-style](../../topics/explanation-style.md)
  (refresher trigger) and `user/MASTERY.md` (at most one reconstruction
  prompt at a natural boundary).
- *Proposal:* the user's goal always carries a learning component, so
  the visible text should be what that component needs. Ideas, none
  validated:
  - A fixed end-of-task "approach and alternatives" slot of at most
    three lines: the path taken, the strongest rejected alternative,
    and the warning sign that would mean the path is wrong. These are
    what the user can steer.
  - Hide routine tool steps that tell the user nothing about the
    approach. This is mostly a YA rendering question: fold passing
    verify runs and plain reads, and show decisions and exceptions.
  - Test: does the slot change the user's next instruction more often
    than its absence does? Needs an ablation
    ([instruction-ablation](../../topics/instruction-ablation.md)).

## 5. New features go in new files (anti-god-file)

- *pstack:* `correct` assumes each agent sees only the files it opened
  and copies the nearest example, so the repo must make the local
  change right for the whole repo. `principle-minimize-reader-load`
  and `principle-model-the-domain` say the same at module level. pstack
  has no explicit new-file rule.
- *Here:* [software-aesthetic](../../topics/software-aesthetic.md)
  § "one named home" per question-sized concept, with a guard against
  splitting into a file per tiny function.
- *Proposal:* a sharper default inside that section: a new feature
  with its own state or entry point starts in a new file in the
  related folder. Adding to a file that is already past a project size
  threshold needs a stated reason. Enforce with a ratchet lint (item 8)
  rather than prose.

## 6. Route external reports to the right running session

- *pstack:* `automations/benny` has a triage automation that
  classifies a report, traces the owning layer, dedupes against the
  tracker, and posts exactly one verdict with a marker. A separate
  repro-and-fix automation waits for that marker, stops if someone
  already owns the fix, and verifies an existing PR instead of
  competing with it. It fails closed on missing config. There is one
  triage and one fixer. Routing to *already running* sessions is not
  covered.
- *Here:* `agentctl` active sessions carry a banner and `scope:`, and
  `session-turn` / SendMessage can deliver turns.
  [handling-bug-reports](../../topics/handling-bug-reports.md) covers
  intake within one session.
- *Proposal:* a project triage session (a steward-like role, as in
  [on-deck](../../topics/on-deck.md)) that reads the live sessions'
  `scope:` and gist lines plus gaps and handoffs, and routes each
  report to the session whose intent owns it. It uses `session-turn
  send --eventual`, marks the turn as peer-authored, and opens a gap
  when no session owns the report. Borrow benny's gates: one verdict
  per report, and no fix if someone already owns one.

## 7. Group intake so one upstream fix can cover several reports

- *pstack:* benny dedupes against tracker duplicates only. The
  closest is `principle-fix-root-causes`.
- *Proposal:* the triage session clusters open reports by suspected
  causal layer before anyone fixes them, and writes one gap per
  cluster that lists its member reports. A fix closes the cluster only
  after each member report is re-checked. A member that does not
  reproduce is a finding, not a closure. This applies "fix the
  invariant" (global § Code quality) across reports.

## 8. Periodic pattern finders feed a batch-decision queue

- *pstack:* `correct` ("If the pattern is already common, fail only
  when a change adds more"; exceptions on the offending line with a
  reason and an expiry), and `reflect`, whose Backlog list holds items
  better enforced by structure than accepted as prose.
- *Here:* harsh-review is a range review with a contiguous high-water
  marker, run every few days on `~/ya`.
  [tool-surprises](../../topics/tool-surprises.md) mines logs for
  repeat failures. Both are periodic and batched, the same shape as
  this item.
- *Proposal:* scheduled finders (lints, `rg` patterns, a cheap model
  pass) append hits to a queue file per project and never fix inline.
  The working session is not interrupted, and scope does not creep. A
  periodic batch pass, the same rhythm as harsh-review, decides each
  cluster once: revise the finder (false positive), make one sensible
  change (sweep), or add a ratchet so the pattern stops growing.
  Harsh-review advisories could feed the same queue. Open: queue
  format (a gap file per cluster vs one JSONL), and whether `/at`
  ([at-scheduling](../../topics/at-scheduling.md)) or on-deck owns the
  cadence.

**Open decisions:** which item to prototype first (`scripts/verify`
plus the quiet-success acli profile looks most immediately useful on
`~/ya`); whether items 6–8 share one queue-and-triage substrate; how
to measure item 4.
