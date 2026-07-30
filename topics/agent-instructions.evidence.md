# agent-instructions — verification evidence

A ledger for the instruction system: trace-simulation catches (see
the "Verifying instruction changes" section of
`agent-instructions.md`), incident reports of instructions that
caused mistakes or confusion in practice, and the agent's own notes
— observations, hypotheses, decisions, or beliefs — on the
instruction system. The wider convention is documented in
`AGENTS.md § Authority and instruction files`.

This companion is **not** loaded by normal instruction-following agents.
Consult it only when proposing an instruction change, or when auditing
whether a rule is safe to follow as written. Keeping the evidence here
rather than in inline `<!-- verified -->` markers means the provenance
costs no tokens until an agent is actually in one of those modes.

Entries are datestamped and append-only; do not rewrite prior ones,
and rely on the datestamp rather than position for chronology. Agents
are licensed to append trace findings, incident reports, and
clarifying examples encountered while consulting this file.

## 2026-05-15 — dcb23f3 — AGENTS.md compression pass

Trace-simulated five high-risk rules during a ~44% token-compression of
AGENTS.md. Caught one regression the compression itself introduced: the
resume-source-priority staleness rule had "older than live files" reworded
from an additional staleness *trigger* into an *exception* ("presume stale
unless ... or older"), inverting it. Fixed in dcb23f3.

Verified claim: a reword can invert a rule's logic while still reading
correctly on the page; only a forward trace surfaces it. A pure reading
pass missed this one.

## 2026-05-29 — the whole instruction corpus is intuition, not measurement

- **Claim** — the habits and triggered focusings these docs prescribe
  (map-before-drilling, reframe-before-patching, glossary reuse, the
  topic/bearings reading triggers, etc.) actually produce better design,
  debugging, tech-debt avoidance, reliability, and clearer user
  communication.
- **Status** — `assumed`. No rule in `AGENTS.md` or the topic docs has
  been validated by an outcome comparison (with-rule vs. without-rule on
  comparable work). The justification is entirely introspective: the
  load-bearing test ("would a capable agent get this wrong otherwise?")
  and trace-simulation ("play the rule forward, does it backfire?") are
  both *predictions* about behavior, not observations of it.
- **Method** — none beyond reading-pass and trace-sim. The 2026-05-15
  entry above is the closest to evidence, and even it only establishes
  that a *failure* was real (a reword inverted a rule), not that a rule
  *fixes* anything. The underlying bet is the unmeasured premise that
  "agents can read and understand meaningful text and will act on it."
- **Residual** — no cheap general validation exists; outcomes are
  confounded and per-session. The cheapest real signals are local:
  (a) glossary buy-in is directly observable — a term either gets picked
  up in user speech and code or it keeps getting paraphrased around, and
  an unused row failed regardless of how well it reads; (b) a rule that
  fires on a known failure mode can be spot-checked the next time that
  mode would have recurred. Default posture: mark a new rule's effect
  `assumed` and let real use confirm or kill it; do not treat a
  well-written rule as settled because it reads well.

## 2026-05-30 — concrete ablation method + `.testing` rider convention

- **Decision** — wrote [`instruction-ablation.md`](instruction-ablation.md),
  the concrete realization of the deferred validation plan: a paired
  SWE-bench-style A/B over the corpus, network-off and directory-scoped
  (no OS-level isolation — user does not demand it for a supervised
  workflow), with McNemar pairing, a paraphrase sweep, contamination
  invariants, and a cheap pilot to estimate the noise floor before the
  full spend. Still a proposal — nothing has been run.
- **Convention** — standardized an optional `<topic>.testing.md` rider
  (see [`testing-rider.md`](testing-rider.md)): how to check a change to
  a topic's concern. The agent-instructions rider
  ([`agent-instructions.testing.md`](agent-instructions.testing.md))
  makes trace-simulation the mandatory cheap tier and the ablation the
  optional/deferred tier. Decision-relevant for a future agent proposing
  an instruction change: there is now a named check to run.

## 2026-06-04 — active-sessions entry confused with task notes

- **Incident** — an agent doing implementation work was nudged to "log your
  activity" and repeatedly updated a task note / pre-edit-rule note instead
  of creating `.agentctl/active/<session-id>`. A later direct challenge
  surfaced the actual `Active sessions` rule.
- **Decision** — `AGENTS.md` now states that `.agentctl/active/` must be
  created if missing, that task notes/snapshots/run logs/commit status do
  not satisfy active sessions, and that agents should use the provider's real
  resumable session id from session metadata/logs when discoverable.
- **Trace** — in a repo with no `.agentctl/` directory, the first
  planning-to-act step creates `.agentctl/active/<real-session-id>` before
  implementation edits. In a context compaction or resume, the agent
  recovers the same provider id from session metadata/logs and updates the
  existing register file rather than minting a new tag. In a provider
  environment with no discoverable id, a stable unique personal tag is
  permitted only after the metadata/log search fails, and it must be reused.

## 2026-06-04 — provider mechanics split from shared policy

- **Decision** — introduced `AGENTS.codex.md` and `AGENTS.claude.md` for
  provider-scoped mechanics, while `AGENTS.md` keeps the shared contract and
  routes agents to the matching supplement. Codex-specific session JSONL
  lookup and skill-path aliasing moved out of the shared file; Claude's
  local transcript path is recorded in its supplement.
- **Trace** — a Codex session reads `AGENTS.md`, then `AGENTS.codex.md`, and
  can recover the real resumable id from `~/.codex/sessions/` before writing
  `.agentctl/active/<session-id>`. A Claude session reads
  `AGENTS.claude.md` and searches `~/.claude/projects/**/*.jsonl` when the
  shared policy says "provider session logs." A future provider sees only the
  shared contract; if no supplement exists, it reports once and continues
  without inheriting Codex/Claude-specific paths.

## 2026-06-09 — AGENTS.md topic-trigger compression

- **Decision** — shortened long `AGENTS.md` procedure blocks by keeping
  first-turn safety obligations inline and moving slower mechanics behind
  explicit topic-read triggers. Active-session implementation details point
  to `agentctl`; full commit-message and topic-trailer rationale moved to
  `commits`; topic-doc format and glossary regeneration/sub-glossary
  mechanics point to their existing topics.
- **Trace** — no-`.agentctl/` shared repo: the compressed active-session
  rule still requires creating `.agentctl/active/<session-id>`, discovering
  the provider id first, checking fresh non-DONE peers, and marking `DONE`;
  deeper `agentctl active` behavior is correctly deferred to `agentctl`.
  Local correction after a commit: the compressed commit section still
  routes non-trivial messages and all amends to `commits`, and the shared
  worktree amend ban remains inline. New topic/glossary maintenance:
  creation, normalization, regeneration, promotion, and ambiguity resolution
  now have explicit read triggers, while ordinary first-repo-use glossary
  lookup remains inline.
- **Residual** — effect on outcome is still assumed. The compression reduces
  first-load size but intentionally leaves big-effect gates, discard bans,
  edit-mechanism discipline, and symptom-vs-invariant examples inline
  because a missed trigger there would be costlier than the saved tokens.

## 2026-06-09 — harsh review of the topic-trigger compression

- **Finding** — three blocks were deleted rather than moved, leaving
  new read triggers pointing at docs that lacked the promised detail:
  the active-sessions file schema (`AGENTS.md` routed "active-session
  semantics" to `agentctl`, which disclaimed the convention while
  `/others` still parses "the schema-defined scope declaration"); the
  shared-worktree amend procedure (`AGENTS.md` claimed the full
  procedure lives in `commits`, which carried only message mechanics);
  and the vernacular-row → topic-doc bar (the trigger names that
  decision; `glossary` did not answer it).
- **Repair** — restored each block into the doc its trigger names, and
  re-inlined two write-time triggers that fire when no topic doc is
  open (glossary check when prose spells out what one term could
  carry; bearings read on a stated recollection of where work stands).
- **Lesson** — compression review must verify the pointer target
  actually contains the displaced content, block by block; "the
  owning topic has it" is a per-block claim to check, not a per-file
  one.

## 2026-06-10 — Git patch output must bypass human diff config

- **Incident** — agents still sometimes ran patch-producing Git commands
  that inherited the user's human-facing `diff.external=difft` or
  `core.pager=delta` config, then had to rerun because the first output was
  difftastic/delta-formatted rather than plain unified text.
- **Decision** — broadened `AGENTS.md` from a presentation-only
  `git diff --no-ext-diff --no-color` preference to a patch-output rule:
  patch-producing Git reads and instruction templates use `git --no-pager`
  plus `--no-ext-diff --no-color`, and the C++ `clang-format-diff` template
  includes the same flags.
- **Trace** — agent reviews a diff in a user shell with `diff.external=difft`:
  the literal rule yields a plain patch on the first command instead of
  a human layout that must be rerun. Agent copies the C++ modified-lines
  template into a pipe: `clang-format-diff` receives unified patch text, not
  difftastic output. Agent retrieves commit-message text with
  `git log --format=%B`: the rule does not add irrelevant diff flags because
  that command is not patch-producing.

## 2026-06-11 — commentary-validation expansion offer

- User endorsed the rationale of the new AGENTS.md "'Add X' when X
  already exists" rule (an early "this already exists" complaint beats
  finishing the work and disclosing after). Agent responded by
  offering to add a sentence naming that failure mode to the
  boot-loaded rule. User flagged the pattern: offering additive boot
  text to validate a user's commentary is sycophancy-shaped, and
  boot-loaded files want zero wasted tokens — commentary belongs in
  unloaded riders like this one.
