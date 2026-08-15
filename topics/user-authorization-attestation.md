# User authorization attestation consumption

> User authorization attestation consumption is a dormant, gate-specific
> protocol by which an agent mechanically verifies one exact user-issued
> capability without making routine user-intent or inter-agent claims depend on
> signatures.

Topic: `user-authorization-attestation`

Status: no verifier, key, gate, or required-attestation rule is implemented or
authorized. The signed-gate registry is empty by default.

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

The advisor interaction prefix in `advisor/serve.md` is also separate. Its
`from`/`sign-off` lines are a return address and claimed provenance, not this
capability.

Candidate protocol shapes are kept in
[authorization-attestation sketches](user-authorization-attestation.sketches.md).
