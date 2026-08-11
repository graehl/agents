# Distributed URL comments with human/AI provenance

> Give any URL an external comment layer whose pseudonymous authorship tracks
> human versus AI participation and whose annotations remain anchored to the
> content people actually saw.

Status: seed — preserved, with no commitment to build.
Captured: 2026-08-11

## Core shape

- A browser, client, or service can show comments for any URL without requiring
  the site owner to host or enable them.
- Storage and discovery may be distributed (for example, DHT-shaped),
  federated, or supplied by interchangeable third-party hosts. The shared
  protocol matters more than one mandatory operator.
- Each comment retains a pseudonymous identity and explicit provenance for
  human-authored, AI-authored, mixed/assisted, or unknown origin. The system
  must not collapse author identity merely because a thread crosses categories.
- Human and AI comments can have separate presentation strata. A human reply to
  an AI comment brings that thread into the human-attention section while the
  per-comment provenance remains intact.
- A URL alone is not a stable annotation target: pages disappear and mutable
  pages change. An annotation therefore identifies or archives the exact
  response content/version it addresses, ideally with a content hash and enough
  retrieval metadata to show later readers what was commented on.

## Why it may be interesting

This would make discussion a property of a resource rather than of the
publisher's chosen platform. It could connect commentary across mirrors and
social systems, preserve context after link rot or edits, and let readers apply
their own trust, identity, and human-attention filters instead of accepting one
site's ranking or moderation surface.

The human/AI distinction is more useful as provenance plus filtering than as a
single exclusion rule. AI-originated material can become socially relevant
when a human engages with it, without laundering the original author type.

## Prior-art leads, not novelty claims

The user recalls hearing a related idea around BitTorrent and expects that DHT
or decentralized-web projects may already have explored it. The user and Kyle
also expect blockchain projects to have tried tokenized variants; a token is
not intrinsic to this seed. Search distributed web annotation, content-addressed
annotations, federated comments, and human/AI authorship provenance before
claiming novelty or choosing an architecture.

## Hard questions

- What can “human” or “AI” provenance honestly mean when authors may use tools,
  lie, share keys, or collaborate? Signed declarations and client provenance
  are tractable; proof of humanness is a different and harder system.
- How are URL canonicalization, fragments, dynamic responses, personalized
  pages, mirrors, and revisions mapped without merging unrelated content?
- Who pays for snapshots, and how do copyright, deletion, privacy, malware,
  and legal takedown requirements interact with durable archives?
- How do readers select trust roots, moderation lists, ranking policies, and
  spam/Sybil defenses without recreating one centralized social network?
- How are comments discovered efficiently while allowing multiple hosts,
  offline replication, and graceful loss of any one index?
- What non-token incentives are sufficient for hosting, moderation, identity
  reputation, and long-term availability?
