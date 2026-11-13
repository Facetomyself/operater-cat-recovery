from __future__ import annotations

from src.py.com.yun.mao.fea._fs_jh_zb_file import assemble_parse_beans_from_messages
from src.py.com.yun.mao.util.need.AllBeanDef import CreateOrderBean, ParseBean
from src.py.com.yun.mao.util.need.signals import global_ui_signal
from src.py.com.yun.mao.util.need import utils


def test_parse_plan_assembles_parse_bean():
    messages = [type("M", (), {"id": 1, "text": "hello"})()]
    plan = {
        "planId": "p1",
        "requestId": "r1",
        "groups": [{"uniId": "u1", "msgIds": [1], "tartMsgId": 1}],
    }
    beans = assemble_parse_beans_from_messages(plan, messages)
    assert len(beans) == 1
    assert isinstance(beans[0], ParseBean)
    assert beans[0].uniId == "u1"


def test_bean_and_signal_fallbacks():
    assert CreateOrderBean(otype="x").to_string().startswith("CreateOrderBean(")
    assert global_ui_signal is not None


def test_pure_utils_contracts():
    assert utils.split_session(r"C:\x\a.session")[1] == "a.session"
    assert utils.extract_username_or_channel("https://t.me/demo") == "demo"
    assert utils.convertPrivateIdIfNeed("123") == "-100123"
    assert utils.strTobool("yes")
    assert utils.format_time(65) == "1分5秒"
