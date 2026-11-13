from __future__ import annotations

from src.py.com.yun.mao.util import EnumClass


def test_enum_constants_match_runtime_dictionary():
    assert EnumClass.CARD_EXPERIENCE == "experience"
    assert EnumClass.CARD_BEGINNER == "beginner"
    assert EnumClass.CARD_ADVANCED == "advanced"
    assert EnumClass.CARD_GEEK == 2
    assert EnumClass.NOT_EXIT == -1
    assert EnumClass.YOU_KE == 0
    assert EnumClass.HUI_YUAN == 1
    assert EnumClass.EXP_EIGHT == 3
    assert EnumClass.FREEZE == 2
