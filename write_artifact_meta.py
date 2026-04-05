#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import artifact_meta


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Write <artifact>.meta.md for a saved research output."
    )
    p.add_argument(
        "output", help="Primary saved output artifact, e.g. untracked/runs/.../foo.out"
    )
    p.add_argument(
        "--title", default="", help="Optional title override for the metadata heading"
    )
    p.add_argument(
        "--cwd",
        default=".",
        help="Working directory the generating command was run from",
    )
    p.add_argument(
        "--cmd-bash",
        default="",
        help="Actual generating command, without the leading cd",
    )
    p.add_argument(
        "--setup", action="append", default=[], help="Setup key/value as KEY=VALUE"
    )
    p.add_argument(
        "--result", action="append", default=[], help="Result key/value as KEY=VALUE"
    )
    p.add_argument("--note", action="append", default=[], help="Additional note line")
    p.add_argument(
        "--input",
        action="append",
        default=[],
        help="Input artifact as PATH or CODE=PATH for short inherited-meta codenames",
    )
    p.add_argument(
        "--related",
        action="append",
        default=[],
        help="Related file as LABEL=PATH; auto-detected score/stats sidecars are also included",
    )
    p.add_argument(
        "--stats-file",
        action="append",
        default=[],
        help="Additional stats file to summarize into the metadata body",
    )
    p.add_argument(
        "--score-summary-from-sidecar",
        action="store_true",
        help="If <output>.score exists, add its first non-empty line to the Result section",
    )
    p.add_argument(
        "--excerpt-lines",
        type=int,
        default=8,
        help="Max propagated input-meta excerpt lines",
    )
    p.add_argument(
        "--excerpt-chars",
        type=int,
        default=700,
        help="Max propagated input-meta excerpt chars",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    sidecars = artifact_meta.sidecars_for_output(args.output)
    sidecars.meta.parent.mkdir(parents=True, exist_ok=True)

    setup = artifact_meta.parse_keyvals(args.setup)
    results = artifact_meta.parse_keyvals(args.result)
    notes = list(args.note)

    if args.score_summary_from_sidecar:
        summary = artifact_meta.score_summary_from_file(Path(f"{sidecars.out}.score"))
        if summary:
            results.append(("score-summary", summary))

    for stats_path_str in args.stats_file:
        stats_path = Path(stats_path_str)
        stats_lines = artifact_meta.load_stats_text(stats_path)
        if stats_lines:
            notes.append(f"Stats excerpt from {stats_path.name}:")
            notes.extend(
                line if not line.startswith("- ") else line[2:] for line in stats_lines
            )

    related = artifact_meta.autodetect_related(sidecars)
    related.extend(
        (label, Path(path)) for label, path in artifact_meta.parse_keyvals(args.related)
    )

    text = artifact_meta.build_meta_markdown(
        output_path=sidecars.out,
        title=args.title or None,
        cwd=Path(args.cwd),
        command=args.cmd_bash or None,
        setup=setup,
        results=results,
        notes=notes,
        inputs=artifact_meta.parse_input_specs(args.input),
        related=related,
        input_excerpt_lines=args.excerpt_lines,
        input_excerpt_chars=args.excerpt_chars,
    )
    sidecars.meta.write_text(text, encoding="utf-8")
    print(sidecars.meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
