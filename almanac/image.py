"""Terminal image display with a structured fallback at the CLI boundary."""

from __future__ import annotations

import base64
import mimetypes
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

RENDERERS = ("auto", "none", "kitty", "iterm2", "sixel", "chafa", "viu", "timg")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass(frozen=True)
class DisplayResult:
    rendered: bool
    renderer: str | None
    reason: str | None = None


def mime_type(path: Path) -> str:
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def detect_renderer(
    env: Mapping[str, str] | None = None,
    *,
    which=shutil.which,
) -> str | None:
    env = os.environ if env is None else env
    term = env.get("TERM", "").lower()
    term_program = env.get("TERM_PROGRAM", "").lower()
    if (
        env.get("KITTY_WINDOW_ID")
        or env.get("WEZTERM_PANE")
        or "kitty" in term
        or term_program in {"kitty", "wezterm", "ghostty"}
    ):
        return "kitty"
    if term_program in {"iterm.app", "iterm2"} or env.get("LC_TERMINAL") == "iTerm2":
        return "iterm2"
    if which("img2sixel") and ("sixel" in term or env.get("ALMANAC_SIXEL") == "1"):
        return "sixel"
    for helper in ("chafa", "viu", "timg"):
        if which(helper):
            return helper
    return None


def _write_kitty(path: Path, width: int, out: BinaryIO) -> DisplayResult:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        return DisplayResult(False, "kitty", "Kitty direct rendering requires PNG")
    encoded = base64.standard_b64encode(data)
    chunks = [encoded[index : index + 4096] for index in range(0, len(encoded), 4096)]
    for index, chunk in enumerate(chunks):
        more = int(index + 1 < len(chunks))
        params = f"a=T,f=100,t=d,q=2,c={width},m={more}" if index == 0 else f"m={more}"
        out.write(b"\x1b_G" + params.encode() + b";" + chunk + b"\x1b\\")
    out.write(b"\n")
    return DisplayResult(True, "kitty")


def _write_iterm2(path: Path, width: int, out: BinaryIO) -> DisplayResult:
    data = path.read_bytes()
    name = base64.standard_b64encode(path.name.encode()).decode()
    params = (
        f"name={name};size={len(data)};width={width};inline=1;preserveAspectRatio=1"
    )
    out.write(
        b"\x1b]1337;File="
        + params.encode()
        + b":"
        + base64.standard_b64encode(data)
        + b"\x07\n"
    )
    return DisplayResult(True, "iterm2")


def _run_helper(path: Path, renderer: str, out: BinaryIO) -> DisplayResult:
    executable = "img2sixel" if renderer == "sixel" else renderer
    resolved = shutil.which(executable)
    if not resolved:
        return DisplayResult(
            False, renderer, f"renderer executable {executable!r} not found"
        )
    proc = subprocess.run([resolved, str(path)], capture_output=True, check=False)
    if proc.returncode:
        detail = proc.stderr.decode(errors="replace").strip()
        reason = f"{renderer} exited {proc.returncode}"
        if detail:
            reason += f": {detail[-300:]}"
        return DisplayResult(False, renderer, reason)
    out.write(proc.stdout)
    if not proc.stdout.endswith(b"\n"):
        out.write(b"\n")
    return DisplayResult(True, renderer)


def display_image(
    path: Path,
    *,
    renderer: str = "auto",
    width: int = 40,
    out: BinaryIO | None = None,
    is_tty: bool | None = None,
    env: Mapping[str, str] | None = None,
) -> DisplayResult:
    """Display ``path`` when stdout is a capable TTY; otherwise explain why."""
    if renderer not in RENDERERS:
        raise ValueError(f"renderer must be one of {RENDERERS}")
    if width < 1:
        raise ValueError("width must be positive")
    if out is None:
        out = sys.stdout.buffer
    if is_tty is None:
        is_tty = sys.stdout.isatty()
    if not is_tty:
        return DisplayResult(False, None, "stdout is not a terminal")
    if renderer == "none":
        return DisplayResult(False, None, "rendering disabled by --renderer none")
    selected = detect_renderer(env) if renderer == "auto" else renderer
    if selected is None:
        return DisplayResult(
            False,
            None,
            "no supported inline-image protocol or renderer detected",
        )
    if selected == "kitty":
        result = _write_kitty(path, width, out)
    elif selected == "iterm2":
        result = _write_iterm2(path, width, out)
    else:
        result = _run_helper(path, selected, out)
    if result.rendered and hasattr(out, "flush"):
        out.flush()
    return result