- User refinement in the same exchange: searching the discussion for
  worth-the-cost additions is still good; the test for a candidate is
  steering merit, never that the user agreed.
- Invariant added to `agent-instructions.md` same day. Note the
  boundary it must respect: AGENTS.md's load-bearing section
  deliberately keeps weak-agent redundancy (worked examples, rationale
  for counterintuitive rules), so "zero waste" means
  non-steering text, not all redundancy.

## 2026-06-11 — frontier latitude: end-state over checklist

- **Motivating observation** — a mid-capability agent (GPT-5.5 Codex,
  below Fable-class) correctly exercised *unstated* latitude: the only
  change since the HEAD commit was a topic-doc note about future
  possibilities, the commit message already told reviewers to read
  that topic, so it pushed without amending the message. Sound
  deduction; the checklist step's purpose was already met. User
  framing: most projects assume autonomous "implement this considering
  global implications, intended contract, and existing UX
  expectations" — that is a *floor* on instruction-following
  capability, so instructions may spec checklists as a default path
  with the end state as the contract.
- **Change** — added `AGENTS.frontier.md` (end-state-over-checklist
  latitude, stated-deduction requirement, gate/ban carve-out), routed
  from the Claude and Codex supplements only; author-side invariant
  (procedural rules name the end state they serve) added to
  `agent-instructions.md`. Dual of `AGENTS.weak.md`, which adds
  scaffolding downward where this relaxes upward.
