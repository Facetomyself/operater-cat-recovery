# Recovered module: src.py.com.yun.mao.fea._sq_r_ks
# UI-side remote report tasks: SPI, UI and ROI.
from __future__ import annotations

import asyncio

from PyQt5.QtCore import QRunnable, QThreadPool

from . import _sq_chk, _sq_jqm, _sq_r_bao, _sq_r_qi, _sq_r_req
from ..dclass import ItemMemStore
from ..link._fds_jm import sec
from ..link._fds_rt import fs_by_pf
from ..util import TracePrinterHelper
from ..util.need import signals, utils
from ._pl_wd_file import b_x1_trim
from ._r_hb_file import RemoteHb


_ROI_BIZ_RETRY = 4
_SPUI_BIZ_RETRY = 3
_UI_BIZ_RETRY = 3


def _dispatch_ui_callback(callback, ok: bool) -> None:
    """Invoke the Qt callback on the main thread, with a safe fallback."""

    def _run() -> None:
        try:
            if callback is not None:
                callback(bool(ok))
        except Exception as exc:
            try:
                print(sec("lk_ex_pre_01"), exc)
            except Exception:
                pass

    try:
        signals.global_ui_signal.invoke_on_main_thread.emit(_run)
    except Exception:
        _run()


def _hb_ok(hb: RemoteHb | None) -> bool:
    if hb is None:
        return False
    if isinstance(hb, RemoteHb):
        return (not hb.terminal) and bool(hb.msg == "" or hb.data is not None)
    return bool(hb)


def _as_hb(result) -> RemoteHb | None:
    if result is None:
        return None
    if isinstance(result, RemoteHb):
        return result
    try:
        return _sq_r_qi._coerce_remote_hb(result)
    except Exception:
        return RemoteHb.success(result)


def _snapshot() -> tuple[int, bool, str]:
    """Return ``(dirty_generation, with_item, item_b64)``."""
    try:
        dirty_gen = int(ItemMemStore.get_dirty_generation())
    except Exception:
        dirty_gen = 0
    try:
        with_item = bool(ItemMemStore.is_item_dirty() or dirty_gen)
    except Exception:
        with_item = bool(dirty_gen)
    if not with_item:
        return dirty_gen, False, ""
    try:
        item_b64 = ItemMemStore.dump_snapshot_gzip_b64()
    except Exception:
        item_b64 = ""
    try:
        b_x1_trim()
    except Exception:
        pass
    return dirty_gen, bool(item_b64), item_b64


def _ucode() -> str:
    ucode = getattr(_sq_jqm.current_account_info, "ucode", "") or ""
    try:
        return utils.un_mask_ucode(ucode)
    except Exception:
        return ucode


def _item_body(ucode: str, item_b64: str, include_item: bool) -> str:
    try:
        return _sq_r_bao.zq_r_item_hb(
            ucode,
            item_b64=item_b64,
            include_item=include_item,
        )
    except TypeError:
        try:
            return _sq_r_bao.zq_r_item_hb(
                ucode,
                item_b64,
                include_item,
            )
        except TypeError:
            return _sq_r_bao.zq_r_item_hb(ucode, include_item=include_item)


class KjRSpuiTask(QRunnable):
    """Periodic SPI task used by the UI."""

    def __init__(self, ui_call_back=None):
        super().__init__()
        self.ui_call_back = ui_call_back

    def run(self) -> None:
        try:
            asyncio.run(self._inner())
        except Exception as exc:
            try:
                TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
            except Exception:
                pass
            _dispatch_ui_callback(self.ui_call_back, False)
            _ = exc

    async def _inner(self):
        last_hb = None
        ucode = _ucode()
        dirty_gen, with_item, item_b64 = _snapshot()
        body = _item_body(ucode, item_b64, with_item)
        retries = _SPUI_BIZ_RETRY
        data = report = None
        for attempt in range(retries):
            try:
                last_hb = _as_hb(await _sq_r_req.sq_r_spui(body))
                if last_hb is None:
                    continue
                data = last_hb.data
                if _hb_ok(last_hb):
                    report = data
                    if with_item:
                        ItemMemStore.clear_item_dirty_if_generation(dirty_gen)
                    break
                if last_hb.terminal:
                    break
            except Exception as exc:
                last_hb = RemoteHb.failed_retry(str(exc))
            if attempt + 1 < retries:
                try:
                    await asyncio.sleep(_sq_r_req._R_RETRY_DELAY_SEC)
                except Exception:
                    pass
        _dispatch_ui_callback(self.ui_call_back, _hb_ok(last_hb))
        return report


