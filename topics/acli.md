# acli: using agent-facing command-line tools

> acli (agent-CLI) provides discoverable command-line contracts: a full
> structured-output baseline or separately declared capabilities.

Topic: `acli`

Read this guide when a tool identifies itself as acli, or when its agent
instructions declare acli capabilities. Use the tool's exact invocation and
help/guide for its application-specific arguments. The accompanying
[v1 specification](acli-spec.md) defines the complete contracts.
These two documents are sufficient for users and consumers; no library,
repository layout, or particular session host is required.

## Discover what the tool supports

Use the entry point supplied by the tool's instructions, including its working
directory and any launcher prefix. For example, a documented package script
might expose help through `pnpm -s artifact:capture --help`.
A TypeScript source path alone does not tell you how to invoke it.

### Capability line, version, and help footer

Look for one of these declarations:

```text
acli: 1 complete +commentary
```

This promises the full v1 baseline, completion, and commentary.

```text
acli-capabilities: commentary/1
```

This promises only the commentary package. A small runnable may declare it
in `--help` **or its agent instruction guide**. A guide-only tool need not
provide help or unrelated baseline options. Do not infer `--pretty`,
completion, a banner, environment settings, or other features from partial
support. Implementations may use any language and need no acli library.

Successful explicit `--help` writes to stdout, exits 0, and ends with the
declaration as its final nonempty line. Keep stderr separate: error-triggered
usage is not successful help interrogation. Read any subcommand restrictions
before applying a root command's capability list.

| Seen in full help | Seen in a partial declaration | What it lets you do |
| --- | --- | --- |
| `+commentary` | `commentary/1` | Receive Markdown commentary with declared JSON/JSONL output. |
| `+commentary-lines` | `commentary-lines/1` | Receive marked Markdown lines on an activated text stream. |
| `complete` | `complete/1` | Request argument candidates. |
| `repl` | `repl/1` | Start an explicit command loop. |
| `+toon` | `toon/1` | Select documented flat-table TOON output. |

None of these packages is implied by bare `acli: 1`. Use capabilities whose
versions you understand. A script-header marker can help identify a candidate,
but does not authorize trial execution of arbitrary programs. Use the approved
entry point or the consumer's tool registry.

## Output format

For a full acli tool:

| Need | Selection |
| --- | --- |
| Compact machine output | Default for pipes/agents; `--json` explicitly selects JSONL. |
| One JSON document | `--pretty`. |
| Readable summary | `--text`, if the verb promises a text renderer; otherwise JSONL is allowed. |
| Omitted details | `--full`. |
| Data without commentary | `--no-commentary`, when commentary is supported. |
| TOON table | `--toon`, only on an advertised supporting verb. |

V1's `--json` means one JSON value per line, possibly multiple records.
A command's help tells you whether it emits rows or a single response envelope.
`--pretty` provides one document. Both are baseline requirements; TOON is
optional. Explicit encodings override the text preference and session detection.
Do not combine conflicting encoding flags.

Without flags, an interactive human TTY receives indented JSON; pipes and
detected agent sessions receive JSONL. Neither text nor TOON is auto-selected.
Partial tools choose their own documented default and supported modes.

Treat an explicit empty result as definitive. A missing result is not evidence
of zero matches. Read truncation counts and pagination boundaries before asking
for more; `--full` restores available omitted content, not additional authority
or an unbounded stream.

## Results, errors, and completion of work

Capture stdout, stderr, and process status. Full tools use stdout for results.
Failures end stderr with a compact error envelope, for example:

```json
{"ok":false,"exit_code":4,"error":{"code":"not_found","message":"Artifact not found."}}
```

Parse that last line, not the entire stderr stream. A tool may document a
negative predicate as a normal result with a nonzero status. Signals or
interruption may leave no envelope. Preserve prior valid stream records while
reporting that the overall call failed or did not finish.

### Stderr banner at launch

A full tool normally emits `# acli: 1 ...` on stderr once at launch.
It is metadata, not an error or a stdout record. `--acli-quiet` or nonempty
`ACLI_QUIET` suppresses it. Explicit help and completion omit it.
Partial tools need not emit a banner.

### Expected duration and output channel

