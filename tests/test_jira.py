#!/usr/bin/env python3
"""Tests for scripts/jira: description formatting, and the sprint, status and
planning-field lookups with the request layer stubbed; no network."""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import traceback
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "jira"
_loader = importlib.machinery.SourceFileLoader("jira_tool", str(SCRIPT))
jira = importlib.util.module_from_spec(
    importlib.util.spec_from_loader("jira_tool", _loader)
)
_loader.exec_module(jira)


def _blocks(markdown: str) -> list[dict]:
    return jira.markdown_to_adf(markdown)["content"]


def _text(block: dict) -> str:
    return jira._adf_text(block).strip()


def test_inline_marks_become_marked_text() -> None:
    (paragraph,) = _blocks("Use `get` for **all** of *it*, see [docs](https://x.y/z).")
    marked = {
        node["text"]: node["marks"][0]
        for node in paragraph["content"]
        if "marks" in node
    }
    assert marked["get"] == {"type": "code"}
    assert marked["all"] == {"type": "strong"}
    assert marked["it"] == {"type": "em"}
    assert marked["docs"] == {"type": "link", "attrs": {"href": "https://x.y/z"}}
    assert _text(paragraph) == "Use get for all of it, see docs."


def test_arithmetic_stars_stay_literal() -> None:
    (paragraph,) = _blocks("cost is 2 * n * m")
    assert paragraph["content"] == [{"type": "text", "text": "cost is 2 * n * m"}]


def test_double_stars_in_arithmetic_and_globs_stay_literal() -> None:
    for prose in ("cost is x ** 2 + y ** 2", "match **/*.py and **/*.md files"):
        (paragraph,) = _blocks(prose)
        assert paragraph["content"] == [{"type": "text", "text": prose}]


def test_number_ending_a_wrapped_line_stays_prose() -> None:
    (paragraph,) = _blocks("We shipped it in\n2024. Then we stopped.")
    assert _text(paragraph) == "We shipped it in 2024. Then we stopped."


def test_numbered_list_keeps_its_first_number() -> None:
    (numbered,) = _blocks("3. c\n4. d")
    assert numbered["attrs"] == {"order": 3}


def test_inline_triple_backticks_do_not_open_a_fence() -> None:
    first, second = _blocks("```x``` is inline\n\nstill prose")
    assert first["type"] == second["type"] == "paragraph"


def test_wrapped_lines_join_and_blank_lines_split_paragraphs() -> None:
    first, second = _blocks("one\ntwo\n\nthree")
    assert (_text(first), _text(second)) == ("one two", "three")


def test_list_keeps_items_across_blank_lines_and_wraps() -> None:
    heading, bullets, numbered, after = _blocks(
        "## Steps\n- a\n  wrapped\n\n- b\n1. x\n2. y\nafter\n"
    )
    assert heading["attrs"] == {"level": 2}
    assert bullets["type"] == "bulletList"
    assert [_text(item) for item in bullets["content"]] == ["a wrapped", "b"]
    assert numbered["type"] == "orderedList"
    assert len(numbered["content"]) == 2
    assert _text(after) == "after"


def test_fenced_code_is_verbatim() -> None:
    (code,) = _blocks("```bash\nrm *.o\n\n- not a list\n```")
    assert code["attrs"] == {"language": "bash"}
    assert code["content"] == [{"type": "text", "text": "rm *.o\n\n- not a list"}]


def test_no_empty_text_nodes() -> None:
    def walk(node: dict) -> None:
        assert node.get("type") != "text" or node["text"]
        for child in node.get("content", []):
            walk(child)

    walk(jira.markdown_to_adf("# h\n\n```\n```\n\n```\n\n```\n\n- `a`\n\n**b**\n"))


class FakeJira:
    """Stands in for `jira._request`: answers GETs from `replies`, records writes.

    A reply is a dict, or an int status; a status the caller lists in
    `absent_on` reads as `None`, any other fails the test.
    """

    def __init__(self, replies: dict[str, dict | int]) -> None:
        self.replies = replies
        self.writes: list[tuple[str, str, dict | None]] = []

    def __call__(self, args, method, path, payload=None, *, absent_on=()):
        if method != "GET":
            self.writes.append((method, path, payload))
            return {}
        reply = self.replies[path]
        if isinstance(reply, int):
            assert reply in absent_on, f"unexpected {reply} for {path}"
            return None
        return reply


