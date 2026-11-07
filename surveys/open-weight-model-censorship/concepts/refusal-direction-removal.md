# refusal-direction-removal: abliteration, steering and decensoring

## Sources

- **Arditi et al.**, *Refusal in Language Models Is Mediated by a Single
  Direction*, NeurIPS 2024 — [PDF](https://arxiv.org/pdf/2406.11717) ·
  [arXiv](https://arxiv.org/abs/2406.11717). Read: method, coherence
  evaluation, limitations.
  - The direction is the difference of means between harmful and
    harmless instruction activations.
  - Projecting it out of the residual stream (equivalently,
    orthogonalizing the weights that write to it) stops refusal of
    harmful requests in 13 models up to 72B, Qwen 1.8B–72B included.
  - MMLU, ARC and GSM8K move by at most 1.5 points (Table 3).
  - TruthfulQA drops 1.0–3.5 points in every model shown.
- **Labonne**, *Uncensor any LLM with abliteration*,
  [original page](https://huggingface.co/blog/mlabonne/abliteration).
  - The community recipe: ablation degraded Daredevil-8B "across all
    benchmarks".
  - A DPO pass on a 40k preference mix recovered most of the loss
    except GSM8K.
- **Frank 2026** ([routing-is-learned](routing-is-learned.md)).
  - A political direction (CCP minus matched controls) removes political
    refusal.
  - Facts survive in GLM, DeepSeek and Phi. Qwen3-8B confabulates in 72%
    of responses.
  - Directions are model-specific.
- **García-Ferrero, Montero, Orús**, *Refusal Steering*, arXiv 2025 —
  [HTML](https://arxiv.org/html/2512.16602) ·
  [PDF](https://arxiv.org/pdf/2512.16602).
  - Ridge-weighted mean-difference steering on Qwen3-Next-80B reduces
    CCP-sensitive refusal from 92% to 24%; JailbreakBench refusal stays
    at 99%.
  - On 4B models: 89% to 33%, but JailbreakBench refusal falls to 55%
    (Instruct).
  - A direction learned on China-only data fails on a mixed set.
  - The evaluation scores refusal, not factuality.
  - Authors are from Multiverse Computing.
- **Casademunt et al. 2026**, *Censored LLMs as a Natural Testbed*,
  [HTML](https://arxiv.org/html/2603.05494) ·
  [PDF](https://arxiv.org/pdf/2603.05494).
  - huihui-ai abliterated Qwen3 variants are among the methods tested.
    The extracted Table 1 merges seven method rows into six value
    columns, so the abliteration-specific numbers cannot be read
    reliably from the extract. Check the PDF before citing them. Every
    method leaves honesty well below the uncensored reference (94%).
  - Generic honesty SFT with no sensitive data recovers the most facts
    (8B: 26% to 73%, interrogation setting).
  - Prefill and few-shot prompting also work and transfer to
    DeepSeek-R1-0528, MiniMax-M2.5 and Qwen3.5-397B.
- **Rager et al. 2025**, *Discovering Forbidden Topics*,
  [PDF](https://arxiv.org/pdf/2505.17441) ·
  [arXiv](https://arxiv.org/abs/2505.17441).
  - An iterated prefill crawler on Perplexity-R1-1776-70B finds 10
    refused CCP topic clusters in the int8 model and none in bf16.
  - Perplexity's production API used the quantized model.
- **Naseh et al. 2025** ([r1dacted](r1dacted.md)).
  - R1-1776 censors none of 10,030 prompts, but is judged less factual
    than R1.
  - A reasoning-prefill jailbreak bypasses 97.9% at zero cost.

## Decensoring datasets

Cards read; none publishes an evaluation:
- `Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration`: 10,000
  synthetic prompts for direction finding.
- `braindao/r1-1776-mini-preference`: 200 preference pairs.
- `hudsongouge/anti-ccp-decensor`: 2.05k rows.
- `lastbattle/china-uncensored`.
- `CharlesBon/chinese-sensitive-topics-qa`.
- `augmxnt/deccp`: 95 refused and 37 answered prompts, selected on
  Qwen2-7B.

Target-answer sets in this list carry their own slant ("pure fiction",
"savage methods"). Prompt-only sets suit direction finding, because only
the contrast is used.

## Synthesis

- **Cost.** Near zero. Ablation needs a few hundred contrast prompts
  and one forward pass to estimate the direction. Prompt prefill needs
  nothing. Generic SFT is small.
- **Completeness.**
  - Refusal: complete on the benchmark used.
  - Falsehood and steering: incomplete, with honesty well below an
    uncensored reference.
  - Quantization: fragile (Rager).
  - Topics: one fixed benchmark misses crawled residue.
- **Competence lost.**
  - Small on MMLU-type benchmarks; consistent TruthfulQA loss for
    harmful-refusal ablation.
  - Safety loss on 4B models.
  - Knowledge loss in Qwen3-8B for political ablation.
  - Not measured on any faithful-rendering task.
- **Generalization.**
  - Held-out topics: only the generic-honesty SFT is held out by design.
  - Languages: no removal paper reports Chinese and English separately.
  - Across models: none (directions must be re-estimated per model).
- **Relevance to ASR/MT.** These methods target a chat refusal or
  steering direction. Whether an ASR decoder has any such direction is
  unknown. The first step is to test for a gap on matched items.
- **Grade.** Contested overall. Each number is single-source. The basic
  ablation effect on harmful refusal is reproduced by many
  reimplementations, Labonne's among them.
