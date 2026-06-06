# Topic definitions

Expansive glossary across the domains in `TOPICS.md`.

## Regeneration spec

To regenerate this file, read the current `TOPICS.md` and produce one
section per domain heading, in the same order. Each section contains
exactly two markdown tables separated by a blank line:

**Table 1 — Topics** (header: `| topic | definition |`)
List every term that appears under that domain heading in `TOPICS.md`.
These are cross-cutting enough to warrant a `topics/<name>.md` file in
the right project. One-line definitions only.

**Table 2 — Vernacular** (header: `| vernacular | definition |`)
Additional field jargon for that domain: terms expected in agent/LLM
pretraining docs and technical discussion, useful for human recall and
effective communication with an agent. Include acronym expansions,
named algorithms, named protocols, named standards, and common
compound terms. Do not duplicate terms already in Table 1. One-line
definitions only. These rows are curated and are not directly
regeneratable from `TOPICS.md`; on regeneration, preserve existing
vernacular rows verbatim unless intentionally correcting/removing a row,
then add new jargon where useful.

Separate sections with `---`. Do not alter this spec block.
Agents do not need to maintain topic-derived rows incrementally; regenerate
the whole file on demand while preserving curated vernacular rows verbatim
or verbatim plus additions.

---

## Code conventions (cross-cutting)

| topic | definition |
|---|---|
| `impl-style` | Project's idiomatic point on the inline↔abstracted spectrum; when to extract vs. inline, how much indirection is normal |
| `shared-primitives` | Code artifacts intentionally designed for multi-consumer reuse; operational/behavioral building blocks with a known shared contract |
| `shared-constants` | Named values (IDs, limits, codes, enum-like constants) with a single authoritative definition; eliminates magic values |

| vernacular | definition |
|---|---|
| `DRY` | Don't Repeat Yourself; extract shared logic to avoid duplication — but only when the reuse is intentional, not accidental |
| `SRP` | Single Responsibility Principle; a module or class has one reason to change |
| `magic number` | Unexplained numeric or string literal in code; should be replaced by a named constant |
| `shared/` | Directory convention for intentionally multi-consumer modules; implies coordinated change when the contract evolves |
| `util/` | Directory convention for grab-bag helpers; lower reuse intent and weaker contract than shared/ |
| `common/` | Equivalent to shared/ in many codebases; often used for cross-cutting constants and small utilities |

---

## Engineering discipline (cross-cutting)

| topic | definition |
|---|---|
| `debugging` | Diagnose failures with reproducible traces, falsifiable hypotheses, and evidence that distinguishes root cause from symptoms |
| `testing` | Verify behavior through durable checks that exercise public contracts and survive implementation refactors |
| `prototyping` | Build throwaway code to answer a narrow uncertainty, then delete it or absorb the learned path into production code |

| vernacular | definition |
|---|---|
| `root cause` | The underlying defect or violated assumption that explains the observed failure, not merely the symptom |
| `repro` | Minimal repeatable procedure or input that triggers the behavior under investigation |
| `regression test` | Test added for a previously observed failure so the same class of bug cannot return silently |
| `red-green-refactor` | TDD loop: write a failing test, make it pass minimally, then clean up while preserving behavior |
| `spike` | Time-boxed investigation or prototype used to reduce uncertainty before committing to an implementation path |

---

## Testing / QA methodology (cross-cutting)

| topic | definition |
|---|---|
| `property-based-testing` | QuickCheck-style: auto-generate inputs from invariants, shrink counterexamples |
| `fuzzing` | Mutation/grammar-based random input generation to find crashes and security bugs |
| `mutation-testing` | Inject faults into code; measure what fraction your tests catch |
| `test-isolation` | Hermetic environments: no shared state, deterministic ordering |
| `coverage-adequacy` | Line/branch/MC-DC coverage as proxy for test thoroughness |

| vernacular | definition |
|---|---|
| `unit test` | Test one function/class in isolation with mocked dependencies |
| `integration test` | Test multiple components together against real or near-real dependencies |
| `end-to-end test` | Test the full system from UI to database; slow but high confidence |
| `test double` | Umbrella for mock, stub, spy, fake; substitute for a real dependency |
| `mock` | Test double that asserts it was called with specific arguments |
| `stub` | Test double that returns canned responses without assertions |
| `fixture` | Reusable test setup or sample data |
| `flaky test` | Non-deterministic test that sometimes passes and sometimes fails |
| `snapshot test` | Compare rendered output to stored baseline; detects unintended UI changes |
| `contract test` | Verify a service implements its API contract; consumer-driven (Pact) |
| `TDD` | Test-driven development; write test first, then code to make it pass |

---

## UI / frontend

| topic | definition |
|---|---|
| `scroll-prefetch` | Prefetch off-screen content based on scroll velocity so load latency is hidden before the user reaches it |
| `layout-stability` | Prevent unexpected content shifts (CLS) by reserving space before content loads; covers pre-load extent estimates and server-sent height placeholders |
| `discoverability` | Ensure users can find features and affordances; command palette, tooltips, empty-state guidance, progressive feature reveal |
| `perceived-performance` | Felt speed of the UI regardless of actual latency; skeleton screens, optimistic updates, streaming, and prefetch all serve this |
| `spatial-stability` | Elements must not move unexpectedly under any trigger (load, resize, stream arrival, scroll); governing principle behind layout-stability |
| `progressive-disclosure` | Show only what is needed now; reveal complexity on demand to avoid overwhelming new users while keeping expert paths reachable |
| `direct-manipulation` | Actions feel physically coupled to objects; drag, resize, inline edit; feedback latency must be <100ms to feel immediate |
| `keybinds` | Keyboard shortcut registration, conflict detection, customization persistence, and in-UI discoverability (tooltips, cheat-sheet overlay) |
| `power-user-efficiency` | Features that reduce friction for expert/repetitive workflows: keybinds, macros, command palette, batch operations |
| `theming` | Aesthetic customization: color schemes, font choice, density, dark/light mode; separate from functional accessibility requirements |
| `temporal-layout` | Spatial encoding of time in 1D or 2D: timelines, calendar grids, scatter plots with time axes, inactivity gap separators in chat |
| `linearization` | Rendering inherently non-linear structure (DAG, causal graph) as a scannable 1D spatial sequence with minimal back-edges |
| `animation` | UI motion: micro-animations, transitions, time-swept evolution highlights; must respect prefers-reduced-motion; frame budget ≤16ms |
| `audio-feedback` | Sound cues for events (notifications, errors, success); must be mutable; accessible fallback to visual-only feedback |
| `haptic-feedback` | Device vibration patterns for touch events; mobile/device-specific; permission and pattern vocabulary vary by platform |

