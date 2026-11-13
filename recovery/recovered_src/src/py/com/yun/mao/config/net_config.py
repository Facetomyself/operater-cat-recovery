# Recovered module: src.py.com.yun.mao.config.net_config
# Reconstruction from Nuitka metadata, static strings, and Hex-Rays.
# This is not original source; unmarked bodies are stubs.
from __future__ import annotations
from . import tabl_cache

# Imports observed in the runtime module dictionary

# Module constants (secrets redacted)
INNER_IP = '127.0.0.1'
INNER_PORT = '40008'
PROXY_SETTING_GROUP = 'proxy_setting_group'
PROXY_SETTING_enable = 'proxy_enable'
PROXY_SETTING_ip = 'proxy_ip'
PROXY_SETTING_port = 'proxy_port'

# Module-level functions
def enable_proxy() -> bool:
    proxy_enable_str = tabl_cache.INSTANCE().read_cache(
        PROXY_SETTING_GROUP, PROXY_SETTING_enable, "False"
    )
    return proxy_enable_str != "False"


def get_ip() -> str:
    ip = tabl_cache.INSTANCE().read_cache(
        PROXY_SETTING_GROUP, PROXY_SETTING_ip, INNER_IP
    )
    return ip


def get_port() -> str:
    port = tabl_cache.INSTANCE().read_cache(
        PROXY_SETTING_GROUP, PROXY_SETTING_port, INNER_PORT
    )
    return port


def get_proxy_config() -> tuple[str, str, str]:
    return ("socks5", get_ip(), get_port())

# Other global objects
# tabl_cache: instance <module>

# --- static symbol index ---
# Static symbols observed in the binary string table.
# src.py.com.yun.mao.config.net_config
