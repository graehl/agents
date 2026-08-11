# ideas/ — uncommitted project seeds

`ideas/` is the tracked incubator for a clever, fun, or potentially useful idea
that the user wants preserved here but that does not govern the agents
repository. A seed records enough for later rediscovery without declaring a
project, roadmap item, task, or intention to build.

This separation keeps `topics/` searchable as current project context. Use a
topic when the material governs this repository; use `tasks/` for private
active-work state, `gaps/` for a deferred defect, and `on-deck/` only for an
executable queued run. None is a synonym for an idea seed.

## Entry format

Use one kebab-case file per idea: `ideas/<slug>.md`. No central index is
required; filenames and full-text search are the index. Start with:

```markdown
# <idea name>

> <one-sentence, self-contained statement of the idea>

Status: seed — preserved, with no commitment to build.
Captured: <YYYY-MM-DD>
```

Then record only what gives the seed durable value: why it may be interesting,
the minimum mechanism or shape that makes it distinct, important constraints or
dead ends already noticed, and open questions. Use descriptive sections when
they help; do not add empty template headings. Write for the user and a fresh
capable agent with no session context.

## Retrieval and lifecycle

Do not scan `ideas/` during ordinary work. Read it when the user asks to recall,
compare, refine, or pursue a saved idea. Existence is not authorization to
research, plan, implement, queue, or periodically revisit it.

When an idea becomes real work:

- if it now governs this repository, move its durable content into the relevant
  `topics/` document and remove the seed in the same commit;
- if it becomes a separate project, establish the new repository's own source
  of truth, then remove the seed in a small commit that names or links the
  destination; and
- if it is no longer worth preserving, delete it in a small commit rather than
  accumulating retired or rejected seeds.

Git history is the archive. Do not retain a second authoritative copy or a
permanent promoted stub merely to keep `ideas/` populated.
