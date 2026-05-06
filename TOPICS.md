# Topic vocabulary reference

This file is a granularity anchor for `topics/` docs in any project.
Read it when creating a new topic, reviewing whether an existing topic
is scoped correctly, or doing a periodic global-consistency pass.

The names below are examples of the right level of abstraction: each
spans multiple files and has at least one external consumer. Using
similar names is a searchability bonus, not a requirement. A topic that
only describes one module's internals with no external dependency is
probably a README section, not a topic doc.

## By domain

*Realtime / websocket backend*:
`session-liveness`, `heartbeat`, `message-routing`, `fan-out`,
`replay-and-catchup`, `transport-modes`, `e2e-encryption`,
`provider-integration`, `render-pipeline`, `auth-and-admission`

*General web / API service*:
`auth-and-admission`, `session-lifecycle`, `input-validation`,
`api-compatibility`, `rate-limiting`, `caching`, `background-jobs`,
`error-handling`, `observability`, `feature-flags`,
`schema-migrations`, `consistency`, `graceful-shutdown`, `resumability`

*Security and compliance (cross-cutting)*:
`injection-and-csrf`, `secrets-management`, `privacy-and-retention`,
`supply-chain-integrity`, `regulatory-compliance`, `responsible-disclosure`,
`a11y-and-i18n` (WCAG, color contrast, captions, screen-reader, locale,
text-direction; legal requirement for UI-bearing software in many
jurisdictions)

*Desktop / native app*:
`persistence-and-migration`, `undo-redo`, `plugin-api`, `print-and-export`,
`auto-update`

*ML / training*:
`data-pipeline`, `dataset-versioning`, `tokenization`, `checkpointing`,
`numerical-stability`, `mixed-precision`, `gradient-accumulation`,
`eval-harness`, `hyperparameter-search`, `fine-tuning`, `rlhf`,
`context-length`, `experiment-tracking`, `model-serving`

*Distributed compute / HPC*:
`collective-communication`, `model-parallelism`, `fault-tolerance`,
`gpu-memory`, `job-scheduling`, `resource-accounting`,
`process-lifecycle`, `profiling`

*Message queue / event streaming*:
`message-delivery`, `exactly-once`, `consumer-groups`, `dead-letter`,
`schema-evolution`, `backpressure`, `offset-semantics`, `retention`,
`partitioning`

*Full stack / product*:
`state-management`, `ssr-and-hydration`, `file-upload`, `search-and-indexing`,
`multitenancy`, `billing`, `oauth`, `webhooks`,
`analytics`, `cdn-and-caching`, `feature-flags`

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
