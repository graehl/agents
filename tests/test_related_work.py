#!/usr/bin/env python3
"""Tests for scripts/related-work — the shared survey related-work engine.

No test reaches the network: fetching is covered by driving the sentinel and
manifest state that the fetch path branches on, which is where every bug this
tool exists to prevent has actually lived.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "related-work"

_loader = importlib.machinery.SourceFileLoader("related_work", str(TOOL))
_spec = importlib.util.spec_from_loader("related_work", _loader)
rw = importlib.util.module_from_spec(_spec)
# @dataclass resolves annotations through sys.modules, so register before exec.
sys.modules["related_work"] = rw
_loader.exec_module(rw)


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def run(cwd: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=dict(os.environ, PYTHONPATH=str(REPO_ROOT)),
    )


def jsonl(proc: subprocess.CompletedProcess) -> list[dict]:
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


MANIFEST = """\
meta:
  field_slug: demo
  coverage_cutoff: 2026-07-31
  grounding_mode: grounded-in-progress

papers:
  - key: alpha2020-one
    short: one
    concept_page: concepts/one.md
    title: "One"
    arxiv: "2001.00001"
    grounded: true
    authors: ["Alpha Author"]
    venue: "DemoConf"
    year: 2020
    verified: true
    fetched: 2026-07-31
  - key: beta2021-two
    title: "Two"
    url: "https://example.invalid/two"
    grounded: false
    authors: ["Beta Author"]
    venue: "DemoConf"
    year: 2021
    verified: false
    fetched: null
  - key: gamma2022-three
    title: "Three"
    arxiv: "2203.00003"
    grounded: false
    authors: ["Gamma Author"]
    venue: "DemoConf"
    year: 2022
    verified: true
    source: anchor-bib
    fetched: null
