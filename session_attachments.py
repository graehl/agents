"""Image preparation policy at the session delivery boundary."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def attachment_profile(target: dict, turn_api: dict) -> dict:
    # The portable policy is also the native-resume adapter's policy. Watchers
    # consume it without knowing model names or provider resizing rules.
    profile = {"maxLongEdge": 2000, "maxBytes": 4 * 1024 * 1024, "quality": 85}
    try:
        descriptor, token = turn_api["discover_provider_host"]()
        rows = turn_api["host_request"](descriptor, token, {"op": "inventory"})
    except turn_api["TransportFailure"]:
        return profile
    for row in rows:
        if (
            row.get("harness") == target["harness"]
            and row.get("providerSessionId") == target["providerSessionId"]
            and row.get("imagePreparationProfile") is not None
        ):
            profile = row["imagePreparationProfile"]
            break
    for key, maximum in (
        ("maxLongEdge", 6000),
        ("maxBytes", 64 * 1024 * 1024),
        ("quality", 100),
    ):
        value = profile.get(key)
        if not isinstance(value, int) or not 1 <= value <= maximum:
            raise ValueError(f"Invalid image preparation profile: {key}")
    return profile


def prepare_attachment(path: Path, mime: str, profile: dict) -> dict:
    if mime not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        return {"size": path.stat().st_size, "mimeType": mime}
    executable = shutil.which("magick")
    if not executable:
        raise RuntimeError("Image preparation requires ImageMagick's magick executable")
    limits = [
        "-limit",
        "memory",
        "128MiB",
        "-limit",
        "map",
        "256MiB",
        "-limit",
        "disk",
        "512MiB",
    ]
    result = subprocess.run(
        [executable, "identify", *limits, "-format", "%w %h", f"{path}[0]"],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    width, height = map(int, result.stdout.split())
    original_dimensions = {"width": width, "height": height}
    edge = profile["maxLongEdge"]
    if max(width, height) <= edge and path.stat().st_size <= profile["maxBytes"]:
        return {**original_dimensions, "size": path.stat().st_size, "mimeType": mime}
    output = path.with_name(
        ".prepared.png" if mime == "image/gif" else ".prepared" + path.suffix
    )
    for _ in range(12):
        subprocess.run(
            [
                executable,
                *limits,
                f"{path}[0]",
                "-auto-orient",
                "-resize",
                f"{edge}x{edge}>",
                "-strip",
                "-quality",
                str(profile["quality"]),
                str(output),
            ],
            capture_output=True,
            check=True,
            timeout=30,
        )
        if output.stat().st_size <= profile["maxBytes"]:
            break
        edge = max(32, int(edge * 0.8))
    else:
        raise RuntimeError("Image preparation could not satisfy the adapter byte limit")
    result = subprocess.run(
        [executable, "identify", "-format", "%w %h", str(output)],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    width, height = map(int, result.stdout.split())
    if mime == "image/gif":
        final = path.with_suffix(".png")
        output.replace(final)
        path.unlink()
        path = final
        mime = "image/png"
    else:
        output.replace(path)
    return {
        "width": width,
        "height": height,
        "size": path.stat().st_size,
        "mimeType": mime,
        "path": str(path),
        "profile": profile,
    }
