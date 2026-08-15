# Helper scripts

> Repeatable agent operations get a named CLI helper with a tight
> spec — name, UI, post-conditions, 2-3 input/output examples — so
> any agent rebuilds the same tool from spec when missing and
> recognizes broken output without guesswork.

Topic: `helper-scripts`

## When to add a helper

A helper earns its weight when (a) the inline form has a chronic
fiddly failure mode (≥3 observed across sessions), (b) the operation
is mechanical enough that a script removes ambiguity, and (c) the
post-condition can be expressed as a test the script itself runs
(exit code). Commit-message linting clears the bar; one-off shell
pipelines do not.

## Where impls live

- **Canonical source**: `scripts/<name>` in this repo. Python
  3.10+ pure-stdlib unless a dependency is justified.
  Every helper ships with its initial tested impl — specs without a
  working impl are aspirational, not installable.
- **Runtime install**: `~/bin/<name>` per machine. Agent installs
  on first use (symlink to the canonical source, or copy if the env
  rejects symlinks). Assumption: a Python 3.10+ interpreter is on
  PATH.
- **Local fallback**: if the installed helper fails its own post-
  conditions on a known-good input in this env, replace
  `~/bin/<name>` with a fresh impl built to the same spec — keep
  the name and CLI identical so callers do not change.
- **Project-shaped helpers** (those that know repo-specific
  conventions): repo-local gitignored `scripts/agent/<name>` inside
  the consuming project. Agent rebuilds from spec on first use per
  clone.

## Rebuild trigger

If the named helper is missing on a system, or its output fails its
own post-condition checks against a known-good input, rebuild from
the spec entry below. The examples are the test suite — pass them
all or do not ship the rebuild. Do not invent a different UI.

## Spec entries

### commit-msg-lint

**CLI**: reads draft on stdin. If stdin is empty, reads the current
`HEAD` commit message via `git log -1 --format=%B`. On success
echoes the checked message verbatim to stdout, exits 0. On violation
lists issues on stderr (one per line, prefixed `commit-msg-lint:`),
exits 1. Empty input with no readable `HEAD` message exits 2.

**Post-conditions** (derived from `AGENTS.md` Commits section):
- subject ≤65 chars
- no literal `\n` in subject (multi-`-m` shell-quoting symptom)
- blank line between subject and body if body present
- body lines ≤71 cols, except where the longest single token on
  the line is itself >71 (unavoidable long-token carve-out for
  URLs, paths, identifiers)
- no `Co-Authored-By:` trailer

Not enforced (deliberately — these are visual/judgment rules the
linter would mis-fire on): bullet/indent preservation, narrative
quality, presence of `Topic:` trailers, `Known coverage gaps:`
section structure.

**Examples**:
1. Single-line subject `feat: do thing` → exit 0, echoed verbatim.
2. Subject containing literal `\n` (e.g. `feat: foo\nbody`) → exit
   1, `literal '\n' in subject`.
3. 70-char subject + valid body → exit 1,
   `subject 70 > 65 chars`.
4. Clean subject, blank line, body line of 85 cols of prose →
   exit 1, `line 3: 85 > 71 cols`.
5. Clean subject, blank line, body line containing a single
   90-char URL with no spaces → exit 0 (long-token carve-out).
6. No stdin in a Git checkout with `HEAD` → lints `HEAD` and echoes
   the commit message on success.

**Canonical source**: `scripts/commit-msg-lint` (in this repo).
**Install target**: `~/bin/commit-msg-lint` (symlink by default).

**Usage**:
```sh
git commit -F <(commit-msg-lint < draft.txt) && rm draft.txt
# or, fail fast before committing:
commit-msg-lint < draft.txt && git commit -F draft.txt
# or, check the current commit:
commit-msg-lint
```

### commit-msg-fmt

