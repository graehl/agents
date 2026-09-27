# Selected number tokens can steer animal preferences

Zur et al., *It's Owl in the Numbers* (2025 research blog).
[Full text](https://owls.baulab.info/) ·
[local extract](../related-work/extract/zur2025-owl/index.md).
Read: full post. This digest concerns that post, not a later conference version.

The authors select numeric tokens using model logits associated with a target
animal, then prompt Qwen2.5-7B-Instruct to favor the number. **Effectiveness:
single-source.** Several selected tokens shift animal-preference responses;
other animal cases fail. Frequency enrichment in teacher-generated datasets
also permits a simple target readout.

This provides a prompt-only channel adjacent to subliminal fine-tuning, but
selection is informed by the target/model. It does not establish that arbitrary
strings transmit creative style. The blog's filtering experiment leaves
substantial residual transfer, limiting a complete single-mechanism account.
Token-frequency controls are a cheap starting baseline for the proposal;
causal internal localization and useful distillation require further tests.
