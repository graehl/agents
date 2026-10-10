# LLM compute in fuzzing: drivers and input generation

> Read-backed digest (cluster C, trust `single-source`). Three uses of LLM
> compute: writing fuzz drivers (harnesses) for library APIs, generating
> inputs for language-consuming systems, and full LLM-plus-fuzzing
> vulnerability systems in the DARPA AIxCC final. Cen Zhang is first author of
> both the driver study and the AIxCC SoK. The SoK's reference fuzzer and
> patch agent come from the winning team's open-source system, "atlantis" /
> OSS-CRS.

## LLM-generated fuzz drivers (Zhang et al.)

**Paper.** Cen Zhang, Yaowen Zheng, Mingqiang Bai, Yeting Li, Wei Ma, Xiaofei
Xie, Yuekang Li, Limin Sun, Yang Liu, "How Effective Are They? Exploring Large
Language Model Based Fuzz Driver Generation," ISSTA 2024
([arXiv](https://arxiv.org/abs/2307.12469),
[PDF](https://arxiv.org/pdf/2307.12469),
[local extract](../related-work/extract/zhang2024-llm-fuzz-driver/html/2307.12469.md)).

### Method

The benchmark has 86 driver-generation questions, one per core API, taken from
30 OSS-Fuzz C projects. It crosses 6 prompting strategies with 5 models
(gpt-4-0613, gpt-3.5-turbo-0613, text-bison-001, codellama-34b, wizardcoder-15b)
and 5 temperatures. In total the study generates 736,430 drivers using 0.85B
tokens (more than $8,000 of charged tokens). A driver counts as effective if it
compiles, gains coverage in a one-minute seedless run, and either reports no
bugs or only bugs matching a filter of true bugs. That filter comes from 10
CPU-days of OSS-Fuzz fuzzing. Handwritten API-specific semantic checks catch
misuse such as fuzzing a filename instead of file contents. The field
comparison against OSS-Fuzz drivers uses 38 merged drivers for 53 questions.
It runs libFuzzer and AFL++ for 24 h with 5 repetitions, 3.75 CPU-years in
total.

### Evidence

- The best configuration (gpt-4, iterative, temperature 0.5) solves 78 of 86
  questions (91%). Solving means at least one effective driver among up to 40
  repeated attempts. A naive single query solves about 10%.
- Cost: 45% of solved questions need 10 or more full query rounds per
  effective driver. Example snippets roughly double the questions solved but
  multiply tokens by about 14.65× on average (about 32k tokens per correct
  driver). Iteration adds 159% more solved questions over the basic prompt at
  +57% tokens. Returns from repetition drop after about 6 rounds.
- Limits: 29 of 86 APIs (34%) need semantic checks that cannot be automated,
  and without those checks fuzzing floods with false positives. Five
  questions are unsolved because they need complex context, such as a running
  server.
- Against OSS-Fuzz's human drivers, coverage and unique crashes are "similar or
  better" for most questions. The comparison has caveats: it covers only
  questions every configuration solved, it uses unique crashes, a metric
  Schloegel et al. reject, and it uses 5 repetitions. LLM drivers contained no
  semantic oracles, while OSS-Fuzz drivers had them for 15 questions. Some
  LLM drivers called fewer project APIs: 14% of gpt-4 drivers and 39% of
  wizardcoder drivers.

## Fuzz4All: LLM as a universal input generator

**Paper.** Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel,
Lingming Zhang, "Fuzz4All: Universal Fuzzing with Large Language Models," ICSE
2024 ([arXiv](https://arxiv.org/abs/2308.04748),
[PDF](https://arxiv.org/pdf/2308.04748),
[local extract](../related-work/extract/xia2024-fuzz4all/html/2308.04748.md)).

### Method

GPT-4 distils user documentation into candidate prompts ("autoprompting"),
and the prompt with the most valid generated inputs is kept. StarCoder then
generates inputs in a loop. Each round adds a previous valid input and one of
three instructions (generate new, mutate, or rewrite into a
semantically equivalent form). Oracles are mainly crashes. Systems under test
span six languages (GCC/Clang, G++, CVC5/Z3, Go, javac, Qiskit), each compared
with a language-specific fuzzer (GrayC/Csmith, YARPGen, TypeFuzz, go-fuzz,
Hephaestus, MorphQ). Runs last 24 h with 5 repetitions and a Mann-Whitney U
test. Each Fuzz4All run uses one RTX A6000 GPU, and the paper does not
normalize compute against the CPU-only baselines.

### Evidence

- Line coverage after 24 h is higher on all six coverage targets, by 13.7% (Go)
  to 75.6% (Qiskit), 36.8% on average over the best baseline. Fuzz4All keeps
  gaining coverage at 24 h while the baselines plateau.
- It does this with 56% lower validity and 43% fewer inputs, because GPU
  inference is the bottleneck.
- Targeted prompts reach an 83% average hit rate on a chosen feature, against
  near zero for general fuzzing. For newly added Qiskit features, general
  fuzzing had a 0% hit rate.
- It found 98 bugs, of which developers confirmed 64 as previously unknown. The
  examples include features older generators do not support, such as C++
  `noexcept` and Go's `runtime` package, which is outside go-fuzz's templates.
- In the ablation, autoprompting beats both the raw documentation and an empty
  prompt, and the full loop beats sampling from a fixed prompt.

## AIxCC final: LLM-heavy systems against a plain-fuzzing reference

**Paper.** Cen Zhang, Younggi Park, Fabian Fleischer, Yu-Fu Fu, Jiho Kim,
Dongkwan Kim, Youngjoon Kim, Qingxiao Xu, Andrew Chin, Ze Sheng, Hanqing Zhao,
Michael Pelican, David J. Musliner, Jeff Huang, Jon Silliman, Mikel Mcdaniel,
Jefferson Casavant, Isaac Goldthwaite, Nicholas Vidovich, Matthew Lehman,
Taesoo Kim, "SoK: DARPA's AI Cyber Challenge (AIxCC): Competition Design,
Architectures, and Lessons Learned," USENIX Security 2026
([arXiv](https://arxiv.org/abs/2602.07666),
[PDF](https://arxiv.org/pdf/2602.07666),
[local extract](../related-work/extract/zhang2026-aixcc-sok/zhang2026-aixcc-sok.md)).

### Method

In the August 2025 final, seven autonomous cyber reasoning systems ran for
about 143 h on 48 scored OSS-Fuzz-based challenge projects (24 repositories,
C and Java). The projects contained 63 injected vulnerabilities, mostly
hand-crafted synthetics. Each team had $85K of Azure compute and $50K of LLM
credit. 16 projects were full-mode, with bugs anywhere in the repository; 32
were delta-mode, with bugs inside a pull-request diff. The SoK draws on team
code, the organizers' database and team interviews. It labels each
vulnerability with lab reference runs. For finding bugs the reference is
plain parallel fuzzing: OSS-Fuzz configurations, 16 cores per harness, up to
6 h per harness, union of 3 runs, 8,906 CPU-hours. For patching, the
references are a minimal patch agent and Claude Code.

### Evidence

- **Plain fuzzing alone** finds 34 of 63 vulnerabilities: 30 of 40 in C but 4
  of 23 in Java. The paper attributes the Java gap to semantically constrained
  inputs, timeout and out-of-memory bugs, and weak default seeds.
- **What the systems added.** Six systems each solved 7–16 vulnerabilities that
  the fuzzing reference missed, 22 in total (8 C, 14 Java). Fifteen of the 22
  were delta-mode: the systems read the diff and wrote triggering inputs. The
  two teams that also ran classic directed fuzzing found no delta-mode bug
  that teams without it missed. The other additions were grammar-conforming
  inputs (TLV, PDF/XFA, XLSX) and solving logical guards such as regexes,
  encodings and compression. The paper attributes these gains mainly to LLM
  components, by inference: three teams' bug-finding was basic parallel
  fuzzing plus LLMs, and all three solved cases the reference missed.
- **What they missed.** Systems also failed on cases plain fuzzing solves,
  because of pipeline breakage: non-standard harnesses, about 1 TB of
  wireshark build output, single-run reproduction of stateful bugs, wrong
  sanitizer, coarse deduplication. The score gap is mostly stability. The
  winner had 392.8 points, nearly 80% above second place, and two teams
  plateaued after a disk-heavy project. A system that applied the reference
  techniques reliably would have placed in the top three.
- **Compute and LLM spend.** No team used its full quota. Azure spend ran
  $7.1K–$73.9K and LLM spend $0.6K–$29.4K, about 94% of it on Anthropic and
  OpenAI. LLM spend rank closely tracks final score. On score per $1K, the
  winner ranks third (3.80), behind two teams with mid-size LLM budgets and
  small Azure spend (6.63 and 5.54).
- **Patching.** The patch agents pass automatic validation yet are
  semantically wrong 38–46% of the time. The higher-accuracy systems are
  wrong 16–21% of the time.
- **No ablation.** The authors list the lack of a controlled ablation as a
  limitation, citing the cost of migrating the systems onto one platform. The
  paper does not separate LLM contribution from engineering under equal
  compute.

## Decision edge and limits

- **Where LLM compute buys reach.** It helps where plain fuzzing cannot start
  or stalls. It writes harnesses that would otherwise cost an expert's time,
  and it generates structured inputs for new or rarely seen language features,
  where grammar or template fuzzers have no coverage. Both are diversity gains
  across targets and features. Each opens a new cheap region of the
  diminishing-returns curve rather than pushing one saturated target further.
  AIxCC adds a third case: reading a diff and writing a triggering input. This
  accounts for most of what LLM-heavy systems found beyond plain fuzzing, and
  classic directed fuzzing added nothing there. That bears directly on
  change-directed CI fuzzing (see `change-directed-fuzzing.md`).
- **Where plain fuzzing already suffices.** On C memory bugs with OSS-Fuzz
  harnesses, plain parallel fuzzing found three quarters of AIxCC's injected
  vulnerabilities. There, LLM budget pays off less than pipeline robustness
  does: builds, sanitizers, reproduction and deduplication.
- **Where it does not.** Per-input throughput is far lower than coverage-guided
  byte mutation. Neither paper shows LLM generation beating a modern greybox
  fuzzer on a target that already has a good harness, and neither tried.
  Driver generation still needs a human or a semantic check to reject API
  misuse before fuzzing compute is spent.
- **Cost accounting is incomplete.** Zhang et al. report tokens and dollars;
  Fuzz4All reports GPU-hours only implicitly (one GPU per run). Neither reports
  bugs per dollar against a CPU-equal baseline. Under Schloegel et al.'s
  fairness rule, the coverage gains are measured at unequal compute. AIxCC
  reports dollars per team, but its fuzzing reference ran in the lab (16
  cores per harness, unscored, outside the competition). Its "systems
  minus reference" counts compare systems against a configuration, not an
  ablation.
- **AIxCC regime.** The vulnerabilities are mostly synthetic, injected into
  projects that already have harnesses. Delta diffs that contain a
  vulnerability are small (163–1,407 lines). Each team had about $135K and 143
  h. These conditions favour diff reading more than ordinary pull-request
  traffic would.
