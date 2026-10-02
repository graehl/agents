---
slug: auditable-agent-traceability
noticed: 2026-10-02
where: topics/user-authorization-attestation.md; topics/provenance-tracking.md
---

**Outcome:** every consequential agent action (tool call, edit, message to
another session, external effect) can be audited after the fact for two
things: the authority that permitted it, and the context it could have been
caused by. "Could have been caused by" covers the instructions, user turns,
peer messages, tool results and external data in context at that moment.
The aim is to answer "why did the agent do X, and who allowed it?" from
records rather than from the agent's own retelling.

The user expects organization-scale AI routers, the central services that
mediate many users, agents and data sources (Palantir-style platforms, for
example), to move this way. Single-user harnesses such as YA plus `~/agents`
are a small testbed for the same structure.

**Approach:** three layers, each useful without the next.

1. *Authenticated inputs.* Messages crossing a trust boundary carry
   signatures that can be checked mechanically:
   - Provider or router signs model outputs. The system prompt names the
     router's verification key, so a receiving session can check that a
     cross-session message really came from that router and a named session,
     not from copied prose.
   - Verify before execute: the harness runs a tool call only if it carries
     a valid provider signature. This is the first piece to build, because
     a malicious router writing tool calls directly is the highest-impact
     threat (see *Malicious-router threat* below). The signature must cover
     a hash of the request context plus a nonce or sequence number.
     Otherwise the router can replay a genuine signed call, such as a real
     `rm -r build/`, in a context where it does damage. Prose and reasoning
     can stay unsigned at first.
   - User authorization attestations: gate-specific signed user approvals.
     The dormant design is in
     [user-authorization-attestation](../../topics/user-authorization-attestation.md)
     and its sketches companion (agent consumption), plus YA's
     `topics/user-authorization-attestation*.md` (issuance and transport).
     That design covers only user authorizations; provider-output signing is
     new here.
   - Optionally, harness-signed tool results, so a later auditor can tell a
     real tool output from text the model wrote that looks like one.
