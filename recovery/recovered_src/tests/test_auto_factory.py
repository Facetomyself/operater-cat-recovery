from __future__ import annotations


def test_auto_factory_dispatches_by_auto_type():
    from src.py.com.yun.mao.dclass.DTopClass import (
        AutoFlowBean,
        BanYunBean,
        DownLoadBean,
        YuLanBean,
        YunAutoBean,
        YunPreViewBean,
    )
    from src.py.com.yun.mao.dclass.DTopClassHelper import dic_to_Auto_obj

    cases = {
        1: BanYunBean,
        2: AutoFlowBean,
        3: YuLanBean,
        4: DownLoadBean,
        5: YunAutoBean,
        6: YunPreViewBean,
    }
    for auto_type, expected in cases.items():
        bean = dic_to_Auto_obj(
            {
                "kid": f"k{auto_type}",
                "auto_type": auto_type,
                "name": "flow",
                "source": "src",
            }
        )
        assert isinstance(bean, expected)
        assert bean.kid == f"k{auto_type}"
        assert bean.auto_type == auto_type
        assert bean.name == "flow"
        assert bean.source == "src"


def test_auto_factory_unwraps_bean_like_and_converts_nested_beans():
    from src.py.com.yun.mao.dclass.DTopClass import AutoFlowBean, ModelWrapper
    from src.py.com.yun.mao.dclass.DTopClassHelper import dic_to_Auto_obj

    bean = dic_to_Auto_obj(
        {
            "kid": "k",
            "auto_type": 2,
            "active": False,
            "priority": 7,
            "beanLike": {
                "name": "inner",
                "source": "src",
                "modelWrapper": {"model": "random", "random": True},
            },
        }
    )
    assert isinstance(bean, AutoFlowBean)
    assert bean.name == "inner"
    assert bean.source == "src"
    assert bean.active is False
    assert bean.priority == 7
    assert isinstance(bean.modelWrapper, ModelWrapper)
    assert bean.modelWrapper.random is True
