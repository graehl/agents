"""Original section and paragraph ranges carried through Quarto renders.

A target names a half-open, zero-based `[line, utf16-column]` range in an
editable `.qmd` fragment. Targets travel through the render as paired
`ya-source-target:v1` HTML comments (or `% source-map:v1` TeX comments via a
print filter), and the HTML build emits a hash-bound `.map` sidecar with the
final generated ranges.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import tempfile
from bisect import bisect_right
from collections import defaultdict
from contextlib import contextmanager
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote_to_bytes

ATTRIBUTE = "data-qmd-source"
IMAGE_ATTRIBUTE = "data-qmd-image-source"


def _range_end(lines, source, end):
    if end < len(lines) or source.endswith("\n"):
        return [end, 0]
    return [end - 1, len(lines[-1].encode("utf-16-le")) // 2]


def section_source_targets(path: Path, quarto: str, relative_to: Path) -> list[dict]:
    """Locate headings and prose blocks using original parser source positions.

    `source` in each target is the fragment path relative to `relative_to`,
    normally the directory holding the generated artifact.
    """
    source = path.read_text()
    parsed = json.loads(
        subprocess.check_output(
            [
                quarto,
                "pandoc",
                str(path),
                "--from",
                "commonmark_x+sourcepos",
                "--to",
                "json",
            ],
            text=True,
        )
    )
    lines = source.splitlines(keepends=True)
    name = os.path.relpath(path, relative_to)
    headings = []
    for block in parsed["blocks"]:
        if block["t"] != "Header":
            continue
        level, attributes, _ = block["c"]
        position = dict(attributes[2])["data-pos"]
        match = re.search(r"@(\d+):1-", position)
        if not match:
            raise ValueError(f"Unsupported heading source position: {position}")
        line = int(match[1]) - 1
        if not re.match(r"^#{1,6}\s", lines[line]):
            raise ValueError(f"Source editing requires ATX headings: {path}:{line + 1}")
        headings.append((level, line, attributes[0]))
    if not headings or any(line.strip() for line in lines[: headings[0][1]]):
        raise ValueError(f"Expected a section beginning with a heading: {path}")
    targets = []
    ids = set()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    for index, (level, start, anchor) in enumerate(headings):
        end = next(
            (line for depth, line, _ in headings[index + 1 :] if depth <= level),
            len(lines),
        )
        target_id = (
            "paper-" + hashlib.sha256(f"{path.name}:{anchor}".encode()).hexdigest()[:20]
        )
        if target_id in ids:
            raise ValueError(
                f"Duplicate heading target; add an explicit anchor: {target_id}"
            )
        ids.add(target_id)
        targets.append(
            {
                "id": target_id,
                "headerId": anchor,
                "source": name,
                "sourceRange": [[start, 0], _range_end(lines, source, end)],
                "precision": "item",
                "sourceSha256": digest,
            }
        )
    for index, block in enumerate(parsed["blocks"]):
        if block["t"] != "Div" or dict(block["c"][0][2]).get("wrapper") != "1":
            continue
        if not any(child["t"] != "RawBlock" for child in block["c"][1]):
            continue
        position = dict(block["c"][0][2])["data-pos"]
        match = re.search(r"@(\d+):1-(\d+):(\d+)$", position)
        if not match:
            raise ValueError(f"Unsupported block source position: {position}")
        start, end, column = map(int, match.groups())
        start -= 1
        # Captions must remain adjacent to the table they describe.
        if lines[start].startswith(": "):
            continue
        end = min(end - (column == 1), len(lines))
        # CommonMark can include the first line of a following raw comment.
        for following in parsed["blocks"][index + 1 :]:
            if following["t"] not in {"Header", "Div", "CodeBlock", "Table"}:
                continue
            attrs = (
                following["c"][1] if following["t"] == "Header" else following["c"][0]
            )
            next_pos = dict(attrs[2]).get("data-pos", "")
            next_starts = re.findall(r"[@;](\d+):1-", next_pos)
            if next_starts:
                end = min(end, min(map(int, next_starts)) - 1)
                break
        while end > start and not lines[end - 1].strip():
            end -= 1
        targets.append(
            {
                "id": "paper-"
                + hashlib.sha256(f"{path.name}:block:{start}".encode()).hexdigest()[
                    :20
                ],
                "source": name,
                "sourceRange": [[start, 0], _range_end(lines, source, end)],
                "precision": "item",
                "sourceSha256": digest,
            }
        )
    return targets


def manuscript_source_targets(
    sections: list[Path], quarto: str, relative_to: Path
) -> list[dict]:
    """Resolve repeated automatic heading anchors in manuscript include order."""
    targets = []
    header_ids = set()
    for section in sections:
        for target in section_source_targets(section, quarto, relative_to):
            if "headerId" not in target:
                targets.append(target)
                continue
            base = target["headerId"]
            suffix = 1
            while target["headerId"] in header_ids:
                target["headerId"] = f"{base}-{suffix}"
                suffix += 1
            header_ids.add(target["headerId"])
            targets.append(target)
    return targets


def target_comment(target):
    record = json.dumps(target, ensure_ascii=True, separators=(",", ":")).replace(
        "--", r"--"
    )
    return f"<!-- ya-source-target:v1 {record} -->"


def marked_source(source: str, targets: list[dict]) -> str:
    """Carry paragraph source ranges as invisible comments through Quarto."""
    lines = source.splitlines(keepends=True)
    for target in sorted(
        targets, key=lambda item: item["sourceRange"][0], reverse=True
    ):
        if "headerId" in target:
            continue
        (start, _), (end, column) = target["sourceRange"]
        stop = end + bool(column)
        lines[stop:stop] = [f"\n\n<!-- /ya-source-target:v1 {target['id']} -->\n\n"]
        lines[start:start] = [target_comment(target) + "\n\n"]
    return "".join(lines)


def targets_for(section: Path, targets: list[dict], relative_to: Path) -> list[dict]:
    name = os.path.relpath(section, relative_to)
    return [target for target in targets if target["source"] == name]


@contextmanager
def staged_sources(
    root: Path,
    sections: list[Path],
    targets: list[dict],
    relative_to: Path,
    skip: set[str],
):
    """Render an isolated sibling copy of the document directory.

    The copy sits beside the document directory, so relative resource paths
    such as `../..` resolve to the same files. Included fragments are replaced
    by marked copies; every other entry is a symlink. `skip` names top-level
    entries (output and cache directories) left out of the copy.
    """
    home = root.parent
    marked = {Path(os.path.normpath(section)): section for section in sections}
    # Not a dot-directory: Quarto 1.9 ignores the project output-dir inside one.
    with tempfile.TemporaryDirectory(
        prefix="qmd-source-", dir=home.parent
    ) as directory:
        staged_home = Path(directory)

        def mirror(source_dir: Path, target_dir: Path):
            for path in source_dir.iterdir():
                if source_dir == home and path.name in skip | {root.name}:
                    continue
                if path in marked:
                    selected = targets_for(marked[path], targets, relative_to)
                    (target_dir / path.name).write_text(
                        marked_source(path.read_text(), selected)
                    )
                elif (
                    path.is_dir()
                    and not path.is_symlink()
                    and any(section.is_relative_to(path) for section in marked)
                ):
                    (target_dir / path.name).mkdir()
                    mirror(path, target_dir / path.name)
                else:
                    (target_dir / path.name).symlink_to(path.absolute())

        mirror(home, staged_home)
        staged_root = staged_home / root.name
        staged_root.write_text(root.read_text())
        yield staged_root


class SectionPositions(HTMLParser):
    """Find producer-marked HTML sections without reserializing their content."""

    def __init__(self, html: str):
        super().__init__(convert_charrefs=False)
        self.offsets = [0]
        for match in re.finditer("\n", html):
            self.offsets.append(match.end())
        self.stack = []
        self.sections = {}
        self.images = []
        self.feed(html)
        self.close()
        if self.stack:
            raise ValueError("Unclosed HTML section in document")

    def source_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == "section":
            self.stack.append((dict(attrs).get(ATTRIBUTE), self.source_offset()))
        elif tag == "img" and IMAGE_ATTRIBUTE in dict(attrs):
            self.images.append(
                (
                    dict(attrs),
                    self.source_offset(),
                    self.source_offset() + len(self.get_starttag_text()),
                )
            )

    def handle_endtag(self, tag):
        if tag != "section":
            return
        if not self.stack:
            raise ValueError("Unexpected HTML section close in document")
        target_id, start = self.stack.pop()
        if target_id:
            if target_id in self.sections:
                raise ValueError(f"Duplicate rendered source target: {target_id}")
            self.sections[target_id] = (start, self.source_offset() + len("</section>"))


def image_source_targets(
    html: str, resources: list[Path], extension: str, output: Path
) -> list[dict]:
    """Map embedded figures to the exact local assets supplied to Quarto."""
    targets = []
    for index, (attrs, _, _) in enumerate(SectionPositions(html).images):
        name = attrs[IMAGE_ATTRIBUTE]
        asset = Path(name)
        if not asset.suffix:
            asset = asset.with_suffix("." + extension)
        candidates = [directory / asset for directory in resources]
        path = next(
            (candidate.resolve() for candidate in candidates if candidate.is_file()),
            None,
        )
        if path is None:
            raise ValueError(f"Cannot resolve figure source: {name}")
        payload = path.read_bytes()
        prefix, encoded = attrs["src"].split(",", 1)
        embedded = (
            base64.b64decode(encoded)
            if prefix.endswith(";base64")
            else unquote_to_bytes(encoded)
        )
        if embedded != payload:
            raise ValueError(f"Embedded figure differs from source: {path}")
        source = os.path.relpath(path, output.parent)
        text = payload.decode("utf-8")
        end = [text.count("\n"), len(text.rsplit("\n", 1)[-1].encode("utf-16-le")) // 2]
        targets.append(
            {
                "id": "paper-image-"
                + hashlib.sha256(f"{source}:{index}".encode()).hexdigest()[:20],
                "imageIndex": index,
                "source": source,
                "sourceRange": [[0, 0], end],
                "precision": "item",
                "sourceSha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return targets


class TargetComments(HTMLParser):
    """Read real HTML comment pairs, ignoring comment-like script text."""

    def __init__(self, html):
        super().__init__(convert_charrefs=False)
        self.line_offsets = [0, *(match.end() for match in re.finditer("\n", html))]
        self.stack = []
        self.ranges = {}
        self.feed(html)
        self.close()
        if self.stack:
            raise ValueError("Unclosed source target comment")

    def handle_comment(self, data):
        line, column = self.getpos()
        offset = self.line_offsets[line - 1] + column
        value = data.strip()
        if value.startswith("ya-source-target:v1 "):
            target_id = json.loads(value.removeprefix("ya-source-target:v1 "))["id"]
            if target_id in self.ranges or any(
                item[0] == target_id for item in self.stack
            ):
                raise ValueError(f"Duplicate source target comment: {target_id}")
            self.stack.append((target_id, offset + len(data) + 7 + 1))
        elif value.startswith("/ya-source-target:v1 "):
            target_id = value.removeprefix("/ya-source-target:v1 ")
            if not self.stack or self.stack[-1][0] != target_id:
                raise ValueError(f"Mismatched source target comment: {target_id}")
            _, start = self.stack.pop()
            self.ranges[target_id] = (start, offset - 1)


def source_mapped_html(
    html: str, targets: list[dict], filename: str
) -> tuple[str, dict]:
    """Emit paired YA comments and a hash-bound sidecar with final HTML ranges."""
    positions = SectionPositions(html)
    sections = positions.sections
    if set(sections) != {target["id"] for target in targets if "headerId" in target}:
        raise ValueError("Rendered sections do not match the original source targets")
    insertions = defaultdict(list)
    for target in targets:
        if "imageIndex" in target:
            _, start, end = positions.images[target["imageIndex"]]
        elif "headerId" in target:
            start, end = sections[target["id"]]
        else:
            continue
        insertions[start].append(target_comment(target) + "\n")
        insertions[end].insert(0, f"\n<!-- /ya-source-target:v1 {target['id']} -->")
    for offset in sorted(insertions, reverse=True):
        html = html[:offset] + "".join(insertions[offset]) + html[offset:]
    html = re.sub(rf'\s+{ATTRIBUTE}="[^"]*"', "", html)
    html = re.sub(rf'\s+{IMAGE_ATTRIBUTE}="[^"]*"', "", html)
    html = html.replace(
        "</head>", f"<!--# sourceMappingURL={filename}.map -->\n</head>", 1
    )
    if f"<!--# sourceMappingURL={filename}.map -->" not in html:
        raise ValueError("Missing HTML head for source map discovery")

    comments = TargetComments(html)
    if set(comments.ranges) != {target["id"] for target in targets}:
        raise ValueError("Rendered blocks do not match the original source targets")

    def coordinate(offset):
        line = bisect_right(comments.line_offsets, offset) - 1
        return [
            line,
            len(html[comments.line_offsets[line] : offset].encode("utf-16-le")) // 2,
        ]

    mapped_targets = []
    for target in targets:
        start, end = comments.ranges[target["id"]]
        mapped_targets.append(
            {**target, "generatedRange": [coordinate(start), coordinate(end)]}
        )
    source_map = {
        "version": 3,
        "file": filename,
        "sources": list(dict.fromkeys(target["source"] for target in targets)),
        "names": [],
        "mappings": "",
        "x_ya_source_targets": {"version": 1, "targets": mapped_targets},
        "x_ya_artifact_sha256": hashlib.sha256(html.encode()).hexdigest(),
    }
    return html, source_map
