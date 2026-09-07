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

## Calling-agent dialogue

[Dormant gap](../gaps/acli-calling-agent-dialogue.md): tools may request answers
from the calling agent and resume through existing watched-process handling.
A live stdin/stdout exchange or a fresh process attaching to the same tool
session can carry the interaction. No new mechanism is needed for the examples
considered. The gap records self-documentation, pending-result tracking, and
optional broker/standard adapters; interface choice waits for a concrete
workflow and evidence of harness/model competence. Human input remains a
different interaction.