| vernacular | definition |
|---|---|
| `CLS` | Cumulative Layout Shift; Core Web Vitals metric for visual stability; sum of unexpected layout shift scores |
| `LCP` | Largest Contentful Paint; Core Web Vitals metric for perceived load speed |
| `INP` | Interaction to Next Paint; Core Web Vitals responsiveness metric (replaced FID) |
| `jank` | Visible frame drops or stuttering; typically caused by main-thread blocking past 16ms |
| `FLIP` | First Last Invert Play; technique for performant layout animations using transform instead of layout properties |
| `RAF` | requestAnimationFrame; schedule work to run before next paint |
| `easing` | Motion timing curve controlling acceleration and deceleration |
| `spring` | Physics-like animation model with stiffness and damping instead of fixed timing |
| `stagger` | Delayed sequence where related elements animate one after another |
| `enter/exit animation` | Motion used when an element appears or disappears |
| `virtual scrolling` | Render only visible list items; recycle DOM nodes as user scrolls to handle arbitrarily large lists |
| `skeleton screen` | Placeholder UI showing content shape before data loads; reduces perceived wait vs. spinner |
| `optimistic update` | Update UI immediately before server confirms; roll back on error |
| `empty state` | View shown when there is no content yet; should explain the state and expose the next useful action |
| `loading state` | Temporary UI while work is pending; includes spinners, skeletons, disabled controls, and progress text |
| `command palette` | Keyboard-driven search over all available commands and features; primary discoverability mechanism for power users |
| `home link` | Logo, title, or nav affordance that routes to the app's default or top-level view; navigation, not creation |
| `launcher` | Entry-point control that starts or opens a primary workflow, app, tool, or workspace; qualify it when ambiguous |
| `affordance` | Visual or physical property that signals how an object can be used (Gibson/Norman); basis for discoverability |
| `tooltip` | Short hover/focus explanation for an element; informational, not an interactive panel |
| `tooltip trigger` | Element whose hover or keyboard focus reveals a tooltip |
| `hover target` | Mouse hover-sensitive element; should have a keyboard-focus equivalent when it reveals information |
| `Fitts's law` | Time to acquire a target ∝ log(distance/size + 1); basis for minimum touch target sizing |
| `touch target` | Interactive area large enough to tap reliably on touch devices |
| `hit target` | Actual clickable/tappable region for an element, which may be larger than the visible affordance |
| `focus ring` | Visible indicator showing the currently keyboard-focused element |
| `focus trap` | Keyboard focus stays inside an open modal, drawer, or sheet until it is dismissed |
| `prefers-reduced-motion` | CSS media query indicating the user has requested minimal animation; must gate all non-essential motion |
| `WAI-ARIA` | Web Accessibility Initiative ARIA; roles and properties for assistive technology interop |
| `WCAG` | Web Content Accessibility Guidelines; A/AA/AAA conformance levels; legal requirement in many jurisdictions |
| `badge` | Compact count/status marker attached to a label, icon, tab, row, or button |
| `pill` | Rounded compact label or control, often used for status, filters, modes, or small option groups |
| `chip` | Compact inline token representing an item, filter, attachment, or selection; often removable |
| `segmented control` | Small set of mutually exclusive options presented as adjacent buttons |
| `accordion` | Disclosure pattern where sections expand or collapse, often one at a time |
| `toast` | Temporary non-modal notification; should not steal focus; often auto-dismisses |
| `snackbar` | Toast-like transient message, often bottom-aligned and sometimes carrying one short action |
| `banner` | Prominent page- or section-level message strip; usually more persistent than a toast |
| `callout` | Inline contextual note, warning, or explanation placed near the related content |
| `dialog` | Focused panel for details, confirmation, or input; may be modal or non-modal |
| `modal` | Blocking dialog/overlay mode where background interaction is disabled and focus should be managed |
| `sidebar` | Persistent side region for navigation or supporting content; may resize, collapse, or become a drawer on narrow screens |
| `drawer` | Edge-attached panel that opens and closes over or beside content |
| `navigation drawer` | Drawer used for app navigation, often the mobile or overlay form of a sidebar |
| `sheet` | Edge-presented temporary panel, commonly used for secondary choices or details |
| `bottom sheet` | Mobile-style sheet rising from the bottom, often partially or fully expanded |
| `popover` | Anchored floating panel with richer content or controls than a tooltip |
| `scrim` | Dimmed visual layer behind an overlay that separates foreground from background |
| `backdrop` | Layer behind an overlay, often used for dimming, blur, outside-click dismissal, or inert background coverage |
| `portal` | Render overlay content outside its normal DOM parent so stacking, clipping, and positioning work predictably |
| `z-index` | CSS stacking order value; only comparable within the same stacking context |
| `stacking context` | CSS layering boundary that controls how z-index values compare; common cause of overlay ordering bugs |
| `scroll lock` | Prevent background or page scrolling while an overlay or modal interaction is active |
| `overview ruler` | Scrollbar-adjacent rail summarizing important off-screen positions with markers, such as search hits, errors, comments, or user turns |
| `scroll anchoring` | Keep the user's visible scroll position stable when content above changes |
| `scroll restoration` | Restore previous scroll position after navigation, reload, or reopening a view |
| `responsive layout` | Layout adapts across viewport sizes, input modes, and device constraints |
| `viewport` | Visible browser/app region used for layout calculations; on mobile it can be affected by browser chrome and safe areas |
| `breakpoint` | Width or condition where layout rules change, such as a sidebar becoming a bottom nav |
| `media query` | CSS condition based on viewport, device, or user preference state |
| `container query` | Style or layout decision based on a component's container size rather than the whole viewport |
| `safe area` | Screen inset reserved for notches, rounded corners, and mobile home indicators |
| `density` | Compactness of UI spacing and controls, such as compact, default, or comfortable modes |
| `sticky positioning` | Element remains fixed within its scroll container after crossing a threshold; common for headers and toolbars |

---

## Full stack / product

| topic | definition |
|---|---|
| `state-management` | Client-side app state: Redux, Zustand, signals; sync strategy with server state |
| `ssr-and-hydration` | Render HTML on server for fast first paint; attach event handlers client-side |
| `file-upload` | Chunked or multipart upload; resume on failure; virus scan; storage handoff |
| `search-and-indexing` | Full-text and faceted search; inverted index, tokenization, relevance ranking |
| `multitenancy` | Isolate data and configuration per tenant; shared vs. dedicated infrastructure |
| `billing` | Usage metering, subscription lifecycle, invoice generation, payment provider integration |
| `oauth` | Delegated authorization; authorization code flow, PKCE, token refresh, scopes |
| `webhooks` | Push event notifications to registered URLs; signing, retries, idempotent handlers |
| `analytics` | Event capture, aggregation, funnel analysis; privacy-compliant instrumentation |
| `cdn-and-caching` | Edge caching of static and dynamic content; cache invalidation strategy |
| `feature-flags` | Gate features per user/cohort; gradual rollout, A/B testing, kill switch |

| vernacular | definition |
|---|---|
| `SPA` | Single-page application; JS renders UI; server returns data APIs, not HTML |
| `CSR` | Client-side rendering; browser fetches data and renders entirely in JS |
| `SSG` | Static site generation; render HTML at build time; no per-request server |
| `ISR` | Incremental static regeneration (Next.js); revalidate pages in background |
| `virtual DOM` | In-memory tree diffed against real DOM to minimize mutations (React) |
| `component` | Reusable UI unit with props, state, and lifecycle; React/Vue/Svelte |
| `hook` | React/Svelte function for stateful logic inside functional components |
| `suspense` | React mechanism to show fallback while async data loads |
| `tree-shaking` | Dead-code elimination for JS bundles; remove unused exports |
| `hydration mismatch` | Server-rendered HTML differs from client render; React error at startup |

---

## Realtime / websocket backend

| topic | definition |
|---|---|
| `session-liveness` | Track which WebSocket sessions are alive; detect stale connections via ping/pong or heartbeat timeout |
| `heartbeat` | Periodic keepalive signal between client and server; detect silent disconnects before TCP notices |
| `message-routing` | Deliver messages to the correct session(s) by user/room/channel identity |
| `fan-out` | Broadcast one message to many sessions; bottleneck in large-scale pub/sub |
| `replay-and-catchup` | Allow reconnected clients to receive missed messages from a durable log |
| `transport-modes` | WebSocket, SSE, long-poll, WebTransport; fallback strategy across network conditions |
| `e2e-encryption` | Encrypt payload client-to-client so the server cannot read content; Signal protocol, MLS |
| `provider-integration` | Webhook ingestion and API calls to third-party services (Twilio, Stripe, etc.) |
| `render-pipeline` | Server-side or client-side assembly of UI from streamed events |
| `auth-and-admission` | Authenticate connections and enforce access control at session establishment |

| vernacular | definition |
|---|---|
| `pubsub` | Publish/subscribe pattern; producers emit events, consumers subscribe to topics |
| `room` | Named grouping of sessions that receive the same broadcast |
| `presence` | Track which users are online; typically via heartbeats and TTL |
| `ping/pong` | WebSocket built-in keepalive frames (opcode 9/10) |
| `back-channel` | Server-to-client push outside the request/response cycle |
| `multiplexing` | Multiple logical channels over one WebSocket connection |
| `sticky session` | Route requests from the same client to the same server instance |
| `event-driven` | Architecture where components react to events rather than polling |

---

## Backend service

| topic | definition |
|---|---|
| `auth-and-admission` | Authenticate requests (JWT, session cookie) and enforce authorization (RBAC, ABAC) |
| `session-lifecycle` | Create, refresh, expire, and invalidate user sessions; token rotation |
| `input-validation` | Reject or sanitize malformed/malicious inputs at service boundaries |
| `api-compatibility` | Maintain backward compatibility; versioning strategy, deprecation, changelog |
| `rate-limiting` | Throttle requests per client/IP/user to prevent abuse; token bucket / leaky bucket |
| `caching` | Store computed responses (CDN, Redis, in-process) to reduce latency and load |
| `background-jobs` | Async work outside the request cycle: queues, workers, retries, idempotency |
| `error-handling` | Consistent error codes, messages, and logging; distinguish client vs. server errors |
| `observability` | Metrics, traces, and structured logs to understand system behavior at runtime |
| `feature-flags` | Gate features by user/cohort without deploying new code; enable gradual rollout |
| `schema-migrations` | Evolve database schema safely under live traffic; backward-compatible changes |
| `consistency` | Read-your-writes, monotonic reads, causal ordering guarantees at the API layer |
| `graceful-shutdown` | Drain in-flight requests before terminating; avoid dropped connections on deploy |
| `resumability` | Allow clients to resume interrupted operations (uploads, streams) without restart |

| vernacular | definition |
|---|---|
| `REST` | Representational state transfer; stateless HTTP + resource URIs + verbs |
| `GraphQL` | Query language for APIs; client specifies shape of response; single endpoint |
| `gRPC` | RPC framework using protobuf over HTTP/2; bidirectional streaming |
| `middleware` | Composable request/response handlers in a pipeline |
| `idempotency-key` | Client-provided unique ID to make POST requests safe to retry |
| `pagination` | Cursor-based or offset-based delivery of large result sets |
| `CORS` | Cross-origin resource sharing; browser security policy for cross-domain requests |
| `OpenAPI` | Machine-readable REST API spec format (formerly Swagger) |
| `circuit-breaker` | Stop calling a failing dependency; fail fast until health recovers |
| `bulkhead` | Isolate failure domains so one slow service doesn't exhaust all threads/connections |
| `RBAC` | Role-based access control; permissions attached to roles, roles attached to users |

---

## Message queue / event streaming

