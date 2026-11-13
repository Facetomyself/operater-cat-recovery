from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT.parent / "agent-notes" / "dyna_retranslate_pairs.json"
UI_DIR = ROOT / "src" / "resource" / "ui" / "dyna"


def _calls(tree: ast.Module, class_name: str):
    method = next(
        node
        for node in next(
            item for item in tree.body if isinstance(item, ast.ClassDef) and item.name == class_name
        ).body
        if isinstance(node, ast.FunctionDef) and node.name == "retranslateUi"
    )
    found = set()
    for node in ast.walk(method):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute) or not isinstance(func.value, ast.Attribute):
            continue
        owner = func.value
        if not (isinstance(owner.value, ast.Name) and owner.value.id == "self"):
            continue
        if not node.args:
            continue
        index = None
        if func.attr == "setItemText":
            if len(node.args) < 2:
                continue
            try:
                index = ast.literal_eval(node.args[0])
            except (ValueError, TypeError):
                continue
            arg = node.args[1]
        else:
            arg = node.args[0]
        if not isinstance(arg, ast.Call) or len(arg.args) < 2:
            continue
        if not isinstance(arg.args[1], ast.Constant):
            continue
        if index is None:
            found.add((owner.attr, func.attr, arg.args[1].value))
        else:
            found.add((owner.attr, func.attr, index, arg.args[1].value))
    return found


def test_generated_forms_contain_all_recovered_pairs():
    payload = json.loads(PAIRS.read_text(encoding="utf-8"))
    for module in payload["modules"]:
        short_name = module["module"]
        if short_name == "yun_yin_mao_main":
            continue
        path = UI_DIR / f"{short_name}.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        type_map = next(
            ast.literal_eval(node.value)
            for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "_TYPE_MAP"
        )
        found = _calls(tree, "Ui_Form")
        for triple in module["triples"]:
            if triple["method"] not in {
                "setText",
                "setTitle",
                "setPlaceholderText",
                "setItemText",
                "setCurrentText",
            }:
                continue
            if triple["widget"] not in type_map:
                continue
            args = ast.literal_eval(triple["args"])
            if triple["method"] == "setItemText":
                assert (
                    triple["widget"],
                    triple["method"],
                    triple.get("index"),
                    args[1],
                ) in found
            else:
                assert (triple["widget"], triple["method"], args[1]) in found
