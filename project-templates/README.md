# Create and share project templates for YA

> A guide to making reusable project starters, extending YA-default bases,
> and sharing a template source with other YA users.

Topic: project-template-authoring

A template gives a new project its starting files, instructions and tools.
A **base** is a reusable part of that starter, such as web tooling, testing
guidance or a canvas app. Your template can combine several bases and add its
own files, so you do not need to copy the YA-default library to make a new
starter.

The YA-default source is [graehl/agents](https://github.com/graehl/agents),
using its `project-templates` directory. It contains **App canvas**, **Web
page** and **Storybook**. It is the default library for this system; a separate
repository or future vendored copy is not required to use its bases.

**Current delivery:** YA's source settings retrieve and validate libraries.
Creating and preparing projects through YA is still being integrated. Draft
templates can be inspected but are not approved for project creation. The
default templates remain draft until their content review is complete.

## Add a source in YA

Open **Settings → Project templates**, enable templates, and choose
**Fetch / update**. The **GitHub or local dir** field starts with
`https://github.com/graehl/agents/project-templates`. Put a GitHub directory
path directly after the repository URL; there is no separate subdirectory field.
GitHub sources also have a revision:

- Use just the repository URL when `library.json` is at its root.
- Use `HEAD` to fetch the repository's default branch tip when you update.
- Use a branch, tag or full commit SHA to select a particular version. A full
  commit SHA makes a shared example reproducible.

For GitHub sources, YA displays the commit SHA it actually fetched. Updating
checks the selected revision and reports **Already up to date** if it has not
changed. **Update from default branch** selects `HEAD` for that source.
There is no automatic background update or automatic check when opening the
template chooser.
While templates are disabled, Save records your settings without downloading.

For local work, enter an absolute directory or a path such as
`~/community/project-templates`. YA uses its files directly, without copying
or rewriting them. If it belongs to a Git repository, YA shows that repository's
HEAD and permits file references within that repository. Otherwise the chosen
directory is the source boundary. Git HEAD is provenance, not a fingerprint of
uncommitted files: Update always revalidates local sources. A local directory
can be a primary source or a supplementary overlay, just like a GitHub directory.

Use **Add source** for your own or a community library. Keep the YA-default
source in the list if your templates use its bases. Later sources replace
earlier entries with the same base or template ID. **Move up** changes that
order. Give new templates distinctive IDs unless you deliberately want to
replace an existing entry. The inventory identifies the source supplying
each effective template.

## Make a small community library

Start a GitHub repository with this layout. You may instead place the whole
layout in a subdirectory and tell YA its path.

```text
library.json
templates/
  my-canvas/
    template.json
    instructions.md
```

List the entries your source contributes in `library.json`:

```json
{
  "formatVersion": 1,
  "bases": [],
  "templates": ["my-canvas"]
}
```

Then create `templates/my-canvas/template.json`:

```json
{
  "formatVersion": 1,
  "kind": "template",
  "status": "draft",
  "id": "my-canvas",
  "title": "My canvas",
  "description": "A canvas starter for exploring my idea.",
  "extends": ["web-app", "canvas"],
  "files": [
    { "from": "instructions.md", "to": "AGENTS.md" }
  ],
  "overrides": []
}
```

The `web-app` and `canvas` bases come from the YA-default source. Add your
repository after that source in YA, then fetch both. `instructions.md` should
explain what is special about your starter and how an agent should work on it.
It is combined with the inherited root instructions.

Useful YA-default bases include `software-engineering`, `testing`,
`typescript`, `web-ui`, `web-app`, `canvas`, `page`, `writing`, `story`, and
`server`. `web-app` supplies shared web tooling; combine it with `canvas`
for a drawing app or with `page` for a content-led page. `story` builds on
`writing`. The server base supplies an optional add-on; inheriting it does
not mean a backend is already running.

To contribute a reusable base, put its manifest under `bases/<id>/`, use
`"kind": "base"`, and list the ID in `library.json`'s `bases` array. Bases
can themselves extend other bases. Keep `overrides` empty on a base; explicit
file overrides belong to the selected template.

## Choose how files combine

`from` names a file relative to its manifest. `to` names where that file goes
in the new project. Set `"executable": true` for a file that needs that mode.
Every referenced source file must exist inside its own repository. Relative
links to sibling directories are supported, including symlinks whose targets
stay inside the repository. Include complete skill resources and any files a
later add-on will need; a created project must stand on its own.

Source order selects the winning **base or template definition**. It does not
silently overwrite conflicting **project files** from different bases:

- Identical file bytes and executable modes coalesce.
- Different contents at the same destination require an explicit override.
- Root `AGENTS.md` combines distinct complete instruction fragments, in base
  order, without repeating an identical fragment.

For example, to replace an inherited README, put your replacement beside the
manifest and add this entry to the template's `overrides` array:

```json
{ "op": "replace", "from": "README.md", "to": "README.md" }
```

Use `omit` to remove an inherited destination. `append` and `prepend` add
UTF-8 text to an existing, unambiguous file; they do not resolve two conflicting
versions. There is no automatic JSON merge. Missing bases, dependency cycles
and inconsistent base ordering are validation errors.

## Keep content portable and suitable

Prefer relative source references. In retrieved GitHub content, YA also
relocates explicit `~/repository` references, such as `~/agents/topics/...`,
to the configured source directories. Local content is not rewritten.
Those aliases refer to the configured repositories, not a user's home folder.
Give repositories distinct names when using these aliases; with repeated
names, the later configured source supplies the alias.

For instructions installed into a project, use that project's declared
destination paths. Do not assume it can access the author's checkout or YA's
source cache. A file being reachable is not enough: review whether it helps
the intended task. Route writing advice to writing tasks, UI guidance to UI
tasks, and leave personal machine settings and unrelated research procedures
out of ordinary app starters.

An optional `.project-template/preview.svg` can illustrate the template.
It should be self-contained; YA displays it as an image. Runtime commands
and preparation instructions are described by `.project-template/app.json`.
Only use sources whose setup code you trust: fetching and validating a source
does not execute its setup, install packages or publish an app.

## Test before sharing

1. Add the repositories and revisions your template requires to YA in the
   documented order, and fetch them. Fix validation errors before proceeding.
2. Inspect the effective template and its source. Check that any intentional
   replacement comes from the expected layer.
3. Materialize a fresh project with the authoring tools, run its setup,
   build and tests, and exercise its intended browser interactions and add-ons.
   Review the composed instructions as well as the running application.
4. Repeat with access to the original source removed. Required instructions,
   skills, scripts and add-ons must still be available in the project.
5. Promote the template from `draft` to `ready` only after that review.

For a self-contained library, run the local authoring tools from the
`graehl/agents` repository root (Python 3.10+; setup needs Node.js 22.18+):

```sh
python3 project-templates/project-template.py validate --json
python3 project-templates/project-template.py inspect --template app-canvas --pretty
python3 project-templates/project-template.py create --template app-canvas \
  --target /path/to/new-project --name "My canvas" \
  --description "An interactive idea to build" --allow-draft --setup --json
```

The target must not exist and its parent must exist. `--allow-draft` permits
local testing before content review. Omit `--setup` to materialize files
without executing template code. With it, setup installs the pinned packages
and runs the template's verification. Failed setup retains the target and
logs for inspection. In the generated project, `npm run preview` serves the
starter, and `npm run server:add` installs the included optional backend.

The tools document their other commands with `project-template.py --help`;
they validate one self-contained library. Use YA's combined-source validation
for a community library that depends on bases from another source. See
[FORMAT.md](https://github.com/graehl/agents/blob/master/project-templates/FORMAT.md)
for the detailed manifest reference.

Share your GitHub directory URL, tested revision and required source order.
Include the tested YA-default commit when your template relies on its
bases. This lets another person reproduce your starter instead of guessing
which changing branch version you used.

This guide is maintained in YA at `topics/project-template-authoring.md`.
`graehl/agents/project-templates/README.md` is a synchronized copy; its
`VENDORED.md` records the source revision and how to refresh it.
