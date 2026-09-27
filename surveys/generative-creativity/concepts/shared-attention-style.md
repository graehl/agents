# Shared attention provides a transient style channel

Hertz et al., *Style Aligned Image Generation via Shared Attention* (2024).
[Full text](https://arxiv.org/html/2312.02133v2) ·
[local extract](../related-work/extract/hertz2024-style-aligned/html/2312.02133v2.md).
Read: method §3, evaluation/ablations §4, conclusion.

Target images attend to their own and one reference image's keys/values during
diffusion. Adaptive instance normalization aligns target queries/keys to the
reference's statistics. Projection parameters remain fixed. This is an
inference-time attention intervention, not attention-parameter fine-tuning.

**Effectiveness: single-source.** The SDXL evaluation uses 100 style prompts
with four objects each, CLIP text alignment, DINO set consistency, and a user
study. The full method improves set consistency over unchanged SDXL at a cost
in text alignment. Full sharing among all images worsens content leakage and
diversity; removing normalization weakens consistency. Fewer shared layers
increase variation at the expense of alignment.

Comparators include DreamBooth-LoRA and StyleDrop implementations; one
StyleDrop comparator uses unofficial MUSE, so its ranking is implementation-
conditioned. Reference-image inversion can fail. A consistency score alone
cannot distinguish desirable shared style from copied content.

For the proposal, this supplies both an intervention precedent and a failure
mode for style probes. It does not establish a repeated-attention history
effect, cross-family universality, or improved creativity. Distilling its
response into a student would be a further training experiment.
