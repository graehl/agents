"""Command-line interface for install-agents."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import InstallError, install, status, uninstall
from .harnesses import select_harnesses


def _parser() -> argparse.ArgumentParser:
    def formatter(prog: str) -> argparse.HelpFormatter:
        return argparse.HelpFormatter(prog, max_help_position=34, width=999)

    parser = argparse.ArgumentParser(
        prog="install-agents",
        description=(
            "Install AGENTS.global.md and repo skills with a restorable "
            "pre-install manifest."
        ),
        formatter_class=formatter,
    )
    parser.add_argument("command", choices=("install", "status", "uninstall"))
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Target home directory; use a synthetic path to test safely.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        help="Instruction checkout; defaults to the checkout containing this script.",
    )
    parser.add_argument(
        "--harness",
        action="append",
        help="Harness name, comma-separated names, or all (default: all). Repeatable.",
    )
    parser.add_argument("--json", action="store_true", help="Emit the result as JSON.")
    return parser


def _human(result: dict) -> str:
    if "harnesses" in result:
        lines = [
            f"home: {result['home']}",
            f"active install: {'yes' if result['active'] else 'no'}",
        ]
        for name, state in result["harnesses"].items():
            instruction = "ok" if state["instruction_ok"] else "missing/drifted"
            skills = "ok" if state["skills_ok"] else "missing/drifted"
            lines.append(f"{name}: instructions {instruction}; skills {skills}")
        if result.get("drift"):
            lines.append("drift: " + ", ".join(result["drift"]))
        return "\n".join(lines)
    lines = [f"status: {result['status']}", f"changed paths: {result.get('changed', 0)}"]
    if result.get("manifest"):
        lines.append(f"manifest: {result['manifest']}")
    if result.get("backup"):
        lines.append(f"backup: {result['backup']}")
    if result.get("retained_dirs"):
        lines.append(
            "retained non-empty directories: " + ", ".join(result["retained_dirs"])
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo_root = (args.repo or Path(__file__).resolve().parents[2]).resolve()
    try:
        harnesses = select_harnesses(args.harness)
        if args.command == "install":
            result = install(args.home, repo_root, harnesses)
        elif args.command == "status":
            result = status(args.home, repo_root, harnesses)
        else:
            result = uninstall(args.home)
    except (InstallError, ValueError) as exc:
        print(f"install-agents: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True) if args.json else _human(result))
    if args.command == "status":
        harness_drift = any(
            not state["instruction_ok"] or not state["skills_ok"]
            for state in result["harnesses"].values()
        )
        if result.get("drift") or harness_drift:
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
