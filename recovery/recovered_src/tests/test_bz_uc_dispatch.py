from __future__ import annotations

import pytest


def test_aq_22_rt_78_emits_and_fans_out(monkeypatch):
    import importlib

    from src.py.com.yun.mao.bz_uc import aq_22_rt_78
    from src.py.com.yun.mao.util.need import signals

    calls = []

    class FakeSignal:
        def emit(self):
            calls.append("emit")

    class FakeSignals:
        notify_crypto_ctx_broken = FakeSignal()

    class FakeModule:
        def __init__(self, name):
            self.name = name

        def qt_h5_go(self):
            calls.append("qt_h5_go")

        def xa_o6_rx(self):
            calls.append("xa_o6_rx")

    def fake_import(name):
        calls.append(name)
        return FakeModule(name)

    monkeypatch.setattr(signals, "global_ui_signal", FakeSignals())
    monkeypatch.setattr(importlib, "import_module", fake_import)

    aq_22_rt_78.yb_25_fan()

    assert calls == [
        "emit",
        "src.py.com.yun.mao.bz_uc.xa_o6_yb_p3",
        "qt_h5_go",
        "src.py.com.yun.mao.kv_nx.be_s0_yb_p3",
        "xa_o6_rx",
    ]


def test_ya_p1_xz_o4_seals_and_aborts(monkeypatch):
    import sys
    import types

    import src.py.com.yun.mao as mao_pkg
    from src.py.com.yun.mao.bz_uc import ya_p1_xz_o4
    from src.py.com.yun.mao.link import _fds_h_x, _fds_jm, _fds_sj
    from src.py.com.yun.mao.rm_qh import zc_q8_wy_n9
    from src.py.com.yun.mao.wp_jt import vx_m2_wz_n1

    calls = []

    class FakeFds:
        def seal_abort(self):
            calls.append("seal")

    class FakeWindow:
        def isVisible(self):
            return True

    fake_geh = types.ModuleType("src.py.com.yun.mao.GlobalExceptionHandler")
    fake_geh.global_window = FakeWindow()
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
        _fds_jm,
        "decode_str_tuple",
        lambda encoded, key: ("part-a", "part-b"),
    )
    monkeypatch.setattr(
        zc_q8_wy_n9, "rt_i8_rx", lambda: calls.append("rt")
    )
    monkeypatch.setattr(
        vx_m2_wz_n1, "km_b7_go", lambda: calls.append("km")
    )

    ya_p1_xz_o4.aq_m7_sk()

    assert calls == [
        "seal",
        ("tip", {"error_msg": "part-a\n\npart-b", "timeout": 1000}),
        "km",
        "rt",
    ]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("bd_s8_mo_d9", "ad_r9_go"),
        ("be_s0_ij_z5", "qs_h3_go"),
        ("zc_q2_eu_s1", "il_z7_go"),
    ),
)
def test_privilege_then_hidden_command(monkeypatch, module_name, function_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.bz_uc.{module_name}")

    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module._ops,
        "enable_privileges",
        lambda advapi, kernel, privileges: calls.append(
            ("privilege", advapi, kernel, tuple(privileges))
        ),
    )
    monkeypatch.setattr(
        module._ops,
        "hidden_popen",
        lambda command: calls.append(("popen", tuple(command))),
    )

    getattr(module, function_name)()

    assert calls == [
        (
            "privilege",
            "sec:gh_wo_4r",
            "sec:hi_xp_7m",
            ("sec:fg_vn_9c",),
        ),
        (
            "popen",
            (
                "sec:zp_uq_6n",
                "sec:bv_lt_8p",
                "sec:cw_rj_1a",
                "sec:dy_sk_5e",
                "sec:ez_um_2w",
            ),
        ),
    ]


def test_km_74_qs_60_delayed_dispatch_order(monkeypatch):
    from src.py.com.yun.mao.bz_uc import km_74_qs_60

    calls = []
    captured = {}

    class FakeTimer:
        def __init__(self, interval, callback):
            captured["interval"] = interval
            captured["callback"] = callback

        def start(self):
            calls.append("start")

    class FakeModule:
        def __init__(self, name):
            self.name = name

        def lo_c4_rx(self):
            calls.append("lo_c4_rx")

        def eh_v3_go(self):
            calls.append("eh_v3_go")

    def fake_import(name, package=None):
        calls.append(name)
        return FakeModule(name)

    monkeypatch.setattr(km_74_qs_60.threading, "Timer", FakeTimer)
    monkeypatch.setattr(km_74_qs_60.importlib, "import_module", fake_import)

    km_74_qs_60.km_23_arm()
    assert captured["interval"] == 1.0
    assert calls == ["start"]

    captured["callback"]()
    assert calls == [
        "start",
        "src.py.com.yun.mao.kv_nx.zc_q2_or_f7",
        "lo_c4_rx",
        "src.py.com.yun.mao.bz_uc.nq_e0_wz_n5",
        "eh_v3_go",
    ]


