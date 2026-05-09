#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import json
import math
import re
import subprocess
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Sidecars:
    out: Path
    meta: Path
    log: Path


@dataclass(frozen=True)
class InputSpec:
    code: str
    path: Path


@dataclass(frozen=True)
class AimWriteResult:
    run_hash: str
    repo: str
    experiment: str
    run_name: str


DEFAULT_AIM_READ_ROOTS = ("runs/aim", "research/aim")


def sidecars_for_output(output: str | Path) -> Sidecars:
    out = Path(output)
    return Sidecars(out=out, meta=Path(f"{out}.meta.md"), log=Path(f"{out}.log"))


def shortest_relpath(target: str | Path, meta_path: str | Path) -> str:
    target_path = Path(target)
    base_dir = Path(meta_path).parent
    return os.path.relpath(target_path, start=base_dir)


def meta_candidates(path: str | Path) -> list[Path]:
    p = Path(path)
    if str(p).endswith(".meta.md"):
        return [p]
    return [Path(f"{p}.meta.md"), p.with_suffix(f"{p.suffix}.meta.md") if p.suffix else Path(f"{p}.meta.md")]


def find_input_meta(path: str | Path) -> Path | None:
    seen: set[Path] = set()
    for cand in meta_candidates(path):
        if cand in seen:
            continue
        seen.add(cand)
        if cand.exists():
            return cand
    return None


def read_text_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def normalize_one_line(text: str, max_chars: int = 240) -> str:
    flat = " | ".join(part.strip() for part in str(text).splitlines() if part.strip())
    if len(flat) > max_chars:
        flat = flat[: max_chars - 3].rstrip() + "..."
    return flat


def utc_now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stable_created_at() -> str:
    return os.environ.setdefault("ARTIFACT_META_CREATED_AT", utc_now_iso())


def git_output(args: list[str], *, cwd: str | Path) -> str:
    try:
        return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def machine_defaults(*, cwd: str | Path) -> list[tuple[str, str]]:
    defaults: list[tuple[str, str]] = [("created_at", stable_created_at())]
    git_branch = git_output(["git", "branch", "--show-current"], cwd=cwd)
    git_commit = git_output(["git", "rev-parse", "HEAD"], cwd=cwd)
    git_dirty = (
        "true" if git_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=cwd) else "false"
    )
    for key, value in (
        ("git_branch", git_branch),
        ("git_commit", git_commit),
        ("git_dirty", git_dirty if git_branch or git_commit else ""),
    ):
        if value:
            defaults.append((key, value))
    try:
        from importlib.metadata import version

        aim_version = version("aim")
    except Exception:
        aim_version = ""
    if aim_version:
        defaults.append(("aim_version", str(aim_version)))
    return defaults


def merge_machine_defaults(
    machine: list[tuple[str, str]] | None,
    *,
    cwd: str | Path,
) -> list[tuple[str, str]]:
    items = list(machine or [])
    present = {key for key, _value in items}
    for key, value in machine_defaults(cwd=cwd):
        if key not in present and value:
            items.append((key, value))
    return items


def excerpt_markdown(text: str, max_lines: int = 8, max_chars: int = 700) -> str:
    kept: list[str] = []
    in_code = False
    used = 0
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("# "):
            continue
        if not line.strip() and not kept:
            continue
        if not line.strip() and kept and kept[-1] == "":
            continue
        candidate = line[: max(0, max_chars - used)]
        if not candidate and kept:
            break
        kept.append(candidate)
        used += len(candidate) + 1
        if len(kept) >= max_lines or used >= max_chars:
            break
    while kept and kept[-1] == "":
        kept.pop()
    return "\n".join(kept)


def parse_keyvals(items: Iterable[str]) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"expected KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        parsed.append((key.strip(), value.strip()))
    return parsed


