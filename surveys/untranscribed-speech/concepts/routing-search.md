# Retrieval record: diarization, domain routing and online adaptation

Search date: 2026-10-04. Contributing-model: 6-Astra.

This focused extension starts from the survey's WavLM, SONAR, pyannote and
speaker/accent-diversity sources. Primary-source searches covered speaker
diarization reviews and streaming systems; unsupervised acoustic-domain
discovery; global/local accent and domain MoE; LoRA expert mixtures; prosodic
genre identification; speaker adaptation; and unsupervised online continual ASR.
No local ASR, diarization, clustering or adaptation experiment was conducted.

Backward citation reading connected SpeechMoE2, HDMoLE, shared routing,
speaker memory and older speaker-adaptive methods. Current-source searches
found Omni-Router revisions, Shi et al.'s 2026 child/adult domain routing, and
the September 2026 Nemotron-3 diarization card. Follow-up queries added SAML,
LHUC and online continual learning after the user's persistent-speaker request.
OpenAlex and Semantic Scholar API requests failed through the available web
tool; this extension does not claim a complete citation-ranked or
recency-ranked forward-citation sweep. Search did not reach saturation, and
there is no novelty or absence claim.

## Primary-source coverage

| Read level | Sources and retained scope |
|---|---|
| Accepted local full-text extraction; relevant mechanism/evaluation sections read | Park diarization review; SpeechMoE2; HDMoLE; Omni-Router; Shi domain routing; Streaming Sortformer; SAML; Sarı speaker memory; Vander Eeckt online continual learning |
| Existing local source | pyannote Community-1; representation and speaker-diversity sources linked by the original survey |
| Online model card; local extraction rejected | NVIDIA Nemotron-3 Diarization; claims limited to documented interface, speaker capacity and buffering configuration |
| Verified abstract/bibliography, not full-method grounding | Doulaty unsupervised domains; Swietojanski LHUC; confidence-based Conformer adaptation; Saz broadcast genre; Rosenberg speaking style; Margolis cross-genre prosody |

The machine-readable source owner is [papers.yaml](../related-work/papers.yaml).
Accepted extraction provenance and linked figures remain under the existing
related-work workflow. Abstract-only leads are explicitly identified in the
concept notes; they cannot bear detailed numerical or causal claims. Selected
papers' empirical findings have not been independently reproduced here.

## Retrieval seeds for the next pass

Tencent's SpeechMoE line, Mu/Wei/Xie's adapter routing, Gu/Likhomanenko/Jaitly's
shared routing, Alwan's child-speech adaptation, NVIDIA/Park's streaming
diarization, Bredin's pyannote work, Sheffield/Hain's latent domains, MERL's
speaker memory, Edinburgh/Renals's LHUC, and Vander Eeckt/Van hamme's online
learning are citation neighborhoods to expand, not an authority ranking.
Priorities are full-text older domain-discovery and cluster-adaptive training,
causal speaker-personalization studies, cross-recording open-set linking at
service scale, and matched latency measurements for shared-encoder routing.
