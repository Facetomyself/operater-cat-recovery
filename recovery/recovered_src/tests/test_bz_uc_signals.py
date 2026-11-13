from __future__ import annotations

import sys
import types

from src.py.com.yun.mao.bz_uc import aq_22_rt_78, fi_49_qs_87, nq_23_vy_24


class _Signal:
    def __init__(self, calls: list[str], name: str):
        self.calls = calls
        self.name = name

    def emit(self) -> None:
        self.calls.append(self.name)


def _handler_module(
    calls: list[str],
    module_name: str,
    attr: str,
    label: str,
) -> types.ModuleType:
    module = types.ModuleType(module_name)
    setattr(module, attr, lambda: calls.append(label))
    return module


def _install(monkeypatch, calls: list[str]) -> None:
    signal_module = types.ModuleType(
        "src.py.com.yun.mao.util.need.signals"
    )
    signal_module.global_ui_signal = types.SimpleNamespace(
        notify_crypto_ctx_broken=_Signal(calls, "crypto"),
        notify_link_integrity_fail=_Signal(calls, "link"),
        report_probe_mid_fault=_Signal(calls, "mid"),
    )
    monkeypatch.setitem(
        sys.modules,
        "src.py.com.yun.mao.util.need.signals",
        signal_module,
    )
    for module_name, attr, label in (
        (
            "src.py.com.yun.mao.bz_uc.xa_o6_yb_p3",
            "qt_h5_go",
            "qt_h5_go",
        ),
        (
            "src.py.com.yun.mao.kv_nx.be_s0_yb_p3",
            "xa_o6_rx",
            "xa_o6_rx",
        ),
        (
            "src.py.com.yun.mao.kv_nx.dg_u6_qt_h5",
            "tv_k0_rx",
            "tv_k0_rx",
        ),
        (
            "src.py.com.yun.mao.bz_uc.ps_g8_ad_r9",
            "mo_d9_go",
            "mo_d9_go",
        ),
        (
            "src.py.com.yun.mao.kv_nx.fh_w2_il_z7",
            "ru_i4_rx",
            "ru_i4_rx",
        ),
        (
            "src.py.com.yun.mao.bz_uc.hk_y0_ce_t5",
            "kn_b3_go",
            "kn_b3_go",
        ),
    ):
        monkeypatch.setitem(
            sys.modules,
            module_name,
            _handler_module(calls, module_name, attr, label),
        )


def test_crypto_signal_fanout(monkeypatch):
    calls: list[str] = []
    _install(monkeypatch, calls)

    aq_22_rt_78.yb_25_fan()
    assert calls == ["crypto", "qt_h5_go", "xa_o6_rx"]


def test_link_signal_fanout(monkeypatch):
    calls: list[str] = []
    _install(monkeypatch, calls)

    nq_23_vy_24.cf_79_fan()
    assert calls == ["link", "tv_k0_rx", "mo_d9_go"]


def test_mid_probe_signal_fanout(monkeypatch):
    calls: list[str] = []
    _install(monkeypatch, calls)

    fi_49_qs_87.aq_87_fan()
    assert calls == ["mid", "kn_b3_go", "ru_i4_rx"]
