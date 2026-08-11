"""Current user-level instruction and skill locations for supported harnesses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Harness:
    name: str
    instruction: tuple[str, ...]
    skill_root: tuple[str, ...]


HARNESSES = {
    "codex": Harness("codex", (".codex", "AGENTS.md"), (".agents", "skills")),
    "claude": Harness(
        "claude", (".claude", "CLAUDE.md"), (".claude", "skills")
    ),
    "pi": Harness(
        "pi", (".pi", "agent", "AGENTS.md"), (".pi", "agent", "skills")
    ),
    "opencode": Harness(
        "opencode",
        (".config", "opencode", "AGENTS.md"),
        (".agents", "skills"),
    ),
    "grok": Harness("grok", (".grok", "AGENTS.md"), (".grok", "skills")),
    "copilot": Harness(
        "copilot",
        (".copilot", "copilot-instructions.md"),
        (".agents", "skills"),
    ),
}

ALIASES = {
    "claude-code": "claude",
    "copilot-cli": "copilot",
    "grok-build": "grok",
}


def select_harnesses(values: list[str] | None) -> list[Harness]:
    """Expand repeated/comma-separated harness selectors in stable order."""
    requested = []
    for value in values or ["all"]:
        requested.extend(
            part.strip().lower() for part in value.split(",") if part.strip()
        )
    if "all" in requested:
        if len(requested) != 1:
            raise ValueError("'all' cannot be combined with named harnesses")
        return list(HARNESSES.values())

    names = []
    for name in requested:
        canonical = ALIASES.get(name, name)
        if canonical not in HARNESSES:
            choices = ", ".join(HARNESSES)
            raise ValueError(
                f"unknown harness {name!r}; choose all or one of: {choices}"
            )
        if canonical not in names:
            names.append(canonical)
    if not names:
        raise ValueError("select at least one harness")
    return [HARNESSES[name] for name in names]
