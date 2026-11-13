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


class _Window:
    def isVisible(self):
        return True


class _GlobalExceptionHandler:
    global_window = _Window()


def _install(monkeypatch, calls, mapping):
    from src.py.com.yun.mao.wp_jt import _ops

    def fake_load_attr(module, name, default=None):
        return mapping.get((module, name), default)

    def fake_show(**kwargs):
        calls.append(("tip", kwargs))

    monkeypatch.setattr(_ops, "load_attr", fake_load_attr)
    monkeypatch.setattr(_ops, "decode_abort_parts", lambda: ("left", "right"))
    monkeypatch.setattr(
        _ops,
        "call_method",
        lambda obj, name: calls.append(("method", obj, name)),
    )
    mapping.setdefault(
        ("src.py.com.yun.mao", "GlobalExceptionHandler"),
        _GlobalExceptionHandler,
    )
    mapping.setdefault(
        ("src.py.com.yun.mao.link", "_fds_sj"), object()
    )
    mapping.setdefault(
        ("src.py.com.yun.mao.ErrorDialog", "show_error_tip"), fake_show
    )


def test_gj_x5_ft_v6_abort_then_targets(monkeypatch):
    from src.py.com.yun.mao.wp_jt import gj_x5_ft_v6

    calls = []
    mapping = {
        (
            "src.py.com.yun.mao.bz_uc.dv_r4_uw_l7",
            "sv_j1_go",
        ): lambda: calls.append("sv"),
        (
            "src.py.com.yun.mao.kv_nx.xz_o4_eu_s1",
            "zc_q2_rx",
        ): lambda: calls.append("zc"),
    }
    _install(monkeypatch, calls, mapping)

    gj_x5_ft_v6.ac_r3_sk()

    assert calls == [
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "sv",
        "zc",
    ]


def test_kn_b9_rt_i8_abort_then_targets(monkeypatch):
    from src.py.com.yun.mao.wp_jt import kn_b9_rt_i8

    calls = []
    mapping = {
        (
            "src.py.com.yun.mao.bz_uc.pr_g6_eh_v3",
            "wz_n5_go",
        ): lambda: calls.append("g"),
        (
            "src.py.com.yun.mao.kv_nx.hk_y0_qs_h3",
            "dg_u6_rx",
        ): lambda: calls.append("r"),
    }
    _install(monkeypatch, calls, mapping)

    _entry(kn_b9_rt_i8)()

    assert calls == [
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "g",
        "r",
    ]


def test_or_f3_df_u0_seals_then_abort_then_targets(monkeypatch):
    from src.py.com.yun.mao.wp_jt import or_f3_df_u0

    calls = []

    class FakeFds:
        pass

    mapping = {
        (
            "src.py.com.yun.mao.link._fds_h_x",
            "FdsHhx",
        ): FakeFds,
        (
            "src.py.com.yun.mao.bz_uc.bd_s8_mo_d9",
            "ad_r9_go",
        ): lambda: calls.append("ad"),
        (
            "src.py.com.yun.mao.kv_nx.pr_g6_ce_t5",
            "hk_y0_rx",
        ): lambda: calls.append("mtd"),
    }
    _install(monkeypatch, calls, mapping)

    _entry(or_f3_df_u0)()

    assert calls[0][0] == "method"
    assert calls[0][2] == "seal_abort"
    assert isinstance(calls[0][1], FakeFds)
    assert calls[1:] == [
        ("tip", {"error_msg": "left\n\nright", "timeout": 1000}),
        "ad",
        "mtd",
    ]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (("be_s4_km_b7", "wz_n1_go"), ("hj_y4_eg_v7", "oq_f1_go")),
)
def test_wp_jt_five_part_hidden_command(
    monkeypatch, module_name, function_name
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.wp_jt.{module_name}")
    calls = []
    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module._ops,
        "hidden_popen",
        lambda command: calls.append(tuple(command)),
    )

    _entry(module)()

    assert calls == [
        (
            "sec:zp_uq_6n",
            "sec:bv_lt_8p",
            "sec:cw_rj_1a",
            "sec:dy_sk_5e",
            "sec:ez_um_2w",
        )
    ]


