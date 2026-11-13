# Recovered module: src.py.com.yun.mao.telefast.FastDownUpLoadUtils
from __future__ import annotations

import time

from . import CallBack


def fast_down_load(client, document, fileAbsPath, progress_callback=None):
    """Download a Telegram document through the fast transfer helper."""

    from .FastTelethon import download_file

    CallBack.down_start_time = time.time()
    with open(fileAbsPath, "wb") as out:
        return download_file(
            client,
            document,
            file=out,
            progress_callback=progress_callback,
        )


def fast_down_load_partial(
    client,
    document,
    fileAbsPath,
    max_bytes=None,
    byte_offset=0,
    append=False,
    progress_callback=None,
    reset_timer=True,
):
    """Download a byte range, optionally appending to an existing file."""

    from .FastTelethon import download_file

    if reset_timer:
        CallBack.down_start_time = time.time()
    mode = "ab" if append else "wb"
    with open(fileAbsPath, mode) as out:
        return download_file(
            client,
            document,
            file=out,
            max_bytes=max_bytes,
            byte_offset=int(byte_offset or 0),
            progress_callback=progress_callback,
        )


def fast_up_load(
    client,
    fileAbsPath,
    progress_callback=None,
):
    """Upload a local file through the fast transfer helper."""

    from .FastTelethon import upload_file

    CallBack.up_start_time = time.time()
    with open(fileAbsPath, "rb") as out:
        res = upload_file(
            client,
            file=out,
            progress_callback=progress_callback,
        )
    return res
