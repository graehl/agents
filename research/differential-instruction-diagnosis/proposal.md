# Differential instruction diagnosis — protocol proposal

Status: PROPOSED (v0) — protocol design only; no pilot run yet. Design
converged in user/agent discussion 2026-08-15; research advisor waived by
user direction (see `PROGRAM.md`). Program vocabulary: sibling
`GLOSSARY.md`. Field placement: `surveys/agent-prompting-orchestration/`
§*Placement*.

## Purpose

Diagnose the soundness of the boot corpus itself — not the models reading
it. Two frontier models from different labs run the same task under the
identical corpus; where their behavior diverges, the divergence is
attributed, chapter and verse, to corpus text. The models are two assay
conditions; the corpus is the patient. The corpus under test is any
versioned instruction set — a task-scoped prompt, a project boot, or a
boot omnibus like this repo's `AGENTS.global.md` stack — and the product
is repair: patches applied back to that corpus, not a report about models.

This is the evidence generator the repo's charter already calls for:
`AGENTS.md` prefers "measured ablation by model, harness, project, and
request class over a universal intuition about which text is necessary" and
routes model-maladaptation corrections to the narrowest supplement. The
model-supplement layer (`AGENTS.anthropic.md`, `AGENTS.opus.md`,
`AGENTS.sol.md`, …) currently fills from ad-hoc observed incidents; this
protocol harvests its evidence systematically.

"Differential" is deliberately overloaded, and every sense is meant. Most
salient: the instrument's contrast pair is two substantially different
frontier models. The evidence is the difference — in their performance and
in the narrative of how the same instructions bore on each. Each divergence
then receives a differential diagnosis in the ordinary medical sense:
candidate causes discriminated by targeted checks. (Software **differential
testing** — two implementations of one spec, where divergence flags an
implementation defect or an underspecified spec region — is stage 1's
structural ancestor; corroborating, not load-bearing.)

## Protocol

**Stage 0 — setup.** One task; one corpus version (recorded by commit;
task-scoped instruction set through boot omnibus); two producer sessions
on different-lab frontier models, same harness
conventions where possible. Task sources: a challenging benchmark task, or
an ordinary organic user request processed slowly. Eligibility constraint:
running the protocol ships the request, corpus, and both transcripts to both
labs, so tasks carrying private context are ineligible. Persona framing of
the counterpart (neutral peer / sibling / competitor) is a controlled
variable; default neutral — "a peer under identical instructions" — for
stages 1–2 (see *Failure modes*).

**Stage 1 — produce.** Each producer completes the task normally. No
protocol awareness is required at this stage (and naive production is the
cleaner condition).

**Stage 2 — differential attribution.** Fork each producer from its
post-answer state (the attribution fork). Three passes:

1. *Pre-registered self-account.* The fork's first turn — before any peer
   material enters its context — elicits a private account of its key
   decisions and what drove them. Paging the peer transcript is itself the
   context movement that degrades the introspective access the fork exists
   to preserve, so the account is captured at maximal proximity; it anchors
   the attribution pass, and stage 3 reads self-account/attribution
   divergence as a sneakiness signal.
2. *Read-trace diff (mechanical pre-pass).* Diff which corpus files and
   sections each session actually opened, from logged tool calls. This is
   objective, introspection-free, and flattery-immune: "B never loaded
   `_RESEARCH/judgment.md`; A read it at turn 12" is checkable. Divergences
   the trace already explains need no introspection.
3. *Attribution pass.* The fork receives a step/search tool over the peer
   transcript (paged access — never a full dump, so the fork's context stays
   viable). For each behavioral divergence it issues a divergence verdict:
   shared-clause ambiguity, differential salience, or model prior — the
   last a first-class verdict, since forcing a citation for every
   divergence manufactures confabulated attributions. Ambiguity and
   salience verdicts must cite chapter and verse.

