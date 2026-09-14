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