class KjRUiTask(QRunnable):
    """UI report task that applies the remote account state."""

    def __init__(self, ui_call_back=None):
        super().__init__()
        self.ui_call_back = ui_call_back

    def run(self) -> None:
        try:
            asyncio.run(self._inner())
        except Exception:
            try:
                TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
            except Exception:
                pass
            _dispatch_ui_callback(self.ui_call_back, False)

    async def _inner(self):
        last_hb = None
        try:
            fs_by_pf()
        except Exception:
            pass
        ucode = _ucode()
        dirty_gen, with_item, item_b64 = _snapshot()
        body = _item_body(ucode, item_b64, with_item)
        for attempt in range(_UI_BIZ_RETRY):
            try:
                last_hb = _as_hb(await _sq_r_req.sq_r_ui(body))
                if last_hb is None:
                    continue
                data = last_hb.data if isinstance(last_hb, RemoteHb) else last_hb
                if isinstance(data, dict):
                    ok, _ = _sq_r_qi._apply_user_from_remote(
                        data,
                        _sq_jqm.current_account_info,
                    )
                    if ok:
                        if with_item:
                            ItemMemStore.clear_item_dirty_if_generation(dirty_gen)
                        break
                if getattr(last_hb, "terminal", False):
                    break
            except Exception as exc:
                last_hb = RemoteHb.failed_retry(str(exc))
            if attempt + 1 < _UI_BIZ_RETRY:
                try:
                    await asyncio.sleep(_sq_r_req._R_RETRY_DELAY_SEC)
                except Exception:
                    pass
        _dispatch_ui_callback(self.ui_call_back, _hb_ok(last_hb))
        return last_hb


class KjRRoiTask(QRunnable):
    """ROI/report task."""

    def run(self) -> None:
        try:
            asyncio.run(self._inner())
        except Exception:
            try:
                TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
            except Exception:
                pass

    async def _inner(self):
        last_hb = None
        ucode = _ucode()
        _, with_item, item_b64 = _snapshot()
        body = _item_body(ucode, item_b64, with_item)
        for attempt in range(_ROI_BIZ_RETRY):
            try:
                last_hb = _as_hb(await _sq_r_req.sq_r_roi(body))
                if last_hb is None:
                    continue
                report = last_hb.data
                if isinstance(report, dict):
                    try:
                        parsed = _sq_chk.parse_report(report)
                        if parsed is not None:
                            report = parsed
                    except Exception:
                        pass
                    if report.get("isSuccess") and report.get("itemUpdated"):
                        try:
                            ItemMemStore.clear_item_dirty_if_generation(
                                ItemMemStore.get_dirty_generation()
                            )
                        except Exception:
                            pass
                if _hb_ok(last_hb):
                    break
                if last_hb.terminal:
                    break
            except Exception as exc:
                last_hb = RemoteHb.failed_retry(str(exc))
            if attempt + 1 < _ROI_BIZ_RETRY:
                try:
                    await asyncio.sleep(_sq_r_req._R_RETRY_DELAY_SEC)
                except Exception:
                    pass
        return last_hb


def kj_r_spui(ui_call_back=None):
    task = KjRSpuiTask(ui_call_back)
    QThreadPool.globalInstance().start(task)
    return task


def save_item_r_ui(ui_call_back=None):
    task = KjRUiTask(ui_call_back)
    QThreadPool.globalInstance().start(task)
    return task


def roi_report_fire(report=None, callback=None):
    """Start a ROI task or parse an already supplied report."""
    if report is not None:
        try:
            parsed = _sq_chk.parse_report(report)
            if parsed is not None:
                return parsed
        except Exception:
            pass
    task = KjRRoiTask()
    QThreadPool.globalInstance().start(task)
    if callback is not None:
        callback(bool(report))
    return task