Check duration, delivery channel, and completion conditions before choosing
how to run a slow tool. If it returns a job acknowledgement, use its documented
status/wait/retrieval method. Do not treat arrangement as completion or infer
a standard deferral protocol. A timeout does not prove that a mutation had
no effect; check state before retrying.

### Schema-announced workflow output

If a tool documents workflow tags or other progress protocols, use their
declared stream. Raw progress text does not belong in JSONL result or
completion output. See the spec's [stream rules](acli-spec.md#long-running-work-and-progress).

## Tool-mediated user communication

A tool may satisfy an instruction to communicate something to the user when
its declared presentation behavior and delivery result establish that the
communication occurred. Know what was presented and retain its delivery state.
Then count the communication as done; repeat it only when more explanation
is useful.

Operation success, commentary emission, and presentation are different facts.
Metadata in a raw pipe or a queue acknowledgement does not prove the user has
the prose in their conversation. Conversely, failure of the operation does
not erase commentary already delivered. Assistant-history injection is optional;
a briefed agent need not believe it authored the tool's text.

### Stdout-aligned commentary

Participating JSON/JSONL may contain `_acli.commentary` on any object:

```json
{"path":"capture.png","_acli":{"commentary":[{"text":"Captured [the page](capture.png)."}]}}
```

Its `text` is exact Markdown prose. An aware UI may collect it as paragraphs
or a list alongside ordinary output, using its normal assistant-prose renderer
for links, math, and supported media. Emission does not promise UI support.

Attached commentary refers to its enclosing object. A metadata-only array
item or JSONL record refers to the nearest preceding data item/record.
Top-level-map context normally needs no tooltip; nested maps and preceding
items are useful hover or margin-note context. Consumers resolve associations
before hiding metadata. Detailed ordering and data-preservation rules are in
the [commentary contract](acli-spec.md#commentary-package-commentary1).

Use `--no-commentary` for the ordinary data projection. Do not blindly strip
similarly named fields from unrelated tools or reinterpret JSON-looking strings.
Malformed participating metadata is an error, not prose to render.

### Shell-friendly line commentary

A script can opt a stream into `commentary-lines/1`, then print ordinary
output and marked Markdown with no JSON escaping:

```sh
printf '%s\n' '# acli-capabilities: commentary-lines/1'
printf '%s\n' 'report.html'
printf '%s\n' '# _acli.commentary: Built [the report](report.html).'
```

The declaration must be the stream's first line. Only the exact
`# _acli.commentary: ` prefix carries commentary; ordinary `# ` lines stay
data. Each marked line is a separate Markdown item. Use JSON commentary for
one item containing multiline Markdown.

On stdout, commentary refers to the preceding block of ordinary lines;
consecutive notes share that block. Flush buffered output before its note.
Sending the declaration and commentary to stderr with `>&2` preserves stdout's
format, but that commentary is unsequenced relative to stdout and gets only
invocation context. The same applies when an observer lost the original stream
identity. Do not infer associations from cross-stream arrival order.

`--no-commentary` omits marked records and retains ordinary data. Unaware
consumers retain readable text. The complete
[line commentary contract](acli-spec.md#line-commentary-package-commentary-lines1)
defines activation, framing, malformed input, and presentation.

## Completion protocol

With `complete/1`, invoke the documented entry point followed by
`--acli-complete` and the partial arguments. The last token is being completed;
pass a final empty string for a new argument. Results replace that token.
Preserve candidate order and never insert display-only hint rows.

A successful empty stream allows path fallback. A hint alone suppresses that
fallback. Failure or malformed output is not a successful empty answer.
Completion must not execute the ordinary action. Use registered entry points.
See the [completion contract](acli-spec.md#completion-package-complete1) for
candidate fields and quoting responsibilities.

## REPL (`--repl`)

With `repl/1`, an explicit `--repl` starts a command loop. Use it when the
documented repeated-call interaction is useful; do not assume every tool has it.
`exit`, `quit`, or EOF ends it. A failed line is reported and the loop continues.

The loop's final status does not summarize every command. Its output is not
automatically one JSONL stream; separate invocations are easier for consumers
requiring individual result boundaries. See the
[REPL contract](acli-spec.md#repl-package-repl1).
