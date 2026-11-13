from __future__ import annotations


def test_sanitized_layer_neutralizes_card_key_and_destructive_entries():
    import ctypes
    import os
    import subprocess

    from src.py.com.yun.mao.ade import _ade_sing, _u_common
    from src.py.com.yun.mao.fea import (
        _cw_jm_file,
        _qf_rn_file,
        _yg_bn_file,
    )
    from src.py.com.yun.mao.link import (
        _fdg_ct_ew,
        _fdg_ct_is,
        _fds_h_x,
        _lk_gy_r,
        _lk_gy_w,
    )
    from src.py.com.yun.mao.sanitized import neutralize

    def _forbidden(*args, **kwargs):
        raise AssertionError("destructive primitive was called")

    neutralize.apply()
    original_popen = subprocess.Popen
    original_windll = ctypes.WinDLL
    original_system = os.system
    subprocess.Popen = _forbidden
    ctypes.WinDLL = _forbidden
    os.system = _forbidden
    try:
        assert _lk_gy_w.gy_jc_a5(object()) is True
        assert _lk_gy_r.gy_jc_b1(object()) is True
        assert _lk_gy_w._gy_uc() == "SANITIZED-UCODE"

        probe = _fds_h_x.FdsHhx()
        assert probe.jk_bd_api() is False
        assert probe.try_begin_abort() is False
        probe.fh_quan()
        probe.seal_abort()

        assert _qf_rn_file.g_wp_flush() is None
        assert _cw_jm_file.o_yt_purge() is None
        assert _yg_bn_file.v_hz_scrub() is None
        assert _fdg_ct_ew.ct_ew_drop() is None
        assert _fdg_ct_is.ct_is_snap() is None
        assert _u_common.encrypt_log([], "header") is False
        _ade_sing._ak()
    finally:
        neutralize.restore()
        subprocess.Popen = original_popen
        ctypes.WinDLL = original_windll
        os.system = original_system


def test_sanitized_restore_puts_the_faithful_gate_back():
    from src.py.com.yun.mao.sanitized import neutralize

    neutralize.apply()
    neutralize.restore()

    from src.py.com.yun.mao.link import _lk_gy_w

    assert _lk_gy_w.gy_jc_a5(object()) is False
