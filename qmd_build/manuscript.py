"""Manuscript facts shared by the qmd build tools: config, includes, assets."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

INCLUDE = re.compile(r"\{\{< include ([^ ]+) >\}\}")
RASTER_OR_PRINT = {".pdf", ".png", ".jpg", ".jpeg"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Config:
    """A JSON build config whose relative paths resolve against its directory.

    A tool that runs without a config file gets an empty one based at the
    current directory, so every setting falls back to its documented default.
    """

    def __init__(self, data: dict, base: Path, source: Path | None, allowed: set[str]):
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(
                f"Unknown config keys {sorted(unknown)}; allowed: {sorted(allowed)}"
            )
        self.data, self.base, self.source = data, base, source

    @classmethod
    def load(cls, path: Path | None, allowed: set[str]) -> Config:
        if path is None:
            return cls({}, Path.cwd(), None, allowed)
        path = path.resolve()
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            raise ValueError(f"Config must be a JSON object: {path}")  # noqa: TRY004 -- bad input file, not a caller type error
        return cls(data, path.parent, path, allowed)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def path(self, key: str) -> Path | None:
        value = self.data.get(key)
        return None if value is None else (self.base / value).resolve()

    def paths(self, key: str) -> list[Path]:
        return [(self.base / value).resolve() for value in self.data.get(key, [])]


def root_document(config: Config, positional: Path | None) -> Path:
    root = positional.resolve() if positional else config.path("root")
    if root is None:
        raise ValueError("Name the root .qmd as an argument or as config key `root`")
    if not root.is_file():
        raise ValueError(f"Root document not found: {root}")
    return root


def includes(root: Path, *, required: bool = True) -> list[str]:
    """Section fragments in the root's explicit include order.

    With `required=False` a root without includes is one self-contained
    document and yields an empty list.
    """
    names = INCLUDE.findall(root.read_text())
    if (required and not names) or len(names) != len(set(names)):
        raise ValueError(f"Expected distinct explicit include directives in {root}")
    return names


def first_heading_text(path: Path) -> str | None:
    """Plain text of the first ATX level-1 heading, for a page title."""
    match = re.search(r"^# +(.+?)\s*(?:\{[^}]*\})?\s*$", path.read_text(), re.MULTILINE)
    return None if match is None else re.sub(r"[*_`]", "", match[1])


def fragment_anchors(sections: list[Path], quarto: str) -> dict[str, str]:
    """Each included fragment's file name -> the id of its first heading.

    Lets links between fragments resolve inside the one rendered document.
    """
    anchors = {}
    for section in sections:
        if section.name in anchors:
            raise ValueError(f"Included fragments share a file name: {section.name}")
        parsed = json.loads(
            subprocess.check_output(
                [
                    quarto,
                    "pandoc",
                    str(section),
                    "--from",
                    "commonmark_x",
                    "--to",
                    "json",
                ],
                text=True,
            )
        )
        header = next((b for b in parsed["blocks"] if b["t"] == "Header"), None)
        if header is None:
            raise ValueError(f"Included fragment has no heading: {section}")
        anchors[section.name] = header["c"][1][0]
    return anchors


def front_matter(root: Path, key: str) -> str | None:
    """A scalar from the root's leading YAML block; quoted or bare."""
    match = re.match(r"---\n(.*?)\n---\n", root.read_text(), re.DOTALL)
    if not match:
        return None
    value = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", match[1], re.MULTILINE)
    if not value:
        return None
    text = value[1]
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1]
    return text


def print_asset(target: str, directories: list[Path]) -> Path | None:
    """The file a LaTeX build places for an image link, searched like Quarto's
    resource path; SVG and extensionless links select the matched PDF."""
    if "://" in target or target.startswith(("#", "data:")):
        return None
    link = Path(target)
    if link.suffix.lower() == ".svg":
        link = link.with_suffix(".pdf")
    elif link.suffix.lower() not in RASTER_OR_PRINT:
        link = link.with_name(link.name + ".pdf")
    for directory in directories:
        candidate = directory / link
        if candidate.is_file():
            return candidate.resolve()
    return None


def resolve_executable(name: str) -> str:
    found = shutil.which(name)
    if found is None:
        raise ValueError(f"Executable not found: {name}")
    return str(Path(found).absolute())
