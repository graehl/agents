# Agent CLI (ACLI)

> An ACLI (Agent CLI) is a command-line tool built agent-first: compact
> structured output by default, named composite verbs over agent-glued
> round-trips, structured errors and exit codes, and no interactive
> prompts — while protecting interactive human users by *detecting* them
> rather than making agent-friendliness opt-in.

Topic: `agent-cli`

Our term for the pattern the AXI project (Agent eXperience Interface,
`github.com/kunchenguid/axi`) names externally. This doc is prescriptive:
it is how we build CLI tools an agent will drive. A shared `acli` Python
package (see *The `acli` module*) turns each rule below into a callable so
compliance is the path of least resistance, not ten rules an author must
remember. `agentctl.py` is the flagship consumer.

The core stance, from which the rest follows: **the agent-friendly shape is
the default, never the opt-in.** An agent that forgets a flag must still get
usable output. What we make conditional is the *upgrade to human-readable
output*, gated on detecting that a human is actually there.

## Output format

**Compact by default; detect the human; flags win.** The no-opt-in rule
bites only when the fallback is hostile. Forgetting the base format would
drop an agent to pretty human output — hostile — so compact structured
output is the mandatory default. The tool decides format per call as:

```
compact (default) if ANY of:
    not isatty(stdout)              # workhorse: piped/redirected → machine consumer
    AGENTCTL_SESSION_ID set         # repo launcher (see agentctl active-sessions)
    AGENT_GUARD set                 # agent-guarded wrapper (provider-agnostic)
    CLAUDECODE / CLAUDE_CODE_* set  # Claude harness (survives a bare `claude`)
    CI set                          # defensive convention
    CODEX_THREAD_ID set             # Codex (thread-scoped id; presence ⇒ agent)
    PI_CODING_AGENT set             # pi (@earendil-works/pi-coding-agent) — explicit bool, cleanest
    # grok: no reliable marker found — omit rather than guess
pretty otherwise                    # real TTY AND none of the above → interactive human

# explicit --format / --compact / --pretty / --toon overrides the heuristic in both directions
```

Why a disjunction, not one env var: any single marker is sometimes absent
(a subshell that dropped it, a bare invocation, a different launcher).
`isatty(stdout)==false` already catches every piped or redirected call
regardless of env — most agent calls and every `| jq` / `> file`. The env
markers only cover the residual "real TTY but not an interactive human"
case (a PTY-allocating harness). Keep the whole disjunction in one function
(`acli.session`) so a new harness marker is a one-line edit. It is
deliberately *broader* than the session-id set agentctl uses for active
sessions (`AGENTS.md § Active sessions`): detection needs only *presence*,
so `PI_CODING_AGENT` (a boolean, not an id) and `CODEX_THREAD_ID`
(thread-scoped — finer than a session) both answer "is this an agent?" but
are not drop-in session ids.

**A "reasonable" heuristic is enough because both sides have an override.**
Detection sets only the *default*; an explicit flag always wins. A
mis-detected human passes `--pretty`; a mis-detected agent passes
`--compact` (or just parses the JSON anyway). The cost of a miss is one
flag, not a broken workflow — so ship a good disjunction, not an exhaustive
one.

**Default machine format is JSONL; the human fallback is pretty JSON, not a
table.** "Pretty JSONL" is a contradiction — JSON Lines is one compact
object per line, and indenting it breaks the line contract. So the human
path is a *different* format: a pretty (indented) JSON value. Prefer that
over an ANSI/box-drawing table as the fallback, because a mis-detected
agent still parses pretty JSON but chokes on a rendered table. If you want
tables for humans, gate them behind higher-confidence detection (real TTY
*and* no markers *and* a capable `TERM`) so a misread never lands an agent
on the one format it cannot read.

## TOON as an orthogonal agent opt-in

TOON (see `GLOSSARY.md`) is an upgrade *within* the compact branch, never
auto-selected. It is opt-in — and that does not violate the no-opt-in rule,
because forgetting `--toon` drops you to compact JSONL, which is already
friendly. It *should* be opt-in: only the calling agent knows the payload
is large and uniform and that it will treat rows as CSV. The tool cannot
know that; the caller can.

Scope, enforced by the tooling rather than by prose:

- **Large uniform tables with named columns only.** The saving comes from
  writing column names once instead of per row, so it amortizes over *rows*
  (roughly ≥ ~10 uniform rows). On nested, heterogeneous, or small payloads
  the saving shrinks to ~0 or reverses and compact JSON is as good or
  better.
- **Static per subcommand, not dynamic per call.** A subcommand's output
  format must be statically predictable so the consumer's parser is fixed;
  never flip format at runtime on actual row count. Gate at design time: a
  subcommand *expected* to emit large uniform tables is a TOON subcommand,
  and it emits TOON even on the occasional short result.
- **We write our own encoder — no dependency.** Our sanctioned use is the
  flat-uniform-table subset (`name[N]{c1,c2,...}:` header + delimited
  rows), which is a ~20-line encoder. Implement only that subset and raise
  on nested/non-uniform input, so the scope is self-enforcing rather than a
  rule to remember. (Consult `toonformat.dev` for the exact delimiter and
  quoting/escaping rules at implementation time.)

## Kill round-trips without becoming a scripting language

Round-trips (each a full agent turn: inference + latency + context growth)
are the real cost lever — far bigger than serialization. Own the common
multi-step paths *in the tool*, two mechanisms in priority order:

