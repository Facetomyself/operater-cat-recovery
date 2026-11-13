from __future__ import annotations

import sys
import types

import pytest


def _entry(module):
    return next(
        value
        for name, value in vars(module).items()
        if callable(value)
        and not name.startswith("_")
        and getattr(value, "__module__", None) == module.__name__
    )


def test_be_s0_ij_z5_shows_abort_only_when_window_visible(monkeypatch):
    import src.py.com.yun.mao as mao_pkg
    from src.py.com.yun.mao.bz_uc import gi_x9_hk_y8
    from src.py.com.yun.mao.kv_nx import be_s0_ij_z5
    from src.py.com.yun.mao.link import _fds_sj
    from src.py.com.yun.mao.rm_qh import gs_w3_df_u0

    calls = []

    class FakeWindow:
        def __init__(self, visible):
            self.visible = visible

        def isVisible(self):
            return self.visible

    fake_geh = types.ModuleType("src.py.com.yun.mao.GlobalExceptionHandler")
    fake_geh.global_window = FakeWindow(True)
    fake_error = types.ModuleType("src.py.com.yun.mao.ErrorDialog")
    fake_error.show_error_tip = lambda **kwargs: calls.append(("tip", kwargs))

    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.GlobalExceptionHandler", fake_geh
    )
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.ErrorDialog", fake_error
    )
    monkeypatch.setattr(mao_pkg, "GlobalExceptionHandler", fake_geh, raising=False)
    monkeypatch.setattr(mao_pkg, "ErrorDialog", fake_error, raising=False)
    monkeypatch.setattr(_fds_sj, "ABORT_PARTS_ENC", "enc")
    monkeypatch.setattr(_fds_sj, "KEY", "key")
    monkeypatch.setattr(
        be_s0_ij_z5, "decode_str_tuple", lambda encoded, key: ("left", "right")
    )
    monkeypatch.setattr(gs_w3_df_u0, "nq_e6_go", lambda: calls.append("nq"))
    monkeypatch.setattr(gi_x9_hk_y8, "ux_l9_rx", lambda: calls.append("ux"))

    be_s0_ij_z5.jm_a6_sk()
    assert calls == [
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "nq",
        "ux",
    ]

    calls.clear()
    fake_geh.global_window = FakeWindow(False)
    be_s0_ij_z5.jm_a6_sk()
    assert calls == ["nq", "ux"]


def test_cf_44_ps_55_emits_and_calls_two_targets(monkeypatch):
    from src.py.com.yun.mao.kv_nx import cf_44_ps_55
    from src.py.com.yun.mao.util.need import signals

    calls = []

    class FakeSignal:
        def emit(self):
            calls.append("emit")

    class FakeSignals:
        cmd_socket_env_reject = FakeSignal()

    fake_wp = types.ModuleType("src.py.com.yun.mao.wp_jt.ru_i0_gj_x5")
    fake_wp.ac_r3_go = lambda: calls.append("ac")
    fake_rm = types.ModuleType("src.py.com.yun.mao.rm_qh.jm_a2_sv_j7")
    fake_rm.hj_y4_rx = lambda: calls.append("hj")

    monkeypatch.setattr(signals, "global_ui_signal", FakeSignals())
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.wp_jt.ru_i0_gj_x5", fake_wp
    )
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.rm_qh.jm_a2_sv_j7", fake_rm
    )

    cf_44_ps_55.pr_40_fan()

    assert calls == ["emit", "ac", "hj"]


