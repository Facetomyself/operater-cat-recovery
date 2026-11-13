# Recovered module: src.py.com.yun.mao.link._fds_rt
# Response/probe wrappers reconstructed from the module constants and the
# FdsHhx method names. Probabilities and throttles are taken from the
# Nuitka constant chunk; the branch order is confirmed by the constant order.
from __future__ import annotations

import random
import threading
import time

from ._fds_h_x import FdsHhx


_BY_PF_MID_EVERY = 10
_DT_LQ_MID_MIN_INTERVAL_SEC = 60.0
_by_pf_count = 0
_dt_lq_last_mid_mono = 0.0
_by_pf_lock = threading.Lock()
_dt_lq_mid_lock = threading.Lock()


def _probe() -> FdsHhx:
    return FdsHhx()


def fs_jc_qd():
    """Start/continue the fast watchdog loop."""
    _probe().fh_ht_jk(4.0, 8.0)


def fs_ui_ok():
    """UI/startup probe entry."""
    _probe().fh_ui_qd()


def fs_sjk_ws():
    """Medium response wrapper."""
    _probe().fh_zhong()


def fs_sjk_qd():
    """Light response wrapper."""
    _probe().fh_zhong()


def fs_http():
    """Probabilistic network/probe escalation (0.55/0.85 thresholds)."""
    roll = random.random()
    if roll < 0.55:
        _probe().fh_qing()
    elif roll < 0.85:
        _probe().fh_lx_sd()
    else:
        _probe().fh_zhong()


def fs_hy_men():
    """Light response wrapper with the 0.25 sample threshold."""
    if random.random() < 0.25:
        _probe().fh_zhong()
    else:
        _probe().fh_qing()


def fs_zh_tb():
    """Full response wrapper."""
    _probe().fh_zhong()


def fs_dt_mk():
    """Probabilistic full/medium probe used by the dynamic-task path."""
    if random.random() < 0.25:
        _probe().fh_quan()
    else:
        _probe().fh_zhong()


def fs_dt_lq():
    """Rate-limit the medium-depth scan to one call per interval."""
    if random.random() < 0.9:
        _probe().fh_qing()
    global _dt_lq_last_mid_mono
    now = time.monotonic()
    do_mid = False
    with _dt_lq_mid_lock:
        if now - _dt_lq_last_mid_mono >= _DT_LQ_MID_MIN_INTERVAL_SEC:
            _dt_lq_last_mid_mono = now
            do_mid = True
    if do_mid:
        _probe().fh_zhong_fast()


def fs_by_pf():
    """Return True every ``_BY_PF_MID_EVERY`` calls."""
    global _by_pf_count
    with _by_pf_lock:
        _by_pf_count += 1
        n = _by_pf_count
    if n % _BY_PF_MID_EVERY == 0:
        _probe().fh_zhong_fast()


def fs_pz_jm():
    if random.random() < 0.12:
        _probe().fh_quan()
    else:
        _probe().fh_zhong()


def fs_yp_js():
    """Probabilistic sample used by the media/parse path (0.60)."""
    if random.random() < 0.60:
        _probe().fh_qing()
    else:
        _probe().fh_lx_sd()
