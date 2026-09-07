# acli sketches

> Dormant candidate extensions to the acli spec; none is current behavior
> until promoted into `acli.md` and implemented.

Topic: `acli`

## `+confirm`: two-phase action/confirmation verbs

For verbs whose result has a slow follow-on check — push to GitHub Pages,
then the deploy propagates; push to a repo, then Jenkins goes green — the
fast action result and the slow confirmation are two phases of one verb.

- **Output contract.** The action result prints on stdout as usual; then,
  unless the caller chose to wait, the verb's last stdout line is a
  confirmation-phase deferral envelope (a `kind` distinguishing it from the
  plain deferral in § Expected duration and output channel, which mandates
  wholly-sync or wholly-deferred output — `+confirm` is the sanctioned
  two-part exception). The envelope names the channel, the watcher job, and
  the literal prefix of the future notification, so the calling agent is
  told at call time what turn to expect.
- **Watcher engine: agentctl by reuse.** The verb launches its checker as
  `agentctl start --no-aim confirm-<slug> -- <check-cmd>`, buying the
  detached wrapper and recorded exit, `wait`/`watch` foreground attach, the
  wake-plugin turn POST (YA session-wake), the caller's active-entry launch
  note, and `--after confirm-<slug>` gating of successors on confirmation
  (the watcher exits 0 only on CONFIRMED, and `--after` requires clean
  exit). Extracting the wrapper machinery into `acli` is a later refactor
  if a non-agentctl consumer appears.
- **Caller-selected notice.** Standard flags wired by capability
  registration: `--confirm-wait` (foreground both phases; blocks the async
  notice and puts the confirmation on stdout), `--confirm-channel
  turn|job|file` (`turn` = watcher wake-POSTs the calling session; `job` =
  agent backgrounds `agentctl wait confirm-<slug>` itself — on Claude the
  harness's tracked-job completion then re-invokes it with no YA
  dependency; `file` = watched file), `--confirm-timeout`, `--no-confirm`.
  Agent default: action foreground, confirmation deferred. Human-detected
  default: action result plus one line naming the watcher job and the
  attach command.
- **Notification grammar**, three-valued so a watcher timeout never reads
  as success: `[confirm] CONFIRMED: <what>`, `[confirm] DISCONFIRMED:
  <what> — <evidence>`, `[confirm] UNRESOLVED: <what> — <timeout/error>`.
  Standing guidance for receipt: CONFIRMED → one-line acknowledgment,
  clear any pending note, no action; DISCONFIRMED/UNRESOLVED → treat as a
  fresh defect signal.
- **Registration brings help.** Declaring `+confirm` in `acli.args` wires
  the flags *and* renders a canonical library-owned help section
  explaining the two-phase output, envelope, and channels — the same prose
  in every `+confirm` tool, so the capability cannot be declared without
  shipping its self-contained explanation, and the banner/footer cannot
  advertise what is not wired.

## `+defer` as an explicit token

The § Expected duration and output channel deferral envelope is today a
per-verb behavior documented in help. A `+defer` token would surface it in
the capability line the way `+confirm` surfaces the two-phase form, with
the same registration-brings-flags-and-help mechanism (`--timeout`,
channel selection, the envelope's `ref`/status fields).

## Optional color for text output

Possible later affordance, with no current implementation intent: opt into
color for `--text` output, using detected terminal capabilities (`TERM` and
terminal presence) or an explicit terminal specification, including `plain`.
Keep structured JSON output unchanged. The shared library would own capability
selection and styling so individual text renderers do not invent incompatible
color flags. Plain output remains available for captions, logs, and pipes;
the exact flag names and detection precedence are undecided.

## Stdout-aligned commentary

User-approved direction; shared library encoding and YA presentation remain
unimplemented. [Caller guidance](acli.md#tool-mediated-user-communication)
applies now when a tool and its consumer already declare such presentation.

Keep commentary aligned with ordinary stdout results. For implementing tools,
emit it by default; do not require `--commentary`. A proposed
`--no-commentary` suppresses commentary metadata and metadata-only records for
callers needing only result data. Existing consumers should be inspected and
updated where needed, without inventing a compatibility population. This is
an extension adopted by a tool, not a claim that every current acli v1 consumer
already accepts it.

Participating tools reserve `_acli` on any JSON object, including nested
objects; `_acli.commentary` holds an array of commentary items. Result fields
stay in their existing locations. Indicative encoding, not a wired API:

```jsonl
{"_acli":{"commentary":[{"text":"Checking the configured remotes."}]}}
{"remote":"a","ok":true,"_acli":{"commentary":[{"text":"Remote a responded."}]}}
{"remote":"b","ok":false}
{"_acli":{"commentary":[{"text":"Finished: one remote responded; one failed."}]}}
```

The initial YA presentation collects commentary into a `ul` or paragraphs
styled like assistant prose while retaining the normal output box. Collect per
tool invocation, preserving JSONL record order and commentary-array order;
the rendered commentary need not be physically interleaved with data rows.
Within nested JSON, walk members in serialized encounter order and arrays in
index order. That is deterministic presentation order, not a claim about
execution chronology; use an explicit commentary array or separate JSONL
records when semantic ordering matters.

Recognize metadata only in output of tools adopting this convention. Recurse
through ordinary objects and arrays, but not into `_acli` metadata or strings
that happen to contain JSON. For the normal output view, remove recognized
`_acli` members while preserving surrounding containers, empty objects, and
array positions. A metadata-only top-level JSONL record produces no data row.
Ordinary fields named `commentary` or `announcements` are application data.
Tools forwarding arbitrary external JSON must account for the reserved-name
collision before adopting recursive extraction; literal-data escaping remains
an implementation decision.

Serialize complete records on the same stdout stream and flush at commentary
boundaries for prompt delivery; flushing cannot overcome downstream buffering.
YA can strip protocol syntax from the displayed result, but the agent must
retain the announcement text and evidence that it was presented, as required
by the caller guidance.

A complete JSON document can use metadata on any contained object; a bare
scalar or an array without objects needs an envelope or another agreed
representation to carry commentary. Incremental commentary in a single
JSON document needs a streaming parser. Text and TOON require explicit packet
framing if they share stdout with commentary. Marked stderr packets remain an
alternative when stdout must stay unchanged, but do not supply the same
cross-stream ordering. Exact framing outside JSONL remains undecided.

Use fluent statements scoped to the tool's actual observations and actions;
do not invent the calling agent's reasoning, intentions, or independent checks.
Normal acli operation remains independent of YA. A YA parser may upgrade the
presentation; provider history injection is separately opt-in and tracked in
the [injection gap](../gaps/acli-commentary-history-injection.md).

## Calling-agent dialogue

[Dormant gap](../gaps/acli-calling-agent-dialogue.md): tools may request answers
from the calling agent and resume through existing watched-process handling.
A live stdin/stdout exchange or a fresh process attaching to the same tool
session can carry the interaction. No new mechanism is needed for the examples
considered. The gap records self-documentation, pending-result tracking, and
optional broker/standard adapters; interface choice waits for a concrete
workflow and evidence of harness/model competence. Human input remains a
different interaction.
