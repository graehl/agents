#!/usr/bin/env python3
"""Manage per-project on-deck run queues."""
from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STEWARD_PRIORITY_MAX = 3
STATUSES = {"pending", "launched", "done", "skipped", "blocked", "retired"}
AUTHORS = {"director", "steward"}
SIZE_CLASSES = {"small", "medium", "large"}
INDEX_CELL_MAX = 60
FRONTMATTER_ORDER = (
    "slug",
    "priority",
    "by",
    "status",
    "runtime_estimate",
    "size_class",
    "cheap_reversible",
    "guard",
    "skip_if",
    "provenance",
    "created_at",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise SystemExit("slug must contain at least one letter or digit")
    return slug


def deck_dir(root: Path) -> Path:
    return root / "on-deck"


def entry_path(root: Path, slug: str) -> Path:
    return deck_dir(root) / f"{slug}.md"


def done_entry_path(root: Path, slug: str) -> Path:
    return deck_dir(root) / "done" / f"{slug}.md"


def parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y"}:
        return True
    if value in {"0", "false", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got {raw!r}")


def fm_value_text(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value))


def parse_fm_value(raw: str) -> object:
    text = raw.strip()
    if not text:
        return ""
    if text[0] in {"'", '"'}:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text.strip("\"'")
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def parse_entry(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing frontmatter fence")
    fields: dict[str, object] = {}
    end = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = idx
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, raw_value = line.partition(":")
        if not sep:
            raise ValueError(f"bad frontmatter line: {line!r}")
        fields[key.strip()] = parse_fm_value(raw_value)
    if end is None:
        raise ValueError("unterminated frontmatter")
    return fields, "\n".join(lines[end + 1 :])


def read_entry(path: Path) -> tuple[dict[str, object], str]:
    return parse_entry(path.read_text())


def section(body: str, heading: str) -> str:
    # Headings inside fenced launch blocks must not start or end a section.
    in_fence = False
    collecting = False
    out: list[str] = []
    for line in body.splitlines():
        if not in_fence and line.rstrip() == f"## {heading}":
            collecting = True
        elif collecting and not in_fence and line.startswith("## "):
            break
        elif collecting:
            out.append(line)
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
    return "\n".join(out).strip()


def markdown_escape(value: object) -> str:
    text = str(value or "").replace("\n", " ")
    return text.replace("|", r"\|")


def index_cell(value: object) -> str:
    text = markdown_escape(value)
    if len(text) > INDEX_CELL_MAX:
        return text[: INDEX_CELL_MAX - 1] + "…"
    return text


def cost_text(entry: dict[str, object]) -> str:
    runtime = entry.get("runtime_estimate") or "?"
    size = entry.get("size_class") or "?"
    cheap = entry.get("cheap_reversible")
    if cheap is True:
        cheap_text = "cheap"
    elif cheap is False:
        cheap_text = "gated"
    else:
        cheap_text = "?"
    return f"{runtime}, {size}, {cheap_text}"


def iter_entries(root: Path) -> list[tuple[Path, dict[str, object], str]]:
    deck = deck_dir(root)
    if not deck.exists():
        return []
    entries = []
    for path in sorted(deck.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        try:
            fields, body = read_entry(path)
        except ValueError as exc:
            fields, body = {"slug": path.stem, "status": "invalid", "error": str(exc)}, path.read_text()
        entries.append((path, fields, body))
    return entries


def sorted_entries(root: Path) -> list[tuple[Path, dict[str, object], str]]:
    def key(item: tuple[Path, dict[str, object], str]) -> tuple[int, str]:
        path, fields, _body = item
        priority = fields.get("priority")
        return (-(priority if isinstance(priority, int) else -1), str(fields.get("slug") or path.stem))

    return sorted(iter_entries(root), key=key)


def validate_entry(path: Path, fields: dict[str, object], body: str) -> list[str]:
    if "error" in fields:
        return [f"{path}: {fields['error']}"]
    errors: list[str] = []
    required = (
        "slug",
        "priority",
        "by",
        "status",
        "runtime_estimate",
        "size_class",
        "cheap_reversible",
        "guard",
        "skip_if",
    )
    for key in required:
        if fields.get(key) in {None, ""}:
            errors.append(f"missing {key}")
    priority = fields.get("priority")
    if not isinstance(priority, int) or priority < 0 or priority > 10:
        errors.append("priority must be an integer from 0 to 10")
    by = fields.get("by")
    if by not in AUTHORS:
        errors.append("by must be director or steward")
    status = fields.get("status")
    if status not in STATUSES:
        errors.append(f"status must be one of {', '.join(sorted(STATUSES))}")
    size = fields.get("size_class")
    if size not in {None, ""} and size not in SIZE_CLASSES:
        errors.append(f"size_class must be one of {', '.join(sorted(SIZE_CLASSES))}")
    if by == "steward":
        if isinstance(priority, int) and priority > STEWARD_PRIORITY_MAX:
            errors.append(f"steward-authored entries must use priority <= {STEWARD_PRIORITY_MAX}")
        if fields.get("cheap_reversible") is not True:
            errors.append("steward-authored entries must be cheap_reversible=true")
    if not section(body, "Launch"):
        errors.append("missing ## Launch")
    if not section(body, "Check"):
        errors.append("missing ## Check")
    if not section(body, "Status Log"):
        errors.append("missing ## Status Log")
    return [f"{path}: {error}" for error in errors]


def entry_warnings(path: Path, fields: dict[str, object], body: str) -> list[str]:
    warnings: list[str] = []
    launch = section(body, "Launch")
    if re.search(r"agentctl\s+start", launch) and "--context-note" not in launch:
        warnings.append("agentctl launch lacks --context-note (see the on-deck skill)")
    return [f"{path}: warning: {warning}" for warning in warnings]


def validate(root: Path) -> int:
    entries = iter_entries(root)
    errors: list[str] = []
    for path, fields, body in entries:
        errors.extend(validate_entry(path, fields, body))
        for warning in entry_warnings(path, fields, body):
            print(warning, file=sys.stderr)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    suffix = "y" if len(entries) == 1 else "ies"
    print(f"validated {len(entries)} on-deck entr{suffix}")
    return 0


def render_frontmatter(fields: dict[str, object]) -> str:
    lines = ["---"]
    for key in FRONTMATTER_ORDER:
        if key in fields:
            lines.append(f"{key}: {fm_value_text(fields[key])}")
    for key in sorted(k for k in fields if k not in FRONTMATTER_ORDER):
        lines.append(f"{key}: {fm_value_text(fields[key])}")
    lines.append("---")
    return "\n".join(lines)


def render_entry(args: argparse.Namespace, launch: str) -> str:
    fields = {
        "slug": args.slug,
        "priority": args.priority,
        "by": args.by,
        "status": args.status,
        "runtime_estimate": args.runtime_estimate,
        "size_class": args.size_class,
        "cheap_reversible": args.cheap_reversible,
        "guard": args.guard,
        "skip_if": args.skip_if,
        "provenance": "; ".join(args.provenance or []),
        "created_at": utc_now(),
    }
    return f"""{render_frontmatter(fields)}

# {args.slug}

## What
{args.what}

## Why
{args.why}

## Launch
```bash
{launch}
```

## Check
{args.check}

## On Success
{args.on_success}

## Status Log
- {utc_now()} {args.by}: created {args.status} entry
"""


def write_index(root: Path) -> Path | None:
    deck = deck_dir(root)
    if not deck.exists():
        return None
    index = deck / "INDEX.md"
    rows = [
        "# On-deck Index",
        "",
        "Derived file; regenerate with `python3 ~/agents/scripts/on_deck.py index`.",
        "",
        "| priority | slug | by | status | cost | guard | skip-if | provenance | file |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for path, fields, _body in sorted_entries(root):
        if fields.get("status") == "retired":
            continue
        rel = path.relative_to(root)
        rows.append(
            "| {priority} | {slug} | {by} | {status} | {cost} | {guard} | {skip_if} | {provenance} | [{file}]({file}) |".format(
                priority=index_cell(fields.get("priority", "")),
                slug=index_cell(fields.get("slug") or path.stem),
                by=index_cell(fields.get("by", "")),
                status=index_cell(fields.get("status", "")),
                cost=index_cell(cost_text(fields)),
                guard=index_cell(fields.get("error") or fields.get("guard", "")),
                skip_if=index_cell(fields.get("skip_if", "")),
                provenance=index_cell(fields.get("provenance", "")),
                file=markdown_escape(rel),
            )
        )
    rows.extend(["", f"Generated: {utc_now()}", ""])
    index.write_text("\n".join(rows))
    return index


def add(args: argparse.Namespace) -> int:
    args.root = args.root.resolve()
    args.slug = slugify(args.slug)
    if not args.launch:
        print("missing launch command after --", file=sys.stderr)
        return 2
    path = entry_path(args.root, args.slug)
    done_path = done_entry_path(args.root, args.slug)
    if path.exists() or done_path.exists():
        print(f"on-deck entry already exists for slug {args.slug!r}", file=sys.stderr)
        return 1
    text = render_entry(args, shlex.join(args.launch))
    fields, body = parse_entry(text)
    errors = validate_entry(path, fields, body)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 2
    for warning in entry_warnings(path, fields, body):
        print(warning, file=sys.stderr)
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.parent / "done").mkdir(exist_ok=True)
    path.write_text(text)
    index = write_index(args.root)
    if index is None:
        raise RuntimeError("internal error: add created entry without an on-deck directory")
    print(path.relative_to(args.root))
    print(f"index: {index.relative_to(args.root)}")
    return 0


def index_cmd(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    index = write_index(root)
    if index is None:
        print("no on-deck directory")
        return 0
    print(index.relative_to(root))
    return 0


def replace_status(text: str, status: str) -> str:
    new_text, count = re.subn(r"(?m)^status: .*$", f"status: {fm_value_text(status)}", text, count=1)
    if count == 0:
        raise ValueError("no status: frontmatter line to update")
    return new_text


def log_cmd(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    slug = slugify(args.slug)
    path = entry_path(root, slug)
    if not path.exists():
        print(f"unknown on-deck entry: {slug}", file=sys.stderr)
        return 1
    text = path.read_text()
    if args.status:
        try:
            text = replace_status(text, args.status)
        except ValueError as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            return 1
    if "\n## Status Log\n" not in text:
        print(f"{path}: missing ## Status Log", file=sys.stderr)
        return 1
    line = f"- {utc_now()} {args.by}: {' '.join(args.message)}"
    path.write_text(text.rstrip() + f"\n{line}\n")
    write_index(root)
    print(path.relative_to(root))
    return 0


def retire(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    slug = slugify(args.slug)
    path = entry_path(root, slug)
    if not path.exists():
        print(f"unknown on-deck entry: {slug}", file=sys.stderr)
        return 1
    dest = done_entry_path(root, slug)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"done entry already exists: {dest.relative_to(root)}", file=sys.stderr)
        return 1
    try:
        text = replace_status(path.read_text().rstrip() + "\n", "retired")
    except ValueError as exc:
        print(f"{path}: {exc}", file=sys.stderr)
        return 1
    reason = args.reason or "retired"
    text += f"- {utc_now()} {args.by}: retired - {reason}\n"
    shutil.move(str(path), str(dest))
    dest.write_text(text)
    write_index(root)
    print(dest.relative_to(root))
    return 0


CONDITION_TIMEOUT = 120


def run_condition(root: Path, command: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["bash", "-c", command],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=CONDITION_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {CONDITION_TIMEOUT}s"
    detail = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, detail


def condition_note(detail: str) -> str:
    if not detail:
        return ""
    first = detail.splitlines()[0]
    return f" — {first[:120]}"


def eligible_cmd(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    entries = sorted_entries(root)
    if args.slug:
        slug = slugify(args.slug)
        entries = [item for item in entries if (item[1].get("slug") or item[0].stem) == slug]
        if not entries:
            print(f"unknown on-deck entry: {slug}", file=sys.stderr)
            return 1
    for path, fields, _body in entries:
        slug = str(fields.get("slug") or path.stem)
        status = fields.get("status")
        if status != "pending":
            if args.slug:
                print(f"{slug}: not pending (status: {status})")
                return 1
            continue
        if args.steward and fields.get("cheap_reversible") is not True:
            if args.slug:
                print(f"{slug}: outside steward autonomy (cheap_reversible is not true)")
                return 1
            continue
        skip_fired, detail = run_condition(root, str(fields.get("skip_if") or "false"))
        if skip_fired:
            print(f"{slug}: skip_if fired{condition_note(detail)}")
            if args.slug:
                return 1
            continue
        guard_ok, detail = run_condition(root, str(fields.get("guard") or "false"))
        if not guard_ok:
            print(f"{slug}: guard failed{condition_note(detail)}")
            if args.slug:
                return 1
            continue
        print(f"eligible: {slug} ({path.relative_to(root)})")
        return 0
    print("no eligible entry")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a project on-deck/ run queue.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser(
        "add",
        usage="%(prog)s slug [options] -- <launch command>",
        help="Create one on-deck entry.",
        description="Create one on-deck entry. Append -- <launch command> after the entry options.",
    )
    add_p.add_argument("slug")
    add_p.add_argument("--root", type=Path, default=Path.cwd())
    add_p.add_argument("--priority", type=int, required=True)
    add_p.add_argument("--by", choices=sorted(AUTHORS), default="director")
    add_p.add_argument(
        "--status",
        choices=["pending", "blocked"],
        default="pending",
        help="blocked records a triage item whose launch needs director/implementation work first",
    )
    add_p.add_argument("--runtime-estimate", required=True)
    add_p.add_argument("--size-class", required=True)
    add_p.add_argument("--cheap-reversible", type=parse_bool, required=True)
    add_p.add_argument("--guard", required=True)
    add_p.add_argument("--skip-if", required=True)
    add_p.add_argument("--what", required=True)
    add_p.add_argument("--why", required=True)
    add_p.add_argument("--provenance", action="append", default=[])
    add_p.add_argument("--on-success", required=True)
    add_p.add_argument("--check", required=True)
    add_p.set_defaults(func=add)

    index_p = sub.add_parser("index", help="Regenerate on-deck/INDEX.md.")
    index_p.add_argument("--root", type=Path, default=Path.cwd())
    index_p.set_defaults(func=index_cmd)

    validate_p = sub.add_parser("validate", help="Validate on-deck entries.")
    validate_p.add_argument("--root", type=Path, default=Path.cwd())
    validate_p.set_defaults(func=lambda args: validate(args.root.resolve()))

    log_p = sub.add_parser("log", help="Append a status log line.")
    log_p.add_argument("slug")
    log_p.add_argument("message", nargs="+")
    log_p.add_argument("--root", type=Path, default=Path.cwd())
    log_p.add_argument("--status", choices=sorted(STATUSES))
    log_p.add_argument("--by", choices=sorted(AUTHORS), default="steward")
    log_p.set_defaults(func=log_cmd)

    retire_p = sub.add_parser("retire", help="Move an entry to on-deck/done/.")
    retire_p.add_argument("slug")
    retire_p.add_argument("--root", type=Path, default=Path.cwd())
    retire_p.add_argument("--reason", default="")
    retire_p.add_argument("--by", choices=sorted(AUTHORS), default="steward")
    retire_p.set_defaults(func=retire)

    eligible_p = sub.add_parser(
        "eligible",
        help="Run guard/skip_if commands; report the first launchable entry.",
        description="Evaluate skip_if then guard as bash commands from the project root "
        "(exit 0 = skip fires / guard passes). With a slug, report that entry only.",
    )
    eligible_p.add_argument("slug", nargs="?")
    eligible_p.add_argument("--root", type=Path, default=Path.cwd())
    eligible_p.add_argument(
        "--steward",
        action="store_true",
        help="only consider entries a steward may launch unaided (cheap_reversible true)",
    )
    eligible_p.set_defaults(func=eligible_cmd)

    return parser


def main(argv: list[str]) -> int:
    launch: list[str] | None = None
    if argv[:1] == ["add"]:
        try:
            sep = argv.index("--")
        except ValueError:
            launch = []
        else:
            launch = argv[sep + 1 :]
            argv = argv[:sep]
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "add":
        args.launch = launch or []
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
