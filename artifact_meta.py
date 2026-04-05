#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import json
from typing import Iterable


@dataclass(frozen=True)
class Sidecars:
    out: Path
    meta: Path
    log: Path


@dataclass(frozen=True)
class InputSpec:
    code: str
    path: Path


def sidecars_for_output(output: str | Path) -> Sidecars:
    out = Path(output)
    return Sidecars(out=out, meta=Path(f"{out}.meta.md"), log=Path(f"{out}.log"))


def shortest_relpath(target: str | Path, meta_path: str | Path) -> str:
    target_path = Path(target)
    base_dir = Path(meta_path).parent
    return os.path.relpath(target_path, start=base_dir)


def meta_candidates(path: str | Path) -> list[Path]:
    p = Path(path)
    if str(p).endswith(".meta.md"):
        return [p]
    return [Path(f"{p}.meta.md"), p.with_suffix(f"{p.suffix}.meta.md") if p.suffix else Path(f"{p}.meta.md")]


def find_input_meta(path: str | Path) -> Path | None:
    seen: set[Path] = set()
    for cand in meta_candidates(path):
        if cand in seen:
            continue
        seen.add(cand)
        if cand.exists():
            return cand
    return None


def read_text_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def excerpt_markdown(text: str, max_lines: int = 8, max_chars: int = 700) -> str:
    kept: list[str] = []
    in_code = False
    used = 0
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("# "):
            continue
        if not line.strip() and not kept:
            continue
        if not line.strip() and kept and kept[-1] == "":
            continue
        candidate = line[: max(0, max_chars - used)]
        if not candidate and kept:
            break
        kept.append(candidate)
        used += len(candidate) + 1
        if len(kept) >= max_lines or used >= max_chars:
            break
    while kept and kept[-1] == "":
        kept.pop()
    return "\n".join(kept)


def parse_keyvals(items: Iterable[str]) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"expected KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        parsed.append((key.strip(), value.strip()))
    return parsed


def sanitize_code(text: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in text.strip().lower())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "input"


def parse_input_specs(items: Iterable[str]) -> list[InputSpec]:
    specs: list[InputSpec] = []
    used: set[str] = set()
    for idx, item in enumerate(items, start=1):
        if "=" in item:
            raw_code, raw_path = item.split("=", 1)
            code = sanitize_code(raw_code)
            path = Path(raw_path.strip())
        else:
            path = Path(item)
            stem = path.name
            if stem.endswith(".meta.md"):
                stem = stem[: -len(".meta.md")]
            elif "." in stem:
                stem = stem.split(".", 1)[0]
            code = sanitize_code(stem)
        base = code
        n = 2
        while code in used:
            code = f"{base}-{n}"
            n += 1
        used.add(code)
        specs.append(InputSpec(code=code, path=path))
    return specs


def autodetect_related(sidecars: Sidecars) -> list[tuple[str, Path]]:
    related: list[tuple[str, Path]] = []
    for suffix, label in ((".score", "score"), (".stats.json", "stats"), (".clean", "clean"), (".scores", "scores")):
        p = Path(f"{sidecars.out}{suffix}")
        if p.exists():
            related.append((label, p))
    return related


def score_summary_from_file(path: Path) -> str | None:
    text = read_text_if_exists(path)
    if text is None:
        return None
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return None


def format_link(label: str, target: Path, meta_path: Path) -> str:
    return f"[{label}]({shortest_relpath(target, meta_path)})"


def format_keyvals(items: Iterable[tuple[str, str]]) -> list[str]:
    return [f"- {key}: `{value}`" for key, value in items]


def load_stats_text(path: Path) -> list[str]:
    text = read_text_if_exists(path)
    if text is None:
        return []
    if path.suffix == ".json":
        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                return [f"- {k}: `{obj[k]}`" for k in sorted(obj)]
        except json.JSONDecodeError:
            pass
    excerpt = excerpt_markdown(text, max_lines=8, max_chars=700)
    if not excerpt:
        return []
    return [f"```text\n{excerpt}\n```"]


def parse_meta_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def inherited_meta_lines(
    spec: InputSpec,
    input_meta: Path,
    text: str,
    meta_path: Path,
) -> list[str]:
    sections = parse_meta_sections(text)
    wanted = ("output", "result", "machine")
    lines: list[str] = []
    any_added = False
    for section in wanted:
        body = sections.get(section, [])
        body_lines = [line for line in body if line.strip()]
        if not body_lines:
            continue
        any_added = True
        for body_line in body_lines:
            stripped = body_line.strip()
            if stripped.startswith("- "):
                lines.append(f"- ({spec.code}.{section}) {stripped[2:]}")
            elif stripped.startswith(">"):
                continue
            else:
                lines.append(f"- ({spec.code}.{section}) {stripped}")
    return lines if any_added else []


def build_meta_markdown(
    *,
    output_path: str | Path,
    title: str | None,
    cwd: str | Path,
    command: str | None,
    setup: list[tuple[str, str]],
    results: list[tuple[str, str]],
    notes: list[str],
    inputs: list[InputSpec],
    related: list[tuple[str, Path]],
    input_excerpt_lines: int = 8,
    input_excerpt_chars: int = 700,
) -> str:
    sidecars = sidecars_for_output(output_path)
    meta_path = sidecars.meta
    title_text = title or sidecars.out.name
    lines: list[str] = [f"# Run Metadata: {title_text}", ""]

    lines.extend(
        [
            "## Output",
            f"- out: {format_link(sidecars.out.name, sidecars.out, meta_path)}",
            f"- log: {format_link(sidecars.log.name, sidecars.log, meta_path)}",
            "",
        ]
    )

    if command:
        lines.extend(["## Command", "```bash", f"cd {cwd}", command, "```", ""])

    if setup:
        lines.extend(["## Setup", *format_keyvals(setup), ""])

    if results:
        lines.extend(["## Result", *format_keyvals(results), ""])

    if related:
        lines.append("## Related")
        for label, path in related:
            lines.append(f"- {label}: {format_link(path.name, path, meta_path)}")
        lines.append("")

    if inputs:
        lines.append("## Inputs")
        for spec in inputs:
            path = spec.path
            lines.append(f"### `{spec.code}`")
            lines.append(f"- path: {format_link(path.name, path, meta_path)}")
            input_meta = find_input_meta(path)
            if input_meta is not None:
                lines.append(f"- meta: {format_link(input_meta.name, input_meta, meta_path)}")
                text = read_text_if_exists(input_meta)
                if text:
                    inherited = inherited_meta_lines(spec, input_meta, text, meta_path)
                    if inherited:
                        lines.append("")
                        lines.extend(inherited)
                    else:
                        excerpt = excerpt_markdown(
                            text, max_lines=input_excerpt_lines, max_chars=input_excerpt_chars
                        )
                        if excerpt:
                            lines.append("")
                            lines.append(f"> Excerpt from `{input_meta.name}`:")
                            for ex_line in excerpt.splitlines():
                                lines.append(f"> {ex_line}" if ex_line else ">")
            lines.append("")

    if notes:
        lines.extend(["## Notes", *[f"- {note}" for note in notes], ""])

    return "\n".join(lines).rstrip() + "\n"
