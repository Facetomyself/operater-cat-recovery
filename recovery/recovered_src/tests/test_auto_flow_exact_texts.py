from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src" / "resource" / "ui" / "dyna" / "auto_flow_item.py"

EXPECTED = {
    ("verticalGroupBox_4", "setTitle", "基础"),
    ("label", "setText", "来源频道/群组"),
    ("lineEdit_flow_source", "setPlaceholderText", "公有链接或私有ID(支持话题)"),
    ("auto_flow_topic_jiao_chen", "setText", "教程"),
    ("pushButton_auto_step1", "setText", "第一步、搬运到私密会员频道"),
    ("label_2", "setText", "会员目标频道/群组(支持多个，一行一个，支持话题)"),
    (
        "textEdit_flow_dest_list",
        "setPlaceholderText",
        "公有链接或私有ID（支持多个，一行一个，支持话题）",
    ),
    ("pushButton_auto_step2", "setText", "第二步、自动生成预览资源，并发布到公开预览频道"),
    ("label_4", "setText", "公开预览频道/群组(支持多个，一行一个，支持话题)"),
    (
        "textEdit_flow_auto_flow_dest_list",
        "setPlaceholderText",
        "公有链接或私有ID（支持多个，一行一个，支持话题）",
    ),
    ("ziyuanleiixing", "setTitle", "资源类型"),
    ("checkBox_flow_video_photo", "setText", "仅包含视频的消息组"),
    ("checkBox_flow_photo", "setText", "图片"),
    ("checkBox_flow_video", "setText", "视频"),
}

EXTRA_WIDGETS = {
    "verticalGroupBox_4",
    "pushButton_auto_step1",
    "label_2",
    "pushButton_auto_step2",
    "label_4",
    "ziyuanleiixing",
}


def _call_name(node: ast.Call):
    func = node.func
    if not isinstance(func, ast.Attribute):
        return None
    if not isinstance(func.value, ast.Attribute):
        return None
    owner = func.value
    if not (isinstance(owner.value, ast.Name) and owner.value.id == "self"):
        return None
    return owner.attr, func.attr


def test_auto_flow_retranslate_has_exact_pairs():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    retranslate = next(
        node
        for node in next(
            item
            for item in tree.body
            if isinstance(item, ast.ClassDef) and item.name == "Ui_Form"
        ).body
        if isinstance(node, ast.FunctionDef) and node.name == "retranslateUi"
    )
    found = set()
    for node in ast.walk(retranslate):
        if not isinstance(node, ast.Call):
            continue
        pair = _call_name(node)
        if pair is None or pair[1] not in {"setText", "setTitle", "setPlaceholderText"}:
            continue
        if not node.args:
            continue
        arg = node.args[0]
        if (
            isinstance(arg, ast.Call)
            and (
                (isinstance(arg.func, ast.Name) and arg.func.id == "_translate")
                or (
                    isinstance(arg.func, ast.Attribute)
                    and arg.func.attr == "translate"
                )
            )
            and len(arg.args) >= 2
            and isinstance(arg.args[1], ast.Constant)
        ):
            found.add((pair[0], pair[1], arg.args[1].value))
    assert EXPECTED <= found


def test_auto_flow_type_map_includes_extra_widgets():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    type_map = next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "_TYPE_MAP"
    )
    assert EXTRA_WIDGETS <= set(type_map)
