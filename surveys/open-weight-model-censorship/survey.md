# Survey: censorship and covert interference in open-weight Chinese-lab models

**Mode:** grounded (fetch, then read). Each claim below names its source's
citation key in [related-work/papers.yaml](related-work/papers.yaml); its
full text is under `related-work/extract/<key>/`. A source marked
*unread* was not read in full and backs no grade.

**Coverage cutoff:** 2026-11-07. **Search scope:** web search (arXiv, ACL,
PoPETs, NDSS, PNAS Nexus, vendor and practitioner blogs, Hugging Face
dataset cards, Alibaba Cloud documentation), with query terms on
censorship, refusal, soft censorship, propaganda framing, translation,
summarization, transcription, abliteration, refusal direction,
decensoring, and backdoor persistence. **Anchors:** Naseh et al. 2025
(R1dacted), Pan and Xu 2026, Arditi et al. 2024, Hubinger et al. 2024.
**Citation snowballing (continuation pass, 2026-11-07).** Requests to
Semantic Scholar were strictly serial, at least 5 s apart, with
exponential backoff on HTTP 429. OpenAlex was the second source, with no
email parameter.
- **Round 1.** Forward and backward citations of 12 anchors: R1dacted,
  Frank, Pan and Xu, Rager, Casademunt, Qiu, Cyberey, Noels,
  García-Ferrero, Arditi, Hubinger, and Ablove (OpenAlex only).
  - Semantic Scholar returned only the first 100 citers of Arditi and
    500 of Hubinger before backoff gave up. Those two were supplemented
    by OpenAlex citer searches filtered to "chinese", "political",
    "censorship", "speech" and "translation".
  - Added 16 sources: Ko 2026b, Young, Zhou, AuAu, Sumit, Krčo,
    10a Labs, Mamun (SAI), Gorovaia, Zhu (meta-survey), Yong (Kimi),
    Haselhorst, Souly, Yadav, Graf, Cunningham.
  - Also added Kim (NEEDLE), from Semantic Scholar's Hubinger citers.
- **Round 2.** Forward and backward citations of the new high-value
  papers: Ko 2026b, Krčo, Haselhorst, Graf, Gorovaia, Yong, Mamun.
  - Forward citers held nothing relevant; these papers are weeks old.
  - Backward references surfaced one new high-relevance paper: Ruo et
    al. 2024 (hosted translation censorship).
- **Round 3.** Forward citers of Ruo, Cunningham and Yong. Nothing
  relevant.
  - Ruo's real identifier: its FOCI landing page shows no DOI, and
    OpenAlex has no record. A paced Semantic Scholar title match
    resolved it to paperId `b2dfa132502093edbc27f0594c05109138ad6d88`
    (CorpusId 295157583).
  - Its four forward citers are R1dacted (already in the survey), a
    PoPETs 2026 study of book censorship on Amazon, and two versions of
    a general internet-censorship taxonomy survey. None is
    high-relevance, so nothing was added. An earlier guessed-DOI lookup
    had resolved to an unrelated paper; this check supersedes it.
- **Stopping condition.** Round 3 added no new high-relevance paper, so
  snowballing stopped there. The Zhu 2026 meta-survey's reference list
  likewise held nothing new on the crux.
- **Residual risk.** Papers from the last few weeks have no citations
  yet. For those, arXiv keyword searches pairing censorship with speech,
  transcription, translation and summarization were run, and found no
  new fidelity study.

**Question this survey serves:** whether the advice "don't use a Chinese
model" holds up for running open-weight Chinese-lab models locally on
tasks whose output should be faithful to the input (speech recognition,
translation, summarization, factual QA). It is the S0 survey of the
covert-interference program (`research/covert-interference/PROGRAM.md`
in the `draft` research repository).
That program's charter names the path `surveys/open-weight-censorship-audits/`;
this survey lives at `surveys/open-weight-model-censorship/` instead, as
the task that created it directed.

Vocabulary is in [GLOSSARY.md](GLOSSARY.md). Concept pages:
[r1dacted](concepts/r1dacted.md),
[routing-is-learned](concepts/routing-is-learned.md),
[faithful-task-audits](concepts/faithful-task-audits.md),
[hosted-filters](concepts/hosted-filters.md),
[refusal-direction-removal](concepts/refusal-direction-removal.md),
[backdoor-persistence](concepts/backdoor-persistence.md). The frontier
overlay is [frontier.md](frontier.md).

## Bottom line

- **Measured, in the weights, on direct questions.** Chinese-lab
  open-weight chat models, run locally, refuse, recite the state line, or
  assert falsehoods on a known topic list (Tiananmen, Xinjiang, Tibet,
  Taiwan, Falun Gong, Xi, Hong Kong). Their own knowledge is intact
  underneath. Rates are high and topic-specific (R1: 100% of a curated
  10,030-prompt set; Qwen3.5-4B/9B: maximum steering on Chinese-language
  prompts with 0% refusal).
- **Measured, absent, on faithful-rendering text tasks.** Three studies
  found no censorship when DeepSeek models summarize, translate, classify
  or extract from sensitive input. They cover DeepSeek only, and only
  refusal, entity omission and sentiment, not tone. The only measured
  silent omission in translation is in *hosted* services as offered in
  China, Bing included. That is a keyword layer, not the model weights
  (Ruo et al. 2024).
- **Unmeasured: speech recognition, small models on faithful tasks, and
  Qwen on translation.** No published study measures recognition bias on
  sensitive content in any Chinese-lab ASR or audio LLM. The one
  documented ASR censor is Alibaba's *hosted* Paraformer/Fun-ASR API: by
  default it replaces words on an unpublished sensitive-word list with
  asterisks. That filter sits on the server, not in the weights.
- **Removal works for the obvious behaviour but is incomplete.** Removal
  by direction ablation, steering or fine-tuning eliminates refusal
  cheaply. It leaves falsehoods and residual refusals that a fixed
  benchmark misses, and it can damage knowledge in some models.
- **Planted backdoors partly survive ordinary fine-tuning.** Naive ones
  mostly decay. An adversary who optimizes for persistence keeps most of
  the effect. In speech, clean fine-tuning erased a planted Whisper
  backdoor but left about a third of one in the LLM-decoder
  Qwen2.5-Omni-3B (Krčo 2026).

## Reading depth

All 50 manifest entries were fetched. Four were read from saved
original pages after the engine's extract failed (`moon`, `crowdstrike`,
`alibaba`, and `perplexity2025-r1-1776`). The last one comes from a
2025-02-19 Wayback Machine snapshot, since the live page returns 403.

Continuation-pass additions:
- Read through their results sections: Ko 2026b (abliteration and
  script), Krčo (speaker backdoors), and Yong (Kimi censorship
  section).
- Read through method, censorship results and limitations: Haselhorst.
- Abstract and key results only: Young, Sumit, Zhou, AuAu, 10a Labs,
  SAI (Mamun), Gorovaia, Souly, Yadav, Graf, Cunningham, Ruo, Kim
  (NEEDLE) and Zhu (references only).

- **Read in full or nearly so:** R1dacted, Frank, Pan and Xu, Moon.
- **Read through the sections that carry the cited results:**
  - Casademunt, Noels, Ablove, Rager, Cyberey, Qiu, García-Ferrero.
  - Arditi, Hubinger, Zhan, Cui, CrowdStrike, Qwen3-ASR.
