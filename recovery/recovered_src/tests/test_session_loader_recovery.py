from __future__ import annotations

import sys
import types


def _install_fake_telethon(monkeypatch):
    telethon = types.ModuleType("telethon")

    class TelegramClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    errors = types.ModuleType("telethon.errors")
    for name in (
        "PhonePasswordFloodError",
        "AuthKeyDuplicatedError",
        "RPCError",
    ):
        setattr(errors, name, type(name, (Exception,), {}))
    functions = types.ModuleType("telethon.functions")
    functions.updates = types.SimpleNamespace(GetStateRequest=object)
    telethon.TelegramClient = TelegramClient
    telethon.errors = errors
    telethon.functions = functions

    tl = types.ModuleType("telethon.tl")
    tl_functions = types.ModuleType("telethon.tl.functions")
    account = types.ModuleType("telethon.tl.functions.account")
    account.GetPrivacyRequest = type(
        "GetPrivacyRequest",
        (),
        {"__init__": lambda self, *args, **kwargs: None},
    )
    account.SetPrivacyRequest = type(
        "SetPrivacyRequest",
        (),
        {"__init__": lambda self, *args, **kwargs: None},
    )
    tl_types = types.ModuleType("telethon.tl.types")
    for name in (
        "InputPrivacyKeyStatusTimestamp",
        "InputPrivacyValueDisallowAll",
        "PrivacyValueDisallowAll",
    ):
        setattr(
            tl_types,
            name,
            type(name, (), {"__init__": lambda self, *args, **kwargs: None}),
        )

    mods = {
        "telethon": telethon,
        "telethon.errors": errors,
        "telethon.functions": functions,
        "telethon.tl": tl,
        "telethon.tl.functions": tl_functions,
        "telethon.tl.functions.account": account,
        "telethon.tl.types": tl_types,
    }
    for name, module in mods.items():
        monkeypatch.setitem(sys.modules, name, module)


def test_session_loader_exception_classification(monkeypatch):
    _install_fake_telethon(monkeypatch)
    from src.py.com.yun.mao.login import SessionLoader

    class AuthKeyUnregisteredError(Exception):
        pass

    class UserBannedInChannelError(Exception):
        pass

    assert SessionLoader._is_dead_exception(AuthKeyUnregisteredError())
    assert SessionLoader._is_band_exception(UserBannedInChannelError())
    assert not SessionLoader._is_dead_exception(ValueError())


def test_session_loader_message_and_scan(monkeypatch, tmp_path):
    _install_fake_telethon(monkeypatch)
    from src.py.com.yun.mao.login import SessionLoader

    monkeypatch.setattr(
        SessionLoader.utils,
        "generate_random_chinese",
        lambda length: "随机内容",
    )
    assert SessionLoader.ramdom_message("猫") == "随机内容 say 猫"
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "a.session").write_text("x", encoding="utf-8")
    (nested / "ignore.txt").write_text("x", encoding="utf-8")
    assert SessionLoader.list_session_file(str(tmp_path)) == [
        str(nested / "a.session")
    ]


def test_login_once_sends_startup_greeting(monkeypatch):
    _install_fake_telethon(monkeypatch)
    from src.py.com.yun.mao.login import SessionLoader

    sent = []
    errors = []

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def connect(self):
            return None

        def is_connected(self):
            return True

        async def is_user_authorized(self):
            return True

        async def __call__(self, request):
            return None

        async def get_me(self):
            return types.SimpleNamespace(full_name="猫")

        async def send_message(self, target, message):
            sent.append((target, message))

    async def no_invisible(client):
        return True

    monkeypatch.setattr(SessionLoader, "TelegramClient", FakeClient)
    monkeypatch.setattr(SessionLoader, "set_invisible_mode", no_invisible)
    monkeypatch.setattr(SessionLoader.InnerAppIdConfig, "get_api_id", lambda: 1)
    monkeypatch.setattr(SessionLoader.InnerAppIdConfig, "get_api_hash", lambda: "hash")
    monkeypatch.setattr(
        SessionLoader,
        "connectException",
        lambda exc, prefix="": errors.append((exc, prefix)),
    )
    monkeypatch.setattr(
        SessionLoader.utils,
        "split_session",
        lambda session: ("", "+10000"),
    )
    monkeypatch.setattr(
        SessionLoader.utils,
        "generate_random_chinese",
        lambda length: "随机内容",
    )
    monkeypatch.setattr(
        SessionLoader.net_config,
        "enable_proxy",
        lambda: False,
    )
    monkeypatch.setattr(
        SessionLoader.ClientCacheHelper,
        "save_cache_client",
        lambda client: None,
    )
    monkeypatch.setattr(
        SessionLoader._sq_jqm.current_account_info,
        "sendAtName",
        "@owner",
        raising=False,
    )

    import asyncio

    result = asyncio.run(
        SessionLoader._login_once("+10000.session")
    )
    assert errors == []
    assert result[0].__class__ is FakeClient
    assert sent == [("@owner", "随机内容 say 猫")]


def test_set_invisible_mode_skips_when_already_disallowed(monkeypatch):
    _install_fake_telethon(monkeypatch)
    from src.py.com.yun.mao.login import SessionLoader

    calls = []

    class FakeClient:
        async def __call__(self, request):
            calls.append(request)
            if type(request).__name__ == "GetPrivacyRequest":
                from types import SimpleNamespace

                return SimpleNamespace(
                    rules=[SessionLoader.PrivacyValueDisallowAll()]
                )
            return None

    monkeypatch.setattr(
        SessionLoader.FloodGuard,
        "with_flood_retry",
        lambda fn, prefix="x": fn(),
    )

    import asyncio

    assert asyncio.run(SessionLoader.set_invisible_mode(FakeClient())) is True
    assert len(calls) == 1


def test_set_invisible_mode_sets_rules_when_not_present(monkeypatch):
    _install_fake_telethon(monkeypatch)
    from src.py.com.yun.mao.login import SessionLoader

    calls = []

    class FakeClient:
        async def __call__(self, request):
            calls.append(request)
            if type(request).__name__ == "GetPrivacyRequest":
                from types import SimpleNamespace

                return SimpleNamespace(rules=[])
            return None

    monkeypatch.setattr(
        SessionLoader.FloodGuard,
        "with_flood_retry",
        lambda fn, prefix="x": fn(),
    )

    import asyncio

    assert asyncio.run(SessionLoader.set_invisible_mode(FakeClient())) is True
    assert len(calls) == 2
    assert type(calls[1]).__name__ == "SetPrivacyRequest"
