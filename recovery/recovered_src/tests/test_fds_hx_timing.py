from __future__ import annotations

import inspect


def test_probe_timing_constants_match_recovered_values():
    from src.py.com.yun.mao.link._fds_h_x import FdsHhx

    assert FdsHhx.DEEP_SCAN_MIN_INTERVAL_SEC == 300.0
    assert FdsHhx.STARTUP_PROBE_WAIT_SEC == 5.0
    assert FdsHhx.CONT_FAST_SCAN_MIN_SEC == 10.0
    assert FdsHhx.CONT_FAST_SCAN_MAX_SEC == 12.0
    assert FdsHhx.CONT_FULL_SCAN_MIN_SEC == 18.0
    assert FdsHhx.CONT_FULL_SCAN_MAX_SEC == 180.0


def test_fh_ht_jk_and_wait_startup_probe_signatures():
    from src.py.com.yun.mao.link._fds_h_x import FdsHhx

    fh = inspect.signature(FdsHhx.fh_ht_jk)
    assert list(fh.parameters) == [
        "self",
        "interval",
        "min_interval",
        "max_interval",
    ]
    assert fh.parameters["interval"].default == 5.0
    assert fh.parameters["min_interval"].default is None
    assert fh.parameters["max_interval"].default is None

    wait = inspect.signature(FdsHhx.wait_startup_probe)
    assert list(wait.parameters) == ["self", "timeout"]
    assert wait.parameters["timeout"].default == 0.5
