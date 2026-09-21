---
name: riff
description: Redo the most recent creative request, or a supplied new request, as four independent random-string-inspired alternatives for choosing and refining a favorite. Use when the user invokes /riff or $riff. Covers UI, stories, roleplay, and technical-document creation or revision.
---

# Riff

Produce four alternatives from the **same request and procedure**, each with a
fresh inspiration string. The point is to vary independent runs of one prompt,
not to prescribe four styles or ask successive attempts to avoid earlier ones.

## Resolve the request

`/riff <request>` supplies a fresh creative request. Bare `/riff` redoes the
most recent substantive creative request, retaining relevant user constraints,
source material, attachments, and later corrections. Skip intervening status
or meta discussion; do not reinterpret "redo" as refining the default answer.
If there is no recoverable request or essential source, ask for it. Otherwise
state the recovered brief in one sentence and proceed.

A tail that only modifies execution (for example, "use model-generated
strings") still targets the last creative request; do not treat it as a new
creative brief.

Creation and revision include UI concepts, storywriting, roleplay, and technical
documents. Preserve facts and API behavior in technical prose, established
canon and player agency in roleplay, and the user's functional requirements in
UI. Choose comparable scope and polish for all four candidates.

## Generate four candidates

Prepare one shared brief with the source material and constraints. Use fresh
subagents or equivalent isolated contexts when available and allowed, one per
candidate; give each the same brief and procedure below. Do not inherit the
whole conversation, the previous default attempt, sibling candidates, or this
four-candidate orchestration instruction. Leaves produce one candidate and do
not delegate. Batch them if concurrency is limited; fresh contexts matter more
than simultaneous execution. Use the session's model unless the user asks
otherwise.

Keep artifact outputs separate and start from the same source snapshot. Avoid
reading prior candidate artifacts as inspiration. If the current source already
contains changes from the default attempt and the earlier source is unavailable,
say what baseline is being used; never silently undo user work. The coordinator
may have seen the first attempt: do not pass its design choices to the leaves
unless the user specifically asks to retain them.

If fresh contexts are unavailable or forbidden, produce four separate attempts
locally and disclose that they share conversation context. Do not claim they
are independent. This skill never rewinds or clears the current conversation.

Give each candidate this procedure:

> [The same creative request, source material, and constraints]
>
> Generate a long random alphanumeric string using a shell tool.
> Define a coherent creative direction based on the string. Look for
> subpatterns, numbers, fragments, rhythms, or other associations that inspire
> you. Use judgment to bring that direction to life and make it work well for
> the request. Do not reveal the string in the creative output; it is only
> inspiration.

Default to an external shell-generated string, once per candidate. If the user
explicitly asks for model-generated randomness, replace only the generation
sentence: generate the string yourself without tools, scripts, random-device
reads, external services, or retrieved strings. Honor the chosen source; do not
silently substitute when a required facility is missing. Retain strings with
working artifacts when practical, outside the creative deliverables.

Do not select among several strings, preassign artistic visions, or rewrite
candidates to manufacture distinctness after comparison. Preserve the initial
four, including similarities; this recipe's benefit is not established.
Ordinary correctness and rendering repairs are fine. Compare only after all
four candidates exist.

## Present and refine

Label alternatives A–D, each with a short description of its actual direction.
Recommend a favorite with a concrete reason, then ask the user to choose one
or identify qualities to combine. An existing instruction to choose and refine
autonomously authorizes that step; otherwise wait for selection. Refine the
chosen direction without flattening what made it interesting. Preserve the
unchosen alternatives; roleplay branches do not become canon by being shown.

For UI, follow the project's design and capture facilities. Use a verified
interactive comparison view when available: four expandable candidates,
ordinarily in a 2×2 container. Otherwise deliver inspected screenshots one at a
time with concise prose; follow mobile checks where applicable. For writing,
present comparable excerpts sequentially in chat or the requested artifact
format. Do not build a viewer merely to run this skill or claim a local URL is
reachable without checking. Mark an unrenderable UI candidate as unrendered.

This invocation authorizes creative alternatives, not production deployment or
overwriting the original. A request to implement the chosen result is handled
under the project's ordinary workflow.
