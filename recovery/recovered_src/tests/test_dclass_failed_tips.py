from __future__ import annotations

from src.py.com.yun.mao.dclass.DTopClass import AutoBean, ModelWrapper


def test_random_mode_failed_tips(capsys):
    bean = AutoBean(
        source="src_channel",
        modelWrapper=ModelWrapper(random=True),
    )
    bean.printFailedTips()
    output = capsys.readouterr().out
    assert "当前频道： src_channel|src_channel" in output
    assert "当前搬运模式为随机模式" in output
    assert "清除资源记录" in output


def test_increase_mode_failed_tips(capsys):
    bean = AutoBean(
        source="src_channel",
        modelWrapper=ModelWrapper(increase=True),
    )
    bean.printFailedTips()
    output = capsys.readouterr().out
    assert "当前搬运模式为顺序模式" in output
    assert "继续顺序模式搬运频道资源" in output