**CLI**: `commit-msg-fmt -m "subject" [-m "para" ...]`. Writes a
formatted commit message to stdout, exits 0. The first `-m` is the
subject and passes through unwrapped. Subsequent `-m` args are
wrapped to 71 cols. `-m` args are joined with single newlines —
**no blank lines are inserted automatically**, unlike `git commit
-m -m`. To insert a blank line (e.g. between subject and body),
pass `-m ''`. No `-m` args or empty subject exits 2.

**Post-conditions**:
- output line 1 (subject) equals first `-m` arg verbatim
- each body line ≤71 cols (except where a single token in the
  input is itself >71)
- blank lines in output come only from explicit `-m ''`
- output ends with exactly one trailing newline

**Scope limitation**: each `-m` is treated as one plain-prose
paragraph. Pre-formatted content (bullets, hanging indents, ASCII
diagrams, tables, code blocks) must not be passed through this
formatter — write those messages directly with `git commit -F`
instead. The formatter intentionally collapses internal whitespace
when wrapping.

**Examples**:
1. `commit-msg-fmt -m "feat: do thing"` → `feat: do thing` + newline.
2. `commit-msg-fmt -m "feat: do thing" -m "" -m "Body paragraph
   long enough to wrap across two lines at 71 cols of width."`
   → subject, blank line, body wrapped to ≤71 cols.
3. `commit-msg-fmt -m "feat: do thing" -m "" -m "Para 1." -m "" -m
   "Para 2."` → subject, blank, `Para 1.`, blank, `Para 2.`.
4. `commit-msg-fmt -m "feat: do thing" -m "Body, no blank above."`
   → subject directly followed by body line; commit-msg-lint will
   flag the missing blank.
5. `commit-msg-fmt` (no args) → exit 2, `no -m args`.

**Canonical source**: `scripts/commit-msg-fmt` (in this repo).
**Install target**: `~/bin/commit-msg-fmt` (symlink by default).

**Composes with commit-msg-lint**:
```sh
commit-msg-fmt -m "feat: do thing" -m '' -m "Body paragraph." \
  | commit-msg-lint && git commit -F -
```

### at-queue

Sole writer of the clone-local activation store described in
`topics/at-scheduling.md`; provider launch and object-level scheduling judgment
remain outside it. Every
mutation goes through this helper — the store is machine-owned, and callers
must not hand-edit it.

**CLI** (all verbs take `--root <project>`; all emit one JSON line):
- `activate --job <name> --run-after <RFC3339>` — schedule a prompt source and
  record the hash of the bytes being approved. Also the re-approval action
  after a source changes. Replacing a live claim also requires its
  `--occurrence <receipt>`.
- `pause --job <name>` / `resume --job <name>` — stop or restart scheduling
  without discarding the schedule.
- `claim --session <canonical-id> --harness <name> --owner-pid <pid>` —
  atomically claim at most one due job. `--owner-pid` is required and must
  outlive the claim: its process-start identity is the exclusion proof. The
  result includes an opaque `occurrence_id` receipt.
- `done --job <name> --occurrence <receipt> (--run-after <RFC3339> | --park)
  [--status <s>]` — clear only that run occurrence and stamp the outcome.
- `list` — report every job's state and `blocked_by` reason.

**Exit codes**: 0 success; 3 `claim` found nothing claimable; 4 refused, with a
JSON `error` naming what to fix; 2 argparse usage.

**Post-conditions**:
- An absent `<project>/at/` is never created, and a claim that takes nothing
  writes no activation file.
- A tracked `at-activation.json` is refused by every verb, because clone-local
  activation is what stops a `git pull` from scheduling agent work.
- Loading a file at-queue did not write (non-canonical formatting) succeeds but
  emits a `warnings` entry.
- Prompt sources are never rewritten; `activate` and `done` touch only
  activation.
- A same-host claim whose recorded process is gone is re-claimable with no
  heartbeat, lock-breaking, or adjudication. Foreign-host liveness stays
  unknown and blocked.
- A source whose bytes differ from the approved hash is skipped, not run.
- `done` retains the claimed hash rather than approving source edits made
  during the run; stale occurrence receipts cannot alter a newer claim.

