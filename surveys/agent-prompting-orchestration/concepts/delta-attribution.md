# Harness-Delta Attribution — what evolved harness gains are made of

Read method: full read of the saved source HTML (converted locally; committed
extract pending a fidelity-gate failure), 2026-09-25. Also read: the saved
`blog_data.js` payload, which holds per-model breakdowns and draft analysis
text, some of it stale; and the linked method spec
[HDA_SKILL.md](https://github.com/Wenwen-D/HarnessDeltaAttribution/blob/main/src/hda/HDA_SKILL.md)
(v2.0, 2026-08-07, fetched live). The appendix page was not saved or read.
Source: [blog](https://wenwen-d.github.io/blog/harness-delta-attribution/).
Wenxuan Ding, Qin Lu, Changlong Yu, Sha Li, Shuowei Jin, Xin Liu, Greg
Durrett. Blog post, August 2026; not peer-reviewed.

**What it is.** A decomposition of an evolved harness E's gain over baseline
B, scored on *one* evaluation set, into three terms that sum exactly to
S(E) − S(B):
- **T** = S(B_cc) − S(B). B_cc is the baseline at E's per-item budget,
  measured in executor calls, samples, or tool steps: self-consistency for
  separable metrics, pool-then-rescore for pooled ones.
- **O** = S(E) − S(E_neutral). E_neutral is E with detected shortcuts
  removed by the smallest edit that sends each decision back to a live
  model call.
- **G** = S(E_neutral) − S(B_cc), the residual.

O is a lower bound and G an upper bound. The procedure has five steps:
1. A paired-bootstrap significance gate on ΔS (no bar if the CI contains 0,
   with a winner's-curse warning if the eval set is the selection set).
2. A fresh baseline rerun, whose gap from the recorded baseline sets a
   sensitivity band.
3. Shortcut discovery from code: never-invoked model calls, lookup tables
   keyed on items, item-ID gates, string-match early returns, and distilled
   prompt recipes.
4. Neutralization, using stub-free edits marked in the code plus a shift
   that renames or permutes memorized keys.
5. Two human approvals: the compute-match plan and the neutralization diff.

For artifacts with no code line to cut, the eval set is split into
artifact-bearing and clean items (the "meta-split"). Shares are
|X|/(|O|+|T|+|G|), never divided by ΔS, and each comes with a per-item
gained/lost ledger.

**Anti-overfitting / generalization evidence.** The evolution loop is
Meta-Harness with Claude Code (Opus 4.8) as proposer. Train results give full
trajectories and per-item scores; val gives aggregate scores only. Train- and
val-selected winners are then tested once on held-out test. Across 16
settings, test gains are much smaller than train gains. In 4/16 the
train-selected harness is below baseline on test. Val selection helps
little: +8.0 (ALFWorld), +0.8 (LiveMath), +8.0 (SWE-bench Verified), −0.4 CU
(CREATE) over train selection, and still 5.9/11.7/9.3 pp and 9.3 CU below
the training gains.

**Edit categories found (with examples).**
- *Overfitting*:
  - Executor bypass. ALFWorld winners make zero LLM calls, running a 44–47
    key object→location prior plus regex task parsers the proposer knew
    from pretraining.
  - Dataset-artifact string match. On LiveMath, "a stronger result can be
    proven" is gold on 21/35 train items.
  - Soft behavioural artifact. Larger models prefer the hedge option with
    no lexical trace; a code-only check first scored these gains 71–90%
    genuine.
  - Statistics measured from the benchmark. A SWE-bench "patch is LARGE"
    threshold (adds ≥ 12, deletes ≥ 8) was booked as O.
  - Distilled prompt recipes.
- *Test-time scaling*: CREATE's 20-frame parallel generation and voting,
  retries, and verification passes.
- *Generalizable*: on SWE-bench, edit-effect feedback, a block editor, an
  undefined-name guard, and telling the model only its first action block
  ran.

**Evidence and regime.** Executors are Qwen 0.8B–122B and Claude Haiku 4.5;
30–40 iterations; one evolution run per setting. Split sizes are small:
LiveMath train 35; ALFWorld train 50; SWE-bench train/val/test 48/24/50.
- ALFWorld: O 98 / T 0 / G 2 (ΔS-weighted over 5 models). 8B neutralized
  1.00 → 0.32, exactly the baseline.
- LiveMath: O 79 / T 10 / G 11. The 0.8B model goes 2/35 → 29/35, with 20
  of the 27 added correct answers on meta-option items.
- CREATE: T 73 / G 27. Haiku splits T 49 / G 51. For Qwen-35B the
  call-matched baseline beats E (18.74 vs 11.90 CU; G_raw −6.8).
- SWE-bench:
  - Qwen3-4B val-selected: test 4 → 22%; O 15 / T 23 / G 62; train
    p = 0.003.
  - 30B-A3B: test 12 → 26% (val-selected 36%); O 0 / T 6 / G 94.
  - 27B: train 77 → 85%, test 66 → 64%.
  - Coder-30B: train 56 → 69%, test 40 → 34%.
- The draft payload shows pending and replaced numbers: an earlier SWE-bench
  split was withheld, and a text-classification case with a crash-averaging
  scoring bug (86% headline, ~57% true) was dropped from the post. Grade:
  `single-source`.

**Bearing on RRSI and on memorization.** This is the strongest direct
evidence for the user's suspicion. Most search-split gains are overfitting
or bought compute. A near-zero O does not mean transfer: the SWE-bench 27B
and Coder-30B runs book as 100% G yet regress on test, because fitting the
selection set is invisible inside a one-set decomposition. RRSI's mechanisms
map onto HDA terms:
- The leakage critic that reads diffs matches HDA's code-side detection,
  which missed the soft artifacts.
- The token-cost rule addresses T only.
- The noise-band floor matches HDA's rerun band and gate.

None of these addresses selection-set fit. Only held-out evaluation does,
and val gating recovered little. The data payload also reports that
aggregate-only proposer feedback correlated with less hacking. That
observation is unpublished.

**Relation to a practitioner-maintained instruction corpus.** HDA's
neutralization is clause-level ablation. It swaps one shortcut region, or
one distilled prompt passage, for the baseline's generic form, changes
nothing else, and re-scores. A human approves the diff. That is the
mechanics the repo's planned clause-cited attribution needs. Its rerun
sensitivity band is the repo's same-model noise floor, and its signed
gained/lost ledger fits the append-only evidence ledger. Three cautions
carry over:
- Attribution by reading text misses behavioural artifacts; partition the
  cases the clause could touch.
- "Survives ablation" does not mean "transfers"; incident-derived clauses
  need out-of-incident checks.
- The 4c judgment of general versus benchmark-specific guidance is exactly
  where incident-driven clauses risk encoding the incident itself.
