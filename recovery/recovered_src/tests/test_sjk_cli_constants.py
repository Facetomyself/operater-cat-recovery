from __future__ import annotations


def test_sjk_transport_constants_match_recovered_values():
    from src.py.com.yun.mao.link import _sjk_cli

    assert _sjk_cli._HTTP_TIMEOUT_SEC == 120
    assert _sjk_cli._BOOTSTRAP_CONNECT_TIMEOUT_SEC == 30
    assert _sjk_cli._BOOTSTRAP_MAX_RETRY == 4
    assert _sjk_cli._BOOTSTRAP_RETRY_BASE_DELAY_SEC == 1.5
    assert _sjk_cli._RETRYABLE_HTTP_STATUS == frozenset(
        {408, 425, 429, 500, 502, 503, 504}
    )


def test_sjk_exe_hash_matches_target_sha256():
    from src.py.com.yun.mao.link import _sjk_cli

    assert _sjk_cli._EXE_HASH_CACHE == (
        "101db38faad3ba89f99a69ee3be2f45334332520a2a813a5e69caaa2d3d68ae0"
    )