**Examples**:
1. No activation → `claim` exits 3 with `{"status":"none","skipped":{}}`.
2. Due `at/review.md` → exit 0 with `job`, `occurrence_id`, `source`,
   `prompt_sha256`, `run_after`; a concurrent `claim` exits 3 with
   `skipped:{"review":"already running"}`.
3. Source edited after activation → `claim` exits 3 with
   `"prompt changed since activation; re-activate to approve"`.

**Canonical source**: `scripts/at-queue` (in this repo). No install is
required; startup uses this path only when it exists and is executable.

### session-turn

Sends one user turn to a durable provider session and streams one compact JSON
record per lifecycle event. This is a generic cross-session transport; it does
not select a research advisor or impose an advisor protocol.

**CLI**:

- `session-turn <claude|codex> <provider-session-id> [options]` sends and
  normally waits through terminal;
- `session-turn send <claude|codex> <provider-session-id> [options]` detaches
  after durable host acceptance;
- `session-turn await <submission-id> [--after-cursor <n>] [--timeout
  <seconds>]` replays and follows that accepted submission; and
- `session-turn receipt <submission-id>` performs a point-in-time receipt
  lookup.

Turn options are `[--ya-session-id <id>] [--submission-id <id>] [--cwd
<path>] [--model <name>] [--effort <level>] [--timeout <seconds>]`; the
combined form additionally accepts `[--wait-timeout <seconds>]`. The turn body
is stdin. Turn `--timeout` defaults to 30 minutes, accepts 1 second through 2
hours, and bounds provider work; a native provider CLI owns its own duration.
Combined `--wait-timeout` begins after host acceptance, defaults to zero (wait
through terminal), and bounds only observation. Await `--timeout` has the same
observer meaning and zero means unbounded. `--cwd`, `--model`, and `--effort`
apply when protocol 3 resumes an absent worker and when native resume is
required. An incumbent provider-host worker retains its owning project and
configuration. stdout is compact JSONL and flushes after every record;
warnings, continuation commands, and native provider diagnostics go to stderr.

**Transport selection**:

1. On Linux, resolve YA's stable same-user provider-host descriptor, require
   private owner-only descriptor/token/socket paths, and negotiate descriptor
   version 1 plus host protocol 2 or 3 with the `session-turn` feature.
2. Submit one `sessionTurn` request to a matching incumbent through the
   host-owned worker queue. Under protocol 3 that same request carries a
   `launch` option: if no incumbent exists, the host atomically reserves the
   target, resumes an auxiliary worker, verifies its durable provider id, and
   only then offers the message for acceptance. A supplied YA session id is an
   additional ownership cross-check. Hono may claim the reserved worker but is
   not in this transaction's delivery path. When the host advertises
   `recent-runtime-recovery` and no model/effort override was supplied, the
   request also prefers an exact recipe consumed from the predecessor's recent
   orderly shutdown; its caller-generated `launch` remains the atomic fallback
   when no eligible recipe exists.
3. If protocol 2 has no incumbent, or no compatible usable host accepts the
   turn, invoke the harness's native resume command. Never use YA HTTP. The
   stderr warning names the rejected host path, target, reason, and native
   fallback. `forkRisk:"concurrent-native-resume"` records that another writer
   can produce a different-parent branch.

Detached `send` and finite combined observation require a host advertising
`session-turn-await`; they never start a helper-owned native process that would
be orphaned on detach. If the host is absent, incompatible, or rejects before
acceptance, they emit the blocking cause and exit 11. The default unbounded
combined form retains native fallback.

The stable wrapper records are `transport`, `accepted`, `providerEvent`,
`interruptRequested`, `waitExpired`, and terminal `terminal` or `error`. Turn
records name the selected `transport`, `harness`, durable `providerSessionId`,
and `submissionId`; await records necessarily identify transport and
submission. Host records include a cursor equal to the retained record count
through that record. Host-normalized provider events retain their `message`;
native JSONL records live under `providerRecord`. Terminal records carry the
host receipt or a native `native-record:<count>` watermark. `transport`
records report `resumeIfAbsent` and `resumeRecentRuntime` where applicable. A
caller has not received the result until it reads a terminal `terminal` or
`error` record. A shell or tool yielding partial JSONL while the helper remains
running is not completion.

