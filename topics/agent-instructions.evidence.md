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

## 2026-08-03 — verified provenance for row-wise rewrites

- **Motivation** — expensive translated and paraphrased datasets could carry a
  parallel row-to-source map while a sorting/unpermutation defect silently
  shifted the actual outputs. `RUNS.md` now requires inline source identity and
  independently checked hashes, plus concrete length-outlier pairs.
- **Trace: shifted rows** — a length-sorted translator emits output `i` with
  source metadata `i+1`. Reopening `line_1based` and checking the embedded
  source text/hash catches a stale locator; a frozen length policy can also
  expose source/output mismatch. If the producer shifts text and metadata
  together between equal-length rows, length alone cannot prove semantic
  alignment, so the rule retains operation-specific checks rather than
  claiming length is sufficient.
- **Trace: self-normalized garbage** — an entire batch is shifted consistently.
  Fitting center/range on that same batch merely describes the broken batch;
  the rule limits same-batch fitting to exploration and requires a previously
  frozen operation/language policy for acceptance.
- **Trace: cross-script MT** — valid Chinese-to-English output has a large
  codepoint ratio and looks anomalous under a language-agnostic range. The
  policy is frozen per direction and count unit; tokenizer counts are retained
  when already available, while codepoints remain the universal fallback.
- **Trace: legitimate expansion** — a creative rewrite exceeds the length
  range. The required artifact exposes the actual pair for review and does not
  automatically reject it, avoiding a pressure to make the range so broad it
  ceases to detect failures.

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

## 2026-07-30 — advisor read cursor vs. semantic understanding

- **User direction** — after the first program-scoped advisor handoff, graehl
  asked that an advisor maintain its internal knowledge summary after reading
  followed documents, using the last-read markers in `docs/state.md` or a
  separate understanding file.
- **Decision** — retain the existing two-file separation rather than add a
  third overlapping state file. `docs/state.md` is the mechanical read cursor;
  `notes.md` is the semantic program understanding. Every successful document
  synchronization writes state first, reconciles notes against the material
  deltas, and advances a notes watermark containing the exact state observation
  time and HEAD SHA. A mismatch is explicit reconciliation debt for the next
  advisor activation.
- **Trace** — (a) a followed paper changes its selected incumbent while the
  packet asks about another issue: the advisor reads the paper, updates the
  semantic summary and marker, then answers, so a successor does not inherit
  the old incumbent. (b) only formatting changes: the cursor and notes marker
  advance, but the summary does not accumulate invented narrative churn. (c)
  the process stops after atomically updating `docs/state.md` but before notes:
  the next activation sees the marker lag and reconciles before advising.
- **Status** — `assumed`; the next fresh advisor start should verify that the
  marker mismatch is noticed and repaired without replaying already folded
  transcript archives.

## 2026-08-02 — literary register in implementation talk; decision-request shape

- **Trigger** — a status summary closed a flagged open decision with "yours to
  make, not one to slip in", and posed the decision under a bare "## The
  choice" heading that went straight into option A with no aim sentence. graehl
  named the coda "LLM-assistant-instruction-tuning-ese" and asked why the
  existing rule did not fire.
- **Why it did not fire** — the ban on aphorism and clever reversal already
  existed at `topics/agent-instructions.md` § *Writing rules*, but scoped to
  *writing instruction text*. Nothing extended it to prose written **to** the
  user about an implementation, so an agent following the letter had no rule
  against a balanced-clause sign-off in a status report.
- **Decision** — generalize it in the boot-loaded `AGENTS.md` § *Interaction
  style* rather than duplicate it in `AGENTS.user.md`. The failure is generic
  assistant register, not a graehl-specific taste, and § *Interaction style*
  already owns "no plucky affect". The new text names the concrete defect: a
  balanced two-clause coda hides which half is the claim, and adds no fact.
  The cross-reference to `topics/agent-instructions.md` keeps the two scopes
  visibly related instead of silently redundant.
- **Second decision** — added `AGENTS.md` § *Asking for a decision*: aim
  sentence first ("We want X"), one short self-contained paragraph, oversized
  context reachable by link or exact Ctrl-F substring, never by a coined
  phrase, and no re-opening a settled decision. graehl supplied all four
  constraints across two messages in the same exchange; the coined-phrase
  clause has its own separate trace (he asked "explain - what is this" about
  "the fidelity-vs-latency decision", a string absent from the repo).