| topic | definition |
|---|---|
| `message-delivery` | At-most-once, at-least-once, exactly-once delivery semantics and their tradeoffs |
| `exactly-once` | Combine idempotent producers + transactional consumers to avoid duplicates |
| `consumer-groups` | Multiple consumers share partitions for parallel processing; rebalance on join/leave |
| `dead-letter` | Route poison messages to a DLQ after N retries; prevents queue head-of-line blocking |
| `schema-evolution` | Add/remove fields without breaking producers or consumers; forward/backward compat |
| `backpressure` | Signal upstream to slow down when consumer is overwhelmed; prevents unbounded buffering |
| `offset-semantics` | Each message has a monotone offset; consumers commit offsets to track progress |
| `retention` | Keep messages for a fixed time or size window; allows replay from any offset |
| `partitioning` | Shard a topic into ordered partitions; key-based routing preserves per-key ordering |

| vernacular | definition |
|---|---|
| `broker` | Server that stores and routes messages (Kafka, RabbitMQ, Pulsar) |
| `producer` | Client that publishes messages to a topic |
| `consumer` | Client that reads messages from a topic or queue |
| `ACK` | Acknowledgment; consumer signals message was processed; triggers offset commit |
| `NACK` | Negative acknowledgment; message is returned for redelivery |
| `idempotent producer` | Kafka setting that deduplicates in-flight messages by sequence number |
| `log compaction` | Retain only the latest value per key; enables infinite-retention state topics |
| `watermark` | Marker in a stream indicating event time has advanced past a threshold |

---

## Desktop / native app

| topic | definition |
|---|---|
| `persistence-and-migration` | Local database or file storage; schema migration without data loss on upgrade |
| `undo-redo` | Command history stack; inverse operations or memento snapshots |
| `plugin-api` | Extension points for third-party code; sandboxing, versioning, lifecycle hooks |
| `print-and-export` | Render document to PDF/PNG/paper; pagination, fonts, resolution concerns |
| `auto-update` | Check for, download, verify, and apply updates; rollback on failure |

| vernacular | definition |
|---|---|
| `sandboxing` | Restrict app permissions via OS policy (macOS entitlements, AppContainer) |
| `deep-link` | URL scheme that opens the app to a specific location |
| `tray` | System notification area / menu bar icon |
| `native-module` | C/C++ addon called from JS/Python for performance or OS access |
| `code-signing` | Digitally sign the app binary; required for notarization and distribution |
| `main/renderer` | Electron process model; main has OS access, renderer runs page JS |

---

## General infrastructure / ops

| topic | definition |
|---|---|
| `deployment` | Release new code to production; blue/green, canary, rolling update strategies |
| `dependency-pinning` | Lock transitive dependency versions for reproducible builds |
| `secrets-management` | Vault, KMS, or secrets injection; rotation and least-privilege access |
| `observability` | Metrics (Prometheus), traces (OTEL), logs (structured JSON); unified correlation |
| `incident-runbooks` | Step-by-step response procedures for known failure modes |
| `backup-and-recovery` | Scheduled backups, retention policy, tested restore procedures |

| vernacular | definition |
|---|---|
| `IaC` | Infrastructure as code; Terraform, Pulumi, CloudFormation |
| `CI/CD` | Continuous integration / continuous delivery; automated build-test-deploy pipeline |
| `container` | Lightweight isolated process namespace; Docker image + runtime |
| `pod` | Kubernetes scheduling unit; one or more containers sharing network/storage |
| `Helm` | Kubernetes package manager; templates for resource manifests |
| `sidecar` | Secondary container in a pod providing cross-cutting concerns (logging, proxy) |
| `ingress` | Kubernetes resource routing external HTTP(S) traffic to services |
| `service mesh` | Istio/Linkerd; mutual TLS, retries, circuit-breaking via sidecar proxies |
| `GitOps` | Declarative infra state in git; operator reconciles live state to desired state |

---

## Availability (cross-cutting)

| topic | definition |
|---|---|
| `fault-tolerance` | System continues operating correctly despite component failures; achieved via redundancy, isolation, and graceful degradation |
| `backup-and-recovery` | Periodic snapshots of data with tested restore paths; defined by RPO and RTO targets |
| `data-durability` | Data survives failures; achieved via replication, checksums, fsync, and write-ahead log |
| `failover` | Automatic promotion of a standby system when the primary fails; requires health detection and state synchronization |
| `circuit-breaker` | Stop calling a failing dependency and fail fast; half-open probe to detect recovery; prevents cascading failure |
| `retry-and-backoff` | Retry transient failures with exponential backoff and jitter; distinguish retryable from non-retryable errors |
| `degraded-mode` | Operate with reduced functionality when components fail; define what is essential vs. optional per subsystem |
| `chaos-engineering` | Deliberately inject failures in production-like environments to verify fault-tolerance assumptions hold |

| vernacular | definition |
|---|---|
| `RPO` | Recovery Point Objective; maximum acceptable data loss measured in time |
| `RTO` | Recovery Time Objective; maximum acceptable downtime before service is restored |
| `MTTR` | Mean Time To Recovery; average time to restore service after a failure event |
| `MTBF` | Mean Time Between Failures; average uptime between failure events |
| `SLA` | Service Level Agreement; contractual availability guarantee (e.g., 99.9% uptime) |
| `SLO` | Service Level Objective; internal target stricter than the SLA (e.g., 99.95% over 30 days) |
| `SLI` | Service Level Indicator; the measured metric underlying an SLO (e.g., request success rate) |
| `health check` | Liveness/readiness probe; distinguishes "process alive" from "can serve traffic" |
| `bulkhead` | Isolate failure domains so one slow dependency cannot exhaust all threads or connections |
| `active-passive` | One primary handles traffic; a cold standby takes over on failure |
| `active-active` | Multiple nodes handle traffic simultaneously; no cold failover delay |
| `Chaos Monkey` | Netflix tool that randomly terminates instances to test resilience of the system |

---

## Performance (cross-cutting)

| topic | definition |
|---|---|
| `performance` | Throughput, latency, and resource efficiency under expected and peak load; cross-cutting property availability depends on |
| `scalability` | Ability to handle growing load by adding resources; horizontal vs. vertical scaling; identify bottlenecks before they bind |
| `profiling` | Measure where time and memory are actually spent; flamegraphs, perf counters, sampling vs. instrumentation tradeoffs |
| `caching` | Store computed results to avoid redundant work; cache invalidation, TTL, and consistency trade-offs |

| vernacular | definition |
|---|---|
| `p50/p95/p99` | Percentile latencies; tail latency (p99) often matters most for user experience and SLO compliance |
| `throughput` | Requests or operations per second the system can sustain at target latency |
| `bottleneck` | The slowest stage limiting overall system throughput; profiling locates it; Amdahl's law bounds the gain from fixing it |
| `flamegraph` | Visualization of sampled call stacks; width = time spent; finds hot paths quickly |
| `Amdahl's law` | Parallelization speedup is bounded by the sequential fraction; S ≤ 1/(1−p) |
| `working set` | Data actively accessed in a time window; must fit in cache or RAM for good performance |
| `cache hit rate` | Fraction of requests served from cache without a backend call; >95% is typically the target for hot paths |
| `GC pause` | Stop-the-world garbage collection pause; causes latency spikes in managed runtimes |
| `lock contention` | Multiple threads waiting for the same lock; degrades throughput under concurrency |
| `Little's law` | L = λW; mean queue length = arrival rate × mean wait time; useful for capacity planning |

---

## Security (cross-cutting)

| topic | definition |
|---|---|
| `injection-and-csrf` | SQL/command/template injection prevention; CSRF token and SameSite cookie defense |
| `secrets-management` | Store and rotate API keys, passwords, certs in a vault; never in env vars or plaintext |
| `supply-chain-integrity` | Pin dependencies; verify signatures; audit transitive packages; maintain SBOM |
| `responsible-disclosure` | Process for receiving and responding to external vulnerability reports |

| vernacular | definition |
|---|---|
| `OWASP` | Open Web Application Security Project; publishes top-10 web vulnerability list |
| `XSS` | Cross-site scripting; inject malicious scripts into pages viewed by other users |
| `SQLi` | SQL injection; embed SQL in user input to manipulate database queries |
| `SSRF` | Server-side request forgery; trick server into making unintended internal requests |
| `JWT` | JSON Web Token; self-contained signed/encrypted claims for stateless auth |
| `OAuth2` | Delegated authorization framework; resource owner grants scoped token to client |
| `OIDC` | OpenID Connect; identity layer on OAuth2; issues ID tokens with user claims |
| `MFA` | Multi-factor authentication; require ≥2 factors (knowledge, possession, biometric) |
| `ABAC` | Attribute-based access control; policies evaluate arbitrary subject/resource attributes |
| `PKI` | Public key infrastructure; CAs, certificate chains, revocation (CRL/OCSP) |
| `STRIDE` | Threat modeling: Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation |

---

## Cryptography