One send creates exactly one logical provider turn with one terminal boundary,
although any number of provider events, tool cycles, status records, or
compaction boundaries may precede it. `await` addresses that submission, never
all activity on a session. Omitting `--after-cursor` replays from record zero;
supplying the last observed cursor drains only later records. After the host
has pruned the in-memory stream or restarted, await can return its durable
terminal receipt but cannot recreate discarded provider events.

**Exit codes**: 0 completed; 10 provider failed or the submitted turn was
interrupted; 11 transport failed before acceptance; 12 delivery is uncertain
after acceptance; 13 the observer deadline expired while the accepted turn
remains active or available for later observation; 2 argparse usage. Exit 13
emits a nonterminal `waitExpired` record with the latest cursor and prints the
exact `session-turn await ... --after-cursor ...` continuation command to
stderr. It does not interrupt, cancel, or resubmit the provider turn. The
session can remain busy until that already accepted turn reaches terminal.

**Post-conditions**:

- Host dispatch uses only the documented host control socket and
  `sessionTurn`; it never attaches as a Hono controller, opens a worker socket,
  or writes provider-child stdin.
- Protocol 3 incumbent selection, absent-worker resume, and message offer are
  one receipt-keyed `sessionTurn` transaction. The helper does not first
  provoke an unavailable result and then issue a separate launch request.
- One client-generated submission id follows the turn across host receipt
  lookup and native fallback. A host error explicitly marked unaccepted, or a
  post-disconnect `sessionTurnStatus` result proving no receipt, permits native
  fallback. Any accepted or uncheckable delivery blocks fallback and exits 12.
- `send` stays connected through `accepted`, then closes only its listener.
  `await` uses `awaitSessionTurn` with an explicit or zero cursor and follows
  only that receipt-keyed submission. Neither observer disconnect nor exit 13
  cancels host-owned work.
- Ctrl-C requests `interruptSessionTurn` for a hosted submission. On native
  fallback it signals only the helper-created process group, with bounded
  escalation; neither path kills an unrelated incumbent session.
- Native fallback launches with the supplied target YA session, or otherwise
  the target provider session, as `AGENTCTL_SESSION_ID`; it uses the target
  harness as `YEP_AGENT_HARNESS`. It removes caller-owned provider ids, YA's
  Bash identity bridge and wake capability, initial model/effort markers, and
  agentctl launch-depth state; unrelated configuration remains inherited.
- Native acceptance requires both a successful write/flush of the complete
  turn body and a harness-recognized provider JSON lifecycle record. Non-JSON
  warnings and unknown JSON records remain provider events but cannot prove
  acceptance. A process that exits without both conditions is a transport
  failure before acceptance; stderr states that an active writer or invalid
  resume handle may be the blocking cause.
- Provider output is consumed and emitted line by line. A compaction event is
  an ordinary provider event and does not replace terminal receipt tracking.
- The wrapper accepts at most 900 KiB for one turn and never loads or replays a
  whole provider conversation.

**Examples**:

1. `session-turn claude <provider-id> < review.md` with a compatible incumbent
   emits `transport:provider-host`, `accepted`, provider events, then a terminal
   receipt without starting a second Claude resume.
2. With protocol 3 and no incumbent, the same command resumes an auxiliary
   worker inside that `sessionTurn` request, reports `resumeIfAbsent:true`, and
   reaches acceptance without Hono. Explicit cwd/model/effort values become
   launch and reattachment facts; the host reaps an unclaimed auxiliary worker
   after its idle deadline.
3. The same command with no descriptor emits the native-resume fork-risk
   warning, wraps Claude's stream JSON, and exits according to the native
   process result. Native Claude can form a different-parent branch under
   concurrent resume; native Codex refuses an active writer. Without explicit
   overrides, either native CLI may use its current model/effort defaults.
