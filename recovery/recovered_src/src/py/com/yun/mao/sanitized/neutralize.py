"""Replace card-key gates and destructive entry points with inert stubs.

This module never calls the original network, subprocess, WinDLL or
encryption code.  It only monkeypatches already-imported modules.  The
faithful recovery tree remains unchanged unless ``apply()`` is called.
"""
from __future__ import annotations

from typing import Any

_PATCHES: list[tuple[object, str, Any]] = []
_APPLIED = False


def _patch(owner: object, name: str, replacement: Any) -> None:
    if not hasattr(owner, name):
        return
    _PATCHES.append((owner, name, getattr(owner, name)))
    setattr(owner, name, replacement)


def _patch_card_key() -> None:
    from src.py.com.yun.mao.dclass import AutoBeanXXX
    from src.py.com.yun.mao.fea import _sq_jqm
    from src.py.com.yun.mao.link import _lk_gy_r, _lk_gy_w

    info = _sq_jqm.current_account_info
    info.ucode = "SANITIZED-UCODE"
    info.status = 1
    info.grade = 1
    info.mul = True

    _patch(_sq_jqm, "_zh_rd_code", lambda *a, **k: ("SANITIZED-UCODE", True))
    _patch(_lk_gy_w, "_gy_uc", lambda: "SANITIZED-UCODE")
    for name in (
        "_gy_h0",
        "_gy_ex",
        "_gy_sa",
        "_gy_sb",
        "_gy_sc",
        "_gy_af",
        "_gy_rs",
    ):
        _patch(_lk_gy_w, name, lambda *a, **k: True)
    for index in range(1, 10):
        _patch(_lk_gy_w, f"gy_jc_a{index}", lambda *a, **k: True)
    _patch(_lk_gy_r, "gy_jc_b1", lambda *a, **k: True)
    _patch(
        AutoBeanXXX.AutoBeanXXX,
        "ensure_valid",
        lambda self, ucode: True,
    )


def _patch_anti_debug() -> None:
    from src.py.com.yun.mao.link import _fds_h_x

    cls = _fds_h_x.FdsHhx
    for name in (
        "_jk_jz_biao",
        "jk_bd_api",
        "jk_sx",
        "jk_ky_jc_fast",
        "jk_ky_jc_deep",
        "jk_ky_jc",
        "jk_qb",
        "jk_ky_jc_mk_all",
        "entry_blocked",
    ):
        _patch(cls, name, lambda self, *a, **k: False)
    for name in (
        "fh_lx_sd",
        "fh_qing",
        "fh_zhong_fast",
        "fh_zhong",
        "fh_quan",
        "fh_ui_qd",
        "fh_ht_jk",
        "fh_cj",
        "seal_abort",
    ):
        _patch(cls, name, lambda self, *a, **k: None)
    _patch(cls, "try_begin_abort", lambda self: False)
    _patch(cls, "wait_startup_probe", lambda self, timeout=0.5: None)


def _patch_shutdown() -> None:
    from src.py.com.yun.mao.fea import (
        _cw_jm_file,
        _dr_vx_file,
        _hb_yt_file,
        _lk_ps_file,
        _qf_rn_file,
        _yg_bn_file,
    )
    from src.py.com.yun.mao.link import (
        _fdg_cm_rx,
        _fdg_ct_ew,
        _fdg_ct_is,
        _fdg_os_kx,
        _fdg_pw_rm,
    )

    for module, names in (
        (_dr_vx_file, ("s_bq_sweep",)),
        (_qf_rn_file, ("g_wp_flush",)),
        (_hb_yt_file, ("k_dm_drain",)),
        (_lk_ps_file, ("n_lc_rinse",)),
        (_cw_jm_file, ("o_yt_purge",)),
        (_yg_bn_file, ("v_hz_scrub",)),
    ):
        for name in names:
            _patch(module, name, lambda *a, **k: None)

    _patch(_fdg_ct_ew, "ct_ew_drop", lambda *a, **k: None)
    _patch(_fdg_ct_is, "ct_is_snap", lambda *a, **k: None)
    _patch(_fdg_pw_rm, "pw_rm_fire", lambda *a, **k: None)
    _patch(_fdg_cm_rx, "cm_rx_push", lambda *a, **k: None)
    _patch(_fdg_os_kx, "os_kx_blow", lambda *a, **k: 0)


def _patch_ransom() -> None:
    from src.py.com.yun.mao.ade import (
        _ade_sing,
        _u_h,
        _u_hgd,
        _u_hvm,
        _u_common,
        _um_h,
        ad_t,
    )

    _patch(ad_t, "ad_t", lambda *a, **k: None)
    _patch(_u_common, "encrypt_log", lambda *a, **k: False)
    for module, names in (
        (_u_h, ("sk_nt",)),
        (_u_hgd, ("vm_star",)),
        (_u_hvm, ("iv_sk",)),
        (_um_h, ("sk_ntm",)),
    ):
        for name in names:
            _patch(module, name, lambda *a, **k: None)
    _patch(_ade_sing, "_ade_sing", lambda *a, **k: set())
    _patch(_ade_sing, "_ak", lambda *a, **k: None)
    _patch(_ade_sing, "encrypt_one", lambda *a, **k: False)
    _patch(_ade_sing, "delete_one", lambda *a, **k: False)


def apply() -> None:
    """Apply every neutralization patch once."""

    global _APPLIED
    if _APPLIED:
        return
    _patch_card_key()
    _patch_anti_debug()
    _patch_shutdown()
    _patch_ransom()
    _APPLIED = True


def restore() -> None:
    """Restore the faithful recovered implementations."""

    global _APPLIED
    for owner, name, original in reversed(_PATCHES):
        setattr(owner, name, original)
    _PATCHES.clear()
    _APPLIED = False
