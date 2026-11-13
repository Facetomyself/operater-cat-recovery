# Shared control-flow primitives for the bz_uc recovery layer.
# Definitions only: WinDLL/Popen/os.system are not invoked at import time.
from __future__ import annotations

import ctypes
import os
import subprocess
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


def hidden_popen(
    command: tuple[str, ...] | list[str] | str,
    *,
    creationflags: int = 0,
) -> subprocess.Popen:
    """Start a hidden child with the DEVNULL/CREATE_NO_WINDOW contract."""
    return subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False,
        creationflags=creationflags | subprocess.CREATE_NO_WINDOW,
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
                # 1300 == ERROR_NOT_ALL_ASSIGNED; other non-zero values are
                # left to the caller's control flow.
                return ctypes.get_last_error() != 1300
        return False
    finally:
        kernel32.CloseHandle(token)


def system_command(command: str) -> int:
    return os.system(command)
