from __future__ import annotations

from types import SimpleNamespace


def test_resource_action_and_mode_helpers():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    assert helper.get_action_text(helper.ACTION_AUTO) == "自动方式"
    assert helper.get_action_text(helper.ACTION_DOWNLOAD) == "强制下载方式"
    assert helper.get_resource_text("video_photo") == "仅包含视频的消息组"
    assert helper.get_resource_text("photo,video") == "图片,视频"
    assert helper.get_model_text("random") == "随机模式"
    assert helper.get_present_text("short") == "预览视频占比：10%"
    assert helper.get_present_text("customer") == "预览视频占比：customer%"


def test_filter_word_and_dest_round_trips():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    assert helper.filter_words_to_str([" a ", "b"]) == "a|b"
    assert helper.str_to_filter_words("a| b ") == ["a", "b"]
    assert helper.destes_to_str(["a", " b "]) == "a\nb"
    assert helper.str_to_destes("a\n b ") == ["a", "b"]
    assert helper.replaces_to_str(SimpleNamespace(replaces=["a->b"])) == "a->b"
    assert helper.replaces_to_str([("a", "b")]) == "a->b"
    assert helper.str_to_replaces("a->b\nc->d") == ["a->b", "c->d"]


def test_gen_base_filter_desc():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    base = SimpleNamespace(
        durationFilterBean=SimpleNamespace(min=1, max=10),
        sizeFilterBean=SimpleNamespace(min=2, max=20),
    )
    assert (
        helper.gen_base_filter_desc(base)
        == "时长范围：1 ~ 10 分钟；大小范围：2 ~ 20 MB"
    )


def test_ad_file_round_trip(tmp_path):
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    first = tmp_path / "first.html"
    second = tmp_path / "second.html"
    first.write_text("one", encoding="utf-8")
    second.write_text("two", encoding="utf-8")
    assert helper.ad_file_to_str(f"{first}\n{second}") == "onetwo"

    output = helper.ad_str_to_file("hello")
    try:
        with open(output, "r", encoding="utf-8") as handle:
            assert handle.read() == "hello"
    finally:
        import os

        os.remove(output)


def test_gen_bean_format_text_smoke():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    bean = SimpleNamespace(
        is_ramdom_mode=lambda: True,
        ramdom_want_count=lambda: 3,
        ramdom_numberMode=lambda: "group",
        is_increase_mode=lambda: False,
        is_loop_mode=lambda: False,
        getName=lambda: "demo",
        getSource=lambda: "@source",
        getDestes=lambda: ["@dest"],
        dtype="photo",
        model="random",
        forWardAction=SimpleNamespace(action="auto"),
        commentRule=SimpleNamespace(copyComment=False, wantCount=0),
        baseFilter=SimpleNamespace(
            durationFilterBean=SimpleNamespace(min=1, max=10),
            sizeFilterBean=SimpleNamespace(min=2, max=20),
        ),
        advancedFilterBean=SimpleNamespace(
            keepSourceText=True,
            deleSourceText=False,
            deleLink=False,
            containWords=[],
            excludeWords=[],
            filterButton=False,
        ),
        tail=None,
        aiEmployee=None,
        water=None,
        selfAdWrapper=SimpleNamespace(
            adEnable=False,
            adIsBottomUp=False,
            delete=False,
        ),
    )
    text = helper.genBeanFormatText(bean)
    assert "随机模式，随机参数->期望数量：3" in text
    assert "名称：demo" in text
    assert "来源：@source" in text
    assert "目标：@dest" in text
    assert "资源类型：图片" in text
    assert "模式选择：随机模式" in text
    assert "搬运方式：自动方式" in text
    assert "评论区：没有开启评论区复刻" in text
    assert "AI文案：未开启" in text
    assert "AI文案：AI文案" not in text


def test_dic_to_helpers_apply_recovered_defaults():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    forward = helper.dic_to_forWardAction({"action": "auto"})
    assert forward.action == "auto"
    assert forward.randon_sleep_min == 3
    assert forward.randon_sleep_max == 5

    assert helper.dic_to_GridOpt({}).number == 6
    assert helper.dic_to_CommentRuleBean_obj({}).wantCount == 0

    mode = helper.dic_to_yuLanModeBean_obj(
        {
            "mode": "present_model",
            "presentMode": {"present": "short"},
        }
    )
    assert mode.presentMode.present == "short"
