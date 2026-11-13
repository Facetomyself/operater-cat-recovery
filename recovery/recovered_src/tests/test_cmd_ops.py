from __future__ import annotations


def test_module_name_and_load_attr():
    from src.py.com.yun.mao.fea import _cmd_ops

    assert (
        _cmd_ops.module_name("src.py.com.yun.mao.fea._sq_jqm")
        == "src.py.com.yun.mao.fea._sq_jqm"
    )
    assert (
        _cmd_ops.load_attr(
            "src.py.com.yun.mao.fea._sq_jqm", "current_account_info"
        )
        is not None
    )
    assert (
        _cmd_ops.load_attr(
            "src.py.com.yun.mao.fea._sq_jqm", "missing", "fallback"
        )
        == "fallback"
    )


def test_call_attr_and_optional_call():
    from src.py.com.yun.mao.fea import _cmd_ops

    class Target:
        def first(self, value):
            return value + 1

    assert (
        _cmd_ops.call_attr(
            "src.py.com.yun.mao.fea._sq_jqm", "zh_zw_uc", "ucode"
        )
        == "ucode"
    )
    assert _cmd_ops.optional_call(Target(), ("missing", "first"), 1) == 2
    assert _cmd_ops.optional_call(None, ("first",)) is None


def test_reorder_and_mix32():
    from src.py.com.yun.mao.fea import _cmd_ops

    assert _cmd_ops.reorder("abcdefgh", (7, 0, 6, 1, 5, 2, 4, 3)) == tuple(
        "hagbfced"
    )
    assert _cmd_ops.reorder("ab", (0, 9, 1)) == ("a", "b")
    assert _cmd_ops.mix32(1, 3, 5, 1, 7) == 15


def test_hidden_popen_uses_fake_backend():
    from src.py.com.yun.mao.fea import _cmd_ops

    class FakeBackend:
        CREATE_NO_WINDOW = 0x08000000
        DEVNULL = -3

        def Popen(self, command, **kwargs):
            return command, kwargs

    command, kwargs = _cmd_ops.hidden_popen(["demo"], module=FakeBackend())

    assert command == ["demo"]
    assert kwargs["shell"] is False
    assert kwargs["stdin"] == -3
    assert kwargs["creationflags"] == 0x08000000


def test_enable_privileges_failure_path(monkeypatch):
    from src.py.com.yun.mao.fea import _cmd_ops

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
        _cmd_ops.ctypes, "WinDLL", lambda name, **kwargs: FakeDll()
    )

    assert _cmd_ops.enable_privileges("advapi", "kernel", ("priv",)) is False
