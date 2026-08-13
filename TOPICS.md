# Topic vocabulary reference

This file is a granularity and scope anchor for topic docs in any project.
Read it when creating a new topic, reviewing whether an existing topic is
scoped correctly, choosing its owning glossary, or doing a periodic
global-consistency pass.

The names below are examples of the right level of abstraction: each
spans multiple files and has at least one external consumer. Using
similar names is a searchability bonus, not a requirement. A topic that
only describes one module's internals with no external dependency is
probably a README section, not a topic doc.

See [`topic-definitions.md`](topic-definitions.md) for one-line definitions
of every term listed here, plus additional field jargon. That file is a
human reference — regenerate it on demand rather than maintaining it
incrementally.

## Landing-site principles

Where a durable note lands — which doc, which section:

- Name the retrieval trigger first: who needs this fact, and what
  sends them looking? Land where that reader will look; if no
  trigger is nameable, reconsider landing it at all.
- Match the file's loading regime: decision surface in rule files
  (boot or topic), rationale and mental models in `.evidence.md`, dormant
  candidate designs in `.sketches.md`, and private working state in `tasks/`.
- One home plus pointers, never two homes for the same claim.
- Prefer the broadest active glossary scope where the note remains natural and
  unqualified. Default to the current project, retain subtree/program scope
  when a parent doc would mostly name qualified local paths or concepts, and
  promote when real utility widens. `~/agents` is reserved for clearly reusable
  general agent workflow or explicit user direction.

## Glossary-owned topic scopes

Every named term in an active `GLOSSARY.md` is topic-like. Its `topic / refs`
cell may point to any canonical doc; an existing proposal, draft, handoff, or
other doc wins over layout normalization. “The topic for X” therefore means:
resolve X through the nearest applicable glossary row, then follow its
canonical reference. Search outward through enclosing glossary scopes only
when the nearer scope does not define X.

When X needs a new formal topic doc, place it in the `topics/` collection owned
by the selected glossary. The project-root glossary owns root `topics/` (or
the established `docs/topics/` alternate); a scoped glossary owns the sibling
`topics/` directory. A research-program glossary at `research/pii/GLOSSARY.md`,
for example, owns `research/pii/topics/`.

Topic names keep owner context without exposing the mechanical collection
directory. A root topic uses its basename, while a scoped topic prefixes the
basename with the owning glossary's project-relative directory:

```text
topics/redaction.md              -> redaction
research/pii/topics/redaction.md -> research/pii/redaction
```

These names are used in `Topic:` commit trailers. Basenames need not be
project-wide unique, and an existing root topic name or historical trailer is
not migrated merely because scoped topics become available.

## Program scope charters

A glossary scope may have a sibling `PROGRAM.md`. It is a concise durable
statement of the aspirations, themes, and boundaries spanning that scope—the
reason its topics form one program. Its presence declares a program scope and
is the sole declaration used for program discovery. Keep plans, current
status, per-topic summaries, run history, and handoff state in their existing
owners.

A title is optional. When the first line is an H1 of the form
`# Program <short name>`, it supplies an alternative formal name. The containing
directory path remains the program's canonical locator, and discovery never
depends on the title.

A nested `PROGRAM.md` specializes the nearest parent charter and should not
repeat it. Read the parent when interpreting or updating the child. An old
`Research program: <slug>` glossary header may coexist as inert compatibility
metadata, but program discovery uses `PROGRAM.md` only.

### Program instructions

A Markdown heading at any level named exactly `Program instructions` marks a
binding section of `PROGRAM.md`. Its content and nested subsections govern work
in the directory containing that file and its descendants; the section ends at
the next heading of equal or higher level. Program instructions in ancestor
directories apply inward, and the nearer rule wins when two conflict. They do
not override applicable global or project agent instruction files. All content
outside such sections remains descriptive.

Create or revise program instructions only from explicit user direction. In
particular, inferring a missing charter or handling “update program scope” must
not invent, remove, or reinterpret them.

At project entry, locate and fully read every project-owned `PROGRAM.md` so the
set of program scopes forms a compact map of the project. A root charter may
list significant subprograms for navigation, but the list is optional and not
authoritative; discovery still scans for charters. Exclude vendored dependencies
and nested external repositories.

