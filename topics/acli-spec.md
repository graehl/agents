# acli v1 specification

> The language-independent contract for full acli tools and independently
> adopted capabilities, covering discovery, invocation, output, and consumers.

Topic: `acli-spec`

## Scope and conformance

This document defines acli version 1. **Must** states a requirement,
**should** a recommendation that may have a documented reason for differing,
and **may** an option. Requirements apply only to the declared surface.
No programming language, library, package manager, or session host is required.

A **full acli tool** declares `acli: 1` and implements the baseline below.
A **partial implementation** declares selected versioned capability packages.
It implements each selected package and its discovery requirements, without
inheriting the baseline or unrelated packages. A package is a protocol contract,
not a software dependency. Direct implementation in a small script is valid.

A partial declaration may be witnessed in either the tool's `--help` or its
agent instruction guide. A guide-only tool need not implement `--help`.
Instructions must identify the exact runnable and supported modes; a source
path or an unsupported flag is not a capability declaration.
The full baseline always requires `--help`.

The baseline comprises help and invocation, JSONL/JSON output, result/error
semantics, nonblocking agent operation, and the launch banner.
Optional packages are:

| Package | Full-acli token | Contract |
| --- | --- | --- |
| `commentary/1` | `+commentary` | Markdown metadata in declared JSON/JSONL modes. |
| `complete/1` | `complete` | Argument completion through `--acli-complete`. |
| `repl/1` | `repl` | An explicitly requested command loop through `--repl`. |
| `toon/1` | `+toon` | Explicitly selected flat-table TOON output. |

The second-column spellings are v1 shorthands for the packages.
None is implied by `acli: 1`. Application features need not become packages.
A declaration identifies producer support, not implementation language, UI
rendering, or provider-history delivery. Importing a library does not certify
a runnable's compliance.

## Discovery and help

### Declarations

The declaration is one unwrapped ASCII line, with single spaces between tokens:

```text
acli: 1
acli: 1 complete +commentary
acli-capabilities: commentary/1
acli-capabilities: complete/1 commentary/1
```

These are alternatives, not four lines to emit together. Use one full or
partial declaration per declared command scope. Partial declarations list at
least one package. Advertise only behavior that is wired, not merely accepted
options. If subcommands have different capabilities, help or the guide must
identify which packages apply to each verb. A root declaration does not imply
every listed package applies to every subcommand.

Names and versions are case-sensitive. Consumers must not assume they
understand unknown versions or packages. An unknown optional token does not
invalidate independently understood capabilities. Consumer support for one
package does not require support for all packages listed.

A script may mirror its declaration in a comment within the first 1 KiB,
using its language's comment syntax. This permits inspection without execution.
Help or the explicit agent guide remains the behavioral authority.
A conflicting mirror is a tool defect; do not guess which behavior is wired.

### Invocation and capability interrogation

Help or the agent guide must give the executable/launcher prefix, working
directory requirements, argument grammar, output modes, and relevant capability
behavior. Package-manager and interpreter entry points are valid.
A library import does not declare another externally callable transport.

When `--help` is supported, an explicit help request must:

- work without required action operands;
- perform no ordinary command action or interactive prompting;
- exit 0 and write help to stdout;
- end with the applicable declaration as the final nonempty stdout line; and
- omit the startup banner. Stderr remains available for diagnostics.

Error-triggered usage may appear on stderr with a nonzero exit; that is not
successful help interrogation. Full tools must also provide subcommand help.
Help must describe flags, results, exit statuses, and capability restrictions
without requiring this document. Keep option names searchable and do not
hard-wrap descriptions to a guessed terminal width; human wrapping may be opt-in.

A partial tool may instead put its declaration and equivalent usage details
in its agent guide. Callers must use that documented route rather than
inventing a `--help` requirement or assuming baseline flags exist.

Consumers may inspect approved entry points through help or supplied guides.
Automatic discovery/completion must use an explicit registry or allowlist,
not trial execution of arbitrary programs with special flags. An entry point
supplied for the task can authorize deliberate inspection; a marker found
in an arbitrary file does not authorize execution. For help probes, capture
status and stdout separately from stderr, bound execution time, and reject
failed or malformed responses. Cache with the command identity and scope;
refresh when its executable, guide, or registration changes.

## Full baseline

### Invocation

Unknown options and invalid arguments must fail before the requested action.
Honor `--` as the end of options. Help must identify argument placement
restrictions; callers should use the shown placement. Do not interpret
argument strings as shell commands unless that is the documented operation.

Agent and noninteractive calls must not block on human confirmation prompts.
Execute within established authorization or return an error explaining the
needed explicit option or prerequisite. Agent detection is not itself approval.
Interactive human confirmation may remain; any bypass must be documented.

