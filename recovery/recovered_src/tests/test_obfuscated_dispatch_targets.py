from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parents[1] / "src"

STRING_ONLY = {
    "src.py.com.yun.mao.bz_uc.dg_u6_qs_h3",
    "src.py.com.yun.mao.bz_uc.lo_c4_or_f7",
    "src.py.com.yun.mao.bz_uc.ru_i4_il_z7",
    "src.py.com.yun.mao.bz_uc.xa_o6_yb_p3",
    "src.py.com.yun.mao.kv_nx.be_s0_yb_p3",
    "src.py.com.yun.mao.kv_nx.lo_c4_sv_j1",
    "src.py.com.yun.mao.kv_nx.ru_i4_mp_d1",
    "src.py.com.yun.mao.kv_nx.tv_k0_eh_v3",
    "src.py.com.yun.mao.rm_qh.bx_n2_yb_p7",
    "src.py.com.yun.mao.rm_qh.jm_a2_sv_j7",
    "src.py.com.yun.mao.rm_qh.tw_k6_mp_d5",
    "src.py.com.yun.mao.rm_qh.zb_q6_gj_x5",
    "src.py.com.yun.mao.wp_jt.fi_w8_wy_n9",
    "src.py.com.yun.mao.wp_jt.lo_c8_qt_h9",
    "src.py.com.yun.mao.wp_jt.ru_i0_gj_x5",
    "src.py.com.yun.mao.wp_jt.xa_o0_ad_r5",
}


def test_string_only_dispatch_targets_are_not_loader_entries():
    loader = json.loads(
        (ROOT / "agent-notes" / "nuitka_module_table.json").read_text(
            encoding="utf-8"
        )
    )
    loader_names = {entry["name"] for entry in loader["entries"]}
    assert not (STRING_ONLY & loader_names)


def test_string_only_dispatch_targets_have_no_source_files():
    for name in STRING_ONLY:
        relative = name.removeprefix("src.py.com.yun.mao.").replace(".", "/")
        assert not (SRC / "py" / "com" / "yun" / "mao" / f"{relative}.py").exists()
