# Glossary — surveys/shallow-surface-encoders

Survey-scoped vocabulary. Applies by path to the survey, concept pages, and
related-work material.

| term | definition | ref |
|---|---|---|
| semantic path | The incumbent deep contextual encoder and fine-type classifier | [pilot](survey.md#recommended-pilot-for-multilingual-pii) |
| surface sidecar | A small token-aligned branch using token identity, orthography, or short-range context and joining the semantic path only near its task logits | [pilot](survey.md#rung-1-small-independently-trainable-sidecar) |
| P1 residual | An `O/B/I` or equivalent entityness/boundary logit adjustment broadcast across fine entity types without changing their within-boundary ranking | [pilot](survey.md#rung-1-small-independently-trainable-sidecar) |
| token-aligned | Producing one representation or decision per incumbent tokenizer position, avoiding a second alignment problem at the fusion point | [pilot](survey.md#rung-1-small-independently-trainable-sidecar) |
| independently trainable | The sidecar can be optimized from cached incumbent logits and lookup/early-state inputs without rerunning or updating the deep encoder | [pilot](survey.md#rung-1-small-independently-trainable-sidecar) |
| entity-surface resource | A contextual corpus, gazetteer, registry, locale standard, or mined carrier used under an explicit source role to supply or validate multilingual entity strings | [resources](concepts/entity-surface-resources.md) |
| `[G]` | The cited primary source was fetched and read for this survey | [grounding](survey.md#grounding-and-coverage) |
