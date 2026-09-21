"""Authoring CLI; YA will later consume the same composition contract."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from composition import TemplateLibrary, materialize

import acli


def main() -> None:
    parser = acli.argument_parser(
        description="Validate, inspect, or create a template project. Create writes a fresh target; --setup installs/builds/tests there (usually under a minute). Result on stdout; child output is saved in the project. Failed partial targets are retained.",
        capabilities=(),
    )
    acli.add_standard_args(parser)
    parser.add_argument("action", choices=("validate", "inspect", "create"))
    parser.add_argument(
        "--repository", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--content-path", default="project-templates")
    parser.add_argument("--template", default="app-canvas")
    parser.add_argument("--target", type=Path)
    parser.add_argument("--name")
    parser.add_argument("--description")
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Authoring only: permit creation from a draft template.",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run the vendored setup script after materialization; executes trusted template code.",
    )
    args = parser.parse_args()
    try:
        output_format = acli.resolve_format(args)
        if args.action != "create" and (
            args.setup
            or args.target
            or args.name
            or args.description
            or args.allow_draft
        ):
            raise ValueError("Creation options require the create action")
        library = TemplateLibrary(args.repository, args.content_path)
        if args.action == "validate":
            result = {
                "ok": True,
                "templates": [
                    name
                    for name, node in library.nodes.items()
                    if node["kind"] == "template"
                ],
                "nodes": len(library.nodes),
            }
        else:
            composition = library.compose(args.template)
            result = composition.describe()
            if args.action == "create":
                if args.target is None or args.name is None or args.description is None:
                    raise ValueError(
                        "Create requires --target, --name, and --description"
                    )
                if composition.template["status"] != "ready" and not args.allow_draft:
                    raise ValueError(
                        "Draft template cannot create projects without authoring --allow-draft"
                    )
                setup_command = None
                if args.setup:
                    app_file = composition.files.get(".project-template/app.json")
                    if app_file is None:
                        raise ValueError("Template has no .project-template/app.json")
                    app = json.loads(app_file.content)
                    setup_command = app.get("setup") if isinstance(app, dict) else None
                    if (
                        not isinstance(setup_command, list)
                        or not setup_command
                        or any(
                            not isinstance(arg, str) or not arg or "\0" in arg
                            for arg in setup_command
                        )
                    ):
                        raise ValueError("Template setup must be a nonempty argv array")
                target = materialize(
                    composition, args.target, args.name, args.description
                )
                result["target"] = str(target)
                if args.setup:
                    logs = target / ".project-template/logs"
                    logs.mkdir(parents=True, exist_ok=True)
                    with (
                        (logs / "setup.out").open("w") as stdout,
                        (logs / "setup.err").open("w") as stderr,
                    ):
                        subprocess.run(
                            setup_command,
                            cwd=target,
                            stdout=stdout,
                            stderr=stderr,
                            check=True,
                        )
                    result["setup"] = "passed"
        acli.emit(result, output_format)
    except (
        ValueError,
        TypeError,
        OSError,
        RuntimeError,
        subprocess.CalledProcessError,
    ) as exc:
        acli.die(str(exc), acli.ExitCode.DATA)


if __name__ == "__main__":
    main()
