from __future__ import annotations


CHAINS = {
    "_nx_r4_qm": (
        ("src.py.com.yun.mao.ade._u_h", "sk_nt"),
        ("src.py.com.yun.mao.wp_jt.pr_13_hk_48", "df_75_arm"),
        ("src.py.com.yun.mao.bz_uc.nq_23_vy_24", "cf_79_fan"),
    ),
    "_jv_c8_wt": (
        ("src.py.com.yun.mao.ade._u_hgd", "vm_star"),
        ("src.py.com.yun.mao.rm_qh.aq_70_eg_67", "bd_29_arm"),
        ("src.py.com.yun.mao.kv_nx.cf_44_ps_55", "pr_40_fan"),
    ),
    "_pl_a1_hz": (
        ("src.py.com.yun.mao.ade._u_hvm", "iv_sk"),
        ("src.py.com.yun.mao.bz_uc.pr_43_qs_39", "xa_56_arm"),
        ("src.py.com.yun.mao.wp_jt.vx_16_il_49", "bd_29_fan"),
    ),
    "_yk_m6_bd": (
        ("src.py.com.yun.mao.ade._um_h", "sk_ntm"),
        ("src.py.com.yun.mao.kv_nx.pr_40_oq_84", "ru_48_arm"),
        ("src.py.com.yun.mao.rm_qh.kn_97_oq_36", "ik_30_fan"),
    ),
    "_sg_e3_uf": (
        ("src.py.com.yun.mao.ade._u_h", "sk_nt"),
        ("src.py.com.yun.mao.wp_jt.xz_59_tv_92", "rt_67_arm"),
        ("src.py.com.yun.mao.bz_uc.aq_22_rt_78", "yb_25_fan"),
    ),
    "_to_x9_kr": (
        ("src.py.com.yun.mao.ade._u_hvm", "iv_sk"),
        ("src.py.com.yun.mao.rm_qh.wz_79_su_79", "xa_98_arm"),
        ("src.py.com.yun.mao.kv_nx.hk_29_lo_78", "kn_46_fan"),
    ),
    "_wq_b2_ln": (
        ("src.py.com.yun.mao.ade._u_h", "sk_nt"),
        ("src.py.com.yun.mao.bz_uc.ps_42_sv_93", "yb_39_arm"),
        ("src.py.com.yun.mao.wp_jt.ps_38_ad_71", "ru_95_fan"),
    ),
}


def test_probe_chain_targets(monkeypatch):
    from src.py.com.yun.mao.link import _fds_h_x, _fds_tan

    recorded = []

    class Probe:
        def try_begin_abort(self):
            return True

        def seal_abort(self):
            pass

    class Module:
        def __init__(self, module_name):
            self.module_name = module_name

        def __getattr__(self, name):
            recorded.append((self.module_name, name))
            return lambda: None

    monkeypatch.setattr(
        _fds_tan,
        "FdsHhx",
        Probe,
    )
    monkeypatch.setattr(_fds_h_x, "FdsHhx", Probe)
    monkeypatch.setattr(
        _fds_tan.importlib,
        "import_module",
        lambda module_name, *args, **kwargs: Module(module_name),
    )
    for name, expected in CHAINS.items():
        recorded.clear()
        getattr(_fds_tan, name)()
        assert tuple(recorded) == expected, name


def test_probe_functions_take_no_arguments():
    import inspect

    from src.py.com.yun.mao.link import _fds_tan

    for name in CHAINS:
        signature = inspect.signature(getattr(_fds_tan, name))
        assert list(signature.parameters) == [], name


def test_probe_chain_stops_when_abort_gate_is_busy(monkeypatch):
    from src.py.com.yun.mao.link import _fds_h_x, _fds_tan

    calls: list[str] = []

    class BusyProbe:
        def try_begin_abort(self):
            calls.append("try_begin_abort")
            return False

        def seal_abort(self):
            calls.append("seal_abort")

    monkeypatch.setattr(_fds_tan, "FdsHhx", BusyProbe)
    monkeypatch.setattr(_fds_h_x, "FdsHhx", BusyProbe)
    monkeypatch.setattr(
        _fds_tan.importlib,
        "import_module",
        lambda *args, **kwargs: calls.append("import"),
    )

    assert getattr(_fds_tan, next(iter(CHAINS)))() is None
    assert calls == ["try_begin_abort"]


def test_probe_chain_calls_each_step_without_arguments(monkeypatch):
    from src.py.com.yun.mao.link import _fds_h_x, _fds_tan

    calls: list[tuple[str, tuple]] = []

    class Probe:
        def try_begin_abort(self):
            return True

        def seal_abort(self):
            calls.append(("seal_abort", ()))

    class Step:
        def __getattr__(self, name):
            def run(*args, **kwargs):
                calls.append(("run", args))
                return "ok"

            return run

    monkeypatch.setattr(_fds_tan, "FdsHhx", Probe)
    monkeypatch.setattr(_fds_h_x, "FdsHhx", Probe)
    monkeypatch.setattr(
        _fds_tan.importlib,
        "import_module",
        lambda *args, **kwargs: Step(),
    )

    assert getattr(_fds_tan, next(iter(CHAINS)))() is None
    assert calls == [("run", ()), ("run", ()), ("run", ()), ("seal_abort", ())]


def test_timing_threshold_matches_recovered_constant():
    import inspect

    from src.py.com.yun.mao.link import _fds_tan

    signature = inspect.signature(_fds_tan._wb_jk_sx)
    assert signature.parameters["threshold_ms"].default == 50000


def test_wb_zs_bd_low_roll_only_probes(monkeypatch):
    from src.py.com.yun.mao.link import _fds_tan

    calls: list[str] = []

    class FakeProbe:
        def fh_lx_sd(self):
            calls.append("fh_lx_sd")

        def jk_ky_jc(self):
            calls.append("jk_ky_jc")
            return False

    monkeypatch.setattr(_fds_tan, "FdsHhx", FakeProbe)
    monkeypatch.setattr(
        _fds_tan,
        "_yk_m6_bd",
        lambda *args, **kwargs: calls.append("chain"),
    )
    monkeypatch.setattr(_fds_tan.random, "random", lambda: 0.1)

    _fds_tan.wb_zs_bd()
    assert calls == ["fh_lx_sd"]


def test_wb_zs_bd_high_roll_runs_chain_on_detection(monkeypatch):
    from src.py.com.yun.mao.link import _fds_tan

    calls: list[str] = []

    class FakeProbe:
        def fh_lx_sd(self):
            calls.append("fh_lx_sd")

        def jk_ky_jc(self):
            calls.append("jk_ky_jc")
            return True

    monkeypatch.setattr(_fds_tan, "FdsHhx", FakeProbe)
    monkeypatch.setattr(
        _fds_tan,
        "_yk_m6_bd",
        lambda *args, **kwargs: calls.append("chain"),
    )
    monkeypatch.setattr(_fds_tan.random, "random", lambda: 0.9)

    _fds_tan.wb_zs_bd()
    assert calls == ["jk_ky_jc", "chain"]
