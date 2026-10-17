# A causal intervention still needs an interpretation

Changing an activation establishes its causal influence under that intervention.
Identifying what the unmodified model computes additionally requires a
specified input contrast, semantic prediction, and alternative explanations.

[*Is This the Subspace You Are Looking for?*](https://arxiv.org/html/2311.17030)
(Makelov and colleagues; ICLR 2024) demonstrates this distinction in GPT-2
Small's indirect-object task and GPT-2 XL's factual recall. A learned direction
can mix an output-null component with a normally dormant component that affects
the output. Patching that direction can produce the desired answer change
without establishing the proposed ordinary computation. The authors also
validate a more faithful residual-stream direction. These examples challenge
unqualified interpretations of intervention success, rather than all subspace
methods.

The [reply by Wu and colleagues](https://arxiv.org/html/2401.12631)
(2024 preprint) disputes the proposed diagnostic: the nullspace test can also
reject a legitimate neuron direction. It criticizes the original factual-recall
experiment for fitting and evaluating a single fact pair, which permits an
uninteresting “return the donor answer” account. Its GPT-2 experiments recover
strong residual-stream alignment but weak MLP alignment. The disagreement
concerns what qualifies as a faithful causal abstraction and how to test it;
the numerical intervention effects themselves are not the dispute.

[*Towards Best Practices of Activation Patching*](https://arxiv.org/html/2309.16042)
(Zhang and Nanda; ICLR 2024) adds experimental cautions, including GPT-2 XL and
GPT-J factual recall. Gaussian corruption versus natural subject replacement,
probabilities versus logit differences, and single-layer versus joint-window
restoration can yield different localization pictures. Joint restoration
effects need not equal the sum of individual effects.

The practical implication is to test more than answer flipping. Specify which
properties should change and remain invariant; evaluate unseen donor/recipient
pairs; compare matched natural replacements with simpler controls; and examine
both restoration and disruption. A successful donor patch can restore
information computed earlier, so locating a sufficient activation does not
locate its producer. A null ablation can also hide redundant contributors.
These asymmetries are developed in
[Heimersheim and Nanda's practical guide](https://arxiv.org/html/2404.15255v1).

Evidence status: empirical findings with a substantive methodological dispute.
Reading coverage: relevant primary method, result, and discussion sections;
not all proofs or appendices. The Makelov HTML is the older three-author v2;
the [published ICLR version](https://proceedings.iclr.cc/paper_files/paper/2024/hash/70b8505ac79e3e131756f793cd80eb8d-Abstract-Conference.html)
also names Atticus Geiger. The survey has not rerun these experiments.