- **Naming correction in the same exchange** — the agent had labelled the
  cold-tokenize cost a "fidelity-vs-latency decision". graehl objected that
  harm confined to perf-only internal state is properly a miss cost or
  outlier drag, not fidelity. Half-right and worth recording precisely: the
  *first-view cost itself* is a cache-miss cost and naming it "fidelity"
  invited the confusion, but the *remedy under discussion* — lowering
  `WHOLE_FILE_HIGHLIGHT_MAX_CHARS` — does change rendered output, verified by
  running it (a prose `import` inside a Python docstring tokenizes as a
  keyword when the opening `"""` falls outside the excerpt). Lesson for the
  instruction: name the mechanism, not a compound abstraction spanning two
  different costs.
- **Status** — `assumed`; watch whether summaries stop acquiring balanced-clause
  sign-offs and whether decision requests open with an aim sentence.

## 2026-08-02 — concision scope broadened to everything but doc authorship

- **Why the old rule missed** — `AGENTS.user.md` § *Writing and summary style*
  compressed "implementation and debugging" and explicitly exempted "design or
  research discussion". A request for graehl's input reads as design
  discussion, so a long decision ask was compliant.
- **Decision** — invert the scope: compress everything written to graehl,
  exempt only prose written into project artifacts. Decision asks are named
  in-scope so the carve-out cannot be re-derived.
- **Tension made explicit in the rule** — graehl's other complaint the same
  day was *under*-specification ("undue inference burden", an unsearchable
  coined phrase, a bare "The choice" heading with no aim). Concision and
  self-containedness pull opposite ways, so the rule says which loses: cut
  restatement and narration, never the aim sentence or the identifier.
- **Status** — `provisional` by graehl's framing: run it broadly and see
  whether discussion quality improves. Revert or re-narrow if it reads worse.

## 2026-08-03 — publication preserves local commit order

- **Incident** — after an accidental feature PR, the agent proposed rebuilding
  publication history so that the PR's exact cherry-picked head preceded an
  older completed local commit. That would have made GitHub mark the PR merged
  by changing the local sequence to fit PR bookkeeping. graehl corrected the
  governing invariant: completed local commits reach `origin/main` and
  `graehl/main` in their existing order; only an order-preserving rebase is
  allowed when `origin/main` has advanced.
- **Decision** — `yepanywhere/AGENTS.local.md` now states this as a mandatory
  publish rule and explicitly bans reorder, cherry-pick, squash, fold, or
  reconstruction for PR closure. An unpushed commit that achieves an open PR
  may instead have its message amended with the closing reference before the
  normal ordered push.
- **Trace** — local history `base → A → B`, unchanged upstream: push `A → B`
  to both remotes even if a PR independently carries B's patch. Upstream moves:
  rebase the whole sequence to `new-base → A' → B'`, retaining A-before-B.
  Duplicate PR head exists: amend B's message with the closing reference and
  push the local sequence; never insert the PR commit ahead of A.

## 2026-08-03 — worked example for broad concision

- **Trigger** — after the 2026-08-02 scope broadening, graehl had not observed
  much new concision and asked for a one-shot example. The first proposed
  `Before` was constructed without checking a pre-rule model output; graehl
  challenged its representativeness and required an actual sample at least 72
  hours old.
- **Probe** — a 2026-07-29 `gpt-5.6-sol` transcript predating the broad rule
  showed competent, moderately narrated discussion: concrete finding, causal
  explanation, then next action, commonly in a 60–100-word paragraph. The
  worked negative is a glossary-specific reconstruction of that observed
  shape, not a transcript quotation. Its elision is only token economy.
- **Decision** — preserve the complete target: decision first, then the
  concrete resolution, invalidation, and persistence handles.
- **Trace** — an implementation update and a plan discussion both compress to
  the target form without losing the directory-listing versus glossary-file
  invalidation split. Prose authored into a topic doc remains exempt under the
  immediately preceding scope clause.
- **Status** — `provisional`; the example sharpens the intended behavior but
  does not establish that the broader rule changes model output.

## 2026-08-05 — Edit-anchor failures measured across models

- **Trigger** — graehl reported "many edit failures by a Sol agent" in a YA
  gateway session and asked whether instructions could help. Diagnosis read
  the raw transcript rather than trusting the report's framing.
