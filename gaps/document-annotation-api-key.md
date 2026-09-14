---
slug: document-annotation-api-key
noticed: 2026-09-14
where: document_annotation/cli.py, document_annotation/codex.py
---

**Gap:** the reusable [document-annotation](../topics/document-annotation.md)
facility currently supports Codex subscription sessions only. The user also
wants an optional API-key transport, explicitly permitted to remain a gap in
this extraction. A supplied key does not currently select or enable a route.

**Noticed while:** generalizing draft's Luna fixed-prefix, document-segment
annotation driver and optional per-response validation.

**Fix sketch:** identify the intended provider and exact “Messages API”
documentation first. The user recalls a guarantee that fixed initial messages
pass through a global cache; its endpoint, qualifying models, prefix/breakpoint
rules, retention, billing and guarantee remain unverified. A nonblocking link
request was made; do not substitute a remembered API name or treat OpenAI
Responses prompt caching as proof of that specific claim.

Add an explicit backend/auth selection at the CLI boundary and a transport
adapter beneath the existing segment/validator/receipt contract. Preserve
ordered document context and clean retry semantics without requiring server
thread IDs where the provider instead accepts explicit message history. Bind
the backend, complete fixed messages, cache controls, model revision, validator
and usage accounting into the campaign manifest. No automatic billed fallback
after a subscription failure.

Closure needs an official supported API contract, response/usage and resume
integration tests, a bounded authorized live check, and a matched annotation
quality/cost comparison before claiming greater efficiency. Keep subscription
and API billing units distinct. Remove this gap when that route is implemented
and its operating limits are documented.
