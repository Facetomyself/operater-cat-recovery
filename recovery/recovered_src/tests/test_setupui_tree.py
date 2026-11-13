from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TREES = ROOT.parent / "agent-notes" / "dyna_setupui_trees.json"


def _walk(node):
    yield node
    for child in node.get("children", []):
        yield from _walk(child)


def test_ai_employee_setupui_tree_is_recovered():
    payload = json.loads(TREES.read_text(encoding="utf-8"))
    assert payload["schema"] == "operater-cat-dyna-setupui-trees.v1"
    module = next(item for item in payload["modules"] if item["module"] == "ai_employee_item")
    assert module["qword_refs"] > 100
    names = {node["name"] for node in _walk(module["tree"])}
    assert {
        "horizontalLayout",
        "verticalLayout",
        "horizontalLayout_8",
        "textEdit_em_role_display",
        "lineEdit_em_name",
        "btn_em_save",
    } <= names
