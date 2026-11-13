"""Shared helpers for the ``rm_qh`` recovery layer.

Importing this module must not trigger any target action.  Application
modules are imported lazily and guarded so a partial recovery tree stays
importable.
"""
from __future__ import annotations

import gc
import importlib
import os
import subprocess
import threading
from typing import Any, Callable, Iterable


def _module_name(full_name: str) -> str:
    # The recovered tree keeps the loader-table ``src.py.`` prefix.
    return full_name


def import_module(full_name: str):
    return importlib.import_module(_module_name(full_name))


def load_attr(full_name: str, attr_name: str, default: Any = None) -> Any:
    try:
        return getattr(import_module(full_name), attr_name, default)
    except Exception:
        return default


def call_entry(full_name: str, attr_name: str, *args: Any, **kwargs: Any) -> Any:
    func = load_attr(full_name, attr_name)
    if func is None:
        return None
    return func(*args, **kwargs)


def call_method(obj: Any, method_name: str, *args: Any, **kwargs: Any) -> Any:
    if obj is None:
        return None
    method = getattr(obj, method_name, None)
    if method is None:
        return None
    return method(*args, **kwargs)


def emit(signal_obj: Any, signal_name: str, *args: Any) -> bool:
    signal = getattr(signal_obj, signal_name, None)
    emitter = getattr(signal, "emit", None)
    if emitter is None:
        return False
    emitter(*args)
    return True


def redacted_secret(label: str) -> str:
    """Opaque stand-in for an encoded literal redacted in the evidence."""
    return f"<redacted:{label}>"


def redacted_name(label: str) -> str:
    """Opaque stand-in for a symbol name redacted in the evidence."""
    return f"<redacted-name:{label}>"


def decode_abort_parts() -> tuple[str, ...]:
    decoder = load_attr("src.py.com.yun.mao.link._fds_jm", "decode_str_tuple")
    parts = load_attr("src.py.com.yun.mao.link._fds_sj", "ABORT_PARTS_ENC", ())
    key = load_attr("src.py.com.yun.mao.link._fds_sj", "KEY", b"")
    parts = tuple(parts or ())
    if decoder is None:
        return parts
    try:
        return tuple(decoder(parts, key))
    except Exception:
        return parts


def abort_message() -> str:
    return "\n\n".join(decode_abort_parts())


def show_error_tip(error_msg: str, timeout: int = 1000) -> Any:
    show = load_attr("src.py.com.yun.mao.ErrorDialog", "show_error_tip")
    if show is None:
        dialog = load_attr("src.py.com.yun.mao.ErrorDialog", "ErrorDialog")
        show = getattr(dialog, "show_error_tip", None) if dialog is not None else None
    if show is None:
        return None
    try:
        return show(error_msg=error_msg, timeout=timeout)
    except TypeError:
        return show(error_msg, timeout)


def prepare_abort_dialog(
    _show: Any,
    _geh: Any,
    _w: Any,
    _dst: Any,
    _sj: Any,
    _msg: Any,
    _ed: Any,
    _g: Any,
    _r: Any,
) -> tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any]:
    """Execute the shared decode-and-show prefix used by the three dialogs."""
    _geh = _geh or global_exception_handler()
    _w = _w or global_window()
    if _w is not None and getattr(_w, "isVisible", lambda: False)():
        _show = _show or _geh
    _dst = decode_abort_parts()
    _sj = load_attr("src.py.com.yun.mao.link", "_fds_sj", _sj)
    _msg = "\n\n".join(_dst)
    _ed = _ed or load_attr("src.py.com.yun.mao.ErrorDialog", "ErrorDialog")
    _g = show_error_tip(error_msg=_msg, timeout=1000)
    _r = _g
    return _show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r


def global_window() -> Any:
    return load_attr("src.py.com.yun.mao", "global_window")


def global_exception_handler() -> Any:
    return load_attr("src.py.com.yun.mao", "GlobalExceptionHandler")


def create_timer(delay: float, callback: Callable[[], Any], daemon: bool = True) -> threading.Timer:
    timer = threading.Timer(delay, callback)
    timer.daemon = daemon
    return timer


def start_timer(delay: float, callback: Callable[[], Any], daemon: bool = True) -> threading.Timer:
    timer = create_timer(delay, callback, daemon=daemon)
    timer.start()
    return timer


def collect_and_exit(code: int = 1) -> None:
    gc.collect(2)
    os._exit(code)


def hidden_popen(argv: Iterable[Any], creationflags: int | None = None) -> subprocess.Popen:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if creationflags is None else creationflags
    return subprocess.Popen(
        list(argv),
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=flags,
    )


def load_callable(full_name: str, attr_name: str) -> Callable[..., Any] | None:
    func = load_attr(full_name, attr_name)
    return func if callable(func) else None