def test_dv_r4_uw_l7_shows_abort_only_when_window_visible(monkeypatch):
    import src.py.com.yun.mao as mao_pkg
    from src.py.com.yun.mao.bz_uc import qt_h5_tv_k0
    from src.py.com.yun.mao.kv_nx import dv_r4_uw_l7
    from src.py.com.yun.mao.link import _fds_sj
    from src.py.com.yun.mao.rm_qh import su_j5_nq_e6

    calls = []

    class FakeWindow:
        def __init__(self, visible):
            self.visible = visible

        def isVisible(self):
            return self.visible

    fake_geh = types.ModuleType("src.py.com.yun.mao.GlobalExceptionHandler")
    fake_geh.global_window = FakeWindow(True)
    fake_error = types.ModuleType("src.py.com.yun.mao.ErrorDialog")
    fake_error.show_error_tip = lambda **kwargs: calls.append(("tip", kwargs))

    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.GlobalExceptionHandler", fake_geh
    )
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.ErrorDialog", fake_error
    )
    monkeypatch.setattr(mao_pkg, "GlobalExceptionHandler", fake_geh, raising=False)
    monkeypatch.setattr(mao_pkg, "ErrorDialog", fake_error, raising=False)
    monkeypatch.setattr(_fds_sj, "ABORT_PARTS_ENC", "enc")
    monkeypatch.setattr(_fds_sj, "KEY", "key")
    monkeypatch.setattr(
        dv_r4_uw_l7, "decode_str_tuple", lambda encoded, key: ("left", "right")
    )
    monkeypatch.setattr(su_j5_nq_e6, "ru_i0_go", lambda: calls.append("ru"))
    monkeypatch.setattr(qt_h5_tv_k0, "yb_p3_rx", lambda: calls.append("yb"))

    dv_r4_uw_l7.tw_k2_sk()
    assert calls == [
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "ru",
        "yb",
    ]

    calls.clear()
    fake_geh.global_window = FakeWindow(False)
    dv_r4_uw_l7.tw_k2_sk()
    assert calls == ["ru", "yb"]


def test_aq_m7_ln_c2_falls_back_to_hidden_command(monkeypatch):
    from src.py.com.yun.mao.kv_nx import aq_m7_ln_c2

    calls = []

    class FakeFunc:
        def __call__(self, *args, **kwargs):
            calls.append(("call", args, kwargs))
            return 0

        def __getattr__(self, name):
            return FakeFunc()

    class FakeDll:
        def __getattr__(self, name):
            return FakeFunc()

    monkeypatch.setattr(
        aq_m7_ln_c2.ctypes, "WinDLL", lambda name, **kwargs: FakeDll()
    )
    monkeypatch.setattr(aq_m7_ln_c2, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        aq_m7_ln_c2.subprocess,
        "Popen",
        lambda command, **kwargs: calls.append(("popen", command, kwargs)),
    )

    aq_m7_ln_c2.xz_o4_go()

    popen = next(item for item in calls if item[0] == "popen")
    assert popen[1] == [
        "sec:zp_uq_6n",
        "sec:bv_lt_8p",
        "sec:cw_rj_1a",
        "sec:dy_sk_5e",
        "sec:ez_um_2w",
    ]
    assert popen[2]["shell"] is False
    assert popen[2]["creationflags"] == aq_m7_ln_c2.subprocess.CREATE_NO_WINDOW


