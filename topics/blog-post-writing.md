# Blog-post writing

> Build a technical or research blog post as a static, navigable web document
> with a strong first screen, locally owned rich elements, and citations
> calibrated to the claims rather than to a venue quota.

Topic: `blog-post-writing`

## Default publishing shape

Use a [Quarto website blog](https://quarto.org/docs/websites/website-blog.html)
for the default GitHub Pages or simple-static-host path. It supplies post
listings, navigation, search, categories, feeds, draft handling, citations,
math, code, and the same rich-element route used by other research documents.
One post normally owns:

```text
posts/<post-slug>/
  index.qmd
  data/
  figures/
  components/
```

Create only used directories. Keep a post's images, data extracts, and custom
components beside it unless they are genuinely site-wide. Use relative links
and record any site `base-url`/subpath setting needed by GitHub Pages.

Front matter states title, one-sentence description or dek, author, publication
date, modified date when materially updated, categories, preview image and alt
text, draft status, and canonical URL when syndication could create duplicates.
Configure the site-wide navigation, feed, analytics, and license once rather
than restating them in every post.

## Reader path

The first screen shows the rewarding object or concrete claim, a compact
explanation of why it matters, and enough regime/scope to prevent the hook from
overclaiming. Then give the shortest path through result, mechanism or recipe,
comparison, limitations, and ways to inspect or reproduce more. Follow
[`technical-writing`](technical-writing.md) for cold-reader comprehension; a
research showcase additionally follows
[`research-blog-writing`](research-blog-writing.md).

Place plots, result tables, example rows, math, and demos where they establish
the adjacent claim. Do not exile the post's best evidence to a download or a
dashboard reached only after the prose. Follow
[`document-writing-browser-interactive`](document-writing-browser-interactive.md)
for captions, client-side interaction, static fallbacks, tooltips, math, and
navigation.

Use Observable JavaScript inside Quarto for a few reactive displays. Promote a
standalone data explorer to Observable Framework, or a bespoke publication UI
to Astro, only when that experience is itself a maintained artifact. Link it
from the post and preserve the post as the durable, static explanation of what
the explorer shows.

## Citation calibration

When the post reports research, follow
[`research-writing`](research-writing.md). Always link or cite the closest
competing/alternative work and the most influential or inspirational parent
works. Attribute borrowed datasets, code, metrics, visual grammars, and
methods. A lighter inline-link style is usually more readable than a
conference-paper citation surface; use formal citation keys and a bibliography
when the post's claims are dense, scholarly, or intended as a durable research
reference.

Do not cite every commonplace statement or inflate a related-work parade to
signal seriousness. Citation density is appropriate when a reader can locate
the sources needed to understand provenance, compare the contribution, and
challenge its scope without the references overwhelming the reading path.

## Release check

Build the whole site, not only the post preview. Verify the post from the site
root and its direct URL, the listing card and feed entry, preview image, heading
anchors, internal and external links, citations, math, downloads, static
fallbacks, phone layout, and JavaScript-enhanced controls. A post intended for
plain static hosting must remain useful when custom JavaScript fails.
