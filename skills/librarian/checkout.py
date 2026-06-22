#!/usr/bin/env python3
"""Cache and refresh remote git repositories under ~/.cache/checkouts."""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import NoReturn


def die(message: str, code: int = 2) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_repo(repo_input: str) -> tuple[str, str, str]:
    repo_input = repo_input.strip().split("?", 1)[0].split("#", 1)[0]

    if repo_input.startswith("git@") and ":" in repo_input:
        host, path = repo_input[len("git@") :].split(":", 1)
    elif repo_input.startswith("ssh://"):
        host, _, path = repo_input[len("ssh://") :].partition("/")
        host = host.split("@", 1)[-1]
    elif repo_input.startswith(("http://", "https://")):
        host, _, path = repo_input.split("://", 1)[1].partition("/")
    elif "/" in repo_input:
        first = repo_input.split("/", 1)[0]
        if "." in first or first == "localhost":
            host, path = repo_input.split("/", 1)
        else:
            host = os.environ.get("LIBRARIAN_DEFAULT_HOST", "github.com")
            path = repo_input
    else:
        die(f"unsupported repository format: {repo_input}")

    host = host.split("@", 1)[-1]
    path = path.strip("/")
    parts = [part for part in path.split("/") if part]

    # For GitHub-like deep links, cache the repository, not the page path.
    if len(parts) >= 3 and parts[2] in (
        "tree",
        "blob",
        "pull",
        "issues",
        "commit",
        "actions",
        "releases",
        "compare",
        "wiki",
    ):
        parts = parts[:2]

    if parts and parts[-1].endswith(".git"):
        parts[-1] = parts[-1][:-4]

    if len(parts) < 2:
        die(f"repository path must contain at least org/repo: {path}")

    org = "/".join(parts[:-1])
    repo = parts[-1]
    if not host or not org or not repo:
        die(f"failed to parse repository: {repo_input}")

    return host, org, repo


def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ensure a cached git checkout exists under ~/.cache/checkouts."
    )
    parser.add_argument("repo")
    parser.add_argument("--path-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--force-update", action="store_true")
    parser.add_argument(
        "--update-interval",
        type=int,
        default=os.environ.get("LIBRARIAN_UPDATE_INTERVAL", "300"),
        help="minimum seconds between updates (default: 300)",
    )
    args = parser.parse_args()

    repo_input = str(args.repo)
    force_update = bool(args.force_update)
    update_interval = int(args.update_interval)
    if update_interval < 0:
        die("update interval must be a non-negative integer")

    host, org, repo = parse_repo(repo_input)

    cache_root = Path(os.environ.get("LIBRARIAN_CACHE_ROOT", "~/.cache/checkouts")).expanduser()
    checkout_path = cache_root / host / org / repo
    origin_url = f"https://{host}/{org}/{repo}.git"

    checkout_path.parent.mkdir(parents=True, exist_ok=True)

    if not (checkout_path / ".git").is_dir():
        git("clone", "--filter=blob:none", origin_url, str(checkout_path))

    if not (checkout_path / ".git").is_dir():
        die(f"checkout path is not a git repository: {checkout_path}", code=3)

    current_origin = (git("remote", "get-url", "origin", cwd=checkout_path, check=False).stdout or "").strip()
    if not current_origin:
        git("remote", "add", "origin", origin_url, cwd=checkout_path)
    elif current_origin != origin_url:
        git("remote", "set-url", "origin", origin_url, cwd=checkout_path)

    last_fetch_file = checkout_path / ".git" / "librarian-last-fetch"
    now = int(time.time())
    needs_update = True

    if last_fetch_file.is_file() and not force_update:
        try:
            needs_update = now - int(last_fetch_file.read_text().strip()) >= update_interval
        except ValueError:
            pass

    if needs_update:
        git("fetch", "--prune", "--tags", "origin", cwd=checkout_path)
        last_fetch_file.write_text(f"{now}\n")

        branch = (git("symbolic-ref", "--short", "-q", "HEAD", cwd=checkout_path, check=False).stdout or "").strip()
        upstream = (
            git(
                "rev-parse",
                "--abbrev-ref",
                "--symbolic-full-name",
                "@{u}",
                cwd=checkout_path,
                check=False,
            ).stdout
            or ""
        ).strip()
        dirty = (
            git("status", "--porcelain", "--untracked-files=no", cwd=checkout_path, check=False).stdout or ""
        ).strip()

        if branch and upstream and not dirty:
            git("merge", "--ff-only", upstream, cwd=checkout_path, check=False)

    print(checkout_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