def test_pr_43_qs_39_delayed_dispatch_order(monkeypatch):
    from src.py.com.yun.mao.bz_uc import pr_43_qs_39

    calls = []
    captured = {}

    class FakeTimer:
        def __init__(self, interval, callback):
            captured["interval"] = interval
            captured["callback"] = callback

        def start(self):
            calls.append("start")

    class FakeModule:
        def nq_e0_rx(self):
            calls.append("{{SECRET_5c0o2an0}}")

        def gi_x9_go(self):
            calls.append("{{SECRET_d0l0v9h1}}")

    def fake_import(name, package=None):
        calls.append(name)
        return FakeModule()

    monkeypatch.setattr(pr_43_qs_39, "Timer", FakeTimer)
    monkeypatch.setattr(pr_43_qs_39.importlib, "import_module", fake_import)

    pr_43_qs_39.xa_56_arm()
    assert captured["interval"] == 1.18
    assert calls == ["start"]

    captured["callback"]()
    assert calls == [
        "start",
        "src.py.com.yun.mao.kv_nx.xa_o6_wz_n5",
        "{{SECRET_5c0o2an0}}",
        "src.py.com.yun.mao.bz_uc.vy_m8_ux_l9",
        "{{SECRET_d0l0v9h1}}",
    ]


def test_fi_49_qs_87_emits_and_calls_both_handlers(monkeypatch):
    from src.py.com.yun.mao.bz_uc import fi_49_qs_87, hk_y0_ce_t5
    from src.py.com.yun.mao.kv_nx import fh_w2_il_z7
    from src.py.com.yun.mao.util.need import signals

    calls = []

    class FakeSignal:
        def emit(self):
            calls.append("emit")

    class FakeSignals:
        report_probe_mid_fault = FakeSignal()

    monkeypatch.setattr(signals, "global_ui_signal", FakeSignals())
    monkeypatch.setattr(hk_y0_ce_t5, "kn_b3_go", lambda: calls.append("kn"))
    monkeypatch.setattr(fh_w2_il_z7, "ru_i4_rx", lambda: calls.append("ru"))

    fi_49_qs_87.aq_87_fan()

    assert calls == ["emit", "kn", "ru"]


def test_nq_23_vy_24_emits_and_calls_both_handlers(monkeypatch):
    from src.py.com.yun.mao.bz_uc import nq_23_vy_24, ps_g8_ad_r9
    from src.py.com.yun.mao.kv_nx import dg_u6_qt_h5
    from src.py.com.yun.mao.util.need import signals

    calls = []

    class FakeSignal:
        def emit(self):
            calls.append("emit")

    class FakeSignals:
        notify_link_integrity_fail = FakeSignal()

    monkeypatch.setattr(signals, "global_ui_signal", FakeSignals())
    monkeypatch.setattr(dg_u6_qt_h5, "tv_k0_rx", lambda: calls.append("tv"))
    monkeypatch.setattr(ps_g8_ad_r9, "mo_d9_go", lambda: calls.append("mo"))

    nq_23_vy_24.cf_79_fan()

    assert calls == ["emit", "tv", "mo"]


def test_terminal_entries_call_gc_then_exit(monkeypatch):
    from src.py.com.yun.mao.bz_uc import gi_x9_hk_y8, ya_p1_fh_w2

    calls = []
    monkeypatch.setattr(
        gi_x9_hk_y8.gc, "collect", lambda generation: calls.append(("gc", generation))
    )
    monkeypatch.setattr(
        gi_x9_hk_y8.os, "_exit", lambda code: calls.append(("exit", code))
    )

    gi_x9_hk_y8.ux_l9_rx()
    ya_p1_fh_w2.aq_m7_rx()

    assert calls == [
        ("gc", 2),
        ("exit", 1),
        ("gc", 2),
        ("exit", 1),
    ]


