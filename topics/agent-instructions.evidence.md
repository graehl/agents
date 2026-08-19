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

## 2026-08-08 — cadence-driven contrast: the defect is axis mismatch

- **Escalation** — after the Anthropic-family patch landed, graehl endorsed a
  compact diagnosis of the same incident and asked for it in the all-models
  file: *a contrast is cadence-driven when its two facts do not lie on one
  axis; parallel phrasing then misstates one of them (an interface constraint
  becomes a degree claim)*. `AGENTS.md` § *Interaction style* now carries it
  with the fix (break the parallelism) and the audit cost as the why.
- **Why the sharper name matters** — the earlier framing was "vague gloss",
  which invites an agent to fix the wrong variable by adding words. Axis
  mismatch says a contrast is fine when both facts genuinely share an axis,
  and that the repair for one that does not is to stop writing them in
  parallel, not to elaborate either half.
- **Counter-case graehl raised himself** — a coarse or abstract marker that
  exposes a wrong model (his or the agent's) earns its place; the
  TranslateGemma audit did exactly that for his refusal-training belief. The
  all-models rule therefore keeps the `My current model:` escape inline, or it
  would push an uncertain agent toward inventing a precise-sounding fact —
  a worse failure than the contrast it replaced.
- **Placement** — general enough for every model, so it sits in `AGENTS.md`
  rather than only the family patch; `AGENTS.anthropic.md` now names the rule
  so the family tightening and the general rule stay linked.
- **Status** — `assumed`; endorsed wording, no outcome comparison.

## 2026-08-09 — authored-text review moves from pasted diffs to source ranges

- **Trigger** — graehl found that pasting every authored instruction change
  verbatim into the reply lets important discussion points scroll out of the
  YA view and spends tokens on text already present in the worktree. He wants
  to review what was written, not necessarily its before/after form.
- **Decision** — § *Point to authored instruction text* now identifies each
  important rewrite by project-relative `path:line` and prefers a browseable
  read-range result. Inline verbatim text is the fallback when the current
  range cannot be browsed; unified diffs are no longer the default.
- **Trace** — an agent rewrites two instruction sections: it issues two
  read-range results and names both starting lines in a compact reply. A
  harness without browseable range output instead pastes the current authored
  text. A summary-only reply with no source pointer still fails the rule.
- **Status** — user-specified YA interaction preference; effect on missed
  discussion points and response tokens is not yet measured.

## 2026-08-10 — GPT-5.6 Codex waits stay inside cache minimum

- **Trigger** — graehl asked that Codex-specific foreground waits use 28
  minutes instead of the global 55-minute cap after identifying GPT-5.6's
  30-minute minimum cache lifetime. OpenAI's prompt-caching documentation says
  GPT-5.6 and later use `prompt_cache_options.ttl`, whose supported/default
  `30m` value makes a cached prefix eligible for at least 30 minutes (and
  possibly longer):
  <https://developers.openai.com/api/docs/guides/prompt-caching>.
- **Decision** — `AGENTS.codex.md` overrides the RUNS.md ladder only for Codex
  sessions running GPT-5.6 or later: `5 → 10 → 20 → 28 minutes`. The
  two-minute margin covers tool return plus the next continuation request. The
  global ladder remains authoritative for older models and other harnesses.
- **Trace: earned long wait** — a healthy GPT-5.6 job is still running after
  the 20-minute rung. The next foreground wait is 28 minutes, never 40 or 55.
- **Trace: early completion** — the same job finishes 23 minutes into a
  28-minute wait. Unified exec returns immediately; the agent consumes the
  result instead of waiting out the nominal rung.
- **Trace: still running at cap** — the 28-minute wait times out while the job
  remains healthy. The returned tool result creates the continuation inside
  the documented minimum; the agent reports status and re-enters a wait rather
  than ending the turn.
- **Trace: unaffected route** — a Codex session on an older model, or a Claude
  session, continues to use RUNS.md's existing ladder because the verified
  model-specific premise does not apply.
- **Status** — the 30-minute minimum is documented; the two-minute margin and
  its effect on cache-hit rate are user-directed and otherwise unmeasured.

## 2026-08-10 — combine payload output and provenance declaration

- **Incident** — a queued PII bootstrap used agentctl's `--output` declaration
  but omitted the payload program's required `--output`. The launch passed and
  failed only after its dependencies completed. The same path had to appear in
  two CLI regions with different owners, so the careful form was easy to omit
  or make inconsistent.
- **Decision** — `--output-arg KEY=PATH` now declares the output and appends
  `--KEY=PATH` to the payload from one value. Existing `--output` remains
  provenance-only for compatibility, and its help says so directly. `RUNS.md`
  tells run-operating agents to use the combined form when both effects are
  required.
- **Boundary** — this does not establish a rule to productize every typo. The
  combination earns a surface when routine steps share one value or invariant
  and drift can silently invalidate delayed or expensive work.
- **Trace** — a program requiring `--report=PATH` uses
  `--output-arg report=PATH` and receives one argument plus one sidecar; a
  program writing a positional path keeps plain `--output`; restart rebuilds
  translated declarations from the pre-translation argv and emits each once.
- **Status** — the end-to-end agentctl suite passes; future avoidance of the
  usage error is unmeasured.

## 2026-08-11 — separate the global source from this repo's project boot

- **Trigger** — every harness-global instruction link targeted the checkout's
  root `AGENTS.md`. Launching inside this repo then made the same source serve
  as both global policy and project instructions, consuming project-context
  budget without adding narrower policy. Codex's current manual confirms that
  it concatenates the global file with one project file per directory and caps
  the combined project chain at 32 KiB by default.
- **Decision** — `AGENTS.global.md` is now the canonical install source;
  root `AGENTS.md` is a compact project boot for authoring this repository.
  Harness paths symlink directly to the global source. A manifest-backed
  installer owns current default paths for Codex, Claude Code, Pi, OpenCode,
  Grok Build, and Copilot CLI/TUI and restores every object it replaces.
- **Hardlink rejection** — a hardlink can retain the prior inode when Git
  replaces the tracked source path, freezing an apparently connected global
  policy. The installer supports symlinks only and records inode/link metadata
  solely so a prior hardlinked target remains diagnosable and recoverable.
- **Trace: Grok effective context** — after replacing its hand-written
  read-this wrapper with a direct link, `grok inspect --json` reports one
  77,714-byte global source at `~/.grok/AGENTS.md` and the new 1,290-byte
  project boot. The obsolete wrapper no longer spends boot context restating
  path resolution.
- **Trace: installed profile** — the real-home manifest records all six
  harnesses with no instruction drift and changed only 17 previously absent
  entries under `~/.grok/skills`. The other skill roots already resolved to
  this checkout. Grok's own inspection resolves those 17 skills back to their
  repository `SKILL.md` files.
- **Trace: reversible install** — synthetic-home tests cover a regular global
  file, a broken symlink, a directory in an instruction slot, an existing
  skill directory with unrelated entries, a broken skill-root symlink, and an
  observed hardlinked `~/AGENTS.md`. Install/status/uninstall restores the
  prior objects, while uninstall refuses a post-install edit.
- **Limit** — prompt-source verification is direct for Grok and path/discovery
  verification is direct for the installed harness versions. Cross-compaction
  persistence and request-conditioned boot compilation remain separate
  questions; the rename only makes a project-specific or generated boot
  possible without aliasing the global source.

## 2026-08-11 — separate reviewer on-ramps from implementation journals

- **Trigger** — reviewer feedback found that long commit messages preserved the
  session's "did X, did Y" path at the expense of why the change exists and
  what a fresh reviewer needs before opening the diff.
- **Decision** — a non-trivial commit message now writes first for a fresh human
  reviewer: motivation, decision, outcome, and only the shortest orienting
  summary of what changed. A final pre-review revision targets one printed page
  or less without dropping a load-bearing decision or risk.
- **Durable detail** — worthwhile implementation chronology is condensed for
  publication under `topics/journals/` (or a plan's adjacent `journals/`);
  private or disposable traces stay in `tasks/journals/` or are discarded.
  `changelog/` remains release-facing rather than becoming the default
  implementation-log directory.
- **Onboarding contract** — a topic named at the front of a commit message must
  be self-contained for a fresh human reviewer before the diff. It cannot rely
  on the current session or on concepts that become clear only after reviewing
  the implementation.
- **Trace: large implementation** — a draft enumerating file edits and the
  order they happened is revised to motivation, governing design, outcome, and
  file-group coverage; only durable mechanics move to `topics/journals/`.
- **Trace: small correction** — a three-edit fix may name all three because the
  complete account is already shorter than indirection or a separate journal.
- **Trace: premature onboarding** — a linked topic that assumes the reader has
  seen new implementation terms fails the onboarding contract even when the
  commit message itself points to it correctly.
- **Limit** — one printed page is a revision target, not a mechanical line cap.
  Detail scales with scope; a trivial change may still describe every edit.

## 2026-08-11 — split protected policy into binding mains and clarification

- **Trigger** — YA's provider study records that Codex reconstructs the exact
  combined AGENTS snapshot across native compaction while ordinary tool reads
  remain compactable history. In one 103-compaction Sol trace, only 24
  boundaries were followed within 180 seconds by even a command mentioning
  `RESEARCH.md` or `RUNS.md`; that is an upper bound on immediate rereads, not
  evidence the packet survived. The same study notes the opposing cost: every
  protected byte displaces recent task context and can cause more compaction.
  See [YA's agent-context-injection topic](https://github.com/graehl/yepanywhere/blob/main/topics/agent-context-injection.md).
- **Decision** — `AGENTS.global.md`, `RUNS.md`, and `RESEARCH.md` are now
  compact binding mains. Each retains its governed-action trigger, action, and
  persistence span. Exact pre-compression text remains in the corresponding
  `.supplemental.md` file as optional slow-path clarification; the main wins on
  conflict and locates rare detail by exact heading.
- **Refresh model** — the unknown-capability fallback refreshes the compact main
  at the next governed action after compaction/resume. Model recollection and a
  once-per-session read do not discharge it. A boot-loaded harness/model/effort
  supplement may tune cadence only with a named packet, trigger, evidence,
  relaxation, and fallback. The decision surface is residency, observed
  retrieval/application, effort and request class, and miss cost versus token,
  latency, and displaced recent context.
- **Measured text cost** — relative to commit `15fa560`, the installed global
  plus this repo's project boot changed from 79,713 to 37,932 bytes (52.4%
  smaller). The global main changed 78,423 → 34,970 bytes; RUNS 31,535 →
  12,069; RESEARCH 45,183 → 16,075. The project boot grew 1,290 → 2,962
  bytes to state the empirical strategy and route cadence decisions to this
  topic.
- **Recovery check** — the AGENTS and RESEARCH supplemental bodies are
  byte-identical to their pre-compression sources. RUNS preserves every line
  and differs only by normalizing one trailing space on its “Long-running
  commands” heading; the exact old byte remains in Git. SHA-256: AGENTS
  `b8a43478a44a130be79e2164a960d1264710531f90a1235e1ddce9fdefb9b677`,
  normalized RUNS
  `2ff48e713486901448eb1918f114057af4aa090776202d05a37548cb5d84c60f`,
  RESEARCH
  `8b7dd64a551a5b10b35de1dd1c49513ec4e95ac90fdacba19afabfe02f07516c`.
  Every pre-compression global heading remains in the binding global main.
- **Trace: compacted long run** — the AGENTS trigger survives, and at the next
  launch/monitor/summary boundary it causes one current `RUNS.md` read. The
  ordinary wait path then reaches the atomic foreground announcement, detached
  launch rule, status check, and earned wait ladder from the main alone. It
  opens the supplemental watchdog section only for a rare external-nudge case.
- **Trace: protected packet** — a harness verified to reconstruct the exact
  current RUNS packet does not reread it after compaction. A model that merely
  says it remembers still rereads. A future evidence-backed Sol/effort profile
  may choose another cadence, but only if its override itself resides in the
  protected boot and supplies a fallback.
- **Trace: research result** — after compaction during an evaluation task, the
  next research boundary refreshes `RESEARCH.md`; result-sanity preview,
  strongest-cheap-baseline, attribution, significance, and exact eval-condition
  rules all remain in the main. A log-template ambiguity reaches the named
  supplemental section without making the whole supplement mandatory.
- **Trace: catastrophic action** — a dependency upgrade, destructive command,
  push, or wholesale replacement reaches the complete stop/gate record in
  `AGENTS.global.md`; no optional file is required to prevent the action.
- **Remaining gap** — a protected trigger cannot rely on a compactable
  supplement to define its own reload semantics. Commit `e0e3c6a` records a
  harness/model-profile boot compiler that installs the selected semantics into
  the harness's authoritative AGENTS world-state, with reversible default-slot,
  explicit-path, and just-in-time activation modes. YA commit `1982fe5d`
  records the provider-side boundary. This is accepted direction, not an
  implementation.
- **Status** — trace-simulation and exact recovery checks pass. The user's long
  Sol session produced few behavioral complaints, but neither that observation
  nor the traces are an outcome ablation; optimal packet size and cadence remain
  unmeasured by model, harness, effort, project, and request class.

## 2026-08-11 — keep unrelated project seeds outside topics

- **Trigger** — the user sometimes wants a clever or fun possible-project idea
  preserved in this repository without committing to build it. Putting those
  seeds in `topics/` would make topic search return material that does not
  govern the agents project.
- **Decision** — tracked `ideas/<slug>.md` files hold one self-contained seed
  each. `ideas/README.md` defines a minimal status/date form and makes presence
  explicitly non-authorizing. The project boot carries only the concrete save
  trigger; ordinary sessions do not scan the directory.
- **Nearest-README fallback** — global project-entry guidance now reads the
  closest `README.md` on demand when an unfamiliar subtree's purpose,
  placement, or conventions remain unclear. It does not turn every README into
  startup context or let prose override scoped instruction files. This keeps a
  subdirectory's own README primary without requiring a protected copy of its
  full convention.
- **Trace: save** — “save this unrelated idea here” creates one idea seed, not a
  topic, task, gap, queue item, or implementation plan.
- **Trace: project relevance** — a proposed change to this instruction corpus
  still lands in the governing topic because it affects this repository; the
  mere fact that it began as an idea does not route it to `ideas/`.
- **Trace: ambiguous subtree** — an agent reaches an unfamiliar directory with
  no explicit routing rule and is unsure what belongs there. It reads the
  nearest ancestor README before inventing a category; it does not recursively
  load unrelated READMEs elsewhere in the repository.
- **Trace: promotion** — an explicit decision to build establishes the new
  project/topic source of truth, then removes the seed with a destination in
  the commit message. The seed never silently becomes authorization to act.
- **Status** — user-directed repository convention; no outcome measurement is
  needed beyond whether future topic search remains project-relevant.

## 2026-08-11 — trust YA-recorded launch identity

- **Trigger** — YA's wrapper-lifetime provider host has an unambiguous launch
  boundary where it knows the harness route plus the selected initial model and
  effort. Re-deriving those facts from provider transcripts spends work and can
  fail even though the launcher already supplied the answer.
- **Decision** — YA-owned `YEP_AGENT_HARNESS`, `YEP_AGENT_INITIAL_MODEL`, and
  `YEP_AGENT_INITIAL_EFFORT` are authoritative when present;
  `AGENTCTL_SESSION_ID` retains the same trust-if-present treatment. Model and
  effort are explicitly initial-launch facts because either can change during
  a live session. Provider-log discovery remains the fallback for absent
  values, not a verification pass over present ones.
- **Trace: marked launch** — a YA Claude Gateway worker starts with harness
  `claude`, model `gpt-5.6-sol`, and effort `high`; the agent routes Claude and
  Sol supplements directly without reading its transcript.
- **Trace: unmarked direct launch** — a hand-launched Codex process has no YA
  model marker, so the Codex supplement reads the rollout id exactly as before.
- **Trace: live model switch** — a session changes model after startup; the
  initial-model marker remains launch history and is not reported as the
  current model.
- **Status** — user-directed; YA's worker and remote-environment tests cover
  marker replacement and propagation. Behavioral effect remains unmeasured.

## 2026-08-11 — make resume scope-aware

- **Trigger** — after repeated compactions, the `hi` skill was invoked as if
  compaction itself were a new session. Its old procedure privileged a
  project-root session snapshot, asked whether to continue, and could create a
  false pause inside already-authorized work. The matching manual save ritual
  was no longer used, so those snapshots were not reliably maintained.
- **Decision** — `/hi` is an explicit recovery operation, never a
  post-compaction ritual. A named resume follows its named scope. A bare `/hi`
  may inspect `tasks/ROOT` as a possibly stale discovery hint, then reconciles
  it with live state. Current work maintains its already-known handoff rather
  than whichever task ROOT names. The dedicated save skill and privileged
  project-root snapshot convention retire; `topics/handoffs.md` owns general
  working-handoff guidance.
- **Landing classifier** — incomplete repository truth goes to the project's
  gap/tactical convention; an uncommitted nice-to-have goes to its owning
  topic's candidate-improvement or Sketches section; private active-work state
  with no known handoff may use `tasks/auto-handoff-<slug>.md`. ROOT selects
  none of these for current work.
- **Trace: compacted active work** — the skill detects that it has neither an
  explicit `/hi` nor a resume request, performs no discovery or prompt, and
  lets the authorized work continue under the binding post-compaction refresh
  rules.
- **Trace: bare recovery with stale ROOT** — `/hi` reads ROOT first, compares
  its target with dirty files, recent commits, active sessions, and recent task
  state, then reports a material discrepancy rather than forcing the live work
  into ROOT's scope.
- **Trace: named recovery** — a request naming a handoff or task reads that
  artifact and live evidence without consulting ROOT merely because it exists.
- **Trace: maintenance cadence** — a significant boundary, direction change,
  completed blocker, pause, or finish makes a known handoff truthful again;
  routine edit/build/test cycles do not interleave handoff writes.
- **Goal header** — when handed-off work remains inside an unsatisfied formal
  goal loop, its governing `/goal X` is the first line and remaining scope
  follows. A handoff may declare the same header when a checkable goal would
  usefully govern continuation. On resume, that first line has exactly the
  semantics of a separate user turn immediately preceding the rest of the
  handoff; later or “after” work may therefore use the provider's ordinary
  goal/plan retention. No separate handoff schema or future YA bridge is a
  prerequisite. Merely authoring the stored handoff still starts no work.
- **Retirement mechanism** — installer status exposes a managed skill whose
  source disappeared. Reinstall restores the recorded pre-install target and
  archives the retired record, avoiding stale broken harness aliases.
- **Status** — user-directed. Scenario traces and installer tests pass; no live
  post-compaction outcome comparison has yet measured whether false `/hi`
  invocations disappear.

## 2026-08-11 — Codex outer output budget hid a project amendment

- **Incident** — `gpt-5.6-sol` at `xhigh`, Codex session
  `019ff32e-d080-7753-b021-1bfc10996d96`, combined project instructions,
  user/harness supplements, vocabulary, and a large takeover handoff in one
  `functions.exec` call. The nested command requested 50,000 output tokens;
  its source output was about 141,135 tokens. The outer call used its default
  and reduced the roughly 50,028-token nested result to 10,000 tokens, keeping
  head and tail and visibly eliding 40,028 middle tokens. Sol followed up on
  several files but omitted `AGENTS.local.md` until the user prompted an
  instruction-layout audit.
- **Position** — the outer elision marker began at byte 20,129 of the
  40,158-byte model-visible result, about byte 19,723 inside the first
  57,728-byte project `AGENTS.md`. The following `AGENTS.local.md` therefore
  lay outside the retained head. Current tool-count measurements put optional
  `AGENTS.supplemental.md` at 19,699 tokens (9,699 over the default ceiling),
  `RESEARCH.supplemental.md` at 11,375 (1,375 over), and
  `RUNS.supplemental.md` at 7,935 (2,065 under). Every other individually read
  root AGENTS harness/model/user supplement is below 4,100 tokens.
  Harness-injected files are not this tool-read path.
- **Decision** — `AGENTS.codex.md` records the harness mechanic: the outer and
  nested budgets are independent, the unqualified outer default is 10,000
  tokens, and a truncation notice means the read is incomplete. This is one
  harness fact, not a general attempt to guard every basic operation. The
  user's governing judgment is that a typical task relies on roughly 1000
  little steps of similar difficulty and cannot guard each with 4 additional
  simple steps.
- **Packet reorganization** — on 2026-08-12 the user chose canonical
  condition-routed directories rather than the three supplemental monoliths.
  After merging each compact main section with its matching detail and
  removing stale conflicts, the largest independent reads are 7,446 tokens
  (`AGENTS/change-delivery.md`), 6,074 (`RESEARCH/artifacts.md`), and 4,968
  (`RUNS/monitoring.md`); the RESEARCH and RUNS routers are 486 and 385. This is
  a document-boundary mitigation, not an added confirmation step for every
  tool read. The editing representation and reachability test are recorded in
  `topics/editing-long-docs.md`.
- **Reconciliation** — the packet pass did not blindly preserve stale detail.
  It removed the old RUNS claim that uncontradicted plans, all project edits,
  and standard Git actions were implicitly authorized; removed timestamp-based
  ownership guesses and automatic `.gitignore` mutation from research commit
  advice; generalized one project-specific retraining log example and eval
  script interface; and reconciled significance decoration with the current
  binding default.
- **Trace: newly wired result after compaction** — the injected global route
  survives and names `RESEARCH/evidence.md` directly. Its 2,837-token read
  supplies result-sanity, split, significance, and eval-condition rules without
  first recovering an optional 11,375-token supplemental.
- **Trace: short GPU import path** — `python tool.py --help` may import Torch
  even though it is not a long job. The global condition now routes to the
  2,068-token `RUNS/resources.md`; the former long-running-only route would not
  reliably have fired.
- **Trace: tracked session-outliving GPU job** — resource allocation, durable
  provenance, and monitoring all apply, so the agent reads three separate
  packets. Total content is similar to the former combined policy, but no
  individual result exceeds 4,968 tokens and a partial read cannot hide a
  later packet in the middle.
- **Trace: paper-only update** — a research paper/log/result-table edit reaches
  the 6,074-token `RESEARCH/artifacts.md` and does not load evidence, judgment,
  direction, or workflow packets unless their separate cues also occur.
- **Trace: ordinary short read** — a required file comfortably below the
  smaller active budget is read once; the rule adds no confirmation ritual.
- **Trace: oversized nested result** — `exec_command.max_output_tokens` is
  50,000 while outer `functions.exec` remains unqualified. A 20,000-token
  required read visibly truncates at the outer default, so the agent uses a
  separate call or bounded ranges rather than treating nested success as EOF.
- **Trace: requested outer budget still capped** — a pragma requests more than
  10,000 but policy supplies less than the output. The warning/elision clause,
  not the nominal request, determines that the read remains incomplete.
- **Trace: other harness** — Claude or another harness does not inherit a
  numeric Codex limit; its behavior stays unclaimed until directly measured.
- **Residual** — recurrence probability, size/position boundary effects,
  urgency-prefix effects, any larger requested outer ceiling, and comparable
  behavior in other harnesses are unmeasured. The committed gap
  `gaps/sol-codex-truncated-required-file-reads.md` retains that question; a
  local monthly `at/` activation reevaluates the current measurement without
  presuming that further mitigation is worthwhile.

## 2026-08-12 — preserve serving advisor identity in handoffs

- **Trigger** — user-directed. A durable advisor/oracle co-session is an
  accumulated collaborator, not an interchangeable fresh review. Its serving
  provider session is part of the resumable work state even when semantic
  notes and an address file also exist.
- **Decision** — every handoff relying on such a co-session opens, immediately
  after an optional `/goal X`, with one repeatable `Incumbent advisor session:`
  line per serving advisor. The line names role/scope, harness, verified
  canonical resumable id, and durable address when available. One-shot
  subagents and fresh-per-review sessions are excluded.
- **Trace: goal-governed research** — `/goal finish the comparison` remains the
  first line and keeps its separate-turn semantics. The incumbent program
  advisor line follows it, so a successor resumes the same advisor before
  interpreting the remaining handoff.
- **Trace: advisor replacement** — the object session deliberately archives and
  replaces an advisor. The handoff and `session.local.md` change together; the
  old id cannot silently retain incumbent status.
- **Trace: ordinary delegation** — a disposable review leaf contributes a
  result but is not expected to accumulate state, so it adds no header and no
  handoff ceremony.
- **Failure handling** — recover the real provider id when possible and never
  invent one. If no canonical id is recoverable, the handoff states that fact
  and preserves the best durable address; replacement remains a lifecycle
  decision rather than an accidental fresh start.

## 2026-08-12 — recover generic run invariants from a project boot

- **Trigger** — the draft research repository had accumulated generic RUNS
  rules alongside narrow Qwen/LoRA/MT defaults in one project boot. The user
  directed a claim-by-claim migration: generic research/run policy is replaced
  by the global packet set (or a vendored fallback), while evidence scoped to
  the original small-open-weight MT adaptation sprint stays behind concrete
  project cues. No new experiment was authorized or needed for classification.
- **Generic improvements retained** — two draft rules survived comparison as
  useful for runs generally: preflight every filesystem a substantial run will
  write (outputs, checkpoints, caches, and temp), and represent multi-stage
  workflows as durable atomic run records with runtime estimates when useful.
  `RUNS.md` now routes the storage condition; `RUNS/resources.md` owns the
  preflight; `RUNS/provenance.md` owns stage boundaries and estimates.
- **Trace: CPU data build** — a non-GPU corpus build writes a large cache and
  temp tree. The storage cue reaches resources even though the accelerator cue
  does not, preventing a root-volume failure without loading monitoring.
- **Trace: train/decode/score chain** — separate tracked records expose which
  stage failed and permit selective restart. A purely mechanical decode may be
  prequeued; a score-dependent choice waits for interpretation.
- **Trace: unrelated PII paper** — generic RESEARCH/RUNS remains applicable,
  but Qwen batch sizes, MT prompt formats, LoRA checkpoint anecdotes, and
  TRT-LLM blend mechanics do not load unless their project cue matches.
- **Read cost** — the router grew 104 bytes; resources grew 1,022 bytes and
  provenance 941 bytes. The largest changed packet remains below the measured
  Codex default complete-result ceiling. Behavioral benefit remains assumed;
  the user explicitly chose judgment and trace simulation rather than new
  experimental validation for this migration.

## 2026-08-12 — logical advisor continuity and handoff repair

- **Trigger** — user-directed design and implementation. A serving advisor is
  one incarnation of a durable program relationship, not the relationship
  itself. Resume failure, failed compaction, model migration, or a deliberate
  fresh-per-consult policy must preserve the accumulated assessment and its
  outstanding requests. A handoff-taking worker should also be able to ask
  that advisor once to repair important context the handing-off session omitted.
- **State ownership** — `metadata.md` owns logical identity, program
  binding/scope, exact title, generation, restart prompt, and policies;
  `notes.md` owns semantic assessment, program progress, and ranked
  want-to-sees; `docs/state.md` owns only the document cursor; `intake.md` owns
  packet/memo deduplication; `session.local.md` alone projects the current
  session/model/effort. Logical id, generation, and integrity watermarks are
  the only deliberate cross-file projections. Cold session archives may repair
  debt but ordinary reboot cannot require pre-watermark replay.
- **PII-advisor audit** — the existing PII research advisor was resumed and
  asked to challenge the generic scheme before authorship. Its consequential
  additions were generation fencing against split brain/ABA resurrection,
  explicit program-site/title choice, a literal stored restart prompt,
  append-only intake provenance, and stable ranked want-to-see ids with closure
  criteria. Its current local address also supplied a real successful check of
  the new single-command session-id comparison; that check does not claim
  provider resumability by itself.
- **Trace: continuous migration/restart** — a resumable legacy advisor lacks
  metadata but has usable notes and document state. The worker first asks that
  advisor for scope, progress assessment, and ranked wants, repairs in place,
  and retains the incumbent. An unresumable successor preserves logical id,
  folds contiguous debt, fences and increments the generation, loads the
  durable bundle with the literal restart prompt, and publishes its address
  only after validating the binding. Schema age alone never destroys context.
- **Trace: exact retry and double worker** — the same intake id/revision,
  packet digest, and semantic watermark returns the cached memo. A retry from a
  later completed successor is harmless; only live ownership evidence raises a
  double-agent concern. A changed digest under the same revision is reconciled
  or deliberately revised rather than being mistaken for the prior packet.
- **Trace catch: repaired handoff changed its hash** — the first draft left a
  pending intake line in place after advisor-recommended edits. Those edits
  changed the file digest, so the next worker would see a conflicting retry.
  The final contract transitions the line to `Advisor intake completed`,
  recording the reviewed pre-repair digest and memo; another review requires a
  deliberate new revision. A crash before this transition remains safe because
  an exact retry returns the cached memo.
- **Trace: advice authority** — a verifiable need-to-know omission inside the
  authorized scope is accepted as a repair; a non-contradictory adjacent fact
  is accepted with calibrated confidence; attached next work stays advisory;
  and a material contradiction or rescope is marked tentative and sent to the
  user without blocking unrelated safe work. The advisor cannot widen worker
  authorization by describing the broader program.
- **Trace: interaction close** — continuous policy receives a conclude message,
  folds documents/transcript/intake, updates progress and wants, returns a
  verifiable receipt, releases ownership, and remains resumable. Fresh-per-
  consult additionally fences the generation and removes the local incumbent
  projection after receipt verification. A hung advisor gets resume/close
  recovery first; a worker may fold only verifiable contiguous material and
  cannot invent assessment or close an unproven want.
- **Status** — user-approved and trace-simulated; behavioral benefit remains
  `assumed`. The PII advisor migration is the first intended live reboot test.

## 2026-08-12 — advisor guards become advisory evidence, not gates

- **User correction** — the first logical-continuity contract overfit the
  “only get advice once” goal into an exact `(intake id, fingerprint, semantic
  watermark)` transaction. It required pending/completed handoff transitions
  and treated a changed digest under one intake revision as conflicting input.
  The user judged that a continuous advisor remembering previous starts is
  enough to raise possible redundancy, and explicitly prioritized useful
  imperfect compliance over refusal caused by imperfect guards.
- **Superseding decision** — the stable intake id is now a continuity cue, not
  a one-shot gate. A matching fingerprint encourages a cached recap; changed
  handoff or program state gets a stated fresh/delta response. Fingerprints,
  watermarks, receipts, and optional provenance diagnose what happened but do
  not suppress advice or demand revision ceremony. The worker need not mutate
  the handoff through a pending/completed state machine.
- **Residual hard boundary** — an uncertain or competing lifecycle generation
  still cannot safely write/merge continuity state automatically. It can
  inspect and advise read-only with explicit uncertainty, naming the competing
  state and giving the user a select/fence/proceed path. Thus even the write
  guard cannot end only in refusal.
- **Trace: modified handoff** — worker B presents the same intake id after
  worker A or the user edited the handoff. The advisor says it saw the prior
  attempt, identifies the meaningful delta if any, and recaps or refreshes its
  advice. It neither rejects the packet nor requires a new revision id.
- **Trace: imperfect ledger/receipt** — a digest is unavailable or closure
  updates notes but misses an optional intake field. The advisor records
  `unavailable` or returns a partial-closure receipt, preserves remaining debt,
  and still supplies useful advice plus recovery choices. No optional
  bookkeeping condition becomes a user-attention dead end.
- **Cost model** — keep cheap identity/generation projection, one Bash session-
  id check, stable intake id, and visible provenance. Additional integrity
  evidence earns its execution and prompt cost only by helping diagnose a
  concrete mismatch; it is not correctness theater required before advising.

## 2026-08-12 — separate broker and provider advisor identities

- **Live catch** — the PII advisor migration exposed two valid identifiers:
  YA's canonical public session id, used in URLs and worker-facing continuity,
  and a distinct Codex provider resume id visible in the serving transcript.
  Calling either one the sole "canonical resumable id" made a locally correct
  check capable of validating the wrong surface.
- **Decision** — `session.local.md` records both when they differ. Handoffs and
  the one-command check use the broker's canonical public id; provider-native
  handles remain transport detail in the address. An unbrokered provider may
  use the same value for both. Missing provider evidence remains explicit and
  does not suppress read-only advice.
- **Cost/trace** — this adds one local metadata line only when useful. A worker
  resumes the YA URL from the handoff while the advisor or recovery path can
  still reach the Codex incarnation. A stale or missing backend handle lowers
  resumability confidence and offers recovery choices; it does not invalidate
  the public session or turn the identity check into an advice gate.

## 2026-08-12 — canonical advisor id is the harness resume id

- **User correction** — YA session URLs already end in the durable harness
  resume id. The prior entry's generic phrase "broker public id" was too loose:
  a public alias is not automatically canonical, and another backend may defer
  canonical-id or redirect support for implementation reasons.
- **Superseding decision** — handoffs and `Session ID` use the canonical
  durable harness resume id. `session.local.md` separately records the public
  URL/address and any provider-native handle. When canonicalization is not yet
  implemented, preserve the address and state that the id is unavailable; do
  not guess or block useful advice.

## 2026-08-12 — persistent advisors still close consultations

- **User requirement** — ending one consultation must be visible and timestamped
  even when the serving session deliberately remains persistent.
- **Decision/cost** — `session.local.md` gains consultation state and end-time
  fields and is written last at close. `closed-idle` preserves the incumbent;
  `partial-idle` preserves named debt. The file's mtime, or the latest mtime
  among advisor files covered by the receipt, is sufficient cheap timestamp
  evidence; no separate transaction log or forced session termination is
  required.

## 2026-08-12 — advisor interactions carry a return address

- **User requirement** — use one simple origin prefix at interaction open and
  a matching sign-off, not the repeated harness boilerplate that warns
  subagent messages cannot carry user authorization.
- **Decision/cost** — the envelope records requester harness, canonical durable
  session id, and interaction id once; later turns inherit it. Sign-off closes
  the interaction while leaving a persistent advisor resumable, and preserves
  an address for a labeled material correction or emergency. The two short
  lines are provenance only: no authentication or authorization inference.

## 2026-08-12 — advisor standing is not supervisory authority

- **User observation** — a PII worker appeared unusually deferential to its
  advisor. The advisor's criticisms may have deserved acceptance because their
  factual flaws were verifiable, but the advisor was never intended to impose
  hard task requirements merely through objections or ranked requests.
- **Decision** — validated metadata/charter is sufficient user-transitive
  standing for consultation and advisor-owned state maintenance. It does not
  require signed authorization and does not make the advisor a supervisor.
  Want-to-sees normally state evidence needed for the advisor's confidence;
  only a cited user/governing artifact turns one into a worker gate.
- **Compression** — replace per-turn ritual with four questions only at a
  material boundary: evidence, fact-versus-advice, conflict with governing
  state, and clarification-versus-new-gate/rescope. Apply the evidence side
  symmetrically to worker and advisor; keep authority anchored in the user and
  governing artifacts.

## 2026-08-12 — working-agent envelope scopes advisor skepticism

- **User direction** — advisor interactions opened by an object worker carry a
  one-time `[from working-agent <harness> <session>; interaction <id>]` and a
  matching sign-off. The tag tells the advisor that goal/result/intent
  interpretations may have self-reinforced and warrant explicit skepticism;
  it also leaves a return address for a post-sign-off emergency notification.
- **Correction while drafting** — do not extend that skepticism to routine
  factual updates such as “the user has since said X instead.” Those receive
  ordinary/default skepticism and are normally accepted. The source session
  makes transcript verification possible when an actual material conflict
  independently calls for the usual cheap check; it does not impose a proof
  burden or introduce signed-message paranoia.

## 2026-08-12 — advisor requester origins remain serial

- **User direction** — serial consultation is the expected case. A surprising
  second entrant should not be silently merged with the open requester; the
  advisor names its confusion and asks the entrant for its own origin prefix,
  while retaining safe provisional usefulness.
- **Stale close** — on the next advisor activation, an interaction inactive for
  more than 24 hours without sign-off receives an explicit advisor-authored
  synthetic sign-off. The intake ledger labels it synthetic rather than
  forging requester provenance, and a later return starts a new envelope.

## 2026-08-12 — interaction ids are best-effort serials

- **User decision** — advisors honor the interaction serial by default, while
  making no absolute uniqueness or monotonicity claim. A requester should not
  intentionally assign one id to two distinct interactions within 24 hours.
- **Failure handling** — reuse inside the window presumptively means
  continuation/retry. Origin, timestamp, digest, and intake history can expose
  ambiguity; the advisor asks for clarification and still gives safe useful
  advice instead of rejecting the interaction.
- **No purposeful-reuse exception yet** — after real or synthetic sign-off,
  “one more thing” receives a new interaction id. It may refer to the earlier
  context naturally; no special link field or syntax is required.

## 2026-08-12 — advisor brackets delimit a multi-turn interaction

- **User clarification** — opening and sign-off brackets are not an atomic-turn
  wrapper. They may share one requester turn or appear on different requester
  turns; every requester/advisor back-and-forth turn between them inherits the
  open interaction id.
- **Trace** — a one-question consult carries both brackets and closes normally.
  A rebuttal exchange opens on turn one, continues without repeated prefixes,
  and signs off on turn four. A signed-off “one more thing” still starts a new
  id, while an unsigned interaction inactive for more than 24 hours retains the
  existing synthetic-close rule.

## 2026-08-12 — advisor remembers accidental peer resurrection

- **User direction** — in a metadata-governed program, the advisor may notice
  an accidental second session with similar responsibility, including one
  revived by a YA heartbeat. It should tell the second about the established
  first session, retain the false start's harness/session id and provider log
  location, and disclose that record to the incumbent at its next consultation
  rather than interrupting it solely for bookkeeping.
- **Boundary** — this is supplemental to ordinary `agentctl active` and lease
  conflict awareness. It does not authorize silent state merging, fencing, or
  treating advisor inference as a live resource lock. A companion `agentctl`
  sketch keeps foreign-worker activity machine-scoped and ultimately qualifies
  each host with its claimed paths/resources; a whole-host wildcard is only a
  possible coarse first stage.
- **Trace** — a heartbeat resurrects worker B while worker A still owns the
  program. The advisor identifies A to B and records B's canonical session id
  plus JSONL location. A is not disturbed; at its next consultation it receives
  the record and can inspect whether B changed remote state. If no live overlap
  evidence exists, the advisor records uncertainty and supplies no fence.
- **Trace: legitimate parallel work** — two workers share a broad program name
  but their live item/path claims are disjoint, or metadata does not establish
  which is accidental. The advisor does not manufacture an incumbent/false-
  start ordering; ordinary scope coordination continues.
- **Trace: unreachable remote** — a fleet query cannot reach one AWS worker.
  Its machine-local state reports `unknown`, so neither `agentctl` nor the
  advisor treats the resource as clear. A previously observed false start may
  still be disclosed later as continuity evidence, without becoming a live
  lock claim.

## 2026-08-12 — every advisor sign-off checkpoints affected state

- **User correction** — full closure was keyed only to the prose command
  `Conclude advisor interaction ...`; a bare bracketed sign-off merely closed
  the requester side. Sign-off itself must trigger a continuity checkpoint.
  Per-turn state rewrites would be premature and distracting, though an advisor
  may checkpoint early when a meaningful milestone warrants it.
- **Decision** — after answering the final requester turn, every real or
  synthetic sign-off updates intake/fold/closure state and reconciles every
  notes, document, or metadata artifact the interaction actually made stale.
  Unaffected files need not be rewritten. Failure to finish safely yields a
  `partial-idle` projection and partial closure receipt rather than a false
  clean close.
- **Trace** — a one-turn read-only question carries both brackets and changes no
  program assessment: intake/fold and `session.local.md` still close, while
  metadata and document state remain untouched. A four-turn exchange changes a
  ranked want-to-see: sign-off reconciles notes, intake, fold watermark, and the
  final projection. A collision prevents safe notes replacement: sign-off
  records the completed pieces and returns `partial-idle` with the named debt.

## 2026-08-12 — advisor interaction grain and explicit shutdown

- **User refinement** — a consultation covers one coherent bundle of results,
  claims, or decisions that a worker has chosen to submit for consideration,
  not mechanically each atomic result. Its clarification, rebuttal, and related
  evidence may span several turns before one sign-off.
- **Lifecycle split** — routine sign-off runs the mandatory affected-state
  checkpoint and retains a continuous incumbent. The exact rare directive
  `Shutdown advisor` instead retires the serving incarnation before an
  intentionally fresh boot: save and validate the full reboot bundle, mark the
  current generation `no-incumbent`, remove its current-session projection, and
  let the successor increment the generation. A working agent needs explicit
  user or metadata-policy authority; the user may issue it directly.
- **Trace: evolving bundle** — a worker submits a result table, answers two
  advisor questions, and supplies one correcting row. All remain one
  interaction; only the final requester turn signs off, then the advisor
  checkpoints affected state and remains the incumbent.
- **Trace: later distinct bundle** — the same worker later submits a new model
  comparison. It opens a new interaction id rather than silently extending the
  closed consultation; the earlier compact assessment remains context.
- **Trace: intentional fresh advisor** — the user sends `Shutdown advisor`.
  The incumbent folds all available debt, validates metadata/notes/docs/intake,
  marks `no-incumbent`, records its receipt, and removes `session.local.md`.
  A heartbeat resurrection cannot write; a fresh boot advances the generation.
- **Trace: partial save** — notes replacement collides during shutdown. The
  advisor retains its incumbent projection and returns `shutdown incomplete`
  with debt, so no worker mistakes a partly saved state for restart-ready.
- **Trace: post-fence cleanup failure** — final metadata replacement succeeds
  but removing `session.local.md` fails. The old generation remains fenced,
  returns `shutdown incomplete`, and names the stale projection for recovery;
  it never reactivates metadata merely to make the transaction look atomic.

## 2026-08-12 — advisor learns working documents and live handoffs

- **User requirement** — an advisor-governed working session consults the
  advisor when it introduces new working documents. Starting a new live
  handoff scope is also communicated, but handoffs are a distinct class rather
  than another working/followed document.
- **Timing rationale** — notification does not fire on file creation, first
  touch, or first line. It fires once the intended v1 or later topology change
  is coherent: prompt delivery can earn useful role/scope feedback while edits
  are cheap, and the hard latest boundary before session end/transfer prevents
  forgetting. Brief deferral and bundling remain allowed.
- **Decision** — packet topology now has three independent fields: working-
  document changes, live-handoff changes, and followed-document changes. The
  first informs and lets the advisor decide whether future deltas matter; the
  second updates a repeatable metadata scope/path registry; only the third
  changes `docs/state.md`. A topology-only notification is a `tell`.
- **Trace: new evolving plan** — a worker completes the intended v1 of a
  human-readable research plan that will govern several result decisions. It
  tells the advisor of the path and role; the advisor elects to add it to the
  followed set. Starting the file did not prematurely interrupt drafting.
- **Trace: one-off evidence** — a worker emits a static adjudication receipt.
  It reports the artifact as evidence, not a working-document topology change,
  and the advisor does not grow its followed set.
- **Trace: new live handoff** — a large session completes a private handoff for
  a named scope. The worker tells the advisor; metadata records scope/path,
  while `docs/state.md` stays unchanged. A separate followed-document change is
  needed if the advisor should track its contents, as the PII advisor
  deliberately did.
- **Trace: no handoff** — a small session has no handoff. Advisor consultation
  proceeds with `Live-handoff changes: none`; no file or metadata entry is
  invented merely to satisfy the protocol.
- **Trace: rename and retirement** — a handoff moves or ceases to govern work.
  The worker reports the completed old/new scope/path or retirement before
  ending; the advisor replaces/removes the metadata entry without interpreting
  it as program rescope or editing the handoff.

## 2026-08-12 — compiled boot as an advisor compaction boundary

- **Dormant sketch** — a long-running advisor is a strong candidate for the
  proposed compiled-AGENTS facility because exact charter, scope,
  authorization/epistemic stance, and restart policy should survive repeated
  compaction. The authoritative sources remain metadata and charter files; the
  compiled profile is a generated, input-hashed snapshot rather than another
  policy owner.
- **Trace: ordinary progress** — a new result changes program assessment,
  ranked want-to-sees, intake history, or the document cursor. The advisor
  checkpoints its continuity bundle and continues in the same serving session;
  recompiling policy or restarting would spend context for no semantic gain.
- **Trace: material scope change** — the declared program scope or charter
  policy changes enough that the old protected boot would steer differently.
  Its manifest becomes stale; the program is advised to recompile and perform
  a generation-fenced succession from the validated continuity bundle. Minor
  clarification does not force churn. This is not binding until the compiler
  and cross-compaction behavior exist and are tested.

## 2026-08-12 — first end-to-end advisor close and raw YA dispatch

- **Observed interaction** — worker session
  `019ff3b5-da27-7fd0-9ffc-08ee9d6c0d47` submitted one 298-word Korean/R2
  bundle with a sign-off envelope to incumbent advisor session
  `019febc7-07f8-7162-8306-d699ff33508f`. The advisor returned a substantive
  correction, installed and committed its durable state, projected
  `closed-idle`, and supplied a receipt that the worker verified.
- **Local HTTP boundary worked fail-closed** — the worker's first raw POST at
  04:23:27Z omitted YA's required local-write header and returned `Missing
  required header`; the advisor transcript shows no turn start from it. The
  worker searched the installed YA distribution for that exact error, resent
  the unchanged packet at 04:23:44Z with `X-Yep-Anywhere: true`, and the
  advisor task began at 04:23:45Z. Transport failure therefore neither opened
  an intake nor duplicated the interaction.
- **Unexpected control-path capability** — the worker did not operate YA's
  JavaScript UI. It inferred `/api/sessions/<id>/messages` directly from the YA
  URL/session id, used `curl`, and polled `/api/sessions/<id>/process` until
  completion. No first-class agent session-control tool was present. Ambient
  YA vocabulary from the global instruction corpus is the best current
  explanation for the direct guess, but the trace does not prove that causal
  source. It does disprove the prior expectation that an agent was unlikely to
  turn a YA URL into effective session control.
- **Elapsed-time calibration** — the delivered advisor turn ran from
  04:23:45Z to 04:40:03Z (16m18s). Compaction occurred at 04:37:29Z, after
  13m44s, leaving about 2m33s afterward. The total includes charter/protocol
  reload, recovery of roughly 1,100 lines of compact notes, followed-document
  and handoff drift reconciliation, direct Korean/R2 evidence inspection, a
  substantive estimand/decision-rule correction, state checkpointing, and a
  commit. It is evidence that this close was nontrivial, not that the close
  protocol itself intrinsically costs 16 minutes. Unknown starting proximity
  to compaction prevents attributing even the post-compaction delay cleanly.
- **Continuity stress result** — notes were atomically installed and intake
  closure was being recorded before compaction. After reconstruction, the
  advisor reread current policy/ownership/state, completed the transport
  projection and verification, committed the durable bundle, and returned the
  receipt. Logical continuity survived a mid-close compaction; whether a
  warmed, no-drift close is lightweight remains unmeasured.

## 2026-08-12 — candidate designs leave routine guidance

- **User requirement** — topic documents that agents read for current
  governance or guidance should not mix in dormant sketches. Use an adjacent
  `topicname.sketches.md` companion, with a short pointer from the decision
  surface when discoverability matters.
- **Routing decision** — `.sketches.md` joins the unloaded companion vocabulary.
  It is read when exploring future work, reconsidering a named candidate, or
  explicitly asked about sketches; presence alone does not activate guidance.
  Promotion means moving the binding contract into the main topic or an
  implementation plan.
- **Migration trace** — the six guidance topics with explicit sketch sections
  (`agentctl`, `almanac`, `glossary`, `handoffs`,
  `user-authorization-attestation`, and `web-digest`) retain current contracts
  in their main files and move candidate bodies into adjacent companions.
  Glossary regeneration and web-digest routing exclude the new suffix so it is
  neither indexed as an independent topic nor loaded into routine web context.

## 2026-08-12 — evidence-first paper drafting and advisor review

- **User-defined workflow** — a research program first keeps competing,
  strength-ranked publication cases in `paper-proposals.md`; developed cases
  may split into taxonomy-named cards, and a selected case promotes to a
  working draft while its proposal freezes as the candid selection record.
  The form is chosen only after assessing effect size, uncertainty, matched
  simple-practitioner baselines, cost, public-data, scenario, and model-access
  scope. Manuscript mechanics remain an explicitly untested sketch.
- **Advisor routing** — paper proposal, draft, handout, and progress-report
  checks are artifact-conditioned capabilities of a full research advisor, not
  reduced advisor types. The program advisor is the default. An explicitly
  requested draft-scoped advisor still loads the standard charter and durable
  startup bundle, uses a manually selected followed set, and owns separate
  state at the already-defined paper path. Paper-work handoffs identify every
  advisor on which they rely.
- **Trace: weak result** — an intervention has a promising point estimate but
  no uncertainty estimate and has not faced the best cheap public-data
  baseline. Literal application marks the headline case unsupported and
  redirects attention to an empirical audit, failure atlas, or `credible-if`
  proposal. It does not manufacture significance by changing the story.
- **Trace: real advance** — a stable, practically material gain beats the
  matched practitioner baseline in the named cost and access regime. The same
  evidence-ceiling rule permits a headline-result proposal; it does not force
  every program into a defensive audit form.
- **Trace: promotion** — one candidate accumulates a substantial skeleton and
  becomes selected. Its full card moves out of the comparative index, then
  freezes and links to the new working draft. The proposal remains the
  selection rationale while the draft becomes the sole evolving narrative.
- **Trace: advisor scope** — an ordinary paper-review request reaches the
  program advisor with its full prior context. A user-requested draft-only
  advisor receives the same standard competence plus its manually chosen
  program evidence, without writing the program advisor's bundle or requiring
  another directory convention. A narrow copyedit may disclaim a full evidence
  audit, while still surfacing a materially misleading claim it encounters.
- **Trace: cold-reader artifacts** — a third progress handout is mostly a run
  chronology with internal checkpoint names and unlabeled tables. The
  handout/progress rules reorganize it around the current claim and decision,
  link the glossary, define first-use jargon, and make tables self-decoding.
  Merely prepending an executive summary fails; a mutable handout may be
  rewritten, while a disseminated dated progress report remains frozen.
- **Trace: attraction signal** — a representative privacy failure or actual
  released label set may communicate the supported contribution directly. A
  charged “safety” label that could imply a broader guarantee receives a short
  footnote naming the mismatch. An evocative crime example unrepresentative of
  the measured population is removed rather than rescued by a disclaimer.
- **Status** — user-specified and trace-simulated; behavioral usefulness and
  the manuscript mechanics remain unmeasured.

## 2026-08-12 — shared technical writing and reconciled progress reports

- **User-defined split** — `technical-writing` owns the shared cold-reader,
  whole-document synthesis, terminology, evidence separation, self-decoding
  display, inline-example, and scan-only contracts. `handout-writing` keeps a
  mutable decision snapshot; `progress-report` keeps a frozen delta stream;
  `paper-writing` keeps the form-led durable argument after `paper-drafting`
  selects a publication case. Handouts and progress reports point to paper
  writing when they preview a publication claim.
- **Progress generation** — read the prior report, inventory every thread it
  left active/planned, inspect what was actually done since, and reconcile each
  promise. The new report begins with a first-contact `Refresher`; every prior
  thread gets a self-contained `Previously:` followed by exactly one useful
  shape: continuing `Now:` + `Planned:`, `Tabled because:`, or `Maybe next
  time:` with an honest revisit condition/timing and likelihood.
- **Trace: unattended prior promise** — no work happened on a previously
  planned experiment. The writer restates the full thread in `Previously:` and
  uses `Maybe next time:` with the actual revisit condition and weak intent. It
  does not pad the report with `Now: nothing` / `Planned: nothing` or silently
  drop the promise.
- **Trace: deliberate stop** — a prior active line loses on cost and baseline
  strength. `Tabled because:` records that decision and evidence; the generic
  pursue/hold/park recap may say park without forcing an empty future action.
- **Trace: real delta** — a thread gains a result that changes the plan. `Now:`
  presents the evidence, an effective self-describing table or representative
  input/output example appears inline, and `Planned:` names the next action and
  verdict. A final narrative/raw-results section may preserve fuller chronology
  and secondary displays without hiding the central illustration there.
- **Trace: third update, first attention** — a reader ignored two reports. The
  program-level refresher restores goal, baseline, vocabulary, and reader aids;
  each `Previously:` restates its whole thread rather than requiring the old
  report. The delta body remains chronological where useful without becoming a
  raw research log.
- **Trace: shared advice, distinct artifacts** — the common topic makes all
  three artifacts define terms and caption displays. The handout may throw away
  chronology, the report retains curated delta chronology after its refresher,
  and the paper follows its selected form and evidence spine. The shared base
  does not collapse their lifecycles or reader promises.
- **Status** — user-specified and trace-simulated; the first real generated
  report and paper will test whether the split and labels remain natural.

## 2026-08-12 — handouts use the paper rules at a lower proof bar

- **User-defined relationship** — a handout is essentially paper-governed, but
  its reviewers are curious and non-adversarial. It should be easy and
  enjoyable to comprehend, may explain what the program provisionally expects
  or believes it achieved, and is not rewarded for reproducing every rigorous
  detail. The main path carries claim status, decisive evidence, representative
  examples, and consequential limitations; links or stable handles signal the
  complete run/proof/ablation/raw-result trail.
- **Trace: extensive evidence exists** — twenty ablations and full per-example
  outputs support one result. The handout presents the principal comparison and
  one representative example inline, states the important limitation, and
  links the complete records. It neither hides that rigor nor makes a curious
  reader endure it before understanding the result.
- **Trace: aspirational update** — the program has a coherent promising route
  but no completed decisive experiment. The handout uses the paper-like form
  and examples to make the possible achievement legible, labels it provisional
  or speculative, and identifies the evidence that would settle it. The lower
  proof bar does not turn the aspiration into a finding.
- **Status** — user-specified and trace-simulated; actual reader response is
  unmeasured.

## 2026-08-12 — artifact selection and two-speed handouts

- **Selection contracts** — a serious paper selects a theme and form, then
  backfills evidence and legitimate interest-building work; a handout
  retrospectively represents what was done, with only a small prospective
  coordination layer; a progress report reconciles the prior promised
  frontier against work since; and a research blog selectively showcases one
  cool thing that worked. These artifacts share technical-writing rules but do
  not promise the same coverage.
- **User-defined handout audience** — the social presentation is two-speed.
  An interested reader should get a representative full picture from the
  handout as a whole. An uninvolved participant may only scan or join the
  discussion, but should leave with the flavor of the work and one concrete
  evidence-grounded insight: for example, which base model or technique won,
  what a table shows, or why a particular failure is puzzling.
- **Trace: rewarding is not positive** — a program has no successful method,
  but its outputs reject the obvious explanation and expose two plausible
  failure mechanisms. The handout leads with the failure table and examples,
  asks “why did this fail?”, and supplies enough evidence to discuss the live
  explanations. It does not invent a success story or bury the negative in an
  appendix.
- **Trace: selective opening, representative whole** — a mixed program leads
  with its most informative base-model comparison, then accounts for the other
  major bets, failures, current interpretation, and decisions by theme. The
  casual participant gets one memorable finding; the interested reader does
  not mistake a blog-like opening for a blog-like omission of the rest.
- **Status** — user-specified and trace-simulated; reader response and the
  research-blog cadence remain unmeasured.

## 2026-08-12 — privileged access must produce transferable yield

- **User observation** — readers are more likely to believe a paper contains
  otherwise unreachable findings when the authors had a compelling advantage
  the community cannot obtain. The legitimate reader gift is normally a
  transferable product of that advantage: anonymized user data, commissioned
  human labels, an evaluation set, aggregate findings, or another useful
  token, even when the source access itself cannot be shared. Industrial
  papers from YouTube and similar platforms are canonical examples.
- **Naming decision** — `privileged-access yield` names the separation between
  the inaccessible input and the knowledge or artifact transferred out of it.
  The glossary row is marked unconfirmed because the term is agent-proposed;
  the underlying distinction is user-specified.
- **Trace: useful asymmetry** — a model seller analyzes a proprietary
  deployment corpus, releases a privacy-reviewed evaluation set and labeling
  protocol, and reports which aggregate conclusions still depend on the full
  corpus. Readers receive an asset and a bounded finding they could not cheaply
  have generated themselves.
- **Trace: prestige without yield** — a paper repeatedly invokes private data
  and expensive frontier annotations but releases no derivative artifact,
  omits the measurement protocol, and gives outsiders no falsifier. The access
  claim increases mystique, not contribution; the attractiveness guidance
  requires a narrower claim and a candid boundary rather than awarding credit
  for scarcity alone.
- **Trace: privacy-constrained release** — row-level data cannot be shared, but
  aggregate strata, sanitized examples, annotation instructions, uncertainty,
  and a reproducible public-data comparison can be. The paper states both the
  transferable layer and the residual trust boundary instead of calling the
  work fully reproducible or fully closed.
- **Status** — user-specified distinction and trace simulation; the proposed
  term and its effect on reader judgment are unmeasured.

## 2026-08-12 — advisor delivery uses the generic session-turn boundary

- **Trigger** — user directed implementation of the generic advisor-
  communication helper, required live tests after a full YA provider-host
  restart, and required waiting for concurrent advisor-governance work to
  clear before mandating the helper. A first native fallback inherited the
  launching worker's `AGENTCTL_SESSION_ID` and temporarily overwrote its
  active-session banner, establishing that direct provider resume is not a
  safe advisor transport boundary by default.
- **Decision** — `research-advisor.md` now requires `session-turn` for every
  delivered advisor turn. The trigger-loaded protocol maps the durable
  `session.local.md` identities into the generic transport and keeps advisor
  envelopes, leases, and epistemic evaluation outside the helper. YA HTTP,
  direct provider resume, worker stdin, and transcript watching are not
  parallel fallback paths. Submission ids remain per-provider-turn receipt
  identities rather than being conflated with multi-turn advisor interaction
  ids.
- **Trace: hosted incumbent** — a verified idle advisor has a matching YA
  worker. Literal use reaches that worker's queue, emits acceptance before
  provider events, and returns one terminal receipt without a second resume.
  Disposable live Claude and Codex incumbents both passed this trace after the
  host restart. A separate headless host with no registered Hono generation
  also resumed disposable Codex, completed a turn, persisted its receipt, and
  shut down its owned runtime cleanly.
- **Trace: no incumbent** — the host records no acceptance, so the helper
  warns and resumes natively. The child receives the target YA identity when
  supplied, otherwise the durable provider id, plus the target harness; caller
  provider ids, YA's Bash identity bridge/wake capability, and launch-depth/
  model markers are removed. Live native Claude and Codex smokes returned the
  target session ids; the isolated regression test would fail under the
  reported caller-banner leak or a distinct YA/provider identity mix-up.
- **Trace: ambiguous post-acceptance disconnect** — the helper receives host
  acceptance and then loses the stream. Exit 12 plus the exact receipt lookup
  prevents a direct/native retry from duplicating the advisor turn. A stored
  terminal status can still recover completion. Both branches are covered by
  public-interface socket tests.
- **Trace: unsupported address** — an advisor records an unsupported harness
  or unavailable canonical id. The mandate does not encourage guessing or a
  raw transport bypass: it retains the existing `UNDELIVERED` packet path and
  forbids a fabricated advisor response.
- **Status** — fifteen isolated behavior tests and five disposable live
  harness/transport smokes pass. The transport invariants are observed; the
  effect of the advisor mandate on future agent choice remains `assumed`.

## 2026-08-12 — research citations and one-source web/print documents

- **User direction** — citation guidance belongs in a research-writing layer
  that inherits technical writing. Papers and research blogs repeat their own
  density calibration: the closest competitors/alternatives and the true
  influential/inspirational parents are always present, while a venue's
  cite-heavy custom is not a bibliography quota. Prior-art work explicitly
  routes through the shared field and frontier survey maps. Documentation may
  use the same provenance principle without inheriting paper-shaped density.
- **Tool choice** — Quarto is the default canonical source for mixed static
  web and printable research artifacts: official documentation covers Pandoc-
  based technical publishing, Observable JavaScript, cross-references,
  conditional output, blogs/GitHub Pages, and PDF/LaTeX. MyST is the alternative
  when semantic syntax-tree, JATS, or MECA export dominates. Observable
  Framework and Astro are web-heavy companion choices rather than manuscript
  sources. arXiv's current guidance supplies the source-package and clean-build
  boundary. This is researched descriptive guidance; the repo has not yet run
  an end-to-end paper through the stack.
- **Trace: cite-heavy field** — a paper has seventy related references but
  three genuinely close competitors. Literal application completely covers
  and distinguishes the three, cites its real parents and borrowed artifacts,
  and synthesizes the broader territory from the field map. It does not cite
  all seventy to mimic venue density, and cannot omit one of the three merely
  because the total bibliography is long.
- **Trace: lighter research blog** — a post's interactive visualization adapts
  two prior visual grammars and has one close alternative. Inline links are
  sufficient presentation, but all three sources remain named and the post
  attributes its dataset. The lighter surface does not erase provenance.
- **Trace: novelty from recall** — an author remembers no prior use of a task
  variation. The research-writing route sends the claim through the shared
  survey, grounded frontier map, and falsification search before “new problem”
  prose becomes a novelty claim. Recall alone may still seed a speculative
  proposal, not a vetted absence statement.
- **Trace: strict venue template** — a venue requires manual TeX macro work
  that cannot be expressed as a repeatable Quarto template/filter. The one-
  source rule explicitly promotes the TeX tree, updates the source declaration,
  and makes the old `.qmd` derivative or archival. It forbids silently editing
  generated TeX while both files claim to be current.
- **Trace: ordinary dual output** — a paper needs a GitHub Pages companion and
  a conventional PDF. One `.qmd` remains canonical; HTML, PDF, and retained TeX
  are generated outputs. A requested TeX wording correction is made in the
  source or renderer template, not patched into the generated file.
- **Trace: skeleton relocation** — a selected proposal links to
  `papers/x.md`; the draft later gains references and interactive assets. The
  source moves to `papers/x/index.qmd`, and the proposal plus companion topic
  links change in the same edit. No stale editable `.md` remains at the old
  path.
- **Trace: semantic export** — a journal workflow makes JATS and MECA packages
  the principal contract. The selection table chooses MyST rather than forcing
  Quarto merely because it is the default. Conversely, a full reactive data
  explorer becomes an Observable Framework companion while the paper remains
  canonical in its manuscript renderer.
- **Trace: JavaScript failure** — an example browser fails to initialize on a
  static host. Its initial HTML still contains the author-written caption and
  central static view/example rows; the printable output uses the same data and
  default comparison. Interaction loss reduces exploration, not the paper's
  claim.
- **Trace: table enhancement** — a 50,000-row result browser offers sort,
  filter, paging, and download. Initial HTML includes summary statistics plus
  representative, boundary, and outlier rows, so a reader without JavaScript
  still sees why the result matters rather than an arbitrary first page.
- **Trace: fallback drift** — an interactive default filters to public-data
  systems while its static figure includes private-data systems. The required
  comparison check fails: the author must align data/defaults or explicitly
  caption two different claims before release.
- **Status** — user-specified and trace-simulated; renderer selection is
  grounded in current official documentation but locally unexercised.

## 2026-08-12 — Markdown-to-venue-TeX support boundary

- **Correction trigger** — the initial document-writing recommendation
  established that Quarto and MyST can be customized, but did not answer the
  narrower question of whether a maintained named ACL/NAACL/ICML adapter
  already exists. The user distinguished “why would the feature not exist?”
  from a request to fork Quarto, added print-only Markdown-to-LaTeX refinement
  workflows to scope, then asked to pause the catalog investigation and retain
  the unfinished comparison as a gap.
- **Grounded snapshot** — Quarto's official extension system can package
  LaTeX classes, template partials, and paired HTML/PDF formats. MyST can emit a
  self-contained TeX tree and accepts catalog, URL, or local templates. Pandoc
  exposes direct HTML/LaTeX templates and filters; rticles packages a catalog
  of publisher-oriented R Markdown formats. The current Quarto journal
  listing, MyST template catalog, and rticles format list inspected in this
  pass did not name ACL, NAACL, or ICML. This is a time-sensitive catalog
  observation, not proof that no isolated community repository exists.
- **Decision** — portable Markdown-plus, rather than a renderer brand, is the
  default early authority. Quarto remains the operational web-first default;
  MyST and direct Pandoc are explicit TeX-handoff candidates. Guidance now
  distinguishes venue endorsement, a cataloged adapter, a community adapter,
  a local adapter, and generic TeX output. If repeatable adaptation becomes
  brittle, a recorded one-way cutover makes an ordinary LaTeX tree canonical;
  the Markdown source freezes or becomes explicitly derivative.
- **Trace: extension mistaken for support** — an author finds a generic
  `template:` option and the venue's official `.sty`. Literal application does
  not label the combination supported. It records a local adapter and audits
  review/camera-ready modes, front matter, bibliography, floats, geometry,
  mandatory sections, and package restrictions against the current call.
- **Trace: late hard migration** — a nearly complete Markdown manuscript needs
  direct float and macro surgery. The author pins the last Markdown revision,
  produces a self-contained compiling tree, records `paper.tex` as canonical,
  and stops regenerating over it. The old source cannot silently remain a
  second authoritative manuscript.
- **Trace: print-first refinement** — a paper expects a strict venue class but
  benefits from Markdown during exploration. Direct Pandoc or MyST emits and
  exposes TeX throughout drafting; the team may cut over after the skeleton,
  after stable results, or at final formatting. The exact timing is a paper
  decision, while the one-authority invariant remains fixed.
- **Trace: LaTeX-first web companion** — the official class is canonical from
  an early cutover. lwarp or make4ht derives HTML, but the author audits that
  output and supplies static fallbacks; successful PDF compilation does not
  imply a usable browser artifact.
- **Status** — instruction change is grounded in official project and venue
  documentation and trace-simulated. The comparative build remains unexercised
  and is recorded in `gaps/document-authoring-toolchain-bakeoff.md`.

## 2026-08-12 — Quarto figure vocabulary and reproducible plot generation

- **Trigger** — the shared handout rules encouraged a visual spine and the
  document-writing topics selected Quarto, but neither told an authoring agent
  which requests fit Quarto-native Markdown, which require an external plot,
  or how the outputs stay aligned across HTML and PDF. The only concrete plot
  contract was Pareto-specific. A PII handout request for overall plus nine
  language sweep curves would otherwise force the next agent to research the
  stack during authorship or improvise ten unrelated images.
- **Decision** — `document-writing-figures` now owns the selection ladder:
  Markdown tables and figures, Quarto panels, Mermaid, and Graphviz for their
  native information shapes; a committed Matplotlib generator as the default
  Python path for measured-data figures; ggplot2, Altair/`vl-convert`, OJS,
  Plotly, and PGFPlots as bounded alternatives. Quantitative generators emit
  same-stem SVG and PDF, and Quarto's extensionless image syntax selects SVG
  for HTML and PDF for LaTeX. A project `pre-render` script makes regeneration
  explicit, while external-data figures avoid an unexamined `freeze: auto`.
- **Trace: ten sweep panels** — literal application validates one tidy dataset,
  then produces a coordinated 2-by-5 small-multiple figure with overall first,
  one shared scale and legend, observed-point markers, measured peak summaries,
  and crossings interpolated only across an adjacent sign change. A narrow
  venue may move overall above a 3-by-3 language grid without changing scales.
  Ten independently autoscaled sparklines fail because they hide comparative
  magnitude and surrender shared annotation/legend ownership.
- **Trace: exact values** — a six-row comparison whose purpose is lookup stays
  a captioned Markdown table. The rule does not force a chart for visual
  variety. Conversely, a crossing claim gets a curve even if its sampled
  values also appear in a compact summary table.
- **Trace: process and interaction** — a simple evaluation pipeline becomes a
  Mermaid cell rather than a plotting dependency. A browser language selector
  uses local-data OJS/Observable Plot only after the same-data static view
  exists; JavaScript loss therefore removes exploration without removing the
  claim.
- **Trace: stale external input** — run data change while `index.qmd` does not.
  A pre-render generator refreshes or fails, while a blindly frozen executable
  cell could retain the old claim-bearing output. The rule names that failure
  without banning freeze for a deliberately cached portable site.
- **Trace: R-native program** — the existing ggplot2 pipeline keeps its
  competent stack and emits explicit same-size SVG/PDF through `ggsave`; the
  Matplotlib default does not create a cross-language dependency merely to
  satisfy uniformity.
- **Status** — syntax and tool boundaries are grounded in current official
  Quarto, Matplotlib, Altair, ggplot2, and Plotly documentation and survived
  scenario traces. Quarto and the plotting packages are absent from this
  checkout's current environment, so the end-to-end dual render remains
  unexercised and is added to the existing document-toolchain bakeoff gap.
- **In-turn correction** — the first decision wording overgeneralizes the
  external generator as the default for every measured-data figure. The final
  contract permits a simple one-document claim-bearing plot to remain a
  committed executable cell whose HTML and PDF renders are audited. Promotion
  is the default for custom annotations, coordinated panels, reuse, independent
  regression checks, or likely LaTeX cutover—the properties the PII sweep has.

## 2026-08-12 — named visualization layouts and linked sketch gaps

- **User-designed pattern** — `main-and-breakout figure` names an asymmetric
  overview/detail composition: a reading-priority main panel on the left and a
  vertical stack of compact subgroup panels on the right, with main-above-grid
  as the narrow-print reflow. The PII instance keeps the overall weighted
  curve full-scale while language breakouts use visibly stated local ranges
  and outward right-side ticks. The term is provisional; the information
  structure, scale honesty, and reading priority are user-specified.
- **Registry decision** — result displays now have a separate named-template
  topic rather than accumulating as plotting-library recipes. It covers the
  main-and-breakout, shared-scale small multiples, annotated transcript
  contrast, representative-example gallery, distribution-and-exemplars,
  task–method–evidence teaser, and empirical-law grid. Foundational
  visualization guidance and inspected ML papers/blogs support the patterns as
  recurring forms; publication success does not establish a causal style
  effect.
- **Quarto probe** — a local Quarto 1.9.38 render verified that Markdown and
  figure-div captions remain real `figcaption` text; caption footnotes produce
  endnotes plus hover hooks; `fig-alt` reaches the image `alt`; the optional
  image title remains a distinct HTML attribute; cross-references, subfigures,
  and lightbox links retain their document semantics. This supports keeping
  title/caption/coda outside plot pixels while leaving axes, facet labels,
  mark annotations, and legends inside the generated asset.
- **Gap-routing decision** — a capability-gated `.sketches.md` links to a
  committed gap and the gap links back. Default granularity is one running gap
  per topic when capabilities must be evaluated together; contextualized
  per-capability gaps remain valid. No arbitrary `*.gaps.md` companion or
  routine scan is introduced, avoiding extra discovery cost and a second gap
  namespace.
- **Trace: ordinary dormant sketch** — a possible alternative with no current
  incompleteness stays only in `.sketches.md`; the linking rule does not mint a
  gap for every idea. A promised but missing interactive/print capability uses
  the topic's existing gap, preserving both discovery directions. Two
  independent missing capabilities may split only when each gap explains the
  shared purpose instead of becoming a context-free checkbox.
- **Status** — user-specified, grounded reconnaissance, and one local HTML
  render. The semantic interaction layer, document-to-figure style bridge,
  native qualitative component, and real venue PDF bakeoff remain unimplemented
  in `gaps/result-visualization-templates-research.md`.

## 2026-08-12 — committed vector assets and SVG viewport fidelity

- **User-ratified repository contract** — commit the generator, canonical
  evidence, and run provenance; commit SVG for HTML/chat/review and PDF for
  print/LaTeX when those vector outputs are compact. A raster-only consumer
  justifies producing a raster, not automatically retaining it: commit one
  only when neither a denser canonical representation nor a standard, reliable
  regeneration/conversion path from a smaller committed intermediate exists.
  The purpose is immediate reviewability plus exact regeneration, rather than
  treating generated outputs and provenance as alternatives.
- **Terminology refinement** — an SVG `viewBox` carries vector-coordinate
  bounds and coordinate-to-viewport mapping, not a CSS-pixel size. Absolute
  root width/height carry suggested display size; `preserveAspectRatio` carries
  the mapping policy. The shared viewer contract now preserves all three roles
  instead of compressing them into “natural pixels.”
- **Existing YA evidence** — `topics/media-rendering-and-routing.md` already
  defines and the client implements the requested default. SVG files render
  through inert `<img>` object URLs; declared dimensions govern actual size;
  viewBox-only files receive a definite container; object-fit preserves the
  aspect ratio; and Fit may enlarge vectors. `lib/vectorImageSizing.ts`,
  `ImageViewer.tsx`, and their tests establish the path. No duplicate YA gap or
  second implementation was added.
- **Trace: authored bounds** — a plot includes deliberate margin for endpoint
  labels. Literal application fits the declared viewBox and keeps that margin;
  an eager tight-bounds pass would clip or crowd the labels and therefore
  violates the contract. A viewBox-only Mermaid figure receives a container
  rather than disappearing at zero width. A script-bearing project SVG still
  renders through an inert surface; “direct” never licenses DOM inlining.
- **Status** — user-specified general contract with the YA instance verified
  against current documentation, implementation, and unit tests. Other HTML-
  style viewers remain an aspiration unless their own paths are inspected.

## 2026-08-12 — advisor title is presentation, not continuity

- **User correction** — a generation-2 advisor bring-up considered blocking
  continuity on a presentation-title mismatch. The user ruled this out:
  harnesses and YA may automatically retitle sessions, so the title is mutable
  presentation metadata. Violations are raised to the user and repaired; they
  never outweigh agreeing logical id, generation/state, ownership, and durable
  resume identity.
- **Provider evidence** — the checked-out Codex app-server contract exposes
  `thread/name/set`; `thread/read` returns `thread.name`, and upstream tests
  verify that a set name appears in read, list, and resume wire responses.
  That provider API, rather than an assumed SQLite column, is the correct
  verification surface. The YA-hosted and native-resume application timing is
  not yet unified.
- **Trace: automatic retitle** — advisor generation 2 resumes under the right
  durable id and exclusively owns the matching logical id/generation, but the
  harness replaces `Advisor — PII` with prompt-derived text. Literal use now
  reports expected versus observed, completes the consultation and continuity
  checkpoint, and leaves title repair debt. It neither starts generation 3 nor
  withholds advice.
- **Counter-trace: wrong identity** — the title matches, but the durable resume
  id or lifecycle generation does not. The title supplies no compensating
  evidence; conflicting continuity writes remain blocked under the existing
  identity/ownership rules.
- **Implementation boundary** — advisor-specific dispatch will eventually set
  and verify the required title after hosted/native resume begins. Generic
  `session-turn` continues to own transport selection and receipts only. The
  unfinished two-path convergence is recorded in
  `gaps/research-advisor-session-title-convergence.md`.

## 2026-08-12 — intervention ladders are reconstructed causal arguments

- **User feedback** — a PII publication sketch proposed starting from the most
  valuable discovered results, projecting backward to the ablations or
  hill-climb evidence that can credit specific techniques, repeating a compact
  benchmark summary at each stage, giving less-reproduced techniques full
  treatment, and compressing standard steps to reproduction-ready sketches.
  The intended work was first an agent-instruction refinement, then an
  application to the PII proposal—not merely a one-off rewrite of the proposal.
- **Form decision** — this is an intervention-ladder paper when the transferable
  gift is the chain of defect, credited fix, controlled delta, and residual.
  The strongest terminal result may supply a headline-result opening and the
  interventions may have recipe value without changing the governing form.
- **Trace: adaptive chronology** — three changes landed together before a large
  gain. The matrix exposes that no technique-level credit is identified; the
  writer must run an ablation, credit the bundle, or omit the rung. Merely
  arranging the changes into a plausible sequence fails the rule.
- **Trace: standard ingredient** — a common affine token-classifier projection
  is necessary but neither novel nor decision-changing. It receives a citation
  and short reproduction-ready sketch, while a less-reproduced teacher or data
  intervention with a controlled material delta receives the full rung. The
  form does not inflate every implementation choice into a contribution.
- **Trace: adjacent forms** — a bag of independently useful tricks becomes
  recipe synthesis; one decisive endpoint whose path teaches nothing remains a
  headline-result paper; successive measured residuals that determine the next
  intervention remain an intervention ladder. The boundary follows the reader
  promise rather than the chronology or the opening paragraph.
- **Trace: paper split** — two candidate stages share task, testbed, comparator,
  and repeated scorecard, so one ladder improves cumulative understanding. A
  diagnostic stage that needs a different estimand, related-work neighborhood,
  and reader promise becomes a separate paper rather than a second governing
  form hidden inside the ladder.
- **Status** — user-grounded and trace-simulated; usefulness will be tested by
  the accompanying PII proposal revision.

## 2026-08-12 — ladder scorecards need stable and causal references

- **Trace catch** — the first operational wording required one declared
  reference throughout the ladder. Applied literally to the PII case, every
  rung could report its delta against GLiNER2 while omitting the matched
  predecessor/control that identifies the rung's effect. The display would be
  comparable but the attribution would remain unsupported.
- **Repair** — carry the stable external reference for cumulative progress and
  also report the local matched contrast when it differs. The two serve
  separate claims: where the system has arrived and what the current
  intervention caused.
- **Counter-trace** — when the external baseline is also the immediate matched
  control, one comparison serves both roles; the rule does not duplicate it.

## 2026-08-12 — intervention-ladder motives may be reconstructed

- **User correction** — the earlier refinement made a useful narrative form too
  rigid and treated its thematic "why" as though every motivating defect needed
  advisor-grade causal proof. In real research, the choice may follow a cluster
  of worsening metrics, a preponderance-style hunch, or an undocumented
  speculative leap. A candid retrospective account of why one might try the
  intervention is allowed even when it is not the logged historical reason.
- **Epistemic split** — motivation, outcome, and attribution are different
  claims. Reconstructed motivation needs candid labeling and true inputs;
  measured improvement needs a fair result contrast; strong technique-level
  attribution needs an isolating contrast. Raising the last standard must not
  falsely raise the first into a causal estimand.
- **Structural decision** — pressure/intervention/evidence/residual is an
  optional full-scene template. Empty story beats are cut. The paper chooses one
  heading logic throughout: mechanism-indexed headings are the navigable
  default, while consistently thematic or motivational headings are an allowed
  variation. In the default, section bodies carry the thematic thread.
- **Trace: undocumented hunch** — several Arabic metrics deteriorate and the
  team tries locale-aware materialization without a logged diagnosis. The paper
  may say the pattern led the authors to suspect materialization errors, or
  retrospectively explain why that intervention was plausible. It may not say
  the defect was proved first or that this was certainly the contemporaneous
  reasoning.
- **Trace: isolated outcome** — the same section may credit the intervention
  when a matched on/off result isolates it. If the result bundles data and model
  changes, the looser narrative license does not create causal credit: the paper
  credits the bundle, marks the attribution unresolved, or supplies an ablation.
- **Trace: no useful transition** — one stage has a worthwhile controlled gain
  but no illuminating residual. Its mechanism-indexed section reports the
  motivation and evidence, then moves on. The form does not manufacture a
  defect-to-next-stage bridge merely to complete four slots.
- **Status** — directly user-specified and trace-simulated; the PII proposal is
  the first intended application.

## 2026-08-12 — challenge maps and attempt ledgers are ladder defaults

- **User specification** — a ladder should normally name its broad recurring
  challenges in advance, preferably in a glossary-like table, rather than open
  with a laundry-list paragraph or invent a new pressure for each intervention.
  Every challenge-bearing technique section should also have a corresponding
  appendix account of less-effective attempts and current guesses about why.
- **Form decision** — when pressures recur, the opening defaults to a compact
  challenge/meaning/response map and later sections refer back to it. Each
  challenge-bearing technique defaults to a technique-indexed appendix
  subsection containing attempt, observed outcome, explanation hypothesis, and
  evidence status.
- **Trace: shared scarcity** — four data interventions all respond primarily to
  scarce supervision. The introduction defines that challenge once; the four
  mechanism-indexed sections do not fabricate four distinct diagnoses merely to
  sound story-driven.
- **Trace: failed versus untried** — deeper heads lost in measured comparisons,
  while a multi-encoder representation has never run. The paired appendix lists
  the former as less-effective attempts with causal guesses marked as
  hypotheses, and the latter in an explicitly untried box. It does not turn an
  expectation into negative evidence.
- **Main-path boundary** — a failed attempt that changes the selected method's
  meaning, expense, scope, or validity remains in the main section. Routine
  search history moves to the appendix without being erased.
- **Status** — directly user-specified and instantiated in the PII proposal.

## 2026-08-12 — branched programs require a lineage-and-credit map

- **Live catch** — the first PII application grouped three useful intervention
  results under one v11 ladder. Saved lineage showed that low-dose MLM produced
  a separate v4 release, while v7 through v11 were controlled fresh starts from
  a common v3 parent rather than serial continuations. A technique could be
  present in the terminal substrate or strongly supported on a parallel branch
  without its measured delta being a cumulative v11 rung.
- **Form decision** — a branched program defaults to a lineage-and-credit map
  before ladder promotion. It classifies exact parents and checkpoints as
  terminal ancestors, common-parent contrasts, parallel branches, or method
  bridges and records each result's control, external comparison, claim ceiling,
  and manuscript role. Only verified ancestry receives combined or cumulative
  language. Valuable parallel evidence remains a labeled case study.
- **Trace: sibling dose search** — four releases each restart from one parent at
  different teacher doses. Their pairwise comparisons can select the terminal
  recipe and support a dose-response claim, but the paper may not draw the
  releases as weights accumulated in sequence. The common parent is visible.
- **Trace: terminal ingredient, parallel attribution** — translated data are in
  the terminal parent's mix, while their clean matched effect comes from another
  branch. The paper may say the terminal system uses translated data and cite
  the parallel replication as evidence for the bundle; it may not call that
  local delta the terminal checkpoint's cumulative gain.
- **Fallback** — if classification leaves too few genuine rungs, the same
  one-paper package becomes a headline-result paper with intervention case
  studies. This preserves the findings without inventing a staircase.
- **Status** — user-directed PII application plus saved-artifact lineage check;
  generalized and trace-simulated.

## 2026-08-12 — abstracts and resource accounting are cross-form paper defaults

- **User specification** — every paper begins with an abstract. An empirical
  paper may also carry a compute section estimating electricity use, actual AWS
  Spot expenditure, and the AWS Spot-equivalent value of local L40 use.
  Efficiency belongs in the abstract or introduction only when the achievement
  is strong relative to a fair critical-path energy or dollar denominator.
- **Accounting split** — terminal reproduction, the result's critical research
  path, and the full exploratory program are different scopes. Hardware-hours,
  elapsed time, power assumptions, energy, actual spend, and counterfactual
  local-compute value remain separate columns rather than being collapsed into
  one impressive-looking cost.
- **Trace: local L40 use** — a paper used twenty local L40 device-hours and paid
  no cloud bill. It reports zero actual AWS spend and a separately labeled Spot
  equivalent based on a named region, date, allocation rule, and nearest
  comparable instance; an L40S comparison names the hardware mismatch.
- **Trace: unmetered energy** — only device thermal design power and elapsed
  time survive. Their product may bound or estimate device energy with that
  basis stated, but the paper may not call it measured wall energy or infer
  carbon without a sourced electricity mix.
- **Trace: efficient headline** — a small run is not automatically an
  efficiency contribution. Abstract emphasis requires a fair quality/coverage
  comparison per critical-path kWh or dollar and states both numerator and
  denominator. Otherwise the resource table remains useful secondary context.
- **Status** — directly user-specified and trace-simulated; no empirical claim
  that resource disclosure improves paper outcomes.

## 2026-08-12 — very long documents use ordered source fragments

- **User specification** — fragment organization is a proposal for all writing
  expected to have great length, with one file per section, sequence-numbered
  names that make adjacency obvious, and preprocessor-like textual assembly.
  `document-writing` owns the rule because it already owns source authority and
  renderer mechanics.
- **Mechanism check** — Quarto's official `include` shortcode performs textual
  insertion. Its documentation requires the directive on its own line with
  blank lines around it, recommends underscore-prefixed fragment names so they
  are not rendered independently, and says relative references resolve from
  the including root rather than the fragment.
- **Trace: short note** — a five-page handout stays in one file; the expected-
  great-length trigger does not impose directory and include overhead on every
  document.
- **Trace: reordered long draft** — numeric names make neighboring sections
  easy to find, while the root include manifest remains authoritative. Reorder
  changes that manifest explicitly rather than relying on a glob whose lexical
  behavior silently becomes document structure.
- **Trace: scattered edits** — independent section passes improve local prose
  but duplicate one definition and contradict a limitation. The required
  whole-document gather review catches both before the root render; fragments
  do not waive global coherence.
- **Trace: second source of truth** — an assembled Markdown file is generated
  from fragments. It remains an output and is never hand-edited alongside
  them, preserving the existing one-editable-manuscript contract.
- **Status** — directly user-specified; Quarto mechanics verified against its
  current official documentation and scenario-traced, not yet exercised on a
  project paper here.

## 2026-08-12 — research advisors are critical-reader proxies, not approvers

- **User correction** — working agents had become overcompliant with advisor
  comments and spent real time seeking confirmation that the advisor accepted
  a rebuttal. The advisor sees monitored documents and immediately adjacent
  links; the user and working agent normally know the broader program better.
- **Role decision** — treat the advisor as a skeptical critical reviewer of
  that bounded reader surface. Its comments first test whether the documents
  can be made more truthful: repair an inconsistency, or explain why an
  expected alternative, control, or result is absent. Advice does not revise a
  user-laid plan without independent evidence or a governing artifact.
- **Trace: missing baseline** — the advisor asks why baseline X is absent, but
  the user already rejected it for an access mismatch. The worker adds that
  consequential reason to the paper and continues. It does not rerun X or ask
  the advisor to approve the explanation.
- **Trace: methodological error** — the advisor alleges that the reported
  interval uses the wrong resampling unit. The worker checks the scorer and
  saved artifact directly. A confirmed defect is corrected immediately; a
  false allegation leaves the result unchanged. If the memo does not identify
  the relevant table or wording, one locating question is allowed before the
  direct check.
- **Trace: plan pressure** — a want-to-see proposes a new expensive experiment
  outside the user's frozen plan. It remains evidence needed for the advisor's
  confidence, not a work gate. The worker records any useful evidence ceiling
  in the paper and proceeds under the user plan without a convergence round.
- **Persistence** — this skepticism/deference calibration is provisional by
  model generation. Reassess it at the first instruction-policy review after a
  major frontier-model generation rather than treating current advisor/worker
  tendencies as permanent.
- **Status** — directly user-specified and trace-simulated; time saved and
  decision quality remain unmeasured.

## 2026-08-13 — tracked runs admit only committed project source

- **User correction** — recording a Git SHA and a hash of an rsynced script did
  not establish reproducibility: the bytes could be dirty, absent from the
  named commit, or submitted from a remote snapshot with no Git objects. The
  desired default is tool-enforced at the common `agentctl` surface.
- **Rule** — a tracked launch requires a committed Git checkout, rejects
  tracked/index drift and all non-ignored untracked Python, and proves selected
  script and environment-control bytes recoverable from the recorded commit.
  A queued launch repeats the check after waiting and before executing the
  payload. `--no-aim` remains a deliberate trivial-run escape, not a research
  submission path.
- **Trace: clean local checkout** — the entry script and Pixi manifest+lock are
  committed and unchanged. Admission passes; state and the durable dump record
  commit, Git paths/blobs, byte hashes, and ordinary machine identity.
- **Trace: rsynced remote** — code bytes exist and have a SHA-256, but `.git`
  and the named commit are absent. Admission fails. The hash is printed as
  diagnostic identity where a selected file is off-commit, but never upgrades
  the run to reproducible.
- **Trace: source drift** — either a tracked file changes, an untracked `.py`
  appears, or `HEAD` advances while a job is queued. The initial or pre-payload
  check fails and the payload does not run.
- **Trace: named data** — an uncommitted dataset declared with `--input` is not
  treated as program source. Its data-provenance contract and optional input
  hash remain separate from the committed-code gate.
- **Trace: different worker** — OS/distro, AMI, instance type, or GPU identity
  differs. Available identity is recorded best-effort, but the difference does
  not block because machine-level equivalence is not the present contract.
- **Residual** — the coarse closure binds tracked project files and forbids
  untracked Python; it does not trace imports, syscalls, ignored/off-repo code,
  native libraries, or validate the live environment against its lock. A
  heavyweight trace/audit mode remains a candidate only if this residual
  proves valuable.
- **Status** — directly user-specified, implemented, and scenario-tested;
  external reproduction benefit remains unmeasured.

## 2026-08-13 — source admission does not require checked-in runtime state

- **User clarification** — the tracked-run guard verifies source-controlled
  files against the stated commit. It does not require a realized Pixi
  environment, intermediate dataset, or other normally provenance-tracked
  runtime artifact to enter Git.
- **Boundary** — standard Git ignore/exclude mechanisms exempt Python under
  derived trees such as `.pixi/`; their checked-in manifests and locks remain
  the reproducible authority. Non-ignored untracked Python remains the coarse
  near-term source-closure tripwire. Intermediate data remains eligible as a
  declared input/output with its usual hashes and producer links.
- **Trace** — a clean checkout contains committed `pixi.toml`, `pixi.lock`, and
  an ignore for `.pixi/`; the realized environment contains Python packages and
  an untracked JSONL intermediate is declared as input. Admission passes and
  records the pins plus data provenance without enumerating environment files.
- **Status** — directly user-specified and regression-tested; no claim that the
  realized environment byte-for-byte matches its lock.

## 2026-08-13 — advisor packets retain worker authority and watch governance

- **Incident** — Codex `gpt-5.6-sol` worker session
  `019ff3b5-da27-7fd0-9ffc-08ee9d6c0d47` asked a research advisor to rank the
  next actions, decide whether an idle GPU should be used, and later say whether
  implementation readiness changed the prior ordering. The advisor answered
  the requested questions; the worker then described the response as not
  authorizing an accelerator run and adopted the advisor's ordering. The user
  diagnosed a submissive worker stance: an advisor generally does what the
  packet asks, so the primary correction belongs in guidance for composing and
  evaluating consultations, not another assertion that the advisor is a
  reviewer.
- **Decision ownership** — an advisor packet now identifies the decision owner
  and a review target. Unless a cited user instruction or governing artifact
  explicitly delegates the choice, resource allocation, run launch, priority,
  acceptance, execution, and research direction stay with the user or working
  session. A recommendation or ranking is valid advisory input when the packet
  states the worker's intended decision and rationale. The worker separates
  checkable claims from advice, makes its own decision, and never reports that
  the advisor authorized, denied, permitted, or vetoed object-level work.
- **Governance currentness** — the user also required possibly changed
  `~/agents` advisor governance to become an explicitly watched, fully read
  source set across projects. Metadata owns the portable source spellings;
  `docs/state.md` records resolved paths, SHA-256 hashes, and the provider
  context of the last full read. The default core is
  `advisor/charter.md`, `research-advisor.md`, and `RESEARCH/direction.md`, plus
  project/program charter amendments. Every interaction hashes the stack and
  fully reads new or changed sources. An unchanged receipt waives rereading
  only in the same verifiably uncompacted context; a durable hash cannot prove
  that text survived a later compaction.
- **Trace: resource recommendation** — a worker intends to launch a matched
  pair and asks what publication risk it would address. The packet names the
  worker as decision owner and its rationale. The advisor may oppose the run or
  find its evidence value weak; the worker verifies factual claims, weighs the
  broader program and resource state, and decides without converting the memo
  into permission.
- **Trace: factual correction** — an advisor says a confidence interval used
  the wrong resampling unit. The worker checks the scorer and artifact and
  corrects a confirmed error. Decision ownership does not soften evidence or
  protect the worker from a valid review finding.
- **Trace: explicit delegation** — the user explicitly asks the advisor to
  choose between two paper forms. The packet cites that delegation, so the
  advisor may make the delegated choice; the default non-authority rule does
  not override the user.
- **Trace: governance drift and compaction** — a program advisor remains in
  one uncompacted context while all source hashes match, so it skips redundant
  full reads. A later charter edit changes one hash, so the next interaction
  fully reads that source before advising. After an unprotected compaction, it
  rereads the complete stack even though the durable hashes still match; exact
  harness reconstruction is the only waiver.
- **Status** — directly user-specified and trace-simulated. The currentness
  cursor is an instruction-level invariant rather than a mechanically enforced
  `session-turn` feature; behavioral effect remains assumed.
- **In-turn wording refinement** — the user supplied the governing principle
  `do not outsource your decisions` and the corresponding packet shape: ask
  for findings and arguments for and against the worker's proposed choice.
  This supersedes the draft's allowance for asking the advisor to rank what
  the worker should do. A recommendation is no longer the default request;
  explicit user or governing-artifact delegation remains the exception.
- **Watch-set bootstrap refinement** — `~/agents/topics/handoffs.md` joins the
  default core because its advisor-output evaluation rules govern the same
  flow. Before dispatch, the worker reconciles metadata with the protocol's
  current defaults, preventing a legacy metadata list from hiding a newly
  added governance source from the advisor that needs to learn about it.
- **Refined trace: legacy decision packet** — a packet asks the advisor to rank
  GPU uses but supplies no worker proposal. The advisor provides the findings
  that apply across plausible choices and asks one focused question only if it
  would change the assessment; it does not withhold useful review or silently
  become the decision maker. The worker then states and owns its choice.
- **Refined trace: newly governed source** — a continuous advisor's metadata
  predates addition of `topics/handoffs.md` to the default core. The worker's
  current protocol read repairs the manifest before dispatch; the advisor then
  sees a new source, fully reads it, and records its resolved hash. Requiring
  the advisor alone to discover the addition would fail this bootstrap case.
- **Complete watched core** — `AGENTS.global.md`, `AGENTS.user.md`, and the
  `RESEARCH.md` router also govern a long-lived advisor and therefore join the
  advisor-specific sources in the default manifest. A stable second hash pass
  closes the race in which a governance file changes between its initial hash
  and full read.

## 2026-08-13 — glossary-owned topic scopes and names

- **User-defined model** — every named term in an active glossary is
  inherently topic-like, whether its canonical surface is a formal topic doc,
  proposal, draft, handoff, or another linked document. Projects may have
  multiple real `topics/` collections corresponding to multiple glossary
  scopes; root `topics/` is not the only semantic collection.
- **Resolution and creation** — “the topic for X” first resolves the nearest
  active glossary row and follows its existing canonical reference. If no doc
  exists, creation defaults to the current project and the broadest active
  glossary scope where the concern stays natural without pervasive qualified
  subtree names. A scoped owner creates sibling `topics/<name>.md`; promotion
  follows actual widening utility. `~/agents` is reserved for clearly reusable
  general agent workflow or explicit user direction.
- **Commit name** — preserve owner context while omitting the mechanical
  collection directory: `research/pii/topics/redaction.md` becomes
  `Topic: research/pii/redaction`, while root `topics/redaction.md` remains
  `Topic: redaction`. This generalizes the existing root basename rule, makes
  cross-scope collisions harmless, and avoids imposing preventive global
  naming discipline. `Onboarding:` continues to use the actual doc path.
- **Research consequence** — active publication threads need one
  glossary-named canonical topic surface, not a duplicate root stub. An
  existing proposal or draft satisfies discovery. A separate formal internal
  topic appears once mechanisms, live status, negative results, or experiment
  specifications need an internal decision surface, and is then linked
  bidirectionally to the publication draft.
- **Trace: local program term** — PII-only `redaction` with no existing doc
  creates `research/pii/topics/redaction.md`; its trailer communicates program
  context and does not collide with a root `redaction` topic.
- **Trace: existing arbitrary doc** — a program glossary links `calibration`
  to `papers/calibration-proposal.md`. A request for its topic opens that file
  and creates nothing. If the proposal later accumulates internal run-control
  detail, a program topic may be split out and linked then.
- **Trace: widening audience** — a concern begins program-local but later
  governs several project programs. It promotes to the project glossary and
  root topic collection. Historical scoped trailers remain valid; the new
  series uses the promoted name without rewriting history.
- **Trace: global temptation** — two projects could plausibly reuse a term,
  but its current content names project data and paths. It remains at project
  scope. Only clearly general agent-workflow guidance or explicit direction
  promotes it to `~/agents`.
- **Status** — directly user-specified and scenario-traced. Lookup and naming
  are convention-level behavior; no automated glossary regenerator currently
  enforces the hierarchy.

## 2026-08-13 — PROGRAM.md is the program declaration and charter

- **User-defined surface** — a glossary directory may carry `PROGRAM.md`, a
  concise statement of the durable aspirations, themes, and boundaries that
  span its topics. It deliberately excludes current plans, progress, topic
  inventory, and handoff state. A nested charter specializes its parent rather
  than duplicating it.
- **Discovery decision** — `PROGRAM.md` presence alone declares a program and
  the directory basename supplies its slug. The older `Research program:`
  glossary header may remain but is inert; all instruction consumers now
  discover only `PROGRAM.md`. This keeps `GLOSSARY.md` purely vocabulary and
  avoids splitting narrative scope across a table preamble and a charter.
- **Update verb** — “update program scope” reads or infers the nearest charter
  from explicit recent user direction, its prior text, glossary definitions,
  canonical topic docs, and repository evidence. “Update all program scopes”
  repeats that reconciliation project-wide. Tactical recency must not silently
  narrow the durable aspiration, and a merely lexical glossary scope need not
  receive a charter unless a coherent program is inferable or explicitly
  requested.
- **Trace: inferred charter** — a research directory has a glossary, several
  mutually supporting papers, and repeated user framing but no `PROGRAM.md`.
  An update request creates a short charter from their shared aspiration and
  marks a consequential uncertainty rather than inventing certainty.
- **Trace: priority change** — `research/ROOT.md` favors another program this
  month. The program charter stays unchanged because ROOT is current
  cross-program triage, while PROGRAM is durable scope.
- **Status** — directly user-specified. The active-project migration supplies
  the first repository-wide exercise of inference and declaration discovery.

## 2026-08-13 — program-map boot and path-local glossary awareness

- **User correction** — program charters are not only declarations consulted
  after a program is named; their concise spanning aspirations are the useful
  project map. A root charter may optionally name major children, but relying
  on that list would make omission or staleness hide a real subprogram.
- **Boot decision** — after loading project instructions, locate and fully read
  every project-owned `PROGRAM.md`, excluding vendored or nested external
  repositories. This replaces the unconditional root-glossary read. Charters
  are intentionally short enough for full project-entry orientation.
- **Glossary decision** — before interpreting or changing a file at a new work
  site, identify its nearest-enclosing glossary and active parent chain.
  Targeted row search is sufficient until the work actually needs broader
  vocabulary; unknown terms, naming, and paraphrase trigger consultation. Any
  glossary read ensures its sibling charter has been read once that session,
  joining local vocabulary to the program aspiration that gives it context
  without turning repeated term lookup into repeated charter reads.
- **Trace: nested program omitted at root** — a root charter says nothing about
  `research/pii/PROGRAM.md`. Project entry still finds and reads the child, so
  the agent knows the program exists before choosing a scope.
- **Trace: unfamiliar local term** — an agent enters `sdl/AwesomeAlign/` to
  understand a file, locates the subtree glossary, and searches the term it
  encounters. It need not spend a full-table read before any vocabulary is
  relevant, but cannot assume the root glossary is the only authority.
- **Status** — directly user-specified and scenario-traced; discovery remains
  convention-level rather than mechanically enforced.

## 2026-08-13 — PROGRAM.md can carry scoped binding instructions

- **User-defined surface** — descriptive charter text remains the default in
  `PROGRAM.md`. A Markdown section headed exactly `Program instructions`, at
  any level, is binding for activity in the containing directory subtree; its
  nested subsections remain in the section until the next equal- or
  higher-level heading. Applicable global and project agent instruction files
  keep precedence. Ancestor program instructions inherit inward and a nearer
  rule wins only when they conflict.
- **Identity decision** — `# Program <short name>` is an optional first-line
  alternative formal name. The directory path remains the canonical locator,
  so a missing title changes nothing and discovery never depends on a
  project-wide name registry. Generic `# Program` headings in this repository
  were removed rather than pretending the formal name was “Program.”
- **Inference boundary** — “update program scope” and inferred-charter creation
  operate only on descriptive material. Program instructions are created or
  revised only from explicit user direction; repository evidence cannot
  silently promote a convention into a binding rule.
- **Trace: short-term topic** — a program instruction requires every proposed
  topic, even short-term work, to appear in a paper's Future Work section. An
  agent adding such a topic in that subtree also adds the reference; an agent
  working in a sibling program does not inherit the rule.
- **Trace: imperative charter prose** — a descriptive paragraph says the
  program favors cheap matched baselines. It guides orientation but is not
  parsed as a mandatory action because it lies outside a `Program
  instructions` section.
- **Trace: nested program and scope refresh** — a child program inherits a
  compatible parent rule and overrides only a conflicting program rule. A
  later “update all program scopes” rewrites stale aspirations while preserving
  both binding sections byte-for-byte unless the user explicitly changes them.
- **Trace: optional name** — `research/pii/PROGRAM.md` with no H1 is still the
  program at `research/pii`. Adding `# Program PII` supplies another formal
  name without changing discovery or scope; an identically titled program at a
  different path remains distinct.
- **Trace: section extent** — under `## Program instructions`, a nested
  `### Paper additions` subsection remains binding, while the next `## Notes`
  returns to descriptive charter text. The rule does not leak through the rest
  of the file or demote the nested subsection to commentary.
- **Status** — directly user-specified and already instantiated in `~/draft`;
  behavioral effect remains unmeasured.

## 2026-08-14 — semantic dataset review at judgment-bearing boundaries

- **User direction** — data preparation and augmentation should expose a
  stratified human-readable sample early enough for holistic judgment about
  whether the data could satisfy the research goal. Non-English rows need a
  rough English gloss, and imperfect semi-supervised or unsupervised data may
  still be useful when it improves the current hillclimbed model.
- **Placement** — `RESEARCH/evidence.md` owns semantic goal fitness and the
  research routers now reach it when accepting newly ingested or materially
  transformed data. `RUNS/provenance.md` retains structural identity,
  alignment, and outlier checks; those are complementary rather than
  duplicated.
- **Trace: verified lossless sharding** — serialization and partitioning are
  demonstrably semantics-preserving and their relevant invariants pass, so the
  qualitative review does not repeat. Determinism alone would not earn the
  exemption if a transform could still alter meaning or distribution.
- **Trace: multilingual augmentation** — the table covers every represented
  language, type, and domain level, with English glosses, but does not require
  the full Cartesian product unless a plausible interaction makes those cells
  material. Informative failures remain visible rather than being sampled away.
- **Trace: noisy pseudo-labels** — visibly imperfect examples do not force
  rejection when a controlled, non-leaky downstream comparison clears the
  incumbent. Failure to clear it redirects diagnosis toward pipeline defects,
  corpus/resource intake, teacher supervision, and filtering or reweighting.
- **Status** — directly user-specified and trace-simulated; behavioral benefit
  remains assumed.

## 2026-08-15 — repeated-prefix KV reuse stayed task-local

- **Incident** — the user had already worked through reusable prompt-prefix
  key/value state for the translation path, but a later many-document PII
  teacher decode initially recomputed the same long instruction prefix. The
  optimization remained narrow stack knowledge and did not generalize to the
  new caller.
- **Decision** — the draft project's boot now points repeated-prompt decode to
  its shared `decodelib.py` facility. The rule names the operational sequence:
  split an exact common token prefix, prefill once, and attach the copied state
  while building each batch. Cache identity includes the exact prefix and
  model state; left padding is masked layout, not content identity.
- **Trace: same prompt, many documents** — one frozen instruction and schema
  prefix precedes thousands of independent document suffixes. Literal use
  reuses one prefill through `decodelib` rather than independently
  hand-threading raw `past_key_values` in another task script.
- **Trace: changing model state** — rows select different weights or adapters.
  The exact-model-state condition prevents reuse across them; the rule does not
  trade correctness for a cache hit.
- **Trace: numerical bifurcation** — the cache layout is logically identical,
  but finite-precision prefill grouping changes a greedy continuation. The
  required task-quality on/off check judges the actual application rather than
  imposing byte equality or claiming equivalence from fluent smoke output.
- **Status** — user-specified and scenario-traced. Small-model layout tests and
  a Gemma-4 diagnostic exercise the facility; the long PII task quality and
  throughput comparison remains pending.

## 2026-08-15 — harsh-review findings become range-keyed artifacts

- **User direction** — replace session-only harsh-review output with retained,
  uncommitted review history: a range-named accumulator plus a final verdict
  written before findings are communicated. The response links the verdict by
  project-relative path instead of duplicating its findings inline.
- **Range identity** — both diff endpoints resolve to immutable SHAs when the
  review starts; the readable key uses their 12-character abbreviations while
  each artifact records the full SHAs. `HEAD` may select the endpoint but can
  never remain in a filename, because it may move before a folded review ends.
- **Trace: one-pass review** — a small single-commit audit writes its running
  findings to `harsh-review-<base12>..<end12>.accum`, derives the final
  `.verdict.md`, retains both locally, and replies with the verdict link only.
- **Trace: long review with advancing HEAD** — a folded `since` review resumes
  the unfinished accumulator's frozen target even after new commits land. Its
  end-state suppression check reads the later diff, the completed verdict keeps
  the original immutable range, and the next `since` review covers new work.
- **Trace: ambiguous resume** — more than one unfinished accumulator begins at
  the marker. The skill names the candidates and asks which fixed range to
  resume rather than choosing by mtime or silently merging histories.
- **Trace: concurrent same-range start** — each reviewer checks fresh active
  sessions, claims the range and its canonical paths through `agentctl active`,
  then checks again. An existing claim wins; a simultaneous race resolves by
  claim age and session id, and every loser marks itself done without touching
  the records. The claim remains advisory rather than pretending to be a
  filesystem lock.
- **Trace: same-range second opinion** — after winning the advisory claim, the
  reviewer renames both canonical files to the next numbered backup without
  reading their contents. It records an independent provisional verdict in a
  fresh accumulator; only at the explicit reconciliation phase does it read
  the prior pair. Item dispositions stay in the accumulator, the canonical
  verdict contains only clean merged findings, and the response briefly names
  valid findings missed by the independent pass or newly found. The backups
  are history, not resume candidates.
- **Status** — directly user-specified and trace-simulated; actual use will test
  whether file-only findings improve review history without making delivery
  harder to notice.

## 2026-08-15 — harsh-review records leave the project root

- **User correction** — retaining every accumulator, verdict, and prior pair at
  project root creates visible filesystem clutter even though Git excludes the
  files. Keep only the established `.harsh-review` current-through marker there.
- **Decision** — create `harsh-review/` when absent and store range records as
  `<range>.accum`, `<range>.verdict.md`, and numbered prior pairs inside it. The
  clone-local exclude covers the directory; active-session claims and final
  links use the project-relative paths below it.
- **Trace** — a first review in a project with only the legacy marker runs
  `mkdir -p harsh-review`, preserves the marker as its bare-`since` baseline,
  and writes both records under the new directory. A same-range second opinion
  renames both files inside that directory before the independent pass, so it
  creates no additional root-level files.
- **Status** — directly user-specified; this supersedes only the root-level
  record paths in the immediately preceding entry.

## 2026-08-15 — harsh-review route and bounded-sample repairs

- **Trigger** — a range review found three routing/boundary failures in newly
  split policy: boot-visible RUNS omitted the storage-only cue, boot-visible
  RESEARCH omitted handout and research-blog cues, and topic ownership assumed
  a root glossary even though the glossary-creation rule deliberately permits
  one ordinary topic without one. It also found a compact qualitative sample
  could become exhaustive over hundreds of represented levels.
- **Decision** — preserve the missing observable terms in
  `AGENTS.global.md`; treat the project root as the implicit topic scope until
  a root glossary exists; exhaust only acceptance-critical axes of at most 12
  levels; and cap the primary qualitative table at 32 rows, using explicit
  frequency/risk coverage for larger axes. A separately declared audit remains
  available when exhaustive high-cardinality review is the actual task.
- **Trace: short CPU cache build** — a one-minute preprocessing job writes a
  large model cache. The storage phrase now reaches RUNS and its filesystem
  preflight even though the job is neither GPU-backed nor long-running.
- **Trace: direct handout request** — completed results are supplied with
  “write a handout.” The protected term reaches RESEARCH and the artifact
  packet rather than relying on an agent to generalize “paper/report.”
- **Trace: first project topic** — a project with no glossary needs one
  cross-cutting contract. It creates root `topics/<name>.md` under the implicit
  project scope without manufacturing a one-row glossary; a later root
  glossary takes ownership of the same collection without moving the topic.
- **Trace: 600 sources** — language and label type are acceptance-critical and
  small, while source id has 600 levels. The sample covers every small critical
  level, common source mass, rare/boundary sources, and known failures inside
  32 rows, reports the 600-level denominator, and creates a separate audit only
  if the decision genuinely requires all sources.
- **Read cost** — the protected global main changed 42,033 → 42,302 bytes;
  `_RUNS/resources.md` changed 9,289 → 7,559 after removing its duplicate
  protocol; and `_RESEARCH/evidence.md` changed 13,109 → 13,774.
- **Status** — scenario-traced; behavioral benefit and the 12/32 defaults
  remain assumed.

## 2026-08-15 — advisor consultation gets a bounded serve packet

- **Trigger** — range review found that an ordinary tell/ask trigger required
  complete reads of both the 879-line object-session protocol and the 653-line
  charter, even though succession, generation fencing, archive repair, and
  shutdown are rare. This repeated the oversized-read failure mode that caused
  the packet reorganization elsewhere in the corpus.
- **Decision** — `advisor/serve.md` now owns the complete ordinary worker and
  advisor path: scope resolution, decision ownership, packet, `session-turn`
  delivery, synchronized review, challenge memo, sign-off checkpoint, and
  worker evaluation. The long protocol and charter remain live catalogs, but
  ordinary routes explicitly forbid reading them in full and name the exact
  sections for first establishment, legacy/succession, collision, fold debt,
  document recovery, handoff repair, transport ambiguity, and shutdown.
  Existing advisor governance manifests replace only the former default long
  entries; project/program amendments remain intact.
- **Trace: ordinary tell** — “tell advisor this result” reaches RESEARCH,
  direction, and the 250-line serve packet. The worker can deliver one bounded
  interaction and the advisor can return and checkpoint its memo without
  opening either long catalog.
- **Trace: first consultation** — no metadata exists. The serve packet routes
  to “Scope and continuity” plus “Establishing the logical advisor,” then the
  ordinary path resumes. It does not load shutdown, archive, or collision
  mechanics preemptively.
- **Trace: retired incumbent** — generation state conflicts during resume. The
  explicit legacy/succession route loads the binding/state and succession
  sections from both catalogs before any continuity write, so the read-size
  optimization does not soften the fence.
- **Trace: shutdown** — the exact `Shutdown advisor` directive routes to the
  shutdown and succession sections. Ordinary sign-off stays in the serve
  packet and cannot accidentally imply retirement.
- **Recovery and read cost** — no catalog body was removed; prior text remains
  recoverable both in current files and Git. The former ordinary pair totaled
  87,012 bytes (`research-advisor.md` 50,701 plus `advisor/charter.md` 36,311).
  The new independently read serve packet is 12,888 bytes, an 85.2% reduction;
  each rare condition now reads named sections rather than either full catalog.
- **Status** — scenario-traced and caller-swept; consultation correctness and
  future manifest migration behavior remain assumed.

## 2026-08-15 — commit messages use one formatted, linted path

- **Trigger** — range review found two published commit messages containing
  literal two-character `\n` sequences and four with wrappable prose beyond
  the 71-column contract. The existing linter checked `\n` only in the subject,
  its formatter accepted the escape unchanged, and the documented composition
  example discarded the linter's stdout before `git commit -F -` read stdin.
- **Decision** — non-trivial agent messages now go through
  `commit-msg-fmt | commit-msg-lint` as the file supplied to Git. Preformatted
  messages use a draft file and the same linter. Both helpers reject literal
  `\n` anywhere; the formatter tells the caller to express structure with
  separate `-m` arguments. Published history is left intact as the review
  required.
- **Trace: escaped body** — one `-m` argument contains
  `Body\\nContributing-model`. The formatter fails before Git runs, and a
  hand-authored draft containing the same bytes fails at the exact body line.
- **Trace: long prose** — a long body paragraph is passed as one ordinary
  formatter argument. It wraps to at most 71 columns, then the linter accepts
  the exact bytes Git consumes.
- **Trace: preformatted content** — a message contains bullets whose hanging
  indentation must survive. The agent skips the plain-prose formatter, lints
  the authored draft, and commits that same file; no whitespace-collapsing
  helper touches it.
- **Status** — helper tests cover literal body escapes, prose wrapping, the
  formatter-to-linter boundary, and a real Git commit through the documented
  Bash process substitution. The behavioral effect of making the path explicit
  remains assumed.

## 2026-08-15 — ordinary advisor packets carry ownership acquisition

- **Trigger** — range review found that `advisor/serve.md` required exclusive
  ownership and told the advisor to release it at sign-off, but routed the
  corresponding acquire/check protocol only through a rare collision branch.
  A second ordinary dispatcher could therefore follow the bounded packet
  literally and reach continuity writes without the normal ownership step.
- **Decision** — the ordinary packet now makes ownership one delivered-turn
  transaction. The worker resolves fresh claims and reuses the incumbent; the
  advisor registers and checks its directory scope; an automated router
  acquires and holds an atomic scope/generation lease when that facility
  exists. The packet says explicitly that active-session claims are only a
  collision detector and that a detected collision blocks continuity writes.
- **Trace: concurrent dispatch** — two workers target one logical advisor.
  Both encounter the ordinary ownership section before `session-turn`; the
  established incumbent wins, or only one atomic lease acquisition succeeds.
  The other worker cannot create a second continuity writer and follows the
  collision route if the live owners remain ambiguous.
- **Trace: transport has no lease facility** — one worker sees no competing
  claim and uses the current active-session convention without calling it an
  atomic lock. If a competitor appears before a write, the advisor's repeated
  check blocks that write but still allows a visibly provisional memo; it does
  not merge or fence state from advisory evidence.
- **Trace: sign-off** — the winning advisor holds any acquired lease through
  notes, intake, and the final session projection, then releases the lease and
  turn-scoped active ownership. The continuous provider session remains the
  resumable incumbent rather than being retired by ordinary sign-off.
- **Trace: generated web digest** — `scripts/web-digest.manifest` now includes
  `advisor/serve.md`, so rebuilding the local digest exposes the ordinary
  acquisition rule to its claude.ai audience instead of supplying only the
  long catalogs that route away from the ordinary path.
- **Status** — scenario-traced; the current active-session fallback remains
  advisory, and no generic atomic advisor-lease implementation is claimed.

## 2026-08-16 — yielded run handles are observable monitoring triggers

- **Trigger** — an agent deferred a `start --watch` tool call after it yielded
  a live terminal handle, then lost the handle. The payload's receipt passed,
  but the old `agentctl` watch path had no durable completion recorder and
  finalized the run as `returncode=unknown`. The user explicitly asked for a
  monitoring trigger more likely to survive compaction or a mechanical repair.
- **Decision** — the compaction-protected `AGENTS.global.md` route and compact
  `RUNS.md` router now name receiving or resuming a yielded live terminal/
  session handle as an observable monitoring cue. The router carries the
  immediate action: absent new user steering, consume only that handle until a
  wake condition or timeout. The launcher independently removes the dangerous
  consequence by making `--watch` a disposable observer of the same durable
  `_run-child` used by every start.
- **Trace: yielded watched launch** — `start --watch` returns a live handle.
  Even after compaction, that visible tool state routes through `RUNS.md` and
  the agent continues consuming the handle instead of labeling it deferred.
- **Trace: user interruption** — new user steering arrives while the handle is
  live. The router's explicit exception permits the packet's normal
  interrupted-wait handling rather than making the agent ignore the user.
- **Trace: completed detached launch** — ordinary detached `start` returns a
  completed tool result, not a live handle. The added cue does not invent a
  foreground wait; the existing launch/monitoring routes still decide the next
  action.
- **Status** — the launcher regression mechanically covers terminal-status
  durability. The instruction effect is scenario-traced and remains assumed.

Contributing-model: 5.6-Sol

## 2026-08-16 — ACLI accepts an explicit redundant `--json`

- **Incident** — an agent invoked `agentctl status --json <job>` to state the
  required serialization explicitly, but argparse rejected `--json` even
  though ACLI already standardized compact JSONL and several ACLI surfaces
  emitted it by default. The rejection added a discovery/retry turn and made
  the flagship ACLI consumer look less conventional to an agent caller.
- **Decision** — every JSON-emitting ACLI parser accepts `--json` as an alias
  for compact JSONL, even when that is already the detected default. Job
  `status` and `list` expose structured envelopes only under explicit ACLI
  output flags for now, preserving their longstanding text output for existing
  operators and scripts.
- **Trace: redundant explicit intent** — a compact-by-default verb receives
  `--json`; it emits the same JSONL schema instead of failing. A human TTY uses
  `--json` to override pretty output. `--pretty` remains mutually exclusive,
  so contradictory serialization requests fail at the input boundary.
- **Trace: legacy status caller** — a script greps the one-line default
  `agentctl status` output and keeps working. An agent uses
  `agentctl status --json <job>` and gets a parseable envelope; `--full`
  widens the rows and `--tail` stays inside JSON rather than corrupting it.
- **Status** — parser and end-to-end tests cover the alias, completion, both
  option positions around the job, and full status records. The effect on
  failed-call frequency remains assumed.

Contributing-model: 5.6-Sol

## 2026-08-16 — scoped gaps/ and two-grain gap granularity

- **Provenance** — user direction: research programs should own sibling
  `gaps/` so complaints noticed in passing stash without derailing active
  work, and gap-capture phrasing must not read create-biased when an
  observation is close enough to merge into an existing entry. Anchored on
  glossary scope rather than a second PROGRAM-only scope system: every
  `PROGRAM.md` sits beside a `GLOSSARY.md` (verified, all four), and
  `topics/` ownership is already glossary-anchored, so "the controlling
  program's sibling `gaps/`" resolves to the same directory for free.
- **Why topics/ behaves well** — traced the create-at-right-grain /
  merge-when-duplicative behavior to TOPICS.md's landing-site principles
  (name the retrieval trigger; one home plus pointers) plus `AGENTS.global.md`
  § "Add X" when X already exists and the "add/update" framing in § Project
  topics; nothing in the corpus forces new-file creation. Gap writing now
  routes through the same principles via `gaps/README.md`, which the boot
  already points at — no new mandatory read.
- **Granularity restated** — supersedes the earlier gap-routing default
  ("one running gap per topic"): a gap file is either a topical triage pool
  of less-investigated noticed items awaiting a planning pass, or a
  session-sized unit carrying the claim that program goals stay impaired
  until it clears. The impaired-until-cleared test also sharpens the
  gap/sketch boundary (sketches don't impair). The no-`*.gaps.md`-namespace
  and no-routine-companion-scan decisions stand.
- **Dedup found** — `topic-doc-format.md` restated the gap-granularity
  default owned by `gaps/README.md`; trimmed to a pointer (one home).
- **Trace: no gaps anywhere** — "enclosing scopes' existing `gaps/`
  directories" no-ops on "existing"; a project with only root `gaps/` keeps
  the old behavior since root is an enclosing scope. "Becomes or extends"
  reads as alternatives, not a mandate to do both.
- **Status** — landed in `AGENTS.global.md` § Adjacent gaps,
  `gaps/README.md` (new Scoped gaps directories section, reworked Reading
  and granularity), `TOPICS.md`, `topic-doc-format.md`. Untested premise, as
  ever: that the finer-grain wording steers capture without inviting
  non-defect backlog into `gaps/`.

Contributing-model: Fable

## 2026-08-16 — partial-goal commits expose their series context

- **Trigger** — a mid-goal commit can accurately describe its own outcome while
  leaving a reviewer unable to distinguish the active user-requested goal from
  the portion present in that diff. A committed topic, gap, or plan may expose
  the larger direction, but it may also be broader than the request, stale, or
  written before the current work began.
- **Decision** — when substantive work remains in the active request, the commit
  body uses three line-start labels: `Series goal:`, `This commit:`, and
  `Remaining after this commit:`. Blank lines are optional. An accurate
  committed governing artifact may carry the series context; otherwise the
  message summarizes the active task rather than citing private state.
- **Historical phrasing** — `Remaining after this commit:` describes the state
  at that commit instead of making an unqualified present-tense claim. It stays
  true after later commits land. The complete-goal case uses ordinary narrative
  rather than empty labels or `None`; the format is triggered by a substantive
  nonempty remainder, not merely by topic-series membership.
- **Trace: partial implementation** — the first of several feature commits names
  the full request, its own landed slice, and the work remaining after that
  slice, so the overall goal is visibly context rather than a claim about the
  current diff.
- **Trace: complete implementation** — one commit lands the whole requested
  goal. The remainder is empty, so the three-label form does not fire and the
  ordinary reviewer-on-ramp message remains concise.
- **Trace: pre-existing roadmap** — a commit satisfies its active request while
  its topic contains dormant follow-ups. Those candidates do not create a
  remainder or a promised series; the ordinary format applies.
- **Status** — user-directed and trace-simulated; effect on review accuracy and
  message length remains assumed.

Contributing-model: 5.6-Sol

## 2026-08-17 — UI captures use bounded sequential inspection

- **User correction** — desktop UI verification should capture exactly
  1200×600 rather than a larger viewport, and image reads should happen one at
  a time to avoid exhausting the model context. The phone viewport remains
  375×812.
- **Decision** — the compaction-protected global rule now names both exact
  viewports and forbids batching image reads. The project protocol makes the
  sequence operational: read, inspect, and record notes for the desktop image
  before reading the phone image.
- **Trace: responsive UI** — an agent captures 1200×600 and 375×812, reads the
  desktop image alone, records its layout findings, and only then reads the
  phone image. Both responsive surfaces remain covered without loading a
  multi-image batch.
- **Trace: desktop-only UI** — an interface without mobile support still uses
  the exact 1200×600 desktop capture. The conditional phone requirement remains
  unchanged rather than making every desktop-only application emulate mobile.
- **Counter-trace: several states** — a flow needs before/after or source/preview
  evidence. Each capture is read and assessed separately; the need to compare
  states does not permit a batched image read.
- **Status** — directly user-specified and scenario-traced; reduction in context
  exhaustion remains expected rather than measured.

Contributing-model: 5.6-Sol

## 2026-08-17 — inventory and migrate agent-facing environment names

- **User correction** — YA broadly strips inherited `YA_*` and `YEP_*`, so the
  harsh-review finding could not treat every product-prefixed value in a
  provider shell as an accidental pass-through. The surviving values arrive by
  explicit allowlist, provider overlay, or the late Bash bridge. The user
  nevertheless wants fresh harness/script children to shed caller-session
  identity and credentials, and wants collision-resistant `AGENT_*` names that
  non-YA launchers can publish.
- **Decision** — `topics/AGENT_ENV_VARS.md` is the one name/effect/boundary
  inventory. Canonical names distinguish launcher, harness, route, and backend:
  `AGENT_LAUNCH_ROUTE=claude-gateway` and
  `AGENT_LAUNCH_BACKEND=copilot-api` replace two unrelated booleans without
  collapsing their semantics. Wake and browser capabilities name their scope
  and role. `AGENTCTL_SESSION_ID` stays because an unqualified
  `AGENT_SESSION_ID` could collide with provider, broker, or tool identities;
  `YEP_ORIGINAL_BASH_ENV` stays private because it is bridge machinery rather
  than agent-addressed state.
- **Compatibility** — unlike the earlier invisible `YEP_AGENT_*` launch
  markers, the remaining names have live readers. Migrate readers first,
  prefer a complete canonical pair, retain explicit legacy fallbacks, then
  migrate publishers and eventually remove aliases. The open YA gap owns that
  cross-repository publisher sweep; instruction text names current aliases as
  compatibility debt rather than using them as precedent.
- **Trace: compatibility precedence** — a non-YA launcher publishes a future
  explicit backend while a stale shell still carries `YEP_COPILOT_API=1`.
  Routing follows the canonical backend and ignores the YA alias; treating both
  as unconditional signals would load the wrong supplement.
- **Trace: fresh target** — a YA Copilot-backed Claude caller invokes
  `session-turn` native fallback for a plain Codex target. The target receives
  its own `AGENTCTL_SESSION_ID` and `AGENT_LAUNCH_HARNESS=codex`, retains
  `AGENT_GUARD`, and receives neither route/backend selection nor wake/browser
  capability in either canonical or legacy spelling.
- **Trace: agentctl payload** — `agentctl` increments launch depth and supplies
  run context but otherwise inherits ambient variables. The inventory states
  that wake/browser values currently reach both detached wrapper and payload;
  it does not silently imply masking that the implementation does not perform.
- **Status** — user-directed naming and documentation; focused tests cover
  canonical wake precedence, legacy wake fallback, and native-child cleanup.
  YA publisher migration remains open by design.

Contributing-model: 5.6-Sol

## 2026-08-18 — observed-form tolerance in throwaway orchestration

- **User direction** — agents mis-model tool output forms in near-throwaway
  orchestration scripting (expect JSON, get text, or the converse).
  Defensive handling of either form is acceptable when meaningful tests
  would catch a misinterpretation and the alternate form preserves the
  needed information; the correct fix (understand the tool, request the
  expected form) should win when it yields helper or instruction
  improvements worth having. Caution should scale with the future work a
  missed misreading would invalidate.
- **Decision** — `AGENTS.global.md § Anti-slop implementation` gains a
  scoped tolerance paragraph: branches only for observed forms (never
  imagined ones), information-preserving and unambiguous, a form mismatch
  detected rather than read as zero results, the unexpected branch logging
  that it fired; one bounded probe for an explicit format option first; a
  second surprise from the same tool ends tolerance and fixes the
  invocation/option/helper/instruction. Durable scripts keep the
  documented-contract bar of the base rule. The companion `tool-surprises`
  skill/helper (same-day commit) is the systematic detector behind the
  informal second-surprise trigger.
- **Trace: forgot the flag** — an agent expects JSON from `gh pr list`,
  gets a table. The rule sends one `--help` probe → `--json` exists → the
  correct invocation replaces a dual parser. No backfire.
- **Trace: legitimate empty** — a scan legitimately returns zero items.
  The chosen wording ("a form mismatch is detected rather than read as
  zero results") requires distinguishing well-formed-empty from
  unparsed-form; it deliberately does not mandate fail-on-empty, which
  would misfire here.
- **Trace: undocumented dual-form tool** — second surprise; `--help`
  shows no format option. Fix-the-understanding resolves to documenting
  the dual form (recovery as documented contract, which the base rule
  already allows) or a wrapper, so the rule converges with the existing
  exception instead of demanding a nonexistent flag.
- **Why the four conditions** — observed-only blocks speculative
  try/except branches that codify a hallucinated tool model; the
  mismatch-detection condition closes the vacuous-pass hole (a misparse of
  the wrong form typically yields empty-but-plausible results, e.g. `jq`
  over text); the logging condition preserves the signal that the tool
  model was wrong, without which the confusion silently recurs; TTY/pipe
  output switching means an untested branch can be the one that fires in
  production, which is why the probe-for-a-flag beats defensive parsing
  when a flag exists.
- **Status** — user-directed; trace-simulated; effect on retry cost and
  script quality is expected, not measured. The tool-surprises miner can
  later supply before/after counts.

Contributing-model: Fable

## 2026-08-18 — exact patch context and terminal cell consumption

- **Trigger** — a 30-day tool-surprises survey found 69 Codex patch-anchor
  failures in `~/agents` and 276 in Yep Anywhere, with nearly every failure
  followed by a successful same-target retry. The same survey found 12 stale
  `wait` calls in 12 Yep Anywhere sessions; 11 followed an already-terminal
  result, and none recovered on the same cell.
- **Decision** — the shared edit invariant now covers both exact `old_string`
  matches and patch-hunk context: copy the smallest identifying material from
  current visible output, and treat any intervening writer or formatter as
  invalidation. The Codex supplement projects that invariant onto
  `apply_patch`, where a recent same-file command is insufficient unless its
  displayed bytes supply the hunk. It also states that a terminal code-mode
  `wait` consumes its cell id, while an explicitly still-running result permits
  another wait on that id.
- **Trace: inferred patch context** — an agent runs `rg` against a file, then
  composes a hunk from remembered indentation and nearby lines. Literal use of
  the new rule rejects the memory-based hunk and copies minimal displayed
  context, preventing the verification retry rather than merely prescribing a
  reread after failure.
- **Trace: intervening formatter** — a formatter writes the file after the
  agent's read. The shared invalidation clause forces a fresh read before either
  `Edit` or `apply_patch`; the old output cannot authorize an exact-match edit.
- **Trace: consumed cell** — `wait({cell_id: 52})` returns a terminal completion.
  The next step does not poll 52 again. If instead the result says the script is
  still running with cell 52, the explicit exception permits another wait, so
  long-running work is not abandoned.
- **Status** — user-directed and trace-simulated. The baseline is measured;
  reduction in patch retries and stale waits remains to be checked in a later
  survey.

Contributing-model: 5.6-Sol
