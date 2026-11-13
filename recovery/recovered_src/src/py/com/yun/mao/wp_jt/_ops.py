"""Shared control-flow primitives for the recovered ``wp_jt`` package.

Definitions only.  Importing this module does not start a process, load a
DLL, emit a UI signal, or terminate the interpreter.
"""
from __future__ import annotations

import ctypes
import importlib
import subprocess
from collections.abc import Iterable
from ctypes import wintypes
from typing import Any


class _LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG),
    ]


class _LAA(ctypes.Structure):
    _fields_ = [
        ("Luid", _LUID),
        ("Attributes", wintypes.DWORD),
    ]


class _TP(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", _LAA * 1),
    ]


def _module_name(full_name: str) -> str:
    # The recovered tree keeps the loader-table ``src.py.`` prefix.
    return full_name


def import_module(full_name: str):
    return importlib.import_module(_module_name(full_name))


def load_attr(full_name: str, attr_name: str, default: Any = None) -> Any:
    try:
        return getattr(import_module(full_name), attr_name, default)
    except (ImportError, AttributeError, TypeError):
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


def emit_signal(
    module_name: str,
    signal_obj_name: str,
    signal_name: str,
    *args: Any,
) -> bool:
    signal_obj = load_attr(module_name, signal_obj_name)
    return emit(signal_obj, signal_name, *args)


def decode_abort_parts() -> tuple[str, ...]:
    decoder = load_attr("src.py.com.yun.mao.link._fds_jm", "decode_str_tuple")
    parts_source = load_attr("src.py.com.yun.mao.link", "_fds_sj")
    if decoder is None or parts_source is None:
        return ()
    try:
        return tuple(
            decoder(parts_source.ABORT_PARTS_ENC, parts_source.KEY)
        )
    except (AttributeError, TypeError, ValueError):
        return ()


def hidden_popen(command: Iterable[Any] | str) -> subprocess.Popen:
    """Start the hidden child with the recovered kwargs.

    The target passes ``shell=False`` (the constant pool carries
    ``Py_FalseStruct``), all three ``DEVNULL`` handles and
    ``CREATE_NO_WINDOW``.
    """
    return subprocess.Popen(
        command,
        shell=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def shutdown_native(
    advapi32_name: str,
    kernel32_name: str,
    privilege_name: str,
    api_dll_name: str,
    api_name: str,
    api_args: tuple[Any, ...] = (5, 0),
) -> bool:
    """Enable the shutdown privilege, then call the native shutdown API."""

    if not enable_privileges(advapi32_name, kernel32_name, (privilege_name,)):
        return False
    try:
        api_dll = ctypes.WinDLL(api_dll_name, use_last_error=True)
        api = getattr(api_dll, api_name, None)
        if callable(api):
            return bool(api(*api_args))
    except Exception:
        return False
    return False


def enable_privileges(
    advapi32_name: str,
    kernel32_name: str,
    privilege_names: tuple[str, ...],
) -> bool:
    """Enable the requested privilege for the current process.

    The recovered catalog decodes ``SeShutdownPrivilege``; the tuple form is
    retained so callers can pass additional candidates.
    """
    advapi32 = ctypes.WinDLL(advapi32_name, use_last_error=True)
    kernel32 = ctypes.WinDLL(kernel32_name, use_last_error=True)

    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    advapi32.OpenProcessToken.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.HANDLE),
    ]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.LookupPrivilegeValueW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        ctypes.POINTER(_LUID),
    ]
    advapi32.LookupPrivilegeValueW.restype = wintypes.BOOL
    advapi32.AdjustTokenPrivileges.argtypes = [
        wintypes.HANDLE,
        wintypes.BOOL,
        ctypes.POINTER(_TP),
        wintypes.DWORD,
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    advapi32.AdjustTokenPrivileges.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL

    token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(
        kernel32.GetCurrentProcess(),
        0x0020 | 0x0008,
        ctypes.byref(token),
    ):
        return False

    try:
        for privilege_name in privilege_names:
            luid = _LUID()
            if not advapi32.LookupPrivilegeValueW(
                None,
                privilege_name,
                ctypes.byref(luid),
            ):
                continue

            state = _TP()
            state.PrivilegeCount = 1
            state.Privileges[0].Luid = luid
            state.Privileges[0].Attributes = 0x00000002
            ctypes.set_last_error(0)
            if advapi32.AdjustTokenPrivileges(
                token,
                False,
                ctypes.byref(state),
                0,
                None,
                None,
            ):
                # ERROR_NOT_ALL_ASSIGNED means this candidate was not usable.
                return ctypes.get_last_error() != 1300
        return False
    finally:
        kernel32.CloseHandle(token)
