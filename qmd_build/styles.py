"""Named qmd-html document styles, found by name on a style search path.

A style is a directory `<name>/` holding `style.json` and the files it names.
A document names its style in front matter (`document-style: memo`), so a
shared repository carries only the name; the build resolves it from, in
order, the directories in `QMD_STYLE_PATH` (`:`-separated), the user's
`~/.config/qmd-html/styles`, and the styles shipped with this package.

`style.json` keys: `css` (required); `font-families` (registered in
`fonts.FACES`, embedded); `filters` (Lua filters, resolved in the style
directory, then this package); `toc`; `table-widths` (build-time column
widths, `table_layout.py`); `document-corner` (a quiet top-right "rev N ·
date" and, with a printed PDF, a link to it); `print` (default Chromium print options). A style layers over
Quarto's default HTML theme, so headings drive the right-hand outline.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from .fonts import family_faces, font_face_css, font_file

PACKAGE = Path(__file__).resolve().parent
STYLE_PATH_ENV = "QMD_STYLE_PATH"
USER_STYLES = Path.home() / ".config/qmd-html/styles"
BUILTIN_STYLES = PACKAGE / "styles"
CORNER_FILTER = PACKAGE / "document_corner.lua"
MANIFEST_KEYS = {
    "comment",
    "css",
    "font-families",
    "filters",
    "toc",
    "table-widths",
    "document-corner",
    "print",
}


@dataclass(frozen=True)
class DocumentStyle:
    name: str
    directory: Path
    css: Path
    faces: list[tuple[str, int, str]]
    filters: list[Path] = field(default_factory=list)
    toc: bool = True
    table_widths: bool = False
    document_corner: bool = False
    print_options: dict = field(default_factory=dict)


def style_search_path() -> list[Path]:
    configured = os.environ.get(STYLE_PATH_ENV, "")
    return [Path(p).expanduser() for p in configured.split(":") if p] + [
        USER_STYLES,
        BUILTIN_STYLES,
    ]


def _style_file(name: str, directory: Path, relative: str) -> Path:
    for base in (directory, PACKAGE):
        candidate = (base / relative).resolve()
        if candidate.is_file():
            return candidate
    raise ValueError(f"Style {name!r} names a missing file: {relative}")


def document_style(name: str) -> DocumentStyle:
    """Load the first style directory named `name` on the search path."""
    search = style_search_path()
    manifest = next(
        (
            d / name / "style.json"
            for d in search
            if (d / name / "style.json").is_file()
        ),
        None,
    )
    if manifest is None:
        raise ValueError(
            f"Unknown document style {name!r}; searched {[str(d) for d in search]}"
        )
    spec = json.loads(manifest.read_text())
    unknown = set(spec) - MANIFEST_KEYS
    if unknown or "css" not in spec:
        raise ValueError(
            f"Style manifest {manifest} needs `css`; unknown keys {sorted(unknown)}"
        )
    directory = manifest.parent
    return DocumentStyle(
        name=name,
        directory=directory,
        css=_style_file(name, directory, spec["css"]),
        faces=[
            f for family in spec.get("font-families", []) for f in family_faces(family)
        ],
        filters=[_style_file(name, directory, f) for f in spec.get("filters", [])],
        toc=spec.get("toc", True),
        table_widths=spec.get("table-widths", False),
        document_corner=spec.get("document-corner", False),
        print_options=spec.get("print", {}),
    )


def style_render_arguments(style: DocumentStyle, workdir: Path) -> list[str]:
    """Quarto render arguments for `style`; writes its font CSS into `workdir`."""
    arguments = []
    if style.faces:
        fonts = workdir / "style-fonts.css"
        fonts.write_text(font_face_css(style.faces, embed=False) + "\n")
        arguments += ["--css", str(fonts)]
    arguments += ["--css", str(style.css)]
    for lua in style.filters:
        arguments += ["--lua-filter", str(lua)]
    return arguments + (["--toc"] if style.toc else [])


def corner_arguments() -> list[str]:
    """Quarto arguments for the revision/PDF corner (env QMD_PDF_LINK)."""
    return ["--lua-filter", str(CORNER_FILTER)]


def style_inputs(style: DocumentStyle) -> list[Path]:
    """Files whose hashes belong in the build receipt."""
    return [
        style.directory / "style.json",
        style.css,
        *style.filters,
        *([CORNER_FILTER] if style.document_corner else []),
        *(font_file(*face) for face in style.faces),
    ]