4. A socket disconnect after `accepted` never starts native resume. The helper
   checks `sessionTurnStatus`; if no terminal receipt is reachable it emits
   `uncertain-after-acceptance`, includes the exact `session-turn receipt`
   command, and exits 12.
5. `session-turn send codex <provider-id> --submission-id S` emits acceptance
   and returns. `session-turn await S --after-cursor 1 --timeout 30` drains
   later records. If that observer deadline expires, exit 13 and stderr provide
   the next cursor-bearing await command while the original turn continues.
6. After an orderly host restart, a feature-capable combined/send request with
   no explicit model/effort asks the host to prefer the predecessor's exact
   launch recipe. The same request carries its ordinary launch recipe as an
   atomic fallback; no failed lookup or Hono round trip comes first.

**Canonical source**: `scripts/session-turn` (in this repo).
**Install target**: `~/bin/session-turn` (symlink by default).

### install-agents

Installs this checkout's global instructions and skills at the current
user-level locations recognized by supported agent harnesses. It preserves
unrelated skills and records enough prior filesystem state for a guarded
uninstall.

**CLI**: `install-agents <install|status|uninstall> [--home <dir>]
[--repo <dir>] [--harness <name>[,<name>...]] [--json]`.
`--harness` is repeatable and defaults to all of `codex`, `claude`, `pi`,
`opencode`, `grok`, and `copilot`; documented aliases normalize to those
names. `--home` deliberately accepts a synthetic directory for rehearsal.
`status` exits 3 when an instruction or skill target is missing or drifted;
usage and safe refusals exit 2.

**Post-conditions**:
- Harness instruction paths resolve to `<repo>/AGENTS.global.md` through
  ordinary symlinks. The installer never creates or edits `~/AGENTS.md` and
  offers no hardlink mode.
- An absent skill root becomes a link to `<repo>/skills`; an existing directory
  retains unrelated entries and receives one link per repository skill. A root
  already resolving to the source is unchanged.
- Before mutation, `~/.local/state/agents-install/active.json` and its named
  backup directory record every target's prior kind, content or link target,
  mode, and inode/link metadata. `uninstall` restores mutated paths in reverse
  order and retains the backup. Before its first mutation, uninstall validates
  the kind and digest or link target of every restore object.
- Install, status, and uninstall refuse a target whose symlinked parent escapes
  the selected home. Uninstall also refuses to overwrite post-install drift. A
  repeated install for the same checkout and harness selection is a no-op when
  complete and extends the manifest when new repository skills need per-skill
  links.

**Examples**:
1. `install-agents status` reports every supported harness without writing.
2. `install-agents install --home "$test_home"` followed by matching `status`
   and `uninstall` rehearses a complete round trip outside the real profile.
3. `install-agents install --harness codex,grok` installs only those harnesses;
   changing that selection requires uninstalling the active install first.

**Canonical source**: `scripts/install-agents` plus the
`scripts/install_agents/` Python package (in this repo). Run it from the
checkout; it has no separate `~/bin` install target.

### vendor-skill

Copies a subdirectory of a remote git repo into this tree, pinned to an
exact upstream commit, and writes/refreshes a `VENDORED.md` provenance
record. Implements the convention in `topics/vendoring.md`.

**CLI**:
- `vendor-skill <repo> <subpath> [dest]` — sparse-clone `<repo>` at HEAD,
  copy `<subpath>` into `dest` (default `./<basename(subpath)>`), write
  `dest/VENDORED.md`. `<repo>` accepts a full URL, `git@host:org/repo`,
  `host/org/repo`, or `org/repo` (defaulting host `github.com`). Exit 0 on
  success.
- `vendor-skill --check <dest>` — re-read `dest/VENDORED.md`, sparse-clone
  upstream at HEAD, diff the vendored files against current upstream.
  Exit 0 = in sync (prints `up to date: <sha>`), exit 3 = drift (prints a
  unified diff). Modifies nothing.
- Usage/parse errors and a missing/incomplete `VENDORED.md` exit 2.

