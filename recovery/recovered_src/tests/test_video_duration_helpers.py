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
    / "util"
    / "need"
    / "EditAutoFlowItemEditDialog.py"
)


def _function_source(name: str) -> str:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.unparse(node)
    raise AssertionError(f"missing function {name}")


def test_video_duration_helpers_delegate_to_commoncode():
    duration_source = _function_source("_video_duration")
    index_source = _function_source("_video_duration_index")
    assert "CommonCode.parseVideoDuration" in duration_source
    assert "CommonCode.parseVideoIndex" in index_source


def test_commoncode_video_tiers_round_trip():
    from src.py.com.yun.mao.util.need import CommonCode

    assert CommonCode.VIDEO_DURATION_TIERS
    for index, tier in enumerate(CommonCode.VIDEO_DURATION_TIERS):
        assert CommonCode.parseVideoDuration(index) == tier
        assert CommonCode.parseVideoIndex(tier) == index
