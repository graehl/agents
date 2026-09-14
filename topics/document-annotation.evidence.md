# Document annotation evidence

## 2026-09-14 — extract transport, retain caller policy

- **User direction:** generalize draft's Python Codex subscription annotation
  driver for other research projects. The fixed prompt and ordered document
  segments are reusable; format checking may be an optional callable, and
  external batch validation/retry remains legitimate. API-key transport may
  remain an explicit gap.
- **Source:** `~/draft/scripts/pii_codex_app_server.py` at
  `7647b1b6f0c9793107e2b7dc9ea55bf772632266`, inspected with its callers in
  `scripts/pii_api_label.py` and transport/labeler tests. This is extraction of
  the user's code, not third-party vendoring. The draft module now imports the
  shared client; responses bind the loaded client hash so a wrapper-file hash
  alone is not mistaken for complete transport provenance.
- **Choice:** a Python package, CLI and directly routed RESEARCH topic. No new
  skill wrapper, provider SDK dependency or speculative multi-provider base
  class. The generic runner appends turns within a document and resets after
  rejection. The PII caller retains its fork/replay and paragraph policy.
- **Reliability boundary:** raw responses precede validation; validator bugs
  and ambiguous transport failures stop. An unfinished request cannot become
  an automatic free retry on resume. Completed-document prefixes bind config
  and input; continuation checks the last provider turn against its receipt.
- **Counterexample to a stronger cache claim:** draft's six-segment
  `pii-ont3-fork-cache-smoke6-v1` observation reports mixed cache hits, including
  three cold first-segment forks. It has no matched append-only control and no
  annotation-quality score. Neither it nor successful transport extraction
  establishes that this runner is faster, cheaper or quality-equivalent.
- **Verification scope:** subprocess JSONL fixtures exercise the real client,
  document coordinator and CLI, including async validation, clean retries,
  ordered output, context limits, receipt checks, cancellation and timeout
  interruption. Draft's existing transport/labeler tests exercise compatibility
  through the import wrapper. A real installed Codex app-server accepted the
  strict isolated configuration and initialization handshake; that check made
  zero inference requests. No new model-quality or cache-efficiency claim was
  tested in this extraction.
- **API uncertainty:** the requested “Messages API” global-cache guarantee
  needs the exact provider contract. Official OpenAI prompt-caching and Codex
  app-server documentation were consulted; they do not resolve that specific
  recalled guarantee. Keep the key route in the linked gap until verified.

## 2026-09-14 — explicit boundary and fixed role-tagged messages

- **User direction:** preserve the `<!-- CODEX_SESSION_TURN -->` convention
  discovered while preparing a fork-experiment template, and support a fixed
  context that can include several user and canned assistant messages. The
  user explicitly distinguished possible annotation value from tested value.
- **Boundary evidence:** draft's `split_codex_protocol_prompt` already
  enforces one marker, nonempty parts and whitespace trimming at the split;
  `run` rejects differing fixed prefixes after rendering. The shared runner's
  separate prefix/segment inputs need no marker parser. Documentation now
  explains that mapping and keeps marker additions in experimental copies.
- **Transport evidence:** Codex CLI 0.154.0's generated schema includes
  `ThreadInjectItemsParams`; the official app-server documentation's “Inject
  items into a thread” section specifies persisted model-visible history
  without generation. This route is distinct from the Cloud-only unstable
  `thread/resume.history` parameter, which the implementation does not use.
- **Live check:** a real isolated app-server accepted and persisted a fixed
  user message followed by a canned assistant response, preserving their text,
  order and input/output content types. No `turn/start` or inference request
  was issued. The rollout also contained native permissions and environment
  messages, so the authored fixed sequence is not the complete provider wrapper.
- **Trace: fresh retry and resume:** every new thread gets the same authored
  sequence before inference; a resumed existing thread receives no duplicate
  injection. Config and source-file hashes prevent changed roles/content/order
  from silently entering a prior campaign. Injection receipts are marked
  `caller_authored` and never become annotation labels or generated evidence.
- **Trace: markerless or varying template:** a separately named copy receives
  its explicit boundary; a different language's demonstrations require a
  separate common-prefix batch. The generic CLI continues to use separate
  input fields, avoiding a literal marker inadvertently sent to the model.
- **Validation:** CLI tests contrast enabled/disabled fixed messages and
  validators; document tests check clean retries, separation and resume. The
  annotation-quality, retention and cache-cost comparison remains unperformed.

## 2026-09-14 — opt-in Chat Completions and explicit prefix caching

- **User direction:** supplied the official prompt-caching citation, then
  authorized preemptive key-route implementation despite lacking GPT-5.6 API
  access. Live qualification may remain in a gap. This resolves the earlier
  entry's provider/endpoint uncertainty without inventing access or a benchmark.
- **Sources checked:** the current prompt-caching guide and Chat Completions
  create reference linked in the main topic. The endpoint schema supports the
  text blocks used here, including assistant text, request cache mode/TTL and
  cache-write/read usage fields. The implementation does not generalize the
  supplied summary's multimodal/refusal-block claims beyond these verified
  text inputs. The guide and endpoint differ in their long-history lookup-window
  descriptions; this adapter writes one fixed boundary, so it does not depend
  on either window count.
- **Boundary trace:** with developer instructions, a fixed user message, a
  canned assistant reply and a variable segment, the marker lands on the canned
  reply's last text block. Marking only the developer message would omit useful
  fixed history. Appending accepted document turns never moves that boundary.
  Automatic mode omits the new fields for earlier models; unsupported explicit
  requests fail without an implicit-mode fallback.
- **Billing trace:** a discovered environment key does not change the default
  backend. Missing key or output bound fails setup. The API adapter uses an
  owned async HTTP client with no retries or redirects; the key is excluded
  from saved requests and campaign identity. Transport failures leave an
  unfinished attempt that blocks automatic resume. Refusal, truncation and
  empty answers consume the bounded rejection budget even without a validator.
- **History trace:** an accepted result following a rejected attempt starts a
  new local session. Resume reconstructs that session's accepted turns only,
  restoring the fixed sequence exactly once. It does not replay earlier failed
  requests, mix documents or present local session IDs as provider threads.
- **Verification:** 31 tests pass across subscription subprocess and API HTTP
  fixtures, including the CLI argument-to-request path, cache enabled/automatic
  contrast, usage mapping, changed-manifest rejection, history/resume, async
  validation, context resets, incomplete outputs, cancellation, timeouts,
  malformed responses and no-replay failures. No live API request was made.
  The access, cache and quality/cost qualification remains a committed gap.
