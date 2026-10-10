# Predicting or pre-selecting mutants instead of running them

> Read-backed digest (cluster B, trust `contested` for PMT's cross-project
> accuracy: an independent replication finds that the headline AUC mostly
> comes from trivially predictable uncovered mutants. Contextual PMT and
> Cerebro are `single-source`).

**Paper.** Zhang, Zhang, Harman, Hao, Jia, Zhang, "Predictive Mutation
Testing," IEEE TSE 2018; journal extension of the ISSTA 2016 paper
([PDF](https://discovery.ucl.ac.uk/10051793/1/bare_adv.pdf),
[local extract](../related-work/extract/zhang2018-predictive-mutation/zhang2018-predictive-mutation.md)).

**Paper.** Aghamohammadi, Mirian-Hosseinabadi, "The Threat to the Validity of
Predictive Mutation Testing: The Impact of Uncovered Mutants," arXiv 2020
([arXiv](https://arxiv.org/abs/2005.11532),
[PDF](https://arxiv.org/pdf/2005.11532),
[local extract](../related-work/extract/aghamohammadi2020-pmt-threat/html/2005.11532.md)).

**Paper.** Jain, Alon, Groce, Le Goues, "Contextual Predictive Mutation
Testing," ESEC/FSE 2023
([arXiv](https://arxiv.org/abs/2309.02389),
[PDF](https://arxiv.org/pdf/2309.02389),
[local extract](../related-work/extract/jain2023-contextual-pmt/html/2309.02389.md)).

**Paper.** Garg, Ojdanic, Degiovanni, Chekam, Papadakis, Le Traon, "Cerebro:
Static Subsuming Mutant Selection," IEEE TSE 2022
([arXiv](https://arxiv.org/abs/2112.14151),
[PDF](https://arxiv.org/pdf/2112.14151),
[local extract](../related-work/extract/garg2022-cerebro/html/2112.14151.md)).

## Method

### PMT (Zhang et al.)

A random forest predicts whether each mutant is killed or survives, without
running it. Its 14 features cover execution (how often the mutated
statement runs, how many tests cover it), infection (statement and operator
type), propagation (complexity and coupling metrics) and oracles (assertion
counts) (lines 83-126). Training data comes from earlier versions of the
same project (cross-version) or from other projects (cross-project). The
evaluation uses PIT mutants on 9 base projects plus 154 GitHub projects
(lines 160, 208-212). Uncovered mutants stay in the data.

### The uncovered-mutant check (Aghamohammadi)

The authors repeat the cross-project procedure of Mao et al.'s 654-project
PMT extension (95 features, random forest) and score it on covered mutants
only. 66 projects are held out for testing (lines 66, 85). They then
propose ADASYN rebalancing plus a random forest averaged with 50 gradient
boosters, trained on covered mutants only (lines 97-99).

### MutationBERT (Jain et al.)

CodeBERT is fine-tuned on (mutated method as a token-level diff, test
method) pairs to predict a kill bit for each pair, which builds the full
mutant-test matrix. A mutant counts as detected if any test that covers it
scores above 0.25 (lines 145-166). Uncovered mutants are dropped beforehand
by a coverage check, following Aghamohammadi (line 137). The data is
Seshat's Major-on-Defects4J-2.0 set: 6 projects, covered mutants only
(line 263).

### Cerebro (Garg et al.)

An encoder-decoder translation model reads abstracted code around each
mutation point (identifiers and literals replaced by placeholder names,
50 or 100 tokens) and appends a label: subsuming or not. Subsuming mutants
sit at the top of the subsumption hierarchy, so tests that kill them kill
everything below (lines 30, 158-170). The labels come from complete
mutant-test kill matrices built from large test pools: KLEE and SEMu for
48 C Coreutils programs, EvoSuite and PIT run for 48 hours per project for
10 Java projects (lines 311-319). Evaluation is inter-project 5-fold
(line 543). The baselines are random sampling and a gradient-boosted tree
on 28 or 16 hand-made features (line 503).

## Evidence

### PMT

Cross-version prediction reaches above 0.90 on all four metrics for 37 of
39 version pairs. Cross-project AUC exceeds 0.85 for 144 of 163 projects.
Mutation-score error is under 15% for 143 of 163 (line 39). The baseline for
speed is PIT in its default mode, which stops running tests on a mutant
once it is killed. Against that, PMT is 15.2x to 151.4x faster: for
commons-lang, 9,540 s with PIT against 63 s with PMT, nearly all of which
is feature collection (Table 4, lines 374-387).

Predicting the mutation score from statement coverage alone has errors up
to 14.6%, against at most 3.9% (cross-version) and 10.2% (cross-project)
for PMT (line 394). The coverage features are the most informative, and
removing the execution features costs the most (lines 456, 508). The paper
notes that uncovered mutants are trivially predictable (line 550).

### The uncovered-mutant check

62% of the mutants in Mao's dataset are never executed: 1,894,940 against
1,137,336 that are (lines 74-81). On covered mutants alone, PMT's AUC falls
from a median of 0.833 to 0.516, and from a mean of 0.814 to 0.540. On 18 of
66 test projects (27%) it does worse than random guessing, and only 5
projects exceed 0.6 (line 179). The proposed ensemble reaches a mean AUC of
0.613, a median of 0.609, and beats random on every test project
(line 192). Its MCC is 0.239 against 0.138 (Table 4, lines 214-219).

### MutationBERT

On the same-project test split (195,140 mutant-test pairs), the
pair-matrix F1 is 0.75 against Seshat's 0.67. At the suite level, with
undetected mutants as the positive class, precision is 0.81 against 0.56
and F1 0.79 against 0.67. Cross-project, suite-level F1 is 0.58 against
0.30 (Table 3, lines 294-347). The estimated mutation score is 0.61 against
a true 0.59, where Seshat estimates 0.40 (line 358).

Inference takes 34 ms per pair on an RTX 3080 and 84 ms on a CPU
(lines 749, 783). Full Major runs take between 1,290 and 113,343 s per
project. Prediction alone takes 36 to 1,424 s. If each predicted-surviving
mutant is confirmed by actually running it, MutationBERT's total ranges
from 542 to 33,035 s (Table 7, lines 680-746). With that confirmation step
it saves 71% of the time of regular mutation testing, against Seshat's 57%
(line 779). On hard mutants, killed by 1-20% of tests, its accuracy is 30%
higher than Seshat's (line 771).

### Cerebro

Precision is 0.85, recall 0.33, MCC 0.46. MCC is 2.76x (C) and 2.81x
(Java) that of the feature-based tree (lines 34, 41). In a simulated tester
loop with the same number of selected mutants, the subsuming mutation score
is:

- C: 87.5% for Cerebro, 2.39x the tree and 2.63x random;
- Java: 95.9% for Cerebro, 2.0x the tree, 1.70x random (lines 742-744).

Equivalent mutants make up 1.1% of Cerebro's selections against 24-26% for
the baselines on C (line 748). Reaching the same subsuming score takes 291
test executions against 3,149-3,345 for the baselines on C, and 65,741
against 517,040-795,304 on Java (lines 811-812).

Training the 100-token model took 740 GPU-hours on a V100, and the 50-token
model 360 (line 265). At inference, preprocessing and classification take
about 5 minutes each (line 1042).

## Decision edge and limits

These papers address framing (c), replacing "run the whole suite on every
mutant" with prediction or pre-selection. They also show that framing (a)'s
cheap step, dropping uncovered mutants by coverage, is where much of the
apparent prediction skill comes from. Aghamohammadi's check implies the
coverage filter should run first and for free. Prediction on covered
mutants is then a hard problem for metric features (AUC about 0.5-0.6) and
only moderately solved by code-plus-test language models
(F1 0.75-0.79 within a project, 0.48-0.58 across projects).

Prediction pays off for estimating the mutation score and for ranking which
mutants to execute. Surfacing individual surviving mutants still needs
confirmation runs, and those dominate the cost: 33,035 s against 809 s
without checking on jackson-core. A practical design is therefore: predict,
then run only the few tests predicted to kill each mutant, the use Jain et
al. propose for the matrix (line 39). That is test selection for mutants.

Cerebro moves the saving earlier, choosing which mutants to *generate and
execute* from local syntax alone. In simulation it cut test executions by
about 90%. But its labels need exhaustive kill matrices, and in this
evaluation it ran inter-project within one benchmark family, C Coreutils or
10 Java libraries. Transfer to other codebases is untested.

None of the four papers measures schemata or split-stream execution
(framing b). Jain et al. mention meta-mutation and schema generation only as
related cost-reduction ideas (line 797).

Limits. PMT and Aghamohammadi both evaluate on Java with PIT and are
`contested` on exactly the setting that matters, covered mutants across
projects. The Aghamohammadi paper is an unreviewed preprint. Jain et al.
evaluate on single versions of 6 Defects4J projects. Cerebro's
"2x" holds against the learned baseline but is about 1.7-1.8x against
random selection on Java.
