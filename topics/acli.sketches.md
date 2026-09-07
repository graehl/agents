# acli sketches

> Candidate extensions outside acli v1; none is advertised until its
> contract is specified and its implementation is wired.

Topic: `acli`

The current contract lives in [acli-spec](acli-spec.md), with calling guidance
in [acli](acli.md) and library advice in [acli-implementer](acli-implementer.md).
These proposals are not needed by a session merely using an acli tool.

## Deferred results

A possible `+defer` package would standardize operations that begin
synchronously and hand off unfinished work. The candidate behavior is to
return the complete stdout result within a caller-selected timeout, otherwise
return an arrangement acknowledgement identifying a durable delivery route.

An illustrative envelope is:

```json
{"kind":"deferred","id":"job-123","output":{"channel":"file","path":"result.json"},"expected":"minutes","status":["tool","status","job-123"]}
```

This is not a reserved v1 schema. Before adoption, define success versus
arrangement, record framing, status/cancellation commands, timeout meaning,
restart behavior, and retrieval after a lost notification. If a file is the
delivery route, establish its watch target before acknowledging arrangement.

For a single-result operation, a useful invariant would be that the result
arrives wholly on stdout or wholly through the deferred route. Streaming
partial results need their own explicit transition and deduplication semantics.
A UI queue accepting a notification is not proof of delivery to the session.

## Two-phase confirmation

A possible `+confirm` package would distinguish completing an action from
observing a later condition, such as publishing a site and then verifying
that it serves the new content. The first result would acknowledge the action;
a second result would state confirmed, disconfirmed, or unresolved, with
evidence and an operation identifier.

Caller options might select foreground confirmation, a broker message, or a
watched result file. Help would explain both phases and their failure modes.
A standard package needs interruption/retry semantics and a way to recover a
lost confirmation. Reuse a host's existing job observer when available;
the protocol should not mandate a particular launcher or backgrounding trick.

## Mixed commentary framing

`commentary/1` currently uses JSON/JSONL metadata. Text and TOON could later
use a packet format carrying ordinary output and commentary in one ordered
stream. Alternatively, marked stderr packets could preserve an application's
stdout format, but cannot provide a reliable total order across both streams.

Before selecting a framing scheme, test a real fixed-format consumer,
incremental parsing, flushing, malformed packets, suppression, and source
context. Raw prose in JSONL is not an implementation of this proposal.

## Optional assistant-history insertion

An aware UI can present commentary and tell the calling agent what was shown
without inserting an assistant-authored history item. A separate integration
could insert provider-native history items for hosts that support it.

Such an integration needs explicit enablement, preserved tool origin,
idempotent replay, delivery tracking, and behavior on provider rejection.
It must not manufacture the model's reasoning or require the agent to believe
it authored tool output. A YA provider service or session-turn enhancement is
one possible implementation boundary; no such API is defined by acli v1.

## Calling-agent dialogue

A tool could request a decision from its calling agent and resume through
stdin/stdout or a later process attaching to the same operation.
Existing watched-process or broker facilities may suffice; protocol design
should follow a concrete workflow.

Specify how pending questions, answers, cancellation, completion, and process
loss are represented before naming a capability. Agent decisions and human
approval are distinct interactions. A request emitted to a pipe does not
establish that either recipient saw it.

## Shared options and configuration

Small language-specific components could compose capability option definitions
and conditionally insert metadata. A shared core might resolve explicit CLI
values over environment, config, and defaults, retaining which source won.

This remains a library/configuration proposal. No config location, generic
environment mapping, parser-composition API, or TypeScript package is required
by v1. Register option definitions before one parse rather than stripping
arguments through a sequence of independent parsers.

## Optional text color

Text renderers could offer color selected explicitly or through a documented
terminal capability policy. Structured JSON must remain unaffected, and plain
text must remain available for pipes and captions. Flag names and detection
precedence are undecided.