- **Probe** — `~/.claude/projects/-local-graehl-yepanywhere/703283e9-….jsonl`
  (`gpt-5.6-sol`): 8 failed `Edit` calls / 148. Failure-rate comparison over
  recent same-project sessions: `gpt-5.6-sol` 10/224 (4.5%), `claude-opus-5`
  3/245 (1.2%), `claude-fable-5` 29/167 (17%). So the reported model is *not*
  the worst offender in this corpus — the rule was written model-agnostic for
  that reason, not scoped to `AGENTS.weak.md` or a model supplement.
- **Classes observed** — (1) anchor too short, 3 failures, and the retry
  lengthened the *body* rather than reaching upward to the enclosing
  `it("...")`, so it re-failed at the same 2 matches; (2) anchor composed from
  memory, 3 failures, including an 11-line "Status: Partially implemented…"
  paragraph for a doc that actually read "Status: Partly implemented
  (2026-08-05)…"; (3) line structure guessed, 2 failures, anchoring mid-line
  392 as though a soft wrap were a line break, then retrying with a tab
  substituted for the 3 spaces.
- **Severest instance was not a retry cost** — the agent emitted a literal
  NUL byte where TS source needed `\0`, twice:
  `packages/client/src/hooks/useProviders.ts` (`${sourceKey}\0${providerName}`)
  and `packages/server/src/routes/local-resource-policy.ts` (`raw.join("\0")`).
  Both compiled, both passed tests, and both made `rg` classify the file as
  binary and skip it — a silent search hole. The second reached
  `origin/main`. This is what the escape-sequence bullet exists for; the
  others only cost calls.
- **Trace** — bullet 1 was initially "copy from a Read done in the current
  turn", which would have mandated a re-Read after every self-`Edit` and
  regressed the common Read-then-several-Edits path that *Pre-edit re-Read*
  explicitly blesses. Narrowed to writes made indirectly (subagent, formatter,
  codemod), with own-`Edit` excluded because its `new_string` is visible.
  Two candidate bullets were cut as non-load-bearing: `replace_all` semantics
  and "strip the `NNN\t` prefix" are both already in the `Edit` tool
  description.
- **Status** — `provisional`; the classes are measured, the fix is not.

## 2026-08-06 — foreground work before optional delegation

- **Trigger** — graehl observed that Sol under Codex chose direct tools
  sensibly, while the same model through the Claude gateway spawned more
  subagents than wanted, apparently following Claude Code's injected
  subagent suggestions. In YA, foreground research is more visible and its
  scope is easier to steer than child-agent work.
- **Decision** — optional delegation requires both a likely single-stream
  duration over 10 minutes and independent tracks whose parallel execution
  materially reduces wall time. A long but continuous trace stays in the
  parent. The parent also retains the core trace and synthesis; delegated
  prompts forbid further delegation.
- **Prompt precedence** — generic boot text that advertises, suggests, or says
  to consider agents does not open the gate. An explicitly higher-priority
  instruction that requires a named agent still wins; claiming otherwise
  would ask the model to violate instruction precedence rather than resolve
  generic encouragement.
- **Runtime signal** — YA's `claude-gateway` launch now sets the explicit
  `YEP_CLAUDE_GATEWAY=1` marker in the Claude Code child. This identifies the
  gateway route but not its server implementation: `copilot-api` is an HTTP
  endpoint, not the child's parent, and YA supports generic
  Anthropic-compatible gateways. The Sol-specific correction therefore lives
  in `AGENTS.sol.md`, while the global direct-work rule still governs every
  model and harness.
- **Trace** — a five-minute repository exploration remains direct; a
  20-minute call-chain investigation remains direct because it is one
  continuous trace; a requested 30-minute survey with independent source
  groups may fan out and then return to the parent for synthesis; a mandatory
  specialized-agent instruction still fires; no child may create a grandchild.
- **Status** — `provisional`; the threshold and observed UI advantage are
  user-grounded, but no before/after delegation-rate measurement exists yet.

## 2026-08-06 — split harness mechanics from model behavior

- **Trigger** — graehl clarified that the Claude and Codex supplements were
  initially populated partly for their usual coding models (Opus and Sol), not
  solely for harness identity. Model policy trapped in a harness file does not
  follow Sol through Claude Gateway or a future Opus launch through Codex.
