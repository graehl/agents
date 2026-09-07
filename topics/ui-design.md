# UI design proposals

> UI design questions default to an inspected visual proposal grounded in the
> project's components and design language, using project-specific mockup and
> display facilities when available.

Topic: ui-design

## Trigger and scope

Use this route for proposed UI appearance or interaction: "thoughts on the UI
for X", "what do you think X should look like", an explicit mockup request,
or equivalent design/spec discussion. Deliver a rendered proposal by default
without waiting for the word "mockup". Respect prose-only or no-tools requests.
A question about an existing UI defect, a label, or implementation mechanics
does not by itself request a new design. A broad UI audit retains its existing
scope; [ui-report](ui-report.md) owns screenshot-backed audits.

Creating an isolated mockup, rendering it, and capturing it are part of this
design discussion. Use scratch artifacts, a fixture, or an isolated checkout
as appropriate; do not change production behavior or shared live state merely
to illustrate an idea. Ordinary resource, dependency, and publication rules
still apply. The proposal is not permission to implement the feature.

## Project-specific routing

This shared topic owns the default outcome. Before choosing the design or
commands, follow the project's instructions/glossary to its existing design
guide and mockup/export/browser facility. The default project entry is
`topics/ui-design.md`, in the owning topic scope or established `docs/topics/`
layout. A differently named canonical guide wins; follow its links instead of
creating another owner. Project guidance supplies local style and mechanics.
When working in the agents repository itself, this file is the shared guide,
not evidence that a local UI/export facility exists.

If no guide exists or it is incomplete, discover the needed facts from nearby
screens, component examples/stories, styles/assets, package scripts, and browser
tools. Inspect representative existing renders when accessible and read the
relevant component/style owners. State material inferred conventions. Missing
documentation is not a reason to stop or invent a design system.

A project facility guide should provide verified pointers and commands for:

- Representative screens and reusable components, theme/type/spacing tokens,
  icons/fonts, and relevant interaction/mobile conventions.
- Fixture or story setup with realistic data, required providers and themes,
  and the isolated render/capture path.
- Export and viewing: supported document/bundle format, relative asset handling,
  script/font limits, artifact location, and a reachable viewing link.
- Current capabilities versus proposed work, with owning gaps for missing
  pieces. An unimplemented exporter or viewer is not a runnable instruction.

When adding a reusable project facility, record those facts there. Prefer the
existing builder/component playground; established tools such as Vite or
Storybook may supply an adapter, but neither is mandatory. Do not bake a named
project's commands, viewer internals, or proposed bundle schema into global
instructions. Facility setup must remain proportionate to the request.

## Produce and present

Recommend one design with enough context and realistic content to assess its
placement, hierarchy, controls, and important states. Reuse actual project
components/styles when practical; a lightweight HTML/CSS mockup may approximate
them when mounting the app is costly. Identify consequential approximations.
Show alternatives only when a meaningful unresolved choice benefits from them.

Render and inspect the proposal; source code or an accessibility-tree snapshot
alone does not establish its appearance. Follow the project's UI-testing and
layout guidance, including desktop/mobile coverage where applicable. Inspect
captures sequentially. If available tooling cannot render, state that limit
and provide a clearly unrendered sketch rather than claiming visual validation.

Screenshots are sufficient. When a project and the user's display surface
support a higher-fidelity document or HTML/CSS/assets bundle, it may replace or
accompany the image; an image plus a link to the viewable document is welcome.
Verify the actual viewing path and dependencies, including remote reachability
when relevant. A local dev URL, an export file, or a proposed viewer feature
alone does not establish that the user can view it. Fall back to inspected
screenshots when the richer path is unavailable; do not make viewer development
a prerequisite for answering the design question.

Keep the final response focused on the visual artifact, the recommendation and
its main tradeoff, intended interactions, and any material unresolved choice.
Distinguish mocked behavior from working behavior. Retain source and artifacts
at durable paths so a follow-up can revise the proposal without recreating it.