### Output format

Full acli requires compact JSONL and whole-document JSON. Structured stdout
must be UTF-8, use valid JSON values, and contain no banners, progress prose,
terminal escapes, or logs. Emit finite JSON numbers. Represent values outside
a consumer's exact numeric range as documented strings when necessary.
Application schemas must identify the result shape and precision limits.

| Option | Meaning |
| --- | --- |
| `--json`, `--compact`, `--format jsonl`, `--format compact` | Compact JSONL. |
| `--pretty`, `--format pretty` | One indented JSON document. |
| `--text`, `--format text` | Prefer readable text; JSONL fallback is permitted. |
| `--full` | Restore details omitted by the default projection or truncation. |

These are baseline options. In v1, `--json` deliberately means JSONL, including
when a command emits multiple records. A one-record JSONL response is also a
JSON document. Select `--pretty` when a single document is required.
Conflicting encoding selections must fail, rather than letting argument order
silently select the parser the caller needs.

`--text` is a preference, not an encoding guarantee. An explicit structured
encoding overrides it. A command without a text renderer emits JSONL.
`--format text` participates in the mutually exclusive format selection.
Text changes presentation, not the action or exit/error semantics.
A consumer requiring prose must use a verb promising a text renderer.

Without an explicit selection, choose JSONL if stdout is not a TTY, if
TTY detection is unavailable, or if any of these indicators has a nonblank value:

```text
AGENTCTL_SESSION_ID
AGENT_GUARD
CLAUDECODE
CLAUDE_CODE_*      (any variable with this prefix)
CI
CODEX_THREAD_ID
PI_CODING_AGENT
```

Otherwise choose indented JSON. These indicators affect only the default,
not authorization or session identity. Additional host indicators may be
supported and documented. Never automatically select text or TOON.
Explicit flags override detection. No general environment/config equivalent
to these options is standardized in v1.

JSONL has one complete JSON value per line, terminated by LF; line breaks
inside strings are escaped. Emit no blank or comment lines.
Document mode represents the same logical result in its documented shape.
A row stream may become an array; a single response envelope may remain an
object. Do not silently drop application data between encodings.

### Results, empty states, and truncation

Help must describe the default schema and distinguish no matches, a missing
resource, and a predicate returning false where relevant.
A query with no matches must emit an explicit empty result, such as
`{"items":[],"count":0}` or `[]`, rather than silence. A successful mutation
must return a documented acknowledgement or result. Completion's empty stream
is an explicit exception defined by that package.

Default results should contain the fields needed for the normal task.
Disclose omitted fields/content and how to obtain the full result.
Content truncation must carry a size/count hint. `--full` restores omitted
available content; it does not grant permissions, fetch unbounded future data,
or bypass an independent pagination boundary. If nothing is omitted,
accepting `--full` may leave the output unchanged.

Streaming commands must document partial results and what establishes
completion. Flush complete records as they become available; a write or flush
does not guarantee downstream delivery. A valid partial record is not evidence
of overall success. A nonzero exit or interrupted transport must remain visible.

### Errors and exit statuses

Expected command failures, including invalid arguments, must end stderr with
one compact JSON error object followed by LF:

```json
{"ok":false,"exit_code":4,"error":{"code":"not_found","message":"Artifact not found.","detail":{"path":"capture.png"}}}
```

`ok` is false; `exit_code` matches the process status; `error.code` is a stable
machine-readable string; `error.message` is useful human-readable text.
`error.detail` is an optional object for application-specific detail.
Diagnostics may precede the final line; callers must not parse all stderr
as one JSON document. Do not substitute a success envelope on stdout for a
nonzero failure status.

| Exit | Error code | Meaning |
| --- | --- | --- |
| 0 | — | Success. |
| 1 | tool-defined | Documented negative predicate/gate result or tool-specific failure. |
| 2 | `usage` | Invalid invocation. |
| 3 | `data` | Invalid input data. |
| 4 | `not_found` | Requested resource absent. |
| 5 | `conflict` | State prevents the operation. |
| 69 | `unavailable` | Required service/resource unavailable. |
| 70 | `software` | Internal failure caught at the command boundary. |
| 75 | `temporary` | Temporary failure; retry may be appropriate. |

Document additional statuses. A legitimate negative predicate may use its
ordinary result schema instead of an error envelope; help must explain it.
Unhandled termination or signals may prevent an envelope, so callers must
also inspect process status. A timeout or temporary status does not prove a
mutation had no effect; document retry/idempotency behavior where it matters.

### Stderr banner at launch

After successful argument parsing and before ordinary work, a full tool emits
one stderr line: `# ` followed by its full capability declaration.
Emit it once per process, not once per record. `--acli-quiet` suppresses it,
as does a nonempty `ACLI_QUIET` environment value; this environment switch
treats even `0` as nonempty.

