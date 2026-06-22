# LITERATURE SEARCH — retrieving prior art (snowballing-first)

Loaded with `survey-field.md` / `research-frontier.md` whenever the task is to
gather prior art: a full field survey, a "what's known about X" subtopic, or
"catch up on X before I build" reconnaissance. This file is the **retrieval
method** — how to *find* the right papers. `survey-field.md` then organizes
them into a graded field map; `research-frontier.md` ranks the voids. Obey the
`recall` vs `grounded` mode, evidence grading, and disconfirming-search
discipline defined in those files; do not restate them here.

## Why snowballing, not keyword search

An agent reasons from a frozen **training snapshot**. The literature has moved
since the cutoff; keyword search alone over-indexes on SEO'd/blog content and
misses the citation structure that actually organizes a field. The reliable
bridge across the cutoff is **citation snowballing from anchors you already
trust**: established work you are confident about, whose forward citations are,
by construction, the newer papers that build on it.

## Primary: citation snowballing

Needs a paper DB exposing citation/relevance scores. Use these (free, no key):
- **OpenAlex** — forward citations + counts.
  - resolve an anchor: `https://api.openalex.org/works?search=<title words>` →
    take the `id` (a `W…` work id).
  - forward-cite (the bridge across the cutoff):
    `https://api.openalex.org/works?filter=cites:W<id>&sort=publication_date:desc&per-page=25`
    (use `&sort=cited_by_count:desc` for impact-ranked instead of recent).
  - backward-cite: the work's `referenced_works`.
- **Semantic Scholar Graph API** —
  `https://api.semanticscholar.org/graph/v1/paper/<id>/citations?fields=title,year,authors,citationCount,intents,isInfluential&limit=100`.
  `intents` (background / methodology / result) and `isInfluential` are
  relevance signals: a *methodology* or *result* citation is far more on-topic
  than a background mention — rank by them.
- **Connected Papers** (co-citation / bibliographic-coupling neighborhood),
  **Papers with Code** (benchmark + SOTA leaderboards), Google Scholar
  "Cited by" (manual fallback, no clean API).

Fetch the JSON endpoints with the web tool; record the retrieval date.

**Procedure.**
1. **Anchors** — pick 2–5 papers you are confident are seminal in the *exact*
   subarea (not an adjacent one). Pre-cutoff and well-cited makes them reliable
   bridge points. Name the anchor set explicitly in the output.
2. **Forward snowball** — pull each anchor's citers; rank by recency × DB
   relevance (cited_by_count, citation intent, influential flag). This is the
   step that catches post-cutoff work.
3. **Backward snowball** — the anchors' references, for foundational pieces the
   snapshot under-weighted.
4. **Iterate** — promote each newly found high-relevance paper to an anchor and
   repeat. **Stop at saturation**: when new citers stop surfacing unseen
   relevant work (state that you reached it, or that you did not).
5. **Disconfirm** — also chase citers that *refute or bound* an anchor's claim,
   not just descendants that extend it (per `survey-field.md`).

## Secondary: keyword/phrase search — only for the freshest work

The very newest papers have **no citations yet**, so snowballing cannot reach
them. For that frontier slice only, fall back to phrase search (arXiv recent
listings in the relevant categories; web search) — but citation relevance is
absent there, so substitute an **author/lab prior**:
- Keep a **known-productive-labs/authors model** for the subfield (a short
  curated roster). Filter fresh keyword hits through it; a paper from a
  known-strong group is higher-prior than one from an unknown.
- **Engagement signal**: a known author/lab posting, presenting, or discussing
  a paper (including social media) is a fresh-relevance signal when citation
  counts don't exist yet.
- Promote a vetted fresh hit to an anchor so the next snowball pass picks up its
  neighborhood as citations accrue.

Maintain the labs/authors roster as you go — it is reusable across tasks and is
itself a cheap source of anchors.

## Output and hygiene

- For each kept paper: stable key, title, authors, venue+year, DOI/arXiv id,
  URL, citation count, retrieval date, and one line of **what is new vs the
  anchor it descends from**. This feeds `survey-field.md`'s `related-work/`
  manifest directly — do not invent a parallel format.
- Dedup by DOI/arXiv id (the same work recurs under multiple titles/preprints).
- Never fabricate a citation. In `recall` mode you may name a technique and the
  gist of who/when, but flag that exact venue/year/authors need a `grounded`
  snowball to pin down.
- State the **anchor set, the DBs queried, and the coverage-cutoff date** at the
  top of the output, alongside the grounding mode.
