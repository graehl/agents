# Citation retrieval evidence

Retrieved and checked on 2026-10-17. Coverage is specified per entry: primary
abstracts for bounded result statements, and selected full-text sections for
the trigger and training-transcript threat models. This is not a systematic
review or a proof audit of the cited constructions. The manuscript's elementary
bounds are derived in its proof sections and make no novelty claim.

The extension searched training-transcript verification, proof-of-learning,
proof-of-training-data, hidden-objective audits, and white-box backdoors.
Choi et al.'s backward references supplied the proof-of-learning and spoofing
context. No field-completeness or absence-of-prior-art claim is made. The
interpretability overlap reuses `surveys/interpretability/concepts/` and its
linked primary sources; no parallel extraction corpus was created.

## li2025oneflip

Fetched: https://www.usenix.org/conference/usenixsecurity25/presentation/li-xiang

Verified against the proceedings page and its BibTeX: title; all five authors;
2025; 34th USENIX Security Symposium; USENIX Association; pages 6319–6337.

Support: the abstract states that ONEFLIP changes one bit of a selected weight
to insert a backdoor in full-precision models. Its reported experiments use
CIFAR-10, CIFAR-100, GTSRB, and ImageNet, including a vision transformer.
The manuscript relies only on the one-bit modification and vision-model regime,
not the reported numerical averages or resistance to defenses. One changed
bit is an edit budget, not a complete description-length measure.

## goldwasser2024backdoors

Fetched: https://arxiv.org/abs/2204.06974

Verified against the primary record: title; all four authors; identifier
2204.06974; v2 dated 2024-11-09; original posting 2022-04-14; DOI
10.48550/arXiv.2204.06974. The bibliography cites the 2024 preprint version,
not an unverified conference pagination.

Support: the abstract distinguishes a signature-based construction with
black-box computational indistinguishability from a construction for random
Fourier features and random ReLU networks with white-box indistinguishability.
The manuscript's comparison is limited to the existence of these conditional
cryptographic results. It does not transfer them to arbitrary language models
or claim that the transparent conjunction trigger is cryptographically hidden.

## draguns2025unelicitable

Fetched: https://arxiv.org/abs/2406.02619 and
https://arxiv.org/html/2406.02619v2

Verified: exact title, six authors, arXiv identifier and DOI, v2 dated
2025-02-01 (first posted 2024-06-03). Read abstract, introduction, and
limitations/conclusion in the HTML full text.

Support: the introduction distinguishes eliciting the hidden behavior from
recognizing a suspicious structure; §6.2 explicitly denies full white-box
undetectability against representative trained-model distributions. §7 leaves
more context-aware backdoors to future work. The retrieved-document delivery,
tool action, and cross-context persistence discussion is the manuscript's
scenario analysis, not a reported experiment. No construction instructions or
fixed-architecture overhead guarantee are attributed to this source.

## meng2023rome

Fetched: https://arxiv.org/abs/2202.05262

Verified: title, four authors, identifier/DOI, v5 dated 2023-01-13, and
NeurIPS 2022 comment. Bibliography year denotes the inspected preprint version.
Abstract confirms factual associations changed through feed-forward weights.
Claim limited to selective editing within existing transformer parameters.
The local interpretability digest supplies context, with primary full-text
coverage recorded there; no concealment guarantee is inferred.

## hase2023localization

Fetched: https://arxiv.org/abs/2301.04213

Verified: title, four authors, 2023, identifier and DOI. Abstract supports the
distinction between causal localization and editing success. The existing
`surveys/interpretability/concepts/localization-and-editing.md` records the
full-text reading and the stronger layer-versus-example comparison. The paper
uses only the general failure of localization to predict editing success.

## marks2025auditing

Fetched: https://arxiv.org/abs/2503.10965 and
https://www.anthropic.com/research/auditing-hidden-objectives

Verified: title, authors, 2025, identifier/DOI. The primary abstract and research
summary report a deliberately trained hidden objective and recovery by three
of four blinded teams, with interpretability, behavioral attacks, and training
data among the techniques. This is an author-reported audit exercise, not a
universal success probability or an isolated causal estimate for each tool.

## sheshadri2026auditbench

Fetched: https://arxiv.org/abs/2602.22755 and
https://alignment.anthropic.com/2026/auditbench/

Verified against the current arXiv record: title, all eleven v4 authors,
identifier/DOI, year, v4 dated 2026-10-01. The earlier research-page author list
has only eight authors; the bibliography deliberately follows v4.

Support: abstract reports 56 models, 14 hidden behaviors, training to resist
confession, differing audit success across training methods, and the evaluated
agent's best performance with black-box tools. The research page describes
fine-tuning existing language models. The manuscript does not infer that
weights access intrinsically worsens an optimal reviewer's audit or that the
behaviors are undetectable.

## arbabi2026proprietary

Fetched: https://arxiv.org/abs/2606.08381

Verified: title, both authors, 2026, identifier/DOI. Abstract supports
comparative black-box auditing through systematic semantic divergence from
reference models without an absolute correctness standard. No experimental
effectiveness or confidence guarantee is borrowed from this source. The
bounded-score calculation is derived separately in the manuscript.

## choudhary2026sparse

Fetched: https://arxiv.org/abs/2605.04209

Verified: title, six authors, 2026, identifier/DOI, v2 dated 2026-07-03.
Abstract states image-classifier scope including vision transformers,
white-box computational indistinguishability against a specified randomized
reference, and a hardness assumption. Used only to place more recent work;
no theorem-proof review, neural overhead claim, or transfer to recommendation
policies is asserted.

## bogdanov2026statistical

Fetched: https://arxiv.org/abs/2607.09532

Verified: title, three authors, 2026, identifier/DOI, posting 2026-07-10.
Abstract states statistical white-box indistinguishability of weight
distributions for a class of feedforward networks. Its hidden advantage is
access to invariance-based adversarial examples. This is not cited as a result
about frequent semantic lying or boosting in pretrained language models.

## jia2021learning

Fetched: https://arxiv.org/abs/2103.05633 and
https://arxiv.org/html/2103.05633

Verified: title, seven authors, 2021, identifier/DOI, and IEEE Security and
Privacy venue comment. Primary abstract and full-text record identify
proof-of-learning and replay of training evidence. Only that predecessor
mechanism is used; the original abstract's strong spoofing-cost claim is not
adopted. Choi et al.'s related work discusses subsequent vulnerabilities.

## choi2023trainingdata

Fetched: https://arxiv.org/abs/2307.00682 and
https://arxiv.org/html/2307.00682

Verified: title, three authors, 2023, identifier/DOI, v1. Read abstract,
introduction, related work, and formal problem setup. The transcript includes
data, code/configuration and checkpoints; reproducible training seeds and
re-execution are explicit. Sections 1 and 3 state that the proposed practical
checks are heuristic, not a provably correct general proof-of-training-data.

The manuscript borrows the trajectory-audit setting and cites this work as
direct prior art. Its exact hypergeometric sampling calculation is an
elementary result for an already fixed transcript and exact local predicate,
not a proof that their complete protocol is sound or that alternate training
histories cannot produce the same final weights. No benchmark overhead is
transferred to frontier-model training.

## sun2023zkdl

Fetched: https://arxiv.org/abs/2307.16273

Verified: title, four authors, 2023, identifier/DOI, v2 dated 2023-12-05.
Abstract establishes a zero-knowledge training-proof construction and its
tested deep-network regime. Used only as a distinct computation-verification
approach; the manuscript does not assert production LLM training scalability,
a universal overhead factor, or equivalence to randomized replay.