Help and completion requests emit no banner. Ordinary diagnostics and the
final error envelope may follow a launch banner. A partial implementation
need not provide a banner or its suppression options.

## Commentary package: commentary/1

### Encoding and activation

This package applies only to JSON/JSONL modes declared in help or the agent
guide. Commentary is enabled by default in those modes; `--no-commentary`
suppresses it. Structured output need not be the command's default mode.

Participating outputs reserve `_acli` on any JSON object, including nested
objects. In v1 its value must have exactly this shape:

```json
{"commentary":[{"text":"Nonempty Markdown prose."}]}
```

The array is nonempty; each item contains only `text`, a nonblank string.
Do not emit empty metadata or use `_acli` as an ordinary field in a participating
output. Malformed metadata must fail visibly; consumers must not silently
strip or render it. Retain raw output for diagnosis. Producers must validate
before writing the affected record.

Metadata may be attached to data or emitted as a standalone object:

```jsonl
{"path":"capture.png","width":1200}
{"_acli":{"commentary":[{"text":"Captured [the page](capture.png)."}]}}
{"path":"mobile.png","_acli":{"commentary":[{"text":"The mobile capture is ready."}]}}
```

Ordinary fields such as `commentary` remain application data.
Do not search strings or recurse inside the metadata object itself.
Interpretation requires a declared participating tool/mode; a matching key
in unrelated output does not activate the protocol.

### Prose and source context

Decoded `text` is Markdown prose. Preserve its characters, whitespace,
Unicode, links, and math delimiters exactly; do not paraphrase it.
An aware UI uses the same prose renderer and link policy as assistant
messages, including supported math and media extensions. This promises normal
renderer semantics, not support for every extension.

The UI may collect items into paragraphs or a list beside the normal output.
Preserve record order, array order, and depth-first serialized object-member
encounter order. Items within each commentary array retain their order.
Producers must preserve intended member order when serializing commentary.
Do not infer execution chronology from object order.

Resolve context against the original value before stripping metadata:

| Placement | Context |
| --- | --- |
| Attached to an object with ordinary members | That enclosing object, excluding its metadata. |
| Metadata-only array element | Nearest preceding data item in that array. |
| Metadata-only top-level JSONL record | Nearest preceding data record in the invocation. |
| No such predecessor, or another standalone object position | No specific context. |

Skip metadata-only predecessors; an ordinary empty object still is a data
item. Do not reach into a previous invocation for context. Retain associations
when commentary is collected elsewhere. Nested maps and preceding items may
be shown in a hover hint or margin note, with equivalent keyboard/touch access.
A top-level map normally needs no duplicate tooltip because the full result
is nearby. Apply the usual invocation context when resolving relative links.

### Suppression and other encodings

The data projection removes recognized `_acli` members, preserving ordinary
containers, empty objects, and nested array positions. A metadata-only array
element becomes `{}`. A metadata-only top-level JSONL record is omitted.
Attach metadata to a data object when an extra array element is undesirable.

`--no-commentary` must produce this projection and retain ordinary data.
Do not replace suppressed records with blank lines. Consumer data views use
the same projection while retaining original source and context separately.
Flush commentary-bearing JSONL records and all preceding buffered stdout.
Flush whole-document JSON when complete; incremental rendering needs a
capable document parser.

V1 defines no commentary framing for text or TOON. A tool may document those
as separate modes without commentary. Do not silently discard already
constructed commentary when changing encoding: reject that combination with
an actionable error or require `--no-commentary`. Text with JSONL fallback
can carry metadata normally.

### Communication and delivery

Use statements supported by the tool's actions or observations. Do not
manufacture the calling agent's reasoning, verification, or authorship.

A tool whose declared presentation contract effects required communication
may satisfy an instruction to communicate something to the user.
The agent must know the text and delivery state through its result or history.
Once presentation is established, count that communication as done; repeat
it only when additional explanation helps.

Metadata emission, successful work, and prose delivery are distinct events.
A write, queue acknowledgement, or capability declaration alone is not a
presentation receipt. Presentation means available in the user's conversation,
not proof of reading. Failed work does not erase already presented prose;
successful work does not prove presentation.

Assistant-history injection is optional and not defined by `commentary/1`.
A briefed agent can recognize tool-mediated presentation without believing it
authored the text. Preserve tool origin and delivery state even when the UI
uses assistant-prose styling.

## Completion package: complete/1

Invoke `<entry-point> --acli-complete <argv-prefix...>`. The special option
must be the first argument after the documented entry-point prefix.
Remaining arguments exclude that prefix and represent the partial command.
The last token is being completed; a trailing empty token means a new argument.
An empty prefix is equivalent to one empty token. Prefer an argv array;
shell quoting is the caller's responsibility when using a shell.

