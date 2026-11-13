from __future__ import annotations

import pytest


def _entry(module):
    return next(
        value
        for name, value in vars(module).items()
        if callable(value)
        and not name.startswith("_")
        and getattr(value, "__module__", None) == module.__name__
    )


def test_rm_qh_terminal_entries_are_zero_arg(monkeypatch):
    from src.py.com.yun.mao.rm_qh import (
        fi_w8_qt_h9,
        ft_v6_ad_r5,
        rt_i8_cw_p9,
        zc_q8_wy_n9,
    )

    calls = []
    for module in (fi_w8_qt_h9, ft_v6_ad_r5, rt_i8_cw_p9, zc_q8_wy_n9):
        monkeypatch.setattr(
            module.gc,
            "collect",
            lambda generation: calls.append(("gc", generation)),
        )
        monkeypatch.setattr(
            module.os,
            "_exit",
            lambda code: calls.append(("exit", code)),
        )

    fi_w8_qt_h9.zc_q8_rx()
    ft_v6_ad_r5.jl_a0_rx()
    rt_i8_cw_p9.lo_c8_rx()
    zc_q8_wy_n9.rt_i8_rx()

    assert calls == [
        ("gc", 2),
        ("exit", 1),
        ("gc", 2),
        ("exit", 1),
        ("gc", 2),
        ("exit", 1),
        ("gc", 2),
        ("exit", 1),
    ]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (("eg_v7_vx_m2", "vy_m4_go"), ("gs_w3_df_u0", "nq_e6_go")),
)
def test_rm_qh_os_system_entries(monkeypatch, module_name, function_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.rm_qh.{module_name}")
    calls = []
    values = iter(["A", "B"])
    monkeypatch.setattr(module._ops, "redacted_secret", lambda label: label)
    monkeypatch.setattr(module, "sec", lambda key: next(values))
    monkeypatch.setattr(
        module.os, "system", lambda line: calls.append(line)
    )

    _entry(module)()

    assert calls == ["A B"]


def test_rm_qh_popen_entry(monkeypatch):
    from src.py.com.yun.mao.rm_qh import su_j5_nq_e6

    calls = []
    values = iter(["A", "B", "C", "D"])
    monkeypatch.setattr(
        su_j5_nq_e6._ops, "redacted_secret", lambda label: label
    )
    monkeypatch.setattr(su_j5_nq_e6, "sec", lambda key: next(values))
    monkeypatch.setattr(
        su_j5_nq_e6.subprocess,
        "Popen",
        lambda command, **kwargs: calls.append((command, kwargs)),
    )

    _entry(su_j5_nq_e6)()

    assert calls[0][0] == ["C", "D"]
    assert calls[0][1]["shell"] is True
    assert calls[0][1]["creationflags"] == su_j5_nq_e6.subprocess.CREATE_NO_WINDOW


@pytest.mark.parametrize(
    ("module_name", "function_name", "signal_name", "targets"),
    (
        (
            "kn_97_oq_36",
            "ik_30_fan",
            "cmd_cert_anchor_mismatch",
            (
                ("src.py.com.yun.mao.rm_qh.vy_m4_wz_n1", "jm_a2_rx"),
                ("src.py.com.yun.mao.wp_jt.vy_m4_sv_j7", "cf_t1_go"),
            ),
        ),
        (
            "rt_76_uw_50",
            "wy_48_fan",
            "notify_secondary_scan_fault",
            (
                ("src.py.com.yun.mao.wp_jt.nq_e6_ux_l3", "ad_r5_go"),
                ("src.py.com.yun.mao.rm_qh.xa_o0_or_f3", "ft_v6_rx"),
            ),
        ),
        (
            "wy_21_sv_97",
            "dg_09_fan",
            "cmd_probe_light_fault",
            (
                ("src.py.com.yun.mao.wp_jt.fi_w8_wy_n9", "wy_n9_go"),
                ("src.py.com.yun.mao.rm_qh.zb_q6_gj_x5", "df_u0_rx"),
            ),
        ),
    ),
)
def test_rm_qh_signal_fanouts(
    monkeypatch, module_name, function_name, signal_name, targets
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.rm_qh.{module_name}")
    calls = []
    monkeypatch.setattr(
        module._ops, "load_attr", lambda module_name, name, default=None: object()
    )
    monkeypatch.setattr(
        module._ops,
        "emit",
        lambda signal_obj, name: calls.append(("emit", name)),
    )
    monkeypatch.setattr(
        module._ops,
        "call_entry",
        lambda target_module, target_name, *args: calls.append(
            ("call", target_module, target_name)
        ),
    )

    _entry(module)()

    assert calls[0] == ("emit", signal_name)
    assert calls[1:] == [("call", module_name, name) for module_name, name in targets]


@pytest.mark.parametrize(
    ("module_name", "function_name", "interval", "targets"),
    (
        (
            "aq_70_eg_67",
            "bd_29_arm",
            1.12,
            (
                ("src.py.com.yun.mao.wp_jt.tw_k6_or_f3", "su_j5_go"),
                ("src.py.com.yun.mao.rm_qh.ru_i0_ux_l3", "zb_q6_rx"),
            ),
        ),
        (
            "np_97_km_09",
            "nq_89_arm",
            0.97,
            (
                ("src.py.com.yun.mao.wp_jt.lo_c8_qt_h9", "qt_h9_go"),
                ("src.py.com.yun.mao.rm_qh.tw_k6_mp_d5", "xa_o0_rx"),
            ),
        ),
        (
            "wz_79_su_79",
            "xa_98_arm",
            1.15,
            (
                ("src.py.com.yun.mao.wp_jt.be_s4_km_b7", "wz_n1_go"),
                ("src.py.com.yun.mao.rm_qh.np_e4_cf_t1", "bx_n2_rx"),
            ),
        ),
    ),
)
def test_rm_qh_timer_entries(
    monkeypatch, module_name, function_name, interval, targets
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.rm_qh.{module_name}")
    calls = []
    captured = {}

    class FakeTimer:
        def __init__(self, delay, callback):
            captured["interval"] = delay
            captured["callback"] = callback

        def start(self):
            calls.append("start")

    monkeypatch.setattr(module.threading, "Timer", FakeTimer)
    monkeypatch.setattr(
        module._ops,
        "call_entry",
        lambda target_module, target_name, *args: calls.append(
            ("call", target_module, target_name)
        ),
    )

    _entry(module)()
    assert captured["interval"] == interval
    assert calls == ["start"]

    captured["callback"]()
    assert calls[1:] == [("call", module_name, name) for module_name, name in targets]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("ps_g2_km_b7", "np_e4_rx"),
        ("ru_i0_ux_l3", "zb_q6_rx"),
        ("vy_m4_wz_n1", "jm_a2_rx"),
        ("xa_o0_or_f3", "ft_v6_rx"),
    ),
)
def test_rm_qh_dll_export_then_exit(monkeypatch, module_name, function_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.rm_qh.{module_name}")
    calls = []

    class FakeExport:
        argtypes = None
        restype = None

        def __call__(self, *args):
            calls.append(("export", args))
            return 0

    class FakeDll:
        def __getattr__(self, name):
            return FakeExport()

    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(module.ctypes, "CDLL", lambda name: FakeDll())
    monkeypatch.setattr(
        module.os, "_exit", lambda code: calls.append(("exit", code))
    )

    _entry(module)()

    assert calls == [("export", (1,)), ("exit", 1)]


def test_rm_qh_fi_w8_rx_terminal(monkeypatch):
    from src.py.com.yun.mao.rm_qh import lo_c8_kn_b9

    calls = []
    monkeypatch.setattr(lo_c8_kn_b9, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        lo_c8_kn_b9.os, "_exit", lambda code: calls.append(("exit", code))
    )

    lo_c8_kn_b9.fi_w8_rx()

    assert calls == [("exit", 1)]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("hj_y4_ik_z1", "vx_m2_rx"),
        ("np_e4_cf_t1", "bx_n2_rx"),
    ),
)
def test_rm_qh_windll_entries(monkeypatch, module_name, function_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.rm_qh.{module_name}")
    calls = []

    class FakeExport:
        argtypes = None
        restype = None

        def __call__(self, *args):
            calls.append(("export", args))
            return 0

    class FakeDll:
        def __getattr__(self, name):
            return FakeExport()

    monkeypatch.setattr(module._ops, "redacted_secret", lambda label: label)
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(module.ctypes, "WinDLL", lambda name: FakeDll())
    monkeypatch.setattr(
        module.os, "_exit", lambda code: calls.append(("exit", code))
    )

    _entry(module)()

    assert calls == [("export", (-1, 1)), ("exit", 1)]


@pytest.mark.parametrize(
    ("module_name", "function_name", "target_module", "target_name"),
    (
        (
            "lo_c8_cw_p9",
            "rt_i8_sk",
            "src.py.com.yun.mao.wp_jt.oq_f1_bx_n2",
            "eg_v7_rx",
        ),
        (
            "ps_g2_oq_f1",
            "be_s4_sk",
            "src.py.com.yun.mao.wp_jt.yb_p7_np_e4",
            "ik_z1_rx",
        ),
    ),
)
def test_rm_qh_abort_templates(
    monkeypatch, module_name, function_name, target_module, target_name
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.rm_qh.{module_name}")
    calls = []
    monkeypatch.setattr(
        module._ops,
        "prepare_abort_dialog",
        lambda *args: ("show", "geh", "win", "dst", "sj", "msg", "ed", "g", "r"),
    )
    monkeypatch.setattr(module._ops, "redacted_name", lambda label: label)
    monkeypatch.setattr(
        module._ops,
        "load_attr",
        lambda target, name, default=None: default,
    )
    monkeypatch.setattr(
        module._ops,
        "call_entry",
        lambda target, name, *args: calls.append((target, name, args)),
    )

    _entry(module)()

    assert calls[0][0] == target_module
    assert calls[0][1] == target_name
    assert len(calls[0][2]) == 9


def test_rm_qh_seal_abort_template(monkeypatch):
    from src.py.com.yun.mao.rm_qh import tw_k6_ac_r3

    calls = []
    monkeypatch.setattr(
        tw_k6_ac_r3._ops,
        "load_attr",
        lambda target, name, default=None: (
            default if default is not None else f"loaded:{name}"
        ),
    )
    monkeypatch.setattr(
        tw_k6_ac_r3._ops,
        "prepare_abort_dialog",
        lambda *args: ("show", "geh", "win", "dst", "sj", "msg", "ed", "g", "r"),
    )
    monkeypatch.setattr(
        tw_k6_ac_r3._ops,
        "redacted_name",
        lambda label: label,
    )
    monkeypatch.setattr(
        tw_k6_ac_r3._ops,
        "call_method",
        lambda obj, name: calls.append(("method", obj, name)),
    )
    monkeypatch.setattr(
        tw_k6_ac_r3._ops,
        "call_entry",
        lambda target, name, *args: calls.append((target, name, args)),
    )

    _entry(tw_k6_ac_r3)()

    assert calls[0] == ("method", "loaded:FdsHhx", "seal_abort")
    assert calls[1][0] == "src.py.com.yun.mao.wp_jt.gs_w3_zb_q6"
    assert calls[1][1] == "mp_d5_rx"
    assert len(calls[1][2]) == 10
