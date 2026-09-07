---
slug: acli-commentary-history-injection
noticed: 2026-09-07
where: acli/, scripts/session-turn, YA provider service
---

**Status:** optional avenue captured as a gap at the user's request. No
implementation is scheduled; ordinary commentary must remain useful without
history injection.

**Gap:** a tool can communicate required information to the user, but the
calling agent also needs to know what was communicated and that this part of
its instructions is fulfilled. The intriguing optional route is to append the
tool's fluent commentary to the calling session's model-visible assistant
history, alongside ordinary tool results and user-visible presentation.

**Noticed while:** designing acli stdout-aligned commentary and YA parsing.
The user accepts either synthetic assistant history or an agent briefed in
advance on the tool's presentation contract. Injection is not required to
satisfy [the current caller guidance](../topics/acli.md#tool-mediated-user-communication).

**Fix sketch:** acli supplies commentary events; YA's owning provider service
could append them through an enhancement to `session-turn`. The existing
[session-turn contract](../topics/helper-scripts.md#session-turn) sends user
turns and starts provider work. Injection needs a distinct negotiated operation
whose purpose is appending history without starting a user turn or requesting
another generation. Do not treat today's `send` as equivalent.

The [Codex App Server documentation](https://learn.chatgpt.com/docs/app-server#inject-items-into-a-thread)
describes `thread/inject_items`: raw Responses API items, including assistant
messages, are appended to a loaded thread, persisted to its rollout, and
included in subsequent model requests without starting a user turn. Documented
feasibility was checked during this discussion; delivery through the running
YA service and other providers remains unverified.

Before implementation, settle and verify:

- Bind delivery to the calling session and originating tool invocation through
  the owning provider service; retain tool origin even for assistant-role text.
- Preserve event order and define when an active model request can first see
  the injected items. Do not fabricate past reasoning or unfinished actions.
- Keep UI presentation and history insertion separately observable. A queued
  request or a successful stdout write cannot claim either has completed.
- Correlate events and receipts across retries/reconnects so YA presentation
  and provider replay do not duplicate an announcement. Distinguish uncertain
  delivery, unsupported providers, and partial failure from success.
- Keep injection opt-in. A briefed caller may use normal tool-mediated
  presentation when injection is disabled or unavailable; report which route
  actually occurred rather than silently substituting a new user turn.

**Closure evidence:** one real tool invocation presents its commentary once,
appends it to the intended provider history without an extra generation, and
the next model request recognizes the communication as already fulfilled.
Exercise retry/replay and unsupported-provider behavior as well. Keep the
non-injection presentation path independently usable.

**Related:** [stdout-aligned commentary design](../topics/acli.sketches.md#stdout-aligned-commentary)
and [calling-agent dialogue](acli-calling-agent-dialogue.md), a separate route
where a tool requests the agent's judgment rather than communicates to the user.
