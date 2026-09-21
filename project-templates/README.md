# Project templates

A composable inventory for standing up projects and supplying portable agent
instructions, with TypeScript App canvas and content-led Web page starters,
each carrying an optional server.

**Status: runnable authoring version; YA integration remains unimplemented.**
The library has a local validator/materializer, shared capability bases, two
scripted starters, and a vendored server add-on. Manifests remain `draft`
pending the instruction review tracked in the
[first program gap](gaps/portable-capability-bases.md); the authoring CLI's
explicit `--allow-draft` permits testing them. The wholesale boot reference is
retained separately as `legacy-boot` and is not inherited by App canvas.

## Layout

```text
project-templates/
  PROGRAM.md                       durable purpose and boundaries
  GLOSSARY.md                      local vocabulary
  FORMAT.md                        composition and vendoring contract
  library.json                     explicit inventory
  bases/
    base/                          universal project/documentation guidance
    software-engineering/          code structure and change boundaries
    testing/                       behavioral verification
    typescript/                    language guidance and compiler settings
    web-ui/                        responsive UI and browser verification
    web-app/                       shared Vite setup, preview and preparation
    canvas/                        drawing app and Canvas2D conventions
    server/                        inactive, vendored backend add-on
    legacy-boot/
      boot.md -> ../../../AGENTS.global.md
  templates/
    app-canvas/
      template.json                selected bases and app-specific files
      files/                       canvas-specific browser checks
    web-page/                      content-led DOM starter and behavior checks
  composition.py                   local source validation and file union
  project-template.py              acli authoring entry point
  gaps/
    portable-capability-bases.md   first program gap
```

Additional bases belong beside `base`, each with a `template.json` and its
referenced files. Their editorial refinement is part of the gap.
Scripts live with the capability they stand up. Source symlinks are optional
navigation aids; configuration specifies what enters the project.

The universal base includes the project-visible **redoc** skill for autonomous
documentation maintenance and a starter SVG brand. Redoc reorganizes docs for
human/agent readability and truth against current contents. It respects exact
YA-UI identity text in a root `.project-identity.json`, if a deliberate later
human edit created one; initial creation intent does not create that marker.
YA's write path for the marker is still pending in its identity integration gap.

Starter application modules live at project root, tests in `tests/`, and
helpers in `scripts/`. No empty directories are scaffolded. Before fixing
default topic/plan/issue locations, resolve the broader
[document-convention convergence gap](../gaps/project-document-convention-convergence.md).

Read [PROGRAM.md](PROGRAM.md) for scope and [FORMAT.md](FORMAT.md) before
authoring a manifest or implementing a consumer. `library.json` is a content
inventory, not YA's server-settings schema.

## Authoring commands

From the source repository root, with Python 3.10+ and Node.js 22.18+:

```sh
python3 project-templates/project-template.py validate --json
python3 project-templates/project-template.py inspect --template app-canvas --pretty
python3 project-templates/project-template.py create --template app-canvas \
  --target /path/to/new-project --name "My canvas" \
  --description "An interactive idea to build" --allow-draft --setup --json
python3 -m unittest discover -s project-templates -p 'test_*.py'
```

The target must not exist and its parent must exist. Creation writes ordinary
files and a `.project-template/project.json` containing intent and source
hashes; `--setup` executes the configured argv from `.project-template/app.json`.
Only admit trusted template sources: setup is code execution, not a sandbox.
Failures retain the partial target and its setup logs. There is no implicit
retry, cleanup, Git initialization, registration, or agent turn. Those YA
orchestration steps remain for integration after mockup approval.

Without `--setup`, materialization is offline and executes no template code.
With it, `npm ci` installs the pinned lockfile, then typechecks, tests, and builds.
In the created project, `npm run preview` prints its loopback URL; stop that
owned process when finished. `npm run server:add` enables `npm start`, adds
server checks, and changes the vendored app metadata from static to server.
It refuses an existing backend instead of overwriting it. The authoring CLI
uses this repository's shared `acli` Python library; generated projects need
neither Python nor that library.

The app's display name is **App canvas** and its stable template ID is
**`app-canvas`**: the name describes the workspace rather than committing the
project to a particular game. Static hosting is the default; the server base
vendors an optional capability without running it. No publication target is
preconfigured. See the vendored `instructions/run-deploy.md` for deployment.

**Web page** (`web-page`) is a content-led DOM page for documents, stories and
collections. Its starter has searchable/filterable cards and responsive layout;
it does not inherit canvas instructions. Interactivity and multimedia remain
available when they serve the reader. Both templates inherit `web-app` for
their tooling and setup, and can activate the same vendored server later.
Use `--template web-page` in the authoring commands to create one.

Optional writing/worldbuilding guidance and concise GitHub Pages/account/domain
onboarding are tracked in the
[content-authoring capability gap](gaps/content-authoring-capabilities.md).
Static publishing should default to a host-provided URL; a custom domain is
optional. That publishing capability is shared by both kinds of project.

## Approved delivery sequence

1. Commit the representation, charter, first gap, and runnable template content
   under `~/agents` (content implementation was explicitly brought forward).
2. Produce YA mockups and discuss them for approval.
3. Update YA's owning topic with the approved design, then implement the
   YA integration, resolving the instruction gap
   before a template is offered for project creation.

YA mockups are under review; its topics and gaps now track the product contract.
Both starters are static Vite + TypeScript, with an optional server add-on
vendored for later application.
Creation should expose the deterministic starter as soon as feasible, then
automatically send a verify/prepare turn containing the UI-entered intent.
Preparation customizes `AGENTS.md`, writes a useful README lede, verifies
run/test/build, and stops ready to implement the requested app. An early
visible starter is not proof that preparation succeeded; YA must show failures.

YA's New Project flow will offer From template alongside existing-directory
registration. Settings → Users will enforce None / Selected templates / Any
configured template on the server. New limited users default to App canvas;
exactly one allowed template applies automatically. None prevents creation;
Any includes templates configured later. An unavailable or draft default must
not silently select a different template. Parent-directory restrictions and
the existing limited-user execution boundary still apply.

YA's product contracts remain in its `topics/project-templates.md` and
`topics/limited-users.md`. The sequence above preserves this request's agreed
scope until those documents are updated after mockup approval.
