"""Image preparation policy at the session delivery boundary."""

from __future__ import annotations

from pathlib import Path

# Pillow allocates the full decoded frame; refuse sources whose header
# promises more than this before decoding, as the old ImageMagick limits did.
MAX_SOURCE_PIXELS = 64 * 1024 * 1024
SAVE_FORMATS = {
    "image/png": "PNG",
    "image/jpeg": "JPEG",
    "image/webp": "WEBP",
    "image/gif": "PNG",
}


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
    if mime not in SAVE_FORMATS:
        return {"size": path.stat().st_size, "mimeType": mime}
    # Imported here so session-turn, which shares this module through
    # rendezvous, keeps running on a plain interpreter without Pillow.
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise RuntimeError(
            "Image preparation requires Pillow; run rendez through its uv script header"
        ) from exc
    with Image.open(path) as image:
        width, height = image.size
        if width * height > MAX_SOURCE_PIXELS:
            raise RuntimeError(f"Image is too large to prepare: {width}x{height}")
        edge = profile["maxLongEdge"]
        if max(width, height) <= edge and path.stat().st_size <= profile["maxBytes"]:
            return {
                "width": width,
                "height": height,
                "size": path.stat().st_size,
                "mimeType": mime,
            }
        # JPEG only: libjpeg decodes at the smallest 1/2^k scale that still
        # covers the target, which every later, smaller retry edge also fits.
        image.draft(None, (edge, edge))
        source = ImageOps.exif_transpose(image)
    output = path.with_name(
        ".prepared.png" if mime == "image/gif" else ".prepared" + path.suffix
    )
    save_format = SAVE_FORMATS[mime]
    if save_format == "JPEG" and source.mode not in {"RGB", "L", "CMYK"}:
        source = source.convert("RGB")
    for _ in range(12):
        prepared = source.copy()
        prepared.thumbnail((edge, edge), Image.Resampling.LANCZOS)
        prepared.save(output, format=save_format, quality=profile["quality"])
        if output.stat().st_size <= profile["maxBytes"]:
            break
        edge = max(32, int(edge * 0.8))
    else:
        raise RuntimeError("Image preparation could not satisfy the adapter byte limit")
    width, height = prepared.size
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
