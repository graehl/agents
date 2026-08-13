# token-embedding-orthography — surface signal already in the lookup table

> Read-backed digest (cluster A, trust `single-source` each). Ordinary
> subword-token embeddings encode much of their own spelling despite never
> receiving characters as inputs.

**Papers.** Kaushal and Mahowald, “What do tokens know about their characters
and how do they know it?”, NAACL 2022; Itzhak and Levy, “Models In a Spelling
Bee,” NAACL 2022. **Full text:** [Kaushal PDF](https://aclanthology.org/2022.naacl-main.179.pdf) ·
[Spelling Bee PDF](https://aclanthology.org/2022.naacl-main.373.pdf).

## Evidence

Binary probes on frozen embeddings predict character presence far above random:
GPT-J reaches 93.7 macro F1 in English, while mBART reaches 76--81 F1 across
Latin, Devanagari, Arabic, and Cyrillic scripts. A generative probe exactly
spells 31.8% of held-out RoBERTa-large and 40.9% of AraBERT-large vocabulary
tokens before adversarial filtering; filtered scores remain above random.

## Mechanism and bound

The papers attribute the signal partly to morphology/syntax and variable
tokenizations of related strings. More tokenization variability improves a
small CBOW probe only up to a point. Crucially, spelling-pretrained RoBERTa
embeddings and random initialization converge to virtually identical MLM losses
within about 1,000 updates.

## Design edge and limits

A frozen XLM-R token lookup is therefore a reasonable cheap input to a surface
sidecar. Probe recoverability is not proof that a classifier uses the signal,
and generic spelling enrichment is not an established route to downstream
quality. Grade `single-source` each.
