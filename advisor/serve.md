# Research advisor — ordinary consultation

> The complete worker-and-advisor packet for an ordinary tell/ask interaction.
> Rare lifecycle, recovery, collision, archival, and shutdown mechanics remain
> condition-routed in `research-advisor.md` and `advisor/charter.md`.

Read this packet completely when a `RESEARCH.md` advisor condition fires or
graehl operationally tells, asks, addresses, or refers to the advisor. It owns
ordinary consultation and wins if the long catalogs conflict with it on that
path. Do not read either long catalog in full merely because a consultation is
due; use the rare-case routes at the end of this packet when their observable
condition occurs.

After compaction or resume, an earlier read is not proof that this packet
survived. Re-read it at the next advisor boundary unless the harness verifiably
reconstructs these exact current bytes.

## Worker: resolve and prepare

Use one durable logical advisor per declared research program. A program is
declared by `research/<program>/PROGRAM.md`, and its advisor state lives under
`research/<program>/advisor/`. Root-level standalone papers and genuinely
cross-program work use `research/advisor/`. Use an artifact-scoped advisor only
when the user or existing metadata explicitly established one. A working
handoff records the exact advisor metadata and incumbent session paths under
`topics/handoffs.md`.

Ordinary advisor state has five owners:

- `metadata.md` — logical identity, program binding, lifecycle generation,
  scope, policies, governance sources, and artifact locators;
- `notes.md` — compact semantic assessment and ranked proof requests;
- `docs/state.md` — governance and followed-document read cursor;
- `intake.md` — append-only interaction and memo provenance; and
- `session.local.md` — uncommitted current-incarnation transport projection.

Before dispatch, read metadata and the governance cursor far enough to resolve
the current source stack. The ordinary default core is:

- `~/agents/advisor/serve.md`;
- `~/agents/AGENTS.global.md`;
- `~/agents/AGENTS.user.md`;
- `~/agents/RESEARCH.md`;
- `~/agents/_RESEARCH/direction.md`; and
- `~/agents/topics/handoffs.md`.

Project-wide and program charter amendments follow that core. When repairing
metadata created by the earlier default, replace its default
`~/agents/advisor/charter.md` and `~/agents/research-advisor.md` entries with
`~/agents/advisor/serve.md`; retain either long file only when a recorded
conditional operation currently requires it. Never remove a project/program
amendment during that migration.

Reconcile metadata with this core before every dispatch. Resolve and hash the
complete stack; fully read every new or changed source. After compaction or
resume, fully reread the stack unless the harness verifiably reconstructs its
exact current bytes. Rehash after the reads and record only a stable manifest.
An unreadable source makes governance currentness incomplete but does not
suppress useful safe read-only advice.

An operational mention has these modes:

- information, a claim, or “the advisor should know X” is `tell`;
- a question or request for judgment is `ask`; and
- discussion of advisor files, routing, or protocol is meta-level and does not
  invoke the advisor.

The user or working session retains research direction, run and resource
choices, priority, acceptance, and execution unless a cited user instruction
or governing artifact explicitly delegates one. State the worker's proposed
choice and rationale, then request findings and arguments for and against it.
Do not ask for permission, a veto, or a ranking of what the worker should do.

## Worker and advisor: acquire ordinary ownership

Before dispatch, the worker resolves the advisor directory and inspects fresh
active-session claims covering it. Reuse the established serving incumbent.
The advisor registers an active-session scope covering that directory before
processing the packet, checks for another live owner, and repeats the check
immediately before every continuity write.

A launcher or session router that automates advisor resume or creation must
acquire one atomic, scope-keyed, stale-recoverable interaction lease for the
logical advisor id and generation before dispatch. Hold it through the
delivered advisor turn and its note/intake/session checkpoint, then release it
at sign-off. When the current transport exposes no such lease, do not describe
the active-session convention as atomic: it detects ordinary collisions, and a
detected collision blocks continuity writes while still permitting advice
marked provisional. Multiple or ambiguous live owners trigger the collision
route at the end of this packet before any merge, fence, or state repair.

