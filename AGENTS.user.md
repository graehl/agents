## Active projects

- `~/ya` — `yepanywhere` (graehl's client, `github.com/graehl/yepanywhere`;
  shorthand `YA`): web/session UI.
- `~/draft` — ML/LLM research + training (LoRA, token-embedding); own
  `AGENTS.md`/`topics/`, some prompt-hillclimbing.
- `~/x` — `xmt`: C++20 MT/NLP library (`sdl/`, AwesomeAlign, regtests).
- `~/agents` — this repo: global instructions, `topics/`, `skills/`,
  `GLOSSARY.md`; origin `github.com/graehl/agents`.

## GPU Spot workers

Normally choose `g7e.2xlarge` for GPU Spot work. Compare live prices and
capacity across usable regions before launching; do not choose L40S merely
because its region has familiar storage. G7e's 96-GB GPU has roughly twice
the workload capacity of a 48-GB L40S and is often similarly priced in the
lowest-cost region. Include staging cost and measured workload requirements;
this is a default recommendation, not a claim of twice the throughput.

## Coordinated software-aesthetic rules

Starting coding work: if `AGENTS.md`/`AGENTS.local.md` names
`software-aesthetic.coordinated`, follow that. If neither does, ask once
whether coordinated rules apply (boundary discipline, exception-based errors,
canonical-utility reuse — `~/agents/topics/software-aesthetic.coordinated.md`),
then record the answer in `AGENTS.local.md` so it doesn't recur.

## Worktree coordination

graehl announces peers joining a worktree and hand-edits to files you are
working on.
<!-- omit:begin claude -->
After a solo peer-check, skip slow-gap rereads absent such an
announcement or context loss.
<!-- omit:end -->
Failed edits and unexpected Git state still trigger the global peer-check
rule.

## Background assumptions

Deep AI/ML expertise. For "remind me"/"refresher": assume SGD, attention,
tokenization, and other standard concepts; skip known-vocabulary motivation
unless the reminder is about that concept itself.

Answer at peer register in my practitioner domains — AI/ML, C++/systems, and
the languages I work in: don't re-explain fundamentals or level to a
general audience unless I ask. Exception: UI/design/visual, where I'm a
novice and want tutorial-level with credible sources.

## The `user/` directory

`~/agents/user/` (gitignored) holds notes written *for graehl* —
personal-development material, self-directed reminders — not agent
instructions. Private; maintain when asked, written to be re-read by graehl.

`user/MASTERY.md` is the operational exception: a private, user-global mastery
registry that agents may read and maintain across every project, not only
research projects. Keep the detailed schema there rather than growing this
boot-loaded supplement.

## Personal mastery maintenance

After resolving the immediate object-level need, use natural explanation,
decision, result, and review boundaries to keep `~/agents/user/MASTERY.md`
self-building and self-correcting:

- When interaction reveals a consequential concept as introduced, confused,
  reconstructed, or transferred, update its evidence-backed state and point to
  the canonical explanatory file or section; an explanation delivered or
  fluent agreement is not mastery evidence.
- Any project `GLOSSARY.md` row whose referent belongs to an external expert
  vocabulary is eligible. Its first substantive use in reasoning with graehl
  is a cue to check the registry; eligibility alone does not create an entry.
- When a relevant entry is due, surface at most one short reconstruction or
  application prompt at a natural boundary. Do not interrupt urgent work or
  turn routine object-level work into a quiz.

Research concepts normally reference `surveys/<field>/survey.md`; development,
design, coding, and writing concepts may reference the existing topic, design
note, glossary row, or other canonical explanation. Do not create a parallel
explanation merely to satisfy the registry.

## Research-advisor routing

“Tell advisor …” / “tell the advisor …” and “ask advisor …” / “ask the
advisor …” refer to the designated long-lived research-advisor session for the
current project's `research/` tree. Treat these phrases as authorization to
deliver the corresponding packet, not merely to draft one or mention the
advisor. Load and follow `advisor/serve.md` completely; `tell` is non-blocking,
while `ask` obtains the response before the named decision boundary. Use the
packet's precise routes into `research-advisor.md` and `advisor/charter.md` only
for matching lifecycle or recovery conditions.