def test_wp_jt_privilege_then_five_part_command(monkeypatch):
    from src.py.com.yun.mao.wp_jt import nq_e6_ux_l3

    calls = []
    monkeypatch.setattr(nq_e6_ux_l3, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        nq_e6_ux_l3._ops,
        "enable_privileges",
        lambda advapi, kernel, privileges: calls.append(
            ("privilege", advapi, kernel, tuple(privileges))
        ),
    )
    monkeypatch.setattr(
        nq_e6_ux_l3._ops,
        "hidden_popen",
        lambda command: calls.append(("popen", tuple(command))),
    )

    nq_e6_ux_l3.ad_r5_go()

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


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("jm_a2_ik_z1", "yb_p7_go"),
        ("vy_m4_sv_j7", "cf_t1_go"),
    ),
)
def test_wp_jt_privilege_then_dynamic_line_command(
    monkeypatch, module_name, function_name
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.wp_jt.{module_name}")
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

    _entry(module)()

    assert calls[-1] == (
        "popen",
        (
            "sec:lm_bt_1d",
            "sec:mn_cu_8f",
            "sec:zp_uq_6nsec:hm_xd_3k",
        ),
    )


def test_wp_jt_privilege_then_os_system(monkeypatch):
    from src.py.com.yun.mao.wp_jt import jl_a0_mp_d5

    calls = []
    monkeypatch.setattr(jl_a0_mp_d5, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        jl_a0_mp_d5._ops,
        "enable_privileges",
        lambda advapi, kernel, privileges: calls.append(
            ("privilege", advapi, kernel, tuple(privileges))
        ),
    )
    monkeypatch.setattr(
        jl_a0_mp_d5.os,
        "system",
        lambda line: calls.append(("system", line)),
    )

    jl_a0_mp_d5.gs_w3_go()

    assert calls[-1] == (
        "system",
        "sec:zp_uq_6nsec:hm_xd_3k",
    )


@pytest.mark.parametrize(
    ("module_name", "function_name", "loader", "args"),
    (
        ("gs_w3_zb_q6", "mp_d5_rx", "WinDLL", (-1, 1)),
        ("oq_f1_bx_n2", "eg_v7_rx", "CDLL", (1,)),
    ),
)
def test_wp_jt_dll_export_then_exit(
    monkeypatch, module_name, function_name, loader, args
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.wp_jt.{module_name}")
    calls = []

    class FakeExport:
        def __call__(self, *call_args):
            calls.append(("export", call_args))
            return 0

    class FakeDll:
        def __getattr__(self, name):
            return FakeExport()

    monkeypatch.setattr(module, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        module.ctypes, loader, lambda name, **kwargs: FakeDll()
    )
    monkeypatch.setattr(
        module.os, "_exit", lambda code: calls.append(("exit", code))
    )

    _entry(module)()

    assert calls == [("export", args), ("exit", 1)]


@pytest.mark.parametrize(
    ("module_name", "function_name"),
    (
        ("bx_n2_oq_f1", "eg_v7_rx"),
        ("ps_g2_cf_t1", "{{SECRET_77vrbh2n}}"),
        ("vx_m2_wz_n1", "km_b7_go"),
        ("zc_q8_cw_p9", "{{SECRET_2lwg4qku}}"),
    ),
)
def test_wp_jt_os_system_entries(monkeypatch, module_name, function_name):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.wp_jt.{module_name}")
    calls = []
    values = iter(["A", "B"])
    monkeypatch.setattr(module, "sec", lambda key: next(values))
    monkeypatch.setattr(module.os, "system", lambda line: calls.append(line))

    _entry(module)()

    assert calls == ["AB"]


def test_wp_jt_privilege_then_dynamic_line_tw_k6(monkeypatch):
    from src.py.com.yun.mao.wp_jt import tw_k6_or_f3

    calls = []
    monkeypatch.setattr(tw_k6_or_f3, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        tw_k6_or_f3._ops,
        "enable_privileges",
        lambda advapi, kernel, privileges: calls.append(
            ("privilege", advapi, kernel, tuple(privileges))
        ),
    )
    monkeypatch.setattr(
        tw_k6_or_f3._ops,
        "hidden_popen",
        lambda command: calls.append(("popen", tuple(command))),
    )

    _entry(tw_k6_or_f3)()

    assert calls[-1] == (
        "popen",
        (
            "sec:lm_bt_1d",
            "sec:mn_cu_8f",
            "sec:zp_uq_6nsec:hm_xd_3k",
        ),
    )


@pytest.mark.parametrize(
    ("module_name", "function_name", "signal_name", "targets"),
    (
        (
            "km_40_cf_02",
            "rt_40_fan",
            "cmd_probe_full_fault",
            (
                ("src.py.com.yun.mao.bz_uc.lo_c4_or_f7", "mp_d1_go"),
                ("src.py.com.yun.mao.kv_nx.ru_i4_mp_d1", "tw_k2_rx"),
            ),
        ),
        (
            "vx_16_il_49",
            "bd_29_fan",
            "report_conn_timing_fault",
            (
                ("src.py.com.yun.mao.bz_uc.tw_k2_mp_d1", "or_f7_go"),
                ("src.py.com.yun.mao.kv_nx.ps_g8_ux_l9", "vy_m8_rx"),
            ),
        ),
        (
            "ps_38_ad_71",
            "ru_95_fan",
            "report_init_resp_corrupted",
            (
                ("src.py.com.yun.mao.kv_nx.ln_c2_aq_m7", "xz_o4_rx"),
                ("src.py.com.yun.mao.bz_uc.be_s0_ij_z5", "qs_h3_go"),
            ),
        ),
    ),
)
def test_wp_jt_signal_fanouts(
    monkeypatch, module_name, function_name, signal_name, targets
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.wp_jt.{module_name}")
    calls = []
    monkeypatch.setattr(
        module._ops,
        "emit_signal",
        lambda *args: calls.append(("emit", args[2])),
    )
    monkeypatch.setattr(
        module._ops,
        "call_entry",
        lambda target, name, *args: calls.append(("call", target, name)),
    )

    _entry(module)()

    assert calls[0] == ("emit", signal_name)
    assert calls[1:] == [("call", target, name) for target, name in targets]


@pytest.mark.parametrize(
    ("module_name", "function_name", "interval", "targets"),
    (
        (
            "pr_13_hk_48",
            "df_75_arm",
            1.08,
            (
                ("src.py.com.yun.mao.kv_nx.lo_c4_sv_j1", "ln_c2_rx"),
                ("src.py.com.yun.mao.bz_uc.ru_i4_il_z7", "eu_s1_go"),
            ),
        ),
        (
            "qs_52_vy_70",
            "ln_06_arm",
            0.92,
            (
                ("src.py.com.yun.mao.kv_nx.nq_e0_kn_b3", "jm_a6_rx"),
                ("src.py.com.yun.mao.bz_uc.jm_a6_kn_b3", "ce_t5_go"),
            ),
        ),
        (
            "xz_59_tv_92",
            "rt_67_arm",
            1.03,
            (
                ("src.py.com.yun.mao.kv_nx.hk_y8_ad_r9", "ps_g8_rx"),
                ("src.py.com.yun.mao.bz_uc.zc_q2_eu_s1", "il_z7_go"),
            ),
        ),
    ),
)
def test_wp_jt_timer_entries(
    monkeypatch, module_name, function_name, interval, targets
):
    import importlib

    module = importlib.import_module(f"src.py.com.yun.mao.wp_jt.{module_name}")
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
        lambda target, name, *args: calls.append(("call", target, name)),
    )

    _entry(module)()
    assert captured["interval"] == interval
    assert calls == ["start"]

    captured["callback"]()
    assert calls[1:] == [("call", target, name) for target, name in targets]


def test_wp_jt_yb_p7_np_e4_windll(monkeypatch):
    from src.py.com.yun.mao.wp_jt import yb_p7_np_e4

    calls = []

    class FakeExport:
        def __call__(self, *args):
            calls.append(("export", args))
            return 0

    class FakeDll:
        def __getattr__(self, name):
            return FakeExport()

    monkeypatch.setattr(yb_p7_np_e4, "sec", lambda key: f"sec:{key}")
    monkeypatch.setattr(
        yb_p7_np_e4.ctypes, "WinDLL", lambda name: FakeDll()
    )
    monkeypatch.setattr(
        yb_p7_np_e4.os, "_exit", lambda code: calls.append(("exit", code))
    )

    _entry(yb_p7_np_e4)()

    assert calls == [("export", (-1, 1)), ("exit", 1)]