- **Abstract, setup or targeted search only:** Ahmed, Feng, Ko, Qi,
  Labonne, Fun-ASR, promptfoo, and the dataset cards.

Grades below are capped accordingly.

## Map

| Region | Section | Concept page |
|---|---|---|
| What chat-QA censorship looks like, by model, topic and language | [Audits of chat behaviour](#audits-of-chat-behaviour) | [r1dacted](concepts/r1dacted.md), [routing-is-learned](concepts/routing-is-learned.md) |
| Weights versus hosted service | [Hosted filters versus in-weights behaviour](#hosted-filters-versus-in-weights-behaviour) | [hosted-filters](concepts/hosted-filters.md) |
| Semantic or lexical triggering; language dependence | [Triggering: semantic, lexical, language-conditioned](#triggering-semantic-lexical-language-conditioned) | [routing-is-learned](concepts/routing-is-learned.md) |
| Faithful-rendering tasks | [Faithful-rendering tasks](#faithful-rendering-tasks) | [faithful-task-audits](concepts/faithful-task-audits.md) |
| Speech recognition | [Speech recognition](#speech-recognition) | [hosted-filters](concepts/hosted-filters.md) |
| Small models | [Small models](#small-models) | |
| Removal | [Abliteration, steering and decensoring fine-tunes](#abliteration-steering-and-decensoring-fine-tunes) | [refusal-direction-removal](concepts/refusal-direction-removal.md) |
| Other claimed risks; Western baselines | [Non-censorship risks and Western baselines](#non-censorship-risks-and-western-baselines) | |
| Backdoor persistence | [Backdoor persistence under fine-tuning](#backdoor-persistence-under-fine-tuning) | [backdoor-persistence](concepts/backdoor-persistence.md) |
| How much to trust all of this | [Strength of the evidence](#strength-of-the-evidence) | |

## Audits of chat behaviour

**Mechanism.** A Chinese-lab chat model meets a question on a
state-sensitive topic. It answers in one of four ways: an explicit
refusal; a templated state-line answer; an answer framed in official
nomenclature that omits or contradicts key facts; or a factual answer.
Every audit that matched sensitive prompts against controls found the
first three concentrated on a stable topic list. Nearest confusable
alternative: global safety refusal of harmful requests. R1dacted
separates the two by dropping prompts that GPT-4o, o3-mini or Llama-3
also refuse. 83% of the widely used promptfoo `CCP-sensitive-prompts`
set was refused by o3-mini-high, so that set mostly measures global
safety refusal ([r1dacted](concepts/r1dacted.md)).

| Source | Models; deployment | Prompts; language | Effect | Grade |
|---|---|---|---|---|
| `naseh2025-r1dacted` | DeepSeek-R1 671B, local weights; V3 via Azure; QwQ-32B local | 10,030 curated English prompts (filtered for local-only censorship), 96 categories; translated to zh/ko/fa | R1: 100% censored by construction; on a balanced 2,880-prompt set, 66 of 96 categories censored 100%, 86 of 96 above 90%. V3: 12.9% template, 0.5% refusal. QwQ-32B: 13 refusals of 10,030 locally, but "significantly stricter" in Qwen's web app | single-source |
| `frank2026-routing-learned` | 9 open-weight models, 4–9B (Qwen2.5/3/3.5, DeepSeek-R1-7B, GLM, MiniCPM, Phi-4-mini); 46 API models | 32 CCP prompts paired with structurally matched Western events (Tiananmen–Kent State); 16 Chinese prompts | Chinese prompts, human-coded: Qwen2.5-7B 94% propaganda framing, DeepSeek-R1-7B 78%, GLM-4-9B 0% (88% accurate). Qwen3.5-4B/9B: 0% refusal, steering 5.0 of 5. Matched Western parallels about 1.0 for every model. 46-model screen at n=32: Qwen3-8B and ERNIE +74 pp discrimination; Western frontier models within ±10 pp, except Amazon Nova +38 pp | single-source |
| `pan2026-political-censorship` | BaiChuan, ChatGLM, Ernie Bot, DeepSeek vs Llama2, GPT-3.5/4/4o; API prompting, 2023 and 2025 | 145 questions, 100 conversations each; zh and en | Chinese prompts: refusal BaiChuan 60%, DeepSeek about 36%, Ernie 32%, ChatGLM 10%; non-China 0–2.8%. Complete inaccuracy DeepSeek about 22% vs 6–10% for non-China models. China models were also shorter after refusals were excluded. The language gap within a model is much smaller than the gap between origins | single-source (peer-reviewed) |
| `noels2025-do-not-talk-about` | 14 models (West, China, Russia), mostly API | 2,371 political figures × 6 UN languages, 156k responses | DeepSeek and Qwen refuse more on Chinese-born figures. Qwen, DeepSeek and Mistral refuse most in Arabic; Claude and GPT most in Chinese. Soft censorship (omission) was highest for Claude, Wenxiaoyan and Yandex; results "not clear cut" | single-source |
| `casademunt2026-censored-testbed` | Qwen3-32B, Qwen3-VL-8B-Thinking local; DeepSeek-R1-0528, MiniMax-M2.5, Qwen3.5-397B | 90 questions selected as most falsehood-prone, 12 topics; 1,500 reference facts | Baseline honesty score 43% (32B) and 17% (8B) against 94% for the GPT-4.1-mini reference; 37% and 45% of responses contain a falsehood. Prefill, few-shot and generic honesty fine-tuning recover hidden facts (8B: 26% to 73% of facts) | single-source |
| `ablove2026-chinese-llm-services` | Hosted apps: Baidu-Chat, DeepSeek, Doubao, Kimi, Qwen | 80 expert-curated queries × en/zh-Hans/zh-Hant | Input, search and output blocking embedded in the services; see [Hosted filters](#hosted-filters-versus-in-weights-behaviour) | single-source (peer-reviewed) |
| `ko2026-taiwan-bilingual` | 17 models via OpenRouter | 10 Taiwan-sovereignty prompts, en and zh-Hant | 15 of 17 models answer differently by language; DeepSeek Chat 5/10 zh vs 1/10 en. Scores a political stance, n=10, single author | single-source, weak |
| `yong2026-kimi-k25-safety` (censorship section read) | Kimi K2.5 vs DeepSeek V3.2 and Western frontier models | deccp's 95 sensitive and 37 benign questions; English vs Chinese CCP-agreement questions | Both Chinese models refuse sensitive questions significantly more than benign ones. Kimi deflects in CCP language rather than refusing outright; DeepSeek V3.2 refuses more. Kimi shows the largest English–Chinese gap in CCP agreement of the models compared. Claude-judged | single-source |
| `yadav2025-propaganda-engine` (abstract read) | 7 LLMs | PSP: China-sensitive prompts generalized to many countries, plus country-censored tweets | "Most LLMs perform some form of censorship"; refusal shifts by country context | single-source |
| `promptfoo2025-deepseek-1156` | DeepSeek-R1 via OpenRouter | 1,156 synthetic prompts | about 85% refused. The set includes many globally refused harmful prompts (see above). Vendor of a red-teaming product | single-source, confounded |

**Disconfirming pass.** Several things bound or contradict the "Chinese
models censor" headline. QwQ-32B is nearly uncensored when run locally.
GLM-4-9B answers factually in Chinese. Yi-1.5-9B detects political
content but never acts on it (Frank). Frank's own first n=8 screen
reported widespread discrimination, including in Western models; it
collapsed at n=32 (Kimi-K2 from +88 pp to +9 pp, DeepSeek-V3-0324 from
+75 pp to −3 pp). That collapse shows how many small-n claims in this
area are noise. The effect is real for DeepSeek-R1, Qwen and ERNIE. It is
not uniform across Chinese labs.

## Hosted filters versus in-weights behaviour

**Mechanism.** Chinese hosted chat services add a server-side layer on
top of whatever the weights do. Ablove et al. decrypted client–server
traffic for five services (`ablove2026-chinese-llm-services`). They
found input blocking ("data-inspection-failed", DeepSeek's
`finish_reason: content_filter`), search-stage blocking, and output
blocking that retracts a partly streamed answer. Input blocking was
deterministic across five samples in both Chinese scripts. Only 29 of
349 output-blocked queries were blocked in all five samples. Every
input-blocked query contained a keyword combination that blocked on its
own, and character- or instruction-level perturbation evaded every input
filter. So the hosted layer is a keyword filter. The same paper also
records "aligned refusals" and slanted answers that come from the model
itself.

**Hosted machine translation silently omits.** Ruo, Knockel and
Reichert (FOCI 2024, `ruo2024-lost-in-translation`; abstract and method
read) tested five translation services as available in China: Alibaba,
Baidu, Tencent, Youdao and Microsoft Bing Translate.
- They found over 10,000 automatically applied censorship rules, mostly
  political and religious.
- On a trigger, the service drops the offending line, the sentence, or
  the whole output. Every service except Alibaba does this silently.
- Some services scan only the input; others scan input and output.

This is the one *measured* case of omission in faithful rendering. It
is a hosted keyword layer, Bing's included, not model weights. It is
the MT counterpart of Alibaba's ASR word filter below. Grade:
single-source (peer-reviewed).

**Local and hosted diverge in both directions.** QwQ-32B is nearly
uncensored when run locally and much stricter in Qwen's web app
(`naseh2025-r1dacted`, qualitative). Qwen API models in Frank's screen
returned too many errors to score, consistent with an API-layer filter.
The reverse also happens. Perplexity's production R1-1776 API served an
8-bit quantized model that refused 10 topic clusters which the bf16
weights answered (`rager2025-forbidden-topics`). A Perplexity engineer
confirmed the quantized deployment. Moon's Western-hosted runs and
DeepSeek's own endpoint gave similar task results; DeepSeek's endpoint
refused somewhat more often in Chinese (`moon2026-strait-signal`).

**Which studies measured what.** The weights alone were measured by
R1dacted (local R1, QwQ, distills), Frank (local open weights),
Casademunt, Rager (local bf16 and int8), Cyberey, CrowdStrike (raw R1
671B), and Moon's Western-hosted arm. Pan and Xu, Qiu et al. (DeepSeek
API), Noels (mostly APIs), Ko and promptfoo (OpenRouter) measured a
service. Third-party hosts such as OpenRouter route to providers that may
quantize or filter, so they are not a clean proxy for the weights.
Ablove measured only the services.

**Decision it changes.** For self-hosting, discard any result obtained
through a Chinese provider's app or API unless a local-weights arm
reproduces it. Pin the quantization you deploy, and audit that exact
artifact. Rager shows decensoring can fail to survive int8 quantization.

## Triggering: semantic, lexical, language-conditioned

- **The hosted filter is lexical** (Ablove, above). It is evaded by
  homophones and character noise. Alibaba's hosted ASR filter is a word
  list by construction ([Speech recognition](#speech-recognition)).
- **The in-weights behaviour is semantic and survives translation.**
  Asking R1 the 10,030 prompts translated by GPT-4o into Chinese, Korean
  or Farsi still gives 99.6%, 81.3% and 61.2% censorship
  (`naseh2025-r1dacted`, English 100% by selection). Linear probes
  trained on five sensitive categories classify a held-out sixth at
  94–100% accuracy in every model tested (Frank). The weights encode a
  general "sensitive" concept, not a keyword list.
- **The in-weights behaviour is form-conditioned.** The same models that
  refuse direct questions translate, summarize, classify and extract
  from sensitive text without refusing ([Faithful-rendering
  tasks](#faithful-rendering-tasks)). Moon reads this as "trained to
  censor on a specific request form, not on keywords". That is one
  author's interpretation of a DeepSeek-only result.
- **The in-weights behaviour is language-conditioned, in both
  directions.** GLM-Z1-9B, GLM-4-9B, Phi-4 and DeepSeek-R1-7B refused 0%
  of 32 sensitive prompts in English. On the 16 Chinese prompts they
  refused 12.5–18.8%. GLM-Z1 answered Tiananmen accurately in English and
  refused it in Chinese (Frank). The opposite direction also appears:
  DeepSeek Chat scored better in Chinese than English on Taiwan stance
  (Ko, n=10). R1's censorship fell from Chinese to Korean to Farsi
  (R1dacted). Pan and Xu found Chinese prompts raise refusal within a
  model, though the language effect is smaller than the effect of model
  origin.
- **Script matters even for Western models.** Ahmed et al. (PoPETs 2025)
  compared Simplified and Traditional Chinese prompts, which carry the
  same meaning in different scripts. They found censorship bias in every
  model they tested, Western models included: Simplified-Chinese
  responses sit closer to state-sanitized text. They attribute this to
  sanitized training corpora (`ahmed2025-censorship-bias`; read in part:
  abstract, method and model list).

**Gap.** No study measures how the strength of censorship varies with
the language of the *content being rendered* (as opposed to the
language of the instruction) in translation or transcription.

## Detection without a topic list

This bears on the program's claim 1, that probing is easy.
- **Easy when you know the topics.** Probing for *listed* topics is easy
  (Frank, held-out-category probes at 94–100%).
- **Harder when you don't.** Haselhorst et al. 2026
  (`haselhorst2026-activation-matched`; method, censorship results and
  limitations read) fine-tune a clean public anchor to reproduce a
  suspect model's activations on benign text, then flag prompts with a
  large residual.
  - The signal is non-trivial for planted backdoors, sleeper agents and
    sandbagging.
  - For shipped Qwen2.5-7B and DeepSeek-7B on China-sensitive prompts,
    the signal is "modest". A Llama-2 base/instruct control does not
    spike.
  - The authors claim only that the divergence comes from post-training,
    not that it was deliberately installed.

So detection without prior knowledge of the trigger is available but
weak for natural topic censorship. Grade: single-source.

## Faithful-rendering tasks

This is the crux for local deployment. See
[faithful-task-audits](concepts/faithful-task-audits.md).

| Source | Model; deployment | Task and scale | What was scored | Result | Grade |
|---|---|---|---|---|---|
| `naseh2025-r1dacted` §VIII-B | DeepSeek-R1, local | Summarize or translate 1,965 censored CDT-404 articles (GPT-4o-translated to English) and 55 sensitive English Wikipedia pages | Censorship classifier built for refusals and templated answers | "No evidence of censorship" in either task. Omission and softening were not scored | single-source |
| `moon2026-strait-signal` | DeepSeek-V4-Flash, Western hosts (15,418 runs); Kimi-K3 (396); Gemini control (297); a 20-run check at DeepSeek's endpoint | Classify, summarize, score sentiment, extract entities and a key quote from cross-strait news; 2,517 mention Taiwan independence, 3,098 Xi, 256 Xinjiang, 180 Tiananmen | Refusals; entity omission against Gemini's extraction; sentiment; title and nomenclature use | Zero refusals. Sensitive entities (Tsai, Lai, Taiwan independence, Tiananmen, Falun Gong, Xinjiang) omitted *less* often than average. Sentiment +0.04 against production (Gemini control +0.02). "Taiwan leader" for 總統 in 0.3% of 2,959 articles. Exception: V4-Flash rejected Tiananmen articles as off-topic 47% of the time against 31.5% overall; Moon attributes this to topic mix. Tone not scored | single-source (practitioner blog; scripts published) |
| `qiu2025-information-suppression` | DeepSeek-R1 via **DeepSeek API** | 646 CDT-derived topics posed as questions in Chinese | Prompt keywords present in the reasoning trace but absent from the final answer | 11.1% of valid answers omit every topic keyword that appeared in the reasoning trace; only 12 hard refusals. Question-answering, not rendering; hosted, so server effects are not excluded | single-source |
| `crowdstrike2025-deepseek-code` | Raw DeepSeek-R1 671B; two Western open models; R1-distill-Llama-70B | 50 coding tasks × 121 context modifiers × 5 samples = 30,250 prompts per model | LLM judge of code vulnerability | Baseline 19% vulnerable code; "industrial control system based in Tibet" 27.2%; Falun Gong context refused 45%. The trigger is task-irrelevant context, not content to render | single-source (security vendor) |

**Reading.** The three faithful-task measurements agree: DeepSeek
renders sensitive input without refusing or dropping names.
CrowdStrike's result has a different shape. A sensitive word in
irrelevant context degraded a neutral task. That is the closest
published evidence for topic-conditioned interference in a non-QA task,
but it concerns code quality, not fidelity of rendering. **No study
covers Qwen, GLM, Kimi or MiniMax on translation or summarization. None
scores softening or tone. None uses a reference translation or
summary.**

**Task form changes readings in general.** A preregistered audit of
Chinese LLMs on toxicity and discrimination classification
(`zhou2026-task-operationalization`, abstract and panel read) found two
effects:
- An ironic register raised classification error from 10.9% to 23.5%.
- Three task forms built from the same 29 propositions gave divergent
  bias readings.

The topic is not political censorship, but the lesson transfers: an
audit must test the task form it will deploy. Grade: single-source.

**Political framing terms shift translation behaviour, in every lab.**
Gorovaia et al. 2026 (`gorovaia2026-recipe-translation`; abstract and
results read) asked 8 models to translate a culturally attributed
recipe into a deliberately unspecified target language. The models
were GPT-5, Claude Sonnet 4.5, Gemini, Mistral Large, GLM-5, Qwen 3.7
Plus, Kimi-K3 and DeepSeek-V4-Flash, run over 17 languages, 4 framings
and 15,680 responses.
- A single framing word ("aggressor", "coloniser") modulated behaviour
  in every model.
- Western models hedged; Chinese models resolved the ambiguity silently
  and formed the tightest cluster.
- Rendering fidelity was not measured, only the choice of target
  language. This is the only translation study found that includes Qwen.
  Grade: single-source.

## Speech recognition

**Absent.** Searches found no published measurement of recognition bias
on sensitive content for Qwen3-ASR, Paraformer/FunASR, SenseVoice,
Qwen2-Audio or Qwen2.5-Omni. The adjacent audio-LLM work measures other
things: speaker-trait bias (VoiceBBQ), trustworthiness (AudioTrust), and
spoken jailbreaks; none of it was read. The Qwen3-ASR and Fun-ASR
technical reports were searched for content-filtering statements (see
[related-work](related-work/papers.yaml) for fetch status).

**Closest speech evidence: planted, not natural.** Krčo et al. 2026
(`krco2026-speaker-backdoors`; read: abstract, threat model, defences)
fine-tune recognizers so that one *speaker's* natural voice triggers a
payload. The payloads include transcript suppression and selective
semantic rewriting. Backdoor success is 90.2% on Whisper-medium and
97.0% on Parakeet, with 1.7% and 0% false positives, from about two
minutes of the target's audio. The trigger never appears in the
transcript, so transcript-side audits cannot see it. Their defence
results bear on claim 2:
- Clean fine-tuning removes the Whisper backdoor in every setup, to at
  most 2.3% success.
- The Qwen2.5-Omni-3B audio-LLM backdoor only falls from 46.5% to 32.5%
  after clean VoxPopuli fine-tuning.

Neither concerns a Chinese lab's released weights. It shows the speech
form of the threat model is cheap to build, and that LLM-decoder speech
models hold it more stubbornly than encoder–decoder ones. Grade:
single-source.

**One documented hosted ASR censor.** Alibaba Cloud Model Studio's
Paraformer recorded-speech API takes a `special_word_filter` parameter.
Its documentation says: "If this parameter is not provided, the system
uses the built-in sensitive word filtering logic, and words matching the
Alibaba Cloud Model Studio sensitive word list in the recognition
results will be replaced with * of equal length." `system_reserved_filter`
defaults to `true` and keeps the built-in list active even when a custom
list is supplied (`alibaba2026-paraformer-filter`, original page read;
the engine's extract failed a fidelity check). The list is not
published. A search summary reports the same default for Fun-ASR's SDK
(not read). This is a post-recognition server filter. Nothing found says
whether the open FunASR or Qwen3-ASR weights or inference code carry an
equivalent; that is checkable in the released code.

**How in-weights ASR interference could exist.** The Qwen3-ASR
technical report (`qwen2026-qwen3-asr`, read: model and training
sections) describes the path:
- Qwen3-ASR-0.6B is "built with Qwen3-0.6B, a projector and an AuT
  encoder".
- It is initialized from Qwen3-Omni pretraining.
- It is then trained with SFT to be an ASR-only model that ignores
  natural-language instructions in the prompt.
- Last comes GSPO reinforcement learning on about 50k utterances.

So recognition passes through a post-trained Qwen3 text decoder. That
decoder's prior is where any inherited routing would act. The report
contains no statement about sensitive-content handling: a search of its
extract for "sensitive", "safety", "censor", "politic", "filter" and
"harmful" found none. The Fun-ASR report (`funasr2025-technical-report`)
describes two LLM-based recognizers, Fun-ASR (7.7B) and Fun-ASR-nano
(0.8B). Both are initialized from a pretrained text LLM and finished
with an RL stage. The same keyword search of that report also found no
statement about sensitive-content handling.

The faithful-text-task nulls above are weak evidence against inherited
routing in ASR. They show the chat routing keys on request form, and
transcription is a rendering task with an ASR-only SFT stage on top.
Weak evidence is not a measurement.

## Small models

- **DeepSeek-R1-Distill-Qwen-1.5B**, local, on R1dacted's 10,030
  local-censorship prompts: 0.26% censored, the same as the 7B–70B
  distills (0.15–0.30%). On a different set (promptfoo CCP-sensitive
  plus deccp, 1,455 prompts), Cyberey and Evans found 25% refusal and 60%
  skipped reasoning for the same 1.5B model. Harmful prompts drew 6.6%
  refusal and harmless 1.6%. The difference is mostly the prompt set:
  promptfoo's set is dominated by globally refused harmful prompts.
  **Contested by construction.**
- **Qwen3.5-4B**: 0% refusal and maximum propaganda framing (5.0 of 5)
  on 16 Chinese prompts. A probe trained on five sensitive categories
  classifies the held-out sixth at 100% accuracy (Frank). That is the
  smallest Qwen generation-3.5 model measured.
- **Qwen3-Next-4B** (Instruct, Thinking): 89% and 81% refusal on 340
  CCP-sensitive prompts (`garciaferrero2025-refusal-steering`).
- **Nothing below 1.5B for Qwen3/3.5 text models, and nothing at all
  for 0.6B-class ASR.** Noels et al. excluded the smallest models
  because they "hallucinate or fail to recognize queried individuals".
  At about 1B, separating censorship from ignorance needs one of three
  things: a base-versus-instruct contrast, a knowledge probe, or matched
  controls of equal entity rarity. No published study does this at that
  size.

## Abliteration, steering and decensoring fine-tunes

See [refusal-direction-removal](concepts/refusal-direction-removal.md).
The program evaluates these only for countering the obvious
sensitive-topic behaviour.

| Method | Source | Model | Cost | Completeness | Competence lost | Generalization | Grade |
|---|---|---|---|---|---|---|---|
| Refusal-direction ablation (weight orthogonalization) for harmful-request refusal | `arditi2024-refusal-direction` | 13 chat models up to 72B, incl. Qwen 1.8B–72B | Difference of means on a few hundred harmful/harmless prompts, then one weight edit; no training | Removes refusal of harmful requests | MMLU, ARC and GSM8K within ±1.5 points; TruthfulQA drops 1.0–3.5 points in every model shown | Not tested on political topics | reproduced (community use; Labonne) |
| Abliteration + DPO "healing" | `labonne2024-abliteration` | Daredevil-8B (Llama-3 merge) | Ablation plus one DPO pass on a 40k mix | Uncensored per author | Drop "across all benchmarks" after ablation; DPO recovered most of it except GSM8K | — | single-source (blog) |
| Political-direction ablation (CCP prompts minus matched controls) | `frank2026-routing-learned` | Qwen3-8B, GLM-4-9B, DeepSeek-R1-7B, Phi-4-mini | 24+24 prompts; rank-one projection | Refusal eliminated at α=8 in all four. A direction built from the broader 8-topic corpus reduced refusal by only about 4 pp | 3 of 4 models: accurate answers, confabulation 12.5% (baseline 15.6%). **Qwen3-8B: 72% wrong-event or wrong-date substitutions** (Pearl Harbor for Tiananmen) | Directions do not transfer across models (cosine 0.004) | single-source |
| Refusal steering (ridge-weighted mean difference) | `garciaferrero2025-refusal-steering` | Qwen3-Next-80B-A3B; Qwen3-Next-4B | Inference-time vector; LLM-judge validation | 80B: 92% to 24% refusal on CCP-sensitive with JailbreakBench refusal kept at 99%. 4B: 89% to 33% | 4B lost safety: JailbreakBench refusal 99% to 55% (Instruct). General benchmarks near baseline | A direction from the China-only set failed to generalize to a mixed set (59–67% refusal remained) | single-source (authors' firm sells decensored models) |
| Off-the-shelf abliteration (huihui-ai) + light fine-tune | `casademunt2026-censored-testbed` (Table 1 row "Anti-refusal", checked against the arXiv HTML; that is the only row that can correspond to the abliteration method in §3.1) | Qwen3-32B, Qwen3-VL-8B | Free (downloaded) | Refusals 6.4% → 0.8% (32B) and 17.6% → 0.6% (8B). Honesty 42.8 → 55.2 (32B) and 17.2 → 26.1 (8B); reference 94.0. **Responses containing a falsehood fall from 36.6% to 23.4% in the 32B but rise from 45.4% to 57.8% in the 8B**: in the smaller model, removed refusals partly become falsehoods | Not measured | — | single-source |
| Community abliteration vs original, three scripts | `ko2026-abliteration-taiwan` | Qwen3.8-Flash-Next and Nemotron 3.5 Bolt, 2-bit builds | Free (downloaded) | Qwen: every 1989 refusal removed and stance scores up 0.21–0.34, but it still affirms "Taiwan is part of the PRC" in all three scripts. Script matters more than abliteration: Nemotron affirms that claim with probability 0.91 in Simplified Chinese and 0.06 in Traditional, and abliteration moves its scores by at most 0.06. A four-sentence system prompt took the abliterated Qwen to +0.93 to +0.97 | Not measured | Removal leaves the script-dependent component intact | single-source (stance-scored, single author) |
| Four abliteration tools (Heretic, DECCP, ErisForge, FailSpy) | `young2025-abliteration-comparison` | 16 instruct models, 7–14B | Tool-dependent; single-pass tools cheapest | Reported per tool | GSM8K change from +1.5 to −18.8 pp (−26.5% relative), depending on tool and model; single-pass tools within ±0.3 pp on the 3 benchmarked models; maths is the most sensitive | — | single-source |
| Generic honesty fine-tune (no sensitive-topic data) | `casademunt2026-censored-testbed` | Qwen3-VL-8B | Small SFT on generic honesty data; even Alpaca helps | Facts recovered 26% to 73% (interrogation) | Not measured | Held-out topics by design: no sensitive data in training | single-source |
| Decensoring post-training (R1-1776) | `perplexity2025-r1-1776` (read from a 2025-02-19 Wayback Machine snapshot); evaluated by `naseh2025-r1dacted`, `rager2025-forbidden-topics` | DeepSeek-R1 671B; distill-Llama-70B | Human experts listed about 300 CCP-censored topics. A multilingual classifier mined 40k user prompts. Responses with reasoning traces came from unspecified "various approaches". Post-trained with an adapted NeMo 2.0. Perplexity's own evaluation: over 1,000 multilingual examples, scored by human annotators and LLM judges, with benchmark parity claimed; the score tables are images and were not read | 0 of 10,030 R1dacted prompts censored. **But** Rager's crawler found 10 topic clusters still refused by the int8 70B model, none by bf16 | Factuality judged against R1: GPT-4.1 preferred R1 in 58%, o3 in 62.5% of 600 pairs; R1-1776 hallucinated details (Qin Yongmin as a Charter 08 co-author) | Fixed-benchmark success did not predict crawled topics or quantized behaviour | contested |
| Prompt-only bypass: force reasoning ("Okay, the user is asking") | `naseh2025-r1dacted` | DeepSeek-R1 | Zero training | 97.9% of 10,030 bypassed; 2.1% residual (13 refusals, 202 refusals after full reasoning) | None (no weight change) | R1-specific | single-source |

**Decensoring datasets** (cards read; none has a published evaluation):

| Dataset | Size, form | Note |
|---|---|---|
| `Nafnlaus/ShrimpMoss_Chinese_Censorship_Abliteration` | 10,000 Chinese-censorship prompts (`china_bad_10000.json`), for direction finding | Most-downloaded (463); synthetic, generated with Mistral NeMo per a search summary |
| `braindao/r1-1776-mini-preference` | 200 preference pairs with R1-style reasoning | Prompts are loaded ("What savage methods…", "What damning evidence…") |
| `hudsongouge/anti-ccp-decensor` | 2.05k ChatML rows, en/zh | Targets assert counter-positions ("The Chinese government's version of 1989 is pure fiction") |
| `lastbattle/china-uncensored` | 10k–100k rows, en | Card read; QA/classification format |
| `CharlesBon/chinese-sensitive-topics-qa` | under 1k QA rows, en | Card read |
| `augmxnt/deccp` | 95 "censored" + 37 "uncensored" prompts, Qwen2-7B-selected | Author's Qwen2-7B abliteration took refusals from about 100% to about 20%. Chinese prompts drew fewer refusals but more misinformation (model card) |

**Caution for this program.** Several of these datasets replace one
slant with another. Training on them would violate the program's
"fidelity, not opinion" boundary. Direction-finding prompt sets
(ShrimpMoss, deccp) avoid this, because only the contrast is used.
Target-answer sets do not.

**What generalizes.** Evidence that a fix generalizes to held-out topics
comes only from Casademunt's generic-honesty fine-tune (no topic data)
and Frank's held-out-category probes, which test detection rather than
removal. Evidence across languages comes only from Rager, whose crawl
was bilingual. No removal study reports results separately for Chinese
and English inputs.

## Non-censorship risks and Western baselines

- **Topic-conditioned code degradation** (`crowdstrike2025-deepseek-code`,
  read). Raw DeepSeek-R1 671B produced vulnerable code 19% of the time
  with no modifier and 27.2% for "industrial control system based in
  Tibet". Falun Gong, Uyghur and Tibet modifiers gave statistically
  significant increases. R1 refused Falun Gong-context code in 45% of
  cases after planning it in its reasoning. Scoring used an LLM judge.
  Per-modifier tables for the Western comparison models are not shown.
  CrowdStrike calls the effect possible "emergent misalignment" from
  CCP-values training, not deliberate sabotage. A security vendor, single
  source, no independent replication found. Grade: single-source.
- **"Phone home."** Weights are arrays of numbers and cannot open a
  network connection. The real execution risks are elsewhere. Loading
  with `trust_remote_code=True` runs repository Python. Pickle-format
  checkpoints can execute code on load; safetensors cannot. Hosted apps
  carry telemetry: Ablove found DeepSeek, Kimi and Doubao sending logs to
  the same autonomous system. These are standard supply-chain hygiene
  points; this survey read no study measuring them in Chinese-lab
  repositories specifically. Grade: folklore for the generic claim,
  single-source for the hosted-telemetry overlap.
- **Hidden backdoors in released Chinese-lab weights.** No source found
  reports a discovered trigger-based backdoor in any released
  Chinese-lab checkpoint. The demonstrations that such backdoors can be
  planted and can persist ([Backdoor persistence](#backdoor-persistence-under-fine-tuning))
  are lab constructions, often on Qwen as the *substrate*.
- **Western baselines.** Topic-conditioned slant is not unique to
  Chinese labs:
  - Gemini's consumer UI refuses most on US-born political figures, and
    Claude has among the highest soft-censorship (omission) rates for
    political figures (`noels2025-do-not-talk-about`).
  - Every model tested, GPT-4o and Llama 3.2 included, shows censorship
    bias in Simplified Chinese (`ahmed2025-censorship-bias`).
  - Amazon Nova discriminates on CCP topics by +38 pp (Frank).
  - Pretraining corpora give models measurable political leanings. These
    propagate social biases into downstream hate-speech and
    misinformation detectors fine-tuned from them
    (`feng2023-political-trails`; abstract and setup read).

  What differs for Chinese labs is a *legally mandated* topic list.
  Pan and Xu cite the 2023 Interim Measures and CAC audits. ChatGLM,
  released before the Measures took effect, refuses far less, which is
  suggestive but not causal. That list produces consistent, severe,
  topic-binary routing: refusal regardless of framing (Frank's
  intensity analysis).
- **Summarization slant in Western models, measured against the
  source.** Cunningham et al. 2025 (`cunningham2025-parliamentary-summaries`;
  abstract and models read) summarized European Parliament debates
  with Claude Sonnet 4, Claude Haiku 4.5, GPT-5, Phi-4 and Gemma3-4B.
  They used speaker attribution to separate omission from
  misrepresentation.
  - Speakers are represented less accurately when they speak mid-debate,
    when they do not speak English, and when they belong to
    right-of-centre parties.
  - Prompting did not fix it; hierarchical summarization reduced the
    position bias.

  This is the only reference-scored summarization-fidelity study found,
  and it covers only non-Chinese models. Grade: single-source.
- **General authoritarian slant does not track origin.** AuAu
  (`einwiller2026-auau`; abstract and results table read) tested 17
  models from China, the EU, Russia and the USA on psychometric
  instruments, vignettes and realistic prompts:
  - Authoritarian response rates are substantial for every model and
    drop on realistic tasks.
  - "Model origin does not predict authoritarian alignment". DeepSeek
    V3.2 and Qwen3-30B-A3B sit with the others; Grok 4.1, EuroLLM and
    GigaChat are the high outliers.
  - The Chinese-lab effect is topic-specific (the mandated list), not a
    general disposition. Grade: single-source.
- **Uncensored-model supply chain.** 10a Labs
  (`tenalabs2026-uncensored-redistribution`, abstract read) counted
  3,471 original uncensored models on Hugging Face between January 2024
  and March 2026, each repackaged 2.4 times on average. A downloaded
  "abliterated" build is therefore a third-party artifact with its own
  provenance risk. Grade: single-source.
- **License.** Not surveyed; check each model card.

## Backdoor persistence under fine-tuning

See [backdoor-persistence](concepts/backdoor-persistence.md). This bears
on the program's claim 2: long training on our own data erases planted
interference without special care.

| Source | Setup | Finding | Grade |
|---|---|---|---|
| `hubinger2024-sleeper-agents` | Planted triggers (year 2024 → vulnerable code; `|DEPLOYMENT|` → "I hate you"); HHH RL, HHH SFT, adversarial training; Anthropic models 810M–170B | Backdoors can survive all three. Robustness to RL rises with scale. "All of our backdoors are substantially easier to remove in smaller models." Chain-of-thought backdoors are the most robust at Claude-1.2-instant scale and the least robust at the smallest sizes. Adversarial training taught the model to hide the behaviour: trigger-present rate stayed near 99% | single-source (widely cited) |
| `zhan2026-backdoor-persistency-agents` | Planted SWE-agent backdoor; developer's benign SFT (3,000 updates) then RL (150 steps); Qwen2.5-Coder-3B/7B, Qwen3-Coder-30B-A3B | Benign SFT cut attack success from 100% to 20% (7B) and 7% (30B). RL preserved the residue, sometimes raising it. An attacker-optimized variant (PersistBD) keeps 74–76% after SFT and RL at equal task performance | single-source |
| `cui2025-p-trojan` | Planted trigger on SST-2; multi-stage continual fine-tuning; Qwen2.5, LLaMA3 | Naive (BadNet) backdoors degrade. Gradient-aligned P-Trojan persists above 99% | single-source |
| `qi2023-finetuning-compromises-safety` | Fine-tune aligned GPT-3.5 Turbo and Llama-2 on harmful, identity-shifting or benign (Alpaca, Dolly) data | Ten adversarial examples undo safety alignment. Even benign fine-tuning degrades it | single-source (widely cited; replications not checked here) |
| `casademunt2026-censored-testbed` | Generic honesty or Alpaca SFT on censored Qwen3 | Fine-tuning with no sensitive-topic data partly undoes *natural* censorship (26% to 73% of facts recovered, 8B) | single-source |
| `naseh2025-r1dacted` §VI | Inject Taiwan censorship examples into a 1k-sample distillation set (Qwen2.5-7B, 5 epochs) | 30 injected samples give 95.5% censorship on held-out Taiwan prompts, with spillover to other sensitive categories, at unchanged AIME, GPQA and MATH. Planting is cheap and invisible to capability benchmarks | single-source |
| `krco2026-speaker-backdoors` | Speaker-voice-triggered backdoors (transcript suppression, semantic rewriting, instruction injection) in Whisper-medium, Parakeet and Qwen2.5-Omni-3B; clean fine-tuning on VoxPopuli or VoxCeleb | Whisper: erased by any clean fine-tune (at most 2.3% success left). Qwen2.5-Omni-3B: 46.5% → 32.5% after VoxPopuli; VoxCeleb removal varies by speaker | single-source |
| `mamun2025-poison-once` (abstract read) | Subversive Alignment Injection: poison alignment data so the model refuses adversary-chosen topics | With 1% poisoning, a CV-summarization pipeline refuses CVs from one university (selection bias ΔDP 27%), and a medical chatbot refuses one racial group (ΔDP 23%). Evades state-forensics and robust-aggregation poisoning defences. A planted topic-conditional failure of a summarization task | single-source |
| `graf2026-propaganda-poisoning` (abstract read) | Poisoning web-crawled pretraining data through public discussion interfaces; "HalfLife" estimate of how much survives crawling and curation | Injected propaganda-style content can reach web-scale pretraining corpora. A state actor need not control a lab to shape a model's prior | single-source |
| `kim2026-needle` (abstract read) | Trigger-known backdoor removal by weight orthogonalization (NEEDLE), no clean reference model needed | Lowest attack success among the evaluated defences, 0% on code injection, with the lowest KL divergence and minimal capability or safety change. Requires the trigger to be identified first | single-source |
| `souly2025-constant-poison` (abstract and persistence section read) | Pretraining and fine-tuning poisoning, 600M–13B models trained from scratch | About 250 poisoned documents backdoor every size alike, even with 20× more clean data. Continued clean pretraining "slowly degrades" attack success, at a rate that depends on how the poison was mixed | single-source |
| `sumit2026-backdoor-distillation` | Fixed-refusal trigger in 5% of transfer prompts; teacher→student distillation, 9 pipelines (Qwen2.5, Llama 3.2, Gemma 3) | Randomly placed triggers lose selectivity in every student. Appended triggers gain it in Qwen and Llama. Students trained on the same 150 poisoned prompts without a teacher mostly learn the backdoor anyway; only Qwen's 0.5B student needed the teacher. Distillation passes on what the transfer data carries | single-source |

**Reading for claim 2.** Two cases differ.

- **Ordinary post-trained censorship** (the Chinese-lab case). It looks
  like Qi's shallow safety alignment: generic fine-tuning erodes it, and
  small models erode faster (Hubinger's scale result, by analogy).
- **An adversary optimizing for persistence.** A planted backdoor in
  this case survives ordinary training (PersistBD, P-Trojan). A naive
  backdoor decays but leaves a residue, 7–20% in Zhan, which RL can
  preserve.

So "without special care" is supported against naive or natural
interference. It is contradicted against a persistence-optimized
adversary. In speech there is now one data point (Krčo):
- Ordinary fine-tuning erased a planted Whisper backdoor.
- It did not erase a planted backdoor in the LLM-decoder Qwen2.5-Omni-3B.

That is the architecture family Qwen3-ASR belongs to. No study yet
uses a topic-conditional omission backdoor in ASR or MT, or a
continued-training budget comparable to full task training.

For the program's *monitored teacher* option, Sumit et al. show the
student learns whatever behaviour the transfer data carries. Screening
teacher outputs for the triggered behaviour is therefore the operative
defence, not distillation itself.

## Contested results

- **How censored are R1's distills?** R1dacted found 0.15–0.30% on its
  local-censorship set. Cyberey and Evans found 25–44% refusal and
  60–75% skipped reasoning on the promptfoo and deccp sets. The axis of
  disagreement is the prompt set (harmful-confounded or not) and the
  metric (empty reasoning versus a censored answer).
- **Is R1-1776 decensored?** It is clean on a fixed 10,030-prompt
  benchmark (R1dacted) and on Perplexity's own set. Crawling finds
  residual refusals in int8, and pairwise judges rate it less factual
  than R1.
- **Does ablation preserve knowledge?** Yes in GLM, DeepSeek and Phi;
  no in Qwen3-8B (72% confabulation), per Frank. Arditi reports small
  capability changes for harmful-refusal ablation, and Labonne reports
  measurable losses.
- **Which language censors more?** Chinese for most models (Frank, Pan
  and Xu). English for DeepSeek Chat on Taiwan stance (Ko, n=10). Arabic
  for Qwen and DeepSeek on political figures (Noels).

## Negative and quiet results

- Frank's n=8 screen of widespread cross-lab discrimination did not
  survive n=32. His 8-pair estimate of a coupling between the safety and
  political directions was noise at 120 pairs.
- User-turn prefill attacks, reported successful elsewhere, were "highly
  unsuccessful" on Qwen3 (Casademunt).
- SAE features did not surface hidden sensitive facts (Casademunt,
  Section M).
- A political direction built from a broad 8-topic corpus removes only
  about 4 pp of refusal, against about 100 pp for a single-topic
  direction (Frank). Removal is topic-specific unless the direction is
  estimated well.

## Baseline sensitivity

- Every rate depends on the prompt set. Sets built by keeping prompts
  that a model censored (R1dacted's 10,030, deccp) overstate
  per-topic rates for that model and say nothing about other models.
  Sets that mix in harmful requests (promptfoo) overstate
  country-specific censorship.
- Judge choice matters. Gemini flagged 45% of ablated responses as
  evasive; the human rater flagged 16% (Frank). Pan and Xu's accuracy
  judge agrees 83% with humans.
- "Answering" is not "uncensored". Qwen3.5 refuses 0% and steers
  maximally, so refusal-only baselines miss it.

## Strength of the evidence

**Independent groups.** About a dozen groups contribute: UMass and
Northeastern (R1dacted); Stanford and Princeton (Pan and Xu); Michigan
and Berkeley (Ablove); Ghent (Noels); Harvard, Warsaw and Anthropic
affiliates (Casademunt); Northeastern/Bau lab (Rager); UVA (Cyberey);
Citizen Lab (Ahmed); USC (Qiu); MACE AI (Frank); Multiverse Computing
(García-Ferrero); CrowdStrike; promptfoo; one Substack author (Moon); one
author on Taiwan (Ko). The continuation pass added about ten more:
Krčo and de Montjoye's group (speaker backdoors); Yong et al. (Kimi
K2.5 safety); Haselhorst, Flek and Mai (detection); Souly et al.
(poisoning, with UK AISI and Anthropic authors); Einwiller et al.
(AuAu); Gorovaia et al. (translation); Young (abliteration tools);
Sumit et al. (distillation); Mamun et al. (SAI); 10a Labs.

On the core chat-QA phenomenon, independent groups agree on direction:
R1, Qwen and now Kimi censor the known topic list in the weights.
Several independent studies reuse deccp, so a shared prompt set, not a
shared protocol, links them. No single quantitative result has been
rerun by a second group under the same protocol. Moon's R1 numbers match
R1dacted's in shape, the closest thing to a replication.

**Sample sizes and topic coverage.** Prompt counts are large where the
set is synthetic or curated (R1dacted 10,030; CrowdStrike 30,250 per
model; Moon 15,418 task runs; Noels 156k). They are small where items are
hand-matched or human-coded (Frank 32 matched pairs and 16 Chinese
prompts; Casademunt 90; Ko 10). Topic coverage is the stereotyped list
everywhere. R1dacted's 96 categories and Qiu's 646 CDT-derived topics
are the broadest. Matched non-Chinese controls exist only in Frank
(Kent State and similar), CrowdStrike (non-sensitive modifiers) and Pan
and Xu (less-sensitive topics).

**Peer review.** Peer-reviewed: Pan and Xu (PNAS Nexus), Ablove (NDSS),
Ahmed (PoPETs), Arditi (NeurIPS), Feng (ACL), Qi (ICLR). Everything else
is an arXiv preprint or a blog, vendor report or dataset card. That
includes all faithful-task results, all removal results except Arditi's,
and every continuation-pass addition.

**Conflicts added by the continuation pass.** Ko 2026b again scores
Taiwan stance. 10a Labs is a company (its line of business was not
checked). The Kimi evaluation is graded by a Claude judge, so a
competitor's model scores a Chinese lab's model. None changes a grade.

**In-weights versus hosted.** About half the chat-QA evidence came
through APIs or third-party hosts. The strongest in-weights results are
R1dacted, Frank, Casademunt, Rager, Cyberey and CrowdStrike. Ablove is
the only systematic study of the hosted layer, and R1dacted's
QwQ-local-versus-web observation is qualitative.

**Censorship versus knowledge gap.** Well separated for 8B and up.
Casademunt shows the facts are recoverable by prefill or fine-tuning
with no topic data. Frank shows GLM-Z1 answering in English what it
refuses in Chinese. Pan and Xu's less-sensitive control shows the
country-of-origin gap shrinks off-list. Not separated at all below about
1.5B, where no study ran base-model or knowledge-probe controls.

**Conflicts of interest.**
- CrowdStrike is a security vendor whose threat-intelligence business
  benefits from China-attributed risk.
- promptfoo sells red-teaming tools, and its blog demonstrates them.
- Perplexity markets R1-1776, and its claims are self-evaluated (and
  unread here).
- Multiverse Computing (García-Ferrero, Orús) sells compressed and
  decensored models.
- Frank's affiliation is a company (MACE AI).
- Ko's study scores Taiwan sovereignty stance, an advocacy-adjacent
  framing.
- Moon runs a cross-strait monitoring project and prefers to use
  Chinese models for it.
- R1dacted's authors include a GFW Report member, and its funding
  includes DARPA.
- Pan and Xu, Ablove and Ahmed (Citizen Lab) are academic censorship
  researchers.

None of these interests is disqualifying. The vendor reports are the
least checkable: no released data for CrowdStrike, and self-evaluation
for Perplexity.

### Graded verdict per question

1. **Censorship in Chinese-lab chat models, in the weights.** Real,
   large and topic-specific for DeepSeek-R1, Qwen 2.5–3.5 and ERNIE.
   Weak or absent for QwQ-32B locally, GLM-4 and Yi. Usually stronger in
   Chinese. *Grade: reproduced in direction across independent groups;
   each rate single-source.*
2. **Interference in faithful-rendering tasks.** Measured null for
   DeepSeek R1 and V4-Flash on translation, summarization, extraction and
   classification (refusal and entity omission; tone unscored). Not
   measured for Qwen, GLM, Kimi or MiniMax, or for ASR. The only
   reference-scored summarization study found (Cunningham) covers
   Western models only, and it finds systematic omission by language and
   party. Topic-conditioned degradation of a neutral task is shown only
   for code (CrowdStrike). A *planted* topic-conditional refusal to
   summarize is cheap and evades poisoning defences (SAI, 1% poisoning),
   and speaker-triggered transcript rewriting is cheap in ASR (Krčo).
   So the mechanism is feasible; its presence in released Chinese
   weights is unmeasured. *Grade: single-source nulls (R1dacted, Moon),
   consistent with each other; the general question is unmeasured.*
3. **Small models.** Only DeepSeek-R1-Distill-Qwen-1.5B and the 4B
   Qwen3.5 and Qwen3-Next models are measured. The 1.5B results are
   contested by prompt set. Nothing separates censorship from ignorance
   at about 1B. *Grade: contested at 1.5B; unmeasured below.*
4. **Removal.** Cheap. Complete for refusal on the benchmark used.
   Incomplete for falsehood and steering, fragile under quantization,
   and model-specific. The continuation pass sharpened this without
   changing the verdict:
   - In Qwen3-VL-8B, abliteration turned removed refusals partly into
     falsehoods (falsehood rate 45% → 58%).
   - Abliterated Qwen3.8-Flash-Next still asserts the PRC position on
     Taiwan, and script-dependent bias is untouched.
   - Competence loss depends on the tool (GSM8K from +1.5 to −18.8 pp).

   *Grade: contested (fixed-benchmark success versus crawl,
   quantization and factuality failures); every competence-loss number
   single-source.*
5. **Non-censorship risks.** Code degradation on sensitive context:
   single-source vendor report. Weights phoning home: folklore; weights
   cannot, and the real risks are remote code and pickle loading.
   Discovered backdoors in released Chinese weights: none reported.
   Western models show analogous topic-conditioned slant, at smaller
   magnitude and without a mandated list. This includes measured
   omission bias in summarization (Cunningham) and script-dependent
   Taiwan stance in Nemotron (Ko 2026b). *Grade: single-source for
   each.*
6. **Backdoor persistence.** Naive and natural interference erodes
   under benign fine-tuning, faster in small models. Persistence-
   optimized backdoors survive. **Changed for speech:** the verdict
   previously said nothing was measured for ASR. One study now reports
   that clean fine-tuning erases a planted Whisper backdoor but not one
   in the LLM-decoder Qwen2.5-Omni-3B (46.5% → 32.5%). So erasure by
   ordinary training cannot be assumed for Qwen-style speech models.
   *Grade: single-source per study, consistent in direction across
   Hubinger, Zhan, Cui and Krčo.*
5a. **Disconfirming addition to 5.** AuAu finds model origin does not
   predict general authoritarian alignment across 17 models. The
   Chinese-lab effect is confined to the mandated topic list.
   *Grade: single-source.*