- **Named composite verbs (porcelain) for hot paths.** This is where
  "pre-computed aggregates" belong — as opt-in verbs, not fields baked into
  every base verb's output, which would fight *Minimal default schemas*
  below. `git pull` (= `fetch` + `merge`) and `git status` (an aggregate
  over the index) are the model. Agents want mostly porcelain; primitives
  stay underneath.
- **Closed-loop, pipeable I/O for the long tail.** "Output of one = input
  of the next" only works without glue if each verb *accepts on stdin the
  same compact format it emits*. Most CLIs break this — emit JSON, accept
  only flags — forcing the agent to parse-and-re-serialize between steps.
  That reshape *is* the ad-hoc script we are avoiding, leaking in at the
  seams. A closed-loop format lets `A | B` run as one invocation.

Two failure modes bound the design: too few named combos and the agent
experiments with composition (an unspecified scripting language —
non-deterministic, token-costly, mistake-prone); too many and you get verb
sprawl with its own discovery cost. **Name the empirically-hot paths; make
the rest pipeable.** Note the round-trip *win* needs single-invocation
composition (a pipe or a named verb) — a sequence of separate calls is
still N turns no matter how obvious the defaults; obvious defaults buy lower
mistake-rate, not fewer turns.

## The remaining principles

- **Minimal default schemas.** 3–4 fields per list item, not 10, with a
  `--full` / `-o wide` escape hatch. Real benefit both ways: fewer tokens
  and less distraction. The escape hatch is what keeps it from costing the
  human anything.
- **Content truncation with a size hint and `--full`.** Stops one huge blob
  eating the context window. The hint must state *how much* was cut and
  `--full` must be lossless.
- **Definitive empty states.** Explicit "0 results", not ambiguous empty
  output — kills the retry-on-ambiguity loop. Good for both readers.
- **Structured errors and exit codes.** Idempotent mutations, a consistent
  error envelope, and fail-loud on unknown flags. "No interactive prompts"
  means *suppressible* (non-TTY or `--yes`), not *absent* — do not drop a
  destructive-op confirmation a human relies on; suppress it when the
  caller is an agent. We already lean on exit-code verbs: `agentctl others`
  answers by exit code (0 alone / nonzero peers), likewise `alone`,
  `tending`.
- **Consistent, concise help.** Per-subcommand reference an agent can pull
  on demand. We already carry the mechanics — `AGENTS.md § Agent-facing CLI
  help`: no terminal-width hard-wrapping (human-wrapped via explicit
  opt-in), reuse the shared parser/formatter, keep option names greppable
  between logs and `--help`.

## Ambient context (#7) — organic, not designed up front

AXI's ambient-context principle (install opt-in session integrations, then
offer an on-demand skill) is the one that arrives by discovery rather than
by design, and we already do it implicitly: tools here read ambient
project-context paths without being told — `research/ROOT.md`, run metadata
under `.agentctl/`, the active-session files, the paths `RESEARCH.md` /
`RUNS.md` establish. That is ambient context in practice; it will keep
accreting as the need occurs to us, not as a big up-front integration.

**Ship worked examples.** AXI ships reference CLIs named by an `-axi`
suffix — `gh-axi`, `chrome-devtools-axi`, `lavish-axi` — each demonstrating
the principles against a real service. Our ACLI scripts should carry `-acli`
worked examples the same way; a principle with a runnable example beside it
is the ambient documentation an agent actually uses.

## The `acli` module

Compliance-by-calling: the package makes the principles above executable
defaults instead of prose. It lives beside `agentctl.py` (importable as
`acli` via the code-root PYTHONPATH agentctl already sets). Surface, in
small pure-function modules — a library, not a framework:

- `acli.session` — `is_agent_session()` and `resolve_format(args)`: the one
  place the detection disjunction lives, so a new harness marker is a
  one-line edit, not a sweep across every script.
- `acli.emit` — `write_jsonl()`, `write_pretty()`, `write_toon_table()`,
  and the writer selection keyed off `resolve_format`.
- `acli.errors` — the structured error envelope, standard exit codes, and a
  `die()` that fails loud.
- `acli.args` — an argparse factory pre-wiring the standard flags
  (`--format`, `--full`, `--pretty`, `--toon`) and the agent-friendly help
  conventions.

Distinct from the `agentctl` cooperative-declaration helpers
(`declare_input` / `declare_output`, a provenance protocol) — different
concern, different namespace.

## Design decisions

- **Agent-friendly default, human upgrade gated** (vs. agent output behind
  a flag): forgetting a flag must never yield hostile output; only the
  human upgrade can be conditional, because its fallback (compact) is
  harmless to an agent. Accepts that a mis-detected agent occasionally gets
  pretty JSON — a token waste, not a break, and overridable.
- **Disjunction + isatty over a single env var** (vs. keying on
  `AGENTCTL_SESSION_ID` alone): any one marker is sometimes absent; `isatty`
  carries most of the load and the env markers cover the PTY residual.
  Accepts that detection is heuristic, made safe by the two-sided override.
- **Pretty JSON, not a table, as the human fallback** (vs. rendered
  tables): degrades safely under mis-detection. Accepts a less pretty human
  experience unless detection confidence is high.
- **TOON opt-in and static per subcommand** (vs. default, or dynamic on row
  count): keeps the base format friendly and the consumer's parser fixed;
  the caller holds the knowledge of when TOON pays. Accepts the occasional
  short TOON payload.
- **Own our TOON encoder, flat-table subset only** (vs. a dependency or the
  full spec): matches the dependency-free ethos and self-enforces the
  large-uniform-table scope by raising on anything else.
- **Aggregates as named verbs, not default fields** (vs. bundling summaries
  into every output): reconciles round-trip elimination with minimal
  schemas — you opt into the aggregate when you want it.