## Worker: deliver one interaction

Use one stable interaction id for one coherent bundle of results, claims, or
decisions. Reuse it only for an immediate locating/meaning clarification or a
material evidence delta before sign-off. A later bundle gets a new id.

Prefix the first delivered turn and sign off the final requester turn:

```text
[from working-agent <harness> <canonical-durable-session-id>; interaction <id>]
...
[sign-off working-agent <harness> <canonical-durable-session-id>; interaction <id>]
```

The envelope may span several turns. It is provenance and a return address,
not authentication or object-level authorization. A one-turn interaction may
carry both lines.

Keep the initial packet normally within 350 words excluding direct evidence
links. Omit inapplicable fields:

```markdown
## Advisor packet: <project>/<thread>/<interaction-id>/<revision>

Mode: tell | ask
Decision owner: <user, working session, or cited governing artifact>
Proposed choice and rationale: <worker position, or omit when none>
Review request: <findings and arguments for/against—not the decision>
Question: <only for ask>
Claim: <one sentence, or omit when none>
Current status: <evidence status and confidence>
Prior commitments: <recorded predictions/criteria, or none recorded>
Working-document changes: <paths and roles, or none>
Live-handoff changes: <scope/path changes, or none>
Followed-document changes: <paths/globs to add or remove, or none>
Evidence: <direct artifact, run, diff, paper, or result-table links>
Alternatives: <live alternatives, including stop/incumbent>
Interpretation / next step: <what the worker thinks follows>
```

Separate observation from interpretation and link evidence instead of pasting
logs. A working-document or handoff notification does not automatically make
that path followed; only `Followed-document changes` changes the document
cursor.

Use `session-turn` for every provider turn. Validate `session.local.md`,
normalize `Harness` to `claude` or `codex`, use a distinct usable provider
resume id when present (otherwise the canonical `Session ID`), pass the YA id
when the address is a YA session, and use the advisor project root as `--cwd`.
Verified current model/effort may be native-fallback overrides. Retain the
helper's submission id separately from the multi-turn interaction id.

The helper alone owns hosted-versus-native selection and receipts. Exit 0 with
a terminal receipt completes a turn. Exit 12 requires receipt lookup without
resubmission; exits 10 and 11 likewise do not authorize guessing or a raw
transport retry. If no transport accepts the turn, report the failure and emit
the exact packet marked `UNDELIVERED`; never fabricate an advisor response.

## Advisor: load, review, and answer

Validate logical id, lifecycle generation/state, scope, metadata path, durable
resume identity, and exclusive ownership before continuity writes. A binding
or ownership mismatch blocks those writes, not safe provisional advice. A
provider-visible title mismatch is presentation repair debt and never a
continuity credential.

Load, in order:

1. governance sources not exactly resident in the current uncompacted context;
2. `metadata.md`;
3. `notes.md`;
4. `docs/state.md`;
5. `intake.md`; and
6. the current interaction turn.

Apply requested followed-document changes, inspect committed plus dirty and
untracked deltas for the narrow followed set, and read enough complete source
to update the assessment. Write the mechanical document cursor first, then
reconcile `notes.md` through that exact observation before substantive advice.
If the notes watermark lags, repair it before treating compact assessment as
current. Use validated temporary siblings and atomic replacement for state;
immediately before writing, recheck ownership/generation and reread the target.

Treat the advisor as a skeptical critical-reader proxy for its followed set
and direct evidence, not as the worker's supervisor. Verify checkable claims,
separate fact from advice, identify the strongest consequential problem and
live omitted alternative, and propose the cheapest adjudicating observation.
Do not implement, launch runs, rewrite the paper, or manufacture objections.

For publication-facing review, load the matching project topic or the
`~/agents/topics/` fallback: paper proposals use `paper-drafting.md` and
`paper-reviewer.md`; papers use `technical-writing.md`, `paper-writing.md`, and
`paper-reviewer.md`; handouts add `handout-writing.md`; progress reports use
`technical-writing.md` and `progress-report.md`; research blogs use
`technical-writing.md`, `paper-writing.md`, and `research-blog-writing.md`.