def test_uw_l7_ln_c2_abort_message_and_handlers(monkeypatch):
    import sys
    import types

    import src.py.com.yun.mao as mao_pkg
    from src.py.com.yun.mao.bz_uc import uw_l7_ln_c2
    from src.py.com.yun.mao.link import _fds_jm, _fds_sj
    from src.py.com.yun.mao.rm_qh import ps_g2_km_b7
    from src.py.com.yun.mao.wp_jt import jl_a0_mp_d5

    calls = []

    class FakeWindow:
        def isVisible(self):
            return True

    fake_geh = types.ModuleType("src.py.com.yun.mao.GlobalExceptionHandler")
    fake_geh.global_window = FakeWindow()
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
        _fds_jm, "decode_str_tuple", lambda encoded, key: ("left", "right")
    )
    monkeypatch.setattr(ps_g2_km_b7, "np_e4_rx", lambda: calls.append("np"))
    monkeypatch.setattr(jl_a0_mp_d5, "gs_w3_go", lambda: calls.append("gs"))

    uw_l7_ln_c2.sv_j1_sk()

    assert calls == [
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "gs",
        "np",
    ]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("hk_y0_ce_t5", "kn_b3_go"),
        ("jm_a6_kn_b3", "ce_t5_go"),
        ("dv_r4_uw_l7", "sv_j1_go"),
        ("tw_k2_mp_d1", "or_f7_go"),
    ),
)
def test_hidden_command_entries_dispatch_five_parts(
    monkeypatch, module_name, function_name
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.bz_uc.{module_name}")
    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module._ops,
        "hidden_popen",
        lambda command: calls.append(tuple(command)),
    )

    getattr(module, function_name)()

    assert calls == [
        (
            "sec:zp_uq_6n",
            "sec:bv_lt_8p",
            "sec:cw_rj_1a",
            "sec:dy_sk_5e",
            "sec:ez_um_2w",
        )
    ]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("nq_e0_wz_n5", "eh_v3_go"),
        ("vy_m8_ux_l9", "gi_x9_go"),
    ),
)
def test_dynamic_line_hidden_command(monkeypatch, module_name, function_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.bz_uc.{module_name}")
    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module._ops,
        "hidden_popen",
        lambda command: calls.append(tuple(command)),
    )

    getattr(module, function_name)()

    assert calls == [
        (
            "sec:lm_bt_1d",
            "sec:mn_cu_8f",
            "sec:zp_uq_6nsec:hm_xd_3k",
        )
    ]


def test_pr_g6_eh_v3_privilege_then_dynamic_line(monkeypatch):
    import importlib

    module = importlib.import_module("src.py.com.yun.mao.bz_uc.pr_g6_eh_v3")
    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module._ops,
        "enable_privileges",
        lambda advapi, kernel, privileges: calls.append(
            ("privilege", advapi, kernel, tuple(privileges))
        ),
    )
    monkeypatch.setattr(
        module._ops,
        "hidden_popen",
        lambda command: calls.append(("popen", tuple(command))),
    )

    getattr(module, "wz_n5_go")()

    assert calls == [
        (
            "privilege",
            "sec:gh_wo_4r",
            "sec:hi_xp_7m",
            ("sec:fg_vn_9c",),
        ),
        (
            "popen",
            (
                "sec:lm_bt_1d",
                "sec:mn_cu_8f",
                "sec:zp_uq_6nsec:hm_xd_3k",
            ),
        ),
    ]


def test_ps_42_sv_93_delayed_dispatch(monkeypatch):
    import importlib

    module = importlib.import_module("src.py.com.yun.mao.bz_uc.ps_42_sv_93")
    calls = []
    captured = {}

    class FakeTimer:
        def __init__(self, interval, callback):
            captured["interval"] = interval
            captured["callback"] = callback

        def start(self):
            calls.append("start")

    class FakeModule:
        def pr_g6_rx(self):
            calls.append("pr")

        def ij_z5_go(self):
            calls.append("ij")

    def fake_import(name, package=None):
        calls.append((name, package))
        return FakeModule()

    monkeypatch.setattr(module.threading, "Timer", FakeTimer)
    monkeypatch.setattr(module.importlib, "import_module", fake_import)

    module.yb_39_arm()
    assert captured["interval"] == 0.95
    assert calls == ["start"]

    captured["callback"]()
    assert calls == [
        "start",
        ("..kv_nx.tv_k0_eh_v3", "src.py.com.yun.mao.bz_uc"),
        "pr",
        (".dg_u6_qs_h3", "src.py.com.yun.mao.bz_uc"),
        "ij",
    ]


def test_ps_g8_ad_r9_system_command_and_swallow(monkeypatch):
    import importlib

    module = importlib.import_module("src.py.com.yun.mao.bz_uc.ps_g8_ad_r9")
    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module._ops, "system_command", lambda command: calls.append(command)
    )

    getattr(module, "mo_d9_go")()
    assert calls == ["sec:zp_uq_6nsec:hm_xd_3k"]

    def boom(command):
        raise RuntimeError("blocked")

    monkeypatch.setattr(module._ops, "system_command", boom)
    getattr(module, "mo_d9_go")()


def test_qt_h5_tv_k0_windll_fallback(monkeypatch):
    import importlib

    module = importlib.import_module("src.py.com.yun.mao.bz_uc.qt_h5_tv_k0")
    calls = []

    class FakeDll:
        def __getattr__(self, name):
            def method(arg):
                calls.append((name, arg))
                return "result"

            return method

    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module.ctypes, "WinDLL", lambda name, **kwargs: FakeDll()
    )

    assert module.yb_p3_rx() == "result"
    assert calls == [("sec:sx_ql_7n", 1)]