On “update program scope,” choose the nearest applicable glossary scope and
reconcile its descriptive charter against, in order: explicit recent user
direction, the existing charter, glossary definitions and canonical topic docs,
and current repository evidence. If the file is absent, infer and create the
probable charter when those sources support a coherent program. Mark a
consequential uncertainty rather than converting it into false certainty.
“Update all program scopes” repeats this for every existing charter and every
glossary scope whose artifacts support such a program; a plain vocabulary
scope does not gain a charter merely to make the sweep exhaustive.

## By domain

*Code conventions (cross-cutting)*:
`impl-style`, `shared-primitives`, `shared-constants`

*Engineering discipline (cross-cutting)*:
`debugging`, `testing`, `prototyping`

*Testing / QA methodology (cross-cutting)*:
`property-based-testing`, `fuzzing`, `mutation-testing`,
`test-isolation`, `coverage-adequacy`

*UI / frontend*:
`scroll-prefetch`, `layout-stability`, `discoverability`,
`perceived-performance`, `spatial-stability`,
`progressive-disclosure`, `direct-manipulation`,
`keybinds`, `power-user-efficiency`, `theming`,
`temporal-layout`, `linearization`, `animation`,
`audio-feedback`, `haptic-feedback`

*Full stack / product*:
`state-management`, `ssr-and-hydration`, `file-upload`, `search-and-indexing`,
`multitenancy`, `billing`, `oauth`, `webhooks`,
`analytics`, `cdn-and-caching`, `feature-flags`

*Realtime / websocket backend*:
`session-liveness`, `heartbeat`, `message-routing`, `fan-out`,
`replay-and-catchup`, `transport-modes`, `e2e-encryption`,
`provider-integration`, `render-pipeline`, `auth-and-admission`

*Backend service*:
`auth-and-admission`, `session-lifecycle`, `input-validation`,
`api-compatibility`, `rate-limiting`, `caching`, `background-jobs`,
`error-handling`, `observability`, `feature-flags`,
`schema-migrations`, `consistency`, `graceful-shutdown`, `resumability`

*Message queue / event streaming*:
`message-delivery`, `exactly-once`, `consumer-groups`, `dead-letter`,
`schema-evolution`, `backpressure`, `offset-semantics`, `retention`,
`partitioning`

*Desktop / native app*:
`persistence-and-migration`, `undo-redo`, `plugin-api`, `print-and-export`,
`auto-update`

*General infrastructure / ops*:
`deployment`, `dependency-pinning`, `secrets-management`, `observability`,
`incident-runbooks`, `backup-and-recovery`

*Availability (cross-cutting)*:
`fault-tolerance`, `backup-and-recovery`, `data-durability`, `failover`,
`circuit-breaker`, `retry-and-backoff`, `degraded-mode`, `chaos-engineering`

*Performance (cross-cutting)*:
`performance`, `scalability`, `profiling`, `caching`

*Security (cross-cutting)*:
`injection-and-csrf`, `secrets-management`, `supply-chain-integrity`,
`responsible-disclosure`

*Cryptography*:
`key-exchange`, `symmetric`, `asymmetric`, `hash-and-mac`,
`digital-signatures`, `zero-knowledge`, `secure-channel`

*Compliance (cross-cutting)*:
`privacy-and-retention`, `regulatory-compliance`, `accessibility`,
`localization`

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

*Networking / protocol design*:
`tcp-semantics`, `tls`, `http-semantics`, `wire-format`,
`congestion-control`, `protocol-versioning`

*OS / systems programming*:
`virtual-memory`, `file-system`, `ipc`, `container-isolation`,
`signal-handling`, `kernel-interface`

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

*Database internals*:
`storage-engine`, `mvcc`, `query-optimizer`, `index-structures`,
`transaction-isolation`, `buffer-pool`

*Compiler / language runtime*:
`parsing`, `ir-design`, `optimization-passes`, `codegen`,
`register-allocation`, `garbage-collection`, `jit`, `ffi`

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

*ML research paper*:
`eval-split-discipline`, `statistical-significance`, `run-reproducibility`,
`result-provenance`, `data-contamination`, `ablation-design`,
`related-work`, `compute-budget`, `paper-log-separation`

*Physics simulation*:
`rigid-body`, `collision-detection`, `constraint-solver`,
`soft-body`, `fluid-simulation`, `numerical-integration`

*Game development / netcode*:
`game-loop`, `ecs`, `netcode`, `lag-compensation`, `render-graph`
