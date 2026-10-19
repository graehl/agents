"""Check a venue PDF against the venue's font, embedding and paper-size rules.

A clean render says nothing about these rules. ARR desk-rejected a paper whose
body text was Liberation Serif: a metric clone of Times, but venue checkers
accept fonts by name, not by width. This reads the PDF itself, so it judges
the exact file to be uploaded, whatever built it.

Every check requires all fonts embedded. A venue profile adds its accepted
body fonts, the minimum share of characters the most-used font must reach,
and its paper size. For ACL it can also run the venue's own checker,
aclpubcheck, which remains the authority. Advice:
topics/document-writing-printable.md § Venue submission path.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

import acli

ACLPUBCHECK_VENV = Path.home() / ".cache/aclpubcheck-venv"
PROFILES = {
    "acl": {
        "source": "https://acl-org.github.io/ACLPUB/formatting.html; "
        "https://github.com/acl-org/aclpubcheck (formatchecker.check_font)",
        "checked": "2026-10-17",
        # aclpubcheck's accepted names as pdftohtml families. pdftohtml drops
        # a standard style suffix ("TeXGyreTermesX-Regular" -> "TeXGyreTermesX")
        # but keeps others ("NimbusRomNo9L-Regu"), so a family is accepted when
        # it equals a name or continues it after "-" (body_font_accepted).
        # aclpubcheck lists STIX and Inconsolata with literal subset tags,
        # which can only be accidental; their families are accepted here.
        "body-fonts": [
            "NimbusRomNo9L",
            "TeXGyreTermesX",
            "TeXGyreTermes",
            "TimesNewRomanPSMT",
            "STIXGeneral",
            "Inconsolatazi4",
        ],
        "min-body-share": 0.35,
        "paper": ("A4", 595.28, 841.89),
        "checker": "aclpubcheck",
    },
}
SUBSET = re.compile(r"^[A-Z]{6}\+")


def embedded_fonts(pdf: Path) -> list[dict]:
    """One row per PDF font object: name without subset tag, type, embedded."""
    return parse_pdffonts(subprocess.check_output(["pdffonts", str(pdf)], text=True))


def parse_pdffonts(text: str) -> list[dict]:
    """Rows of `pdffonts` output, whose names may contain spaces.

    Every column after the name has the fixed width of its header dashes; a
    long name only pushes them right. So the row's tail is sliced by those
    widths and the name is whatever precedes it.
    """
    lines = text.splitlines()
    widths = [len(dashes) for dashes in lines[1].split(" ")]
    tail = sum(widths[1:]) + len(widths) - 1
    rows = []
    for line in lines[2:]:
        cells, position = [], len(line) - tail + 1
        for width in widths[1:]:
            cells.append(line[position : position + width].strip())
            position += width + 1
        rows.append(
            {
                "name": SUBSET.sub("", line[: len(line) - tail].rstrip()),
                "type": cells[0],
                "embedded": cells[2] == "yes",
            }
        )
    return rows


def body_font_accepted(family: str, accepted: list[str]) -> bool:
    return any(family == name or family.startswith(name + "-") for name in accepted)


def font_characters(pdf: Path) -> Counter:
    """Characters of text set in each font family, figure text included."""
    xml = subprocess.check_output(
        ["pdftohtml", "-xml", "-i", "-stdout", "-q", str(pdf)], text=True
    )
    families = {
        spec_id: SUBSET.sub("", family)
        for spec_id, family in re.findall(
            r'<fontspec id="(\d+)"[^>]*family="([^"]*)"', xml
        )
    }
    counts = Counter()
    for spec_id, text in re.findall(r'<text [^>]*font="(\d+)"[^>]*>(.*?)</text>', xml):
        counts[families[spec_id]] += len(html.unescape(re.sub(r"<[^>]+>", "", text)))
    return counts


def page_sizes(pdf: Path) -> list[tuple[float, float]]:
    info = subprocess.check_output(
        ["pdfinfo", "-f", "1", "-l", "100000", str(pdf)], text=True
    )
    return [
        (float(w), float(h))
        for w, h in re.findall(
            r"^Page\s+\d+ size:\s*([\d.]+) x ([\d.]+)", info, re.MULTILINE
        )
    ]


def check_pdf(pdf: Path, profile: str | None = None) -> dict:
    """Facts about `pdf` plus `failures`, empty when every applicable rule holds."""
    if profile is not None and profile not in PROFILES:
        raise ValueError(
            f"Unknown venue profile {profile!r}; known: {sorted(PROFILES)}"
        )
    fonts = embedded_fonts(pdf)
    failures = [
        f"font not embedded: {name}"
        for name in sorted({row["name"] for row in fonts if not row["embedded"]})
    ]
    result = {
        "pdf": str(pdf),
        "profile": profile,
        "fonts": sorted({row["name"] for row in fonts}),
        "type3_fonts": sorted(
            {row["name"] for row in fonts if row["type"] == "Type 3"}
        ),
    }
    if profile is None:
        result["failures"] = failures
        return result
    rules = PROFILES[profile]
    counts = font_characters(pdf)
    total = sum(counts.values())
    if not total:
        raise ValueError(f"No extractable text in {pdf}; cannot identify its body font")
    main, main_count = counts.most_common(1)[0]
    share = main_count / total
    result.update(
        main_font=main,
        main_font_share=round(share, 3),
        source=rules["source"],
        checked=rules["checked"],
    )
    accepted = rules["body-fonts"]
    if not body_font_accepted(main, accepted):
        failures.append(
            f"most-used font is {main} ({share:.0%} of characters); "
            f"{profile} accepts only {accepted}. A metric-compatible clone such as "
            "Liberation Serif is not Times to the venue's checker."
        )
    elif share < rules["min-body-share"]:
        failures.append(
            f"most-used font {main} sets only {share:.0%} of characters; "
            f"{profile}'s checker needs at least {rules['min-body-share']:.0%}"
        )
    paper, width, height = rules["paper"]
    wrong = sorted(
        {
            (w, h)
            for w, h in page_sizes(pdf)
            if abs(w - width) > 2 or abs(h - height) > 2
        }
    )
    result["paper"] = paper
    if wrong:
        failures.append(f"pages not {paper} ({width} x {height} pt): {wrong}")
    result["failures"] = failures
    return result


def aclpubcheck(pdf: Path, executable: Path, paper_type: str) -> dict[str, int]:
    """Run aclpubcheck in a scratch directory; error counts by category."""
    with tempfile.TemporaryDirectory() as work:
        result = subprocess.run(
            [str(executable), "--paper_type", paper_type, str(pdf.resolve())],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,  # its exit status does not reflect findings; read the report
        )
        reports = list(Path(work).glob("errors-*.json"))
        if result.returncode or len(reports) > 1:
            raise ValueError(
                f"aclpubcheck failed (exit {result.returncode}): {result.stderr[-2000:]}"
            )
        # A clean paper prints "All Clear!" and writes no report.
        if not reports:
            if "All Clear" not in result.stdout:
                raise ValueError(
                    f"aclpubcheck wrote no report: {result.stdout[-2000:]}"
                )
            return {}
        return {
            key: len(items) for key, items in json.loads(reports[0].read_text()).items()
        }


def find_aclpubcheck(explicit: Path | None) -> Path | None:
    if explicit:
        return explicit
    found = shutil.which("aclpubcheck")
    if found:
        return Path(found)
    candidate = ACLPUBCHECK_VENV / "bin/aclpubcheck"
    return candidate if candidate.is_file() else None


def main(argv=None) -> int:
    cli = acli.argument_parser(
        prog="venue-pdf-check",
        description=__doc__,
        capabilities=("complete",),
        exit_codes={
            0: "every check passed",
            1: "a venue rule failed",
            2: "check could not run",
        },
    )
    cli.add_argument("pdf", type=Path, help="The exact PDF to be uploaded")
    cli.add_argument(
        "--profile", choices=sorted(PROFILES), help="Venue rules (else embedding only)"
    )
    cli.add_argument(
        "--paper-type",
        default="long",
        help="aclpubcheck --paper_type: long, short, demo or other",
    )
    cli.add_argument(
        "--aclpubcheck",
        type=Path,
        help=f"aclpubcheck executable (else PATH, else {ACLPUBCHECK_VENV}/bin)",
    )
    cli.add_argument(
        "--no-aclpubcheck",
        action="store_true",
        help="Skip the venue checker; the built-in checks still run",
    )
    cli.add_argument(
        "--review",
        action="store_true",
        help="Anonymous review PDF: aclpubcheck margin errors are reported, not failed, "
        "since review line numbers sit in the margin",
    )
    acli.add_standard_args(cli)
    acli.maybe_complete(cli, None if argv is None else [cli.prog, *argv])
    args = cli.parse_args(argv)
    try:
        result = check_pdf(args.pdf, args.profile)
        checker = PROFILES.get(args.profile, {}).get("checker")
        if checker == "aclpubcheck" and not args.no_aclpubcheck:
            executable = find_aclpubcheck(args.aclpubcheck)
            if executable is None:
                raise ValueError(
                    "aclpubcheck not found; install it with `python3 -m venv "
                    f"{ACLPUBCHECK_VENV} && {ACLPUBCHECK_VENV}/bin/pip install "
                    "git+https://github.com/acl-org/aclpubcheck`, or pass --no-aclpubcheck"
                )
            errors = aclpubcheck(args.pdf, executable, args.paper_type)
            result["aclpubcheck"] = errors
            for key, count in sorted(errors.items()):
                if key == "Error.MARGIN" and args.review:
                    continue
                result["failures"].append(f"aclpubcheck {key}: {count}")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        acli.die(str(error), 2)
    lines = [
        f"{args.pdf}: {'PASS' if not result['failures'] else 'FAIL'}"
        + (f" ({args.profile})" if args.profile else " (embedding only)"),
        *(f"  fail: {failure}" for failure in result["failures"]),
    ]
    if "main_font" in result:
        lines.append(
            f"  most-used font: {result['main_font']} ({result['main_font_share']:.0%})"
        )
    if result.get("aclpubcheck", {}).get("Error.MARGIN") and args.review:
        lines.append(
            f"  aclpubcheck margin errors: {result['aclpubcheck']['Error.MARGIN']} "
            "(review line numbers; rerun on the camera-ready build without --review)"
        )
    if result["type3_fonts"]:
        lines.append(f"  note: Type 3 fonts {result['type3_fonts']}")
    acli.emit(result, acli.resolve_format(args), text="\n".join(lines))
    return 1 if result["failures"] else 0