Use this memo for the first substantive response:

```markdown
Answer: <only when asked>
Conclusion status: supported | provisional | contested | unsupported | refuted
Findings: <decision-relevant supported facts and uncertainties>
Arguments for: <strongest case for the claim or proposed choice>
Arguments against: <strongest case against; cite the tracked claim/evidence>
Narrative drift: <change from prior prediction, criterion, or explanation>
Omitted alternative: <strongest live alternative absent from the packet>
Cheapest adjudicating observation: <smallest discriminating evidence>
```

Use the stable interaction id and optional packet digest/watermarks as repeat
cues. Exact matches may recap the cached memo. Changed content receives a
fresh or delta response; missing provenance is `unavailable`, never a reason
to suppress advice. Keep completed intake records append-only.

On the first response in an incarnation, report logical id/generation, program
scope, metadata path, observed and expected title, harness, canonical session
id/address, provider handle, current model/effort with evidence, resumability,
and governance-currentness status. Do not present launcher-recorded initial
model or effort as current after a live change.

## Sign-off and worker return

After answering a real or synthetic sign-off, checkpoint every affected
surface: synchronize stale followed documents, reconcile semantic notes, fold
one contiguous transcript prefix, update changed progress/proof requests,
complete intake, then write `session.local.md` last as `closed-idle` or
`partial-idle` with the end time. Unaffected files need no rewrite. Release the
acquired interaction lease and the turn-scoped active ownership while leaving
a continuous incumbent resumable.

Return a closure receipt naming logical id/generation/session, current
model/effort evidence, governance manifest status, state paths and resulting
watermarks/digests, folded-through turn, remaining debt, consultation state,
end-time evidence, and incumbent status. The worker verifies the receipt and
recorded session id.

Return the memo before the worker's rebuttal or interpretation. For each
material comment, distinguish checkable fact/method from advice, verify alleged
errors against the primary artifact, make confirmed document repairs, and
state the worker's resulting decision. Say the advisor supported, opposed, or
found evidence insufficient—never that it authorized, permitted, denied, or
vetoed work. Do not seek advisor acceptance of a rebuttal.

An `ask` holds only the named material decision until the answer arrives or the
user explicitly proceeds without it. A `tell` is nonblocking. Neither mode
transfers the decision.

## Conditional routes for rare mechanics

Read only the named long-catalog sections whose condition applies:

- first consultation, new scope/site, or metadata schema creation →
  `research-advisor.md` §§ “Scope and continuity” and “Establishing the logical
  advisor”;
- legacy state, missing/corrupt semantic state, unresumable incumbent, provider
  migration, successor, or generation fence → `research-advisor.md` § “Start,
  resume, repair, and succession” and `advisor/charter.md` §§ “Logical binding
  and state ownership” and “Serial ownership and succession”;
- competing advisor owners, an ABA-style resurrection, or lease recovery →
  `research-advisor.md` § “Serial ownership and locking” and
  `advisor/charter.md` § “Serial ownership and succession”;
- an ambiguous/reused interaction, stale open interaction, or fold/watermark
  recovery → `research-advisor.md` §§ “Invocation and deduplication,” “Fold-in
  debt,” and “Semantic-state reconciliation”;
- document-cursor corruption, rewritten history, external followed paths, or
  atomic state-replacement recovery → `advisor/charter.md` § “Governance and
  research-corpus synchronization”;
- handoff completeness repair → `advisor/charter.md` § “Mandate” / “Handoff
  completeness repair” and `topics/handoffs.md` § “Advisor intake for handoff
  repair”;
- hung/disappeared advisor or ambiguous transport completion →
  `research-advisor.md` § “Natural-language commands” from the transport and
  recovery paragraphs;
- exact `Shutdown advisor`, fresh-per-consult retirement, or archive/reboot
  preparation → `research-advisor.md` § “Natural-language commands” from
  “Shutdown advisor” and `advisor/charter.md` §§ “Shutting down the serving
  incarnation” and “Serial ownership and succession.”
