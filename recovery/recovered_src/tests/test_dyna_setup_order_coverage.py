from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "src" / "resource" / "ui" / "dyna"


def _module_order(tree: ast.Module) -> tuple[str, ...]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name)
            and target.id in {"SETUP_ORDER", "WIDGET_NAMES"}
            for target in node.targets
        ):
            continue
        value = ast.literal_eval(node.value)
        if isinstance(value, (tuple, list)):
            return tuple(str(item) for item in value)
    return ()


def _setup_ui(tree: ast.Module) -> ast.FunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "setupUi":
            return node
    return None


def test_generated_dyna_forms_create_every_declared_widget():
    checked = 0
    for path in sorted(UI_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        order = _module_order(tree)
        setup = _setup_ui(tree)
        if not order or setup is None:
            continue
        checked += 1
        attrs = set()
        literals = set()
        for node in ast.walk(setup):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        attrs.add(target.attr)
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                literals.add(node.value)
        missing = [
            name for name in order
            if name not in attrs and name not in literals
        ]
        assert not missing, f"{path.name}: {missing}"
    assert checked >= 8
