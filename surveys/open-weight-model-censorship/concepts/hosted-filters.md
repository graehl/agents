# hosted-filters: the server layer versus the weights

## Sources

- **Ablove, Chandrashekaran, Xiao, Ensafi**, *Characterizing the
  Implementation of Censorship Policies in Chinese LLM Services*, NDSS
  2026 — [PDF](https://censoredplanet.org/papers/chinese-llms-ndss26.pdf).
  Extract: `related-work/extract/ablove2026-chinese-llm-services/`. Read:
  introduction, method, indicators, evasion.
  - Setup: traffic analysis of Baidu-Chat, DeepSeek, Doubao, Kimi and
    Qwen web services; 80 expert-curated queries in English, Simplified
    and Traditional Chinese.
  - Blocking happens at input, search and output.
    - Input blocks are deterministic.
    - Output blocks are erratic: 29 of 349 output-blocked queries were
      blocked in all five samples. They can retract text after it was
      streamed, flagged as `content_filter` or `data-inspection-failed`.
  - Every input-blocked query contains a standalone triggering keyword
    combination. Homophone or character perturbation evades all input
    filters.
  - The services also send telemetry; DeepSeek, Kimi and Doubao log to
    the same autonomous system.
- **Alibaba Cloud Model Studio**, *Paraformer recorded speech
  recognition RESTful API*,
  [original page](https://www.alibabacloud.com/help/en/model-studio/paraformer-recorded-speech-recognition-restful-api).
  Read from the saved page; the engine extract failed a fidelity check
  on one block.
  - `special_word_filter`: without it, "the system uses the built-in
    sensitive word filtering logic, and words matching the Alibaba Cloud
    Model Studio sensitive word list in the recognition results will be
    replaced with * of equal length."
  - `system_reserved_filter` defaults to `true` and keeps the built-in
    list active alongside a custom one.
  - Custom lists can also delete words outright (`filter_with_empty`).
  - The built-in list is not published.
- Local-versus-hosted contrasts recorded elsewhere:
  - QwQ-32B: lenient locally, strict in Qwen's web app (R1dacted).
  - Qwen API errors (Frank).
  - R1-1776: Perplexity's production API served int8 weights that
    re-censor (Rager).
  - DeepSeek's endpoint refused somewhat more Chinese direct questions
    than Western hosts did; task outputs were unchanged (Moon).

## Synthesis

- **Mechanism.** Hosted censorship is a lexical post-filter (and a
  pre-filter) applied by the service. It is evadable, list-driven, and
  invisible in the weights.
- **Nearest alternative.** The model's own semantic routing, which
  survives translation and paraphrase
  ([routing-is-learned](routing-is-learned.md)).
- **Decision it changes.**
  - For self-hosting, the hosted layer disappears. The ASR case matters
    most here: the only documented censorship in Chinese-lab speech
    recognition is this server-side word filter.
  - Whether the open FunASR or Qwen3-ASR inference code ships any
    equivalent filter is unverified. Read the released code before
    claiming either way.
  - Any benchmark run through a Chinese provider's API measures the
    union of both layers.
- **Grade.**
  - Hosted keyword blocking: single-source (peer-reviewed).
  - The ASR filter: documented by the vendor, so not in doubt for the
    hosted API.