def test_hk_y8_gi_x9_seals_and_shows_abort_when_visible(monkeypatch):
    import src.py.com.yun.mao as mao_pkg
    from src.py.com.yun.mao.bz_uc import ya_p1_fh_w2
    from src.py.com.yun.mao.kv_nx import hk_y8_gi_x9
    from src.py.com.yun.mao.link import _fds_h_x, _fds_sj
    from src.py.com.yun.mao.rm_qh import eg_v7_vx_m2

    calls = []

    class FakeFds:
        def seal_abort(self):
            calls.append("seal")

    class FakeWindow:
        def __init__(self, visible):
            self.visible = visible

        def isVisible(self):
            return self.visible

    fake_geh = types.ModuleType("src.py.com.yun.mao.GlobalExceptionHandler")
    fake_geh.global_window = FakeWindow(True)
    fake_error = types.ModuleType("src.py.com.yun.mao.ErrorDialog")
    fake_error.show_error_tip = lambda **kwargs: calls.append(("tip", kwargs))

    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.GlobalExceptionHandler", fake_geh
    )
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.ErrorDialog", fake_error
    )
    monkeypatch.setattr(mao_pkg, "GlobalExceptionHandler", fake_geh, raising=False)
    monkeypatch.setattr(mao_pkg, "ErrorDialog", fake_error, raising=False)
    monkeypatch.setattr(_fds_h_x, "FdsHhx", FakeFds)
    monkeypatch.setattr(_fds_sj, "ABORT_PARTS_ENC", "enc")
    monkeypatch.setattr(_fds_sj, "KEY", "key")
    monkeypatch.setattr(
        hk_y8_gi_x9, "decode_str_tuple", lambda encoded, key: ("left", "right")
    )
    monkeypatch.setattr(eg_v7_vx_m2, "vy_m4_go", lambda: calls.append("vy"))
    monkeypatch.setattr(ya_p1_fh_w2, "aq_m7_rx", lambda: calls.append("aq"))

    hk_y8_gi_x9.bd_s8_sk()
    assert calls == [
        "seal",
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "vy",
        "aq",
    ]

    calls.clear()
    fake_geh.global_window = FakeWindow(False)
    hk_y8_gi_x9.bd_s8_sk()
    assert calls == ["seal", "vy", "aq"]


def test_pr_40_oq_84_delayed_dispatch(monkeypatch):
    import threading

    from src.py.com.yun.mao.kv_nx import pr_40_oq_84

    calls = []
    captured = {}

    class FakeTimer:
        def __init__(self, interval, callback):
            captured["interval"] = interval
            captured["callback"] = callback

        def start(self):
            calls.append("start")

    fake_wp = types.ModuleType("src.py.com.yun.mao.wp_jt.xa_o0_ad_r5")
    fake_wp.ux_l3_go = lambda: calls.append("ux")
    fake_rm = types.ModuleType("src.py.com.yun.mao.rm_qh.bx_n2_yb_p7")
    setattr(fake_rm, "{{SECRET_s71hx1q2}}", lambda: calls.append("be"))

    monkeypatch.setattr(threading, "Timer", FakeTimer)
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.wp_jt.xa_o0_ad_r5", fake_wp
    )
    monkeypatch.setitem(
        sys.modules, "src.py.com.yun.mao.rm_qh.bx_n2_yb_p7", fake_rm
    )

    pr_40_oq_84.ru_48_arm()
    assert captured["interval"] == 0.88
    assert calls == ["start"]

    captured["callback"]()
    assert calls == ["start", "ux", "be"]


@pytest.mark.parametrize(
    "module_name",
    ("dg_u6_qt_h5", "hk_y0_qs_h3", "hk_y8_ad_r9", "ln_c2_aq_m7", "pr_g6_ce_t5"),
)
def test_kv_nx_terminal_entries(monkeypatch, module_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.kv_nx.{module_name}")
    calls = []
    if hasattr(module, "gc"):
        monkeypatch.setattr(
            module.gc,
            "collect",
            lambda generation: calls.append(("gc", generation)),
        )
    if hasattr(module, "sec"):
        monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module, "_exit", lambda code: calls.append(("exit", code))
    )

    _entry(module)()

    assert calls[-1] == ("exit", 1)


