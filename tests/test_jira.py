#!/usr/bin/env python3
"""Description formatting tests for scripts/jira; no network."""

from __future__ import annotations

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