2. *Possible-causal provenance (automatic, sound, imprecise).* Each item
   entering context gets an identity: content hash, source, version and
   timestamp, signed when it crosses a trust boundary. Instruction files are
   identified by Git blob SHA. External data is identified by a reference
   into an immutable, content-addressed store (Git trees, a versioned
   database, or an append-only filesystem), so the exact version read can be
   fetched later. Each action record stores the context manifest at that
   moment: one hash per item, or a Merkle root per turn. Anything absent
   from the manifest cannot have caused the action, apart from what is in
   the weights. That bound needs no model internals. Prior-art analogs are
   in-toto/SLSA step attestations, which record the hashes of each build
   step's inputs and outputs, and C2PA content credentials.

   *Tamper-evident log.* A signing router should not be able to rewrite
   these records after the fact. The standard primitive is an append-only
   Merkle transparency log with published signed tree heads (Certificate
   Transparency, RFC 6962/9162; Sigstore Rekor; Go's checksum database).
   Each kind of fudging needs its own defence:
   - *Rewriting the past:* consistency proofs show each new root extends
     the previous one. Every published trace that carries a signed root and
     an inclusion proof pins all earlier history.
   - *Dropping records:* each record carries a per-session or per-user
     sequence number and the previous record's hash, and the client keeps a
     signed receipt per step. A missing record shows up as a broken chain.
   - *Showing different histories to different parties:* independent
     witnesses cosign tree heads (C2SP tlog-witness), or clients gossip
     them. Two conflicting signed roots for the same tree size prove
     misbehaviour.
   - *Lying about timing:* anchor roots to an external timestamp
     (RFC 3161, Roughtime) or to another public log.
   - *Fabricating content when it is first logged:* the log cannot catch
     this, because it proves consistency, not truth. Layer 1's provider
     signatures on model outputs, client-signed inputs, or hardware-enclave
     attestation for router-side computation are still required.

   Log only salted commitments to the traces. Publishing a trace then means
   revealing its contents together with an inclusion proof, and the log
   itself discloses nothing. Public traces bind the router only if they
   carry signed roots that witnesses cross-check. Otherwise the router can
   keep a clean branch for audited traces and a doctored one for the rest.
   Someone who later steals the key cannot rewrite history already covered
   by published roots. Building blocks: Trillian or Tessera for the log;
   Crosby & Wallach, "Efficient Data Structures for Tamper-Evident Logging"
   (USENIX Security 2009), for history trees.

   *Client-side checks.* An honest client keeps what it sent and what it
   received. It verifies that the router's signed receipt commits to
   exactly those hashes, with an inclusion proof under a signed root. This
   proves that the router signed what that client saw, which gives
   non-repudiation for the client's own view. Collaborating clients
   exchange the roots they hold: any two must be linked by a consistency
   proof, or the pair is a transferable proof of a fork. Each client also
   confirms that its own records are included under the latest root they
   share. The name for this guarantee is *fork consistency*, from SUNDR
   (Li, Krohn, Mazières, Shasha, OSDI 2004). A misbehaving router can split
   clients into separate histories but must keep them apart forever, and
   any later contact between groups, or a shared witness, exposes the fork.
   A partition whose groups never compare stays undetected. That is why
   witnesses remain worthwhile even when clients collaborate.

   *Provider origin without signatures.* Output that works at a frontier
   capability level is weak, implicit evidence that a frontier model
   produced it. A router cannot fake that quality without access to some
   comparable model. This evidence does not rule out substituting another
   capable model, or a cheaper one where a task does not test the
   difference. With a trusted timestamp, for example the log's anchored
   root, a forger cannot backdate a later model's output. The question
   "what could have produced this at time T?" can then be judged
   permanently against the capability frontier at T, so the evidence does
   not decay. It can still be revised when a model that already existed at
   T is disclosed later, which mostly matters near the frontier.

   This evidence cannot catch a focused deception attack: small, targeted,
   high-impact edits spliced into an otherwise genuine output. Altered facts
   are not the main exposure. The harness already distrusts a model's
   uncited facts, and facts it relies on come from tools run in the user's
   harness, whose results the router never handles. Router-hosted tools,
   such as server-side web search, are the exception: their results are
   router-mediated too. The exposure is model output that is *executed or
   relied on as judgment*:
   - tool-call arguments and commands;
   - code and configuration: a flipped constant or sign, a changed
     dependency or version pin, a swapped URL, a dropped check;
   - choices and summaries over trusted facts, such as which result to
     emphasize or which branch to recommend.

   These edits leave the output fluent. Partial defences short of
   signatures:
   - *Random audit sampling:* the client sends a random fraction of
     requests directly to the provider and compares the answers. If the
     router cannot tell audited requests from ordinary ones, sustained
     corruption becomes risky for it. Sampling does nothing against a
     single targeted strike. Comparison is noisy except on deterministic or
     low-temperature requests.
   - *Local verification:* a local model checks that citations resolve to
     harness tool results and support the claims attached to them. This
     enforces the existing fact boundary. It catches little in code or
     actions, where an altered constant cites nothing; review, tests and
     sandboxed execution are the usual guards there.

   Only signatures on the upstream model outputs defeat focused deception.
3. *Attribution narrowing (approximate).* Within the manifest, rank which
   items actually drove the action:
   - attention or gradient attribution, which needs model internals and is
     therefore provider-side only;
   - the model's own stated reasons, accepted only as citations that resolve
     to manifest hashes and never as authoritative, because chain-of-thought
     faithfulness is known to be weak;
   - counterfactual replay: remove or alter one item, rerun, and see whether
     the action changes. This is expensive, so reserve it for incident
     review.

**Malicious-router threat:** a router acting as a man in the middle
between harness and provider is strictly worse than prompt injection. An
injector has to persuade the model. The router writes tool calls directly,
with full knowledge of the context and timing, executes with the harness's
permissions, and can make the call look like the surrounding genuine work.

Without signatures, the client's evidence of provider origin is evidence of
capability. That stops separating provider from attacker, because the
attacker is capable too, and a sneaky but effective command requires
capability. The question shifts from intelligence to *aligned*
intelligence: is this what a trusted, aligned model would have produced
here? That is much harder to judge from one output, since misalignment can
sit in a single action inside otherwise excellent work.

Defences that do not depend on signatures, which also back up
verify-before-execute against ordinary prompt injection:
- *AI control protocols* (Greenblatt et al., "AI Control: Improving Safety
  Despite Intentional Subversion", 2023), with router plus model treated
  as untrusted:
  - trusted monitoring: a local trusted model scores each tool call for
    suspicion before it runs;
  - defer to trusted: above a threshold, the trusted model's own action
    or a sanitized edit of the call runs instead;
  - resampling: the protocol asks the provider directly, bypassing the
    router, for the same step and compares. This is random audit sampling
    applied to actions, whose distribution should match;
  - escalation to human audit, within a limited budget. Showing every
    command for approval is weak against a well-crafted one.
- *Hardened, auditable execution:* every effect is mediated and logged into
  the same tamper-evident record. Permissions are capability-scoped, egress
  is allowlisted, and effects are staged or reversible (filesystem
  snapshots, dry runs), so an audit can find and undo damage rather than
  relying only on blocking it.

**Applications:**
- Forensics for prompt injection: which untrusted item preceded a tool call.
- Instruction-rule attribution: which instruction file version and section
  was in force when a rule fired, feeding
  [instruction-ablation](../../topics/instruction-ablation.md) and the
  evidence ledgers.
- Cross-session claims ("the user approved X") that can be checked against a
  signed origin instead of trusted as prose.
- Run provenance: extends
  [provenance-tracking](../../topics/provenance-tracking.md) from "which
  code produced this output" to "which context produced this action".

**Open decisions:**
- Who signs: provider, router or harness, and whose key the system prompt
  names. A provider signature proves model origin; a router signature proves
  session routing. These are different claims.
- Compaction and summarization break the chain unless a summary carries the
  hashes (or Merkle root) of what it replaced. Decide whether a summary is a
  new signed item that cites its inputs.
- Manifest cost: per-message hashes versus per-turn roots, and storage for
  long sessions.
- Privacy: hashes of secret or personal content can be confirmed by guessing
  low-entropy content; salted or keyed hashes trade this against public
  verifiability.
- Replay nondeterminism makes counterfactual attribution statistical, not
  exact.
- Adoption bar: as for attestations, nothing should be built until a
  concrete recurring audit or authorization failure names what must be
  traceable. Layer 2 is the cheapest to start with, since the harness
  already sees every context item.
