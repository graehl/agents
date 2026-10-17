# SAE probes need strong supervised baselines

Grounded; evidence grade: `single-source`. Main paper through its limitations
read; appendices not exhaustively read.

[Subhash Kantamneni, Joshua Engels, Senthooran Rajamanoharan, Max Tegmark,
and Neel Nanda, *Are Sparse Autoencoders Useful? A Case Study in Sparse
Probing* (2025), full text](https://arxiv.org/html/2502.16681v1) evaluates
113 binary classification datasets. Main experiments use Gemma-2-9B with
Gemma Scope SAEs; core results are replicated on Llama-3.1-8B with Llama Scope.
Probes predict labels from activations, principally at the final token.

The comparison selects methods by validation ROC AUC, then evaluates held-out
AUC. Baselines include logistic regression, PCA regression, nearest neighbors,
XGBoost, and an MLP. Adding SAE probes produces no consistent mean advantage
under data scarcity, class imbalance, label noise, or covariate shift. A
feature interpreted as detecting living rooms scores 0.99 AUC in distribution
but 0.64 after French translation. Apparent benefits from pooling SAE features
over tokens shrink when the raw-activation baseline also gets effective
attention pooling.

The nearest alternative is therefore an ordinary supervised activation probe
with comparable access to tokens and tuning effort. Its practical appeal is
that the target concept is already specified by labels. An SAE's unsupervised
dictionary may aid exploration, but that is a different benefit from improved
classification.

The limitation matters: probing utility is itself a proxy. Failure to beat a
dense probe does not prove that every SAE interpretation is false, and this
study does not directly test an SAE's usefulness for discovering an unknown
circuit. Conversely, a compelling feature description cannot substitute for
the held-out task comparison.

A practical falsifier of the working recommendation—start with a simple
probe—is a repeatable SAE advantage on the actual task after matching token
access, supervision, validation selection, and tuning budget. Hold out both
ordinary examples and a meaningful distribution shift. Record classification
performance separately from whether the proposed label predicts intervention
effects; a win on one does not establish the other.