def merge_keyvals(*groups: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    """Merge flat key/value groups with later values overriding earlier ones."""
    merged: dict[str, str] = {}
    order: list[str] = []
    for group in groups:
        for key, value in group:
            if key not in merged:
                order.append(key)
            merged[key] = value
    return [(key, merged[key]) for key in order]


def sanitize_code(text: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in text.strip().lower())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "input"


def parse_input_specs(items: Iterable[str]) -> list[InputSpec]:
    specs: list[InputSpec] = []
    used: set[str] = set()
    for idx, item in enumerate(items, start=1):
        if "=" in item:
            raw_code, raw_path = item.split("=", 1)
            code = sanitize_code(raw_code)
            path = Path(raw_path.strip())
        else:
            path = Path(item)
            stem = path.name
            if stem.endswith(".meta.md"):
                stem = stem[: -len(".meta.md")]
            elif "." in stem:
                stem = stem.split(".", 1)[0]
            code = sanitize_code(stem)
        base = code
        n = 2
        while code in used:
            code = f"{base}-{n}"
            n += 1
        used.add(code)
        specs.append(InputSpec(code=code, path=path))
    return specs


def running_path(output: str | Path) -> Path:
    path = Path(output)
    if str(path).endswith(".running.md"):
        return path
    return Path(f"{path}.running.md")


def write_running_md(
    output: str | Path,
    *,
    pid: int,
    command: str,
    cwd: str | Path = ".",
    log: str | Path | None = None,
    trainlog: str | Path | None = None,
    started: str = "",
) -> Path:
    """Write <output>.running.md at job launch so a future agent can find in-flight work."""
    out = Path(output)
    path = running_path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# In-Flight Job: {out.name}", ""]
    lines += [
        f"- status: running",
        f"- pid: {pid}",
    ]
    if started:
        lines.append(f"- started: {started}")
    if log:
        lines.append(f"- log: {log}")
    if trainlog:
        lines.append(f"- trainlog: {trainlog}")
    lines += [f"- out: {out}", ""]
    lines += ["## Command", "```bash", f"cd {cwd}", command, "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def cleanup_running(output: str | Path) -> bool:
    """Delete <output>.running.md if it exists. Returns True if deleted."""
    p = running_path(output)
    if p.exists():
        p.unlink()
        return True
    return False


def autodetect_related(sidecars: Sidecars) -> list[tuple[str, Path]]:
    related: list[tuple[str, Path]] = []
    for suffix, label in ((".score", "score"), (".stats.json", "stats"), (".clean", "clean"), (".scores", "scores")):
        p = Path(f"{sidecars.out}{suffix}")
        if p.exists():
            related.append((label, p))
    return related


def aim_read_roots(
    repo_root: str | Path = ".",
    read_roots: Sequence[str | Path] | None = None,
) -> list[Path]:
    """Return configured Aim text dump roots, newest convention first."""
    root = Path(repo_root).resolve()
    if read_roots is None:
        env_roots = [p for p in os.environ.get("AGENTCTL_AIM_READ_ROOTS", "").split(os.pathsep) if p]
        raw_roots: Sequence[str | Path] = env_roots or DEFAULT_AIM_READ_ROOTS
    else:
        raw_roots = read_roots

    paths: list[Path] = []
    seen: set[Path] = set()
    for raw in raw_roots:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = root / path
        path = path.resolve()
        if path in seen:
            continue
        seen.add(path)
        paths.append(path)
    return paths


def find_aim_run_record(
    *,
    meta_path: str | Path,
    setup: list[tuple[str, str]] | None = None,
    repo_root: str | Path = ".",
    read_roots: Sequence[str | Path] | None = None,
) -> Path | None:
    """Return the exported Aim-format run record for this run when present.

    Searches configured read roots. By default this means ``runs/aim/`` first
    (current convention) then ``research/aim/`` (legacy layout). Override with
    ``AGENTCTL_AIM_READ_ROOTS`` or the ``read_roots`` argument for migrations."""
    target_meta = str(Path(meta_path).resolve())
    setup_dict = keyval_dict(setup or [])
    target_hash = setup_dict.get("aim_run_hash", "")
    for dump_root in aim_read_roots(repo_root=repo_root, read_roots=read_roots):
        for run_json in dump_root.glob("*/runs/*.json"):
            try:
                record = json.loads(run_json.read_text(encoding="utf-8"))
            except Exception:
                continue
            source = record.get("source", {}) or {}
            params = record.get("params", {}) or {}
            output = params.get("output", {}) or {}
            candidate_meta = output.get("meta_path", "") or params.get("meta", {}).get("path", "")
            if target_hash:
                if str(source.get("aim_run_hash", "")) != target_hash:
                    continue
            elif candidate_meta:
                if str(Path(candidate_meta).resolve()) != target_meta:
                    continue
            else:
                continue
            return run_json.resolve()
    return None


def find_aim_run_text(
    *,
    meta_path: str | Path,
    setup: list[tuple[str, str]] | None = None,
    repo_root: str | Path = ".",
    read_roots: Sequence[str | Path] | None = None,
) -> Path | None:
    """Return the exported Aim-format text artifact for this run when present."""
    run_json = find_aim_run_record(meta_path=meta_path, setup=setup, repo_root=repo_root, read_roots=read_roots)
    if run_json is None:
        return None
    try:
        record = json.loads(run_json.read_text(encoding="utf-8"))
    except Exception:
        return None
    for text in record.get("texts", []) or []:
        if text.get("name") == "meta.markdown" and text.get("path"):
            candidate = run_json.parent.parent / text["path"]
            if candidate.exists():
                return candidate.resolve()
    return None


def upsert_analysis_summary_markdown(
    text: str,
    summary: str,
    *,
    label: str = "post-run-analysis",
    timestamp: str | None = None,
) -> str:
    summary = normalize_one_line(summary)
    if not summary:
        return text

    lines = text.splitlines()

    def section_bounds(name: str) -> tuple[int | None, int | None]:
        start = None
        end = len(lines)
        header = f"## {name}"
        for i, line in enumerate(lines):
            if line == header:
                start = i
                continue
            if start is not None and line.startswith("## "):
                end = i
                break
        return start, end

    def ensure_section(name: str) -> tuple[int, int]:
        start, end = section_bounds(name)
        if start is not None:
            return start, end or len(lines)
        insert_at = len(lines)
        if name == "Result":
            for candidate in ("## Machine", "## Request Plan", "## Related", "## Inputs", "## Notes"):
                for i, line in enumerate(lines):
                    if line == candidate:
                        insert_at = i
                        break
                if insert_at != len(lines):
                    break
        insert_lines = [f"## {name}", ""]
        if insert_at > 0 and lines[insert_at - 1] != "":
            insert_lines.insert(0, "")
            insert_at += 1
        lines[insert_at:insert_at] = insert_lines
        return insert_at + (1 if insert_lines[0] == "" else 0), len(lines)

    ensure_section("Result")
    result_start, result_end = section_bounds("Result")
    assert result_start is not None and result_end is not None
    result_line = f"- analysis-summary: `{summary}`"
    replaced = False
    for i in range(result_start + 1, result_end):
        if lines[i].startswith("- analysis-summary:"):
            lines[i] = result_line
            replaced = True
            break
    if not replaced:
        insert_at = result_end
        while insert_at > result_start + 1 and lines[insert_at - 1] == "":
            insert_at -= 1
        lines.insert(insert_at, result_line)
        if insert_at == len(lines) - 1:
            lines.append("")

    ensure_section("Notes")
    notes_start, notes_end = section_bounds("Notes")
    assert notes_start is not None and notes_end is not None
    lines[notes_start + 1 : notes_end] = [
        line for line in lines[notes_start + 1 : notes_end] if not line.startswith("- analysis-summary:")
    ]
    notes_start, notes_end = section_bounds("Notes")
    assert notes_start is not None and notes_end is not None
    note_line = f"- {label}: {summary}" if not timestamp else f"- {label} ({timestamp}): {summary}"
    insert_at = notes_end
    while insert_at > notes_start + 1 and lines[insert_at - 1] == "":
        insert_at -= 1
    lines.insert(insert_at, note_line)
    if insert_at == len(lines) - 1:
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def score_summary_from_file(path: Path) -> str | None:
    text = read_text_if_exists(path)
    if text is None:
        return None
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return None


def format_link(label: str, target: Path, meta_path: Path) -> str:
    return f"[{label}]({shortest_relpath(target, meta_path)})"


def format_keyvals(items: Iterable[tuple[str, str]]) -> list[str]:
    return [f"- {key}: `{value}`" for key, value in items]


def env_flag(name: str) -> bool:
    value = os.environ.get(name, "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def maybe_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def keyval_dict(items: Iterable[tuple[str, str]]) -> dict[str, str]:
    return {key: value for key, value in items}


def path_items(items: Iterable[tuple[str, Path]]) -> dict[str, str]:
    return {key: str(path) for key, path in items}


def setting_value(value) -> str:  # noqa: ANN001
    """Stable string form for effective run settings stored in meta/Aim."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float | str):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    try:
        return json.dumps(value, sort_keys=True)
    except TypeError:
        return str(value)


def namespace_keyvals(namespace, *, prefix: str = "effective") -> list[tuple[str, str]]:  # noqa: ANN001
    """Serialize an argparse namespace/object into sorted metadata key/value pairs."""
    data = vars(namespace) if hasattr(namespace, "__dict__") else dict(namespace)
    return [(f"{prefix}.{key}", setting_value(data[key])) for key in sorted(data)]


def namespace_keyvals_selected(  # noqa: ANN001
    namespace,
    *,
    prefix: str = "effective",
    include: set[str] | None = None,
    exclude: set[str] | None = None,
) -> list[tuple[str, str]]:
    data = vars(namespace) if hasattr(namespace, "__dict__") else dict(namespace)
    exclude = exclude or set()
    keys = sorted(data)
    if include is not None:
        keys = [key for key in keys if key in include]
    keys = [key for key in keys if key not in exclude]
    return [(f"{prefix}.{key}", setting_value(data[key])) for key in keys]


def normalize_option_token(token: str) -> str:
    if token.startswith("-"):
        name, eq, value = token.partition("=")
        return name.replace("_", "-") + (eq + value if eq else "")
    return token


def explicit_arg_dests(parser: argparse.ArgumentParser, argv: list[str]) -> set[str]:
    option_to_dest: dict[str, str] = {}
    for action in getattr(parser, "_actions", []):
        for option in getattr(action, "option_strings", []):
            option_to_dest[normalize_option_token(option)] = action.dest
    explicit: set[str] = set()
    for raw in argv:
        token = normalize_option_token(raw)
        if token == "--":
            break
        if not token.startswith("-"):
            continue
        option, _eq, _value = token.partition("=")
        dest = option_to_dest.get(option)
        if dest and dest is not argparse.SUPPRESS:
            explicit.add(dest)
    return explicit


def namespace_key_sources(  # noqa: ANN001
    namespace,
    *,
    explicit_dests: set[str],
    prefix: str = "effective_source",
    include: set[str] | None = None,
    exclude: set[str] | None = None,
) -> list[tuple[str, str]]:
    data = vars(namespace) if hasattr(namespace, "__dict__") else dict(namespace)
    exclude = exclude or set()
    keys = sorted(data)
    if include is not None:
        keys = [key for key in keys if key in include]
    keys = [key for key in keys if key not in exclude]
    return [(f"{prefix}.{key}", "explicit" if key in explicit_dests else "default") for key in keys]


def effective_source_for_dest(  # noqa: ANN001
    namespace,
    *,
    dest: str,
    actual_value,
    explicit_dests: set[str],
) -> str:
    data = vars(namespace) if hasattr(namespace, "__dict__") else dict(namespace)
    if dest not in data:
        return "derived"
    if setting_value(actual_value) != setting_value(data[dest]):
        return "derived"
    return "explicit" if dest in explicit_dests else "default"


# ---------------------------------------------------------------------------
# Per-script legacy value registries
#
# When a new output-affecting CLI option is added to a script, add its legacy
# value here so:
#   1. Every new run written to Aim also carries the key (set to legacy value
#      when the option was not set), keeping all runs graphable together.
#   2. The backfill script can patch old Aim runs that predate the option.
#
# Convention: key = "effective.<arg_name>" (underscores, matching namespace_keyvals).
# Value = string form of the value the option implicitly had BEFORE it existed.
#
# These dicts are intentionally verbose; keep a comment for each entry noting
# when/why the legacy value was chosen.
# ---------------------------------------------------------------------------

# train-lora.py: effective.* legacy values for runs before 2026-04-16 commit f842788
TRAIN_LORA_EFFECTIVE_LEGACY: dict[str, str] = {
    # Objective: old default was weighted (prompt-masked, --weight-input=0.1)
    "effective.standard_loss": "false",
    "effective.weighted_loss": "true",
    "effective.objective": "weighted",
    "effective.weight_input": "0.1",
    # KL regularization: new in f842788, legacy = off
    "effective.kl_base_lambda": "0.0",
    "effective.kl_base_mask": "active",
    "effective.kl_base_enabled": "false",
    # DoRA two-LR: new in f842788, legacy = off (same as current default 0.0)
    "effective.dora_direction_lr": "0.0",
    "effective.dora_magnitude_lr": "0.0",
    # Flat-LoRA: new default-off path
    "effective.flat_lora": "0",
    "effective.flat_lora_sigma": "0.05",
    "effective.flat_lora_schedule": "cosine",
    "effective.flat_lora_burnin_epochs": "0.5",
    "effective.flat_lora_enabled": "false",
    # LR schedule: cosine was hardcoded; warmup used warmup_ratio=0.03, not steps
    "effective.lr_scheduler_type": "cosine",
    "effective.warmup_steps": "0",  # 0 = "used warmup_ratio=0.03" (legacy, not steps)
    # Logical-batch token scheduling: new in f842788, legacy = off
    "effective.logical_batch_loss_tokens": "0",
    "effective.logical_batch_growth": "2.0",
    "effective.logical_batch_growth_epochs": "0",
    # Checkpoint management: new/changed in f842788
    "effective.post_threshold_epochs": "0",
    "effective.average_major_checkpoints": "0",
    "effective.major_checkpoint_min_delta": "0.005",
    # Target modules: old default was no-mlp (q/k/v/o only)
    "effective.target_modules": "no-mlp",
    "effective.target_modules_resolved": "q_proj,k_proj,v_proj,o_proj",
    # Optimizer: old auto-select was lion_32bit
    "effective.optim": "lion_32bit",
    # Learning rate: old default was 2e-4
    "effective.learning_rate": "0.0002",
    # Precision: no 4-bit loading by default
    "effective.load_4bit": "false",
    # DoRA: has always been opt-in (0 = off)
    "effective.dora": "0",
    # RSLoRA and rank: old defaults were rslora=1, rank=16, alpha=32
    "effective.rslora": "1",
    "effective.lora_rank": "16",
    "effective.lora_alpha": "32",
    # Epochs: old default was 5; then 3; val-based stopping did not exist
    "effective.num_train_epochs": "5",
    # Batch: old defaults were batch=8, accum=4
    "effective.per_device_train_batch_size": "8",
    "effective.gradient_accumulation_steps": "4",
    "effective.logical_batch_examples": "32",
    # Val early stopping: new in 2026-04-16, legacy = disabled
    "effective.val_size": "0",
    "effective.val_every_n": "0",
    "effective.val_patience": "0",
    "effective.val_min_delta": "0.0",
    "effective.output_acc_threshold": "0.987",
}

# hf-translate.py: effective.* legacy values for runs before 2026-04-16 commit f842788
HF_TRANSLATE_EFFECTIVE_LEGACY: dict[str, str] = {
    # Blend mode: old runs had no blend by default
    "effective.blend": "",
    "effective.lora": "",
    "effective.loras": "",
    # Batch: old default was 8
    "effective.batch": "8",
    # Temperature: greedy decoding
    "effective.temperature": "0.0",
    # Score: MetricX disabled by default
    "effective.score": "false",
    # Thinking: Qwen3 enable_thinking=False was always the default for inference
    "effective.enable_thinking": "false",
}


TRAIN_LORA_NON_OUTPUT_ARGS: set[str] = {
    "dryrun",
    "log",
    "logfile",
    "output_dir",
    "trt_output_dir",
    "verbose_head",
    "write_query_yaml",
    "yaml_key",
}


HF_TRANSLATE_NON_OUTPUT_ARGS: set[str] = {
    "dryrun",
    "log",
    "logfile",
    "out_edge",
    "output",
    "split_output",
    "verbose_head",
    "write_query_yaml",
    "yaml_key",
}


def merge_legacy_setup(
    setup: list[tuple[str, str]],
    legacy: dict[str, str],
) -> list[tuple[str, str]]:
    """Return setup items extended with any legacy keys absent from setup.

    Legacy keys are injected BEFORE the actual setup items so that if a key
    appears in both, the actual value (appearing later) wins in dict conversion.
    Items returned as a flat list; callers that need a dict should use
    keyval_dict() afterward.
    """
    present = {key for key, _ in setup}
    injected = [(k, v) for k, v in legacy.items() if k not in present]
    return injected + list(setup)


def aim_enabled(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return explicit
    if env_flag("AIM_DISABLE") or env_flag("NO_AIM"):
        return False
    return bool(
        os.environ.get("AIM_REPO")
        or os.environ.get("AIM_EXPERIMENT")
        or os.environ.get("AIM_RUN_NAME")
    )


def write_aim_run(
    *,
    output_path: str | Path,
    meta_path: str | Path,
    log_path: str | Path,
    markdown: str,
    title: str | None,
    cwd: str | Path,
    command: str | None,
    setup: list[tuple[str, str]],
    results: list[tuple[str, str]],
    machine: list[tuple[str, str]] | None = None,
    plan: list[str] | None = None,
    notes: list[str] | None = None,
    inputs: list[InputSpec] | None = None,
    related: list[tuple[str, Path]] | None = None,
    repo: str | Path | None = None,
    experiment: str | None = None,
    run_name: str | None = None,
    run_id: str | None = None,
    tags: list[str] | None = None,
    agentctl: dict[str, str] | None = None,
    source: dict[str, str] | None = None,
    log_markdown: bool = True,
    legacy_setup: dict[str, str] | None = None,
) -> AimWriteResult:
    """Mirror the same metadata used for <out>.meta.md into Aim.

    Aim is optional at the project level, so import it lazily. The Markdown sidecar
    remains the durable artifact record; Aim receives both structured params and,
    when supported, the complete Markdown body as a text object.

    legacy_setup: optional dict of key → legacy-value pairs injected for any key
    absent from setup. Use the per-script TRAIN_LORA_EFFECTIVE_LEGACY /
    HF_TRANSLATE_EFFECTIVE_LEGACY constants. This ensures every Aim run carries
    all known effective.* keys so graphs remain comparable across runs that predate
    a newly introduced option.
    """
    from aim import Run, Text

    out = Path(output_path)
    aim_repo = Path(repo or os.environ.get("AIM_REPO") or ".").expanduser()
    aim_experiment = experiment or os.environ.get("AIM_EXPERIMENT") or "default"
    agentctl_run_name = ""
    if os.environ.get("AGENTCTL_JOB") and os.environ.get("AGENTCTL_RUN_ID"):
        agentctl_run_name = f"{os.environ['AGENTCTL_JOB']}/{os.environ['AGENTCTL_RUN_ID']}"
    aim_run_name = run_name or os.environ.get("AIM_RUN_NAME") or agentctl_run_name or out.name
    aim_run_id = run_id or os.environ.get("AGENTCTL_RUN_ID") or ""
    run = Run(
        repo=str(aim_repo),
        experiment=aim_experiment,
        log_system_params=True,
        capture_terminal_logs=False,
    )
    run.name = aim_run_name
    run["output"] = {
        "path": str(out),
        "meta_path": str(meta_path),
        "log_path": str(log_path),
        "title": title or out.name,
    }
    run["command"] = {
        "cwd": str(cwd),
        "text": command or "",
    }
    aim_setup = merge_legacy_setup(setup, legacy_setup) if legacy_setup else setup
    run["setup"] = keyval_dict(aim_setup)
    run["result"] = keyval_dict(results)
    machine_items = merge_machine_defaults(machine, cwd=cwd)
    run["machine"] = keyval_dict(machine_items)
    run["request_plan"] = list(plan or [])
    run["notes"] = list(notes or [])
    run["related"] = path_items(related or [])
    run["inputs"] = {spec.code: str(spec.path) for spec in (inputs or [])}
    input_runs = collect_input_runs(inputs or [])
    if input_runs:
        run["input_runs"] = input_runs
    agentctl_env = {
        "job": os.environ.get("AGENTCTL_JOB", ""),
        "run_id": aim_run_id,
        "mode": os.environ.get("AGENTCTL_MODE", ""),
        "step_id": os.environ.get("AGENTCTL_STEP_ID", ""),
        "headline_file": os.environ.get("AGENTCTL_HEADLINE_FILE", ""),
        "output": os.environ.get("AGENTCTL_OUTPUT", ""),
    }
    if agentctl:
        agentctl_env.update(agentctl)
    run["agentctl"] = {
        "job": agentctl_env.get("job", ""),
        "run_id": agentctl_env.get("run_id", ""),
        "mode": agentctl_env.get("mode", ""),
        "step_id": agentctl_env.get("step_id", ""),
        "headline_file": agentctl_env.get("headline_file", ""),
        "output": agentctl_env.get("output", ""),
    }
    run["meta"] = {
        "format": "artifact_meta.md",
        "path": str(meta_path),
    }
    if source:
        run["source"] = {str(k): str(v) for k, v in source.items()}
    for tag in ["artifact-meta", *(tags or [])]:
        if tag:
            run.add_tag(tag)
    for key, value in results:
        numeric = maybe_float(value)
        if numeric is not None:
            run.track(numeric, name=f"result.{sanitize_code(key)}", step=0)
    if log_markdown:
        try:
            run.track(Text(markdown), name="meta.markdown", step=0)
        except Exception:
            run["meta"]["markdown_excerpt"] = excerpt_markdown(markdown, max_lines=20, max_chars=4000)
    result = AimWriteResult(
        run_hash=run.hash,
        repo=str(aim_repo),
        experiment=aim_experiment,
        run_name=aim_run_name,
    )
    run.close()
    return result


def load_stats_text(path: Path) -> list[str]:
    text = read_text_if_exists(path)
    if text is None:
        return []
    if path.suffix == ".json":
        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                return [f"- {k}: `{obj[k]}`" for k in sorted(obj)]
        except json.JSONDecodeError:
            pass
    excerpt = excerpt_markdown(text, max_lines=8, max_chars=700)
    if not excerpt:
        return []
    return [f"```text\n{excerpt}\n```"]


def parse_meta_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def parse_markdown_keyvals(lines: Iterable[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw in lines:
        line = raw.strip()
        if not line.startswith("- ") or ": " not in line:
            continue
        key, value = line[2:].split(": ", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("`") and value.endswith("`") and len(value) >= 2:
            value = value[1:-1]
        else:
            match = re.fullmatch(r"\[(?P<label>.*)\]\((?P<target>.*)\)", value)
            if match:
                value = match.group("target")
        parsed[key] = value
    return parsed


def markdown_title(text: str) -> str:
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            if title.lower().startswith("run metadata:"):
                title = title.split(":", 1)[1].strip()
            return title
    return ""


def input_run_info(spec: InputSpec) -> dict[str, str] | None:
    input_meta = find_input_meta(spec.path)
    if input_meta is None:
        return None
    text = read_text_if_exists(input_meta)
    if not text:
        return None
    sections = parse_meta_sections(text)
    setup = parse_markdown_keyvals(sections.get("setup", []))
    info = {
        "path": str(spec.path),
        "meta_path": str(input_meta),
    }
    title = markdown_title(text)
    if title:
        info["title"] = title
    for key in ("aim_run_hash", "aim_repo", "aim_experiment", "aim_run_name"):
        if setup.get(key):
            info[key] = setup[key]
    output = parse_markdown_keyvals(sections.get("output", []))
    if output.get("out"):
        info["output_path"] = output["out"]
    return info if any(info.get(key) for key in ("title", "aim_run_hash", "aim_run_name")) else None


def collect_input_runs(inputs: Iterable[InputSpec]) -> dict[str, dict[str, str]]:
    collected: dict[str, dict[str, str]] = {}
    for spec in inputs:
        info = input_run_info(spec)
        if info:
            collected[spec.code] = info
    return collected


def inherited_meta_lines(
    spec: InputSpec,
    input_meta: Path,
    text: str,
    meta_path: Path,
) -> list[str]:
    link_re = re.compile(r"\[(?P<label>.*)\]\((?P<target>.*)\)")

    def rebase_links(line: str) -> str:
        def repl(match: re.Match[str]) -> str:
            target = match.group("target")
            if "://" in target:
                return match.group(0)
            rebased = input_meta.parent / target
            return format_link(match.group("label"), rebased, meta_path)

        return link_re.sub(repl, line)

    sections = parse_meta_sections(text)
    wanted = ("output", "result", "machine")
    lines: list[str] = []
    any_added = False
    setup = parse_markdown_keyvals(sections.get("setup", []))
    for key in ("aim_run_name", "aim_experiment", "aim_run_hash"):
        value = setup.get(key)
        if value:
            any_added = True
            lines.append(f"- ({spec.code}.setup) {key}: `{value}`")
    for section in wanted:
        body = sections.get(section, [])
        body_lines = [line for line in body if line.strip()]
        if not body_lines:
            continue
        any_added = True
        for body_line in body_lines:
            stripped = rebase_links(body_line.strip())
            if stripped.startswith("- "):
                lines.append(f"- ({spec.code}.{section}) {stripped[2:]}")
            elif stripped.startswith(">"):
                continue
            else:
                lines.append(f"- ({spec.code}.{section}) {stripped}")
    return lines if any_added else []


def build_meta_markdown(
    *,
    output_path: str | Path,
    title: str | None,
    cwd: str | Path,
    command: str | None,
    setup: list[tuple[str, str]],
    results: list[tuple[str, str]],
    machine: list[tuple[str, str]] | None = None,
    plan: list[str] | None = None,
    notes: list[str] | None = None,
    inputs: list[InputSpec] | None = None,
    related: list[tuple[str, Path]] | None = None,
    input_excerpt_lines: int = 8,
    input_excerpt_chars: int = 700,
) -> str:
    sidecars = sidecars_for_output(output_path)
    meta_path = sidecars.meta
    title_text = title or sidecars.out.name
    lines: list[str] = [f"# Run Metadata: {title_text}", ""]

    lines.extend(
        [
            "## Output",
            f"- out: {format_link(sidecars.out.name, sidecars.out, meta_path)}",
            f"- log: {format_link(sidecars.log.name, sidecars.log, meta_path)}",
            "",
        ]
    )

    if command:
        lines.extend(["## Command", "```bash", f"cd {cwd}", command, "```", ""])

    if setup:
        lines.extend(["## Setup", *format_keyvals(setup), ""])

    if results:
        lines.extend(["## Result", *format_keyvals(results), ""])

    machine_items = merge_machine_defaults(machine, cwd=cwd)
    if machine_items:
        lines.extend(["## Machine", *format_keyvals(machine_items), ""])

    if plan:
        lines.extend(["## Request Plan", *[f"- {line}" for line in plan], ""])

    if related:
        lines.append("## Related")
        for label, path in related:
            lines.append(f"- {label}: {format_link(path.name, path, meta_path)}")
        lines.append("")

    if inputs:
        lines.append("## Inputs")
        for spec in inputs:
            path = spec.path
            lines.append(f"### `{spec.code}`")
            lines.append(f"- path: {format_link(path.name, path, meta_path)}")
            input_meta = find_input_meta(path)
            if input_meta is not None:
                lines.append(f"- meta: {format_link(input_meta.name, input_meta, meta_path)}")
                text = read_text_if_exists(input_meta)
                if text:
                    inherited = inherited_meta_lines(spec, input_meta, text, meta_path)
                    if inherited:
                        lines.append("")
                        lines.extend(inherited)
                    else:
                        excerpt = excerpt_markdown(
                            text, max_lines=input_excerpt_lines, max_chars=input_excerpt_chars
                        )
                        if excerpt:
                            lines.append("")
                            lines.append(f"> Excerpt from `{input_meta.name}`:")
                            for ex_line in excerpt.splitlines():
                                lines.append(f"> {ex_line}" if ex_line else ">")
            lines.append("")

    if notes:
        lines.extend(["## Notes", *[f"- {note}" for note in notes], ""])

    return "\n".join(lines).rstrip() + "\n"
