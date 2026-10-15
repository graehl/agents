"""The repo-view base's script through its real command line, on a scratch Git repository."""

from __future__ import annotations

import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
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
        self.write("README.md", "# Demo\n\nSee [the guide](docs/guide.md) and ![logo](img/logo.svg).\n")
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
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True, text=True).stdout

    def run_script(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.script), *args], cwd=self.repo, capture_output=True, text=True, check=False
        )

    def serve(self, *args: str) -> str:
        port = free_port()
        log = (self.repo.parent / f"serve-{port}.err").open("w")
        self.addCleanup(log.close)
        process = subprocess.Popen(
            [sys.executable, str(self.script), "serve", "--port", str(port), *args],
            cwd=self.repo,
            stdout=subprocess.DEVNULL,
            stderr=log,
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
                    self.fail(f"serve exited: {(self.repo.parent / f'serve-{port}.err').read_text()}")
                time.sleep(0.05)
        self.fail("serve did not become ready")

    def get(self, url: str, cookie: str | None = None) -> tuple[int, dict, str]:
        request = urllib.request.Request(url, headers={"Cookie": cookie} if cookie else {})
        try:
            with OPENER.open(request, timeout=10) as reply:
                return reply.status, dict(reply.headers), reply.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as error:
            with error:
                return error.code, dict(error.headers), error.read().decode("utf-8", "replace")

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

    def test_app_json_token_is_shown_and_optionally_required(self) -> None:
        self.write(".project-template/app.json", json.dumps({"yaAccess": "secret-token"}))
        base = self.serve("--require-access")
        self.assertEqual(self.get(base + "/img/logo.svg")[0], 401)
        self.assertEqual(self.get(base + "/img/logo.svg?ya_access=wrong")[0], 401)
        status, headers, page = self.get(base + "/?ya_access=secret-token")
        self.assertEqual(status, 200)
        self.assertIn("ya_app_access=secret-token", headers["Set-Cookie"])
        self.assertIn('<meta name="ya-access" content="secret-token">', page)
        self.assertEqual(self.get(base + "/img/logo.svg", cookie="ya_app_access=secret-token")[0], 200)
        self.write(".project-template/app.json", json.dumps({"yaAccess": "rotated"}))
        self.assertEqual(self.get(base + "/img/logo.svg", cookie="ya_app_access=secret-token")[0], 401)

    def test_project_pages_seed_and_replace_the_root(self) -> None:
        self.write(
            "scripts/dash.py",
            "def pages(root):\n    return {'index.html': '<html><head></head><body>"
            "<a href=\"img/unlinked.txt\">x</a></body></html>'}\n",
        )
        base = self.serve("--pages", "scripts/dash.py:pages")
        status, _, page = self.get(base + "/")
        self.assertEqual(status, 200)
        self.assertIn("img/unlinked.txt", page)
        self.assertEqual(self.get(base + "/img/unlinked.txt")[0], 200)

    def test_enable_declares_the_app_without_clobbering_one(self) -> None:
        self.write(".project-template/app.json", json.dumps({"kind": "static", "dir": "dist", "setup": ["x"]}))
        refused = self.run_script("enable")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("--replace", refused.stderr)
        enabled = self.run_script("enable", "--replace", "--", "--root", "docs")
        self.assertEqual(enabled.returncode, 0, enabled.stderr)
        app = json.loads((self.repo / ".project-template/app.json").read_text())
        self.assertEqual(app["setup"], ["x"])
        service = app["service"]
        self.assertEqual(service["where"], {"kind": "process", "cwd": ".", "entry": "/"})
        self.assertNotIn("basePathEnv", service["serving"])  # readable paths, not /p/<token>/
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
        self.assertIn("instructions/repo-view.md", composition.files["AGENTS.md"].content.decode())
        with tempfile.TemporaryDirectory(prefix="repo-view-created-") as temporary:
            project = materialize(composition, Path(temporary) / "made", "Made", "A page with a view")
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
