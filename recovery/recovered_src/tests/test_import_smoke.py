from __future__ import annotations

import importlib

import pytest


PURE_MODULES = (
    "src.resource.ui.dyna",
    "src.py.com.yun.mao.auto.GlobalWorkingLock",
    "src.py.com.yun.mao.auto.down_load_config",
    "src.py.com.yun.mao.cd.Working",
    "src.py.com.yun.mao.config.NewConfig",
    "src.py.com.yun.mao.dclass.AutoBeanXXX",
    "src.py.com.yun.mao.dclass.DTopClass",
    "src.py.com.yun.mao.fea._pl_wd_file",
    "src.py.com.yun.mao.fea._sq_chk",
    "src.py.com.yun.mao.fea._sq_jqm",
    "src.py.com.yun.mao.fea._sq_r_req",
    "src.py.com.yun.mao.link._fds_sj",
    "src.py.com.yun.mao.link._fds_rt",
    "src.py.com.yun.mao.link._fds_tan",
    "src.py.com.yun.mao.monitor.MonitorStyleDef",
    "src.py.com.yun.mao.tab.BirderConstants",
    "src.py.com.yun.mao.util.AI_INNER_DEF",
    "src.py.com.yun.mao.util.AiTestTipHtmlHelper",
    "src.py.com.yun.mao.util.AppStyleDef",
    "src.py.com.yun.mao.util.EnumClass",
    "src.py.com.yun.mao.util.SuspendFrozenTag",
    "src.py.com.yun.mao.util.need.utils",
    "src.py.com.yun.mao.water.WaterConstants",
)


@pytest.mark.parametrize("module_name", PURE_MODULES)
def test_pure_modules_import_without_runtime_dependencies(module_name):
    module = importlib.import_module(module_name)
    assert module is not None
