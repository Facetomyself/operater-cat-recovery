from __future__ import annotations

import asyncio
from types import SimpleNamespace

from src.py.com.yun.mao.dclass.DTopClass import (
    AdvancedFilterBean,
    BaseFilterBean,
    DurationFilterBean,
    SizeFilterBean,
)
from src.py.com.yun.mao.util.need.CommonCode import (
    checkSendMessagePermission,
    gen_base_filter,
    globalPicWater,
    globalVideoWater,
    match_duration_and_size,
    obtain_comment_to_id,
    parse_ids,
    parseVideoDuration,
    parseVideoIndex,
    privatePicWater,
    privateVideoWater,
    str_id_tip,
)


def test_duration_tier_round_trip():
    tiers = (60, 180, 300, 600, 1800, 3600, 5400, 7200, 9000)
    for index, duration in enumerate(tiers):
        assert parseVideoDuration(index) == duration
        assert parseVideoIndex(duration) == index
    assert parseVideoDuration(99) == 60
    assert parseVideoIndex(99) == 0


def test_private_and_global_water_helpers():
    water = SimpleNamespace(enPic=True, enVideo=False)
    top = SimpleNamespace(
        enPic=True,
        enVideo=False,
        topArgs=SimpleNamespace(water=water),
    )
    assert privatePicWater(top) == (True, top)
    assert privateVideoWater(top) == (False, "")
    assert globalPicWater(top) == (True, water)
    assert globalVideoWater(top) == (False, "")
    assert privatePicWater(None) == (False, "")


def test_text_and_id_helpers():
    assert str_id_tip(12, 13) == "最后12ID：13"
    assert str_id_tip(0, 13) == "最后0ID没有变化"
    assert obtain_comment_to_id([4, 5]) == 4
    assert obtain_comment_to_id(7) == 7
    assert obtain_comment_to_id(None) is None
    messages = SimpleNamespace(
        messages=[SimpleNamespace(id=1), SimpleNamespace(id=2)]
    )
    assert parse_ids(messages) == [1, 2]


def test_filter_model_and_generation():
    duration = DurationFilterBean(duration_min=1, duration_max=10)
    size = SizeFilterBean(min=1, max=20)
    base = BaseFilterBean(durationFilterBean=duration, sizeFilterBean=size)
    advanced = AdvancedFilterBean(keepSourceText=False, chaiZu=True)

    assert base.durationFilterBean is duration
    assert base.sizeFilterBean is size
    assert duration.min == 60
    assert advanced.keepSourceText is False
    assert advanced.chaiZu is True

    generated = gen_base_filter("1", "10", "2", "20")
    assert isinstance(generated, BaseFilterBean)
    assert generated.durationFilterBean.duration_min == 1
    assert generated.durationFilterBean.duration_max == 10
    assert generated.sizeFilterBean.min == 2
    assert generated.sizeFilterBean.max == 20

    video = SimpleNamespace(video=object(), duration=120, size=0)
    assert match_duration_and_size(video, generated) is True
    plain = SimpleNamespace(video=None, duration=0, size=4 * 1024 * 1024)
    assert match_duration_and_size(plain, generated) is True


def test_send_permission_checks_all_destinations():
    class Client:
        async def get_permissions(self, channel, me):
            return SimpleNamespace(
                is_admin=True,
                is_creator=False,
                is_banned=False,
                participant=None,
                default_banned_rights=None,
            )

    auto = SimpleNamespace(
        getName=lambda: "auto",
        getDestes=lambda: ["dest"],
        getYulanDestes=lambda: [],
        isYunAutoType=lambda: False,
        isYunPreViewType=lambda: False,
    )
    me = SimpleNamespace(full_name="tester")
    result = asyncio.run(
        checkSendMessagePermission(Client(), [auto], me)
    )
    assert result == (True, "")
