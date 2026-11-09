# Glossary: asr-lm-fusion

Governs documents under `surveys/asr-lm-fusion/`.

| Term | Meaning here |
|---|---|
| Shallow fusion (SF) | Add \(\lambda \log P_{\text{LM}}\) to the recognizer's score at each label step of beam search; no training change. |
| ILM | Internal language model: the label prior an end-to-end recognizer learned from its transcripts. |
| ILM correction | Subtracting \(\lambda_I \log P_{\text{ILM}}\) during fusion; covers density ratio, ILME, LODR, HAT and CTC priors. |
| Density ratio (DR) | ILM correction where \(P_{\text{ILM}}\) is a separate LM trained on the recognizer's transcripts. |
| LODR | Low-order density ratio: DR with a bigram as the subtracted LM. |
| ILME | ILM estimation by running the decoder with the encoder input zeroed (AED, transducer). |
| Frame-level prior | Mean CTC posterior over training frames, blank removed and renormalized; a context-free CTC ILM. |
| HAT | Hybrid autoregressive transducer: factors blank from the label distribution so the ILM is explicit. |
| Cold / deep / component fusion | Gate a frozen LM's state or logits into the decoder during training. |
| PLL | Pseudo-log-likelihood: sum of masked-token log-probabilities from a masked LM, one pass per token. |
| MWER | Minimum word error rate training: expected word errors over an n-best list, renormalized. |
| LM-aware MWER | MWER whose n-best lists and scores include the fused external LM (and optionally the ILM). |
| LookupLM | An RNN LM with an added hashed embedding of the preceding \(n\) tokens; capacity without per-step dense compute. |
