# Implementing acli tools

> Advice for implementing acli contracts in any language, with the Python
> library's supported surface, integration responsibilities, and limitations.

Topic: `acli-implementer`

The [user guide](acli.md) explains how agents call tools; the
[v1 specification](acli-spec.md) owns the protocol. Those two files can be
vendored together without this guide. This document describes implementation
choices and does not add requirements to a partial capability declaration.
Future proposals belong in [acli sketches](acli.sketches.md).

## Choose the smallest truthful declaration

Use the full baseline for a general agent-facing CLI. Use individual
capability packages for a runnable whose existing usage already serves its
specific agents. A partial tool implements each declared package completely,
without adopting unrelated protocols or a library.

For example, a TypeScript capture script can add a structured mode and
`--no-commentary` to its existing parser, construct `_acli.commentary` in
ordinary objects, and serialize them. Its `--help` or agent guide can declare:

```text
From the project directory:
  pnpm -s artifact:capture <html-path> --json
  pnpm -s artifact:capture --help

--json emits one compact JSON result. Commentary is included by default.
--no-commentary omits commentary metadata and retains ordinary result data.
--text emits readable text without structured commentary.
Commentary text is Markdown for an aware consumer; emission does not prove
that the consumer presented it.

acli-capabilities: commentary/1
```

This is an example contract, not a statement about an existing script's flags.
If the tool uses a guide-only declaration, omit the unsupported help invocation.
Its language and package-manager launcher impose no extra protocols.

Build exact argv from the documented invocation; do not discover invocation
methods by guessing how to execute a source file. Include capability scope
in both guide and help when supplying both. Keep mirrored declarations aligned.

### Small shell scripts

Use `commentary-lines/1` for text-producing scripts. A complete minimal
guide-declared example needs no JSON serializer:

```sh
#!/bin/sh
# Agent guide: ./report.sh [--no-commentary]; prints text and exits when done.
# acli-capabilities: commentary-lines/1
case "$#:$1" in
  0:) commentary=yes ;;
  1:--no-commentary) commentary=no ;;
  *) printf '%s\n' 'usage: report.sh [--no-commentary]' >&2; exit 2 ;;
esac
printf '%s\n' '# acli-capabilities: commentary-lines/1'
printf '%s\n' 'Report complete.'
if [ "$commentary" = yes ]; then
  printf '%s\n' '# _acli.commentary: The report completed successfully.'
fi
```

This partial tool does not claim the full acli interface or its JSON error
envelopes. Use the application's existing option parser when it has one.
Send both the declaration and marked lines to stderr when stdout must retain
another format; such commentary is unsequenced relative to stdout. Flush
buffered stdout before a stdout note about it. Each marked line is one
independent Markdown item; multiline items still use JSON commentary.

## Implementation boundaries

Use the program's existing parser and serializer for simple partial support.
A shared component earns its place when multiple tools need the same behavior.
Keep a capability's protocol logic independent of application schemas,
Playwright, the UI renderer, and the choice of parser.

If composing option groups, register all declarations before parsing once.
Sequential parsers that remove recognized flags can misinterpret another
group's values, positionals, or `--`. Detect option ownership conflicts and
preserve absent values until applying defaults. Do not invent a common
environment/config contract: v1 standardizes detection inputs and
`ACLI_QUIET`, not a general configuration system.

Validate output before publishing the affected JSONL record or JSON document.
Once earlier stream records have been emitted, a later failure must preserve
their partial-result status. A whole document needs serialization or validation
before the first write. Application exceptions belong at the command boundary;
translate expected errors into the standard envelope when claiming the baseline.

For commentary, construct metadata only in participating modes or explicitly
handle a conflicting encoding. Suppression is a data projection, not a string
replacement. Preserve decoded Markdown and serialized member order.
UI context resolution and delivery receipts belong to the consumer; a producer
must not infer presentation success from a flush.

Keep normal schemas small enough for the task, without arbitrary field-count
limits. Prefer named composite verbs for repeated multi-step operations.
Support stdin composition where schemas naturally match; do not force every
command to accept its own output. Document side effects and retry semantics
rather than promising that all mutations are inherently idempotent.

## Python library

The optional [Python library](../acli/) provides dependency-free protocol
helpers; rich REPL editing is optional. The importing application controls how
the library is installed or vendored. No home-directory bootstrap is part of
the protocol, and non-Python tools need not launch a Python subprocess.

The Python writers implement `commentary/1`; they do not emit the separate
`commentary-lines/1` format. Shell producers can implement that format directly.

| Module | Surface | Integration responsibility |
| --- | --- | --- |
| `acli.session` | `is_agent_session`, `resolve_format`, `Format` | Resolve flags and pass the selected format to the writer. |
| `acli.emit` | `emit`, `write_jsonl`, `write_pretty`, `write_toon_table` | Supply the application value, text renderer, and supported TOON shape. |
| `acli.commentary` | `commentary`; writer-side validation/projection | Pass the suppression choice to the emitter. |
| `acli.errors` | `ExitCode`, `error_envelope`, `die` | Translate application failures at the execution boundary. |
| `acli.args` | `argument_parser`, `add_standard_args`, capability footer/banner | Advertise only wired capabilities; define application arguments and help. |
| `acli.args` | `maybe_complete`, `set_completer`, `candidates`, `hint` | Dispatch completion before action side effects. |
| `acli.shell` | `run`; `maybe_repl` is exported from `acli` | Supply command callbacks; optionally bind a grammar with `rewrite`. |