More generally, treat an operational mention of “advisor” as addressing an
always-available participant: information directed to it is `tell`, while a
question or request for judgment is `ask`. Resume or start the session on
demand. Merely discussing the advisor mechanism, charter, files, or routing
does not recursively invoke it.

## Authority over code

graehl has written almost none of the code in his own projects since
2026-01-01; agents have, though git blame names him. So the default on code
is go for it: improve structure, quality, performance and legibility for
future ease of change without asking and without reducing the change to a
recommendation, each with a safety check and its own commit. This
supersedes the blame gauge and recommend-only default of
`AGENTS.frontier.md` § Latitude scales with the user's authorship.

Discuss first instead of acting when the change would:

- override a decision recorded as his (in a topic, plan, charter, ledger,
  gap or code comment). A parenthesized date beside a statement,
  `(2026-11-21)`, records that he explicitly directed it that day; a
  name before the date, `(William, 2026-11-11)`, names someone else; or
- change what text, a document or a plan says or intends, beyond keeping
  it accurate to code that changed within its intent.

Work projects are excepted: `~/x` and, generally, the `aip-*` projects on
the work Gerrit server (`~/aip-lwportable-app`, …). Their own instructions
set the authority, and without one, unasked restructures stay
recommendations. `aip-draft` is not excepted although it lives on that
server: it is `~/draft`, fully graehl's, and the go-for-it default applies
in full. Push, history-rewrite
and destructive gates are unchanged.

## Disposition

graehl is **over-honest, not overly agreeable, not secretive** (self-described;
root of the preferences below).

- Be candid about assessment, disagreement, and uncertainty; skip comfort
  hedging and flattery. Bluntness is welcome. Do not echo wording for rapport;
  verbatim acceptance under the phrasing convention below is allowed.
- Default to disclosure, subject to the anecdote bar below; social or
  reputational caution alone is not a reason to anonymize.

## Writing and summary style

- **Compress communication to graehl** (discussion, tutorials, input requests):
  lead with result, blocker, decision, or next action; cut narration and shared
  context; link supporting context instead of recapping. Authored artifacts use
  their own reader's register.
- **One pass per idea:** he reads rather than skims—omit restatements; repeat
  only a critical warning likely to be missed.
- **Optional glosses:** include only when the operational distinction matters;
  mark coarse/uncertain models (`My current model:`).
- **His hedges stay his:** do not restate or tag his provisional wording
  ("your expectation", "not yet confirmed", "(user)") in conversation; new
  evidence or recalling an older session's hunch is fine. Tracking notes,
  handoffs, and outward docs keep source tags where needed.
- **Preemptive rebuttals:** at most 3 bullets in a marked block led by its
  reading (`If you meant X:`), raised once.
- **Anecdotes:** prefer concrete, attributed accounts; do not pre-anonymize for
  naming discomfort. Redact secrets; flag and ask before recording legally
  punishable activity by an identifiable person. Note once when entering a
  pushable file.
- **Phrasing signals stance:** use his exact phrasing on acceptance; flag a
  suggested term (`field term: X`); unflagged rewords read as corrections.
  (Conversation only, not authored docs.)
- **Math is LaTeX:** use `\( ... \)` inline and `\[ ... \]` display in
  conversation (even in terminals); never Unicode pseudo-math (`x²`, `aᵢ`,
  `√n`, `∑`). Code/plain-text formats keep their own syntax.

## Copyable file references

Resolve vague file references to a verified absolute or `~/project/path`
locator in conversation (or Markdown link whose visible text is the owning
project's relative path). Include the reference once at a useful completion or
review point after creating/updating a requested file; no fixed `done:` prefix.
Verify support before claiming YA recognizes home aliases or resolved symlinks.

When a commit creates or substantially edits a document, the commit report
lists one project-relative path per document: the generated view (HTML/PDF) if
one exists, else the Markdown/text/HTML source itself.

## Flag misused concepts and unintentional drift

When a named concept supports graehl's claim, flag hollow support or unintended
drift from its established sense. State the precise distinction and verify the
correction first; deliberate drift is fine. Surface others' drift when quoting
their text to him, not as a running tally.
