"""Aim text-dump writer for agentctl runs.

For every tracked agentctl run, writes one entry to
``runs/aim/<experiment>/`` matching the ``aim-text-dump-v1`` schema:

- ``manifest.jsonl`` — appended one line per run
- ``runs/<ref>.json`` — full run record
- ``texts/<ref>/meta.markdown.md`` — meta-markdown snapshot

These dumps are the authoritative branch record. Live ``.aim/`` repos are
rebuilt from them downstream via ``import_aim_text.py``; this plugin therefore
does not call the Aim SDK at runtime, even if it happens to be installed.
Importing the module does not require the Aim SDK.

Default-on. Opt out per-run with ``--no-aim`` (e.g. trivial launches the user
runs through ``agentctl`` only for the launcher and permission story).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import agentctl


_BANNER_PRINTED = False


def _maybe_print_install_hint() -> None:
    """One-line FYI on first start when the Aim SDK is absent. Live UI is
    optional — record dumps are written without it — but the hint is useful for
    users who want ``aim up`` browsing of the materialized repo."""
    global _BANNER_PRINTED
    if _BANNER_PRINTED:
        return
    _BANNER_PRINTED = True
    try:
        import aim  # noqa: F401
    except Exception:
        print(
            "agentctl: Aim SDK not installed; runs/aim/ records still written. "
            "Optional UI: pip install aim",
            file=sys.stderr,
        )


def _experiment_for(state: dict) -> str:
    return state.get("experiment") or state["job"]


def _ref_for(state: dict) -> str:
    """Stable dump ref. Defaults to agentctl run_id; user may rename later."""
    return state["run_id"]


def _aim_hash_for(state: dict) -> str:
    """Synthetic 24-hex hash deterministic from run_id. Distinct from real Aim
    hashes (which are also 24-hex) only by being reproducible — collisions
    within our own dumps are impossible because run_ids are unique."""
    return hashlib.md5(state["run_id"].encode()).hexdigest()[:24]


def _dump_root(state: dict) -> Path:
    return agentctl.ROOT / "runs" / "aim" / _experiment_for(state)


def _record_path(state: dict) -> Path:
    return _dump_root(state) / "runs" / f"{_ref_for(state)}.json"


def _text_relpath(state: dict) -> str:
    return f"texts/{_ref_for(state)}/meta.markdown.md"


def _text_abspath(state: dict) -> Path:
    return _dump_root(state) / _text_relpath(state)


def _manifest_path(state: dict) -> Path:
    return _dump_root(state) / "manifest.jsonl"


def _build_record(state: dict, meta_text: str) -> dict:
    ref = _ref_for(state)
    aim_hash = _aim_hash_for(state)
    experiment = _experiment_for(state)
    tags = ["agentctl", *state.get("tags", [])]
    output_path = state.get("output_path", "")
    meta_path = state.get("meta_path", "")
    record = {
        "identity": {
            "agentctl_run_id": state["run_id"],
            "experiment": experiment,
            "run_name": f"{state['job']}/{state['run_id']}",
            "tags": tags,
        },
        "metrics": [],
        "params": {
            "agentctl": {
                "headline_file": state.get("headline_path", ""),
                "job": state["job"],
                "mode": state.get("mode", ""),
                "output": output_path,
                "run_id": state["run_id"],
                "step_id": "",
            },
            "command": {
                "argv": state["argv"],
                "cwd": state["cwd"],
                "text": agentctl.command_string(state["argv"]),
            },
            "inputs": dict(state.get("inputs") or {}),
            "machine": {
                "git_branch": state.get("git_branch", ""),
                "git_commit": state.get("git_commit", ""),
                "pid": str(state["pid"]),
                "started_at": state["started_at"],
            },
            "meta": {
                "format": "artifact_meta.md",
                "path": meta_path,
            },
            "notes": [
                "Created by agentctl at launch; output-specific metadata may overwrite or extend this file.",
            ],
            "output": {
                "log_path": state.get("log_path", ""),
                "meta_path": meta_path,
                "path": output_path,
                "title": f"{state['job']} {state['run_id']}",
            },
            "outputs": dict(state.get("outputs") or {}),
            "related": {
                "agentctl-state": state["state_path"],
            },
            "request_plan": [],
            "result": {},
            "script": dict(state.get("script") or {}),
            "setup": {
                "job": state["job"],
                "launch_status": state.get("status", "running"),
                "run_id": state["run_id"],
            },
        },
        "ref": ref,
        "schema": "aim-text-dump-v1",
        "source": {
            "aim_repo": ".",
            "aim_run_hash": aim_hash,
            "exported_at": agentctl.utc_now(),
        },
        "texts": [
            {"name": "meta.markdown", "path": _text_relpath(state)},
        ],
    }
    if state.get("parent_run"):
        record["parent_run"] = state["parent_run"]
    if state.get("propagate"):
        record["propagate"] = dict(state["propagate"])
    return record


def _manifest_entry(state: dict) -> dict:
    return {
        "agentctl_run_id": state["run_id"],
        "aim_run_hash": _aim_hash_for(state),
        "dump": f"runs/{_ref_for(state)}.json",
        "experiment": _experiment_for(state),
        "metrics": 0,
        "ref": _ref_for(state),
        "run_name": f"{state['job']}/{state['run_id']}",
        "texts": 1,
    }


def _write_dump(state: dict, meta_text: str) -> Path:
    record = _build_record(state, meta_text)
    rec_path = _record_path(state)
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    text_path = _text_abspath(state)
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_text(meta_text, encoding="utf-8")
    manifest = _manifest_path(state)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    # POSIX append-write of a single short line is atomic up to PIPE_BUF (~4096).
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(_manifest_entry(state), sort_keys=True) + "\n")
    return rec_path


# ---- agentctl plugin hooks (all optional; base calls via getattr) ----


def register_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--no-aim",
        action="store_true",
        help="Skip writing the Aim-format run-record dump under runs/aim/.",
    )
    parser.add_argument(
        "--experiment",
        default="",
        help="Group records under runs/aim/<experiment>/. Defaults to <job>.",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Tag added to the run record (may repeat).",
    )


def default_output_path(args, run_dir):
    """Tracked runs need an output path so the .meta.md anchor exists.
    Trivial (--no-aim) runs do not."""
    if getattr(args, "no_aim", False):
        return None
    return run_dir / "run"


def on_start(args, state, env) -> None:
    if getattr(args, "no_aim", False):
        state["aim"] = False
        return
    state["aim"] = True
    state["experiment"] = args.experiment or state["job"]
    state["tags"] = list(args.tag or [])
    state["aim_run_hash"] = _aim_hash_for(state)
    # Convenience env vars for child scripts that write their own live Aim runs
    # (e.g. train-lora.py / hf-translate.py per the aim-authority model). Our
    # plugin itself never calls the Aim SDK, so these are purely for the child.
    env["AIM_EXPERIMENT"] = state["experiment"]
    env["AIM_RUN_NAME"] = f"{state['job']}/{state['run_id']}"
    _maybe_print_install_hint()


def on_meta_built(state, meta_text, *, output_path, log_path, build_meta):
    if not state.get("aim"):
        return None
    rec_path = _write_dump(state, meta_text)
    state["aim_dump_record"] = str(rec_path)
    return None


def on_status_print(state, lines) -> None:
    if state.get("aim_run_hash"):
        lines.append(f"aim={state['aim_run_hash']}")


def on_note(state, note, stamp, *, meta_path, meta_text) -> None:
    rec_path_str = state.get("aim_dump_record")
    if not rec_path_str:
        return
    p = Path(rec_path_str)
    if not p.exists():
        return
    try:
        record = json.loads(p.read_text(encoding="utf-8"))
        params = record.setdefault("params", {})
        result = params.get("result")
        if not isinstance(result, dict):
            result = {}
            params["result"] = result
        result["analysis-summary"] = note
        notes = params.get("notes")
        if not isinstance(notes, list):
            notes = []
            params["notes"] = notes
        notes.append(f"post-run-analysis ({stamp}): {note}")
        ai = params.get("agentctl")
        if not isinstance(ai, dict):
            ai = {}
            params["agentctl"] = ai
        cn = str(state.get("context_note", "")).strip()
        if cn:
            ai.setdefault("context_note", cn)
            ai.setdefault("pre_run_note", cn)
            ai.setdefault("pre_run_noted_at", state.get("started_at", ""))
        ai["post_run_note"] = note
        ai["post_run_noted_at"] = stamp
        p.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if meta_text:
            text_path = _text_abspath(state)
            if text_path.exists():
                text_path.write_text(meta_text, encoding="utf-8")
    except Exception as exc:
        print(f"warning: failed to update aim run-record: {exc}", file=sys.stderr)


def on_finish(state) -> None:
    """Write the back-pointer sidecar (<output>.meta.json) for each declared output
    that exists. Called from run_child after the user command exits."""
    if not state.get("aim"):
        return
    outputs = state.get("outputs") or {}
    if not outputs:
        return
    record_path_str = state.get("aim_dump_record")
    if not record_path_str:
        return
    rec_path = Path(record_path_str)
    try:
        run_dump_rel = str(rec_path.relative_to(agentctl.ROOT))
    except ValueError:
        run_dump_rel = str(rec_path)
    finished_at = state.get("finished_at") or agentctl.utc_now()
    experiment = _experiment_for(state)
    aim_hash = state.get("aim_run_hash", "")
    propagate = state.get("propagate") or {}
    for key, info in outputs.items():
        path_str = info.get("path")
        if not path_str:
            continue
        if info.get("status", "").startswith("missing") or info.get("status", "").startswith("stat_failed"):
            continue
        sidecar_path = Path(f"{path_str}.meta.json")
        sidecar = {
            "agentctl_run_id": state["run_id"],
            "aim_run_hash":   aim_hash,
            "experiment":     experiment,
            "run_dump":       run_dump_rel,
            "output_key":     key,
            "produced_at":    finished_at,
        }
        if propagate:
            sidecar["propagate"] = dict(propagate)
        try:
            sidecar_path.write_text(
                json.dumps(sidecar, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            info["sidecar"] = str(sidecar_path)
        except OSError as exc:
            print(f"warning: failed to write output sidecar {sidecar_path}: {exc}", file=sys.stderr)


def on_restart(state, args) -> None:
    args.no_aim = not state.get("aim", True)
    # Back-compat: old state files used aim_experiment/aim_tags top-level.
    args.experiment = state.get("experiment", "") or state.get("aim_experiment", "")
    args.tag = state.get("tags", []) or state.get("aim_tags", [])
    # Reconstruct declared inputs/outputs so the rerun keeps the same provenance shape.
    # An input with sha256 recorded was either declared via --input-hash or had hashing
    # otherwise requested; preserve that on restart.
    args.input = []
    args.input_raw = []
    args.input_hash = []
    for key, info in (state.get("inputs") or {}).items():
        path = info.get("path", "")
        if not path:
            continue
        spec = f"{key}={path}"
        if info.get("raw"):
            args.input_raw.append(spec)
        elif info.get("sha256"):
            args.input_hash.append(spec)
        else:
            args.input.append(spec)
    args.output = []
    args.output_hash = []
    for key, info in (state.get("outputs") or {}).items():
        path = info.get("path", "")
        if not path:
            continue
        spec = f"{key}={path}"
        if info.get("needs_hash") or info.get("sha256"):
            args.output_hash.append(spec)
        else:
            args.output.append(spec)
    # Script override: if state has a recorded script with an explicit path,
    # pass it through as --script PATH on restart so the same file is fingerprinted.
    args.script = (state.get("script") or {}).get("path", "")
    # Producer-flagged propagation: re-pass static facts via --propagate-json so the
    # restarted run has the same baseline. Cooperative file (if any) was per-run-dir
    # so a fresh run starts with an empty propagate.json again.
    propagate = state.get("propagate") or {}
    args.propagate_json = json.dumps(propagate) if propagate else ""