| topic | definition |
|---|---|
| `key-exchange` | DH / ECDH: establish shared secret over an untrusted channel |
| `symmetric` | AES, ChaCha20: fast bulk encryption with a shared key |
| `asymmetric` | RSA, ECC: public/private key pairs for encryption or signing |
| `hash-and-mac` | SHA-2/3, BLAKE3, HMAC: integrity and authentication without encryption |
| `digital-signatures` | EdDSA, ECDSA: non-repudiable proof of origin |
| `zero-knowledge` | Prove a statement without revealing the witness — zk-SNARKs, Bulletproofs |
| `secure-channel` | Compose authenticated encryption + forward secrecy — Noise protocol, TLS 1.3 |

| vernacular | definition |
|---|---|
| `nonce` | Number used once; prevents replay attacks and ciphertext reuse |
| `IV` | Initialization vector; random input to block cipher mode; must not repeat |
| `GCM` | Galois/Counter Mode; authenticated encryption for AES; produces ciphertext + tag |
| `AEAD` | Authenticated encryption with associated data; confidentiality + integrity together |
| `forward secrecy` | Session keys derived ephemerally; compromise of long-term key doesn't decrypt past traffic |
| `certificate` | X.509 binding of public key to identity; signed by CA |
| `CA` | Certificate authority; trusted party that signs certificates |
| `entropy` | Randomness quality; cryptographic operations require high-entropy random numbers |
| `padding oracle` | Timing/error side-channel that leaks plaintext via padding validity |
| `constant-time` | Code that runs in equal time regardless of secret values; prevents timing attacks |

---

## Compliance (cross-cutting)

| topic | definition |
|---|---|
| `privacy-and-retention` | Collect minimal PII; enforce deletion schedules and data retention windows |
| `regulatory-compliance` | GDPR, CCPA, SOC 2, ISO 27001; map controls to implementation |
| `accessibility` | WCAG conformance, screen-reader support, keyboard navigation, color contrast; legal requirement in many jurisdictions |
| `localization` | Adapt content and formatting for locale: string translation, date/number/currency formats, text direction, plural rules |

| vernacular | definition |
|---|---|
| `GDPR` | EU General Data Protection Regulation; governs personal data collection, processing, and deletion rights |
| `CCPA` | California Consumer Privacy Act; US state-level data privacy law with opt-out rights |
| `PII` | Personally Identifiable Information; data that can identify an individual; subject to retention and deletion rules |
| `l10n` | Localization (abbreviation: 18 letters between l and n); adapting a product for a specific locale |
| `i18n` | Internationalization (abbreviation: 18 letters between i and n); engineering the infrastructure that enables l10n |
| `RTL` | Right-to-left text direction; required for Arabic, Hebrew, Persian; affects layout mirroring |
| `ICU` | International Components for Unicode; standard library for locale-aware formatting and collation |
| `plural rules` | Locale-specific rules for noun pluralization; CLDR defines categories (zero, one, two, few, many, other) |
| `CLDR` | Common Locale Data Repository; Unicode consortium's dataset of locale-specific formatting rules |

---

## Regulated industries (cross-cutting)

| topic | definition |
|---|---|
| `audit-trail` | Immutable log of who did what and when; tamper-evident, queryable |
| `segregation-of-duties` | No single person can initiate and approve a sensitive action |
| `change-management` | Formal review, approval, and rollback plan before production changes |
| `data-residency` | Store and process data only in contractually or legally permitted regions |
| `key-management` | HSM or KMS for key generation, rotation, escrow, and destruction |
| `fips-crypto` | Use only FIPS 140-2/3 validated cryptographic modules |
| `incident-response` | Detection, containment, eradication, recovery, post-mortem procedure |
| `vuln-management` | CVE tracking, CVSS scoring, patch SLA by severity |
| `sbom` | Software bill of materials; enumerate all components and their licenses |
| `zero-trust` | Never implicitly trust by network location; verify every request with identity + context |
| `section-508` | US federal accessibility requirement; equivalent to WCAG 2.1 AA for government software |

| vernacular | definition |
|---|---|
| `SOC 2` | AICPA trust-services audit; Type I (design) vs. Type II (operating effectiveness) |
| `ISO 27001` | ISMS standard; risk-based information security management |
| `HIPAA` | US health data privacy law; governs PHI handling |
| `GDPR` | EU general data protection regulation; governs personal data of EU residents |
| `PCI-DSS` | Payment card industry data security standard; governs cardholder data |
| `penetration test` | Authorized simulated attack to find exploitable weaknesses |
| `vulnerability scan` | Automated tool scan for known CVEs; less thorough than a pentest |
| `risk register` | Documented list of risks, likelihood, impact, and mitigations |

---

## Finance / fintech

| topic | definition |
|---|---|
| `transaction-integrity` | Atomic debit/credit pairs; idempotency keys prevent double charges |
| `aml-and-sanctions` | Screen transactions against OFAC/PEP lists; flag suspicious patterns |
| `kyc` | Know Your Customer; identity verification, document check, risk scoring at onboarding |
| `regulatory-reporting` | Generate SAR, CTR, and regulatory filings on schedule |
| `market-data-entitlements` | Control access to price feeds by subscription tier and exchange agreement |
| `client-data-isolation` | Strict per-customer data separation; no cross-account information leakage |

| vernacular | definition |
|---|---|
| `ledger` | Append-only record of financial transactions; double-entry accounting |
| `reconciliation` | Verify internal ledger matches external statements; catch discrepancies |
| `settlement` | Final transfer of funds between institutions; T+1, T+2 cycles |
| `tokenization` | Replace PANs with tokens; reduce PCI scope |
| `FBO account` | For-benefit-of account; bank account holding pooled funds for many end users |
| `PCI` | Payment card industry; governs storage/transmission of card data |

---

## Healthcare / life sciences

| topic | definition |
|---|---|
| `phi-handling` | Protected health information under HIPAA; encryption at rest and in transit, access log |
| `21-cfr-part-11` | FDA rule for electronic records and signatures in regulated software |
| `de-identification` | Remove or generalize PHI so data no longer identifies individuals |
| `clinical-data-integrity` | Audit trails, validation, and source data verification for clinical trial data |
| `medical-device-safety` | IEC 62304 software lifecycle; risk management per ISO 14971 |

| vernacular | definition |
|---|---|
| `HL7 FHIR` | Modern healthcare data standard; RESTful API for clinical resources |
| `ICD-10` | International classification of diseases codes; billing and diagnoses |
| `SNOMED CT` | Clinical terminology system; structured clinical concepts |
| `EHR` | Electronic health record; longitudinal patient data across providers |
| `DICOM` | Standard for medical imaging data; CT, MRI, X-ray files and protocol |
| `IRB` | Institutional review board; ethics approval for research involving human subjects |

---

## Defense / classified

| topic | definition |
|---|---|
| `classification-markings` | Correct portion and banner markings on all documents and outputs |
| `compartmentalization` | Need-to-know access control within classified levels; SCI/SAP handling |
| `cross-domain-solution` | Approved hardware/software guard to transfer data between classification levels |
| `covert-channel` | Unintended information flow through timing, storage, or resource usage |
| `supply-chain-assurance` | Verify hardware and software provenance; anti-tamper requirements |
| `ato-and-accreditation` | Authority to operate process; DIACAP/RMF compliance documentation |

| vernacular | definition |
|---|---|
| `ITAR` | International Traffic in Arms Regulations; controls defense article export |
| `FISMA` | Federal Information Security Modernization Act; US government security framework |
| `STIG` | Security technical implementation guide; hardening checklists for DoD systems |
| `SCIF` | Sensitive compartmented information facility; physically secure room |
| `CAC` | Common access card; DoD smart card with PKI certificates for identity and signing |
| `need-to-know` | Access only to information necessary for assigned duties; enforced via compartmentalization |

---

## Safety-critical / aviation / industrial

| topic | definition |
|---|---|
| `hazard-assessment` | FMEA/FTA to identify failure modes and their safety consequences |
| `redundancy-and-failsafe` | Duplicate systems with independent failure modes; fail to safe state |
| `deterministic-timing` | Bounded worst-case execution time; no unbounded blocking or GC pauses |
| `sil` | Safety integrity level (IEC 61508); quantified probability of dangerous failure per hour |
| `ot-it-separation` | Air-gap or firewall between operational technology and corporate IT networks |

| vernacular | definition |
|---|---|
| `DO-178C` | Software considerations for airborne systems certification |
| `ASIL` | Automotive safety integrity level (ISO 26262); A–D scale analogous to SIL |
| `watchdog` | Hardware/software timer that must be periodically reset; triggers reset on fault |
| `fail-safe` | Failure mode that moves system to a predetermined safe state |
| `fail-secure` | Failure mode that maintains security properties (deny access) on fault |
| `SPOF` | Single point of failure; component whose fault causes system failure; redundancy target |
| `RTOS` | Real-time operating system; guaranteed worst-case scheduling latency |

---

## Networking / protocol design

| topic | definition |
|---|---|
| `tcp-semantics` | Reliable ordered byte stream; flow control, congestion control, connection state machine |
| `tls` | Handshake, certificate validation, record encryption, session resumption |
| `http-semantics` | Request/response model, headers, status codes, caching directives, versions (1.1/2/3) |
| `wire-format` | Binary/text encoding: framing, endianness, length-prefix vs. delimiter, schema evolution |
| `congestion-control` | AIMD, BBR, CUBIC; detect overload and back off to avoid network collapse |
| `protocol-versioning` | Version negotiation and backward-compatibility across protocol versions |

