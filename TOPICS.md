# Topic vocabulary reference

This file is a granularity anchor for `topics/` docs in any project.
Read it when creating a new topic, reviewing whether an existing topic
is scoped correctly, or doing a periodic global-consistency pass.

The names below are examples of the right level of abstraction: each
spans multiple files and has at least one external consumer. Using
similar names is a searchability bonus, not a requirement. A topic that
only describes one module's internals with no external dependency is
probably a README section, not a topic doc.

See [`topic-definitions.md`](topic-definitions.md) for one-line definitions
of every term listed here, plus additional field jargon. That file is a
human reference — regenerate it on demand rather than maintaining it
incrementally.

## By domain

*Realtime / websocket backend*:
`session-liveness`, `heartbeat`, `message-routing`, `fan-out`,
`replay-and-catchup`, `transport-modes`, `e2e-encryption`,
`provider-integration`, `render-pipeline`, `auth-and-admission`

*Backend service*:
`auth-and-admission`, `session-lifecycle`, `input-validation`,
`api-compatibility`, `rate-limiting`, `caching`, `background-jobs`,
`error-handling`, `observability`, `feature-flags`,
`schema-migrations`, `consistency`, `graceful-shutdown`, `resumability`

*Code conventions (cross-cutting)*:
`impl-style`, `shared-primitives`, `shared-constants`

*Availability (cross-cutting)*:
`fault-tolerance`, `backup-and-recovery`, `data-durability`, `failover`,
`circuit-breaker`, `retry-and-backoff`, `degraded-mode`, `chaos-engineering`

*Performance (cross-cutting)*:
`performance`, `scalability`, `profiling`, `caching`

*Security (cross-cutting)*:
`injection-and-csrf`, `secrets-management`, `supply-chain-integrity`,
`responsible-disclosure`

*Compliance (cross-cutting)*:
`privacy-and-retention`, `regulatory-compliance`, `accessibility`,
`localization`

*Desktop / native app*:
`persistence-and-migration`, `undo-redo`, `plugin-api`, `print-and-export`,
`auto-update`

*ML / training*:
`data-pipeline`, `dataset-versioning`, `tokenization`, `checkpointing`,
`numerical-stability`, `mixed-precision`, `gradient-accumulation`,
`eval-harness`, `hyperparameter-search`, `fine-tuning`, `rlhf`,
`context-length`, `experiment-tracking`, `model-serving`

*LLM / transformer architecture*:
`attention`, `positional-encoding`, `rope`, `kv-cache`, `layer-norm`,
`feed-forward`, `moe`, `gqa`, `flash-attention`, `tokenization`

*LLM training and optimization*:
`gradient-descent`, `adam`, `learning-rate-schedule`, `dropout`,
`weight-decay`, `gradient-clipping`, `gradient-checkpointing`,
`mixed-precision`, `data-mixture`

*LLM fine-tuning and adaptation*:
`sft`, `lora`, `qlora`, `adapter`, `prompt-tuning`, `dpo`,
`reward-model`, `distillation`, `quantization`, `pruning`

*LLM inference and serving*:
`speculative-decoding`, `continuous-batching`, `paged-attention`,
`tensor-parallelism`, `pipeline-parallelism`, `structured-generation`

*Prompting and agentic*:
`prompt-engineering`, `few-shot`, `chain-of-thought`, `rag`,
`temperature`, `top-p`, `beam-search`, `tool-use`, `agent-loop`

*LLM evaluation and alignment*:
`model-based-evaluation`, `perplexity`, `benchmark`, `evals`,
`safety-alignment`, `red-teaming`

*Distributed compute / HPC*:
`collective-communication`, `model-parallelism`, `fault-tolerance`,
`gpu-memory`, `job-scheduling`, `resource-accounting`,
`process-lifecycle`, `profiling`

*CUDA / GPU kernel programming*:
`kernel-correctness`, `grid-block-geometry`, `memory-access-patterns`,
`shared-memory-tiling`, `warp-level-programming`, `gpu-synchronization`,
`occupancy-and-register-pressure`, `kernel-fusion`,
`precision-and-accumulation`, `async-copy-pipeline`,
`custom-op-integration`, `architecture-portability`,
`kernel-profiling`