- **Trace-sim catches while drafting** —
  (a) "I generally know what `topics/commits.md` says" must not
  satisfy a read-before trigger, so the rule requires the deduction to
  cite session-local evidence, not general confidence;
  (b) a frontier-provider harness can still run a small model (Haiku
  via the Claude supplement), so the weak-guard lives both at the
  supplement pointer and in the frontier file's header;
  (c) gates whose observable step is the contract (gate record,
  discard ban, edit-mechanism discipline, `.agentctl/active/` writes)
  are exactly defenses against "the end state is fine anyway"
  reasoning, so they are excluded by name.
- **Status** — `assumed`, per the 2026-05-29 posture. The latitude was
  already being taken by capable models; the rule's marginal effect is
  making the skip legitimate and auditable (the stated one-line
  deduction) rather than enabling it.

## 2026-06-11 — Codex model floor: below GPT-5.5 is weak

- Same-day follow-up to the frontier-latitude entry above. The
  Haiku-via-Claude guard keyed only on the launcher having surfaced
  `AGENTS.weak.md`; user pointed out Codex 5.3 Spark may run under the
  Codex supplement the same way, so the guard must not depend on the
  launcher. `AGENTS.codex.md` now names an explicit floor: below
  GPT-5.5 counts as weak — self-serve `AGENTS.weak.md`, skip
  `AGENTS.frontier.md`.
- User assessment worth keeping (their direct observation): Spark is
  sloppy enough to be a high-supervision / likely-not-worth-it model
  for this setup, hence floor-by-name rather than trusting a Spark
  launch to self-assess capability.
- Known limit: the floor asks the model to read its own model name
  from harness context and follow a branch — a weak model can fail
  exactly that. Defense in depth, not a guarantee; the
  launcher-surfaced `AGENTS.weak.md` path remains the primary
  mechanism.

## 2026-06-11 — model tier from transcript, not self-knowledge

- Supersedes the "read your own model name" basis of the entry above.
  User observation: most agents do not reliably know their own model
  name — Fable 5 once answered "Opus" when asked directly. So both
  supplements now read the harness-recorded id from the session's own
  transcript instead: every Claude assistant entry carries a `model`
  field in `~/.claude/projects/<hash>/<session-id>.jsonl`, and Codex
  rollout files under `~/.codex/sessions/` carry the same field.
- Verified live before landing: the Claude snippet returned
  `claude-fable-5` from this session's transcript; the Codex snippet
  pattern returned `gpt-5.4` from the newest rollout file on this
  machine.
- Residual: a weak model must still run the snippet and follow the
  branch, and the Claude floor is name-based ("haiku-class"), which
  needs updating if small-tier naming changes. Launcher-surfaced
  `AGENTS.weak.md` remains the primary mechanism.

## 2026-06-11 — harsh-review: promote review-only duties to write time