**Post-conditions**:
- After a vendor: `dest` contains the upstream subpath files (exec bits
  preserved); `dest/VENDORED.md` exists with an Upstream **Commit** equal
  to the clone's `git rev-parse HEAD` (full 40-char SHA), a per-file
  sha256 table matching `sha256sum` of the copied files, and a License
  section describing detected upstream license files or their absence.
- A re-vendor over an existing `dest` preserves the hand-written body of
  the `## Local changes` section verbatim; all other sections regenerate.
- `--check` never writes; its temp clone is removed regardless of outcome.

**Examples**:
1. `cd skills && vendor-skill xl0/agent-files skills/librarian` → vendors
   into `skills/librarian/`, prints `vendored …@ <sha12> -> …` and (since
   that repo has no LICENSE) a no-license warning.
2. `vendor-skill --check skills/librarian` with upstream unchanged → exit
   0, `up to date: <sha12>`.
3. Edit a vendored file locally, then `vendor-skill --check skills/librarian`
   → exit 3 and a unified diff of the local edit.
4. Put a note under `## Local changes`, re-vendor the same subpath → exit
   0, files re-pinned to upstream, the note still present.

**Canonical source**: `scripts/vendor-skill` (in this repo).
**Install target**: `~/bin/vendor-skill` (symlink by default).

### queued-anchor

Grounds a queued user message's composition time against the provider
session transcript, so its referents resolve against what the sender
had actually seen rather than the current conversation tail
(`AGENTS.global.md` § Queued-send time separators). Models essentially never
perform this wall-clock-to-turn mapping unaided; the transcript's
per-message timestamps make it mechanical.

**CLI**: `queued-anchor <seconds-ago> [--session <id>]
[--project-dir <dir>] [--transcript <jsonl>]`. `<seconds-ago>` is N
from the leading `--- (Ns ago)` separator. Transcript discovery:
`--transcript` wins; else the session id (`--session`, defaulting to
`$AGENTCTL_SESSION_ID` then `$CLAUDE_CODE_SESSION_ID`) names
`~/.claude/projects/<cwd-dashed>/<id>.jsonl`; else the newest
transcript in that directory. Claude Code jsonl only (v1); other
harnesses exit 3 and the caller falls back to judgment. On success
prints one JSON line: `composed_at`; `anchor` (timestamp plus
≤160-char `text_head` of the last visible assistant text at
composition, null when composition predates all assistant output);
`anchor_turn_continued` (the anchor's turn kept producing text after
composition); `activity_at_composition` (latest thinking or tool_use
event at composition when it postdates the text anchor — a sender
watching the live stream may be reacting to mid-turn activity, not
completed text; null otherwise); `unseen_turn_heads` (ascending;
first visible text of each assistant turn the sender had not seen).
Exit 0 success, 2 usage, 3 no transcript or no timestamped user
events (JSON `error` line on stderr).

**Post-conditions**:
- `composed_at` equals the newest user event's timestamp minus
  `<seconds-ago>`; sidechain (subagent) events are ignored.
- `anchor` is the latest visible assistant text at or before
  `composed_at`; `unseen_turn_heads` holds exactly the turn-opening
  texts after it, in order.
- `anchor_turn_continued` considers only later text in the anchor's assistant
  turn and stops at the next user event. `activity_at_composition` considers
  only activity in the assistant turn live at composition; an earlier turn's
  trailing tool call cannot become current merely because no newer text exists.
- Read-only: never writes anything.

**Examples** (fixture: user@T+0s, assistant "Alpha result is
ready"@T+10s, assistant "Alpha continued detail"@T+20s (same turn),
user@T+100s, assistant "Beta answer"@T+110s, assistant tool_use
`Bash {"command":"git push"}`@T+120s (turn continues), user@T+200s):
1. `queued-anchor 150 --transcript fx.jsonl` → composed T+50; anchor
   "Alpha continued detail"; `anchor_turn_continued` false; unseen
   heads `["Beta answer"]`.
