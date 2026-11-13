from __future__ import annotations

import hashlib

from src.py.com.yun.mao.dclass.AutoBeanXXX import AutoBeanXXX
from src.py.com.yun.mao.dclass.DTopClass import AutoBean
from src.py.com.yun.mao.util.need import utils


def test_auto_bean_topic_uses_private_channel_parts():
    bean = AutoBean(db_channel="https://t.me/c/123456/789")
    wrapped = AutoBeanXXX(kid="k1", auto_type=2, exec_obj=bean)
    assert wrapped.getDbChannelTopic() == "789"
    assert wrapped.getDbChannel() == "https://t.me/c/123456/789"


def test_auto_bean_topic_empty_for_non_private_channel():
    bean = AutoBean(db_channel="https://t.me/demo")
    wrapped = AutoBeanXXX(kid="k2", auto_type=2, exec_obj=bean)
    assert wrapped.getDbChannelTopic() == ""


def test_generate_hash_matches_sha256():
    assert utils.generate_hash("demo") == hashlib.sha256(b"demo").hexdigest()