| vernacular | definition |
|---|---|
| `RTT` | Round-trip time; key latency metric; drives timeout and window sizing |
| `MTU` | Maximum transmission unit; largest packet a link carries without fragmentation |
| `QUIC` | UDP-based transport with TLS 1.3 built in; no HOL blocking across streams |
| `HTTP/2` | Multiplexed streams over one TCP connection; header compression (HPACK) |
| `SNI` | Server name indication; TLS extension so server sends correct cert for hostname |
| `ALPN` | Application-layer protocol negotiation; agree on HTTP/1.1 vs HTTP/2 in TLS |
| `HOL blocking` | Head-of-line blocking; one slow stream stalls all behind it (TCP flaw fixed by QUIC) |
| `Nagle's algorithm` | Buffer small TCP sends until ACK or MSS reached; trades latency for throughput |
| `keepalive` | Probe idle TCP connections to detect silent drops |

---

## OS / systems programming

| topic | definition |
|---|---|
| `virtual-memory` | Address space abstraction: page tables, TLB, demand paging, mmap |
| `file-system` | On-disk structure (inodes, journal), VFS interface, fsync semantics |
| `ipc` | Inter-process communication: pipes, Unix sockets, shared memory, message queues |
| `container-isolation` | Linux namespaces + cgroups for filesystem, network, PID, user isolation |
| `signal-handling` | Async notification delivery; masking, async-signal-safe function constraints |
| `kernel-interface` | Syscall ABI, ioctl, proc/sys — stable contract between userspace and kernel |

| vernacular | definition |
|---|---|
| `syscall` | Synchronous trap into the kernel; user mode → kernel mode transition |
| `page fault` | Access to an unmapped or swapped-out page; kernel services it |
| `TLB` | Translation lookaside buffer; cache for virtual→physical page translations |
| `context switch` | Save current thread state, restore another; main scheduling overhead |
| `spinlock` | Busy-wait loop instead of blocking; correct only if wait time < context-switch cost |
| `futex` | Fast user-space mutex; syscall only on contention; Linux primitive under pthreads |
| `mmap` | Map file or anonymous memory into address space; enables zero-copy I/O |
| `copy-on-write` | Share pages until a write occurs, then copy; used in fork and immutable data |
| `cgroup` | Control group; limit CPU, memory, I/O for a group of processes |
| `eBPF` | Extended Berkeley packet filter; run sandboxed programs in kernel for tracing/networking |

---

## Parallelism / concurrency / scaling

| topic | definition |
|---|---|
| `thread-safety` | Correctness under concurrent access; locks, atomics, or immutable data |
| `lock-ordering` | Acquire locks in a fixed global order to prevent deadlock |
| `memory-ordering` | CPU/compiler reordering rules; acquire/release/seq-cst fence semantics |
| `async` | Non-blocking I/O with cooperative scheduling; event loop, futures, async/await |
| `task-scheduling` | Assign runnable work to threads/cores; work-stealing, priority queues |
| `connection-pooling` | Reuse expensive connections (DB, HTTP) rather than creating per-request |
| `sharding` | Partition data or load by key across nodes; consistent hashing or range partitioning |
| `load-balancing` | Distribute requests across instances; round-robin, least-connections, consistent hash |
| `consensus` | Agreement on a value despite failures; Paxos, Raft, Viewstamped Replication |
| `leader-election` | Choose one node as coordinator; Bully, Raft election, ZooKeeper ephemeral nodes |
| `eventual-consistency` | Replicas converge to the same state given no new updates; no strong ordering |
| `cache-coherence` | Ensure all CPU caches see a consistent view of memory; MESI protocol |

| vernacular | definition |
|---|---|
| `mutex` | Mutual exclusion lock; only one thread holds it at a time |
| `semaphore` | Counter-based lock allowing N concurrent holders |
| `deadlock` | Two threads each hold a lock the other needs; circular wait |
| `livelock` | Threads keep changing state in response to each other without making progress |
| `race condition` | Outcome depends on scheduling order; usually a bug |
| `atomic` | Operation that completes without interruption; read-modify-write variants |
| `CAS` | Compare-and-swap; atomically update a value only if it equals expected |
| `ABA problem` | CAS succeeds spuriously when value changed A→B→A between read and swap |
| `false sharing` | Different data on the same cache line; unnecessary cache invalidation |
| `thundering herd` | Many threads wake simultaneously competing for a resource |
| `work-stealing` | Idle threads steal tasks from busy threads' queues for load balancing |

---

## Distributed systems (cross-cutting)

| topic | definition |
|---|---|
| `crdt` | Conflict-free replicated data type; merge is commutative/associative/idempotent so convergence is guaranteed |
| `vector-clocks` | Per-node counters track causality; compare to detect concurrent vs. ordered events |
| `failure-detector` | Classify nodes as suspected/trusted via heartbeats; phi-accrual and SWIM are common |
| `distributed-transactions` | Atomic multi-node operations; 2PC for strong atomicity, saga for long-running workflows |
| `distributed-snapshot` | Chandy-Lamport algorithm: record consistent global state across async processes |
| `split-brain` | Both partitions believe they are primary; fence the minority or go read-only |
| `idempotency` | At-least-once delivery is safe when operations produce the same result on retry |
| `quorum` | Require R+W > N to guarantee overlap; ensures at least one node has the latest write |
| `write-ahead-log` | Append intent before applying; enables crash recovery and replication |
| `tail-latency` | p99/p999 latency dominated by stragglers; hedged requests and speculative execution help |
| `byzantine-fault-tolerance` | Tolerate nodes that lie or behave arbitrarily; PBFT, HotStuff require 3f+1 nodes |
| `geo-replication` | Replicate data across geographic regions; tradeoff between latency, consistency, cost |

| vernacular | definition |
|---|---|
| `Paxos` | Classic consensus protocol; single-decree, multi-Paxos for replicated logs |
| `Raft` | Consensus designed for understandability; leader election + log replication |
| `ZooKeeper` | CP coordination service; distributed locks, config, leader election |
| `etcd` | Raft-based key-value store; Kubernetes control plane backing store |
| `2PC` | Two-phase commit; coordinator asks all to prepare then commit; blocking on failure |
| `saga` | Sequence of local transactions with compensating rollbacks on failure |
| `linearizability` | Strongest single-object consistency; reads always reflect the latest write |
| `serializability` | Transaction isolation level; equivalent to some serial execution order |
| `CAP theorem` | Can only guarantee 2 of Consistency, Availability, Partition tolerance |
| `PACELC` | Extends CAP: also considers latency vs. consistency tradeoff when no partition |
| `Lamport clock` | Scalar logical clock; max(local, received)+1 on receive; total ordering |
| `Merkle tree` | Hash tree; compare subtree hashes to efficiently detect data divergence |

---

## Peer-to-peer / overlay networks

| topic | definition |
|---|---|
| `dht` | Distributed hash table; map keys to nodes with O(log N) hops — Kademlia, Chord |
| `gossip-protocol` | Epidemic dissemination; each node periodically exchanges state with random peers |
| `nat-traversal` | Punch through NAT via STUN/TURN/ICE; hole-punching for direct peer connections |
| `peer-discovery` | Bootstrap mechanism to find initial peers; DNS seeds, DHT, mDNS, rendezvous |
| `sybil-resistance` | Limit identity creation to prevent one actor from controlling many nodes; PoW, PoS |
| `content-addressing` | Identify data by its cryptographic hash, not location; enables trustless retrieval |
| `churn` | High rate of node join/leave; protocol must maintain routing correctness despite instability |
| `routing-overlay` | Virtual network topology over physical IP; nodes maintain partial routing tables |

| vernacular | definition |
|---|---|
| `Kademlia` | DHT variant using XOR metric; O(log N) routing, parallel α-lookups |
| `Chord` | DHT with ring topology and finger tables; predecessor/successor pointers |
| `bootstrap node` | Well-known node used to join the network initially |
| `seeder` | BitTorrent peer with a complete file; uploads pieces to leechers |
| `leecher` | Peer still downloading; uploads what it has to peers |
| `tit-for-tat` | BitTorrent choking strategy; prefer uploading to peers who upload back |
| `hole-punching` | Simultaneous sends trick NAT into allowing direct peer connection |
| `rendezvous server` | Third-party that introduces peers; can be bypassed after connection |
| `epidemic broadcast` | All-to-all message spread via gossip; O(log N) rounds to full coverage |

---

## Database internals

| topic | definition |
|---|---|
| `storage-engine` | On-disk data layout: B-tree, LSM-tree, heap files; controls read/write amplification |
| `mvcc` | Multi-version concurrency control; readers see a snapshot, writers don't block readers |
| `query-optimizer` | Transform logical plan to efficient physical plan via cost model or rules |
| `index-structures` | B-tree, hash, GiST, bloom filter — fast lookup without full scan |
| `transaction-isolation` | Read-committed / repeatable-read / serializable; which anomalies each level prevents |
| `buffer-pool` | Shared page cache between storage and query execution; eviction and dirty-page management |