2. `queued-anchor 185 --transcript fx.jsonl` → composed T+15; anchor
   "Alpha result is ready"; `anchor_turn_continued` true (the T+20
   event follows within the turn); unseen heads `["Beta answer"]`.
3. `queued-anchor 300 --transcript fx.jsonl` → anchor null; unseen
   heads `["Alpha result is ready", "Beta answer"]`.
4. Nonexistent `--transcript` → exit 3,
   `{"error": "no transcript found"}` on stderr.
5. `queued-anchor 75 --transcript fx.jsonl` → composed T+125; anchor
   "Beta answer"; `activity_at_composition` kind `tool_use`, head
   `Bash {"command": "git push"}` — the sender was likely reacting
   to that in-flight command; unseen heads `[]`.

**Canonical source**: `scripts/queued-anchor` (in this repo).
**Install target**: `~/bin/queued-anchor` (symlink by default).

### perf-sweep

Pre-run / end-of-session sweep for the perf measurement discipline in
`topics/perf.md`: makes leftover measurement processes visible before
they degrade a shared host, and reaps them on request. Report-first
because debris is a finding — possibly a lifecycle defect in the
measured system — so even a fully reaped sweep exits nonzero.

**CLI**: `perf-sweep <marker> [--kill] [--kill-group] [--grace S]
[--no-environ]`. `<marker>` is a literal run identifier (≥5 chars) matched
as a substring against
every process's `/proc/<pid>/cmdline` and, unless `--no-environ`, its
`environ` — env matching finds measured-system children that
inherited the marker env var but carry no argv marker. Prints
greppable `SURVIVOR:` lines (`pid= pgid= age= src=argv|env cmd=`),
`GROUPMATE:` lines for unmatched processes sharing a survivor's
process group (the usual tell that the measured system, not the
driver, spawned them), then with `--kill` a TERM → grace → KILL pass
(`--kill-group` extends it to each survivor's whole group) with
`KILLED:`/`UNKILLABLE:` lines. A `PROTECTED_GROUP:` line means a
survivor shares a process group with the sweep or one of its ancestors;
that group is not signaled, and only its marker-matched processes are
reaped. A final `SWEEP:` summary line follows.
Exit 0 = nothing matched; 10 = debris found (even if fully reaped);
11 = debris remains after kill; 2 = usage (short marker, negative grace,
or `--kill-group` without `--kill`).

**Post-conditions**:
- Never signals anything in report-only mode (the default).
- Never signals a process unless its cmdline/environ matches the
  marker or (under `--kill-group`) it shares a marked survivor's
  process group; never signals itself, its ancestors, or pid/pgid
  ≤ 1.
- Revalidates each target's captured process start time and process group
  immediately before every TERM or KILL. A group signal additionally requires
  a still-matching original survivor in that group; a reused PID or ownerless
  group is not signaled.
- Never group-signals a process group containing itself or an ancestor;
  marker-matched processes in such a group still receive the requested
  per-process signals.
- A post-kill rescan, not signal bookkeeping, decides exit 10 vs 11.
- Exit 0 ⇔ no `SURVIVOR:` line printed.

**Examples**:
1. `perf-sweep no-such-marker-xyzzy` → `CLEAN: …`, exit 0.
2. `setsid python3 -c 'import time; time.sleep(300)' --run-id M &`
   then `perf-sweep M` → one `SURVIVOR: … src=argv …`, exit 10;
   `perf-sweep M --kill` adds `KILLED:`, exit 10; rerun → exit 0.
3. `PERF_RUN_ID=M setsid python3 -c '…sleep…' &` (no argv marker) →
   `perf-sweep M` finds it as `src=env`; `perf-sweep M --no-environ`
   exits 0.
4. `setsid bash -c 'sleep 300 & exec python3 …sleep… --run-id M' &`
   → `perf-sweep M` prints the python as `SURVIVOR:` and the
   unmarked `sleep 300` as `GROUPMATE:`; `--kill --kill-group`
   reaps both.

**Canonical source**: `scripts/perf-sweep` (in this repo).
**Install target**: `~/bin/perf-sweep` (symlink by default).
