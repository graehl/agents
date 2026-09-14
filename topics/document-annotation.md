# Document annotation

> Run fixed-prompt annotation over ordered document segments with isolated
> Codex subscription sessions or opt-in OpenAI Chat Completions, optional caller
> validation, and durable attempt receipts.

Topic: `document-annotation`

Read this topic before building or running fixed-prompt, segmented-document
annotation through Codex or OpenAI Chat Completions. Use the shared Python
transport and runner when their session policy fits; keep domain schemas,
data selection and admission rules in the calling project. This topic is
reached from `RESEARCH.md`; a separate skill would duplicate that route.

## Scope and prerequisites

The implementation is [`document_annotation/`](../document_annotation/), with
the [`document-annotate`](../scripts/document-annotate) CLI. It uses Python 3.11+
and defaults to the installed Codex `app-server` JSONL protocol with a
subscription login. The optional API transport uses `httpx`; see
[Chat Completions](#chat-completions-with-an-api-key) before selecting it.
There is no provider SDK dependency. The CLI also uses this checkout's
`acli` library. Retain or transfer the shared checkout when another project
imports it; do not copy a private transport implementation into each project.

Before annotation spend, satisfy the governing program's input, deduplication,
split-exclusion, authorization and budget gates. Put source/inventory and gate
receipt references in the input metadata or the enclosing campaign manifest.
Duplicate segment IDs are rejected by this runner; that check does **not**
establish that texts or source documents are additional or nonoverlapping.
The optional output validator likewise does not establish data admissibility.

Freeze the prefix, input order, model/effort, validator version and session
limits for a campaign. Qualify the limits on representative data before bulk
use: enough room for the full instructions, segment, history and answer, with
no compaction. A new prompt or validator version is a new campaign linked to
its predecessor. Preserve whether it adds data, replaces labels or reannotates
the same sources; new output filenames do not change their exposure history.

## Rendered-prompt boundary convention

Draft's `--codex-protocol-root` mode consumes exactly one literal
`<!-- CODEX_SESSION_TURN -->` marker in **each rendered prompt**. It marks the
end of fixed content and the start of the per-turn segment:

```text
Fixed task instructions, schema and demonstrations.
<!-- CODEX_SESSION_TURN -->
Per-segment guidance, if any.
Segment:
{text}
Output:
```

The marker is a coordinator convention, not special Codex syntax. Draft's
`split_codex_protocol_prompt` removes it, applies `rstrip()` to the fixed part
and `lstrip()` to the per-turn part, and rejects missing/repeated markers or
empty parts. It then requires one exact common fixed prefix across the rendered
batch. Put all row-dependent text, guidance and metadata after the boundary;
language-dependent demonstrations require separate batches when their fixed
prefixes differ. Freeze both the rendered source and effective split content.

For a fork experiment using a markerless template, create a separately named
copy, place the marker before its first variable content, and pass that copy
explicitly. Keep the ordinary template version intact. Never infer the boundary
from a heading or silently treat a markerless whole prompt as the fixed part.

The shared `document-annotate` CLI already takes the two parts separately:
`--prompt` supplies fixed instructions and each input record's `prompt` supplies
the per-turn suffix. It does not parse the marker; do not add it to those files.
When adapting a combined draft template, render and split it first under the
convention above.

## Fixed user/assistant messages

Optionally pass `--fixed-messages fixed-messages.json` alongside `--prompt`:

```json
[
  {"role":"user","content":"Apply the annotation protocol to every segment."},
  {"role":"assistant","content":"I will do a good job."}
]
```

The fixed context can therefore contain several role-tagged messages. The
Python equivalent is `AnnotationConfig(..., fixed_messages=(
FixedMessage("user", "..."), FixedMessage("assistant", "...")))`, with
`FixedMessage` imported from `document_annotation.messages`. Roles are limited
to `user` and `assistant`, content is nonempty text, and order is preserved.
These are caller-authored messages, including canned/fictitious assistant
replies; they are not recorded as model-generated answers or annotation evidence.

The subscription backend uses Codex's documented
[`thread/inject_items`](https://learn.chatgpt.com/docs/app-server#inject-items-into-a-thread)
to insert the sequence after thread creation and before its first segment.
Insertion persists history without starting generation. It is performed once
for every fresh thread, including validation retries and length resets, and
is not repeated when continuing or resuming that thread. It adds to the fixed
`baseInstructions`; it does not turn every message into a separate inference
request. Codex still adds its native permissions/environment context.

Exact roles, content and order belong to the campaign identity. The CLI also
freezes the source JSON bytes; changing either file requires a new campaign.
Journal entries distinguish authored-message injection from inferred turns.
An injection failure stops before the segment request; resume can abandon that
unused thread and create a fresh one instead of reinjecting into it.

Mechanics have subprocess tests and a real app-server injection/persistence
check with zero inference requests. **The annotation-quality effect is
unqualified.** Before adopting role-play acknowledgments or demonstrations,
compare the same fixed segments with and without the message sequence. Keep
demonstration sources disjoint from those segments; hold model, task
instructions, validator and session policy fixed. Measure semantic quality,
format failures, retention and total input/cache cost.
Injection alone does not prefill the model or establish a cache hit. This
option does not alter draft's existing PII annotation recipe.

## Session and retry policy

Each document gets its own session and ordered segment turns. Documents may run
concurrently; their histories are never combined. A turn sees the fixed prefix,
any fixed user/assistant messages, that session's previous segment prompts and
accepted assistant answers, and the current segment prompt. The prefix is
passed unchanged as Codex `baseInstructions` or API developer-message text.

At the configured segment limit, start a fresh session. An output rejection,
reported compaction, or excessive input-token count also discards the session
for continuation and retries the same segment in a fresh session, within the
retry allowance. The input-token ceiling is a **post-response** check, so the
rejected attempt still costs tokens. An exhausted rejection is recorded and
the next segment starts fresh.

Fresh retries receive the same fixed prefix, fixed messages and segment prompt,
with neither earlier document turns nor the rejected response or rejection
explanation.
Make segments self-contained enough for that case. If a task requires earlier
document context or correction feedback, the calling project must explicitly
assemble and version those inputs or own a different retry coordinator.

The low-level `CodexAppServer` also exposes thread start, fork, read, resume and
turn methods. Draft's PII coordinator continues to own its more specific
fork/replay and paragraph-recovery policy; extracting the transport does not
replace that policy with this runner's simpler append-within-document policy.

## Optional validation callable

The Python interface is `validate(text, segment)`, synchronous or asynchronous:

- Return `None` to accept the response under that validator.
- Return a nonempty string explaining a rejection to request a fresh retry.
- Raise on a validator defect or unavailable dependency. The campaign stops;
  the raw response is already journaled and is not silently regenerated.

For example, a caller can require JSON containing one label per supplied item:

```python
import json

def check_labels(text, segment):
    try:
        labels = json.loads(text)
    except json.JSONDecodeError:
        return "invalid JSON"
    if not isinstance(labels, list) or len(labels) != segment.metadata["item_count"]:
        return "expected one label per item"
    if any(not isinstance(label, str) or label not in {"positive", "negative"} for label in labels):
        return "unknown label"
    return None
```

Supply the callable and a versioned `validator_id` together. CLI
`--validator my_checks:check_labels` imports trusted caller code from the
invoking project and binds its module-file hash into the campaign identity.
That hash does not capture transitive dependencies, model weights or external
resources: bind those in the project's own environment/validator receipt.

With no callable, successful responses are explicitly `unvalidated`; no
caller-format retry occurs. The API transport still rejects incomplete,
refused or empty outputs under its own response contract.
External batch validation and retry are legitimate:
retain the raw campaign, emit separate validation receipts, and link any retry
campaign to the rejected original attempts. Do not relabel raw success as
validated, or change the original journal to hide failures.

## CLI use

Input is one JSON object per line, with required string fields `document_id`,
`segment_id`, `prompt`, and optional object `metadata`. IDs are unique within
each document; input order within a document is significant. Results preserve
the complete input order even when documents run concurrently.

```json
{"document_id":"doc-a","segment_id":"1","prompt":"Label: ...","metadata":{"item_count":2}}
{"document_id":"doc-b","segment_id":"1","prompt":"Label: ...","metadata":{"item_count":1}}
{"document_id":"doc-a","segment_id":"2","prompt":"Label: ...","metadata":{"item_count":3}}
```

Choose an explicitly approved model and qualified limits; the values below are
shell variables for those choices, not model or context recommendations:

```bash
~/agents/scripts/document-annotate \
  --input segments.jsonl --prompt annotation-prefix.txt \
  --out campaigns/labels-v1 --auth-home "$HOME/.codex" \
  --model "$annotation_model" --effort "$annotation_effort" \
  --max-session-segments "$qualified_segment_limit" \
  --max-input-tokens "$qualified_input_limit" \
  --workers 4 --retries 1 --timeout 5m \
  --validator my_checks:check_labels --json
```

The campaign directory must be new; use the same command plus `--resume` for an
existing one. For a private campaign collection, exclude that collection using
the calling project's private-directory convention. The CLI creates the
campaign with mode 0700. In subscription mode it copies only `auth.json` into a
managed `.codex/` profile with mode 0600. **Subscription campaign directories
contain credentials.** Share selected manifests/results/receipts, never the
entire subscription directory. Refreshing authentication is operational state,
not a prompt change.

The Codex child gets a separate home, fixed configuration, disabled instruction-file,
memory, plugin and tool features, and no inherited API-key or parent-agent
environment. Unexpected server tool/approval requests fail the transport.
This is annotation-context isolation, not an OS security boundary for hostile
code. The callable runs as trusted Python in the caller's process.

Exit 0 means all segments finished, including raw `unvalidated` responses;
exit 1 means at least one exhausted rejection. Setup/runtime failures emit an
ACLI error and a nonzero status. JSON stdout is the final campaign summary;
`events.jsonl` is durable incremental progress. `--help` owns current options.

## Chat Completions with an API key

**Implemented, not live-qualified:** GPT-5.6 API-key access is unavailable to
the user as of 2026-09-14. Local HTTP fixtures exercise this path; live model,
cache and annotation-quality qualification remain in the
[API transport gap](../gaps/document-annotation-api-key.md).

Select `--backend openai-chat-completions` explicitly, with `OPENAI_API_KEY`
already set in the environment and `httpx` installed in the invoking Python
environment. Omit `--auth-home`; provide a positive `--max-output-tokens`
(the API's `max_completion_tokens`, including reasoning). For example:

```bash
~/agents/scripts/document-annotate \
  --backend openai-chat-completions \
  --input segments.jsonl --prompt annotation-prefix.txt \
  --fixed-messages fixed-messages.json --out campaigns/labels-api-v1 \
  --model "$annotation_model" --effort "$annotation_effort" \
  --max-session-segments "$qualified_segment_limit" \
  --max-input-tokens "$qualified_input_limit" \
  --max-output-tokens "$qualified_output_limit" \
  --chat-cache-mode explicit --validator my_checks:check_labels --json
```

The key is neither copied into the campaign nor stored in receipts. This
adapter uses the fixed OpenAI HTTPS endpoint, standard service tier,
`store: false`, one non-streaming choice, no tools, and no automatic HTTP
retries or redirects. It ignores environment proxy and alternate-base-URL
settings. A key's presence never changes the default subscription backend.

The adapter assembles the developer prefix, fixed user/assistant messages,
accepted document history and current user segment as typed text blocks.
Its default `--chat-cache-mode explicit` marks the last block of the **whole
fixed sequence**, including a final canned assistant message, with
`prompt_cache_breakpoint: {"mode":"explicit"}` and sends
`prompt_cache_options: {"mode":"explicit","ttl":"30m"}`. The variable suffix
receives no breakpoint. This is the API mapping of the fixed-content boundary;
the HTML marker itself is never a cache control or an API input delimiter.
These fields are documented in the
[Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).

Use explicit mode with a supported GPT-5.6+ model and at least 1,024 visible
tokens before the breakpoint. The rendered prefix and relevant settings must
match; cached entries have a minimum 30-minute lifetime refreshed by reuse.
Explicit mode without a breakpoint would disable caching, so this adapter
always supplies one. For earlier models, select `--chat-cache-mode automatic`,
which omits both new cache fields. It never retries a rejected explicit-cache
request with different semantics. See the
[prompt-caching guide](https://developers.openai.com/api/docs/guides/prompt-caching).

API sessions hold local message history. Resume reconstructs only the accepted
turns in the last continuing session from completed receipts, then reapplies
the same fixed sequence and boundary. Legacy result fields `thread_id` and
`continuation_thread_id` hold a `local-...` session identifier, not a provider
thread; `turn_id` is the API completion ID. Changed backend/cache/output-limit
settings fail resume. Rejections reset context under the shared retry policy.

## Python integration

The runner accepts a live `CodexAppServer` or `ChatCompletions` backend,
immutable `AnnotationConfig`, and `Segment` records. Supply a durable recorder;
`Journal.write` flushes and fsyncs each event. This is the core call within an
owned transport context:

```python
from document_annotation.journal import Journal
from document_annotation.runner import AnnotationConfig, DocumentAnnotator, Segment

config = AnnotationConfig(
    prefix=fixed_prefix, model=model, effort=effort, cwd=str(isolated_work),
    max_segments_per_session=qualified_segment_limit,
    max_input_tokens=qualified_input_limit,
    validator_id="label-check-v1@<source-and-dependency-receipt>",
)
journal = Journal(campaign / "events.jsonl")
results = await DocumentAnnotator(server, config).annotate(
    segments, record=journal.write, validate=check_labels,
    completed=journal.completed(),
)
```

[`cli.py`](../document_annotation/cli.py) shows the complete lifecycle:
profile preparation, frozen manifest/input, campaign lock, owned transport
startup/shutdown and final result publication. For API use, pass a backend from
`async with ChatCompletions(api_key, max_output_tokens=limit, cache_mode="explicit")`,
imported from `document_annotation.chat`. Library callers own those
boundaries themselves. Import `Segment` to construct inputs; each segment's
metadata must be JSON serializable.

## Receipts and resume

The journal records request intent before sending, the raw response before
validation, the rejection reason, and the final segment result. Subscription
raw receipts include provider events, thread/turn IDs, token usage and the
loaded transport source hash. The CLI manifest binds all implementation files
for either backend. Final usage includes accepted and rejected attempts for that
segment. Optional counters absent in the app-server protocol normalize to zero
in the compatibility response; inspect raw events before interpreting an absent
counter as a measured cache-write or reasoning-token zero. The API adapter
preserves request JSON, response body, HTTP status and request ID before
parsing or validation. It maps supplied `prompt_tokens_details.cached_tokens`
and `cache_write_tokens`, and `completion_tokens_details.reasoning_tokens`;
absent optional counters stay absent. Sums include only reported counts, so
inspect raw usage coverage before treating a partial counter as a full total.
The response body retains the returned model revision and service tier.

CLI resume verifies the entire input, exact prefix and fixed messages, settings,
validator module, implementation hashes and transport settings/version
(plus managed Codex configuration for subscription mode). Completed
segments must form a prefix within each document. Before reusing an unfinished
document's Codex thread, its last completed turn must match the saved receipt.
Changing a campaign requires a new output directory and explicit lineage.

Unfinished request intents, partial journal writes and transport failures stop
automatic resume. Reconcile the journal and available provider evidence before deciding
whether an attempt completed or may be repeated; the driver does not infer that
a lost response was free. Cancellation and timeouts interrupt Codex turns or
cancel API requests; the owner closes its transport on exit. This does not
promise that an unreachable provider has stopped billing.

## Design decisions

- **One runner with provider-specific session storage** (vs. duplicating the
  coordinator or emulating a remote API thread): validation, fresh retries and
  ordering stay common; Codex verifies its persisted last turn, while Chat
  Completions reconstructs explicit message history from local receipts.
- **Direct async HTTP for the opt-in key route** (vs. requiring a provider SDK
  for both backends): `httpx` supplies cancellation and bounded requests while
  documented cache fields can be serialized unchanged. The adapter owns its
  response validation; subscription-only use adds no dependency.

## Cache claims and qualification

Thread continuity makes prefix/history reuse possible; it is not a guarantee
of cache routing, quality equivalence or lower cost. Record input, cached-input,
available cache-write/output counts, rejected attempts, startup overhead,
wall time and account quota changes for a representative comparison. Preserve
the exact model and prompt identities. Quota snapshots include other sessions'
spending and are not automatically per-campaign measurements.

API breakpoints do not establish a cache guarantee for Codex subscription
threads. The new route's live cache behavior and matched quality/cost comparison
remain in [the API transport gap](../gaps/document-annotation-api-key.md).
Keep API billing and subscription quota units distinct. No subscription failure
or discovered key silently switches the billing route.
