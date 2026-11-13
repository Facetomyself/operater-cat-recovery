from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HELPER_MODULE = "src.py.com.yun.mao.dialog.ImageDialogHelper"


def test_image_dialog_helper_is_imported_as_a_module():
    bad = []
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if (node.module or "").endswith("dialog.ImageDialogHelper"):
                if any(alias.name == "ImageDialogHelper" for alias in node.names):
                    bad.append(f"{path.relative_to(SRC)}:{node.lineno}")
    assert bad == []


def test_image_dialog_helper_calls_pass_a_parent():
    bad = []
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not isinstance(func, ast.Attribute):
                continue
            if not isinstance(func.value, ast.Name):
                continue
            if func.value.id != "ImageDialogHelper":
                continue
            if not func.attr.startswith("unifyShow"):
                continue
            if not node.args:
                bad.append(
                    f"{path.relative_to(SRC)}:{node.lineno}:{func.attr}"
                )
    assert bad == []
