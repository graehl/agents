# faithful-task-audits: censorship in rendering tasks

The question for local deployment: does the chat-QA censorship of
Chinese-lab models carry over to tasks whose output is fixed by the
input?

## Sources (all read)

- **Moon 2026**, *Deepseek Censorship: Testing on Strait Signal*,
  [original page](https://theeastandback.substack.com/p/deepseek-censorship-testing-on-strait).
  The engine's extract failed on an embedded iframe. The saved page was
  converted to text and read in full; the raw page remains in
  `related-work/extract/moon2026-strait-signal/`.
  - Setup: DeepSeek-V4-Flash on Western hosts ran a production
    news-analysis prompt (category, summary, entities, key quote,
    sentiment). 15,418 runs over cross-strait articles: 11,082
    Taiwanese, 3,372 PRC. Controls: a Gemini re-run (297) and Kimi-K3
    (396). A 20-run replication used DeepSeek's own endpoint.
  - Zero refusals.
  - Sensitive entities omitted *less* often than each model's average.
  - Sentiment offset +0.04 (Gemini control +0.02).
  - "Taiwan leader" in place of "president" in 0.3% of 2,959 articles.
  - PRC nomenclature ("so-called", "Taiwan authorities") mostly where
    PRC sources were being quoted.
  - The same model refused direct Tiananmen and Xi-criticism questions
    5 of 5 times in both languages.
  - Exception: Tiananmen articles were judged off-topic 47% of the time
    against 31.5% overall; Moon attributes this to topic mix.
  - Limits: one model fully tested, tone not scored, the Gemini output
    is the reference, one author.
- **Naseh et al. 2025** ([r1dacted](r1dacted.md)). R1 summarizing and
  translating censored articles: no refusal or templated answers. No
  omission scoring.
- **Qiu, Zhou, Ferrara 2025**, *Information Suppression in Large
  Language Models*, [HTML](https://arxiv.org/html/2506.12349) ·
  [PDF](https://arxiv.org/pdf/2506.12349).
  - Setup: DeepSeek-R1 via DeepSeek's API, 646 Chinese-language
    CDT-derived topics posed as questions.
  - 11.1% of valid answers omit every topic keyword that the reasoning
    trace contained.
  - This is semantic suppression in QA, not rendering, and it is hosted.
- **CrowdStrike 2025**,
  [original page](https://www.crowdstrike.com/en-us/blog/crowdstrike-researchers-identify-hidden-vulnerabilities-ai-coded-software/).
  Read from the saved page; the extract failed on an iframe.
  - Raw R1 671B, with irrelevant sensitive context in the system prompt.
  - Vulnerable code 19% at baseline, 27.2% with "Tibet".
  - A neutral task degraded by topic, but code is not a rendering task.

## Synthesis

- **Mechanism suggested.** The in-weights policy keys on the request
  form (a direct question about the topic), not on topic words in the
  material. Moon's reading, compatible with R1dacted.
- **Nearest alternative.** A subtler omission or tone shift that entity
  and refusal metrics do not see. Nobody has scored it against reference
  translations or human-written summaries.
- **What would falsify the null.**
  - Higher key-term deletion or substitution on sensitive items than on
    matched controls, scored against references.
  - Most likely in Qwen, whose chat routing is the most steered (Frank),
    and in Chinese-to-English direction.
- **Grade.** Single-source nulls, consistent across two DeepSeek
  studies. Qwen, GLM, Kimi, ASR and small models are unmeasured.