Output is compact JSONL, one candidate per line:

```json
{"completion":"--json","kind":"flag","help":"Emit compact JSONL.","nospace":false}
```

`completion` is required and replaces the current token, rather than
appending a suffix. Optional `kind` is `flag`, `value`, `path`, `subcommand`,
or `hint`. Optional `help` is concise single-line text.
Optional `nospace` is a boolean, false by default; true asks the consumer not
to append a space. Empty completion is permitted only with `kind:"hint"`.
Hints are display-only and never inserted. Unknown optional fields may be ignored.

Preserve tool-chosen order; deduplication may preserve the first occurrence.
Put slot-wide guidance in one hint rather than on every candidate.
Report truncation through a hint with a count.

Completion must not perform the command action, prompt, require a TTY, emit
a startup banner, or mix other stdout protocols into its candidates.
It should finish within about one second; consumers must bound the request.
Read-only lookup of completion data is allowed.

Exit 0 with no lines means no candidates and permits generic path fallback.
Any valid candidate or hint suppresses that fallback. Nonzero exit, timeout,
or malformed output is failed completion, not a successful empty result.
Discard failed candidates; UI fallback is consumer policy. None of these
results authorizes invoking the ordinary command. Use registered entry points.

## REPL package: repl/1

`--repl` as the first argument starts an explicitly requested command loop.
Each nonempty input line supplies an invocation's arguments using shell-like
quoting, without shell expansion or execution. Extra launch arguments and
bound subcommand grammars must be documented.

`exit`, `quit`, or end-of-input ends the loop. A command's failure must not
end the loop: report its nonzero status on stderr as `# exit N` and continue.
The loop's process exit status does not summarize prior commands.
Non-TTY input must be read without prompts. The per-command default is
indented JSON where baseline output modes are supported; explicit per-line
encoding selections still win.

Interactive editing/completion is optional; `repl/1` does not imply `complete/1`.
A REPL is not a JSONL multiplexer: multi-document output and per-command
diagnostics require a REPL-aware consumer. Use separate ordinary invocations
when machine-readable command boundaries are needed.

## TOON package: toon/1

TOON (Token-Oriented Object Notation) is optional for every tool and consumer,
including table producers. `--toon` selects it explicitly; a full tool also
accepts `--format toon` when supported. Help must identify supporting verbs.
Never select it by row count or silently fall back to JSON after selection.

This package is restricted to one named flat table with a fixed ordered set
of scalar-valued columns. Declare table name, columns, and delimiter in help
or the result schema; retain them for empty results. Nested or nonuniform
rows are errors. The header declares the row count:

```text
captures[2]{name,ok}:
  desktop,true
  mobile,false
```

Use tabular-array syntax and string/number rules from the
[TOON specification](https://toonformat.dev/reference/spec), with the supported
upstream version stated in tool help. Comma is the default delimiter; document
tab or pipe variants. Consumers must understand the declared version and
profile before selecting TOON. This capability promises neither a token
saving on a particular payload nor a particular encoder implementation.

## Long-running work and progress

Help must state the expected duration (instant, seconds, minutes, or
open-ended), result channel, and how the caller recognizes completion.
Ordinary commands finish with stdout and process status. Work continuing
after return needs a documented acknowledgement, identifier, retrieval/wait
method, and failure handling. An acknowledgement means arranged, not completed.

V1 defines no standard deferral envelope, timeout-to-background transition,
callback broker, or calling-agent dialogue protocol. Do not infer one from
an application field such as `kind:"deferred"`. Open-ended work must not block
indefinitely unless the caller explicitly selects and understands that mode.

Progress must use a documented channel without corrupting structured stdout.
Stderr diagnostics must preserve the final error-envelope rule.
Workflow tags and visualization schemas are separate protocols: if supported,
help or the agent guide must describe their activation and stream.
Do not insert raw tags into JSONL or completion output.

## Conformance checks

Check the declared entry point, not just library functions:

- Identify its exact scope through help or the agent guide. Explicit help
  succeeds without operands and has the final stdout declaration.
- Exercise declared modes, invalid arguments, and representative failures.
  Full tools retain result/error separation and documented statuses.
- Check empty results, `--full`, and finite valid JSON. Compare JSONL and
  document modes against the declared logical result.
- Compare commentary enabled/suppressed, including nested objects,
  metadata-only records, and Markdown escapes. Resolve context before projection.
- For completion, check partial/fresh tokens, hints, empty answers, and failures
  without performing an ordinary command action.
- Verify any asynchronous completion or UI delivery claim against its own
  contract rather than treating process success as proof.
