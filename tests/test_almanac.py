#!/usr/bin/env python3
"""End-to-end tests for the almanac module and launcher (topics/almanac.md).

Stdlib only, no pytest. Each test builds a synthetic dataset in its own
tmp ALMANAC_ROOT and drives the engine via subprocess. Run directly:

    python3 tests/test_almanac.py            # run all
    python3 tests/test_almanac.py -k query   # run tests matching 'query'
    python3 tests/test_almanac.py -v         # verbose
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "almanac"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CARDS = {
    "cards": [
        {"name": "Strike", "tier": "C", "cost": 1, "text": "Deal 6 damage."},
        {"name": "Bash", "tier": "B", "cost": 2, "text": "Deal 8. Vulnerable 2."},
        {
            "name": "Perfected Strike",
            "tier": "A",
            "cost": 2,
            "text": "More per Strike.",
        },
    ]
}

EXTRACT = """#!/usr/bin/env python3
import pathlib, sys
sys.stdout.write(pathlib.Path(sys.argv[1]).read_text())
"""

PNG = b"\x89PNG\r\n\x1a\nsynthetic-test-image"


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def run(root, *args, source=None):
    env = dict(os.environ, ALMANAC_ROOT=str(root))
    argv = [sys.executable, str(SCRIPT), *args]
    if source is not None:
        argv += ["--source", str(source)]
    return subprocess.run(argv, capture_output=True, text=True, env=env)


def jsonl(proc):
    return [json.loads(line) for line in proc.stdout.splitlines()]


def make_dataset(root, name="cards-test", refresh="auto", data=CARDS, url=None):
    directory = Path(root) / name
    directory.mkdir(parents=True)
    manifest = {
        "name": name,
        "url": url or f"https://example.test/{name}",
        "title": "Test cards",
        "refresh": refresh,
        "schema": {
            "records": "cards",
            "key": "name",
            "columns": ["name", "tier", "cost"],
            "filters": ["tier", "cost"],
            "search": ["name", "text"],
            "ordinals": [["tier"]],
        },
    }
    (directory / "manifest.json").write_text(json.dumps(manifest))
    (directory / "data.json").write_text(json.dumps(data))
    if refresh != "frozen":
        extract = directory / "extract"
        extract.write_text(EXTRACT)
        extract.chmod(0o755)
    return directory


def add_images(directory):
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["schema"]["image"] = "image"
    manifest_path.write_text(json.dumps(manifest))

    data_path = directory / "data.json"
    data = json.loads(data_path.read_text())
    images = directory / "images"
    images.mkdir()
    for record in data["cards"]:
        filename = record["name"].lower().replace(" ", "-") + ".png"
        record["image"] = f"images/{filename}"
        (images / filename).write_bytes(PNG)
    data_path.write_text(json.dumps(data))


def registered_root():
    tmp = tempfile.mkdtemp(prefix="almanac-test-")
    make_dataset(tmp)
    bin_dir = Path(tmp) / "bin"
    proc = run(tmp, "register", "cards-test", "--launcher-dir", str(bin_dir))
    _assert(proc.returncode == 0, proc.stderr)
    return Path(tmp), bin_dir


def test_engine_is_an_importable_module():
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "from almanac.cli import build_parser; print(build_parser().prog)",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(proc.returncode == 0 and proc.stdout == "almanac\n", proc.stderr)


def test_image_verb_falls_back_to_a_structured_path():
    root = Path(tempfile.mkdtemp(prefix="almanac-test-"))
    directory = make_dataset(root)
    add_images(directory)
    _assert(run(root, "register", "cards-test", "--no-launcher").returncode == 0)

    proc = run(root, "image", "cards-test", "strike")
    _assert(proc.returncode == 0, proc.stderr)
    result = jsonl(proc)[0]
    _assert(result["record"] == "Strike", result)
    _assert(result["image"] == "images/strike.png", result)
    _assert(result["path"] == str((directory / "images/strike.png").resolve()), result)
    _assert(result["mime"] == "image/png", result)
    _assert(result["rendered"] is False and result["renderer"] is None, result)
    _assert("not a terminal" in result["reason"], result)

    data = json.loads((directory / "data.json").read_text())
    data["cards"][0]["image"] = "../outside.png"
    (root / "outside.png").write_bytes(PNG)
    (directory / "data.json").write_text(json.dumps(data))
    proc = run(root, "image", "cards-test", "strike")
    _assert(proc.returncode == 70, "attachment paths may not escape the dataset")
    _assert("outside" in json.loads(proc.stderr)["error"]["message"], proc.stderr)


def test_image_native_renderers():
    from io import BytesIO

    from almanac.image import detect_renderer, display_image

    def missing(_name):
        return None

    _assert(detect_renderer({"TERM": "xterm-kitty"}, which=missing) == "kitty")
    _assert(detect_renderer({"TERM_PROGRAM": "iTerm.app"}, which=missing) == "iterm2")
    _assert(
        detect_renderer(
            {"TERM": "xterm-sixel"},
            which=lambda name: f"/test/{name}" if name == "img2sixel" else None,
        )
        == "sixel"
    )
    _assert(
        detect_renderer(
            {"TERM": "xterm-256color"},
            which=lambda name: f"/test/{name}" if name == "chafa" else None,
        )
        == "chafa"
    )

    image = Path(tempfile.mkdtemp(prefix="almanac-test-")) / "card.png"
    image.write_bytes(PNG)

    kitty = BytesIO()
    result = display_image(image, renderer="kitty", width=24, out=kitty, is_tty=True)
    _assert(result.rendered and result.renderer == "kitty", result)
    _assert(kitty.getvalue().startswith(b"\x1b_G"), kitty.getvalue())
    _assert(b"f=100" in kitty.getvalue() and b"c=24" in kitty.getvalue())

    iterm2 = BytesIO()
    result = display_image(image, renderer="iterm2", width=24, out=iterm2, is_tty=True)
    _assert(result.rendered and result.renderer == "iterm2", result)
    _assert(iterm2.getvalue().startswith(b"\x1b]1337;File="), iterm2.getvalue())
    _assert(b"width=24" in iterm2.getvalue())

    captured = BytesIO()
    result = display_image(
        image, renderer="kitty", width=24, out=captured, is_tty=False
    )
    _assert(not result.rendered and captured.getvalue() == b"", result)


def test_register_wires_symlink_launcher_and_git():
    root, bin_dir = registered_root()
    result = jsonl(run(root, "register", "cards-test", "--launcher-dir", str(bin_dir)))[
        0
    ]
    _assert(result["warnings"] == [], result)
    _assert(result["git"] == "unchanged", "re-register with no data change is a no-op")
    links = list((root / "by-url").iterdir())
    _assert(len(links) == 1 and links[0].is_symlink(), links)
    _assert((links[0] / "manifest.json").is_file(), "by-url symlink must resolve")
    launcher = bin_dir / "cards-test"
    _assert("almanac launcher" in launcher.read_text())
    _assert((bin_dir / "almanac").exists(), "engine symlink installed")
    log = subprocess.run(
        ["git", "log", "--oneline"], cwd=root, capture_output=True, text=True
    )
    _assert("register cards-test" in log.stdout, log.stdout)


def test_register_conflicts():
    root, bin_dir = registered_root()
    make_dataset(root, name="dupe", url="https://example.test/cards-test")
    proc = run(root, "register", "dupe", "--no-launcher")
    _assert(proc.returncode == 5, f"same url must conflict: {proc.stderr}")
    (bin_dir / "other").write_text("#!/bin/sh\n")
    other = make_dataset(root, name="other", url="https://example.test/other")
    manifest_before = (other / "manifest.json").read_bytes()
    links_before = {path.name for path in (root / "by-url").iterdir()}
    proc = run(root, "register", "other", "--launcher-dir", str(bin_dir))
    _assert(proc.returncode == 5, "foreign launcher file must not be overwritten")
    _assert(
        (other / "manifest.json").read_bytes() == manifest_before,
        "a refused registration must not stamp manifest metadata",
    )
    _assert(
        {path.name for path in (root / "by-url").iterdir()} == links_before,
        "a refused registration must not leave a by-url link",
    )


def test_list_query_show_search():
    root, _ = registered_root()
    rows = jsonl(run(root, "list"))
    _assert(rows[0]["name"] == "cards-test" and rows[0]["records"] == 3, rows)

    rows = jsonl(run(root, "query", "cards-test", "tier=b"))
    _assert([r["name"] for r in rows] == ["Bash"], rows)
    _assert(
        sorted(rows[0]) == ["cost", "n", "n_tier", "name", "seq", "tier"],
        rows[0],
    )

    rows = jsonl(run(root, "query", "cards-test", "name~strike", "tier=a,c"))
    _assert(len(rows) == 2, rows)

    full = jsonl(run(root, "query", "cards-test", "tier=b", "--full"))
    _assert("text" in full[0], full)

    # Unrecognized args are full-text needles over the search fields.
    rows = jsonl(run(root, "query", "cards-test", "vulnerable"))
    _assert([r["name"] for r in rows] == ["Bash"], rows)
    rows = jsonl(run(root, "query", "cards-test", "~strike"))
    _assert(len(rows) == 2, rows)
    # Bare words extend the preceding ~needle: one 'deal 6' needle.
    rows = jsonl(run(root, "query", "cards-test", "~deal", "6"))
    _assert([r["name"] for r in rows] == ["Strike"], rows)
    # Two ~needles AND together.
    rows = jsonl(run(root, "query", "cards-test", "~strike", "~more"))
    _assert([r["name"] for r in rows] == ["Perfected Strike"], rows)

    record = jsonl(run(root, "show", "cards-test", "bash"))[0]
    _assert(record["name"] == "Bash" and "text" in record)
    proc = run(root, "show", "cards-test", "stri")
    _assert(proc.returncode == 4, "ambiguous substring must not guess")
    detail = json.loads(proc.stderr)["error"]["detail"]
    _assert(len(detail["candidates"]) == 2, detail)

    rows = jsonl(run(root, "search", "cards-test", "vulnerable"))
    _assert(len(rows) == 1 and rows[0]["matched"].startswith("text:"), rows)

    empty = jsonl(run(root, "query", "cards-test", "tier=z"))
    _assert(empty == [{"count": 0, "of": "records"}], "definitive empty state")


def test_help_and_no_args():
    root, _ = registered_root()
    proc = run(root)
    _assert(proc.returncode == 0, "no args prints help, not a usage error")
    _assert("examples:" in proc.stdout and "cards-test" in proc.stdout, proc.stdout)
    proc = run(root, "--help")
    _assert("cards-test" in proc.stdout, "top-level --help lists datasets")
    _assert(
        proc.stdout.rstrip().endswith("acli: 1 complete repl toon"),
        "--help ends with the capability line",
    )
    _assert("exit codes:" in proc.stdout and "75" in proc.stdout, proc.stdout)
    proc = run(root, "help", "cards-test")
    _assert(proc.returncode == 0, proc.stderr)
    _assert("sample rows:" in proc.stdout and "Strike" in proc.stdout, proc.stdout)
    _assert("~needle" in proc.stdout, "filter syntax incl. needle grouping documented")
    _assert(
        proc.stdout.rstrip().endswith("acli: 1 complete repl toon"),
        "dataset help also ends with the capability line",
    )

    broken = root / "broken"
    broken.mkdir()
    (broken / "manifest.json").write_text("{not json")
    proc = run(root, "--help")
    _assert(proc.returncode == 0, "one broken dataset must not disable global help")
    _assert("cards-test" in proc.stdout and "acli: 1" in proc.stdout, proc.stdout)


def test_help_examples_quote_spaced_filter_values():
    root = Path(tempfile.mkdtemp(prefix="almanac-test-"))
    data = {
        "cards": [
            {
                "name": "Storybook",
                "tier": "Always Amazing",
                "cost": 1,
                "text": "Example card.",
            }
        ]
    }
    make_dataset(root, name="spaced", data=data)
    proc = run(root, "help", "spaced")
    _assert(proc.returncode == 0, proc.stderr)
    _assert("'tier=Always Amazing'" in proc.stdout, proc.stdout)


def test_sequence_numbers_and_supersets():
    root = Path(tempfile.mkdtemp(prefix="almanac-test-"))
    data = {
        "cards": [
            {"name": "A", "tier": "S", "cost": 1, "text": "a"},
            {"name": "B", "tier": "S", "cost": 2, "text": "b"},
            {"name": "C", "tier": "A", "cost": 1, "text": "c"},
            {"name": "D", "tier": "S", "cost": 1, "text": "d"},
        ],
    }
    directory = make_dataset(root, name="seqs", data=data)
    manifest = json.loads((directory / "manifest.json").read_text())
    manifest["schema"]["ordinals"] = [["tier"], ["tier", "cost"]]
    (directory / "manifest.json").write_text(json.dumps(manifest))
    _assert(run(root, "register", "seqs", "--no-launcher").returncode == 0)

    rows = jsonl(run(root, "query", "seqs", "tier=S"))
    # seq is dataset-wide reading order; n is position within this result;
    # n_tier ranks within all tier=S; n_tier_cost within tier+cost cell.
    _assert([r["seq"] for r in rows] == [1, 2, 4], rows)
    _assert([r["n"] for r in rows] == [1, 2, 3], rows)
    _assert([r["n_tier"] for r in rows] == [1, 2, 3], rows)
    _assert([r["n_tier_cost"] for r in rows] == [1, 1, 2], rows)

    # A single show carries the item's rank in every declared superset.
    d = jsonl(run(root, "show", "seqs", "D"))[0]
    _assert(d["seq"] == 4 and d["n_tier"] == 3 and d["n_tier_cost"] == 2, d)

    # Ordinal columns are in-memory only: data.json is untouched.
    stored = json.loads((directory / "data.json").read_text())["cards"][0]
    _assert("seq" not in stored and "n_tier" not in stored, stored)


def test_derived_ordinals_override_stored_values_in_memory():
    root = Path(tempfile.mkdtemp(prefix="almanac-test-"))
    data = {
        "cards": [
            {"name": "A", "tier": "S", "cost": 1, "text": "a", "n_tier": 999},
            {"name": "B", "tier": "S", "cost": 2, "text": "b"},
        ],
    }
    directory = make_dataset(root, name="derived", data=data)
    _assert(run(root, "register", "derived", "--no-launcher").returncode == 0)

    rows = jsonl(run(root, "query", "derived", "tier=S"))
    _assert([row["n_tier"] for row in rows] == [1, 2], rows)
    stored = json.loads((directory / "data.json").read_text())["cards"][0]
    _assert(stored["n_tier"] == 999, "derived values stay in-memory only")


def test_check_and_update_cycle():
    root, _ = registered_root()
    fixture = root / "fixture.json"
    fixture.write_text(json.dumps(CARDS))

    proc = run(root, "check", "cards-test", source=fixture)
    _assert(proc.returncode == 0 and jsonl(proc)[0]["changed"] is False, proc.stdout)

    changed = {
        "cards": CARDS["cards"]
        + [{"name": "Whirlwind", "tier": "S", "cost": 0, "text": "X hits."}]
    }
    fixture.write_text(json.dumps(changed))
    proc = run(root, "check", "cards-test", source=fixture)
    _assert(proc.returncode == 3 and jsonl(proc)[0]["changed"] is True, proc.stdout)

    result = jsonl(run(root, "update", "cards-test", source=fixture))[0]
    _assert(result["changed"] is True and result["records"] == 4, result)
    _assert(result["git"] == "committed", result)
    _assert(run(root, "check", "cards-test", source=fixture).returncode == 0)

    fixture.write_text(json.dumps({"cards": []}))
    proc = run(root, "update", "cards-test", source=fixture)
    _assert(proc.returncode == 70, "zero records must be refused by default")
    proc = run(root, "update", "cards-test", "--allow-empty", source=fixture)
    _assert(proc.returncode == 0 and jsonl(proc)[0]["records"] == 0, proc.stderr)

    fixture.write_text("{}")
    proc = run(root, "check", "cards-test", source=fixture)
    _assert(
        proc.returncode == 70,
        "check must reject extractor JSON that no longer fits the record schema",
    )


def test_refresh_mode_gates():
    root, _ = registered_root()
    make_dataset(root, name="frozen-notes", refresh="frozen")
    _assert(run(root, "register", "frozen-notes", "--no-launcher").returncode == 0)
    proc = run(root, "check", "frozen-notes")
    _assert(proc.returncode == 69, "frozen dataset cannot check")
    make_dataset(root, name="saved-page", refresh="manual")
    _assert(run(root, "register", "saved-page", "--no-launcher").returncode == 0)
    proc = run(root, "update", "saved-page")
    _assert(proc.returncode == 69, "manual without --source cannot refresh")
    _assert("--source" in json.loads(proc.stderr)["error"]["message"])


def test_completion():
    root, _ = registered_root()
    names = jsonl(run(root, "--acli-complete", "show", "car"))
    _assert([r["completion"] for r in names] == ["cards-test"], names)
    _assert(names[0]["help"] == "Test cards", "dataset candidates carry the title")
    keys = jsonl(run(root, "--acli-complete", "show", "cards-test", "b"))
    _assert([r["completion"] for r in keys] == ["Bash"], keys)
    _assert(keys[0]["help"] == "B · 2", "key candidates summarize the other columns")
    image_keys = jsonl(run(root, "--acli-complete", "image", "cards-test", "b"))
    _assert([r["completion"] for r in image_keys] == ["Bash"], image_keys)
    fuzzy = jsonl(run(root, "--acli-complete", "show", "cards-test", "ash"))
    _assert(
        [r["completion"] for r in fuzzy] == ["Bash"],
        "substring fallback mirrors show's own matching",
    )
    fields = jsonl(run(root, "--acli-complete", "query", "cards-test", "ti"))
    _assert([r["completion"] for r in fields] == ["tier="], fields)
    _assert(fields[0]["nospace"] is True, "field= must not get a space appended")
    _assert("3 distinct" in fields[0]["help"], fields)
    values = jsonl(run(root, "--acli-complete", "query", "cards-test", "tier="))
    # Page order (C, B, A here), never alphabetized: order is the ranking.
    _assert([r["completion"] for r in values] == ["tier=C", "tier=B", "tier=A"], values)
    _assert(values[0]["help"] == "1 records", values)
    verbs = [r["completion"] for r in jsonl(run(root, "--acli-complete", "che"))]
    _assert(verbs == ["check"], verbs)


def test_completion_hint_rows():
    root, _ = registered_root()
    rows = jsonl(run(root, "--acli-complete", "query", "cards-test", ""))
    _assert(rows[0]["kind"] == "hint" and rows[0]["completion"] == "", rows)
    _assert("FIELD=VALUE" in rows[0]["help"], "empty filter slot leads with syntax")
    _assert(
        [r["completion"] for r in rows[1:]] == ["tier=", "cost="],
        "filter fields follow in schema order",
    )
    misses = jsonl(run(root, "--acli-complete", "show", "cards-test", "zzz"))
    _assert(misses[0]["kind"] == "hint" and "zzz" in misses[0]["help"], misses)


def test_repl_batch_lines():
    root, _ = registered_root()
    env = dict(os.environ, ALMANAC_ROOT=str(root))
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--repl"],
        input="query cards-test tier=b\nexit\n",
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    _assert(proc.returncode == 0, proc.stderr)
    _assert('"name": "Bash"' in proc.stdout, "repl defaults to pretty output")
    _assert(
        run(root, "--repl", "nope").returncode == 4,
        "a bad dataset binding fails loud before the loop",
    )


def test_launcher_dispatch():
    root, bin_dir = registered_root()
    add_images(root / "cards-test")
    env = dict(
        os.environ, ALMANAC_ROOT=str(root), PATH=f"{bin_dir}:{os.environ['PATH']}"
    )
    launcher = str(bin_dir / "cards-test")

    proc = subprocess.run([launcher], capture_output=True, text=True, env=env)
    _assert(
        json.loads(proc.stdout.splitlines()[0])["records"] == 3, "bare launcher = info"
    )

    proc = subprocess.run([launcher, "tier=b"], capture_output=True, text=True, env=env)
    _assert(
        json.loads(proc.stdout.splitlines()[0])["name"] == "Bash", "filters = query"
    )

    proc = subprocess.run(
        [launcher, "show", "bash"], capture_output=True, text=True, env=env
    )
    _assert(json.loads(proc.stdout.splitlines()[0])["cost"] == 2, proc.stdout)

    proc = subprocess.run(
        [launcher, "image", "bash"], capture_output=True, text=True, env=env
    )
    image_result = json.loads(proc.stdout.splitlines()[0])
    _assert(
        image_result["record"] == "Bash" and not image_result["rendered"], proc.stdout
    )

    for leading in (["--pretty"], ["--format", "pretty"], ["--format=pretty"]):
        proc = subprocess.run(
            [launcher, *leading, "show", "bash"],
            capture_output=True,
            text=True,
            env=env,
        )
        _assert(
            proc.stdout.startswith("{\n"),
            f"{leading} must reach the engine as a format flag:\n{proc.stdout}",
        )
        _assert(
            json.loads(proc.stdout)["cost"] == 2,
            f"leading standard flags must not change which verb runs: {leading}\n"
            f"{proc.stdout}{proc.stderr}",
        )

    proc = subprocess.run([launcher, "-h"], capture_output=True, text=True, env=env)
    _assert(proc.returncode == 0, proc.stderr)
    _assert("launcher bound to" in proc.stdout, "launcher -h explains the binding")
    proc = subprocess.run(
        [launcher, "--pretty", "help"],
        capture_output=True,
        text=True,
        env=env,
    )
    _assert(proc.returncode == 0 and "launcher bound to" in proc.stdout, proc.stderr)

    proc = subprocess.run(
        [launcher, "vulnerable"], capture_output=True, text=True, env=env
    )
    _assert(
        json.loads(proc.stdout.splitlines()[0])["name"] == "Bash", "bare word = search"
    )

    proc = subprocess.run(
        [launcher, "--acli-complete", "show", "b"],
        capture_output=True,
        text=True,
        env=env,
    )
    _assert(proc.returncode == 0, proc.stderr)
    _assert([json.loads(l)["completion"] for l in proc.stdout.splitlines()] == ["Bash"])
    proc = subprocess.run(
        [launcher, "--acli-complete", "s"],
        capture_output=True,
        text=True,
        env=env,
    )
    completions = [json.loads(line)["completion"] for line in proc.stdout.splitlines()]
    _assert("show" in completions and "search" in completions, completions)

    _assert(
        "# acli: 1 complete repl toon" in Path(launcher).read_text()[:200],
        "launcher head carries the zero-execution capability marker",
    )
    _assert(
        "case " not in Path(launcher).read_text(),
        "generated launcher delegates all argument parsing to the engine",
    )
    proc = subprocess.run(
        [launcher, "--repl"],
        input="tier=b\nshow bash\n~vulnerable\nexit\n",
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    _assert(proc.returncode == 0, proc.stderr)
    _assert(
        proc.stdout.count('"name": "Bash"') == 3,
        f"launcher --repl keeps the launcher grammar:\n{proc.stdout}\n{proc.stderr}",
    )


def _collect_tests():
    return [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]


def main(argv):
    verbose = "-v" in argv
    pattern = None
    if "-k" in argv:
        pattern = argv[argv.index("-k") + 1]
    tests = [(n, f) for n, f in _collect_tests() if pattern is None or pattern in n]
    passed = failed = 0
    failures = []
    start_total = time.time()
    for name, fn in tests:
        t0 = time.time()
        try:
            fn()
            passed += 1
            if verbose:
                print(f"PASS  {name}  ({time.time() - t0:.2f}s)")
            else:
                print(".", end="", flush=True)
        except Exception:
            failed += 1
            tb = traceback.format_exc()
            failures.append((name, tb))
            if verbose:
                print(f"FAIL  {name}  ({time.time() - t0:.2f}s)")
                print(tb)
            else:
                print("F", end="", flush=True)
    if not verbose:
        print()
    print()
    if failures:
        print("=" * 60)
        print(f"{len(failures)} FAILURE(S):")
        for name, tb in failures:
            print(f"\n--- {name} ---")
            print(tb)
    print(f"\n{passed} passed, {failed} failed in {time.time() - start_total:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