| vernacular | definition |
|---|---|
| `B+ tree` | B-tree variant where all data is in leaf nodes linked as a list; standard index |
| `LSM tree` | Log-structured merge tree; writes go to memtable + sorted files; write-optimized |
| `WAL` | Write-ahead log; durability guarantee; crash recovery replays log |
| `ACID` | Atomicity, consistency, isolation, durability; transaction correctness properties |
| `dirty read` | Read uncommitted data from another transaction; prevented by read-committed |
| `phantom read` | New rows appear in a repeated range query; prevented by serializable |
| `vacuum` | Reclaim space from dead MVCC tuples (PostgreSQL VACUUM) |
| `compaction` | Merge and GC sorted files in an LSM tree; reduce read amplification |
| `page` | Fixed-size unit of disk I/O (typically 4–16 KB); unit of buffer pool management |
| `index scan vs seq scan` | Use index for selective queries; sequential scan for large table fractions |

---

## Compiler / language runtime

| topic | definition |
|---|---|
| `parsing` | Convert source text to AST via lexer + grammar rules; LL, LR, PEG common strategies |
| `ir-design` | Intermediate representation between AST and machine code; enables portable optimization |
| `optimization-passes` | IR transformations: DCE, inlining, LICM, loop unrolling, constant folding |
| `codegen` | Lower IR to target machine instructions; instruction selection, scheduling |
| `register-allocation` | Assign IR values to finite CPU registers; graph-coloring or linear scan |
| `garbage-collection` | Automatic memory reclamation: tracing GC, ref-counting, generational, compacting |
| `jit` | Compile at runtime; trades startup latency for peak throughput |
| `ffi` | Foreign function interface; calling conventions and ABI across language/library boundaries |

| vernacular | definition |
|---|---|
| `lexer` | Tokenize source text; identify keywords, literals, identifiers, punctuation |
| `AST` | Abstract syntax tree; hierarchical representation of parsed source |
| `CFG` | Control flow graph; nodes are basic blocks, edges are branches |
| `SSA` | Static single assignment; each variable assigned exactly once; simplifies analysis |
| `dominance` | Node A dominates B if every path to B goes through A; key for SSA and loop analysis |
| `inlining` | Replace call with callee body; eliminates call overhead, enables further opts |
| `DCE` | Dead code elimination; remove unreachable or effect-free code |
| `LICM` | Loop-invariant code motion; hoist computations that don't change inside a loop |
| `escape analysis` | Determine if heap allocation can be stack-allocated |
| `tracing JIT` | Record hot execution paths and compile traces to native code |

---

## Distributed compute / HPC

| topic | definition |
|---|---|
| `collective-communication` | AllReduce, AllGather, Scatter across ranks; NCCL/MPI primitives for gradient sync |
| `model-parallelism` | Split model weights across devices when single-device memory is insufficient |
| `fault-tolerance` | Detect failed workers; checkpoint and restart or elastically rescale the job |
| `gpu-memory` | VRAM budget: activations, optimizer states, gradients, KV cache all compete |
| `job-scheduling` | Allocate cluster resources to jobs; queue, priority, preemption (SLURM, k8s) |
| `resource-accounting` | Track GPU-hours, cost, and utilization per user/project for billing or fairness |
| `process-lifecycle` | Launch, monitor, and cleanly terminate distributed processes; rendezvous/init |
| `profiling` | Measure compute/memory/communication bottlenecks; nsight, torch.profiler |

| vernacular | definition |
|---|---|
| `rank` | Identity of a process in a distributed job; rank 0 is typically the coordinator |
| `world size` | Total number of processes in a distributed job |
| `gradient sync` | AllReduce across ranks to average gradients before parameter update |
| `bandwidth-bound` | Operation limited by memory bandwidth, not arithmetic throughput |
| `compute-bound` | Operation limited by arithmetic throughput, not memory bandwidth |
| `FLOP` | Floating-point operation; used to measure compute cost of a model or training run |
| `MFU` | Model FLOP utilization; fraction of peak FLOP/s actually achieved |
| `ZeRO` | Zero redundancy optimizer (DeepSpeed); shards optimizer states, gradients, params |
| `FSDP` | Fully sharded data parallel; PyTorch's ZeRO-3 equivalent |

---

## CUDA / GPU kernel programming

| topic | definition |
|---|---|
| `kernel-correctness` | Bounds, indexing, shape handling, aliasing, race freedom, and reference-equivalence for custom GPU kernels |
| `grid-block-geometry` | Map problem dimensions onto CUDA grids, blocks, warps, tiles, and per-thread work; controls indexing, edge handling, occupancy, and memory locality |
| `memory-access-patterns` | Global-memory layout, coalescing, alignment, vectorized loads/stores, and cache behavior |
| `shared-memory-tiling` | Tile shapes, shared-memory staging, bank-conflict avoidance, and halo/edge handling |
| `warp-level-programming` | Warp-synchronous algorithms using lanes, masks, shuffles, ballots, and divergence control |
| `gpu-synchronization` | Correct use of barriers, atomics, memory scopes, and inter-thread/inter-block ordering |
| `occupancy-and-register-pressure` | Balance registers, shared memory, block size, and active warps per SM for throughput |
| `kernel-fusion` | Combine operations to reduce launch overhead and memory traffic while managing register pressure |
| `precision-and-accumulation` | Numeric formats, accumulation type, rounding, determinism, overflow, and error tolerance |
| `async-copy-pipeline` | Overlap memory movement and compute with staged or double-buffered async copies |
| `custom-op-integration` | Bind kernels into PyTorch/C++/Python runtimes with dispatch, build flags, ABI, and shape contracts |
| `architecture-portability` | Handle compute capability, SM features, tensor cores, PTX/SASS differences, and fallback paths |
| `kernel-profiling` | Use profiler evidence, roofline reasoning, and microbenchmarks to distinguish memory vs. compute limits |

| vernacular | definition |
|---|---|
| `CUDA` | NVIDIA GPU programming platform/API for kernels, memory management, streams, and libraries |
| `CUDA C++` | Canonical CUDA kernel implementation language/front end for NVIDIA GPUs |
| `Triton` | Python-based DSL/JIT for writing custom GPU kernels, common in ML projects |
| `PyTorch C++/CUDA extension` | PyTorch integration route for custom C++ and CUDA operators |
| `CUTLASS` | NVIDIA C++ template library for high-performance GEMM/convolution-style CUDA kernels |
| `CuTe` | CUTLASS tensor-layout and tiling DSL used in modern NVIDIA kernel templates |
| `HIP` | AMD CUDA-like kernel programming API used with ROCm |
| `ROCm` | AMD GPU compute software stack; HIP, libraries, compiler, and runtime |
| `kernel` | Function launched across many GPU threads |
| `grid` | Whole launched collection of thread blocks |
| `block` | Cooperative thread group scheduled onto one SM; also called CTA |
| `CTA` | Cooperative thread array; CUDA block-level execution unit |
| `thread` | Single CUDA execution instance with its own registers and lane position |
| `SM` | Streaming multiprocessor; hardware unit that schedules warps and executes instructions |
| `warp` | Group of 32 CUDA threads executing in SIMT lockstep |
| `lane` | Thread position within a warp |
| `execution configuration` | CUDA launch parameters such as grid size, block size, dynamic shared memory, and stream |
| `grid-stride loop` | Kernel loop pattern where each thread processes elements separated by total grid size |
| `thread-block shape` | Block dimensions chosen to match data layout, tile shape, memory coalescing, and occupancy |
| `launch bounds` | CUDA annotation constraining threads per block/register use to guide compiler occupancy choices |
| `occupancy` | Ratio of active warps on an SM to the hardware maximum |
| `register pressure` | High per-thread register use that can reduce occupancy or cause spills |
| `spill` | Register value stored to local memory because registers are exhausted |
| `global memory` | High-latency device DRAM visible to all threads |
| `shared memory` | Low-latency per-block scratchpad memory |
| `constant memory` | Cached read-only memory optimized for broadcast-style access |
| `coalescing` | Combining adjacent lane memory accesses into efficient memory transactions |
| `bank conflict` | Shared-memory accesses contend for the same memory bank and serialize |
| `warp divergence` | Lanes in a warp take different control-flow paths, reducing parallel efficiency |
| `shuffle` | Warp intrinsic that moves values between lanes without shared memory |
| `ballot` | Warp intrinsic that collects per-lane predicates into a bitmask |
| `CUDA atomics` | Device atomic operations such as atomicAdd; correctness tool with memory-scope and contention costs |
| `tensor core` | Specialized NVIDIA matrix-multiply hardware for mixed-precision GEMM-like operations |
| `WMMA` | Warp-level matrix multiply-accumulate API targeting tensor cores |
| `MMA` | Matrix multiply-accumulate instruction family used by tensor-core kernels |
| `PTX` | NVIDIA virtual ISA emitted before target-specific assembly |
| `SASS` | NVIDIA machine assembly for a specific GPU architecture |
| `compute capability` | NVIDIA architecture version describing available hardware features |
| `stream` | Ordered queue of GPU work; independent streams can overlap |
| `event` | GPU timing/synchronization marker recorded in a stream |
| `pinned memory` | Page-locked host memory enabling faster/asynchronous host-device transfers |
| `unified memory` | CUDA-managed memory addressable by CPU and GPU with migration |
| `cp.async` | Async copy instruction family for moving global memory into shared memory |
| `roofline` | Performance model comparing arithmetic intensity against memory bandwidth and peak FLOPs |
| `Nsight Compute` | NVIDIA profiler for per-kernel metrics, stalls, occupancy, and memory behavior |
| `compute-sanitizer` | NVIDIA correctness tool for memory errors, races, and synchronization bugs |

