from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "src" / "resource" / "ui" / "dyna"
DIALOG_DIR = ROOT / "src" / "py" / "com" / "yun" / "mao" / "util" / "need"

FORM_MODULES = {
    "ai_employee_item": "EditEmployeeItemEditDialog.py",
    "auto_flow_item": "EditAutoFlowItemEditDialog.py",
    "ban_yun_flow_comment_item": "EditBanYunCommentItemEditDialog.py",
    "down_load_flow_item": "EditDownLoadItemEditDialog.py",
    "yulan_flow_item": "EditYulanFlowItemEditDialog.py",
    "yun_auto_item": "EditYunAutoItemEditDialog.py",
    "yun_preview_item": "EditYunPreViewItemEditDialog.py",
}


def _class_attr(tree: ast.Module, class_name: str, attr_name: str):
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name != class_name:
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                continue
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id == attr_name:
                return ast.literal_eval(stmt.value)
    return None


def test_dyna_modules_exist_and_define_setup():
    expected = set(FORM_MODULES) | {"yun_yin_mao_main"}
    actual = {path.stem for path in UI_DIR.glob("*.py") if path.name != "__init__.py"}
    assert actual == expected
    for name in expected:
        tree = ast.parse((UI_DIR / f"{name}.py").read_text(encoding="utf-8"))
        class_name = "Ui_MainWindow" if name == "yun_yin_mao_main" else "Ui_Form"
        classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
        assert class_name in classes
        methods = {node.name for node in classes[class_name].body if isinstance(node, ast.FunctionDef)}
        assert {"setupUi", "retranslateUi"} <= methods


def test_form_type_maps_match_dialog_contracts():
    for short_name, dialog_name in FORM_MODULES.items():
        dialog_tree = ast.parse((DIALOG_DIR / dialog_name).read_text(encoding="utf-8-sig"))
        expected = None
        ui_module = None
        for node in dialog_tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            for stmt in node.body:
                if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                    continue
                target = stmt.targets[0]
                if not isinstance(target, ast.Name):
                    continue
                if target.id == "UI_MODULE":
                    ui_module = ast.literal_eval(stmt.value)
                elif target.id == "WIDGET_NAMES":
                    expected = tuple(ast.literal_eval(stmt.value))
            if ui_module and ui_module.endswith(f".{short_name}"):
                break
        assert expected is not None
        tree = ast.parse((UI_DIR / f"{short_name}.py").read_text(encoding="utf-8"))
        type_map = None
        setup_order = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == "_TYPE_MAP":
                    type_map = ast.literal_eval(node.value)
                elif isinstance(target, ast.Name) and target.id == "SETUP_ORDER":
                    setup_order = ast.literal_eval(node.value)
        assert type_map is not None
        assert setup_order is not None
        assert set(expected) <= set(type_map)
        assert set(setup_order) == set(type_map)
        assert len(setup_order) == len(type_map)
        assert all(name.isidentifier() for name in type_map)


def test_main_window_surface():
    tree = ast.parse((UI_DIR / "yun_yin_mao_main.py").read_text(encoding="utf-8"))
    names = _class_attr(tree, "Ui_MainWindow", "WIDGET_NAMES")
    if names is None:
        names = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == "WIDGET_NAMES":
                    names = ast.literal_eval(node.value)
                    break
    assert names is not None
    assert {"tabWidget_important", "text_brow_log", "action_reset", "action_copy_code"} <= set(names)


def test_generated_modules_have_no_placeholder_bodies():
    for path in UI_DIR.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            assert len(node.body) > 0
            first = node.body[0]
            assert not (isinstance(first, ast.Pass) and len(node.body) == 1)
            if isinstance(first, ast.Raise) and isinstance(first.exc, ast.Call):
                func = first.exc.func
                assert not (isinstance(func, ast.Name) and func.id == "NotImplementedError")


def test_setup_ui_assigns_every_widget_in_type_map():
    for short_name in FORM_MODULES:
        tree = ast.parse((UI_DIR / f"{short_name}.py").read_text(encoding="utf-8"))
        type_map = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == "_TYPE_MAP":
                    type_map = ast.literal_eval(node.value)
                    break
        assert type_map is not None
        method = next(
            node
            for node in next(
                item for item in tree.body if isinstance(item, ast.ClassDef) and item.name == "Ui_Form"
            ).body
            if isinstance(node, ast.FunctionDef) and node.name == "setupUi"
        )
        assigned = set()
        for node in ast.walk(method):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    assigned.add(target.attr)
        assert set(type_map) <= assigned
