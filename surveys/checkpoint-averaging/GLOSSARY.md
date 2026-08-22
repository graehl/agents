# Glossary — surveys/checkpoint-averaging

Survey-scoped vocabulary. Applies by path to this survey, its concept pages,
and related-work material.

| term | definition | ref |
|---|---|---|
| checkpoint average | A parameter-wise combination of saved states, usually from one training trajectory; the unqualified default in this survey is an equal-weight mean | [recipes](survey.md#recommended-recipes) |
| eligible-tail mean | A uniform mean over a contiguous late window after checkpoints failing predeclared hard health gates are removed | [R1](survey.md#r1-existing-close-checkpoints-eligible-tail-mean) |
| averaging horizon | The represented amount of optimizer time or data exposure; for a window it is checkpoint interval times window length, and for EMA it is summarized by an effective half-life | [R2](survey.md#r2-future-online-run-ema-plus-uniform-tail-control) |
| stochastic weight averaging (SWA) | Post-convergence training with a constant or cyclic learning rate plus a uniform mean of sampled trajectory points | [trajectory averaging](concepts/trajectory-averaging.md) |
| exponential moving average (EMA) | An online recursively updated parameter average whose ingredient weights decay geometrically with age | [exponential averaging](concepts/exponential-averaging.md) |
| latest weight averaging (LAWA) | A uniform rolling mean of the latest fixed number of saved checkpoints | [latest window](concepts/latest-window.md) |
| model soup | A parameter average of models fine-tuned from a shared initialization, either uniform or selected by a disjoint validation rule | [model soups](concepts/model-soups.md) |
| interpolation barrier | A material loss or error increase along the straight parameter path between two endpoints; evidence that a raw mean may be unsafe | [divergent merging](concepts/divergent-merging.md) |
| logit ensemble | An output-space combination of several models' logits or probabilities, preserving inference cost but avoiding an assumption that parameters are aligned | [trajectory geometry](concepts/trajectory-geometry.md) |
| health gate | A predeclared binary eligibility rule for excluding corrupt, discontinuous, off-contract, or objectively bad checkpoints before equal-weight averaging | [health](survey.md#checkpoint-health-and-weighting) |
| `[G]` | The cited primary full text was fetched and read for this survey | [grounding](survey.md#grounding-and-coverage) |