def _with_fake(replies: dict[str, dict | int]) -> FakeJira:
    fake = FakeJira(replies)
    jira._request = fake
    return fake


def _args(**overrides) -> argparse.Namespace:
    values = {"points": None, "points_field": "Story Points", "sprint": None}
    return argparse.Namespace(**(values | overrides))


def _dies(call) -> int:
    try:
        call()
    except SystemExit as stop:
        return stop.code
    raise AssertionError("expected acli.die")


BOARDS = "/rest/agile/1.0/board?projectKeyOrId=P"
SPRINTS = "/rest/agile/1.0/board/{}/sprint?state=active,future&startAt={}"


def _sprint_site() -> dict[str, dict | int]:
    return {
        f"{BOARDS}&startAt=0": {
            "isLast": False,
            "values": [{"id": 1, "type": "scrum", "name": "Team"}],
        },
        f"{BOARDS}&startAt=1": {
            "isLast": True,
            "values": [
                {"id": 2, "type": "kanban", "name": "Flow"},
                {"id": 3, "type": "simple", "name": "No sprints"},
            ],
        },
        SPRINTS.format(1, 0): {
            "isLast": False,
            "values": [{"id": 11, "name": "S2", "state": "future"}],
        },
        SPRINTS.format(1, 1): {
            "isLast": True,
            "values": [{"id": 10, "name": "S1", "state": "active"}],
        },
        SPRINTS.format(3, 0): 400,
    }


def test_sprints_page_boards_and_sprints_and_skip_sprintless_boards() -> None:
    _with_fake(_sprint_site())
    rows = jira._sprints(_args(), "P")
    assert [(s["name"], s["state"], s["board"]) for s in rows] == [
        ("S1", "active", "Team"),
        ("S2", "future", "Team"),
    ]


def test_sprint_resolves_active_or_a_name_and_refuses_no_match() -> None:
    _with_fake(_sprint_site())
    assert jira._sprint(_args(), "P", "active")["id"] == 10
    assert jira._sprint(_args(), "P", "s2")["id"] == 11
    assert _dies(lambda: jira._sprint(_args(), "P", "S9")) == 4


TRANSITIONS = {
    "transitions": [
        {"id": "21", "name": "Start", "to": {"name": "In Progress"}},
        {"id": "31", "name": "In Progress", "to": {"name": "Blocked"}},
    ]
}


def _status_site(status: str) -> dict[str, dict | int]:
    return {
        "/rest/api/3/issue/P-1?fields=status": {"fields": {"status": {"name": status}}},
        "/rest/api/3/issue/P-1/transitions": TRANSITIONS,
    }


def test_transition_prefers_target_status_over_transition_name() -> None:
    fake = _with_fake(_status_site("To Do"))
    assert jira._transition(_args(), "P-1", "in progress") == "In Progress"
    assert fake.writes == [
        ("POST", "/rest/api/3/issue/P-1/transitions", {"transition": {"id": "21"}})
    ]


def test_transition_by_name_dry_run_and_already_there_write_nothing() -> None:
    dry = _with_fake(_status_site("To Do"))
    assert jira._transition(_args(), "P-1", "start", dry_run=True) == "In Progress"
    there = _with_fake(_status_site("In Progress"))
    assert jira._transition(_args(), "P-1", "IN PROGRESS") == "In Progress"
    assert dry.writes == there.writes == []


def test_transition_refuses_an_unreachable_status() -> None:
    fake = _with_fake(_status_site("To Do"))
    assert _dies(lambda: jira._transition(_args(), "P-1", "Done")) == 4
    assert fake.writes == []


def test_planning_fields_map_points_and_sprint_to_field_ids() -> None:
    site = _sprint_site()
    site["/rest/api/3/field"] = [
        {"id": "customfield_1", "name": "Story Points"},
        {"id": "customfield_2", "name": "Sprint"},
    ]
    _with_fake(site)
    result: dict = {}
    fields = jira._planning_fields(_args(points=3.0, sprint="active"), "P", result)
    assert fields == {"customfield_1": 3.0, "customfield_2": 10}
    assert result == {"points": 3.0, "sprint": "S1"}
    assert jira._planning_fields(_args(), "P", {}) == {}


def main() -> int:
    tests = [
        (name, function)
        for name, function in sorted(globals().items())
        if name.startswith("test_") and callable(function)
    ]
    failed = 0
    for name, function in tests:
        try:
            function()
            print(f"PASS  {name}")
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
