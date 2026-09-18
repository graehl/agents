# acli — evidence ledger

Companion to `topics/acli.md`, `topics/acli-spec.md`, and
`topics/acli-implementer.md`; conventions in `topics/evidence-ledger.md`.
Append-only.

## 2026-09-18 design decisions relocated from the pre-split topic

The 2026-09-07 rewrite that split `acli.md` into the user guide, the v1
specification, and the implementer guide (commit b4c1529) dropped the
whole `## Design decisions` section and three rationale sections without
relocating them. `design-thinking.md` § Weigh alternatives makes the
recorded decision the only channel that carries distant effects to a later
reader, so they are restored here verbatim from the pre-split text. Each
bullet is `**<decision>** (vs. <rejected alternative>): <rationale>`; all
were re-checked against the spec at HEAD and still hold.

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
- **Completion by invoking the tool, registry-gated** (vs. per-shell
  completion scripts): `--acli-complete` reuses the tool's own parser and
  needs no bash/zsh/fish artifacts; the consumer-side allowlist carries the
  safety burden, because probing an unknown tool with an unknown flag can
  execute a lax tool's default action.
- **Capability line inside `--help`, not a dedicated manifest flag**
  (vs. an `--acli` JSON manifest): one invocation serves humans,
  agents, and consumer registration, and a second probe flag would be
  one more thing a lax tool could misparse into its default action.
  Accepts that machine consumers grep one anchored line out of human
  help text.
- **Any emitted line suppresses the consumer's path fallback** (vs. an
  explicit no-files directive field): a lone `hint` row is the natural
  "answered; paths are noise here" signal, and a tool that wants path
  completion just stays silent for that slot. Accepts that one slot
  cannot both hint and request path fallback.
- **Per-candidate help from completers; slot guidance as one `hint`
  row** (vs. inheriting the argparse action help onto every value):
  inheritance repeated a whole syntax paragraph on every candidate in
  practice (almanac filters). Accepts bare value rows when a completer
  attaches nothing.
- **Tool-chosen candidate order, preserved end to end** (vs. central
  alphabetization): data order carries meaning (tier ranking, reading
  order — the almanac order contract). Accepts inconsistent ordering
  conventions across tools.
- **Redundant `--json` is accepted** (vs. requiring callers to discover that
  compact JSONL is already the default): explicit serialization intent is a
  common agent-CLI convention, and accepting it costs one alias while avoiding
  a failed discovery round-trip.
- **REPL in the library behind a reserved flag, prompt_toolkit
  optional** (vs. a hard dependency or per-tool shells): every ACLI
  tool gets an interactive mode from the parser it already declares,
  and the dependency-free core survives; readline mode plus an install
  banner covers absence. Accepts two code paths in `acli.shell`.
- **Topic named `acli`, matching the printed token** (vs. keeping
  `agent-cli.md`): the header a reader meets in a terminal or help text
  must locate the spec, so the topic basename equals the token; `agent-cli`
  survives as a glossary alternate for stranded references. Accepts a
  one-time rename sweep.
- **Stderr banner on every launch, library-emitted** (vs. banner only on
  errors/deferrals, or per-tool emission): first contact is when the
  activation prevents contract re-derivation by retry, and a terminal
  user reads the `# ` line as meta at a glance; emitting from
  `parse_args` keeps it uniform and unforgeable by construction (it
  advertises the same registration the flags come from). Accepts one
  short stderr line per process, priced acceptable even on hot verbs;
  `--acli-quiet`/`ACLI_QUIET` is the relief valve.
- **`+` token class for beyond-baseline affordances** (vs. one flat
  token list): an invoker scanning the line needs to distinguish "Tab
  completion exists" (consumer wiring, ignorable) from "this tool has a
  two-phase confirm flow" (changes how you call it). Accepts that
  existing consumers of the flat list see a spelling change (`toon` →
  `+toon`).
- **Shared table emitter in the library** (vs. one `emit_table` per tool,
  added 2026-09-18): the definitive-empty-state record and the TOON column
  projection are the contract's rules, and three copies had to be edited in
  lockstep for `--text`; `acli.emit_table` owns them now.

## 2026-09-18 prior art and rationale relocated from the pre-split topic

**Prior art.** `acli` (alternate spellings `agent-cli`, ACLI) is our term for
the pattern the AXI project (Agent eXperience Interface,
`github.com/kunchenguid/axi`) names externally. The topic is named `acli` to
match the token every compliant tool prints, so the header met in a terminal
locates the doc. AXI ships reference CLIs named by an `-axi` suffix
(`gh-axi`, `chrome-devtools-axi`, `lavish-axi`), each demonstrating the
principles against a real service; a principle with a runnable example
beside it is the ambient documentation an agent actually uses, and our own
tools (`agentctl`, `almanac`, `related-work`) serve that role here.

**Naming acli tools in instructions.** When an instruction file tells an
agent to use an acli tool, tag the introducing mention with the term — "use
the acli `agentctl`" — adding salient `+` tokens when they matter: "the acli
(+confirm) `deploy-pages`". The tag is a two-token typed pointer routing an
unfamiliar reader through the glossary to the contract, and the same
vocabulary then cross-confirms across instructions, the stderr banner, and
`--help`. Later mentions use the bare name. For partial support, name the
package instead: "use `artifact:capture` with acli `commentary/1` support,"
followed by its exact invocation and help command. Do not call it a full
acli tool unless it honors the baseline.

**Kill round-trips without becoming a scripting language.** Round-trips
(each a full agent turn: inference + latency + context growth) are the real
cost lever — far bigger than serialization. Own the common multi-step paths
in the tool, two mechanisms in priority order:

- Named composite verbs (porcelain) for hot paths. This is where
  "pre-computed aggregates" belong — as opt-in verbs, not fields baked into
  every base verb's output, which would fight minimal default schemas.
  `git pull` (= `fetch` + `merge`) and `git status` (an aggregate over the
  index) are the model. Agents want mostly porcelain; primitives stay
  underneath.
- Closed-loop, pipeable I/O for the long tail. "Output of one = input of the
  next" only works without glue if each verb accepts on stdin the same
  compact format it emits. Most CLIs break this — emit JSON, accept only
  flags — forcing the agent to parse-and-re-serialize between steps. That
  reshape is the ad-hoc script we are avoiding, leaking in at the seams. A
  closed-loop format lets `A | B` run as one invocation.

Two failure modes bound the design: too few named combos and the agent
experiments with composition (an unspecified scripting language —
non-deterministic, token-costly, mistake-prone); too many and you get verb
sprawl with its own discovery cost. Name the empirically-hot paths; make
the rest pipeable. The round-trip win needs single-invocation composition
(a pipe or a named verb) — a sequence of separate calls is still N turns no
matter how obvious the defaults; obvious defaults buy lower mistake-rate,
not fewer turns.

**Ambient context — organic, not designed up front.** AXI's ambient-context
principle (install opt-in session integrations, then offer an on-demand
skill) is the one that arrives by discovery rather than by design, and we
already do it implicitly: tools here read ambient project-context paths
without being told — `research/ROOT.md`, run metadata under `.agentctl/`,
the active-session files, the paths `RESEARCH.md` / `RUNS.md` establish.
That is ambient context in practice; it will keep accreting as the need
occurs, not as a big up-front integration.