- **Classification** — session identity, transcript/log paths, wakeup
  mechanics, Claude memory paths, Codex skill aliases, capability-tier
  detection, and the YA gateway marker remain harness mechanics. The Codex
  confirmation rule and the Sol-under-Claude direct-work correction are
  behavioral tightenings and moved to `AGENTS.sol.md`. No additional Claude
  rule moved: the remaining clauses describe Claude Code transport and
  persistence behavior, not Opus personality.
- **Routing** — both harness supplements now select `AGENTS.opus.md` for a
  recorded id containing `opus` and `AGENTS.sol.md` for a recorded id with a
  `sol` model-family segment. Model self-identification remains
  non-authoritative.
- **Trace** — Sol under Codex reads Codex mechanics plus Sol behavior; Sol
  under YA Claude Gateway reads Claude mechanics plus Sol behavior and sees
  `YEP_CLAUDE_GATEWAY=1`; Opus under Claude reads Claude mechanics plus the
  path-trace patch; a hypothetical Opus-under-Codex launch receives the same
  Opus patch; another frontier Codex model no longer inherits Sol's
  personality rule.
- **Status** — structural refactor preserving the two moved rules; no
  behavioral-rate measurement.

## 2026-08-06 — explicit Copilot route and stricter delegation proof

- **Trigger** — graehl asked whether both native Copilot CLI and Claude Code
  backed by `copilot-api` could load one stronger Copilot supplement. Native
  CLI already exposes `COPILOT_CLI=1`; the HTTP gateway is not a parent process
  and previously exposed no stable implementation identity to its Claude
  child.
- **Decision** — `copilot-api` advertises `X-Copilot-API: 1` on `/v1/models`.
  YA accepts only that explicit handshake, remembers it for the configured
  Gateway URL, and injects `YEP_COPILOT_API=1` into later Claude settings and
  child environments. URL, port, model ids, vendors, and catalog shape are
  deliberately insufficient.
- **Behavior patch** — `AGENTS.copilot.md` requires a visible pre-spawn line
  naming a direct estimate over 10 minutes, at least two independent tracks,
  and the material parallelism gain. Missing any fact means direct foreground
  tools. It also repeats the no-nesting rule; YA's depth cap is only defense in
  depth.
- **Trace** — native Copilot CLI loads the file from `COPILOT_CLI=1`; a new YA
  Claude Gateway catalog read against the marked proxy yields
  `YEP_COPILOT_API=1` and loads Claude, Copilot, and any matching model
  supplement; a generic gateway on port 4141 does not; changing the configured
  URL clears a previously learned identity; a launch before any successful
  catalog read remains unmarked rather than guessed.
- **Status** — explicit handshake and routing are covered at both HTTP and YA
  environment boundaries; delegation-rate impact remains unmeasured.

## 2026-08-07 — foreign-repo pivot: truncated boot list, "ambiguous publish"

- **Trigger** — an Opus 5 session launched in `copilot-api` pivoted
  mid-session into yepanywhere work. Its project-entry probe `ls
  AGENTS.md CLAUDE.md GLOSSARY.md` recalled the boot list from memory
  and dropped `AGENTS.local.md`; it then read a 45-line slice of
  CLAUDE.md and announced "publish is genuinely ambiguous — three
  release channels" while ya's unread `AGENTS.local.md` defined bare
  `publish` exactly. The supplement chain (user/claude/opus) was never
  loaded, so the existing path-trace patch — whose
  universally-quantified-claim line condemns "nothing defines this" —
  could not fire. Transcript
  `-home-graehl-copilot-api/3e663caa-….jsonl` lines 158 (probe), 260
  (slice), 333 (claim), 347 (post-correction read). Mitigating
  context, per the user: the harness injects no instruction context
  for a foreign repo (an unexercised scenario), the duty fired far
  from the rule text, and cross-cwd launches are a deliberate style
  that usually works — so blame is shared and mitigations must stay
  low-cost and scoped.
- **Decision** — § Project-level instructions now names the
  mid-session pivot, states the no-injection fact, requires copying
  the boot list rather than recalling it, rules out existence probes
  and sliced excerpts as substitutes, and keeps a no-reread guard
  (user constraint: no redundant re-loading of already-read files).
  A follow-on paragraph routes foreign-project requests: target-cwd
  agent for self-contained tasks, context-carrying fork or in-session
  boot reads when prior context matters. `AGENTS.opus.md` gains the
  verb-resolution instance; ya `AGENTS.md` now names
  `AGENTS.local.md` as its machine-local final authority.
