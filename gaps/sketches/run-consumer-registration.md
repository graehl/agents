---
slug: run-consumer-registration
noticed: 2026-09-24
where: scripts/claim-refs; agentctl_plugins/aim.py on_note
---

**Outcome:** a run record lists the non-run consumers that depend on it — a
manuscript section, a repo-subset publication, a `<topic>.runs/` ledger — so
"what depends on this run?" is answerable from the records and queryable in
Aim. Run consumers already point backward through
`params.inputs.<KEY>.source_run_id`; this adds the non-run case.

**Approach:**
- The consumer's own citations stay authoritative
  ([claim-provenance](../../topics/claim-provenance.md)). A derived
  `claim-refs sync <paper-dir>` writes
  `params.consumers["<section-path>"] = {synced_at}` into each directly cited
  record and removes that consumer from records it no longer cites. Store
  direct edges only; ancestry stays a walk, so cutting a citation removes
  exactly one edge per run.
- Consumers that are not documents register explicitly, e.g.
  `claim-refs register <experiment>/<run-id> <consumer-id>`.
- Both need a write path keyed by run reference. `agentctl note <job>` reaches
  only the job's current run through local `.agentctl/jobs/<job>/current.json`,
  so it cannot annotate an older run or a record pulled back from a remote
  worker. Reuse `on_note`'s record-editing code with a run-reference target.

**Open decisions:** mutating committed run records adds churn to `runs/aim/`
(already excluded from source admission); the alternative is a per-consumer
manifest file, which loses Aim queryability. The reverse query must also
cover consumers of a run's descendants.
