---
slug: document-annotation-api-key
noticed: 2026-09-14
where: document_annotation/cli.py, document_annotation/chat.py
---

**Gap:** the opt-in [document-annotation](../topics/document-annotation.md)
Chat Completions transport is implemented and locally tested, but lacks live
GPT-5.6 API qualification. The user has no API-key access to that model as of
2026-09-14 and authorized preemptive implementation with this limitation
retained. Do not treat local HTTP fixtures as model, cache or cost evidence.

**Noticed while:** generalizing draft's Luna fixed-prefix, document-segment
annotation driver and optional per-response validation.

**Resolved contract:** the user supplied the
[OpenAI prompt-caching guide](https://developers.openai.com/api/docs/guides/prompt-caching),
and the [Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
confirms the endpoint's explicit text-block breakpoints and request cache
options. The supported fixed-prefix mapping and its model/minimum-length
conditions are documented in the topic's API section. These controls are
distinct from a universal hit guarantee for subscription threads.

**Implemented:** `--backend openai-chat-completions` requires an environment
`OPENAI_API_KEY` and an output-token ceiling. A text-only HTTP adapter places
the cache boundary after the complete fixed message sequence, including canned
assistant messages. Backend settings bind manifest/result identities; raw
receipts retain returned model and usage. Accepted document history survives
resume, validation retries start fresh, and HTTP/schema/ambiguous failures stop
without replay. The existing subscription backend remains the default.

**Closure when access exists:** run a bounded authorized live check on an
approved model with a sufficiently long fixed prefix, varied suffixes, and
both a single-message and a fixed user/assistant sequence. Confirm accepted
request fields, returned model, finish reasons, cold/write and warm/read usage,
and identical reconstructed context after resume. Record a representative
matched annotation comparison before claiming quality equivalence or greater
efficiency. Compare actual cache-write/read billing rather than inferring cost
from a hit alone; keep API billing and subscription quota units distinct.
Remove this gap once the operating limits and qualification receipt are linked
from the topic. Until then the implemented route is available but unqualified.