- **Rejected** — an "are you sure?" checkpoint before foreign-repo
  big actions: it would tax the user's intended cross-cwd flow; the
  routing preference replaced it.
- **Status** — rule patches only; recurrence unmeasured.

## 2026-08-08 — delegation reshaped: inform depth-1 leaves, don't gate

- **Trigger** — graehl capped max subagent depth at 1 harness-side and
  asked for the matching global rule: "do not overdelegate but do
  consider data-parallel or sequential fold single sterilized
  subagents. subagents will be blocked from creating subagents."
  In-turn clarifications: "sterilized" = no subagent facilities
  "besides to report back to their creator or siblings"; "repeatedly
  is allowed, i do not mean one-shot only"; "main session could spawn
  a goal advisor oracle 'did we finish'"; a serial fold's accumulator
  "can also ofc be mediated through similar handoff files vs only
  messages"; on the fold itself, "i neither encourage nor discourage
  it" — it shares the property of direct work recording digests to a
  log fully read before appending. Decisive steer: "i would not
  presume to intrude on the default harness tendency to create
  subagent etc flows besides to inform of the depth limit … if the
  result seems sensible i do not object"; but Copilot's habit of
  "explicit planning subagents" — "i am not much in favor of that,
  would prefer not." Motive, stated directly: "i do not use lesser
  quality models for impl. and i prefer to see and engage with plans
  as they are built."
