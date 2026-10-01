"""Named qmd-html document styles: CSS, embedded faces, outline, print page.

A style layers over Quarto's default HTML theme, so headings still drive the
right-hand outline whether the root is one Markdown file or includes
fragments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .fonts import family_faces, font_face_css, font_file

PACKAGE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class DocumentStyle:
    css: Path
    faces: list[tuple[str, int, str]]
    filters: list[Path] = field(default_factory=list)
    toc: bool = True
    # Choose responsive table column widths at build time (table_layout.py).
    table_widths: bool = False
    print_options: dict = field(default_factory=dict)


STYLES = {
    "memo": DocumentStyle(
        css=PACKAGE / "styles/memo.css",
        faces=family_faces("Source Sans 3"),
        filters=[PACKAGE / "styles/table_tokens.lua"],
        table_widths=True,
        print_options={
            "format": "Letter",
            "margin": {
                "top": "0.7in",
                "bottom": "0.7in",
                "left": "0.75in",
                "right": "0.75in",
            },
        },
    ),
}


def document_style(name: str) -> DocumentStyle:
    if name not in STYLES:
        raise ValueError(f"Unknown document style {name!r}; known: {sorted(STYLES)}")
    return STYLES[name]


def style_render_arguments(style: DocumentStyle, workdir: Path) -> list[str]:
    """Quarto render arguments for `style`; writes its font CSS into `workdir`."""
    fonts = workdir / "style-fonts.css"
    fonts.write_text(font_face_css(style.faces, embed=False) + "\n")
    arguments = ["--css", str(fonts), "--css", str(style.css)]
    for lua in style.filters:
        arguments += ["--lua-filter", str(lua)]
    return arguments + (["--toc"] if style.toc else [])


def style_inputs(style: DocumentStyle) -> list[Path]:
    """Files whose hashes belong in the build receipt."""
    return [style.css, *style.filters, *(font_file(*face) for face in style.faces)]
