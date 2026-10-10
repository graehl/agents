# test-amplification glossary

Survey-scoped vocabulary; governs every document under
`surveys/test-amplification/`.

| term | definition | topic / refs |
|---|---|---|
| change-aware testing | Spending test, mutation, fuzzing or generation compute in proportion to its relation to a specific code change (diff, commit, review), rather than uniformly over the codebase | [survey](survey.md) |
| commit-relevant mutant | A mutant whose behaviour interacts with a commit's change: killing or surviving it depends on the changed code, even if the mutant is not located on the diff (Ma et al. 2020) | [survey § B](survey.md#b-targeted-and-cheaper-mutation-testing) |
| arid line | Google's term for a line whose mutants developers judge uninteresting (logging, boilerplate, configuration); excluded before mutating | [targeted mutation](concepts/targeted-mutation.md) |
| predictive mutation testing (PMT) | Predicting whether a mutant would be killed without executing it, from static and coverage features | [targeted mutation](concepts/targeted-mutation.md) |
| subsuming mutant | A mutant whose kill implies kills of other mutants; the non-redundant top of the subsumption hierarchy | [targeted mutation](concepts/targeted-mutation.md) |
| regression test selection (RTS) | Running only the tests whose dependencies a change touched; "safe" RTS guarantees no change-relevant test is skipped under its dependency model | [test selection](concepts/test-selection.md) |
| predictive test selection | Learning, from historical test outcomes, which tests a change is likely to fail, and running only those; trades a small failure-recall loss for large compute savings | [test selection](concepts/test-selection.md) |
| transition | A test's status changing between consecutive runs (pass→fail or fail→pass); the event Google's selection and speculative-testing work predicts | [test selection](concepts/test-selection.md) |
| directed greybox fuzzing | Coverage-guided fuzzing whose power schedule favours seeds estimated to be close to chosen target locations, such as changed code | [change-directed fuzzing](concepts/change-directed-fuzzing.md) |
| power schedule | The rule assigning how many mutated inputs (energy) a fuzzer derives from each seed; the within-campaign compute-allocation knob | [payoff curves](concepts/fuzzing-payoff-curves.md) |
| residual risk | The probability that the next generated input discovers something new (a bug or coverage element), estimated to decide when to stop a campaign; in practice estimated through the discovery probability that bounds it | [payoff curves](concepts/fuzzing-payoff-curves.md) |
| hardening test | A generated test that passes on current code and protects against future regressions (Meta's term) | [agent-written tests](concepts/agent-written-tests.md) |
| catching test | A generated test intended to fail on a pending change, revealing a bug before it lands (Meta's term) | [agent-written tests](concepts/agent-written-tests.md) |
| reproduction test | A test generated from an issue report that fails before and passes after a correct fix (fail-to-pass) | [agent-written tests](concepts/agent-written-tests.md) |
| test overfitting | A patch that passes the tests used during repair but fails held-out tests of the same intended behaviour | [agent-written tests](concepts/agent-written-tests.md) |
| test amplification | Automatically deriving new tests from existing ones (new inputs, new assertions, new targets) to strengthen a suite; the field term of Danglot et al. 2019 | [survey](survey.md) |
