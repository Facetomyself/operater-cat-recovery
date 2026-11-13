from __future__ import annotations

import ast
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "py"
    / "com"
    / "yun"
    / "mao"
    / "auto"
    / "CMCode.py"
)


def _getattr_default(attribute: str) -> int:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "getattr":
            continue
        if len(node.args) < 3:
            continue
        key = node.args[1]
        if isinstance(key, ast.Constant) and key.value == attribute:
            value = node.args[2]
            if isinstance(value, ast.Constant) and isinstance(value.value, int):
                return value.value
    raise AssertionError(f"missing getattr default for {attribute}")


def test_cmcode_retry_defaults_match_config():
    from src.py.com.yun.mao.config import YunYinMaoConfig

    assert YunYinMaoConfig.MAX_TRY_COUNT == 5
    assert YunYinMaoConfig.FILE_PART_PATCH_MAX_PER_N == 3
    assert YunYinMaoConfig.FILE_PART_PATCH_MAX_TOTAL == 50
    assert _getattr_default("MAX_TRY_COUNT") == 5
    assert _getattr_default("FILE_PART_PATCH_MAX_PER_N") == 3
    assert _getattr_default("FILE_PART_PATCH_MAX_TOTAL") == 50


def test_gen_blur_pic_signature_and_blur_infix():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "gen_blur_pic"
    )
    args = [argument.arg for argument in function.args.args]
    assert args == ["group_files", "path_message_map", "radius"]
    body = ast.unparse(function)
    assert "_blur." in body
    assert "old_name.split" in body
    assert "old_files, new_files" in body


def test_gen_preview_video_signature_and_preview_infix():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "gen_preview_video"
    )
    args = [argument.arg for argument in function.args.args]
    assert args == [
        "input_file",
        "photo_or_video_yulan_path_list_for_upload",
        "yuLanModeBean",
    ]
    body = ast.unparse(function)
    assert "_preview." in body
    assert "old_name.split" in body
    assert "FLOW_YU_LAN_MODEL_PRESENT" in body
    assert "STOPPED_BY_USER" in body
    assert "photo_or_video_yulan_path_list_for_upload.append" in body


def test_gen_yulan_if_need_signature_and_res_type_membership():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef)
        and node.name == "gen_yulan_if_need"
    )
    args = [argument.arg for argument in function.args.args]
    assert args == [
        "origin_group_file",
        "yuLanModeBean",
        "force_pic_preview",
    ]
    body = ast.unparse(function)
    assert "YU_LAN_RES_TYPE_VIDEO in yuLanModeBean.resType" in body
    assert "YU_LAN_RES_TYPE_PIC in yuLanModeBean.resType" in body
    assert "await gen_preview_video(" in body