- **Decision** — § Direct work before delegation renamed § Delegation
  and rewritten from gate to information: delegation is the model's
  judgment call; the rule informs (depth-1 mechanics, leaf semantics,
  repeatable engagement, three shapes) rather than gates. The stated
  motives live in the rule as the meaning of "do not overdelegate":
  implementation never goes to a lesser model, plans are built
  visibly in the parent (no dedicated planning subagents). Fold
  recorded as explicitly neutral vs. the direct journal-digest
  equivalent. Journal lifecycle: a task's journal starts untracked in
  `tasks/journals/`; no journal is ever committed automatically ("not
  all journals have lasting value"); most are condensed into the
  eventual commit message and discarded; one worth keeping as a file
  is redacted/condensed for value and offered for review before
  publication into `topics/journals/` or a `journals/` subfolder
  beside the plan file. Vocabulary: the rule says *leaf* (standard tree
  term); "sterilized" recorded as the conversational synonym in the
  GLOSSARY row.
- **Supersedes** — 2026-08-06 "foreground work before optional
  delegation": the duration-and-parallelism both-gate is retired
  globally; it survives only as the Copilot route's proof line.
  Retained as preference rather than gate: core trace and synthesis
  in the parent; injected "consider agents" boot text is a capability
  advertisement, not a default.
- **Route notes** — `AGENTS.copilot.md` keeps its strict proof
  (self-contained now that the global gate is gone) and adds the
  planning-subagent ban. `AGENTS.sol.md` § Direct work under Claude
  Code softened to match the trust extended to advanced models
  (opus/sol/fable).
- **Trace pass** — advanced model delegates a sensible parallel
  Explore sweep unprompted: allowed without ceremony (the point of
  the steer). Copilot spawns a planning subagent: blocked by its
  route supplement. A delegated prompt whose plan assumes the child
  can spawn helpers: blocked by leaf mechanics. A 20-minute
  continuous investigation folded away to save context: still
  counter-indicated ("do not fold away the core investigation").
- **Status** — `provisional`; user-specified; no delegation-rate or
  outcome measurement.

## 2026-08-08 — native agentctl watch timeout preserves exit provenance

- **Incident** — a Fable session ran `timeout 3300 ./agentctl watch ... 2>&1 |
  tail -3`. Bash therefore presented `tail`'s status as the pipeline status,
  while `timeout`/termination lines and agentctl's watched-job return code
  appeared together as body text. The resulting explanation had to reconstruct
  which exit belonged to the payload, shell wrapper, pipeline tail, and tool
  call. The user initially attributed the command to Sol, then corrected the
  model identity to Fable; the failure and fix are model-agnostic.
- **Decision** — add `watch --timeout` beside its existing `--tail`. Terminal
  completion still returns the watched job's exact exit code. Observation
  timeout leaves the job running and returns 124 plus the stderr magic marker
  `[agentctl-watch-timeout-v1]`; the pair distinguishes it from a payload that
  itself exits 124. `RUNS.md` now forbids the shell wrapper/pipeline form and
  gives the native one-command replacement.
- **Trace** — a running job with `--tail 2 --timeout 3300` replays two existing
  log lines, streams additions, and returns 124 + marker at 55 minutes without
  stopping the job. A job that exits 7 first makes `watch` return 7. A job that
  exits 124 first produces the terminal done line and no marker. A poll interval
  longer than the remaining timeout sleeps only to the deadline rather than
  overshooting by a full poll.
- **Status** — implementation and regression coverage added; behavioral effect
  on future agent command choice remains unmeasured.

## 2026-08-08 — optional technical glosses are epistemic claims

- **Incident** — a `claude-fable-5` status summary correctly limited a result
  to primary-stage routing, then volunteered this parenthetical:
  `Gemma-4 honors copy instructions; TranslateGemma barely takes instructions
  at all`. The vague scalar phrase made graehl doubt whether the agent understood
  TranslateGemma's translation-specific interface, a fact he otherwise would
  have assumed from the untouched model name. The extra prose reduced
  confidence and forced an object-level audit.
- **Technical check** — Google's [TranslateGemma model
  card](https://huggingface.co/google/translategemma-27b-it) says the supported
  chat template accepts exactly one text/image content item with source and
  target language codes and produces translation; the documented content schema
  has no arbitrary-instruction field. The card also says manually constructed
  alternate prompts may work but are unsupported. Because open-weights callers
  control input construction, deterministic schema rejection can enforce any
  desired `refusal` before inference; no learned refusal is needed for this
  interface. The supported template is a caller-side interface, not a model
  refusal policy.
- **Diagnosis corrected after the check** — given those facts, `barely takes
  instructions at all` is reasonable high-level shorthand and likely indicated
  that Fable shared the correct interface model. It is not evidence that Fable
  misunderstood TranslateGemma. The failure remains communicative: a volunteered
  graded gloss made graehl verify that understanding. The interrogation happened
  to correct graehl's mistaken belief that TranslateGemma was trained to refuse
  invalid formats, but he explicitly retains the style preference because the
  same audit cost has recurred across many other Anthropic-model interactions.
- **Scope** — the user-level rule records how graehl interprets every agent's
  volunteered gloss: exact, deliberately diagnostic, or omitted. The observed
  recurring pattern is Anthropic-family style, with this incident supplied by
  Fable; graehl has not observed it in Sol. The stronger worked correction
  therefore lives in `AGENTS.anthropic.md`. Both harness supplements route
  recorded `claude` model ids there; Opus continues onward to its additional
  subtype patch. This avoids attaching an unobserved model-specific defect to
  Sol while preserving the general communication preference.
- **Trace: shared term is sufficient** — a summary says the escalation gap is
  the known TranslateGemma placeholder-discipline effect and stops. The rule
  adds no explanation; confidence is preserved without expansion.
- **Trace: mechanism matters** — a comparison relies on arbitrary copy
  instructions being available in Gemma-4 but absent from TranslateGemma's
  supported template. The rule states that interface difference rather than
  grading TranslateGemma as generally bad at taking instructions.
- **Trace: uncertain understanding** — an agent suspects a model accepts only
  translation controls but has not checked. `My current model: the supported
  template has no arbitrary-instruction field (unverified)` exposes the useful
  possible misconception without dressing it as an explanation.
- **Trace: explicit partial disagreement** — graehl says, `TranslateGemma only
  allows strict-template prompt performance`. The agent states the split rather
  than silently accepting or vaguely rephrasing it: the strict template is the
  supported interface, but `only allows` is too strong for open weights because
  callers may send manually constructed token sequences; any guaranteed
  rejection is caller-side. This trace is already required by `AGENTS.md`
  § *Agreement and disagreement quality* plus the new gloss rule, so it adds no
  duplicate boot instruction.
- **Status** — the recurring style cost and preference are user-observed; the
  family scope and behavioral effect remain `assumed`, with no cross-model
  outcome comparison.