### Output and errors

`write_jsonl` treats a nonempty list/tuple as a sequence of records; an empty
list/tuple emits one `[]` record. Other values emit one record. To send a list
as a field in one response, wrap it in an application envelope.
For completion, call the completion API or write each candidate separately:
zero candidates must remain zero records, rather than an empty-result record.

`write_pretty` emits one indented document. Both JSON writers reject non-finite
numbers before writing the affected value. The JSONL writer retains earlier
complete records if a later record fails; document encoding is completed in
memory before any output. Application numeric types still need an explicit
JSON representation.

`ArgumentParser.error` produces a `usage` envelope, exit 2, with usage text
in `error.detail.usage`. Explicit help retains stdout and exit 0, without a
startup banner. This behavior belongs to `acli.argument_parser`; adding
standard options to an ordinary argparse parser does not replace its errors.

`die` emits a final structured stderr error and raises `SystemExit`.
Its details must also be valid JSON. Neither the parser nor the emitter
automatically catches arbitrary exceptions thrown by the application.

### Parser and commentary wiring

`argument_parser` supplies help/footer/banner behavior and the text,
commentary-suppression, and banner-suppression flags.
`add_standard_args` adds the output selectors and `--full`.
Its `allow_toon=False` default prevents TOON selection; set it only on
supporting commands and advertise `+toon` there.

The factory's default capability tuple includes `complete`; explicitly pass
the capabilities actually implemented. Use `capabilities=()` for the baseline
with no optional packages. This still claims the full baseline, not partial
support. Partial implementations using an ordinary parser should render their
own narrow declaration and implement only their selected contracts.

A minimal commentary emission path is:

```python
import acli

parser = acli.argument_parser(
    description="Report capture paths (instant; final result on stdout).",
    capabilities=("+commentary",),
)
acli.add_standard_args(parser)
args = parser.parse_args()

try:
    fmt = acli.resolve_format(args)
except ValueError as exc:
    acli.die(str(exc), acli.ExitCode.USAGE)

result = acli.commentary(
    "No captures are available.", value={"items": [], "count": 0}
)
acli.emit(result, fmt, commentary=not args.no_commentary)
```

This example has no truncated fields, so `--full` leaves its result unchanged.
A real command supplies its schema and catches its own action/serialization
failures. `commentary(*texts, value=object)` returns a new object and appends
to existing commentary without mutating its input; omit `value` for a standalone
record. Metadata may appear on nested objects. The writers implement validation,
projection, and commentary flushing; accepting the option alone does not wire it.

`--no-commentary` works before or after subcommands on the factory.
When using `add_standard_args` with ordinary argparse, use
`getattr(args, "no_commentary", False)` if the option is absent.
Text without a renderer falls back to JSONL. Text with a renderer, or TOON
with constructed commentary, requires suppression or an explicit JSON mode.

### Completion and REPL

Call `maybe_complete(parser)` before normal parsing or application side
effects. It handles flags, verbs, and choices; attach value lookup with
`set_completer(action, fn)`. The function receives `(prefix, tokens)` and
returns strings or candidate objects. `hint(text)` makes a display-only row;
`candidates(parser, tokens)` exposes the same computation in-process.

`maybe_repl(parser)` wires the bare command loop.
`acli.shell.run` supports a tool-specific `rewrite` function for bound
grammars. It catches per-line exit statuses and continues, uses indented JSON
by default, and suppresses prompts on non-TTY input. Rich editing uses
`prompt_toolkit` when installed, with readline fallback. Library choice,
history storage, and editing dependencies are implementation details.

## Coverage and remaining integration gaps

The library implements structured argparse failures, explicit empty JSON
results, and finite-number enforcement in result/error serialization.
Regression checks cover these through the public emitters and a real CLI
help/error path. They are supported behavior, not deferred gaps.

The remaining boundaries are:

- **Partial discovery has no Python factory adapter.** The factory renders
  the full `acli:` declaration. Ordinary help or an agent guide can already
  declare partial packages manually; no new library is required.
- **Application conformance is not automatic.** Schema/truncation rules,
  action errors, retries, permissions, stream completion, and duration/channel
  help remain the command author's responsibility. Existing tools need their
  own entry-point checks.
- **TOON is a narrow encoder, not a verified full upstream implementation.**
  Validate a concrete command's selected upstream version, empty-table schema,
  and scalar cases before advertising it. The library requires explicit
  columns for an empty table.
- **UI presentation is consumer integration.** The library emits and suppresses
  commentary; it does not render prose or acknowledge user delivery.
  No provider-history insertion is implemented by these helpers.

## Verification before declaring support

Run the [spec's conformance checks](acli-spec.md#conformance-checks) against
the actual entry point. Include help or the guide-only path, unsupported
arguments, empty results, suppression, and the modes the tool advertises.
For a wrapper command, test through the wrapper as well as the imported
library. Register completion only after confirming that its special invocation
cannot fall through to ordinary work.

Keep protocol decisions in the spec and implementation observations here.
A shared helper's test coverage does not excuse an unwired caller.
