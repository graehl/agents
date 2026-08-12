# User authorization attestation consumption

> User authorization attestation consumption is a dormant, gate-specific
> protocol by which an agent mechanically verifies one exact user-issued
> capability without making routine user-intent or inter-agent claims depend on
> signatures.

Topic: `user-authorization-attestation`

Status: sketch only. No verifier, key, gate, or required-attestation rule is
implemented or authorized. The signed-gate registry is empty by default.

The YA issuance/transport counterpart is
[user authorization attestations](https://github.com/graehl/yepanywhere/blob/main/topics/user-authorization-attestation.md).
YA owns how an attestation is issued and delivered; this repository would own
how an instructed agent recognizes a named gate and consumes verified claims.

## Boundary

An attestation would be an opt-in capability for a gate declared in advance,
not general proof that one message outranks another. Unless a governing rule
names a particular attestation gate:

- do not invoke a verifier;
- do not ask the user to sign anything;
- do not prefer signed prose over ordinary evidence; and
- do not reject another agent's research report or account of user intent
  merely because it is unsigned.

The advisor interaction prefix in `research-advisor.md` is also separate. Its
`from`/`sign-off` lines are a return address and claimed provenance, not this
capability.

## Gate declaration sketch

A future rule that genuinely needs this mechanism would declare, in advance:

```text
Authorization-attestation gate: <stable gate id>
Claim: <exact action or override the user may authorize>
Scope: <target paths/session/program/external effect>
Destination: <session/logical relation, or any>
Replay/freshness: <none by default, or a stated narrowing>
Fallback: <how the user can issue/reissue or resolve it>
Verifier: <mechanical helper and trusted public-key source>
```

Only a verified payload with the named gate id and compatible claim/scope can
satisfy that gate. It cannot authorize a broader action, and no user-issued
attestation can override system/developer authority. Absence or verifier
failure at a declared gate must expose the exact missing fact and a user path
to issue, reissue, or explicitly choose the documented fallback; it must not
become a dead-end refusal.

## Consumer sketch

The agent should invoke one cheap mechanical verifier rather than reason about
signature bytes. A normalized successful result would expose:

- protocol/version and key id;
- gate id, exact claim, scope, and destination;
- hash of the exact authorized user turn;
- optional stable ids/hashes of the recent turns it answers;
- issue timestamp and message id for audit; and
- verification source (`signature` or a future OS-bounded capability file).

The verifier returns explicit `verified`, `unverified`, `malformed`, or
`unsupported` status and never silently widens claims. Timestamp and message
ids make reuse visible; they imply no expiry or anti-replay rule unless the
declared gate says so. With no anti-replay protection, possession is
intentionally bearer-like for the exact signed claim.

The public key and verifier may live in `~/agents`/`~/bin`, but the private key
must not. A verifier or public-key file writable by the same unconfined actor
offers operational convention, not a security boundary; any implementation
must state the assurance it actually has.

## Linux capability-file alternative

A Linux-security-bounded inbox could normalize to the same verified claim
without public-key computation: YA writes an atomic capability record and the
agent can read but cannot create or alter records. Plain `chmod` within an
unsandboxed same-UID session does not establish that property. The helper must
verify the mount/UID/sandbox boundary before reporting `verified`.

This alternative is attractive for local, bounded sessions and cheap repeated
checks. Signatures travel better across hosts, transcripts, and provider
boundaries. Both transports should share gate ids and normalized claims so a
future rule does not care which trustworthy issuance path was used.

## Adoption bar

Keep the registry empty until a recurring authorization-transfer failure names
a concrete gate. Before implementation, compare the two paths on assurance,
cross-host portability, transcript durability, key/boundary administration,
and agent token/tool cost. Do not build general message-authentication
infrastructure merely because the mechanism is possible.
