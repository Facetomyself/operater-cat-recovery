from __future__ import annotations


def test_sec_catalog_returns_decoded_messages():
    from src.py.com.yun.mao.link._fds_jm import sec

    assert sec("wl_feifa_03") == "非法信息，请重启软件尝试恢复！"
    assert sec("jqm_err_stop_04") == "机器码错误，终止操作！"
    assert sec("hy_feifa_05") == "非法会员，禁止使用！"
    assert "第 {attempt}/{max_retry} 次重试" in sec("sq_log_net_retry_32")


def test_sec_catalog_keeps_plain_ascii_values():
    from src.py.com.yun.mao.link._fds_jm import sec

    assert sec("md5") == "md5"
    assert sec("md5s") == "md5s"
    assert sec("dt_bc_wk_01") == "bcInWorker"


def test_abort_parts_decode_to_six_message_parts():
    from src.py.com.yun.mao.link import _fds_jm, _fds_sj

    parts = _fds_jm.decode_str_tuple(
        _fds_sj.ABORT_PARTS_ENC,
        _fds_sj.KEY,
    )
    assert len(parts) == 6
    assert parts[0] == "检测到调试器或可疑进程！"
    assert parts[-1] == "弹窗3秒后自动退出。"
    assert "x64dbg" in parts[3]