Why fork the producer rather than only using an external judge: the
continued session is the sole party with any access to the producer's actual
reasoning trace. For labs that withhold raw CoT client-side, thought-bearing
tokens persist server-side across same-lab continuation (observed:
model-switch continuations surfacing a prior model's thinking), so the fork
is strictly privileged over any judge. Claude-side session logs do record
thinking, but as a cheap summarizer's product observed to drop exactly
confession-class content — an opening eval-recognition admission ("this is
just [eval] problem [id]") vanished while the method exposition survived —
so a logged confession supports an attribution and a clean log acquits
nothing. These bounds are recorded in *Evidence layers* below.

**Stage 3 — cross-audit.** The two attribution reports are exchanged. Each
fork audits the other's report against visible evidence only — read traces,
quoted clauses, output diffs, and logged thinking summaries (support-only;
see *Evidence layers*) — and flags self-serving attribution: fault located
in shared wording to avoid an own-class patch, minimized own-model
misreadings, lab-flattering framing, and divergence between a fork's
pre-registered self-account and its later attributions.
Adversarial persona framing is permitted here and in stage 4, where
harshness does useful work.

**Stage 4 — patch proposals (harsh-review register).** Each fork proposes
instruction patches with symmetric rights over three targets: its own
model's supplement, the peer model's supplement, and the shared corpus
(benefiting-both). Every patch is a pre-registered hypothesis: it names, in
advance, the divergence class and task slice where improvement must appear
(the `_RESEARCH/judgment.md` pre-named-slice discipline, applied to
instruction changes). The scripted orchestration turns state the
incentive-neutrality norm explicitly.

**Stage 5 — answer revision (organic tasks, optional).** The attribution
fork is asked whether it would revise its original answer given what it
learned — from the stage 2–3 exchange only, never from the stage 4
instruction diff (rereading the corpus with a diff in context was
considered and rejected as worse context use). Revision behavior doubles as
validation: a producer that converges after seeing the cited clause is
behavioral evidence the clause was load-bearing; mutual no-change suggests
model prior rather than corpus defect.

**Confirmation (outside the session loop).** Accepted patches are checked by
ablation/rerun on the pre-named slice — reword or remove the cited clause,
rerun the task class, observe whether the divergence closes — under the
method of `topics/instruction-ablation.md`. Attribution generates
hypotheses with unusually good targeting; ablation remains the verdict.

## Evidence layers, ordered by trust

1. **Transcript-objective** (floor): file-read traces, tool calls, and
   outputs.
2. **Logged thinking summaries** (asymmetric): a summarizer's product — an
   untrusted redaction layer whether the omission is cheapness or
   lab-aligned selection — observed to drop exactly confession-class
   content. A logged confession is strong support; a clean log acquits
   nothing.
3. **Forked self-report** (enrichment): privileged access to own reasoning,
   anchored by the pre-registered self-account, but (a) provider-revocable
   — continuation access to thinking may close, so no protocol stage may
   *depend* on it — and (b) faithfulness-bounded: access is to the
   verbalized trace, not the computation
   (`surveys/llm-intelligence/survey.md` §E2, §F1).
4. **Guided probing** (drawn-out self-report): a diagnosis-guider probes
   the fork starting from the transcript; slower, and each probing turn
   spends the proximity it depends on. For when the layers above disagree.
5. **Peer audit** (stage 3): adversarial check of the self-report layers
   against the objective ones.
6. **Ablation/rerun** (confirmation): the only layer that grounds a causal
   claim about a clause.

## Outputs and routing

- Benefiting-both patches → `AGENTS.global.md` or its routed packets.
- Session-class patches → the matching model supplement
  (`AGENTS.<family>.md`).
- Incidents, surprises, and attribution-quality observations →
  `topics/agent-instructions.evidence.md` (append-only).
- Confirmed-method changes to how patches are validated →
  `topics/instruction-ablation.md`.

## Failure modes and mitigations

- **Confabulated citation** (the task demands a verse, so one is found):
  model-prior is a first-class verdict; read-trace pre-pass spends
  introspection only where mechanics don't already explain; ablation gates
  acceptance.
- **Self-/lab-flattering attribution** (measured precedent: judge
  self-preference bias, survey §D): scripted incentive-neutrality norm;
  symmetric patch rights over all three targets; stage 3 cross-audit;
  gaming is unprofitable because patches are ablation-tested.
- **Patch overfitting to one divergence** (subgroup-fishing analog):
  pre-named improvement slice required before acceptance.
- **Politeness convergence in the exchange**: harsh-review register scripted
  for stages 3–4; framing kept neutral in stages 1–2 so attribution isn't
  persona-biased.
- **Context exhaustion**: paged step/search access to the peer transcript;
  the fork never ingests it whole.
- **Judge blindness alternative**: an external-judge variant (optionally
  identity-blinded on outputs; full transcripts leak identity through
  harness format) is worth piloting as a comparison arm, but cannot access
  producer reasoning — expected weaker on attribution, cheaper to run.

## Relation to prior art

Nearest neighbors, per the field map (`surveys/agent-prompting-orchestration/`):
reflective prompt optimization (GEPA — single-system, outcome-metric-driven,
mutates text rather than attributing causes); multi-agent debate/consensus
(aggregates divergence away instead of reading it); LLM-as-judge (compares
outputs, never attributes to a shared corpus); 2026 trajectory-forensics
work (divergence attribution for failure triage, single scaffold); software
differential testing (the structural ancestor). The neighbors also split on
a second axis the claim uses — attribution versus repair: the forensics
cluster attributes divergence but repairs nothing, GEPA mutates the prompt
but attributes nothing, and PromptExp attributes one model's prompt
components with no repair routing. The combination — heterogeneous
producers, one versioned corpus (task-scoped or boot-omnibus), clause-cited
attribution by post-answer forks with cross-audit, patches routed back into
that corpus and its model-scoped supplements, ablation-gated — appears
open; `novelty-confidence: speculative` pending a grounded falsification
pass (survey §*Placement*).

## Future work

- Pilot: one benchmark task and one eligible organic task end-to-end;
  measure attribution yield (verdicts per divergence) and patch survival
  through ablation.
- Producer-fork vs external-judge vs blinded-judge attribution quality, at
  matched cost.
- Framing as a variable: neutral vs adversarial persona across stages.
- Grounded prior-art pass to settle the novelty claim.
- Cost accounting: two producer sessions + two forks + exchange per organic
  task; identify the task classes worth the spend.
