from __future__ import annotations

import ast
import dataclasses
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "src" / "py" / "com" / "yun" / "mao"


def _fields(cls) -> list[str]:
    return [item.name for item in dataclasses.fields(cls)]


def test_comment_rule_bean_matches_compiled_init_signature():
    from src.py.com.yun.mao.dclass.DTopClass import CommentRuleBean

    assert _fields(CommentRuleBean) == [
        "copyComment",
        "wantCount",
        "dtype",
        "forWardAction",
        "baseFilter",
        "advancedFilterBean",
        "tail",
        "replace",
        "water",
        "selfAdWrapper",
        "yuLanResOp",
        "aiEmployee",
        "aiRefusedOpt",
        "grid",
        "randomCover",
    ]


def test_super_flow_and_auto_bean_carry_link_and_version_fields():
    from src.py.com.yun.mao.dclass.DTopClass import AutoBean, SuperFlowBean

    super_fields = _fields(SuperFlowBean)
    for name in (
        "huiYuanLink",
        "youKeLink",
        "yuLanModeBean",
        "durationInfo",
    ):
        assert name in super_fields
    auto_fields = _fields(AutoBean)
    for name in ("commentRule", "completeVersionOp", "botBean"):
        assert name in auto_fields


def test_small_bean_field_sets_match_compiled_signatures():
    from src.py.com.yun.mao.dclass.DTopClass import (
        AdWrapper,
        AiRefusedOption,
        GridOpt,
        Tail,
    )

    assert _fields(Tail) == ["tail_text"]
    assert _fields(AdWrapper) == [
        "adEnable",
        "adIsBottomUp",
        "delete",
        "ades",
    ]
    assert _fields(AiRefusedOption) == ["action"]
    assert _fields(GridOpt) == ["number"]


def test_duration_mode_keeps_its_own_fields_and_converter():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper
    from src.py.com.yun.mao.dclass.DTopClass import DurationMode

    assert _fields(DurationMode) == [
        "resType",
        "mode",
        "presentMode",
        "durationMode",
    ]
    converted = helper.dic_to_DurationMode_obj(
        {"resType": "video", "mode": "duration"}
    )
    assert isinstance(converted, DurationMode)
    assert converted.resType == "video"
    assert converted.mode == "duration"


def test_all_simple_dataclass_fields_match_compiled_signatures():
    from src.py.com.yun.mao.dclass import DTopClass as module

    expected = {
        "Ad": ["adId", "files", "text", "name"],
        "AdWrapper": ["adEnable", "adIsBottomUp", "delete", "ades"],
        "AddDurationInfo": ["addDurationInfo", "blockquote"],
        "AdvancedFilterBean": [
            "keepSourceText",
            "deleSourceText",
            "deleLink",
            "filterButton",
            "discardNoTextResource",
            "chaiZu",
            "containWords",
            "excludeWords",
        ],
        "AiEmployee": ["enable", "uid"],
        "AiRefusedOption": ["action"],
        "BaseFilterBean": ["durationFilterBean", "sizeFilterBean"],
        "BotBean": ["user_name"],
        "CommentBean": ["copyComment"],
        "CompleteVersionOp": ["blockquote", "linkText"],
        "DurationFilterBean": [
            "duration_min",
            "duration_max",
            "duration_min_second",
            "duration_max_second",
        ],
        "DurationMode": ["resType", "mode", "presentMode", "durationMode"],
        "ForwardActionBean": [
            "action",
            "randon_sleep_min",
            "randon_sleep_max",
        ],
        "GridOpt": ["number"],
        "HuiYuanLink": [
            "enable",
            "text",
            "enableCustomerLink",
            "customerHttpLink",
            "blockquote",
        ],
        "Increase": ["startId", "wantCount", "numberMode"],
        "Loop": ["startId", "endId"],
        "ModelWrapper": ["model", "random", "increase", "loop"],
        "PresentMode": ["present"],
        "Random": ["wantCount", "numberMode"],
        "Replace": ["replaces"],
        "SizeFilterBean": ["min", "max"],
        "Tail": ["tail_text"],
        "Water": [
            "enPic",
            "enVideo",
            "text",
            "picPath",
            "mode",
            "duration",
            "picRatio",
        ],
        "YouKeLink": ["enable", "text", "httpLink", "blockquote"],
        "YuLanModeBean": [
            "resType",
            "mode",
            "presentMode",
            "durationMode",
        ],
        "YuLanResOp": ["picBlur", "spoiler", "radius"],
    }
    for name, fields in expected.items():
        assert _fields(getattr(module, name)) == fields, name


def test_comment_rule_dialog_only_passes_declared_fields():
    from src.py.com.yun.mao.dclass.DTopClass import (
        AdWrapper,
        AiRefusedOption,
        CommentRuleBean,
        GridOpt,
        Tail,
    )

    classes = {
        "AdWrapper": _fields(AdWrapper),
        "AiRefusedOption": _fields(AiRefusedOption),
        "CommentRuleBean": _fields(CommentRuleBean),
        "GridOpt": _fields(GridOpt),
        "Tail": _fields(Tail),
    }
    tree = ast.parse(
        (SOURCE / "comment" / "ConfigCommentRuleDialog.py").read_text(
            encoding="utf-8"
        )
    )
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name):
            continue
        fields = classes.get(node.func.id)
        if fields is None:
            continue
        for keyword in node.keywords:
            if keyword.arg is None:
                continue
            assert keyword.arg in fields, (
                f"{node.func.id} line {node.lineno}: "
                f"unknown keyword {keyword.arg}"
            )
