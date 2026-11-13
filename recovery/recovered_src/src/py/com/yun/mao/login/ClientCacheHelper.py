# Recovered module: src.py.com.yun.mao.login.ClientCacheHelper
# Reconstruction from Nuitka metadata, static strings, and Hex-Rays.
# This is not original source; unmarked bodies are stubs.
from __future__ import annotations

# Imports observed in the runtime module dictionary

# Module constants (secrets redacted)
cache_client = None

# Module-level functions
def safe_disconnect_client():
    """Disconnect the cached Telegram client without raising."""
    if cache_client is None:
        return None
    try:
        from ..util.need.CommonCode import safe_disconnect

        safe_disconnect(cache_client)
    except Exception:
        pass
    return None

def save_cache_client(client):
    """Replace the process-wide cached Telegram client."""
    global cache_client
    safe_disconnect_client()
    cache_client = client
    return None

# Other global objects
# CommonCode: instance <module>

# --- static symbol index ---
# Static symbols observed in the binary string table.
# src.py.com.yun.mao.login.ClientCacheHelper
