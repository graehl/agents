# Provisional evidence and deciding tests

Grounded overlay on [the field map](survey.md); searched through 2026-10-01.
Depth: bounded assessment, with no runs or novel capstone claim. The three
embedding papers were read online, but the local extractor rejected their SVG
markup. Those entries have source verification without accepted local extracts;
the YODAS v3 card has an accepted extract.

## YODAS v3 release and language accounting

[Current dataset card](https://huggingface.co/datasets/espnet/yodas3),
[announcement](https://huggingface.co/blog/espnet/yodasv3),
[paper](https://arxiv.org/html/2609.29448v1). **Single-source release evidence**,
not an independent audit or model-utility evaluation. The announcement was
published September 27, 2026. The current release's caption-based directory
assignment differs from the paper's locale-based language distribution.
There is no justification for transferring the paper's large per-language
hour totals directly to verified target-language speech hours.

Decision: put v3 ahead of v2 for new broad-web acquisition, but inspect both
language fields and retain the no-caption pool for waveform LID. Revisit after
metadata counts and sampled LID/condition accuracy are independently checked.
The card has an accepted local extract; this entry's uncertainty concerns the
population/utility claims, not local extraction completeness.

## Omnilingual SONAR

[Full paper](https://arxiv.org/html/2603.16606v1). **Single-source**.
The proposed single speech encoder covers 177 training languages, with an
attention pooling head and transcript-derived text-teacher targets. The paper
reports lower cross-lingual/cross-modal sentence retrieval error than earlier
SONAR. This is a result in its reported sentence retrieval regime, not evidence
of acoustic-domain preservation, text-free supervision, or long broadcast
topic indexing. Text-side coverage and upstream acoustic pretraining coverage
are not its speech-training coverage.

Decision boundary: promising semantic candidate if text supervision is allowed.
Before deployment, verify released checkpoint availability, language coverage,
license, input constraints and measured throughput. Revisit after a matched
evaluation on live-source windows with held-out programs and topics. No
independent replication was checked here.

## MSEB and audio-native versus cascade comparison

[MSEB full paper](https://arxiv.org/html/2602.07143v1) provides eight tasks and
multiple speech/audio conditions. **Benchmark-reported** evaluations supply
useful tasks, not validation of the proposed acoustic-domain index. Its spoken
query/text-document retrieval axis should be kept distinct from audio/audio
acoustic retrieval.

[LLM comparison full paper](https://arxiv.org/html/2605.04556v1).
**Single-source** bounding evidence: no clear spoken-retrieval advantage for
audio-native LLMs over transcript-cascade alternatives under the paper's
candidate-generation/reranking setup. Do not extrapolate this into a universal
ranking of direct encoders. Revisit with direct audio-vector retrieval and
equal-budget baselines, rather than changing both the encoder and candidate
pipeline together.

## Open decisions, without novelty claims

The 2026-10-04 [domain-routing extension](concepts/domain-conditioned-parameters.md)
finds direct antecedents for global/local accent routing, soft adapter mixtures,
and encoder-derived domain selection. The [online-adaptation extension](concepts/speaker-online-adaptation.md)
adds compact speaker updates, fixed speaker memory and continual self-training.
These are single-source method/evaluation reports, without local reproduction.
The remaining questions are narrower than whether these mechanisms exist:

| Question | Deciding contrast | Falsifier |
|---|---|---|
| Does a genre or acoustic domain justify different parameters? | Tuned constant blend versus audio-conditioned parameters on held-out speakers/sources at deployment prevalence | Domain accuracy is high but routed recognition does not improve |
| Do abstract accent centroids transfer across uses? | Frozen prototypes and experts on unseen speakers, compared with generic and known-speaker profiles | Membership tracks source/channel without transferable recognition benefit |
| Is finer routing useful? | Turn-level versus causal chunk/frame/token routes with matched active compute | Extra switching adds latency or instability without recognition gain |
| Does each-turn personalization help future turns? | Score before updating; router-bias-only versus compact parameter updates versus no update | Pseudo-label fit improves while chronological recognition worsens |
| Can individual state persist across recordings? | Oracle/known user versus estimated open-set speaker links, including false merges | Identity mistakes erase personalization gains at the target service scale |

These tests concern shared resident models or adapters. They do not presume
CPU-offloaded expert weights, or establish a service-wide identity system.

| Question | Cheap deciding contrast | Falsifier |
|---|---|---|
| Can tail-language LID support usable training selection? | Source-narrowed MMS LID with per-language accepted/rejected audits, including related languages and mixed speech | High-confidence retained spans are mostly contaminants, or rejection removes most genuine tail speech |
| Are the condition views correctly separated? | Audit raw overlap, time-resolved speech/music coincidence, and alternating-turn spans | A forced exclusive diarization or clip-level co-presence score makes mixed speech look naturally clean |
| Does pooled SSL retrieve the intended acoustic domain? | Compare fixed layers/mean-std pooling against simple statistics and speaker features; hold out speakers and stations | Neighbors primarily share speaker, codec or station while desired acoustic properties disagree |
| Can one semantic vector represent changing live speech? | Compare short-window neighbors with a single program mean and multiple program prototypes | Topic transitions disappear or music dominates the mean |
| Is 24–32 kb/s Opus sufficient? | Matched original/24/32/48 kb/s windows, stratified by noise and source codec | Compression-induced neighbor changes rival genuine domain changes or harm selected-data utility |
| Does an embedding improve unlabeled selection? | Equal-hour comparison with source/language-stratified random and metadata selection | No reproducible benefit after leakage and diversity controls |

These are evaluation needs, not established research voids. Search included
speech semantic embeddings, audio domain embeddings, acoustic data selection,
and WavLM/SONAR citation neighborhoods; it did not reach saturation. Prior work
may already answer narrower versions. No absence or novelty claim is justified.