"""


def survey(tmp: Path) -> Path:
    """A survey root whose manifest starts out agreeing with disk."""
    root = tmp / "surveys" / "demo"
    related = root / "related-work"
    (related / "extract").mkdir(parents=True)
    (root / "concepts").mkdir()
    (root / "concepts" / "one.md").write_text("# one\n")
    (related / "papers.yaml").write_text(MANIFEST)
    fetched = related / "extract" / "alpha2020-one"
    fetched.mkdir()
    (fetched / "paper.md").write_text("# One\n")
    (fetched / ".fetched").write_text(
        json.dumps(
            {
                "method": "arxiv-html",
                "source": "https://arxiv.org/html/2001.00001",
                "markdown": "paper.md",
                "derived_with": rw.HTML_DERIVATION,
            }
        )
    )
    return root


def test_clean_survey_audits_clean():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "audit")
        _assert(
            proc.returncode == 0,
            f"clean survey should audit clean:\n{proc.stdout}{proc.stderr}",
        )
        row = jsonl(proc)[0]
        _assert(row["drift"] == 0 and row["manifested"] == 3, row)
        _assert(
            row["grounded"] == 1 and row["verified"] == 2 and row["digested"] == 1, row
        )


def test_audit_requires_complete_citation_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        manifest = root / "related-work" / "papers.yaml"
        manifest.write_text(
            manifest.read_text()
            .replace('    title: "One"\n', "    title: null\n")
            .replace('    authors: ["Alpha Author"]\n', "    authors: []\n")
            .replace('    venue: "DemoConf"\n', "    venue: null\n", 1)
            .replace("    year: 2020\n", "    year: null\n")
        )

        proc = run(root, "audit")
        _assert(proc.returncode == 3, proc.stdout)
        finding = next(
            row
            for row in jsonl(proc)
            if row["key"] == "alpha2020-one"
            and row["rule"] == "citation-metadata"
        )
        _assert(
            finding["detail"]
            == "required citation fields are empty: title, authors, venue, year",
            finding,
        )


def test_audit_catches_drift_in_both_directions():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        related = root / "related-work"
        # beta was fetched but the manifest was never updated.
        beta = related / "extract" / "beta2021-two"
        beta.mkdir()
        (beta / ".fetched").write_text(
            '{"method":"url-html","source":"https://example.invalid/two"}'
        )
        # gamma claims grounding it never had.
        text = (
            (related / "papers.yaml")
            .read_text()
            .replace(
                """  - key: gamma2022-three
    title: "Three"
    arxiv: "2203.00003"
    grounded: false""",
                """  - key: gamma2022-three
    title: "Three"
    arxiv: "2203.00003"
    grounded: true""",
            )
        )
        (related / "papers.yaml").write_text(text)

        proc = run(root, "audit")
        _assert(proc.returncode == 3, f"drift must exit 3, got {proc.returncode}")
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        for expected in (
            ("beta2021-two", "grounded"),
            ("beta2021-two", "fetched-date"),
            ("beta2021-two", "verified"),
            ("gamma2022-three", "grounded"),
        ):
            _assert(expected in rules, f"{expected} missing from {sorted(rules)}")


def test_verified_without_own_extract_needs_a_source():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        related = root / "related-work"
        # gamma is verified against the anchor bibliography, which is legal —
        # until it stops saying so.
        text = (
            (related / "papers.yaml")
            .read_text()
            .replace("    source: anchor-bib\n", "")
        )
        (related / "papers.yaml").write_text(text)
        proc = run(root, "audit")
        _assert(proc.returncode == 3)
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        _assert(("gamma2022-three", "source") in rules, sorted(rules))


def test_unregenerable_and_orphan_extracts_are_findings():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        related = root / "related-work"
        (related / "extract" / "nobody-claims-me").mkdir()
        # strip alpha's arxiv id: its extract can no longer be rebuilt
        text = (
            (related / "papers.yaml")
            .read_text()
            .replace('    arxiv: "2001.00001"\n', "")
        )
        (related / "papers.yaml").write_text(text)
        proc = run(root, "audit")
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        _assert(("nobody-claims-me", "orphan-extract") in rules, sorted(rules))
        _assert(("alpha2020-one", "regenerable") in rules, sorted(rules))


def test_missing_concept_page_is_a_finding():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        (root / "concepts" / "one.md").unlink()
        proc = run(root, "audit")
        rules = {(r["key"], r["rule"]) for r in jsonl(proc)}
        _assert(("alpha2020-one", "concept-page") in rules, sorted(rules))


def test_bare_fetch_refuses_to_queue_the_whole_backlog():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "fetch")
        _assert(
            proc.returncode == 2, "a bare fetch must not silently start N downloads"
        )
        envelope = json.loads(proc.stderr.splitlines()[0])
        _assert("2 papers have no extract" in envelope["error"]["message"], envelope)
        _assert(
            sorted(envelope["error"]["detail"]["pending"])
            == [
                "beta2021-two",
                "gamma2022-three",
            ],
            envelope,
        )


def test_completed_extract_is_skipped_without_network():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "fetch", "alpha2020-one")
        _assert(proc.returncode == 0, proc.stderr)
        row = jsonl(proc)[0]
        _assert(
            row
            == {
                "key": "alpha2020-one",
                "status": "skipped",
                "reason": "already fetched",
            },
            row,
        )


def test_unknown_key_is_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        proc = run(root, "fetch", "nope2020-x")
        _assert(proc.returncode == 4, proc.returncode)


def test_sentinel_reads_the_legacy_tab_form():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".fetched"
        path.write_text("arxiv-html\thttps://arxiv.org/html/2001.00001\n")
        sentinel = rw.read_sentinel(path)
        _assert(sentinel.method == "arxiv-html", sentinel)
        _assert(sentinel.source == "https://arxiv.org/html/2001.00001", sentinel)
        _assert(sentinel.etag is None and sentinel.last_modified is None, sentinel)


def test_revalidation_without_validators_never_claims_fresh():
    # No ETag and no Last-Modified means there is nothing to ask the server;
    # "cannot tell" must read as "may have changed".
    _assert(
        not rw.is_unchanged("https://example.invalid/x", rw.Sentinel("url-html", "u"))
    )


def test_legacy_url_pdf_sentinel_does_not_request_html_derivation():
    sentinel = rw.Sentinel("url-html", "https://example.test/paper.PDF?download=1")
    with tempfile.TemporaryDirectory() as tmp:
        _assert(not rw.html_derivation_missing(Path(tmp), sentinel), sentinel)


def test_audit_requires_html_derivation_metadata_and_markdown():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        sentinel_path = root / "related-work" / "extract" / "alpha2020-one" / ".fetched"
        sentinel_path.write_text(
            '{"method":"arxiv-html","source":"https://arxiv.org/html/2001.00001"}'
        )
        proc = run(root, "audit")
        _assert(proc.returncode == 3, proc.stdout)
        rules = {(row["key"], row["rule"]) for row in jsonl(proc)}
        _assert(("alpha2020-one", "html-markdown") in rules, sorted(rules))
        _assert(("alpha2020-one", "html-derivation") in rules, sorted(rules))


def test_audit_requires_markdown_for_a_legacy_completed_extract():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        directory = root / "related-work" / "extract" / "alpha2020-one"
        (directory / "paper.md").unlink()
        (directory / "paper.html").write_text("<p>legacy</p>")
        (directory / ".fetched").write_text("backfilled\talpha2020-one\n")

        proc = run(root, "audit")
        _assert(proc.returncode == 3, proc.stdout)
        rules = {(row["key"], row["rule"]) for row in jsonl(proc)}
        _assert(("alpha2020-one", "extract-content") in rules, sorted(rules))


def _passthrough_html2text(command, **kwargs):
    _assert("html2text==2025.4.15" in command, command)
    _assert("--body-width=0" in command, command)
    return subprocess.CompletedProcess(command, 0, stdout=kwargs["input"], stderr="")


def test_html_derivation_emits_tex_once_after_conversion_and_drops_plain_html():
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        html_dir = directory / "html"
        html_dir.mkdir()
        source = html_dir / "paper.html"
        source.write_text(
            r"""<article><p>inline <math><mi>Φ</mi><annotation encoding="application/x-tex">\Phi</annotation></math>.</p><math display="block"><mi>x</mi><annotation encoding="application/x-tex">x_{1}</annotation></math></article>"""
        )
        original_have, original_run = rw.have, rw.subprocess.run
        rw.have = lambda tool: tool == "uvx" or original_have(tool)
        rw.subprocess.run = _passthrough_html2text
        try:
            result = rw.derive_saved_html(
                directory, "https://example.test/paper", "key"
            )
        finally:
            rw.have, rw.subprocess.run = original_have, original_run

        markdown = (html_dir / "paper.md").read_text()
        _assert(result.markdown == "html/paper.md", result)
        _assert(result.html == "dropped", result)
        _assert(not source.exists(), "plain source HTML should be dropped")
        _assert("Φ" not in markdown, markdown)
        _assert(markdown.count(r"\Phi") == 1, markdown)
        _assert(r"\(\Phi\)" in markdown, markdown)
        _assert(r"\[x_{1}\]" in markdown, markdown)


def test_html_preprocessor_uses_alttext_when_tex_annotation_is_absent():
    processed, replacements, _presentation = rw.preprocess_html(
        r"""<p><math alttext="0"><mn>0</mn></math> <math alttext="wrong"><annotation encoding="application/x-tex">x_{1}</annotation></math></p>"""
    )

    _assert(len(replacements) == 2, replacements)
    _assert(
        [tex for _placeholder, tex, _block in replacements] == ["0", r"x_{1}"],
        replacements,
    )
    _assert(all(placeholder in processed for placeholder, _tex, _block in replacements))


def test_html_derivation_keeps_content_presentation_not_page_chrome():
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        source = directory / "paper.html"
        source.write_text(
            "<header><form><input></form></header>"
            '<article><p id="part">Text <a href="#part">self</a> '
            '<a href="data:text/plain;base64,dGV4dA==">download</a>'
            "</p><svg><path></path></svg></article>"
        )
        original_have, original_run = rw.have, rw.subprocess.run
        rw.have = lambda tool: tool == "uvx" or original_have(tool)
        rw.subprocess.run = _passthrough_html2text
        try:
            result = rw.derive_saved_html(
                directory, "https://example.test/paper", "key"
            )
        finally:
            rw.have, rw.subprocess.run = original_have, original_run

        _assert(source.exists(), "paper-body SVG has presentation absent from markdown")
        _assert(result.html == "kept (data URI, section anchors, svg)", result)
        _assert("data:text/plain" not in (directory / "paper.md").read_text(), result)


def test_html_fetch_records_markdown_derivation():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        loaded = rw.load_survey(root)
        paper = loaded.find("beta2021-two")
        originals = (rw.save_page, rw.http_headers, rw.have, rw.subprocess.run)

        def save_page(directory, _url, stem):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"{stem}.html").write_text("<p>downloaded</p>")
            return True

        rw.save_page = save_page
        rw.http_headers = lambda _url: {}
        rw.have = lambda tool: tool == "uvx" or originals[2](tool)
        rw.subprocess.run = _passthrough_html2text
        try:
            row = rw.fetch_paper(
                loaded,
                paper,
                no_html=False,
                download_only=False,
                svg_figures=False,
                refresh_source=False,
            )
        finally:
            rw.save_page, rw.http_headers, rw.have, rw.subprocess.run = originals

        sentinel = rw.read_sentinel(loaded.sentinel_path(paper.key))
        _assert(
            row["status"] == "fetched" and row["markdown"] == "beta2021-two.md", row
        )
        _assert(sentinel.markdown == "beta2021-two.md", sentinel)
        _assert(sentinel.derived_with == rw.HTML_DERIVATION, sentinel)


def test_revalidate_backfills_a_completed_html_extract_before_network_fetch():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        loaded = rw.load_survey(root)
        directory = loaded.extract_dir("alpha2020-one")
        source = directory / "alpha2020-one.html"
        source.write_text("<p>old download</p>")
        loaded.sentinel_path("alpha2020-one").write_text(
            '{"method":"arxiv-html","source":"https://arxiv.org/html/2001.00001"}'
        )
        originals = (
            rw.is_unchanged,
            rw.save_page,
            rw.have,
            rw.subprocess.run,
            rw.emit_table,
        )
        rows = []

        rw.is_unchanged = lambda _url, _sentinel: True
        rw.save_page = lambda *_args, **_kwargs: _assert(
            False, "a fresh source should not be fetched again"
        )
        rw.have = lambda tool: tool == "uvx" or originals[2](tool)
        rw.subprocess.run = _passthrough_html2text
        rw.emit_table = lambda _args, result, _columns, _name: rows.extend(result)
        args = rw.build_parser().parse_args(
            ["--dir", str(root), "fetch", "alpha2020-one", "--revalidate", "--compact"]
        )
        try:
            result = args.func(args)
        finally:
            (
                rw.is_unchanged,
                rw.save_page,
                rw.have,
                rw.subprocess.run,
                rw.emit_table,
            ) = originals

        row = rows[0]
        sentinel = rw.read_sentinel(loaded.sentinel_path("alpha2020-one"))
        _assert(result == 0 and row["status"] == "derived", row)
        _assert(sentinel.markdown == "alpha2020-one.md", sentinel)
        _assert(sentinel.derived_with == rw.HTML_DERIVATION, sentinel)


def test_derive_only_discovers_and_normalizes_a_legacy_html_only_extract():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        loaded = rw.load_survey(root)
        directory = loaded.extract_dir("alpha2020-one")
        (directory / "paper.md").unlink()
        (directory / "2001.00001.html").write_text("<p>legacy download</p>")
        loaded.sentinel_path("alpha2020-one").write_text("backfilled\talpha2020-one\n")
        originals = (rw.have, rw.subprocess.run, rw.emit_table)
        rows = []

        rw.have = lambda tool: tool == "uvx" or originals[0](tool)
        rw.subprocess.run = _passthrough_html2text
        rw.emit_table = lambda _args, result, _columns, _name: rows.extend(result)
        args = rw.build_parser().parse_args(
            ["--dir", str(root), "fetch", "alpha2020-one", "--derive-only"]
        )
        try:
            result = args.func(args)
        finally:
            rw.have, rw.subprocess.run, rw.emit_table = originals

        row = rows[0]
        sentinel = rw.read_sentinel(loaded.sentinel_path("alpha2020-one"))
        _assert(result == 0 and row["status"] == "derived", row)
        _assert(sentinel.method == "arxiv-html", sentinel)
        _assert(sentinel.source == "https://arxiv.org/html/2001.00001", sentinel)
        _assert(sentinel.markdown == "2001.00001.md", sentinel)


def test_list_and_status_report_the_survey():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        rows = jsonl(run(root, "list"))
        _assert(
            [r["key"] for r in rows]
            == ["alpha2020-one", "beta2021-two", "gamma2022-three"],
            rows,
        )
        _assert(rows[0]["extract"] is True and rows[1]["extract"] is False, rows)

        status = jsonl(run(root, "status"))[0]
        _assert(
            status["extracts"] == 1 and status["coverage_cutoff"] == "2026-07-31",
            status,
        )

        toon = run(root, "list", "--toon")
        _assert(toon.returncode == 0 and "alpha2020-one" in toon.stdout, toon.stdout)


def test_resolves_the_survey_root_or_the_related_work_dir():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        for cwd in (root, root / "related-work"):
            proc = run(cwd, "status")
            _assert(proc.returncode == 0, f"{cwd}: {proc.stderr}")
        outside = Path(tmp) / "elsewhere"
        outside.mkdir()
        _assert(
            run(outside, "status").returncode == 4, "no manifest anywhere = not found"
        )


def test_init_scaffolds_a_new_survey():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "surveys" / "fresh"
        root.mkdir(parents=True)
        proc = run(root, "init")
        _assert(proc.returncode == 0, proc.stderr)
        manifest = root / "related-work" / "papers.yaml"
        _assert(manifest.is_file(), "init writes papers.yaml")
        _assert("field_slug: fresh" in manifest.read_text(), manifest.read_text()[:200])
        _assert(
            "extract/" in (root / "related-work" / ".gitignore").read_text(),
            "extracts are ignored by shared policy, not a per-clone exclude",
        )
        _assert(run(root, "audit").returncode == 0, "an empty survey audits clean")
        _assert(run(root, "init").returncode == 5, "init must not clobber a manifest")


def test_bad_manifest_shapes_fail_loud():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "s"
        (root / "related-work").mkdir(parents=True)
        manifest = root / "related-work" / "papers.yaml"
        manifest.write_text("papers: not-a-list\n")
        _assert(run(root, "audit").returncode == 70, "wrong shape is a schema failure")
        manifest.write_text("papers:\n  - title: keyless\n")
        _assert(
            run(root, "audit").returncode == 70, "a keyless entry is a schema failure"
        )


def test_manifest_paths_cannot_escape_the_survey():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        manifest = root / "related-work" / "papers.yaml"
        original = manifest.read_text()
        manifest.write_text(original.replace("alpha2020-one", "../../victim"))
        proc = run(root, "audit")
        _assert(proc.returncode == 70, proc.stderr)
        _assert("safe path component" in proc.stderr, proc.stderr)

        manifest.write_text(original.replace("concepts/one.md", "../../victim.md"))
        proc = run(root, "audit")
        _assert(proc.returncode == 70, proc.stderr)
        _assert("concept_page" in proc.stderr, proc.stderr)


def test_download_only_never_marks_html_as_extracted():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        loaded = rw.load_survey(root)
        paper = loaded.find("beta2021-two")
        original_save_page = rw.save_page

        def save_page(directory, _url, stem):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"{stem}.html").write_text("downloaded")
            return True

        rw.save_page = save_page
        try:
            row = rw.fetch_paper(
                loaded,
                paper,
                no_html=False,
                download_only=True,
                svg_figures=False,
                refresh_source=False,
            )
        finally:
            rw.save_page = original_save_page
        _assert(row["status"] == "downloaded", row)
        _assert(not loaded.sentinel_path(paper.key).exists(), row)


def test_url_pdf_uses_marker_instead_of_html_derivation():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        loaded = rw.load_survey(root)
        paper = loaded.find("beta2021-two")
        paper.ident = "https://example.test/two.pdf?download=1"
        originals = (rw.download, rw.run_marker, rw.http_headers, rw.save_page)
        calls = []

        def download(_url, target):
            calls.append(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"pdf")
            return True

        rw.download = download
        rw.run_marker = lambda *_args, **_kwargs: {}
        rw.http_headers = lambda _url: {}
        rw.save_page = lambda *_args, **_kwargs: _assert(
            False, "an explicit PDF URL must not use the HTML downloader"
        )
        try:
            row = rw.fetch_paper(
                loaded,
                paper,
                no_html=False,
                download_only=False,
                svg_figures=False,
                refresh_source=False,
            )
        finally:
            rw.download, rw.run_marker, rw.http_headers, rw.save_page = originals

        _assert(row["status"] == "fetched" and row["method"] == "pdf-marker", row)
        _assert(calls == [loaded.extract_dir(paper.key) / "two.pdf"], calls)


def test_pdf_revalidation_replaces_existing_source_before_extraction():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        loaded = rw.load_survey(root)
        paper = loaded.find("alpha2020-one")
        directory = loaded.extract_dir(paper.key)
        pdf = directory / "source.pdf"
        pdf.write_bytes(b"stale")
        originals = (rw.download, rw.run_marker, rw.http_headers)
        calls = []

        def download(_url, target):
            calls.append(target)
            target.write_bytes(b"fresh")
            return True

        def run_marker(source, *_args, **_kwargs):
            _assert(source.read_bytes() == b"fresh", "marker saw stale PDF bytes")
            return {}

        rw.download = download
        rw.run_marker = run_marker
        rw.http_headers = lambda _url: {}
        try:
            row = rw.fetch_paper(
                loaded,
                paper,
                no_html=True,
                download_only=False,
                svg_figures=False,
                refresh_source=True,
            )
        finally:
            rw.download, rw.run_marker, rw.http_headers = originals
        _assert(row["status"] == "fetched", row)
        _assert(calls == [pdf], calls)
        _assert(pdf.read_bytes() == b"fresh", pdf.read_bytes())


def test_limit_rejects_negative_values_and_accepts_zero():
    with tempfile.TemporaryDirectory() as tmp:
        root = survey(Path(tmp))
        negative = run(root, "fetch", "--limit", "-1")
        _assert(negative.returncode == 2, negative.stderr)
        zero = run(root, "fetch", "--limit", "0")
        _assert(zero.returncode == 0, zero.stderr)
        _assert(jsonl(zero) == [{"count": 0, "of": "results"}], zero.stdout)


def test_help_carries_the_acli_footer():
    proc = run(REPO_ROOT, "--help")
    _assert(proc.returncode == 0, proc.stderr)
    _assert("acli: 1 complete toon" in proc.stdout, proc.stdout[-300:])
    _assert("exit codes:" in proc.stdout, proc.stdout[-300:])


def test_completion_offers_verbs():
    proc = run(REPO_ROOT, "--acli-complete", "")
    _assert(proc.returncode == 0, proc.stderr)
    offered = {json.loads(line)["completion"] for line in proc.stdout.splitlines()}
    _assert({"audit", "fetch", "init", "list", "status"} <= offered, offered)


def _collect_tests():
    return [
        (name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")
    ]


def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    passed = failed = 0
    failures = []
    start = time.time()
    for name, fn in _collect_tests():
        try:
            fn()
            passed += 1
            print(
                f"PASS  {name}" if verbose else ".",
                end="" if not verbose else "\n",
                flush=True,
            )
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print(
                f"FAIL  {name}" if verbose else "F",
                end="" if not verbose else "\n",
                flush=True,
            )
    if not verbose:
        print()
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    print(f"\n{passed} passed, {failed} failed in {time.time() - start:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
