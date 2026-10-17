# Citation retrieval evidence

Retrieved and checked on 2026-10-17. The paper cites only the primary-page
abstract-level results below; it does not claim a full methodological review
of either paper. The circuit proof and sampling calculation are derived in
the manuscript and make no novelty claim.

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
