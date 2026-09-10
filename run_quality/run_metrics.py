#!/usr/bin/env python3
"""Routine metrics for any GPU run: what a platform-upgrade baseline needs, for free.

Tracked runs carried an empty ``metrics`` field, so no peak VRAM or throughput was ever
recorded and there is nothing to compare a host or library upgrade against. Everything
here is already computed by the runtime or costs one cheap call, so a library can publish
it unconditionally rather than only when someone remembers to.

Deliberately domain-neutral: nothing here knows about training or decoding. A caller
supplies whatever countable it has -- steps, samples, tokens, rows -- and gets a rate.

Two halves, and a baseline is worthless without both:

* **What ran** — torch, CUDA, cuDNN, driver, GPU name and capability, transformers.
  A throughput number is meaningless when the stack underneath it is unstated.
* **How it went** — peak allocated and reserved VRAM, wall time, and whatever rate the
  caller knows (steps, samples, tokens per second), plus the batch shape and dtype that
  make a rate comparable.

Publication goes to ``$AGENTCTL_RUN_DIR/propagate.json``, which agentctl merges into run
state at completion. Outside a tracked run the environment variable is absent and every
entry point here is a no-op, so importing this never changes how a program behaves.
"""

from __future__ import annotations

import json
import os
import platform
import time
from pathlib import Path
from typing import Any

PROPAGATE_FILENAME = "propagate.json"


def run_dir() -> Path | None:
    """The tracked run's directory, or None when not running under agentctl."""
    value = os.environ.get("AGENTCTL_RUN_DIR", "").strip()
    return Path(value) if value else None


def platform_facts() -> dict[str, Any]:
    """Identity of the software and hardware stack, for upgrade comparisons.

    Best effort throughout: a missing optional library or an unavailable device records
    nothing rather than raising, because metrics must never be the reason a run fails.
    """
    facts: dict[str, Any] = {
        "python": platform.python_version(),
        "kernel": platform.release(),
    }
    try:
        import torch

        facts["torch"] = torch.__version__
        facts["cuda_build"] = torch.version.cuda
        if torch.cuda.is_available():
            facts["gpu"] = torch.cuda.get_device_name(0)
            major, minor = torch.cuda.get_device_capability(0)
            facts["gpu_capability"] = f"{major}.{minor}"
            facts["gpu_total_gib"] = round(torch.cuda.get_device_properties(0).total_memory / 2**30, 2)
            try:
                facts["cudnn"] = torch.backends.cudnn.version()
            except Exception:
                pass
    except Exception:
        pass
    for name in ("transformers", "peft", "accelerate", "safetensors"):
        try:
            facts[name] = __import__(name).__version__
        except Exception:
            pass
    return facts


def peak_memory() -> dict[str, Any]:
    """Peak VRAM this process reached, in GiB.

    Allocated is what the program asked for; reserved is what the caching allocator held
    from the driver, and reserved is the number that decides whether a smaller card fits.
    """
    try:
        import torch

        if not torch.cuda.is_available():
            return {}
        return {
            "peak_vram_allocated_gib": round(torch.cuda.max_memory_allocated() / 2**30, 3),
            "peak_vram_reserved_gib": round(torch.cuda.max_memory_reserved() / 2**30, 3),
        }
    except Exception:
        return {}


def reset_peak_memory() -> None:
    """Start the peak-VRAM window here, so load-time spikes do not mask the steady state."""
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
    except Exception:
        pass


def publish(metrics: dict[str, Any], *, prefix: str = "") -> Path | None:
    """Merge metrics into the tracked run's propagation file; no-op when untracked.

    Merges rather than overwrites so several call sites, and several phases of one run,
    can each contribute without coordinating.
    """
    directory = run_dir()
    if directory is None:
        return None
    payload = {f"{prefix}{key}": value for key, value in metrics.items() if value is not None}
    if not payload:
        return None
    path = directory / PROPAGATE_FILENAME
    existing: dict[str, Any] = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                existing = loaded
        except (OSError, json.JSONDecodeError):
            existing = {}
    existing.update(payload)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(existing, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        return None
    return path


class RunMetrics:
    """Collects a baseline over a phase and publishes it, without ever raising.

    Usage is one line at each end::

        metrics = RunMetrics("train").start()
        ...
        metrics.finish(steps=8000, samples=512000, batch_shape="8x8", dtype="float32")
    """

    def __init__(self, phase: str = ""):
        self.phase = phase
        self.prefix = f"{phase}_" if phase else ""
        self.started: float | None = None

    def start(self) -> RunMetrics:
        reset_peak_memory()
        self.started = time.perf_counter()
        publish(platform_facts(), prefix="platform_")
        return self

    def finish(self, **facts: Any) -> Path | None:
        collected: dict[str, Any] = dict(facts)
        if self.started is not None:
            elapsed = time.perf_counter() - self.started
            collected["wall_seconds"] = round(elapsed, 2)
            for unit in ("steps", "samples", "tokens", "rows"):
                count = facts.get(unit)
                if isinstance(count, (int, float)) and elapsed > 0:
                    collected[f"{unit}_per_second"] = round(count / elapsed, 3)
        collected.update(peak_memory())
        return publish(collected, prefix=self.prefix)


if __name__ == "__main__":
    print(json.dumps({"platform": platform_facts(), "peak": peak_memory()}, indent=2, sort_keys=True))
