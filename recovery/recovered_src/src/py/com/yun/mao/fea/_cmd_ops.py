"""Shared, side-effect-free helpers for the recovered ``fea`` gate modules.

Importing this module only defines classes and functions.  DLL loading,
process creation, timers, exits, and target callbacks stay inside function
bodies.
"""
from __future__ import annotations

import ctypes
import importlib
import subprocess
from ctypes import wintypes
from typing import Any, Iterable, Sequence


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


def module_name(full_name: str) -> str:
    # The recovered tree keeps the loader-table ``src.py.`` prefix.
    return full_name


def load_attr(full_name: str, attr_name: str, default: Any = None) -> Any:
    """Resolve one application attribute lazily.

    The recovered modules are imported in isolation during static checks, so
    a missing optional dependency must not break the module import.
    """

    try:
        module = importlib.import_module(module_name(full_name))
        return getattr(module, attr_name, default)
    except Exception:
        return default


def call_attr(
    full_name: str,
    attr_name: str,
    *args: Any,
    **kwargs: Any,
) -> Any:
    func = load_attr(full_name, attr_name)
    if not callable(func):
        return None
    return func(*args, **kwargs)


def optional_call(target: Any, names: Sequence[str], *args: Any) -> Any:
    """Call the first available method from ``names``.

    Inferred: the proof gates use tolerant duck-typed hook names because the
    original caller objects are reconstructed UI/worker adapters.
    """

    if target is None:
        return None
    for name in names:
        func = getattr(target, name, None)
        if callable(func):
            return func(*args)
    return None


def reorder(values: Iterable[Any], order: Sequence[int]) -> tuple[Any, ...]:
    items = tuple(values)
    return tuple(items[index] for index in order if 0 <= index < len(items))


def mix32(
    value: int,
    multiplier: int,
    increment: int,
    shift: int,
    xor_value: int = 0,
) -> int:
    """Deterministic 32-bit mixer used by the recovered noise helpers.

    Inferred: the four arithmetic constants are confirmed by the module
    constant pool; the exact grouping is reconstructed from the 32-bit mask
    and shift/xor slots.  The per-module ``_noise`` functions carry the
    decompiled formulas; this helper is only a compatibility abstraction.
    """

    mixed = (int(value) * int(multiplier) + int(increment)) & 0xFFFFFFFF
    mixed ^= int(value) >> (int(shift) & 31)
    return (mixed ^ int(xor_value)) & 0xFFFFFFFF


def hidden_popen(
    command: Iterable[Any] | str,
    *,
    shell: bool = False,
    creationflags: int | None = None,
    module: Any = None,
) -> subprocess.Popen:
    """Start a hidden child with the three ``DEVNULL`` handles.

    This helper is defined but never called at import time.  Target modules
    keep their own explicit ``Popen`` call sites when the evidence records
    per-module branches.
    """

    backend = module or subprocess
    flags = (
        getattr(backend, "CREATE_NO_WINDOW", 0)
        if creationflags is None
        else creationflags
    )
    return backend.Popen(
        command,
        shell=shell,
        stdin=backend.DEVNULL,
        stdout=backend.DEVNULL,
        stderr=backend.DEVNULL,
        creationflags=flags,
    )


def enable_privileges(
    advapi32_name: str,
    kernel32_name: str,
    privilege_names: Sequence[str],
) -> bool:
    """Enable the first usable token privilege for the current process.

    Inferred: the native call sequence is confirmed by the module constant
    pool.  Only one successful ``LookupPrivilegeValueW`` /
    ``AdjustTokenPrivileges`` pair is observable in the decompiled body.
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
        40,
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
            state.Privileges[0].Attributes = 2
            ctypes.set_last_error(0)
            if advapi32.AdjustTokenPrivileges(
                token,
                False,
                ctypes.byref(state),
                0,
                None,
                None,
            ):
                return ctypes.get_last_error() != 1300
        return False
    finally:
        kernel32.CloseHandle(token)
