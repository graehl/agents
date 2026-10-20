"""The repo-view base's script through its real command line, on a scratch Git repository."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from composition import TemplateLibrary, materialize

LIBRARY = Path(__file__).resolve().parent
SOURCE = LIBRARY / "bases/repo-view/files/repo_view.py"
HAS_PANDOC = shutil.which("pandoc") is not None


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


class RepoViewTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="repo-view-test-")
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name) / "demo"
        self.write(
            "README.md",
            "# Demo\n\nSee [the guide](docs/guide.md) and ![logo](img/logo.svg).\n",
        )
        self.write(
            "docs/guide.md",
            "---\ntitle: The Guide\n---\n[sibling](other.md#part), [listing](sub/), [up](../README.md).\n",
        )
        self.write("docs/other.md", "# Other\n")
        self.write("docs/sub/a.txt", "a\n")
        self.write("img/logo.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>\n')
        self.write("img/unlinked.txt", "not linked\n")
        # Vendored as a created project would hold it.
        self.script = self.repo / "scripts/repo_view.py"
        self.script.parent.mkdir()
        shutil.copy2(SOURCE, self.script)
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")

    def write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def run_script(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )

    def serve(self, *args: str, env: dict | None = None) -> str:
        port = free_port()
        log = (self.repo.parent / f"serve-{port}.err").open("w")
        self.addCleanup(log.close)
        process = subprocess.Popen(
            [sys.executable, str(self.script), "serve", "--port", str(port), *args],
            cwd=self.repo,
            stdout=log,
            stderr=log,
            env=env,
        )
        self.addCleanup(process.wait)
        self.addCleanup(process.terminate)
        base = f"http://127.0.0.1:{port}"
        for _ in range(100):
            try:
                urllib.request.urlopen(base + "/healthz", timeout=1).read()
                return base
            except OSError:
                if process.poll() is not None:
                    self.fail(
                        f"serve exited: {(self.repo.parent / f'serve-{port}.err').read_text()}"
                    )
                time.sleep(0.05)
        self.fail("serve did not become ready")

    def get(self, url: str, cookie: str | None = None) -> tuple[int, dict, str]:
        request = urllib.request.Request(
            url, headers={"Cookie": cookie} if cookie else {}
        )
        try:
            with OPENER.open(request, timeout=10) as reply:
                return (
                    reply.status,
                    dict(reply.headers),
                    reply.read().decode("utf-8", "replace"),
                )
        except urllib.error.HTTPError as error:
            with error:
                return (
                    error.code,
                    dict(error.headers),
                    error.read().decode("utf-8", "replace"),
                )

    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_live_view_serves_documents_at_their_own_paths(self) -> None:
        base = self.serve()
        status, _, page = self.get(base + "/docs/guide.md")
        self.assertEqual(status, 200)
        self.assertIn("<h1>The Guide</h1>", page)
        self.assertIn('href="other.md#part"', page)  # authored links need no rewriting
        self.assertIn('<a href="../">demo</a>', page)
        self.assertIn('const key = "ya_access"', page)
        status, headers, _ = self.get(base + "/docs?ya_access=T")
        self.assertEqual((status, headers["Location"]), (302, "docs/?ya_access=T"))
        self.assertEqual(self.get(base + "/docs/sub/a.txt")[0], 200)
        self.assertEqual(self.get(base + "/.git/config")[0], 404)

    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_reachable_set_grows_on_demand_and_never_shrinks(self) -> None:
        base = self.serve()
        self.assertEqual(self.get(base + "/img/unlinked.txt")[0], 404)
        self.write("docs/other.md", "# Other\n\n[now linked](../img/unlinked.txt)\n")
        self.assertEqual(self.get(base + "/img/unlinked.txt")[0], 200)
        self.write("docs/other.md", "# Other\n")
        self.assertEqual(self.get(base + "/img/unlinked.txt")[0], 200)

    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_static_build_is_a_self_contained_publishable_closure(self) -> None:
        built = self.run_script("build")
        self.assertEqual(built.returncode, 0, built.stderr)
        site = self.repo / "_site"
        guide = (site / "docs/guide.md.html").read_text()
        self.assertIn('href="other.md.html#part"', guide)
        self.assertIn('href="sub/index.html"', guide)
        self.assertIn('href="../index.html"', guide)
        self.assertTrue((site / "img/logo.svg").is_file())
        self.assertTrue((site / "docs/sub/a.txt").is_file())
        self.assertFalse((site / "img/unlinked.txt").exists())
        published = "".join(p.read_text() for p in site.rglob("*.html"))
        self.assertNotIn("ya_access", published)
        self.assertEqual(self.git("status", "--porcelain"), "")

        base = self.serve("--static")
        status, _, page = self.get(base + "/docs/guide.md")
        self.assertEqual(status, 200)
        self.assertIn('const key = "ya_access"', page)
        self.assertEqual(self.get(base + "/img/unlinked.txt")[0], 404)

    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_failed_build_keeps_the_live_site(self) -> None:
        self.assertEqual(self.run_script("build").returncode, 0)
        site = self.repo / "_site"
        before = (site / "docs/guide.md.html").read_text()
        self.write("docs/guide.md", "# Changed\n")

        too_big = self.run_script("build", "--max-bytes", "1")
        self.assertIn("nothing replaced", too_big.stderr)
        self.assertEqual((site / "docs/guide.md.html").read_text(), before)

        # The swap fails after the live site was retired: it must come back.
        failing_swap = (
            "import pathlib, runpy, sys\n"
            "rename = pathlib.Path.rename\n"
            "def fail(self, target):\n"
            "    if self.name.endswith('.new'):\n"
            "        raise OSError('injected swap failure')\n"
            "    return rename(self, target)\n"
            "pathlib.Path.rename = fail\n"
            "sys.argv = [sys.argv[1], 'build']\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')\n"
        )
        swap = subprocess.run(
            [sys.executable, "-c", failing_swap, str(self.script)],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertIn("injected swap failure", swap.stderr)
        self.assertEqual((site / "docs/guide.md.html").read_text(), before)
        self.assertFalse((self.repo / "_site.new").exists())
        self.assertFalse((self.repo / "_site.old").exists())

        # A site stranded as .old by an interrupted earlier swap is recovered.
        site.rename(self.repo / "_site.old")
        self.assertIn(
            "nothing replaced", self.run_script("build", "--max-bytes", "1").stderr
        )
        self.assertEqual((site / "docs/guide.md.html").read_text(), before)

    def test_app_json_token_is_shown_and_optionally_required(self) -> None:
        self.write(
            ".project-template/app.json", json.dumps({"yaAccess": "secret-token"})
        )
        base = self.serve("--require-access")
        self.assertEqual(self.get(base + "/img/logo.svg")[0], 401)
        self.assertEqual(self.get(base + "/img/logo.svg?ya_access=wrong")[0], 401)
        status, headers, page = self.get(base + "/?ya_access=secret-token")
        self.assertEqual(status, 200)
        self.assertIn("ya_app_access=secret-token", headers["Set-Cookie"])
        self.assertIn('<meta name="ya-access" content="secret-token">', page)
        self.assertEqual(
            self.get(base + "/img/logo.svg", cookie="ya_app_access=secret-token")[0],
            200,
        )
        self.write(".project-template/app.json", json.dumps({"yaAccess": "rotated"}))
        self.assertEqual(
            self.get(base + "/img/logo.svg", cookie="ya_app_access=secret-token")[0],
            401,
        )

    def test_listing_skips_untracked_trees_but_follows_explicit_links(self) -> None:
        self.write("README.md", "# Demo\n[listing](docs/) [built](output/index.html)\n")
        self.write("docs/new.txt", "new file in a tracked directory")
        self.write("docs/scratch/hidden.txt", "untracked tree")
        self.write("output/index.html", '<img src="image.svg">')
        self.write("output/image.svg", "<svg/>")
        self.write("output/secret.txt", "not linked")
        base = self.serve()
        status, _, page = self.get(base + "/docs/")
        self.assertEqual(status, 200)
        self.assertIn("new.txt", page)
        self.assertNotIn("scratch", page)
        self.assertEqual(self.get(base + "/docs/scratch/hidden.txt")[0], 404)
        self.assertEqual(self.get(base + "/output/index.html")[0], 200)
        self.assertEqual(self.get(base + "/output/image.svg")[0], 200)
        self.assertEqual(self.get(base + "/output/secret.txt")[0], 404)
        self.git("add", "docs/scratch/hidden.txt")
        self.assertIn("scratch/", self.get(base + "/docs/")[2])
        self.assertEqual(self.get(base + "/docs/scratch/hidden.txt")[0], 200)

    def test_discovered_file_does_not_wait_for_unrelated_directory_scan(self) -> None:
        self.write("README.md", "# Demo\n[slow](slow/) [logo](img/logo.svg)\n")
        self.write("slow/tracked.txt", "tracked")
        self.git("add", "slow/tracked.txt")
        real_git = shutil.which("git")
        self.write(
            ".tools/git",
            f"#!{sys.executable}\n"
            "import os, sys, time\nfrom pathlib import Path\n"
            "if sys.argv[-1] == 'slow/':\n"
            "    Path('.scan-started').touch()\n"
            "    deadline = time.monotonic() + 10\n"
            "    while not Path('.scan-release').exists() and time.monotonic() < deadline:\n"
            "        time.sleep(.01)\n"
            f"os.execv({real_git!r}, [{real_git!r}, *sys.argv[1:]])\n",
        )
        (self.repo / ".tools/git").chmod(0o755)
        base = self.serve(
            env={**os.environ, "PATH": f"{self.repo / '.tools'}:{os.environ['PATH']}"}
        )
        with ThreadPoolExecutor(max_workers=1) as clients:
            slow = clients.submit(self.get, base + "/slow/")
            try:
                deadline = time.monotonic() + 5
                while not (self.repo / ".scan-started").exists():
                    self.assertLess(
                        time.monotonic(), deadline, "scan did not reach slow directory"
                    )
                    time.sleep(0.01)
                with urllib.request.urlopen(
                    base + "/img/logo.svg", timeout=1
                ) as response:
                    self.assertEqual(response.status, 200)
            finally:
                (self.repo / ".scan-release").touch()
            self.assertEqual(slow.result()[0], 200)

    def test_project_pages_seed_and_replace_the_root(self) -> None:
        self.write(
            "scripts/dash.py",
            "def pages(root):\n    return {'index.html': '<html><head></head><body>"
            '<a href="img/unlinked.txt">x</a></body></html>\'}\n',
        )
        base = self.serve("--pages", "scripts/dash.py:pages")
        status, _, page = self.get(base + "/")
        self.assertEqual(status, 200)
        self.assertIn("img/unlinked.txt", page)
        self.assertEqual(self.get(base + "/img/unlinked.txt")[0], 200)
        # An edited generator applies on the next request, well within --pages-max-age.
        self.write(
            "scripts/dash.py",
            "def pages(root):\n    return {'index.html': '<p>edited</p>'}\n",
        )
        self.assertIn("edited", self.get(base + "/")[2])
        self.write("scripts/dash.py", "def pages(root):\n    return {\n")
        status, _, page = self.get(base + "/")
        self.assertEqual(status, 200)
        self.assertIn("edited", page)

    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_breadcrumbs_open_the_project_page_section_showing_a_directory(
        self,
    ) -> None:
        self.write("docs/sub/deep/note.md", "# Note\n")
        self.write(
            "scripts/dash.py",
            "def pages(root):\n    return {'index.html': '<html><head></head><body>"
            '<details data-repo-dir="docs" id="sec-docs"></details>'
            '<a href="docs/sub/deep/note.md">n</a></body></html>\'}\n',
        )
        self.git("add", ".")
        # docs is marked; deep is neither marked nor linked, so it opens the
        # section of its nearest marked ancestor; the root crumb opens the root.
        # (Whether sub is a servable listing yet depends on discovery order.)
        docs = ' / <a href="../../../index.html#sec-docs">docs</a> / '
        deep = ' / <a href="../../../index.html#sec-docs">deep</a> / note.md</nav>'
        base = self.serve("--pages", "scripts/dash.py:pages")
        status, _, page = self.get(base + "/docs/sub/deep/note.md")
        self.assertEqual(status, 200)
        for crumb in ('<a href="../../../">demo</a>' + docs, deep):
            self.assertIn(crumb, page)
        done = self.run_script("build", "--pages", "scripts/dash.py:pages")
        self.assertEqual(done.returncode, 0, done.stderr)
        built = (self.repo / "_site/docs/sub/deep/note.md.html").read_text()
        # The build reaches the note straight from the page, never listing sub.
        static_crumbs = (
            '<a href="../../../index.html">demo</a>' + docs
            + '<a href="../../../index.html#sec-docs">sub</a>' + deep
        )  # fmt: skip
        self.assertIn(static_crumbs, built)

    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_symlinks_escaping_the_repository_are_never_served(self) -> None:
        secret = self.repo.parent / "secret.md"
        secret.write_text("# Secret outside the repository\n", encoding="utf-8")
        (self.repo / "docs/escape.md").symlink_to(secret)
        (self.repo / "docs/away").symlink_to(self.repo.parent, target_is_directory=True)
        (self.repo / "docs/inside.md").symlink_to(self.repo / "docs/other.md")
        self.write(
            "docs/other.md",
            "# Other\n\n[escape](escape.md) [away](away/secret.md) [inside](inside.md)\n",
        )
        base = self.serve()
        self.assertEqual(self.get(base + "/docs/escape.md")[0], 404)
        self.assertEqual(self.get(base + "/docs/away/secret.md")[0], 404)
        self.assertEqual(self.get(base + "/docs/inside.md")[0], 200)
        built = self.run_script("build")
        self.assertEqual(built.returncode, 0, built.stderr)
        published = "".join(
            path.read_text(errors="replace")
            for path in (self.repo / "_site").rglob("*")
            if path.is_file()
        )
        self.assertNotIn("Secret outside", published)
        self.assertTrue((self.repo / "_site/docs/inside.md.html").is_file())

    def test_enable_declares_the_app_without_clobbering_one(self) -> None:
        self.write(
            ".project-template/app.json",
            json.dumps({"kind": "static", "dir": "dist", "setup": ["x"]}),
        )
        refused = self.run_script("enable")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("--replace", refused.stderr)
        enabled = self.run_script("enable", "--replace", "--", "--root", "docs")
        self.assertEqual(enabled.returncode, 0, enabled.stderr)
        app = json.loads((self.repo / ".project-template/app.json").read_text())
        self.assertEqual(app["setup"], ["x"])
        service = app["service"]
        self.assertEqual(
            service["where"], {"kind": "process", "cwd": ".", "entry": "/"}
        )
        self.assertNotIn(
            "basePathEnv", service["serving"]
        )  # readable paths, not /p/<token>/
        self.assertEqual(service["start"]["argv"][2:], ["serve", "--root", "docs"])


class RepoViewCompositionTest(unittest.TestCase):
    @unittest.skipUnless(HAS_PANDOC, "pandoc renders documents")
    def test_created_project_builds_its_view_without_this_checkout(self) -> None:
        library = TemplateLibrary(LIBRARY.parent, LIBRARY.name)
        page = json.loads((LIBRARY / "templates/web-page/template.json").read_text())
        page.update(id="web-page-view", extends=[*page["extends"], "repo-view"])
        library.nodes["web-page-view"] = page
        library.directories["web-page-view"] = LIBRARY / "templates/web-page"
        composition = library.compose("web-page-view")
        self.assertIn(
            "instructions/repo-view.md", composition.files["AGENTS.md"].content.decode()
        )
        with tempfile.TemporaryDirectory(prefix="repo-view-created-") as temporary:
            project = materialize(
                composition, Path(temporary) / "made", "Made", "A page with a view"
            )
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            built = subprocess.run(
                [str(project / "scripts/repo_view.py"), "build"],
                check=False,
                cwd=project,
                capture_output=True,
                text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            self.assertTrue((project / "_site/index.html").is_file())


if __name__ == "__main__":
    unittest.main()