@pytest.mark.parametrize(
    "module_name",
    (
        "fh_w2_il_z7",
        "nq_e0_kn_b3",
        "ps_g8_ux_l9",
        "xz_o4_eu_s1",
        "zc_q2_or_f7",
        "xa_o6_wz_n5",
    ),
)
def test_kv_nx_windll_entries(monkeypatch, module_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.kv_nx.{module_name}")
    calls = []

    class FakeExport:
        def __call__(self, *args):
            calls.append(("export", args))
            return 0

    class FakeDll:
        def __getattr__(self, name):
            return FakeExport()

    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(module, "WinDLL", lambda name, **kwargs: FakeDll())
    monkeypatch.setattr(
        module, "_exit", lambda code: calls.append(("exit", code))
    )

    _entry(module)()

    if module_name in {"xa_o6_wz_n5", "zc_q2_or_f7"}:
        assert calls == [("exit", 1)]
    else:
        assert calls == [("export", (-1, 1)), ("exit", 1)]


@pytest.mark.parametrize("module_name", ("mo_d9_vy_m8", "ya_p1_dv_r4"))
def test_kv_nx_popen_entries(monkeypatch, module_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.kv_nx.{module_name}")
    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module.subprocess,
        "Popen",
        lambda command, **kwargs: calls.append((command, kwargs)),
    )

    _entry(module)()

    assert calls[0][0] == [
        "sec:zp_uq_6n",
        "sec:bv_lt_8p",
        "sec:cw_rj_1a",
        "sec:dy_sk_5e",
        "sec:ez_um_2w",
    ]
    assert calls[0][1]["shell"] is False


def test_kv_nx_signal_fanouts(monkeypatch):
    from src.py.com.yun.mao.kv_nx import hk_29_lo_78, lo_10_nq_63
    from src.py.com.yun.mao.rm_qh import ft_v6_ad_r5, lo_c8_kn_b9
    from src.py.com.yun.mao.util.need import signals
    from src.py.com.yun.mao.wp_jt import jm_a2_ik_z1, zc_q8_cw_p9

    calls = []

    class FakeSignal:
        def emit(self):
            calls.append("emit")

    class FakeSignals:
        cmd_marshal_pipeline_halt = FakeSignal()
        report_probe_mid_fault = FakeSignal()

    monkeypatch.setattr(signals, "global_ui_signal", FakeSignals())
    monkeypatch.setattr(ft_v6_ad_r5, "jl_a0_rx", lambda: calls.append("jl"))
    monkeypatch.setattr(zc_q8_cw_p9, "cw_p9_go", lambda: calls.append("cw"))
    monkeypatch.setattr(lo_c8_kn_b9, "fi_w8_rx", lambda: calls.append("fi"))
    jm_name = _entry(jm_a2_ik_z1).__name__
    monkeypatch.setattr(jm_a2_ik_z1, jm_name, lambda: calls.append("jm"))

    hk_29_lo_78.kn_46_fan()
    assert calls == ["emit", "cw", "jl"]

    calls.clear()
    lo_10_nq_63.cf_23_fan()
    assert calls == ["emit", "fi", "jm"]


def test_kv_nx_timer_entries(monkeypatch):
    import threading

    from src.py.com.yun.mao.kv_nx import gi_22_uw_87, ps_61_xa_97
    from src.py.com.yun.mao.rm_qh import fi_w8_qt_h9, hj_y4_ik_z1
    from src.py.com.yun.mao.wp_jt import hj_y4_eg_v7, ps_g2_cf_t1

    calls = []
    captured = {}

    class FakeTimer:
        def __init__(self, interval, callback):
            captured["interval"] = interval
            captured["callback"] = callback

        def start(self):
            calls.append("start")

    monkeypatch.setattr(threading, "Timer", FakeTimer)
    monkeypatch.setattr(hj_y4_ik_z1, "vx_m2_rx", lambda: calls.append("vx"))
    oq_name = _entry(hj_y4_eg_v7).__name__
    monkeypatch.setattr(hj_y4_eg_v7, oq_name, lambda: calls.append("oq"))
    monkeypatch.setattr(fi_w8_qt_h9, "zc_q8_rx", lambda: calls.append("zc"))
    monkeypatch.setattr(ps_g2_cf_t1, "sv_j7_go", lambda: calls.append("sv"))

    gi_22_uw_87.xa_96_arm()
    assert captured["interval"] == 0.85
    captured["callback"]()
    assert calls == ["start", "oq", "vx"]

    calls.clear()
    ps_61_xa_97.be_67_arm()
    assert captured["interval"] == 1.05
    captured["callback"]()
    assert calls == ["start", "sv", "zc"]
