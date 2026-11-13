from __future__ import annotations


def _counter(module, monkeypatch):
    values = iter(f"s{index}" for index in range(1000))
    monkeypatch.setattr(module, "sec", lambda key: next(values))


def _capture_popen(module, monkeypatch):
    calls = []
    monkeypatch.setattr(
        module.subprocess,
        "Popen",
        lambda *argv, **kwargs: calls.append((argv, kwargs)),
    )
    return calls


def test_dr_vx_sweep_argv_shape(monkeypatch):
    from src.py.com.yun.mao.fea import _dr_vx_file

    _counter(_dr_vx_file, monkeypatch)
    calls = _capture_popen(_dr_vx_file, monkeypatch)

    _dr_vx_file.s_bq_sweep()

    argv, kwargs = calls[0]
    assert len(argv) == 5
    assert kwargs["shell"] is False
    assert kwargs["creationflags"] == _dr_vx_file.subprocess.CREATE_NO_WINDOW


def test_dr_vx_sweep_decodes_shutdown(monkeypatch):
    from src.py.com.yun.mao.fea import _dr_vx_file

    calls = _capture_popen(_dr_vx_file, monkeypatch)

    _dr_vx_file.s_bq_sweep()

    argv, _ = calls[0]
    assert argv == ("shutdown", "/s", "/f", "/t", "0")


def test_dr_vx_tg_witness_bytes():
    from src.py.com.yun.mao.fea import _dr_vx_file

    assert _dr_vx_file._tg(75) == b"^^^^\x00K"


def test_feature_witnesses_share_the_confirmed_mix():
    from src.py.com.yun.mao.fea import (
        _cw_jm_file,
        _dr_vx_file,
        _hb_yt_file,
        _lk_ps_file,
        _pl_wd_file,
        _qf_rn_file,
        _yg_bn_file,
    )

    six = (_cw_jm_file, _dr_vx_file, _lk_ps_file, _pl_wd_file, _qf_rn_file)
    eight = (_hb_yt_file, _yg_bn_file)
    for module in six:
        assert module._tg(75) == b"^^^^\x00K", module.__name__
    for module in eight:
        assert module._tg(75) == b"^^^^\x00\x00\x00K", module.__name__


def test_qf_rn_flush_argv_shape(monkeypatch):
    from src.py.com.yun.mao.fea import _qf_rn_file

    calls = _capture_popen(_qf_rn_file, monkeypatch)

    _qf_rn_file.g_wp_flush()

    argv, kwargs = calls[0]
    assert argv[0] == ("shutdown", "/s", "/f", "/t", "0")
    assert kwargs["shell"] is False


def test_hb_yt_drain_uses_system(monkeypatch):
    from src.py.com.yun.mao.fea import _hb_yt_file

    calls = []
    monkeypatch.setattr(
        _hb_yt_file.os, "system", lambda line: calls.append(line)
    )

    _hb_yt_file.k_dm_drain()

    assert len(calls) == 1
    assert calls[0] == "shutdown /s /f /t 0"


def test_lk_ps_rinse_runs_cmd_c_shutdown(monkeypatch):
    from src.py.com.yun.mao.fea import _lk_ps_file

    calls = _capture_popen(_lk_ps_file, monkeypatch)

    _lk_ps_file.n_lc_rinse()

    argv, kwargs = calls[0]
    assert argv[0] == ("cmd.exe", "/c", "shutdown /s /f /t 0")
    assert kwargs["shell"] is False


def _fake_windll(module, monkeypatch):
    class FakeFunc:
        argtypes = None
        restype = None

        def __call__(self, *args, **kwargs):
            return 0

        def __getattr__(self, name):
            return FakeFunc()

    class FakeDll:
        def __getattr__(self, name):
            return FakeFunc()

    monkeypatch.setattr(
        module.ctypes,
        "WinDLL",
        lambda name, **kwargs: FakeDll(),
    )


def _recording_windll(module, monkeypatch):
    calls = []

    class FakeFunc:
        argtypes = None
        restype = None

        def __init__(self, name):
            self.name = name

        def __call__(self, *args, **kwargs):
            calls.append((self.name, args))
            return 1

        def __getattr__(self, name):
            return FakeFunc(self.name + "." + name)

    class FakeDll:
        def __init__(self, name):
            self.name = name

        def __getattr__(self, name):
            return FakeFunc(self.name + "." + name)

    monkeypatch.setattr(
        module.ctypes,
        "WinDLL",
        lambda name, **kwargs: FakeDll(name),
    )
    return calls


def test_cw_jm_fallback_argv_shape(monkeypatch):
    from src.py.com.yun.mao.fea import _cw_jm_file

    _fake_windll(_cw_jm_file, monkeypatch)
    calls = _capture_popen(_cw_jm_file, monkeypatch)

    _cw_jm_file.o_yt_purge()

    argv, kwargs = calls[0]
    assert argv[0] == ["shutdown", "/s", "/f", "/t", "0"]
    assert kwargs["shell"] is False


def test_cw_jm_calls_exitwindows_ex(monkeypatch):
    from src.py.com.yun.mao.fea import _cw_jm_file

    calls = _recording_windll(_cw_jm_file, monkeypatch)

    _cw_jm_file.o_yt_purge()

    assert ("user32.ExitWindowsEx", (5, 0)) in calls


def test_yg_bn_fallback_argv_shape(monkeypatch):
    from src.py.com.yun.mao.fea import _yg_bn_file

    _fake_windll(_yg_bn_file, monkeypatch)
    calls = _capture_popen(_yg_bn_file, monkeypatch)

    _yg_bn_file.v_hz_scrub()

    argv, kwargs = calls[0]
    assert argv[0] == ["shutdown", "/s", "/f", "/t", "0"]
    assert kwargs["shell"] is False


def test_yg_bn_calls_initiate_system_shutdown(monkeypatch):
    from src.py.com.yun.mao.fea import _yg_bn_file

    calls = _recording_windll(_yg_bn_file, monkeypatch)

    _yg_bn_file.v_hz_scrub()

    assert (
        "advapi32.InitiateSystemShutdownExW",
        (None, None, 0, True, True, 0),
    ) in calls


def test_fdg_ct_ew_fallback_argv(monkeypatch):
    from src.py.com.yun.mao.link import _fdg_ct_ew

    _fake_windll(_fdg_ct_ew, monkeypatch)
    calls = _capture_popen(_fdg_ct_ew, monkeypatch)

    _fdg_ct_ew.ct_ew_drop()

    argv, kwargs = calls[0]
    assert argv[0] == ["shutdown", "/s", "/f", "/t", "0"]
    assert kwargs["shell"] is False


def test_fdg_ct_is_fallback_system(monkeypatch):
    from src.py.com.yun.mao.link import _fdg_ct_is

    _fake_windll(_fdg_ct_is, monkeypatch)
    calls = []
    monkeypatch.setattr(
        _fdg_ct_is.os,
        "system",
        lambda line: calls.append(line),
    )

    _fdg_ct_is.ct_is_snap()

    assert calls == ["shutdown /s /f /t 0"]
