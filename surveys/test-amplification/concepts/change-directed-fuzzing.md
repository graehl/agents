# Change-directed and continuous fuzzing

> Read-backed digest (cluster C). Trust: the OSS-Fuzz field statistics (RGF,
> Shirai) are `single-source` but come from large populations. The claim that
> "directed beats undirected" is `contested`: AFLGo and AFLChurn report gains
> over AFL, while LibAFLGo's re-implementation finds no overall gain over
> modern LibAFL.

## AFLGo: directed greybox fuzzing

**Paper.** Marcel Böhme, Van-Thuan Pham, Manh-Dung Nguyen, Abhik Roychoudhury,
"Directed Greybox Fuzzing," ACM CCS 2017
([PDF](https://mboehme.github.io/paper/CCS17.pdf),
[local extract](../related-work/extract/bohme2017-aflgo/bohme2017-aflgo.md)).

### Method

At compile time AFLGo computes each basic block's distance to the target
locations, such as the lines a patch changed. It uses a call-graph distance
plus distances inside each function, avoiding a whole-program control-flow
graph. At run time, a simulated-annealing schedule built on AFL 2.40b
gradually shifts fuzzing energy toward seeds whose traces lie closer to the
targets. Evaluations: patch testing against the symbolic-execution tool KATCH
on its benchmark (Binutils/Diffutils), crash reproduction against AFL (20
runs, 8-h timeout, timeouts scored as 8 h) and BugRedux, and an OSS-Fuzz
integration aimed at recent commits.

### Evidence

- Heartbleed commit: about 19 min mean time to exposure over 30 runs; KATCH did
  not expose it in a day.
- Patch coverage: 223 against 198 changed basic blocks not previously covered
  (13% more than KATCH). The overlap is small, and together they cover 42% more
  than KATCH alone. AFLGo ran on 1 core against KATCH's 4. AFLGo found 13 new
  bugs (7 CVEs) on that benchmark.
- Against undirected AFL, crash reproduction was 3–11× faster on three libpng
  CVEs and 1.5–2× faster on most Binutils CVEs. One case was slower (0.64×) and
  two were not significant. Mean Vargha-Delaney A12 was 0.66.
- OSS-Fuzz integration aimed at recent commits found 26 bugs (10 CVEs),
  including incomplete fixes in libxml2 and libming.

## Regression greybox fuzzing (AFLChurn) and OSS-Fuzz regression statistics

**Paper.** Xiaogang Zhu and Marcel Böhme, "Regression Greybox Fuzzing," ACM
CCS 2021 ([PDF](https://mboehme.github.io/paper/CCS21.pdf),
[local extract](../related-work/extract/zhu2021-regression-greybox/zhu2021-regression-greybox.md)).

### Method

The empirical part mines 22,582 (about 23k) fuzzer-reported bugs from 376
OSS-Fuzz projects. A bug counts as a regression when OSS-Fuzz's bisection
identified a bug-introducing commit. AFLChurn fuzzes *all* commits at once
with no single target. Every basic block is weighted by recency (inverse age
from `git blame`) and churn (log of change count). A simulated-annealing
schedule favours seeds that run high-weight code, and an ant-colony schedule
learns which input bytes to mutate. Evaluation is in FuzzBench on 15 OSS-Fuzz
C programs with one known regression each, taken at the revision just before
the fix. Baseline is AFL; 20 trials of 23 h each; over 3 CPU-years in total.

### Evidence

- 77.2% of bug reports are regressions. The share rises from 20.2% for a
  project's first report to over 99% by the 1000th; the abstract says 92%
  "after a few hundred". Mean time from bug-introducing commit to report is 68
  days (median 5). Only 23% are foundational, meaning no introducing commit
  was found.
- After onboarding, reports arrive at about 2.5 per day. They then drop to a
  steady 3.5 per week, almost all regressions.
- AFLChurn reaches regressions about 1.5× faster than AFL on the 8 informative
  subjects; one case drops from 17 h to 9 h. Two bugs are found only by
  AFLChurn, and median gaps favour AFLChurn on 16 of 19 regressions. Three
  subjects crash under neither fuzzer, and four crash before AFL's first queue
  cycle, which gives guidance no room to help. The "20 bugs" include 8 that
  were not targeted.
- Neither recency nor churn alone dominates. AFLGo could be built for only 3 of
  the 15 subjects, so the directed comparison is a case study.

## LibAFLGo: re-evaluating directed fuzzing on a modern stack

**Paper.** Elia Geretto, Andrea Jemmett, Cristiano Giuffrida, Herbert Bos,
"LibAFLGo: Evaluating and Advancing Directed Greybox Fuzzing," IEEE EuroS&P
2025 ([PDF](https://download.vusec.net/papers/libaflgo_eurosp25.pdf),
[local extract](../related-work/extract/geretto2025-libaflgo/geretto2025-libaflgo.md)).

### Method

The authors reimplement the AFLGo, Hawkeye and DAFL policies on LibAFL with
in-process fuzzing, a common analysis stack (SVF) and link-time analysis, and
compare them with undirected LibAFL and Beacon. Time to exposure *includes
build time* and is analysed as censored data: Kaplan-Meier median survival,
log-rank tests and Cox hazard ratios. Benchmark: 40 MAGMA harness-bug pairs,
24 h, 16 repetitions, one core each. Builds use -O0 because MAGMA breaks at
-O3, and ASan stack instrumentation is off.

### Evidence

- LibAFLGo shortens median survival significantly in 1 case and lengthens it in
  6. Some of the losses are build-time cost on bugs found in seconds.
- Heavy analysis costs hours of build time: LibDAFL takes 3.4–3.9 h on php,
  and Beacon takes 35–40 h on openssl. That erases the gains except on small
  projects (libsndfile). There are isolated large wins, such as LibAFLGo 4.65×
  on SSL020 and LibDAFL 87× on PDF018.
- Conclusion: no directed policy beats LibAFL overall. LibAFL performs on par
  with the best directed fuzzer and needs no rebuild per target.
- Prior directed papers handle timeouts by imputing the cap or dropping cases,
  omit build time, and compare against AFLGo-era baselines (their Tables 1–2).
- Possible bias: bugs were admitted only if LibAFL reached them in 7-day runs,
  so targets that only a directed fuzzer reaches are excluded by design.

## Continuous fuzzing at scale (Shirai et al.)

**Paper.** Tatsuya Shirai, Olivier Nourry, Yutaro Kashiwa, Kenji Fujiwara,
Yasutaka Kamei, Hajimu Iida, "Large-Scale Empirical Analysis of Continuous
Fuzzing: Insights from 1 Million Fuzzing Sessions," IEEE TSE 2025
([arXiv](https://arxiv.org/abs/2510.16433),
[PDF](https://arxiv.org/pdf/2510.16433),
[local extract](../related-work/extract/shirai2025-continuous-fuzzing-1m/html/2510.16433.md)).

### Method

The study mines OSS-Fuzz from March 2017 to January 2025: 3.95M build logs,
1.04M coverage reports and 72,660 issues, covering about 1.12M sessions across
878 projects with at least a year of history. Default sessions last about 10
minutes, roughly once a day. The bug-detection rate per session index is the
share of projects reporting a bug in that session. The coverage-change
analysis uses only the 5,465 reports whose revision matches a coverage report.

### Evidence

- 36% of projects report a bug in their first session and 20% in their second.
  The rate falls below 5% at session 26, then holds near a median of 2.19% for
  thousands of sessions. The paper infers that many bugs predate onboarding.
  That is an inference from the first-session rate; no commit bisection backs
  it. It agrees with RGF's 20% regression share for first reports.
- Median coverage rises with session count (aggregate Spearman 0.962), but the
  per-project median correlation is only 0.006, partly because codebases grow.
- Bug-finding sessions show coverage change more often: 51.6% increased and
  27.9% decreased, against 20.6% and 18.4% in sessions without bugs. This is
  an association; the paper does not test causation.

## Decision edge and limits

- **Where marginal bugs live.** On a well-fuzzed project, nearly every new
  report is a regression, and onboarding yields a burst that decays within
  about 25 daily sessions. Steady-state continuous-integration (CI) fuzzing
  budget should therefore follow recent change. Pay the up-front burst when
  onboarding a new target, which is the cheap region of the Böhme & Falk
  curve.
- **How to follow change.** Commit-weighted fuzzing (AFLChurn) needs no
  per-commit rebuild and showed about 1.5× faster regression discovery, but
  only against old AFL. Per-target directed fuzzing pays a rebuild for every
  target, and on a modern in-process stack it has not shown a net gain once
  build time counts. A cheaper default is to rerun an undirected modern fuzzer
  on the changed build with a seeded corpus, and to direct only when a cheap
  target is known, such as an incomplete-fix site or a crash stack.
- **What is not measured.** No study here compares commit-weighted fuzzing
  with a modern undirected baseline, and none prices CI minutes against bugs
  found. Shirai's recommendation to scale fuzzing time with diff size is not
  yet tested.
