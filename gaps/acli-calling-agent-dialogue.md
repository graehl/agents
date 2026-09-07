---
slug: acli-calling-agent-dialogue
noticed: 2026-09-07
where: acli/
---

**Status:** dormant idea, captured as a gap at the user's request. No specific
application is identified; implementation waits for a concrete need.

**Gap:** an optional avenue through the Python `acli` library for a tool to
request an answer from its calling agent and continue using that answer.
The calling agent answers using its task context and judgment. Asking the
human user is a different interaction and does not satisfy this idea.

**Noticed while:** discussing how instructed stdin/stdout dialogue,
continuations, and MCP (Model Context Protocol) could support the same tool
workflow. The user favors allowing useful interaction styles independently,
while leaving capabilities that are not yet needed unimplemented.

**Design sketch:** keep tool behavior separate from its interaction route.
The first candidate to test is instructed stdin/stdout dialogue: the tool
flushes a complete request line, the calling agent reads and answers it by
writing stdin, and the tool continues with its local state intact. Structured
line records can distinguish requests, replies, and results; diagnostics stay
on stderr. Explicit flushing at message boundaries is sufficient.

The execution harness must expose partial stdout, retain writable stdin, and
yield control to the calling agent while the process remains alive. Unbuffered
output alone cannot make a wait-until-exit execution interface interactive.
Tool instructions must tell the caller how to service requests rather than
simply wait for completion. Verify this path in the intended harness.

For async flows, a host broker can deliver a notification or request back to
the calling agent after the arranging invocation returns. Bind the destination
session and originating invocation name/id when granting the tool access to
the broker. The broker attaches that provenance; the payload cannot choose
another caller or claim user authority. An enforced visible prefix helps the
agent recognize the source, but trusted routing and tool-origin metadata carry
the authority distinction. Keep replies correlated with their requests.

The broker needs an explicit delivery rule for a busy, idle, or disconnected
caller. Many harnesses could plausibly expose this facility; actual support,
message placement, and wake/resume behavior must be verified per harness.

**Candidate shared owner:** the proposed YA provider daemon for cron-like,
session-involved actions could also own callback delivery. A scheduled trigger
and a tool callback are different event sources sharing session lookup,
queuing, delivery receipts, wake/resume, and reply routing. Preserve the
origin and authority of each source; delivery alone grants no new authority.
This is a proposed ownership boundary, not a claim that YA implements it.

Return-and-resume continuations remain useful when the live process cannot be
retained. MCP is another possible route: reuse its official Python SDK where
the semantics fit, keeping ordinary `acli` use independent of that dependency.
These avenues are independently optional. Select no public API until an
application establishes what is needed.

MCP user elicitation does not provide calling-agent judgment. A separate model
generation also does not establish access to the calling session's context.
An adapter must preserve who answers, associate each reply with its request,
and let the calling agent answer while the tool is suspended or yielded.
Unsupported routes, cancellation, and caller disappearance need explicit
outcomes; they must not silently turn into human prompts.

**Revisit when:** a tool needs calling-agent judgment during its workflow.
Exercise a complete request, agent answer, and continuation through the chosen
route before advertising it as an `acli` capability.

## Provider feasibility — 2026-09-07

Priority is Codex and Claude, then Grok. Installed CLI versions were Codex
`0.153.4`, Claude Code `2.1.263`, and Grok `1.0.13` (`5e9a58528b76`).

- **Codex live dialogue: exercised in the calling session.** A Python process
  emitted a flushed JSON question asking for seven squared, waited in
  `input()`, and checked the reply. `exec_command(tty=True)` returned the
  question and a live handle; the calling agent sent `49` through
  `write_stdin`. The process emitted `accepted: true` and exited 0. This
  verifies the PTY route; it also echoed input and used terminal line endings.
  It does not verify every harness's plain-pipe behavior.
- **Codex async delivery: documented and present in the installed schema.**
  `codex app-server generate-json-schema --experimental` exposes
  `TurnStartParams.toolOutput` with a tool name, namespace, and output, plus
  `CommandExecWriteParams` for writing process stdin. The
  [App Server documentation](https://learn.chatgpt.com/docs/app-server)
  says `turn/start` accepts tool output, preserves it as `functionCallOutput`,
  and queues it when a turn is active. Async delivery was not exercised.
- **Claude async delivery: documented.**
  [Monitor](https://code.claude.com/docs/en/tools-reference#monitor-tool)
  delivers command output lines or WebSocket messages to Claude. The
  [Channels preview](https://code.claude.com/docs/en/channels-reference)
  provides MCP notifications with a host-assigned source, optional metadata,
  and an ordinary MCP reply tool. Busy-session events are queued; transport
  writes are not processing acknowledgements. Both facilities have documented
  availability restrictions and were not exercised locally. The published
  [Bash schema](https://code.claude.com/docs/en/agent-sdk/python#bash) does not
  establish a retained stdin-write interface; direct live dialogue remains
  unverified.
- **Grok host control: documented and reflected in local CLI help.**
  `grok agent stdio` exposes ACP (Agent Client Protocol) over JSON-RPC;
  `grok agent serve` offers a WebSocket server. The
  [official example](https://docs.x.ai/build/cli/headless-scripting#acp)
  sends `session/prompt` and consumes `session/update`. This establishes a
  host-control route, not tool-origin callback delivery or writable child
  stdin. Those semantics and busy-session behavior remain unverified.

Contributing-model: 6-Astra

**Related:** [acli contract](../topics/acli.md#expected-duration-and-output-channel),
[acli sketches](../topics/acli.sketches.md#calling-agent-dialogue), and
[MCP Python SDK continuation documentation](https://py.sdk.modelcontextprotocol.io/v2/handlers/multi-round-trip/).
