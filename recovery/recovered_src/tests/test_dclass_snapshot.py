from __future__ import annotations

import base64
import gzip
import json

from src.py.com.yun.mao.dclass import ItemMemStore, LoadDataClass


def setup_function():
    ItemMemStore.reset_bootstrap_flag_for_tests()


def test_dirty_generation_only_clears_matching_snapshot():
    ItemMemStore.apply_snapshot({"autoMap": {"a": {"name": "a"}}})
    generation = ItemMemStore.get_dirty_generation()
    ItemMemStore.mark_item_dirty()
    assert ItemMemStore.is_item_dirty()
    assert ItemMemStore.get_dirty_generation() == generation + 1
    assert not ItemMemStore.clear_item_dirty_if_generation(generation)
    assert ItemMemStore.clear_item_dirty_if_generation(generation + 1)
    assert not ItemMemStore.is_item_dirty()


def test_cloud_snapshot_bootstrap_accepts_gzip_base64():
    snapshot = {"autoMap": {"kid": {"name": "cloud"}}, "scheduler": None}
    payload = base64.b64encode(
        gzip.compress(json.dumps(snapshot).encode("utf-8"))
    ).decode("ascii")
    branch = ItemMemStore.bootstrap_item_memory(
        False,
        False,
        "gzip",
        payload,
    )
    assert branch == "cloud_hit"
    assert ItemMemStore.is_bootstrapped()
    assert ItemMemStore.dump_snapshot()["autoMap"]["kid"]["name"] == "cloud"


def test_load_data_class_indexes_auto_map():
    obj = LoadDataClass.loadDTopClass(
        {"autoMap": {"k1": {"kid": "k1", "name": "flow"}}}
    )
    assert obj.autoMap["k1"].name == "flow"
    assert LoadDataClass.getAutoBeanById("k1").name == "flow"


def test_load_data_class_converts_nested_bean_dicts():
    from src.py.com.yun.mao.dclass.DTopClass import (
        CommentRuleBean,
        GridOpt,
        ModelWrapper,
        Tail,
        Water,
    )

    obj = LoadDataClass.loadDTopClass(
        {
            "autoMap": {
                "k2": {
                    "kid": "k2",
                    "name": "nested",
                    "modelWrapper": {"model": "random", "random": True},
                    "tail": {"tail_text": "tail"},
                    "water": {"enPic": True, "text": "wm"},
                    "commentRule": {
                        "copyComment": True,
                        "grid": {"number": 4},
                    },
                }
            }
        }
    )
    bean = obj.autoMap["k2"]
    assert isinstance(bean.modelWrapper, ModelWrapper)
    assert bean.modelWrapper.model == "random"
    assert isinstance(bean.tail, Tail)
    assert bean.tail.tail_text == "tail"
    assert isinstance(bean.water, Water)
    assert bean.water.enPic is True
    assert isinstance(bean.commentRule, CommentRuleBean)
    assert bean.commentRule.copyComment is True
    assert isinstance(bean.commentRule.grid, GridOpt)
    assert bean.commentRule.grid.number == 4


def test_snapshot_round_trip_preserves_nested_bean_types():
    from src.py.com.yun.mao.dclass.DTopClass import (
        AddDurationInfo,
        AdWrapper,
        AdvancedFilterBean,
        AiEmployee,
        AiRefusedOption,
        AutoFlowBean,
        BaseFilterBean,
        BotBean,
        CompleteVersionOp,
        ForwardActionBean,
        GridOpt,
        HuiYuanLink,
        ModelWrapper,
        Replace,
        Tail,
        Water,
        YouKeLink,
        YuLanModeBean,
        YuLanResOp,
    )

    LoadDataClass.loadDTopClass(
        {
            "autoMap": {
                "k": {
                    "kid": "k",
                    "name": "nested",
                    "auto_type": 2,
                    "modelWrapper": {"model": "m", "random": True},
                    "selfAdWrapper": {
                        "adEnable": True,
                        "ades": [{"adId": "a1"}],
                    },
                    "advancedFilterBean": {"containWords": ["x"]},
                    "baseFilter": {
                        "durationFilterBean": {"duration_min": 1},
                        "sizeFilterBean": {"min": 2},
                    },
                    "tail": {"tail_text": "t"},
                    "replace": {"replaces": ["a->b"]},
                    "water": {"enPic": True},
                    "commentRule": {
                        "copyComment": True,
                        "grid": {"number": 6},
                    },
                    "huiYuanLink": {"enable": True, "text": "v"},
                    "youKeLink": {"enable": True, "text": "g"},
                    "yuLanModeBean": {
                        "resType": "video",
                        "mode": "present",
                        "presentMode": {"present": "30"},
                    },
                    "durationInfo": {"addDurationInfo": True},
                    "completeVersionOp": {"linkText": "l"},
                    "botBean": {"user_name": "b"},
                    "forWardAction": {"action": "auto"},
                    "yuLanResOp": {"picBlur": True},
                    "aiEmployee": {"uid": 1},
                    "aiRefusedOpt": {"action": "skip"},
                    "grid": {"number": 6},
                }
            }
        }
    )
    raw = json.loads(
        json.dumps(
            LoadDataClass._snapshot_dict(),
            default=LoadDataClass._json_default,
        )
    )
    bean = LoadDataClass.loadDTopClass(raw).autoMap["k"]

    assert isinstance(bean, AutoFlowBean)
    assert isinstance(bean.modelWrapper, ModelWrapper)
    assert bean.modelWrapper.model == "m"
    assert isinstance(bean.selfAdWrapper, AdWrapper)
    assert bean.selfAdWrapper.ades[0].adId == "a1"
    assert isinstance(bean.advancedFilterBean, AdvancedFilterBean)
    assert bean.advancedFilterBean.containWords == ["x"]
    assert isinstance(bean.baseFilter, BaseFilterBean)
    assert isinstance(bean.tail, Tail) and bean.tail.tail_text == "t"
    assert isinstance(bean.replace, Replace)
    assert isinstance(bean.water, Water) and bean.water.enPic is True
    assert bean.commentRule.copyComment is True
    assert isinstance(bean.commentRule.grid, GridOpt)
    assert isinstance(bean.huiYuanLink, HuiYuanLink)
    assert isinstance(bean.youKeLink, YouKeLink)
    assert isinstance(bean.yuLanModeBean, YuLanModeBean)
    assert isinstance(bean.durationInfo, AddDurationInfo)
    assert isinstance(bean.completeVersionOp, CompleteVersionOp)
    assert isinstance(bean.botBean, BotBean)
    assert isinstance(bean.forWardAction, ForwardActionBean)
    assert isinstance(bean.yuLanResOp, YuLanResOp)
    assert isinstance(bean.aiEmployee, AiEmployee)
    assert isinstance(bean.aiRefusedOpt, AiRefusedOption)
