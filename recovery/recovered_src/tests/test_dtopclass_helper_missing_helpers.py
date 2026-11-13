from __future__ import annotations


def test_comment_and_model_wrapper_converters():
    from src.py.com.yun.mao.dclass.DTopClass import CommentBean, ModelWrapper
    from src.py.com.yun.mao.dclass.DTopClassHelper import (
        dic_to_Comment_obj,
        dic_to_modelWrapper,
    )

    comment = dic_to_Comment_obj({"copyComment": True})
    assert isinstance(comment, CommentBean)
    assert comment.copyComment is True

    model = dic_to_modelWrapper({"model": "random", "random": True})
    assert isinstance(model, ModelWrapper)
    assert model.model == "random"
    assert model.random is True


def test_default_base_filter_and_preview_description():
    from src.py.com.yun.mao.config import YunYinMaoConfig
    from src.py.com.yun.mao.dclass.DTopClass import (
        BaseFilterBean,
        DurationFilterBean,
        SizeFilterBean,
    )
    from src.py.com.yun.mao.dclass.DTopClassHelper import (
        gen_default_base_filter_bean,
        gen_yulan_des,
    )

    base = gen_default_base_filter_bean()
    assert isinstance(base, BaseFilterBean)
    assert isinstance(base.durationFilterBean, DurationFilterBean)
    assert base.durationFilterBean.duration_min == YunYinMaoConfig.BASE_FILTER_DU_MIN
    assert base.durationFilterBean.duration_max == YunYinMaoConfig.BASE_FILTER_DU_MAX
    assert isinstance(base.sizeFilterBean, SizeFilterBean)
    assert base.sizeFilterBean.min == YunYinMaoConfig.BASE_FILTER_SIZE_MIN
    assert base.sizeFilterBean.max == YunYinMaoConfig.BASE_FILTER_SIZE_MAX

    class Auto:
        @staticmethod
        def getYulanDestes():
            return ["a", "b"]

    assert gen_yulan_des(Auto()) == "a\nb"


def test_ai_info_aliases_comment_ai_info():
    from src.py.com.yun.mao.dclass import DTopClassHelper as helper

    employee = type("Employee", (), {"enable": False, "uid": 0})()
    assert helper.ai_info(employee) == helper.comment_ai_info(employee)


def test_auto_desc_includes_recovered_comment_and_link_lines():
    from src.py.com.yun.mao.dclass.DTopClass import (
        AUTO_BEAN_TYPE_YUN_AUTO,
        AutoBean,
        HuiYuanLink,
        YouKeLink,
    )
    from src.py.com.yun.mao.dclass.DTopClassHelper import auto_desc

    bean = AutoBean(
        name="n",
        source="s",
        huiYuanLink=HuiYuanLink(enable=True, text="vip"),
        youKeLink=YouKeLink(enable=True, text="guest"),
    )
    text = auto_desc(bean)
    assert "评论区详情：" in text
    assert "会员链接：文案：vip" in text
    assert "游客链接：文案：guest" in text

    yun = AutoBean(
        name="y",
        source="s",
        auto_type=AUTO_BEAN_TYPE_YUN_AUTO,
        db_channel="private-db",
        yulan_destes=["@preview"],
    )
    yun_text = auto_desc(yun)
    assert "私有仓库：private-db" in yun_text
    assert "预览目标：@preview" in yun_text


def test_model_wrapper_keeps_mode_fields_for_autobean_accessors():
    from src.py.com.yun.mao.dclass.DTopClass import AutoBean
    from src.py.com.yun.mao.dclass.DTopClassHelper import dic_to_modelWrapper

    wrapper = dic_to_modelWrapper(
        {
            "model": "random",
            "random": True,
            "wantCount": 5,
            "numberMode": "group",
        }
    )
    bean = AutoBean(modelWrapper=wrapper)
    assert bean.is_ramdom_mode()
    assert bean.ramdom_want_count() == 5
    assert bean.ramdom_numberMode() == "group"

    loop = dic_to_modelWrapper(
        {"model": "loop", "loop": True, "startId": 1, "endId": 9}
    )
    loop_bean = AutoBean(modelWrapper=loop)
    assert loop_bean.loop_mode_startId() == 1
    assert loop_bean.loop_mode_endId() == 9

    increase = dic_to_modelWrapper(
        {
            "model": "increase",
            "increase": True,
            "startId": 3,
            "wantCount": 7,
        }
    )
    increase_bean = AutoBean(modelWrapper=increase)
    assert increase_bean.increase_startId() == 3
    assert increase_bean.increase_want_count() == 7