---

## ML / training

| topic | definition |
|---|---|
| `data-pipeline` | Ingest, transform, and feed training data; throughput must not bottleneck GPU |
| `dataset-versioning` | Track dataset snapshots so experiments are reproducible; DVC, Delta Lake |
| `tokenization` | Convert raw text to integer token IDs; BPE/WordPiece/SentencePiece |
| `checkpointing` | Save model weights and optimizer state periodically; resume from failure |
| `numerical-stability` | Avoid NaN/inf via initialization, gradient clipping, stable loss formulations |
| `mixed-precision` | Train in bf16/fp16, keep fp32 master weights; saves memory, speeds matmuls |
| `gradient-accumulation` | Sum gradients over N mini-batches before updating; simulates larger batch |
| `eval-harness` | Standardized pipeline to run evaluation tasks; separates model from metric logic |
| `hyperparameter-search` | Grid, random, or Bayesian search over lr, batch size, architecture dims |
| `fine-tuning` | Continue training on task-specific data after pretraining; full or parameter-efficient |
| `rlhf` | Reinforcement learning from human feedback; train reward model then optimize via PPO |
| `context-length` | Maximum token sequence the model can attend to; affects memory and capability |
| `experiment-tracking` | Log hyperparameters, metrics, and artifacts per run (MLflow, W&B, Neptune) |
| `model-serving` | Deploy trained model for inference; batching, latency SLAs, versioning |

| vernacular | definition |
|---|---|
| `epoch` | One full pass over the training dataset |
| `batch size` | Number of samples per gradient update step |
| `learning rate` | Step size for gradient update; most sensitive hyperparameter |
| `loss function` | Scalar objective being minimized; cross-entropy, MSE, contrastive |
| `backpropagation` | Chain-rule-based gradient computation through the compute graph |
| `overfitting` | Model memorizes training data, fails to generalize to held-out data |
| `regularization` | Techniques to reduce overfitting: dropout, weight decay, data augmentation |
| `validation set` | Held-out split used to tune hyperparameters; distinct from test set |
| `precision/recall` | Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 is harmonic mean |
| `AUC-ROC` | Area under ROC curve; threshold-independent classification quality |
| `early stopping` | Halt training when validation loss stops improving |
| `confusion matrix` | TP/FP/TN/FN breakdown for classification models |

---

## LLM / transformer architecture

| topic | definition |
|---|---|
| `attention` | Scaled dot-product Q·Kᵀ/√d then softmax weights V; multi-head runs H parallel instances |
| `positional-encoding` | Inject token position into embeddings; sinusoidal (original), learned, RoPE, ALiBi |
| `rope` | Rotary position embedding; encodes relative position by rotating Q/K vectors; extrapolates well |
| `kv-cache` | Cache past-token K and V projections during autoregressive decoding to avoid recomputation |
| `layer-norm` | Normalize activations per token; pre-norm is standard in modern LLMs; RMSNorm drops mean |
| `feed-forward` | Two-layer MLP after attention; GLU variants (SwiGLU, GeGLU) dominate recent models |
| `moe` | Mixture of experts; route each token to K of N expert FFNs; scales params without proportional FLOPs |
| `gqa` | Grouped-query attention; share K/V heads across query head groups; shrinks KV-cache (Llama 2+) |
| `flash-attention` | Tiled CUDA kernel that avoids materializing full N×N matrix; O(N) memory, fast in practice |
| `tokenization` | BPE/WordPiece/SentencePiece: split text into subword units; vocabulary 32K–128K typical |

| vernacular | definition |
|---|---|
| `transformer` | Architecture with self-attention + FFN blocks; Vaswani et al. 2017 |
| `self-attention` | Attention where Q, K, V all come from the same sequence |
| `cross-attention` | Attention where Q comes from decoder, K/V from encoder |
| `causal mask` | Upper-triangular mask preventing attention to future tokens; used in decoders |
| `context window` | Maximum sequence length the model handles; limited by quadratic attention cost |
| `embedding` | Dense vector representation of a token; first layer of every LM |
| `logits` | Unnormalized scores over vocabulary before softmax |
| `next-token prediction` | Autoregressive LM objective; predict token N from tokens 1…N-1 |
| `residual stream` | The vector each layer reads from and writes to via addition; information highway |
| `head` | One parallel attention computation; multi-head attention concatenates H heads |

---

## LLM training and optimization

| topic | definition |
|---|---|
| `gradient-descent` | Iteratively update weights by −lr × gradient; stochastic (SGD) uses mini-batches |
| `adam` | Per-parameter first + second moment estimates; AdamW decouples weight decay |
| `learning-rate-schedule` | Warmup then cosine/linear decay; warmup prevents early instability |
| `dropout` | Randomly zero activations during training; disabled at inference; regularizes by redundancy |
| `weight-decay` | L2 penalty on parameter magnitude; equivalent to Gaussian prior; decoupled in AdamW |
| `gradient-clipping` | Cap gradient norm before the update step; prevents exploding gradients |
| `gradient-checkpointing` | Recompute activations on backward pass instead of storing them; trades compute for memory |
| `mixed-precision` | Train in bf16/fp16 with fp32 master weights; halves memory, speeds matrix ops |
| `data-mixture` | Combine source domains with fixed sampling weights; controls what the model prioritizes |

| vernacular | definition |
|---|---|
| `pre-training` | Train on large unlabeled corpus; produces base model |
| `loss spike` | Sudden large increase in training loss; often from data quality or lr issues |
| `warm-up` | Linearly increase lr from 0 to target over first N steps |
| `cosine decay` | Smoothly reduce lr following a half-cosine curve to near zero |
| `gradient` | Vector of partial derivatives of loss w.r.t. each parameter |
| `optimizer state` | Momentum/variance terms stored per parameter; 2–3× model memory for Adam |
| `scaling law` | Empirical power-law: model size, data, compute, and loss trade off predictably |
| `Chinchilla` | DeepMind paper showing optimal tokens ≈ 20× parameters; revised scaling laws |

---

## LLM fine-tuning and adaptation

| topic | definition |
|---|---|
| `sft` | Supervised fine-tuning on (prompt, completion) pairs; first step in instruction-tuning |
| `lora` | Low-rank adaptation; inject trainable rank-r matrices A,B alongside frozen W |
| `qlora` | LoRA on a 4-bit quantized base model; enables fine-tuning 70B+ on consumer hardware |
| `adapter` | Small bottleneck MLP modules inserted between frozen layers; older alternative to LoRA |
| `prompt-tuning` | Learn a short sequence of soft token embeddings prepended to every input |
| `dpo` | Direct preference optimization; optimizes preference pairs without explicit reward model or RL |
| `reward-model` | Classifier trained on human preference pairs to score response quality; used in RLHF |
| `distillation` | Train small student to match large teacher's logits or hidden states |
| `quantization` | Reduce weight precision to INT8/INT4 (GPTQ, AWQ, GGUF); shrinks model, speeds inference |
| `pruning` | Remove low-magnitude weights, attention heads, or whole layers; sparsify for smaller footprint |

| vernacular | definition |
|---|---|
| `base model` | Pretrained LM before any instruction tuning or alignment |
| `instruction tuning` | SFT on (instruction, response) pairs; makes model follow directions |
| `PEFT` | Parameter-efficient fine-tuning; umbrella for LoRA, adapters, prompt tuning |
| `rank` | LoRA hyperparameter r; lower = fewer parameters, less expressivity |
| `alpha` | LoRA scaling factor; effective update scale = alpha/rank |
| `merge` | Fold LoRA weights back into base model for inference; no adapter overhead |
| `preference dataset` | Pairs of (prompt, chosen, rejected) responses; used for RLHF/DPO |
| `KL divergence` | Measure of policy drift from reference model; RLHF regularizer |
| `PPO` | Proximal policy optimization; RL algorithm used in RLHF to update the LM |
| `constitutional AI` | Model self-critiques and revises using a principle list; Anthropic method |

---

## LLM inference and serving

| topic | definition |
|---|---|
| `speculative-decoding` | Small draft model proposes tokens; large model verifies in parallel; same output, higher throughput |
| `continuous-batching` | Dynamically add/remove sequences mid-batch; maximizes GPU utilization |
| `paged-attention` | Manage KV-cache in non-contiguous fixed-size pages; enables large concurrent batches (vLLM) |
| `tensor-parallelism` | Split weight matrices column/row-wise across GPUs; each holds a shard |
| `pipeline-parallelism` | Assign consecutive layer blocks to different GPUs; micro-batches fill the pipeline |
| `structured-generation` | Constrain decoding to a grammar or JSON schema via logit masking |

