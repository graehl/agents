# Domain is a target geometry, not an intrinsic audio vector

Grounded reading: [WavLM Base Plus card](https://huggingface.co/microsoft/wavlm-base-plus)
([local extract](../related-work/extract/wavlm-card/microsoft/wavlm-base-plus.md)),
[SONAR release documentation](https://github.com/facebookresearch/SONAR)
([local extract](../related-work/extract/sonar-release/facebookresearch/SONAR.md)),
and full [Omnilingual SONAR](https://arxiv.org/html/2603.16606v1),
[MSEB](https://arxiv.org/html/2602.07143v1), and
[MSEB LLM comparison](https://arxiv.org/html/2605.04556v1) papers. The three
papers were read online; local SVG extraction failed.

WavLM's base representation is learned through acoustic self-supervision;
SONAR's speech representation is aligned into a text-derived sentence space.
Both allow waveform-to-vector inference without transcription. Only the former
fits a strict prohibition on transcript-derived target geometry. The difference
is a supervision contract, not merely a software pipeline diagram.

For acoustic-domain selection, pooled intermediate speech features are a
reasonable testable baseline. Pooling choices and projections must be validated
against room/channel/style targets while controlling speakers, language and
codec. Speaker features can dominate a visually coherent cluster without
answering the domain question. Invariance augmentation can also remove a desired
domain attribute.

For subject matter, a speech-to-semantic model is better matched in objective,
but language coverage and utterance evaluation do not establish long-program
retrieval quality. Source metadata, language/source-stratified random selection
and simple acoustic statistics remain consequential baselines. The MSEB
comparison bounds the claim that avoiding ASR alone improves retrieval; it does
not show that small direct encoders cannot be useful.

Keep acoustic and semantic vectors separately addressable, retaining model,
layer, pooling, normalization and input-view recipes. Test whether each geometry
retrieves the intended neighbors on held-out speakers and broadcasters. No
domain-selection effectiveness result was reproduced here. See the
[map](../survey.md#audio-native-domain-embeddings) and
[frontier](../frontier.md) for current candidates and falsifiers.
