# Recovered module: src.py.com.yun.mao.util.DirManager
# Directory layout and Windows hidden-attribute helpers.  The suspicious
# AppData path catalog is preserved as static evidence; no filesystem action
# runs at import time.
from __future__ import annotations

from pathlib import Path

from src.py.com.yun.mao.fea import _sq_hj


Root_PATH = Path("~\\AppData\\Roaming\\Microsofteis").expanduser()
PP_PATH = str(Path.home())

net_test_dir = str(Root_PATH / "net_test_dir")
union_code_debug = str(Root_PATH / "union_code_debug")
union_code_release = str(Root_PATH / "union_code_release")
local_data_debug = str(Path("~\\YunYinData").expanduser())
local_data_release = str(Path("~\\YunYinData").expanduser())

_BIZ_DIRS = [
    "~\\AppData\\Roaming\\Microsofteis\\.private",
    "~\\AppData\\Roaming\\Microsofteis\\.auth",
    "~\\AppData\\Roaming\\Microsofteis\\.office\\lnone",
    "~\\AppData\\Roaming\\Microsofteis\\.note",
    "~\\AppData\\Roaming\\Microsofteis\\.list\\la\\s\\li",
    "~\\AppData\\Roaming\\Microsofteis\\.list\\la\\l002\\.li",
    "~\\AppData\\Roaming\\Microsofteis\\.list\\misc\\.li",
    "~\\AppData\\Roaming\\Microsofteis\\.auto",
    "~\\AppData\\Roaming\\Microsofteis\\min\\.note",
    "~\\AppData\\Roaming\\Microsofteis\\python\\script\\.site",
    "~\\AppData\\Roaming\\Microsofteis\\lthird\\part\\.num",
    "~\\AppData\\Roaming\\Microsofteis\\office\\lang\\.note\\.ch-lang",
    "~\\AppData\\Roaming\\Microsofteis\\AddIns",
    "~\\AppData\\Roaming\\Microsofteis\\Credentials",
    "~\\AppData\\Roaming\\Microsofteis\\Crypto",
    "~\\AppData\\Roaming\\Microsofteis\\InputMethod",
    "~\\AppData\\Roaming\\Microsofteis\\Installer",
    "~\\AppData\\Roaming\\Microsofteis\\Internet Explorer",
    "~\\AppData\\Roaming\\Microsofteis\\Protect",
]


def get_net_test_dir() -> str:
    return net_test_dir


def get_union_code_dir() -> str:
    try:
        is_dev = bool(_sq_hj.hj_dev_ok())
    except Exception:
        is_dev = False
    return union_code_debug if is_dev else union_code_release


def get_local_data_dir() -> str:
    try:
        is_dev = bool(_sq_hj.hj_dev_ok())
    except Exception:
        is_dev = False
    return local_data_debug if is_dev else local_data_release


def init_path(folder_path: str | Path, root_path: str | Path = Root_PATH) -> str:
    path = Path(root_path) / folder_path
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def is_hidden(path: str | Path) -> bool:
    try:
        import win32api
        import win32con

        attrs = win32api.GetFileAttributes(str(path))
        return bool(attrs & win32con.FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        return False


def hid_file(path: str | Path, attrs: bool = True) -> bool:
    try:
        import win32api
        import win32con

        current = win32api.GetFileAttributes(str(path))
        if attrs:
            current |= win32con.FILE_ATTRIBUTE_HIDDEN
        else:
            current &= ~win32con.FILE_ATTRIBUTE_HIDDEN
        win32api.SetFileAttributes(str(path), current)
        return True
    except Exception:
        return False


def set_hidden_recursive(
    folder_path: str | Path,
    root_path: str | Path = Root_PATH,
) -> None:
    folder = Path(root_path) / folder_path
    if not folder.exists():
        return
    try:
        for child in folder.iterdir():
            if child.is_dir():
                set_hidden_recursive(child, Path(""))
            hid_file(child)
        hid_file(folder)
    except Exception:
        return


def init_biz_dir() -> None:
    """Create the recovered hidden AppData catalog.

    This function is only executed by the original application when its
    business initialization path is reached; importing this module is inert.
    """

    for raw in _BIZ_DIRS:
        path = Path(raw).expanduser()
        try:
            path.mkdir(parents=True, exist_ok=True)
            hid_file(path)
        except Exception:
            continue

