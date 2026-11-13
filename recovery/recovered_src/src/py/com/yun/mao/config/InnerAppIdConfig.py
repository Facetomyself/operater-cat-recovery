# Recovered module: src.py.com.yun.mao.config.InnerAppIdConfig
# Reconstruction from Nuitka metadata, static strings, and Hex-Rays.
# This is not original source; unmarked bodies are stubs.
from __future__ import annotations
from . import tabl_cache
from .tabl_cache import API_FUN_TAB, API_FUN_api_hash, API_FUN_api_id

# Imports observed in the runtime module dictionary

# Embedded fallback credentials recovered from the constants chunk.
INNER_API_HASH = "27d609035e9e324d45346c0b9cdbe6bc"
INNER_API_ID = 27585141

def get_api_hash():
    """Read the Telegram API hash, falling back to the embedded value."""
    app_hash = tabl_cache.INSTANCE().read_cache(API_FUN_TAB, API_FUN_api_hash)
    return app_hash or INNER_API_HASH

def get_api_id():
    """Read the Telegram API id, falling back to the embedded value."""
    app_id = tabl_cache.INSTANCE().read_cache(API_FUN_TAB, API_FUN_api_id)
    value = app_id or INNER_API_ID
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

# Other global objects
# tabl_cache: instance <module>

# --- static symbol index ---
# Static symbols observed in the binary string table.
# src.py.com.yun.mao.config.InnerAppIdConfig
