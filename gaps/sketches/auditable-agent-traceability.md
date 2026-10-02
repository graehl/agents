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
