# Recovered module: src.py.com.yun.mao.link._fds_h_x
# Behavioural reconstruction from Nuitka metadata, Hex-Rays output, and
# the decoded anti-debug catalogs. It is not byte-for-byte original source.
from __future__ import annotations

import ctypes
import random
import threading
import time
from pathlib import PureWindowsPath

import psutil

from . import _fds_jm, _fds_sj


_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_user32 = ctypes.WinDLL("user32", use_last_error=True)


class FdsHhx:
    """Anti-debug probe and response controller."""

    PROC_NAME_CACHE_TTL_SEC = 8.0
    BT_NEG_CACHE_TTL_SEC = 1.0
    DEEP_SCAN_MIN_INTERVAL_SEC = 300.0
    STARTUP_PROBE_WAIT_SEC = 5.0
    CONT_FAST_SCAN_MIN_SEC = 10.0
    CONT_FAST_SCAN_MAX_SEC = 12.0
    CONT_FULL_SCAN_MIN_SEC = 18.0
    CONT_FULL_SCAN_MAX_SEC = 180.0

    def __init__(self) -> None:
        self._scan_cache_lock = threading.Lock()
        self._deep_scan_lock = threading.Lock()
        self._ab_lock = threading.Lock()
        self._ab_invoked = False
        self._ab_inflight = False
        self._probe_loaded = False
        self._continuous_lock = threading.Lock()
        self._continuous_started = False
        self._startup_event = threading.Event()

        self._proc_names_cache: set[str] = set()
        self._proc_names_cache_mono = 0.0
        self._proc_cache_gen = 0
        self._bt_neg_cache_valid = False
        self._bt_neg_cache_mono = 0.0
        self._last_deep_scan_mono = 0.0
        self._sj_xc_mz = 0.0

        self._suspicious_stems = set(
            _fds_jm.decode_str_tuple(_fds_sj.STEMS_ENC, _fds_sj.KEY)
        )
        self._suspicious_prefixes = set(
            _fds_jm.decode_str_tuple(_fds_sj.PREFIXES_ENC, _fds_sj.KEY)
        )
        self._module_stems = set(
            _fds_jm.decode_str_tuple(_fds_sj.MODULE_STEMS_ENC, _fds_sj.KEY)
        )
        self._window_keywords = set(
            _fds_jm.decode_str_tuple(_fds_sj.WINDOW_KEYWORDS_ENC, _fds_sj.KEY)
        )

    def _sj_xc_mz(self) -> float:
        return time.perf_counter()

    def _fd_log_msg(self, template: str, **fields: object) -> str:
        text = _fds_jm.sec(template)
        try:
            return text.format(**fields)
        except (KeyError, ValueError):
            return text

    def _fd_log(self, level: str, template: str, **fields: object) -> None:
        print(f"[{level}] {self._fd_log_msg(template, **fields)}")

    def _jk_jz_biao(self) -> bool:
        is_debugged = bool(_kernel32.IsDebuggerPresent())
        remote = ctypes.c_int(0)
        current = _kernel32.GetCurrentProcess()
        try:
            remote_ok = bool(
                _kernel32.CheckRemoteDebuggerPresent(
                    ctypes.c_void_p(current), ctypes.byref(remote)
                )
            )
        except Exception:
            remote_ok = False
        self._fd_log("RA", "fd_log_RA", value=int(is_debugged))
        self._fd_log(
            "RB", "fd_log_RB", value=int(remote_ok and bool(remote.value))
        )
        return is_debugged or (remote_ok and bool(remote.value))

    def jk_bd_api(self) -> bool:
        return self._jk_jz_biao()

    def jk_yc_ts(self) -> float:
        return self._sj_xc_mz()

    def jk_sx(self) -> bool:
        return self._jk_jz_biao()

    def _jcm_xx_jq(self, proc_name: str) -> str | None:
        name = (proc_name or "").lower()
        for stem in self._suspicious_stems:
            if stem and stem in name:
                return stem
        for prefix in self._suspicious_prefixes:
            if prefix and name.startswith(prefix):
                return prefix
        return None

    def _wj_mz_stem(self, path: str) -> str:
        try:
            return PureWindowsPath(path).stem.lower()
        except Exception:
            return ""

    def _invalidate_scan_caches(self) -> None:
        with self._scan_cache_lock:
            self._proc_cache_gen += 1
            self._bt_neg_cache_valid = False

    def _cached_proc_names(self, force: bool = False) -> set[str]:
        now = time.monotonic()
        with self._scan_cache_lock:
            fresh = (
                now - self._proc_names_cache_mono
                < self.PROC_NAME_CACHE_TTL_SEC
            )
            if not force and fresh:
                return set(self._proc_names_cache)
        names: set[str] = set()
        for proc in psutil.process_iter(["name"]):
            try:
                name = (proc.info.get("name") or "").lower()
                if name:
                    names.add(name)
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue
        with self._scan_cache_lock:
            self._proc_names_cache = names
            self._proc_names_cache_mono = now
            self._proc_cache_gen += 1
        return names

    def _jk_ky_bt(self, keywords: set[str] | None = None) -> tuple[str, str] | None:
        keywords = keywords or self._window_keywords
        found: list[tuple[str, str]] = []
        enum_proc = ctypes.WINFUNCTYPE(
            ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p
        )

        def _enum_cb(hwnd: int, _lparam: int) -> bool:
            if not _user32.IsWindowVisible(hwnd):
                return True
            length = _user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return True
            buf = ctypes.create_unicode_buffer(length + 1)
            _user32.GetWindowTextW(hwnd, buf, length + 1)
            title = (buf.value or "").strip().lower()
            for keyword in keywords:
                if keyword and keyword in title:
                    found.append((keyword, title))
                    return False
            return True

        try:
            _user32.EnumWindows(enum_proc(_enum_cb), 0)
        except Exception:
            return None
        if not found:
            return None
        keyword, title = found[0]
        self._fd_log("RW", "fd_log_RW", matched_keyword=keyword, title=title)
        return keyword, title

    def _jk_ky_1(self, path: str) -> str | None:
        stem = self._wj_mz_stem(path)
        if not stem:
            return None
        for module_stem in self._module_stems:
            if module_stem and module_stem in stem:
                self._fd_log("RPE", "fd_log_RPE", proc=path, stem=module_stem)
                return module_stem
        return None

    def _jk_ky_mk_1(self, force: bool = False) -> bool:
        now = time.monotonic()
        with self._scan_cache_lock:
            if (
                not force
                and self._bt_neg_cache_valid
                and now - self._bt_neg_cache_mono
                < self.BT_NEG_CACHE_TTL_SEC
            ):
                return False
        hit = self._jk_ky_bt()
        with self._scan_cache_lock:
            self._bt_neg_cache_valid = hit is None
            self._bt_neg_cache_mono = now
        return hit is not None

    def _mark_deep_scan_done(self) -> None:
        with self._deep_scan_lock:
            self._last_deep_scan_mono = time.monotonic()

    def _deep_scan_allowed(self, force: bool = False) -> bool:
        with self._deep_scan_lock:
            if force:
                return True
            return (
                time.monotonic() - self._last_deep_scan_mono
                >= self.DEEP_SCAN_MIN_INTERVAL_SEC
            )

    def jk_ky_jc_fast(self, force: bool = False) -> bool:
        for name in self._cached_proc_names(force=force):
            if self._jcm_xx_jq(name):
                return True
        return self._jk_ky_mk_1(force=force)

    def jk_ky_jc_mk_all(self) -> bool:
        return self.jk_ky_jc_fast(force=True)

    def jk_ky_jc_deep(self, force: bool = False) -> bool:
        if not self._deep_scan_allowed(force=force):
            return False
        try:
            for proc in psutil.process_iter(["name", "exe"]):
                try:
                    name = (proc.info.get("name") or "").lower()
                    if self._jcm_xx_jq(name):
                        return True
                    for module in proc.memory_maps() or []:
                        if self._jk_ky_1(getattr(module, "path", "") or ""):
                            return True
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue
        finally:
            self._mark_deep_scan_done()
        return False

    def jk_ky_jc(self, force: bool = False) -> bool:
        return self.jk_ky_jc_fast(force=force) or self.jk_ky_jc_deep(force=force)

    def entry_blocked(self) -> bool:
        return self._ab_invoked or self._probe_loaded

    def try_begin_abort(self) -> bool:
        with self._ab_lock:
            if self._ab_inflight:
                return False
            self._ab_inflight = True
            self._ab_invoked = True
            return True

    def seal_abort(self) -> None:
        with self._ab_lock:
            self._ab_inflight = False
        self._fd_log("GD_QUAN", "fd_log_GD_QUAN")

    def fh_lx_sd(self) -> None:
        self._fd_log("QB", "fd_log_QB")

    def fh_qing(self) -> None:
        self._fd_log("GD_QING", "fd_log_GD_QING")

    def fh_zhong_fast(self) -> None:
        self._fd_log("GD_ZHONG", "fd_log_GD_ZHONG")

    def fh_zhong(self) -> None:
        self._fd_log("GD_ZHONG", "fd_log_GD_ZHONG")

    def fh_quan(self) -> None:
        self._fd_log("GD_QUAN", "fd_log_GD_QUAN")
        self.try_begin_abort()

    def _async_mid(self, timeout: float) -> None:
        hit = self.jk_ky_jc(force=True)
        if hit:
            self.fh_zhong()
        self._probe_loaded = True
        self._startup_event.set()

    def fh_ui_qd(self) -> None:
        self._startup_event.clear()
        thread = threading.Thread(
            target=self._async_mid,
            args=(self.STARTUP_PROBE_WAIT_SEC,),
            name="_sj_xc_mz",
            daemon=True,
        )
        thread.start()
        self.wait_startup_probe()

    def wait_startup_probe(self, timeout: float = 0.5) -> None:
        self._startup_event.wait(timeout=timeout)

    def _primary_loop(self, min_interval: float, max_interval: float) -> None:
        next_fast = time.monotonic()
        while not self.entry_blocked():
            now = time.monotonic()
            if now >= next_fast:
                if self.jk_ky_jc_fast():
                    self.fh_zhong_fast()
                next_fast = now + random.uniform(min_interval, max_interval)
            time.sleep(max(1.0, next_fast - time.monotonic()))

    def _secondary_loop(self, min_interval: float, max_interval: float) -> None:
        next_full = time.monotonic()
        while not self.entry_blocked():
            now = time.monotonic()
            if now >= next_full:
                if self.jk_ky_jc_deep(force=True):
                    self.fh_quan()
                next_full = now + random.uniform(min_interval, max_interval)
            time.sleep(max(1.0, next_full - time.monotonic()))

    def fh_ht_jk(
        self,
        interval: float = 5.0,
        min_interval: float | None = None,
        max_interval: float | None = None,
    ) -> None:
        with self._continuous_lock:
            if self._continuous_started:
                return
            self._continuous_started = True
        fast_min = max(0.05, float(interval))
        fast_max = fast_min
        full_min = (
            self.CONT_FULL_SCAN_MIN_SEC
            if min_interval is None
            else float(min_interval)
        )
        full_max = (
            self.CONT_FULL_SCAN_MAX_SEC
            if max_interval is None
            else float(max_interval)
        )
        threading.Thread(
            target=self._primary_loop,
            args=(fast_min, fast_max),
            daemon=True,
            name="_primary_loop",
        ).start()
        threading.Thread(
            target=self._secondary_loop,
            args=(full_min, full_max),
            daemon=True,
            name="_secondary_loop",
        ).start()
        self._fd_log("GD_CJ", "fd_log_GD_CJ")

    def jk_qb(self) -> bool:
        checks = (
            self._jk_jz_biao,
            self.jk_ky_jc_fast,
            self.jk_ky_jc_deep,
        )
        for check in checks:
            try:
                if check():
                    return True
            except Exception:
                continue
        return False

    def fh_cj(self) -> bool:
        self._fd_log("CJ", "fd_log_CJ")
        self.fh_ui_qd()
        self.fh_ht_jk()
        roll = random.random()
        if roll < 0.55:
            self.fh_qing()
        elif roll < 0.92:
            self.fh_zhong()
        else:
            self.fh_quan()
        return self.jk_qb()
