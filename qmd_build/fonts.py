"""OpenType faces embedded in self-contained HTML and its browser-print PDF.

Faces resolve from the host's TeX Live OpenType tree, so HTML, print, and
LaTeX builds share one set of font files and their hashes enter receipts.
"""

from __future__ import annotations

import base64
from pathlib import Path

OPENTYPE = Path.home() / ".local/texlive/texmf-dist/fonts/opentype"

# (family, weight, style) -> path below OPENTYPE
FACES = {
    ("Source Sans 3", 400, "normal"): "adobe/sourcesans/SourceSans3-Regular.otf",
    ("Source Sans 3", 400, "italic"): "adobe/sourcesans/SourceSans3-RegularIt.otf",
    ("Source Sans 3", 600, "normal"): "adobe/sourcesans/SourceSans3-Semibold.otf",
    ("Source Sans 3", 700, "normal"): "adobe/sourcesans/SourceSans3-Bold.otf",
    ("Source Sans 3", 700, "italic"): "adobe/sourcesans/SourceSans3-BoldIt.otf",
    ("Roboto", 700, "normal"): "google/roboto/Roboto-Bold.otf",
}


def font_file(family: str, weight: int, style: str = "normal") -> Path:
    """The OpenType file for one registered face; missing files fail loudly."""
    key = (family, weight, style)
    if key not in FACES:
        raise ValueError(
            f"Unregistered font face {key}; add it to qmd_build.fonts.FACES"
        )
    path = OPENTYPE / FACES[key]
    if not path.is_file():
        raise ValueError(f"Font file missing for {key}: {path}")
    return path


def family_faces(family: str) -> list[tuple[str, int, str]]:
    return [key for key in FACES if key[0] == family]


def font_face_css(faces: list[tuple[str, int, str]], *, embed: bool = True) -> str:
    """`@font-face` rules for registered faces.

    `embed` inlines each file as a base64 data URI for hand-built HTML; with
    `embed=False` the rule names the absolute file, for renderers such as
    Quarto's `--embed-resources` that inline CSS `url()` targets themselves.
    """
    rules = []
    for family, weight, style in faces:
        path = font_file(family, weight, style)
        source = (
            "data:font/otf;base64," + base64.b64encode(path.read_bytes()).decode()
            if embed
            else str(path)
        )
        rules.append(
            f'@font-face{{font-family:"{family}";font-weight:{weight};'
            f'font-style:{style};src:url("{source}") format("opentype")}}'
        )
    return "\n".join(rules)