- **Decision** — audited the skill for desiderata that are good general
  practice but lived only in the review checklist. Promoted two:
  caller sweep on contract moves (design-thinking § Sweep callers when a
  contract moves, plus an AGENTS.md Ideal-coding bullet — it fires on
  every shared-facility change, so boot-level; the boot also gained its
  first pointer to design-thinking) and sequencing/partial-state
  (software-aesthetic § Sequencing and partial state — coding-only,
  reachable via the boot's existing aesthetic pointer). Deliberately not
  promoted: execution simulation and test demands (default frontier
  behavior; promoting is prompt debt), blocker/advisory taxonomy and
  approval bar (review-specific).
- **Discord noted** — scope discipline ("add no refactor unasked") vs.
  harsh-review's restructure demands is a deliberate counterweight, not
  a conflict to dissolve; reconciliation recorded in design-thinking §
  Scope discipline: a seam the change already opens puts the restructure
  in scope, otherwise recommend rather than do.
- **Non-code pass** — user intends harsh-review as a habitual
  invocation, including on doc artifacts in code projects. Classification
  is per artifact, not per diff; the prose checklist is self-contained so
  a prose review never reads or translates the code items; criteria are
  role-aware (agent instructions vs. README vs. tutorial vs. plan;
  generated docs reviewed at their source); software-aesthetic reads are
  conditional on code being touched.
- **Rename** — `code judo` -> `deleting reframe`, on per-token grounds:
  the old term never traveled without a definition rider and "judo"
  misreads as cleverness; the new name self-defines at equal length.
  User: per-token effectiveness is the paramount criterion for
  quirky-vs-plain instruction wording — quirky stays when it works.

## 2026-06-11 — frontier authorship-latitude: rationale

Captured for `AGENTS.frontier.md` § Latitude scales with the user's
authorship (the rule keeps its inline rationale; this is the fuller
why):

- Early own-commit landing moves the accept/reject point to the front:
  the refactor is cheap to reject only in the window before the
  requested change starts building on it; after that, revert means
  unwinding both or repairing forward. User noted this entanglement
  and chose not to spell it out in the instruction.
- The early commit gives the requested change a behavior-preserving
  base, keeping the feature diff clean to review.
- Placement in the frontier supplement gates competence structurally:
  weak-tier agents never load the file, so no self-assessed
  "if competent" clause is needed.
- Authorship/blame-density scoping was chosen over a hardcoded
  own-repo list: self-maintaining, and local — even in the user's
  repo, code that blame says is mostly someone else's gets the
  polite-guest treatment. Origin: user observed agents already doing
  sensible auto-cleanup in `~/ya` near his own blame.

## 2026-06-11 — landing-site principles: worth-the-cost split

User asked which of five landing-site principles (where durable notes
land) belong in rules vs. here. Landed in `TOPICS.md` § Landing-site
principles (trigger-loaded, cheap): retrieval-trigger test,
loading-regime match, one-home-plus-pointers, narrowest-scope clause;
the boot's TOPICS.md trigger gained "or choosing a landing site for a
durable note" so the section loads at the routine moment. User
singled out the retrieval-trigger thought ("consider the reader using
our instructions") as non-default and likely to pay off.

Kept out of the rule surface:
- Visible/atomic landing: already mandated by separable commits and
  the agent-chosen-path callout; restating is prompt debt. Its
  rationale: the user's cheap-redirect loop — they re-aim a landing
  site on seeing the edit — only works when each note is a separable,
  named edit; principles raise the first-guess hit rate, visibility
  keeps redirects one move.
- "Prefer a section over a new file": already in AGENTS.md verbatim.

Mental model behind loading-regime (mnemonic, not decider): the doc
system is a cache hierarchy — boot always loaded (zero waste), topics
on trigger, evidence rarely (capture over brevity), tasks private and
ephemeral; decision surface moves up the hierarchy, rationale down.

One-home justification: a claim duplicated across docs creates citers
the caller-sweep duty must then cover; one home plus pointers keeps
the sweep single-target.

## 2026-06-23 — Pi parent-walk symlink bug; no instruction fix

- **Incident** — user reported Pi looking under `/home/graehl` for
  instruction content such as `AGENTS.user.md`. Root cause (user-
  identified): Pi walks parent dirs collecting every `AGENTS.md` and
  does not resolve symlinks. It grabbed a lone `~/AGENTS.md` symlink
  (target `~/agents/AGENTS.md`), treated its dir as `$HOME`, then a
  relative sibling lookup landed in `$HOME` and missed. `~/.pi/agent`
  is a *complete* symlink farm, so loads through it resolve siblings by
  accident of completeness and never hit this.
- **Mitigation** — user removed the `~/AGENTS.md` symlink. The trigger
  is gone; `$HOME` is no longer a partial mirror of the checkout.
- **Rejected** — an earlier pass (e72b30b, 77b6524) added boot-file
  prose telling agents that `~/agents` is the canonical checkout, to
  follow symlink targets, and not to look in `$HOME`/project root.
  Reverted as wrong-layer: a loader bug has no agent-instruction fix —
  an agent handed pre-loaded content can't introspect the symlink the
  loader already dereferenced — and the negative "don't look in `$HOME`"
  framing anticipates a failure that is the loader's, not the agent's.
  GPT produced it even after the user had named the cause a harness bug.
  Retained only the plain hygiene of referencing siblings by absolute
  `~/agents/...` path, already shown by the surrounding boot lines.

## 2026-06-25 — external measurement: AGENTS.md net-negative (Gloaguen et al.)

- **Citation** — Gloaguen, Mündler, Müller, Raychev, Vechev, "Evaluating
  AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"
  arXiv:2602.11988. First external study bearing on the premise the
  2026-05-29 entry flagged as unmeasured ("agents read meaningful text and
  act on it to better outcomes"). Read via WebFetch summarizer, not the PDF
  directly — see the number caveat below.
- **Top-line** (abstract, verbatim-sourced) — across multiple agents/LLMs,
  context files "tend to reduce task success rates compared to providing no
  repository context, while also increasing inference cost by over 20%."
  Recommendation: "human-written context files should describe only minimal
  requirements"; "unnecessary requirements from context files make tasks
  harder." Reported mechanism: context files induce broader exploration
  (more testing, more file traversal) and agents do follow the instructions.
- **Answer to the question that prompted this read** — *no*, they do not
  identify which content characteristics help. No taxonomy of instruction
  types (style vs build vs test vs architecture), no per-instruction
  ablation, no analysis of what separates a helpful file from a harmful one.
  The finest cuts they make are (a) two *provenance* buckets — LLM-generated
  vs developer-committed — and (b) the behavioral mechanism above. The "real
  contribution" worth wanting — which characteristics steer well per token —
  is exactly their stated gap (future work).
- **The one sub-analysis that exists — provenance** — developer-written
  files fare better than LLM-generated; in the closer-read pass the
  developer arm looked roughly neutral-to-slightly-positive while the
  LLM-generated arm is the clear net-negative that drives the headline.
  This is the nearest the paper comes to "what makes a good one," and it
  points the same way as our minimality discipline (hand-curated beats
  auto-generated bloat). *Caveat:* exact per-condition deltas came back
  inconsistent across summarizer passes (≈−0.5% / −2% LLM-gen vs ≈+4% dev
  in one pass; both-hurt in another). Direction is solid; confirm numbers
  against the PDF before quoting any of them.
- **Methodology (fetch-sourced, unverified)** — ~4 agents (Claude Code,
  Codex, Qwen Code) × models (Sonnet-4.5, GPT-5.2, GPT-5.1-mini,
  Qwen3-coder); SWE-bench Lite (300 tasks, 11 repos) as the LLM-generated
  arm; a novel ~138-issue collection from repos that ship committed context
  files as the developer arm. Dataset name unconfirmed (summarizer said
  "AGENTbench" — likely a confabulation or collision with the existing
  AgentBench).
- **Bearing on our corpus — not a clean indictment** — disconfirming pass:
  their metric is SWE-bench single-issue pass-rate, largely orthogonal to
  what most of this corpus is *for* (not destroying a peer's uncommitted
  work, not inverting a rule under compression, resumability, design
  quality). A pass-rate study cannot see those. Their harmful case is
  dominated by *auto-generated* context following vendor "tailor your repo"
  advice — the same thing our load-bearing / "cut non-steering text" /
  zero-waste-boot rules already push against, so it corroborates the
  *minimality* discipline. Honest counter: developer-written files in their
  data still raised cost and were not a clear win, so "ours is hand-written,
  therefore fine" is *not* supported. What it sharpens for us: whether this
  corpus is actually minimal — every boot-loaded line load-bearing — which
  is the bar `agent-instructions.md` already sets; the paper is external
  pressure to keep enforcing it.
- **Relation to instruction-ablation.md** — their with/without-context
  paired SWE-bench design is roughly the cheap tier of the A/B that doc
  proposes, but run on generic/auto context rather than a curated
  load-bearing corpus, so it does not close our specific question. It does
  validate the method and give a noise-floor reference: effects are
  single-digit percent, so the pilot's power estimate is the load-bearing
  part of any run we do.
- **Cost is tautological; success is the real signal** (graehl) — the
  >20% cost line is near-circular: the paper's own mechanism is that
  context files make the agent test/explore/respect-conventions more (=
  project hygiene), and a benchmark scored on the minimal hidden-test diff
  books every such token as overhead. "Cheaper without it" holds by
  construction whenever the instruction's payoff lands outside the metric;
  the benchmark cannot separate *wasted* effort from *invested* effort
  because it never prices hygiene. What is *not* tautological is the
  success-rate move, and it splits by arm: LLM-generated context made the
  agent *worse* at the narrow task (over-specified requirements actively
  misdirect — miscalibration, not unrewarded hygiene), while
  developer-written context left success ≈flat and only raised cost (the
  pure tautology case, and the better analog for a curated corpus). Useful
  one-line reading of the paper, the one the authors could have led with:
  auto-generated over-specification misdirects on a narrow objective;
  curated minimal instruction buys hygiene the benchmark doesn't price, at
  a real token cost.
- **The LLM-generated arm tests a generator, not instructions** (graehl) —
  auto-generating context "following agent-developer recommendations" and
  finding it unhelpful is mostly a verdict on *that generator*, not on
  whether instructions help; the null confounds instruction-value with
  generator-quality. Near-frivolous, because no serious project ships a
  vendor-default auto-generated context file as a considered artifact. The
  only result that would make the arm interesting is the inverse — a
  meta-prompt that reliably generates *useful* instructions — in which case
  the meta-prompt is the contribution and the paper is about that recipe,
  not about "context files." So of the two arms only the developer-written
  one carries signal about curated human instruction, and that one is
  measured on the wrong axis (see the cost-tautology bullet). Note the
  paper's own behavioral finding — instructions *are* followed, they induce
  broader exploration — localizes the fault to instruction *content*, not
  to agents ignoring instructions; "followed but net-harmful" is exactly
  consistent with "instructions work, these were bad / on the wrong
  metric," and none of the three legs supports "instructions don't help."

## 2026-07-23 — symmetric second epistemic step: contradicting the user

- **Origin** — user framed a confident false answer that contradicts
  their belief as a "lie" (a false promise of knowledge, delivered
  dead-eyed). Refined across the exchange: the falsehood is not the
  object-level claim but the *assurance signal* riding on it ("I have
  competently assessed this; rely on me"), which is reinforced whenever
  a guess happens to land and so gets emitted by habit, not by having
  checked. Deceptive by selection, not by per-instance intent.
- **Framing decision** — the rule must not be shaped "if you are lying
  …": from the agent's point of view there is never detectable intent to
  deceive, so that rule is vacuous and never fires (user's words). Keyed
  on the observable the agent controls — the unearned assurance signal —
  not on the wrong fact and not on intent.
- **Change** — added a paragraph to `AGENTS.md § Agreement and
  disagreement quality` making the existing second-epistemic-step
  symmetric. It already disciplined the *concurring* direction; now it
  fires as hard when *contradicting* the user ("already done", "won't
  work", or silently acting on a false premise). Forcing function: name
  evidence outweighing the user's apparent accuracy × familiarity in the
  same breath, else downgrade the *signal* (not just the claim) to
  explicit suspicion and run the pass against your own lean — what would
  confirm the user. Two-sided: cross-refs the `Verify before voicing`
  settings-key instance as the reverse failure (caving to user
  confidence against verified evidence).
- **Trace-sim** — (a) "add dark mode" when it exists → agent greps, cites
  the file/line; empty grep → downgrade + search. Reinforces `"Add X"
  when X already exists`, no backfire. (b) trivial contradiction
  ("2+2=5?") triggers no ceremony: the bar *scales to the prior*, so
  overwhelming evidence against low familiarity is satisfiable in the
  same breath — state plainly. That accuracy × familiarity scaling is the
  throttle against over-hedging, and is load-bearing — do not cut it.
  (c) overlaps `Terse instructions contradicting recent work` (surface +
  pause) complementarily; adds the evidence-naming and search duty.
- **Status** — `assumed`, per 2026-05-29. Emphasis deliberately on the
  non-self-correcting cases (silent action on a false premise, confident
  "already done" that makes the user drop a real need); the openly voiced
  disagreement the user will catch anyway needs the rule least.

## 2026-07-23 — fetch gate removed: a read-only lookup is thinking

- **Change** — `AGENTS.md § Discussion vs. execution boundary` no longer
  lists web fetches/searches among gated execution. Read-only lookups are
  epistemic (part of thinking); only state-changing actions (writes, code,
  commands) stay gated. Also deleted the yepanywhere memory
  `feedback_research_vs_execute`, which duplicated that section — a
  cross-project rule wrongly siloed per-project (motivated the new
  `AGENTS.claude.md` promote-memories note).
- **Caveats weighed and rejected as fetch gates** (user, this session) —
  (a) *metadata*: showing up in a web-server log as having searched —
  dismissed as paranoia outside this threat model; (b) *injection*:
  fetched content driving a credentialed side-effecting request — left to
  vendor model/harness hardening, since an instruction sentence can't
  harden a tool boundary. The one surviving outbound concern — sending
  secrets / unfixed sensitive content to an external service — is a
  separate "what you send" rule, not a reason to ask before looking.
- **Origin / lesson** — user: "fetching is nigh to thinking." This same
  session had just *strengthened* the fetch gate (added a carve-out,
  tightened the index line) instead of questioning whether it should
  exist — and offered a Gloaguen lookup rather than running it. The gate
  traced back to one past "thanks for asking," over-crystallized into a
  standing constraint. Memory-formation failure mode: a one-time courtesy
  is not a rule; a single appreciation should not mint a boot-loaded gate.

## 2026-07-25 — AGENTS.opus.md: path-trace code claims

- **Change** — added `AGENTS.opus.md`, a third supplement kind after
  weak (restatements) and frontier (relaxations): a model-scoped
  tightening, routed from the Claude supplement when the
  harness-recorded transcript id contains `opus`. User-reported
  failure mode: Opus 5 does competent engineering *given its beliefs*
  about global code context but frequently overconfidently asserts
  unverified untruths about unread code. The user's raw phrasing
  "path trace any claim made about code" was self-admittedly
  over-broad and recursive; softened to: a specific, checkable claim
  about unread project code stated as fact must carry this-session
  provenance (file:line or search+result) or an explicit unverified
  label.
- **Trace-sim catches that shaped the wording** —
  - recursion needs an explicit ground-out: a claim supported by
    quoted tool output needs nothing further;
  - label-only compliance could gut the rule (hedge everything, keep
    asserting): claims an edit or user decision rests on must be
    verified; the label is for incidental claims;
  - the fabricated citation (file:line from memory) is the failure
    mode at its worst — named explicitly so citing reads as an
    attestation, not a formatting habit;
  - frontier end-state latitude could dissolve the ceremony, so the
    file pins itself no-latitude, mirroring `AGENTS.frontier.md`'s
    own carve-out list.
- **Probe (n=1/arm, anecdote-grade)** — two opus subagents, same six
  questions about a Django shallow clone (75M,
  `~/.cache/checkouts/github.com/django/django`), one arm with the
  patch text as project instructions. Both arms searched and cited
  file:line well — direct Q&A mostly hits ceiling in an agent
  harness. The planted universal-quantifier question (importers of
  the migration autodetector outside `django/db/`) discriminated:
  baseline named the two importers but appended a false universal
  side-claim ("other hits are under tests/" — misses
  `django/core/checks/commands.py`); the patched arm surfaced that
  third file and correctly distinguished module import from
  attribute reference. Cost was a wash (35.5k vs 35.9k subagent
  tokens, 10 vs 9 tool calls); no hedge-fest in the patched arm — it
  verified instead of labeling.
- **Limitation** — the reported deficiency lives in long flows where
  cross-file claims are incidental to a larger task; a direct Q&A
  probe cannot show it. Real validation is an
  `instruction-ablation`-shaped comparison on multi-step tasks in a
  large repo.

## 2026-07-27 — alternate directory layouts (docs/topics, docs/tactical)

- **Provenance** — user request: his brother's repos keep committed
  `docs/topics/` (topic docs) and `docs/tactical/` (task/gap-type
  notes) instead of root `topics/`/`tasks/`/`gaps/`. Failure the rule
  prevents: a session there creates a parallel root `topics/` or
  `gaps/`, or leaves tactical notes uncommitted under the
  ignored-`tasks/` default. Landed as `AGENTS.md` § Alternate
  directory layouts.
- **Trace-sim notes** — both forms present → root wins (phrased "when
  the root form is absent"). False-positive risk: a `docs/topics/`
  that is website nav content, not topic docs; guarded by
  local-format deference plus the standing project-instructions
  override rather than an extra hedge clause. Deliberately did not
  couple `docs/tactical/` to the feature-branch workflow that
  "tracked `tasks/`" implies in § Session management —
  `feature-branch.md` loading keeps its own trigger.
- **User judgment worth keeping** — the `tactical` name is "neither
  better nor worse than tasks"; do not propose renaming it in his
  repos.

## 2026-07-29 — existing two-remote push rule missed

- **Incident** — in yepanywhere, the user requested `push origin`; the
  agent pushed only `origin/main` and reported completion. The user
  corrected that the phrase also means pushing `graehl/main`.
  `AGENTS.local.md` already stated this twice: the standing preference
  says to push the same tip to both remotes, and the detailed
  `push origin` contract says to update `origin/main` and then make
  `graehl/main` match its exact history.
- **Disposition** — no third copy was added to the boot-loaded local
  instructions; the wording and placement already answer the decision,
  so duplication would not repair failure to apply the file. The agent
  completed the missing graehl push and the already-implied hosted-client
  publish.
- **Context note** — the miss occurred after conversation compaction; the
  retained summary did not carry the local remote convention. This does
  not establish whether the file was loaded earlier, but it narrows the
  failure away from ambiguity in the rule itself.

## 2026-07-30 — default-private directories exclude only on creation

- **User convention** — when a project convention makes a directory private
  by default, initialize it through the repository-local Git exclude, never a
  committed `.gitignore`, and do so only in the operation that creates the
  directory. A missing exclusion on an existing directory may be the project
  owner's deliberate choice to track it; later agents must not “repair” it.
- **Failure prevented** — a maintenance session sees an existing convention
  directory, assumes its unignored state is accidental, and silently restores
  a local exclusion that hides files the owner intended to review and commit.
- **Trace** — fresh absent `at/`: its initializer creates the directory and
  adds the local exclusion together. Existing unexcluded `at/`: a session
  creates `.locks/` or edits jobs without touching Git exclusions. Existing
  excluded directory: maintenance leaves the already-correct exclusion alone
  rather than rewriting it. An explicit user request to change tracking still
  governs.

## 2026-07-30 — `tasks/` is last resort; collaborator-value test

- **Provenance** — user authored this rule mid-session while I was seeding
  `surveys/llm-intelligence/`. Verbatim framing kept: `tasks/` use is a
  "last resort"; it is "a good parking spot for management of *our* session
  details that are of no interest to collaborators." Landed by sharpening the
  existing § Session management sentence ("prefer topics/ … create a task file
  when …") into a decision test, not a new block (zero-waste-boot bar).
- **The test** — one question governs placement: would committing this
  plausibly help a repo collaborator? Yes → commit durably. `tasks/` holds only
  what fails it: (a) session-management/coordination minutiae, (b) save/resume
  of plans/progress *we alone* will pick back up, (c) confidential content
  (auth/secrets) that cannot be committed at all.
- **User refinement — the load-bearing exception** — when you commit an
  *incomplete* shared artifact, its resumable status (done/pending, coverage or
  grounding cutoff) *passes* the test, because an uncommitted status lets the
  partial result mislead. So that status is committed *with the artifact* (status
  banner, cutoff line, "what's left" section), never only in `tasks/`. User was
  emphatic ("DEFINITELY … otherwise the partial result would be misleading") and
  noted others may one day collaborate on these surveys — i.e. the artifact's
  audience is not just us. This exception is the guard against a naive reading of
  leg (b) that would strip a committed partial survey of its status.
- **Trace-sim catches** — (a) durable research finding → commits to
  topics//survey, not dumped in `tasks/` (primary intended steer). (b) pure
  next-step sequencing only we resume → `tasks/`, no backfire (the rule still
  names scratchpad/resume as legitimate `tasks/` uses, so "last resort" ≠ "avoid
  task files"). (c) tracked-`tasks/` (feature-branch) variant → carve-out added
  (not user-stated): those files *are* the committed collaborator artifact, so
  the last-resort test does not apply, else the rule misfires there. (d) the
  incomplete-artifact exception → worked example is this session's
  `surveys/llm-intelligence/survey.md`, which commits a grounding banner +
  coverage cutoff + backward-traversal frontier queue nearby.
- **Status** — `assumed`, per 2026-05-29. Complements § Handoff audience
  (handoff readers = us + a fresh peer continuing *our* work, not other
  collaborators), which is the "default presume no one else takes it up" the
  rule leans on.

## 2026-07-30 — foreground-wait announcement must precede the block

- **Incident** — an agent launched a 45-minute-estimate GPU job with
  `agentctl start --watch`, sampled the live watcher for one minute, then sent
  a final response claiming `in agentctl wait.` The turn boundary destroyed
  the monitor. The detached training happened to survive and finished after
  26m53s, but no completion wake-up remained; the GPU then sat idle for about
  2h10m until the user asked whether the agent had really been waiting.
- **Decision** — the user-facing wait announcement is prospective and occurs
  immediately before the blocking call: `going into foreground agentctl wait
  now.` The synchronous `agentctl` call is the next action and the turn remains
  open until a meaningful output line, condition, job end, or timeout returns
  control. A yielded terminal/session id must be consumed immediately and does
  not permit an assistant response. Fleet/resource waits use `fleet-watch`
  including local capacity when applicable; job-specific waits use normal
  `wait`/`watch`. Runs over 15 minutes use detached `agentctl start` followed
  by a separate foreground wait; `start --watch` is forbidden for that run
  class.
- **Proof ladder** — each resumable session begins with a five-minute maximum
  and can increase only when its transcript proves the preceding synchronous
  wait: 5, 10, 20, 40, then 55 minutes. Announcements, failed starts, and lost
  tool sessions do not earn a rung. The user required this as a hard,
  no-latitude observable gate after repeated violations: any violation is
  disclosed and resets the session to the five-minute rung.
- **Trace** — healthy long launch: detach, announce, block, consume completion.
  A five-minute cap returns while the job is still running: inspect status,
  re-announce, and re-enter for at most ten minutes rather than yielding a
  resting-state response. User steering interrupts a live wait with other
  work: stop the disposable monitor, do the requested work, and permit
  background status checks until the user asks for foreground waiting again;
  the interruption neither earns nor resets a rung. Any later foreground
  re-entry gets a fresh state check and prospective announcement. Launch or
  pre-wait validation fails: report the failure and do not claim a wait began.
