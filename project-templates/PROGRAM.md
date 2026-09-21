# Program Project templates

Develop a contributable inventory of project templates, capability bases,
instructions, and setup scripts that gives an agent-built project a working,
understandable starting point. A project can combine several capabilities and
techniques; its template composes multiple bases rather than choosing a single
stack inheritance tree. Shared material has one canonical destination and
content, with the project's root `AGENTS.md` assembled from distinct instruction
contributions in a defined order.

Project creation is primarily configuration and deterministic scripts. A
starter should become usable before a model customizes it. A subsequent
preparation turn incorporates the user's intent into project instructions and
the README description, confirms the run/test/build paths, and leaves the
project ready for app implementation. Ongoing documentation follows actual
behavior, including revising the README lede when the project's purpose changes.

The instruction inventory aims for a legible, portable selection of software
engineering, testing, UI, and stack-specific practices. Universal guidance
belongs in the minimal `base`; capability bases carry conditional routes and
the detail for their languages or activities. Polyglot guidance can be
available without loading every language into every session. Research,
tracked-run infrastructure, agentctl, personal host policy, and the full
authoring repository's boot are outside the intended default project payload.
Expert editing and appropriately scoped experiments should establish which
guidance earns its reading and execution cost.

Templates are also entry points into the inventory: later requests such as
adding a server should use the same conventions and mechanical components as
creation-time selection. An instantiated project vendors the relevant files,
including supported later additions, and works independently of this source
checkout, its symlinks, and YA's continued availability.

This repository's `project-templates/` directory is the YA-default library.
YA retrieves a configured GitHub revision into private application data and
can layer additional sources that reuse these bases. Source repository,
content root and revision are overridable; a future vendored YA copy is an
option, not a requirement for a separate repository or submodule. This program
owns the reusable content and composition contract; YA owns project creation
UI, authorization, source admission, App-pane delivery, and session dispatch.