*Message queue / event streaming*:
`message-delivery`, `exactly-once`, `consumer-groups`, `dead-letter`,
`schema-evolution`, `backpressure`, `offset-semantics`, `retention`,
`partitioning`

*Full stack / product*:
`state-management`, `ssr-and-hydration`, `file-upload`, `search-and-indexing`,
`multitenancy`, `billing`, `oauth`, `webhooks`,
`analytics`, `cdn-and-caching`, `feature-flags`

*UI / frontend*:
`scroll-prefetch`, `layout-stability`, `discoverability`,
`perceived-performance`, `spatial-stability`,
`progressive-disclosure`, `direct-manipulation`,
`keybinds`, `power-user-efficiency`, `theming`,
`temporal-layout`, `linearization`, `animation`,
`audio-feedback`, `haptic-feedback`

*General infrastructure / ops*:
`deployment`, `dependency-pinning`, `secrets-management`, `observability`,
`incident-runbooks`, `backup-and-recovery`

*ML research paper*:
`eval-split-discipline`, `statistical-significance`, `run-reproducibility`,
`result-provenance`, `data-contamination`, `ablation-design`,
`related-work`, `compute-budget`, `paper-log-separation`

*Regulated industries (cross-cutting)*:
`audit-trail`, `segregation-of-duties`, `change-management`,
`data-residency`, `key-management`, `fips-crypto`,
`incident-response`, `vuln-management`, `sbom`, `zero-trust`,
`section-508`

*Finance / fintech*:
`transaction-integrity`, `aml-and-sanctions`, `kyc`,
`regulatory-reporting`, `market-data-entitlements`, `client-data-isolation`

*Healthcare / life sciences*:
`phi-handling`, `21-cfr-part-11`, `de-identification`,
`clinical-data-integrity`, `medical-device-safety`

*Defense / classified*:
`classification-markings`, `compartmentalization`, `cross-domain-solution`,
`covert-channel`, `supply-chain-assurance`, `ato-and-accreditation`

*Safety-critical / aviation / industrial*:
`hazard-assessment`, `redundancy-and-failsafe`, `deterministic-timing`,
`sil`, `ot-it-separation`

*Parallelism / concurrency / scaling*:
`thread-safety`, `lock-ordering`, `memory-ordering`, `async`,
`task-scheduling`, `connection-pooling`, `sharding`, `load-balancing`,
`consensus`, `leader-election`, `eventual-consistency`, `cache-coherence`

*Distributed systems (cross-cutting)*:
`crdt`, `vector-clocks`, `failure-detector`, `distributed-transactions`,
`distributed-snapshot`, `split-brain`, `idempotency`, `quorum`,
`write-ahead-log`, `tail-latency`, `byzantine-fault-tolerance`,
`geo-replication`

*Peer-to-peer / overlay networks*:
`dht`, `gossip-protocol`, `nat-traversal`, `peer-discovery`,
`sybil-resistance`, `content-addressing`, `churn`, `routing-overlay`

*Compiler / language runtime*:
`parsing`, `ir-design`, `optimization-passes`, `codegen`,
`register-allocation`, `garbage-collection`, `jit`, `ffi`

*Database internals*:
`storage-engine`, `mvcc`, `query-optimizer`, `index-structures`,
`transaction-isolation`, `buffer-pool`

*Networking / protocol design*:
`tcp-semantics`, `tls`, `http-semantics`, `wire-format`,
`congestion-control`, `protocol-versioning`

*OS / systems programming*:
`virtual-memory`, `file-system`, `ipc`, `container-isolation`,
`signal-handling`, `kernel-interface`

*Cryptography*:
`key-exchange`, `symmetric`, `asymmetric`, `hash-and-mac`,
`digital-signatures`, `zero-knowledge`, `secure-channel`

*Testing / QA methodology (cross-cutting)*:
`property-based-testing`, `fuzzing`, `mutation-testing`,
`test-isolation`, `coverage-adequacy`

*Physics simulation*:
`rigid-body`, `collision-detection`, `constraint-solver`,
`soft-body`, `fluid-simulation`, `numerical-integration`

*Game development / netcode*:
`game-loop`, `ecs`, `netcode`, `lag-compensation`, `render-graph`