| vernacular | definition |
|---|---|
| `prefill` | Process prompt tokens in parallel; compute KV-cache for all input positions |
| `decode` | Autoregressive generation step; one token per forward pass |
| `TTFT` | Time to first token; latency from request to first generated token; dominated by prefill |
| `TPS` | Tokens per second; throughput metric; dominated by decode speed |
| `memory-bound` | Decode is memory-bandwidth bound, not compute-bound; drives hardware choice |
| `GPTQ` | Post-training quantization by layer-wise optimal quantization; preserves accuracy |
| `AWQ` | Activation-aware weight quantization; identifies salient weights to preserve |
| `GGUF` | llama.cpp weight format; single file with metadata, supports many quant levels |

---

## Prompting and agentic

| topic | definition |
|---|---|
| `prompt-engineering` | Craft input text to elicit desired model behavior without any weight updates |
| `few-shot` | Include example (input, output) pairs in the prompt; model generalizes by analogy |
| `chain-of-thought` | Ask model to emit reasoning steps before answering; improves multi-step accuracy |
| `rag` | Retrieval-augmented generation; fetch relevant docs and inject into context window |
| `temperature` | Divide logits by T before softmax; T<1 sharpens distribution, T>1 flattens it |
| `top-p` | Nucleus sampling; draw from smallest token set whose cumulative probability ≥ p |
| `beam-search` | Keep top-K partial sequences at each step; approximately maximizes sequence probability |
| `tool-use` | Model emits structured calls to external functions; runtime executes and returns results |
| `agent-loop` | Observe–think–act cycle; model plans, calls tools, incorporates results, iterates |

| vernacular | definition |
|---|---|
| `system prompt` | Instructions prepended to every conversation; sets model persona and rules |
| `zero-shot` | No examples in prompt; rely on instruction alone |
| `CoT` | Chain of thought; "think step by step" elicits explicit reasoning |
| `scratchpad` | Space in context for intermediate reasoning; often in `<thinking>` tags |
| `hallucination` | Model generates plausible-sounding but false information |
| `grounding` | Anchor model output to retrieved or provided factual sources |
| `function calling` | Structured output of function name + args; runtime executes and returns result |
| `ReAct` | Interleave reasoning and action; observe → think → act loop |
| `multi-agent` | Multiple LLM instances collaborate or compete on subtasks |
| `prompt injection` | Malicious input in retrieved content that hijacks agent behavior |

---

## LLM evaluation and alignment

| topic | definition |
|---|---|
| `model-based-evaluation` | Use learned/model scorers to grade outputs, label preferences, filter data, guide training, or monitor regressions |
| `perplexity` | exp(cross-entropy loss) on held-out text; measures model surprise; lower = better |
| `benchmark` | Standardized test suite (MMLU, HumanEval, HellaSwag); reproducible apples-to-apples comparison |
| `evals` | Evaluation harness: dataset + metric + runner; broader than benchmark, can be product-specific |
| `safety-alignment` | Constitutional AI, RLHF, DPO tuned to refuse harmful outputs and follow value guidelines |
| `red-teaming` | Systematic adversarial probing for harmful outputs, jailbreaks, or policy violations |

| vernacular | definition |
|---|---|
| `MMLU` | Massive Multitask Language Understanding; 57-subject multiple-choice benchmark |
| `HumanEval` | 164 Python programming problems with unit tests; measures code generation |
| `MT-Bench` | Multi-turn conversation quality benchmark; GPT-4 as judge |
| `ELO` | Chess-style rating updated by win/loss; used in chatbot arena leaderboards |
| `LLM-as-judge` | Use an LLM to score, compare, or critique outputs from prompts, rubrics, or pairwise choices |
| `judge model` | Model used as an evaluator rather than the system being evaluated |
| `learned evaluator` | Trained model or learned metric used to score outputs against a task-specific quality target |
| `reward model` | Learned scorer trained from preference or quality labels; can drive RLHF/RLAIF or ranking |
| `preference model` | Model that predicts which of two or more candidate outputs is preferred |
| `critic` | Model/component that evaluates or critiques candidate outputs, plans, or actions |
| `pairwise preference` | Evaluation format comparing two outputs and choosing the better one |
| `jailbreak` | Adversarial prompt that bypasses safety training |
| `alignment tax` | Reduction in raw capability caused by safety fine-tuning |
| `RLHF` | Reinforcement learning from human feedback; PPO + reward model |
| `DPO` | Direct preference optimization; Bradley-Terry model; no RL loop needed |

---

## ML research paper

| topic | definition |
|---|---|
| `eval-split-discipline` | Keep test set unseen until final report; no hyperparameter selection on test |
| `statistical-significance` | Bootstrap CIs, paired t-test, or permutation test before claiming improvement |
| `run-reproducibility` | Seed control, environment pinning, artifact logging for exact re-run |
| `result-provenance` | Link every reported number to the exact run, config, and data version |
| `data-contamination` | Verify eval benchmarks don't appear in training data; n-gram overlap checks |
| `ablation-design` | Isolate one variable per ablation; share all other hyperparameters across conditions |
| `related-work` | Fair comparison to baselines; cite concurrent work; distinguish from prior art |
| `compute-budget` | Report GPU-hours and cost; enables readers to assess feasibility and fairness |
| `paper-log-separation` | Keep experimental logs and paper prose separate; logs are not the paper |

| vernacular | definition |
|---|---|
| `baseline` | Published or reproduced comparison model; minimum bar to beat |
| `SOTA` | State of the art; best published result on a benchmark at a given time |
| `ablation` | Variant with one component removed; quantifies that component's contribution |
| `held-out set` | Data not used during training or hyperparameter tuning |
| `confidence interval` | Range capturing the true value with stated probability (e.g. 95% CI) |
| `effect size` | Magnitude of difference independent of sample size (Cohen's d, etc.) |
| `replication` | Reproduce a result with the same method; distinct from reproduction (new code) |
| `hyperparameter` | Setting not learned by gradient descent (lr, batch size, architecture) |

---

## Physics simulation

| topic | definition |
|---|---|
| `rigid-body` | Objects with mass + inertia tensor; integrate forces/torques, resolve contacts |
| `collision-detection` | Broad phase (BVH, SAP) + narrow phase (GJK/EPA) to find intersecting geometry |
| `constraint-solver` | Enforce joints and contacts via iterative impulse or Lagrange multipliers |
| `soft-body` | Deformable objects: mass-spring, FEM, or position-based dynamics |
| `fluid-simulation` | SPH, Eulerian grid, FLIP/APIC; advection + pressure solve |
| `numerical-integration` | Euler, Verlet, RK4: stability vs. accuracy tradeoffs for ODE solving |

| vernacular | definition |
|---|---|
| `AABB` | Axis-aligned bounding box; simplest broad-phase collision proxy |
| `OBB` | Oriented bounding box; tighter than AABB, more expensive to test |
| `BVH` | Bounding volume hierarchy; tree of AABBs for O(log N) collision queries |
| `SAP` | Sweep and prune; sort object extents along axes to find overlapping pairs |
| `GJK` | Gilbert-Johnson-Keerthi; narrow-phase distance algorithm for convex shapes |
| `EPA` | Expanding polytope algorithm; follow-up to GJK to find penetration depth |
| `impulse` | Instantaneous change in momentum; how constraints are resolved each frame |
| `restitution` | Bounciness coefficient; 0 = perfectly inelastic, 1 = perfectly elastic |
| `island` | Isolated group of bodies connected by contacts/joints; solve independently |
| `CCD` | Continuous collision detection; sweep shapes through time to catch tunneling |

---

## Game development / netcode

| topic | definition |
|---|---|
| `game-loop` | Fixed/variable timestep update-render cycle; determinism vs. smoothness tradeoff |
| `ecs` | Entity-component-system: data-oriented separation of data from behavior; cache-friendly |
| `netcode` | Client-server sync: authoritative server, client prediction, state reconciliation |
| `lag-compensation` | Server rewinds world state to client's perceived time for hit registration |
| `render-graph` | Declarative DAG of render passes with automatic resource/barrier management |

| vernacular | definition |
|---|---|
| `tick rate` | Server simulation update frequency (Hz); higher = more accurate, more bandwidth |
| `delta compression` | Send only changed state fields each tick; reduces bandwidth |
| `snapshot interpolation` | Interpolate between received state snapshots on the client |
| `client prediction` | Apply inputs immediately client-side; reconcile when server confirms |
| `rollback netcode` | Re-simulate from last confirmed state after misprediction; used in fighting games |
| `entity interpolation` | Smooth remote entity movement between received positions |
| `hitbox` | Invisible collision shape for hit detection; can differ from rendered mesh |
| `draw call` | CPU-to-GPU command to render a mesh; minimize for performance |
| `batching` | Combine multiple meshes/sprites into one draw call |
| `frustum culling` | Skip rendering objects outside the camera view volume |
| `LOD` | Level of detail; swap high-poly mesh for lower-poly at distance |
| `Vulkan` | Khronos cross-vendor low-level graphics and compute API, common in engines and portable GPU rendering paths |
| `compute shader` | GPU shader stage used for general compute work outside the traditional graphics pipeline |
| `SPIR-V` | Khronos binary intermediate representation used by Vulkan shaders and compute kernels |
