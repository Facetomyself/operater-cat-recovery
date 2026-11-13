from __future__ import annotations

from src.py.com.yun.mao.config import (
    InnerAppIdConfig,
    YunYinMaoConfig,
    net_config,
)


class _Cache:
    def __init__(self, values):
        self.values = values

    def read_cache(self, group, key, default=None):
        if (group, key) in self.values:
            return self.values[(group, key)]
        return default


def test_net_config_uses_instance_and_returns_socks5_tuple(monkeypatch):
    cache = _Cache(
        {
            (net_config.PROXY_SETTING_GROUP, net_config.PROXY_SETTING_enable): "True",
            (net_config.PROXY_SETTING_GROUP, net_config.PROXY_SETTING_ip): "10.0.0.8",
            (net_config.PROXY_SETTING_GROUP, net_config.PROXY_SETTING_port): "1080",
        }
    )
    monkeypatch.setattr(
        net_config.tabl_cache,
        "INSTANCE",
        lambda: cache,
        raising=False,
    )
    assert net_config.enable_proxy() is True
    assert net_config.get_ip() == "10.0.0.8"
    assert net_config.get_port() == "1080"
    assert net_config.get_proxy_config() == ("socks5", "10.0.0.8", "1080")


def test_inner_app_id_uses_instance_cache(monkeypatch):
    monkeypatch.setattr(
        InnerAppIdConfig,
        "API_FUN_api_id",
        "test-api-id-key",
    )
    monkeypatch.setattr(
        InnerAppIdConfig,
        "API_FUN_api_hash",
        "test-api-hash-key",
    )
    cache = _Cache(
        {
            (
                InnerAppIdConfig.API_FUN_TAB,
                InnerAppIdConfig.API_FUN_api_id,
            ): "12345",
            (
                InnerAppIdConfig.API_FUN_TAB,
                InnerAppIdConfig.API_FUN_api_hash,
            ): "cached-hash",
        }
    )
    monkeypatch.setattr(
        InnerAppIdConfig.tabl_cache,
        "INSTANCE",
        lambda: cache,
        raising=False,
    )
    assert InnerAppIdConfig.get_api_id() == 12345
    assert InnerAppIdConfig.get_api_hash() == "cached-hash"


def test_inner_app_id_constants_match_recovered_values():
    from src.py.com.yun.mao.config import tabl_cache

    assert InnerAppIdConfig.API_FUN_TAB == tabl_cache.API_FUN_TAB
    assert InnerAppIdConfig.API_FUN_api_id == tabl_cache.API_FUN_api_id
    assert InnerAppIdConfig.API_FUN_api_hash == tabl_cache.API_FUN_api_hash
    assert InnerAppIdConfig.API_FUN_TAB == "api_fun_group"
    assert InnerAppIdConfig.API_FUN_api_id == "api_id"
    assert InnerAppIdConfig.API_FUN_api_hash == "api_hash"
    assert InnerAppIdConfig.INNER_API_ID == 27585141
    assert (
        InnerAppIdConfig.INNER_API_HASH
        == "27d609035e9e324d45346c0b9cdbe6bc"
    )
def test_yunyinmaoconfig_media_and_water_constants():
    assert YunYinMaoConfig.PIC_MEDIA_FILE_LIST == [".jpg", ".jpeg", ".png"]
    assert YunYinMaoConfig.VIDEO_MEDIA_FILE_LIST == [
        ".mp4",
        ".mov",
        ".avi",
        ".m4v",
    ]
    assert YunYinMaoConfig.WATER_MODE_TEXT == "文字水印"
    assert YunYinMaoConfig.WATER_MODE_PIC == "图片水印"
    assert YunYinMaoConfig.YUAN_SHI_PIN_DURATION[-1] == "完整版"


def test_commoncode_reads_cached_identity_values():
    from src.py.com.yun.mao.util.need import CommonCode

    assert CommonCode.read_soft_name() == "运营猫"
    assert CommonCode.read_ucode_pre() == "yunyinmao"
    assert CommonCode.read_contact_link() == "https://t.me/yunyingmaoo"
