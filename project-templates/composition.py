"""Resolve a template library into a portable, deterministic file tree."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path, PurePosixPath


def exact_fields(
    value: dict, required: set[str], optional: set[str] = frozenset()
) -> None:
    if (
        not isinstance(value, dict)
        or not required <= value.keys()
        or value.keys() - required - optional
    ):
        raise ValueError(
            f"Template fields must be {sorted(required)}; optional {sorted(optional)}"
        )


def project_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"Invalid project path: {value!r}")
    parts = value.split("/")
    if any(
        part.casefold() in {"", ".", "..", ".git"} or part.endswith((".", " "))
        for part in parts
    ):
        raise ValueError(f"Invalid project path: {value!r}")
    if any(
        re.fullmatch(r"(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?", part)
        for part in parts
    ):
        raise ValueError(f"Nonportable project path: {value!r}")
    return value


@dataclass(frozen=True)
class Contribution:
    content: bytes
    executable: bool
    source: str

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.content).hexdigest()


@dataclass
class Composition:
    template: dict
    order: list[str]
    files: dict[str, Contribution]
    contributors: dict[str, list[str]]

    def describe(self) -> dict:
        return {
            "template": self.template["id"],
            "status": self.template["status"],
            "order": self.order,
            "files": [
                {
                    "path": path,
                    "sha256": item.digest,
                    "bytes": len(item.content),
                    "executable": item.executable,
                    "sources": self.contributors[path],
                }
                for path, item in sorted(self.files.items())
            ],
        }


class TemplateLibrary:
    def __init__(self, repository: Path, content_path: str) -> None:
        self.repository = repository.resolve(strict=True)
        self.root = self.source(self.repository, project_path(content_path))
        inventory = self.read_json(self.root, "library.json")
        exact_fields(inventory, {"formatVersion", "bases", "templates"})
        if inventory["formatVersion"] != 1:
            raise ValueError("Unsupported template library version")
        self.nodes: dict[str, dict] = {}
        self.directories: dict[str, Path] = {}
        for kind, group in (("base", "bases"), ("template", "templates")):
            if not isinstance(inventory[group], list):
                raise TypeError(f"Template inventory {group} must be an array")
            for identifier in inventory[group]:
                if not isinstance(identifier, str) or not re.fullmatch(
                    r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", identifier
                ):
                    raise ValueError(f"Invalid template identifier: {identifier!r}")
                if identifier in self.nodes or (
                    identifier == "base" and kind != "base"
                ):
                    raise ValueError(
                        f"Duplicate or reserved template identifier: {identifier}"
                    )
                directory = self.root / group / identifier
                node = self.read_json(directory, "template.json")
                exact_fields(
                    node,
                    {
                        "formatVersion",
                        "kind",
                        "status",
                        "id",
                        "title",
                        "description",
                        "extends",
                        "files",
                        "overrides",
                    },
                )
                if (
                    node["formatVersion"] != 1
                    or node["kind"] != kind
                    or node["id"] != identifier
                    or node["status"] not in {"draft", "ready"}
                ):
                    raise ValueError(f"Invalid template manifest: {identifier}")
                for field in ("title", "description"):
                    if not isinstance(node[field], str) or not node[field].strip():
                        raise ValueError(f"Invalid {field}: {identifier}")
                for field in ("extends", "files", "overrides"):
                    if not isinstance(node[field], list):
                        raise TypeError(
                            f"Template {field} must be an array: {identifier}"
                        )
                if kind == "base" and node["overrides"]:
                    raise ValueError(
                        f"Base cannot apply template overrides: {identifier}"
                    )
                self.nodes[identifier] = node
                self.directories[identifier] = directory
        for identifier, node in self.nodes.items():
            if any(
                not isinstance(base, str)
                or base not in self.nodes
                or self.nodes[base]["kind"] != "base"
                for base in node["extends"]
            ):
                raise ValueError(f"Unknown base in {identifier}")
            if len(set(node["extends"])) != len(node["extends"]):
                raise ValueError(f"Repeated base in {identifier}")
        for identifier, node in self.nodes.items():
            self.order(identifier)
            for entry in node["files"]:
                self.read_entry(identifier, entry)
            for entry in node["overrides"]:
                self.read_entry(identifier, entry, override=True)
        for identifier, node in self.nodes.items():
            if node["kind"] == "template":
                self.compose(identifier)

    def source(self, directory: Path, value: str) -> Path:
        if (
            not isinstance(value, str)
            or not value
            or "\\" in value
            or ":" in value
            or PurePosixPath(value).is_absolute()
        ):
            raise ValueError(f"Invalid template source: {value!r}")
        lexical = directory / value
        path = lexical.resolve(strict=True)
        if (
            not path.is_relative_to(self.repository)
            or ".git" in path.relative_to(self.repository).parts
            or ".git" in lexical.parts
        ):
            raise ValueError(f"Template source escapes repository: {value}")
        return path

    def read_json(self, directory: Path, value: str) -> dict:
        return json.loads(self.source(directory, value).read_text(encoding="utf-8"))

    def order(self, identifier: str) -> list[str]:
        edges: dict[str, set[str]] = {}

        def visit(name: str) -> None:
            if name in edges:
                return
            edges[name] = set()
            bases = self.nodes[name]["extends"]
            for base in bases:
                visit(base)
                edges[base].add(name)
            for left, right in pairwise(bases):
                edges[left].add(right)

        visit(identifier)
        incoming = dict.fromkeys(edges, 0)
        for children in edges.values():
            for child in children:
                incoming[child] += 1
        result = []
        while len(result) < len(edges):
            ready = next((name for name, count in incoming.items() if count == 0), None)
            if ready is None:
                raise ValueError(
                    f"Conflicting base order or cycle: {', '.join(incoming)}"
                )
            result.append(ready)
            del incoming[ready]
            for child in edges[ready]:
                incoming[child] -= 1
        return result

    def read_entry(
        self, name: str, entry: dict, override: bool = False
    ) -> tuple[str, Contribution | None]:
        if override:
            if not isinstance(entry, dict) or entry.get("op") not in {
                "replace",
                "append",
                "prepend",
                "omit",
            }:
                raise ValueError(f"Invalid template override: {name}")
            operation = entry["op"]
            required = {"op", "to"} if operation == "omit" else {"op", "to", "from"}
            optional = {"executable"} if operation == "replace" else set()
        else:
            operation, required, optional = "replace", {"to", "from"}, {"executable"}
        exact_fields(entry, required, optional)
        destination = project_path(entry["to"])
        if operation == "omit":
            return destination, None
        executable = entry.get("executable", False)
        if type(executable) is not bool:
            raise ValueError(f"Invalid executable flag: {name}/{destination}")
        source = self.source(self.directories[name], entry["from"])
        if not source.is_file():
            raise ValueError(f"Template source is not a file: {source}")
        content = source.read_bytes()
        if destination == "AGENTS.md" or operation in {"append", "prepend"}:
            content.decode("utf-8", errors="strict")
            if b"\0" in content or (destination == "AGENTS.md" and executable):
                raise ValueError(f"Invalid instruction text: {name}/{destination}")
        return destination, Contribution(
            content, executable, source.relative_to(self.repository).as_posix()
        )

    def compose(self, identifier: str) -> Composition:
        if identifier not in self.nodes or self.nodes[identifier]["kind"] != "template":
            raise ValueError(f"Unknown project template: {identifier}")
        node = self.nodes[identifier]
        order = self.order(identifier)
        if node["status"] == "ready" and any(
            self.nodes[name]["status"] != "ready" for name in order
        ):
            raise ValueError(f"Ready template inherits draft base: {identifier}")
        files: dict[str, Contribution] = {}
        contributors: dict[str, list[str]] = {}
        conflicts: set[str] = set()
        instruction_hashes: set[str] = set()
        for name in order:
            for entry in self.nodes[name]["files"]:
                destination, item = self.read_entry(name, entry)
                assert item is not None
                contributors.setdefault(destination, []).append(item.source)
                previous = files.get(destination)
                if destination == "AGENTS.md":
                    if item.digest in instruction_hashes:
                        continue
                    instruction_hashes.add(item.digest)
                    if previous:
                        item = Contribution(
                            join_text(previous.content, item.content, 2),
                            False,
                            item.source,
                        )
                elif previous and (
                    previous.content != item.content
                    or previous.executable != item.executable
                ):
                    conflicts.add(destination)
                files[destination] = item
        for entry in node["overrides"]:
            destination, item = self.read_entry(identifier, entry, override=True)
            operation = entry["op"]
            if destination in conflicts:
                if operation not in {"replace", "omit"}:
                    raise ValueError(f"Unresolved template conflict: {destination}")
                conflicts.remove(destination)
            if operation != "replace" and destination not in files:
                raise ValueError(
                    f"Template override needs existing file: {destination}"
                )
            if operation == "omit":
                del files[destination]
                del contributors[destination]
                continue
            assert item is not None
            if operation in {"append", "prepend"}:
                previous = files[destination]
                previous.content.decode("utf-8", errors="strict")
                if b"\0" in previous.content:
                    raise ValueError(f"Cannot edit binary text: {destination}")
                left, right = (
                    (previous.content, item.content)
                    if operation == "append"
                    else (item.content, previous.content)
                )
                item = Contribution(
                    join_text(left, right, 1), previous.executable, item.source
                )
            files[destination] = item
            contributors.setdefault(destination, []).append(item.source)
        if conflicts:
            details = {path: contributors[path] for path in sorted(conflicts)}
            raise ValueError(f"Template file conflicts: {details}")
        portable: dict[str, str] = {}
        for path in sorted(files):
            folded = path.casefold()
            if folded in portable:
                raise ValueError(f"Template path collision: {path}, {portable[folded]}")
            portable[folded] = path
        for path in portable:
            if any(
                parent.as_posix() in portable
                for parent in PurePosixPath(path).parents
                if parent.as_posix() != "."
            ):
                raise ValueError(f"Template file/directory collision: {path}")
        return Composition(node, order, files, contributors)


def join_text(left: bytes, right: bytes, newlines: int) -> bytes:
    if not left or not right:
        return left + right
    trailing = len(left) - len(left.rstrip(b"\n"))
    leading = len(right) - len(right.lstrip(b"\n"))
    return left + b"\n" * max(0, newlines - trailing - leading) + right


def materialize(
    composition: Composition, target: Path, name: str, description: str
) -> Path:
    """Create a fresh project; failures retain its partial tree for diagnosis."""
    if not name.strip() or not description.strip():
        raise ValueError("Project name and description must be nonempty")
    if any(
        path.casefold() in {".project-template", ".project-template/project.json"}
        or path.casefold().startswith(".project-template/project.json/")
        for path in composition.files
    ):
        raise ValueError("Reserved project context destination")
    target = target.absolute()
    target.mkdir()
    for destination, item in composition.files.items():
        output = target / destination
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(item.content)
        output.chmod(0o755 if item.executable else 0o644)
    context = target / ".project-template/project.json"
    context.parent.mkdir(parents=True, exist_ok=True)
    context.write_text(
        json.dumps(
            {
                "name": name,
                "description": description,
                "origin": composition.describe(),
            },
            indent=2,
        )
        + "\n"
    )
    return target
