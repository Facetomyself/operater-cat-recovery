#!/usr/bin/env python3
"""Offline protocol lab for the recovered operater-cat tree.

This script is intentionally standalone.  It does not modify the recovered
source tree, does not touch the network, and never starts the target binary.
Synthetic responses only exercise the recovered parsing/state-transition code.
"""
from __future__ import annotations

import asyncio
import json
import socket
import sys
from contextlib import ExitStack
from pathlib import Path
from typing import Any


LAB_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LAB_DIR.parent
RECOVERED_DIR = PROJECT_DIR / "recovered_src"
FIXTURES = LAB_DIR / "fixtures" / "synthetic_responses.json"
OUTPUT = LAB_DIR / "run-output.json"

if str(RECOVERED_DIR) not in sys.path:
    sys.path.insert(0, str(RECOVERED_DIR))


def _jsonable(value: Any) -> Any:
    if isinstance(value, bytes):
        return {"hex": value.hex()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "__dict__"):
        return _jsonable(vars(value))
    return value


def _patch(stack: ExitStack, owner: object, name: str, value: Any) -> None:
    original = getattr(owner, name)
    stack.callback(setattr, owner, name, original)
    setattr(owner, name, value)


def _network_disabled(*args: Any, **kwargs: Any) -> Any:
    raise RuntimeError("offline lab: network access is disabled")


def main() -> int:
    from src.py.com.yun.mao.sanitized import neutralize

    neutralize.apply()

    import aiohttp
    from src.py.com.yun.mao.dclass import ItemMemStore, LoadDataClass
    from src.py.com.yun.mao.fea import (
        _sq_chk,
        _sq_jqm,
        _sq_r_bao,
        _sq_r_ca,
        _sq_r_qi,
        _sq_req,
    )
    from src.py.com.yun.mao.fea._r_hb_file import RemoteHb
    from src.py.com.yun.mao.link import _sjk_cli

    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    result: dict[str, Any] = {
        "lab": "offline-synthetic-only",
        "network": "disabled-by-stub",
        "sanitized": "applied",
        "fixtures": str(FIXTURES.relative_to(LAB_DIR)),
    }

    with ExitStack() as stack:
        _patch(stack, socket, "create_connection", _network_disabled)
        _patch(stack, aiohttp, "ClientSession", _network_disabled)

        # 1. Bootstrap response.  The real transport is replaced by a synthetic
        #    response; the client-side validation and state transition still run.
        bootstrap_calls: list[dict[str, Any]] = []

        async def fake_bootstrap_post(*args: Any, **kwargs: Any):
            bootstrap_calls.append(
                {
                    "args": [str(arg) for arg in args],
                    "kwargs": _jsonable(kwargs),
                }
            )
            return fixtures["bootstrap"], False

        _patch(
            stack,
            _sjk_cli.SjkCli,
            "_sjk_post_once",
            staticmethod(fake_bootstrap_post),
        )
        bootstrap_ok = asyncio.run(
            _sjk_cli.SjkCli.sjk_lq_qd(
                url="https://lab.invalid/xb/iil",
                public_key="LAB-PUBLIC-KEY-NOT-REAL",
                ssl_verify=False,
            )
        )
        result["bootstrap"] = {
            "result": bootstrap_ok,
            "responses": bootstrap_calls,
        }

        # 2. Heartbeat and account report parsing.  `qd_r_spi_boot` is synchronous
        #    in the recovered tree, so the async fetch is replaced by a sync stub.
        heartbeat_calls: dict[str, Any] = {}
        original_hy_jx_bc = _sq_chk.hy_jx_bc
        try:
            original_hy_jx_bc(fixtures["heartbeat"]["data"])
            heartbeat_calls["hy_jx_bc_contract"] = {"direct_inner_error": None}
        except Exception as exc:
            heartbeat_calls["hy_jx_bc_contract"] = {
                "direct_inner_error": f"{type(exc).__name__}: {exc}",
                "expected_input": "envelope containing a top-level 'data' key",
            }

        # The recovered `_apply_user_from_remote` unwraps the envelope before
        # calling `hy_jx_bc`, while `hy_jx_bc` expects the envelope again.
        # This shim is lab-only and is documented as a recovered-code defect.
        def hy_jx_bc_shim(oj: dict):
            normalized = oj if "data" in oj else {"data": oj}
            return original_hy_jx_bc(normalized)

        def fake_spi_fetch(ucode: str):
            heartbeat_calls["ucode"] = ucode
            heartbeat_calls["request_body"] = json.loads(
                _sq_r_bao.zq_r_item_hb(ucode, include_item=False)
            )
            return RemoteHb.success(fixtures["heartbeat"])

        def fake_bootstrap_item_memory(
            is_register: bool,
            cloud_empty: bool,
            cloud_encoding: str,
            cloud_payload_b64: str,
        ) -> str:
            heartbeat_calls["bootstrap_args"] = {
                "is_register": is_register,
                "cloud_empty": cloud_empty,
                "cloud_encoding": cloud_encoding,
                "cloud_payload_b64": cloud_payload_b64,
            }
            return "cloud_empty_no_local"

        login_calls: list[str] = []

        def fake_login(ucode: str, *args: Any, **kwargs: Any) -> bool:
            login_calls.append(ucode)
            return True

        _patch(stack, _sq_r_qi, "_spi_fetch", fake_spi_fetch)
        _patch(stack, _sq_chk, "hy_jx_bc", hy_jx_bc_shim)
        _patch(
            stack,
            ItemMemStore,
            "bootstrap_item_memory",
            fake_bootstrap_item_memory,
        )
        _patch(
            stack,
            LoadDataClass,
            "getAutoMap",
            lambda: {"lab-auto-a": object(), "lab-auto-b": object()},
        )
        _patch(stack, _sq_req, "sq_jy_ma", fake_login)
        _patch(
            stack,
            _sq_jqm,
            "current_account_info",
            _sq_jqm.SqJqm(ucode="LAB-UCODE", mul=True),
        )

        # `_sq_qi` imports PyQt5 at module import time.  The lab avoids the UI
        # wrapper and reproduces the non-UI body of `s_b_i_kaishi()`.
        def startup_sequence():
            boot = _sq_r_qi.qd_r_spi_boot()
            if boot is not None:
                return boot
            ucode = _sq_jqm.current_account_info.ucode
            if not ucode:
                return None
            return _sq_req.sq_jy_ma(ucode, callback_need_await=True)

        startup_result = startup_sequence()
        account = _sq_jqm.current_account_info.zh_ye_xx()
        result["heartbeat"] = {
            "startup_result": startup_result,
            "hy_jx_bc_contract": heartbeat_calls.get("hy_jx_bc_contract"),
            "request": heartbeat_calls.get("request_body"),
            "bootstrap_args": heartbeat_calls.get("bootstrap_args"),
            "login_ucodes": login_calls,
            "account_after": _jsonable(account),
        }

        # 3. Batch conversion response.  The ordered items are supplied by the
        #    fixture; `q_m3_seal` is recorded to show the post-processing point.
        convert_calls: dict[str, Any] = {}

        async def run_convert():
            def fake_build_convert_items(beans: list[Any]) -> list[dict[str, Any]]:
                convert_calls["bean_count"] = len(beans)
                return [{"kid": "kid-lab-1", "source": "lab"}]

            def fake_sq_r_ca(body: str):
                convert_calls["request_body"] = json.loads(body)
                return True, fixtures["convert"], b"LAB-PROOF"

            def fake_seal(items: list[Any]) -> None:
                convert_calls["sealed_items"] = _jsonable(items)

            _patch(
                stack,
                _sq_r_ca,
                "build_convert_items",
                fake_build_convert_items,
            )
            _patch(stack, _sq_r_ca._sq_r_req, "sq_r_ca", fake_sq_r_ca)
            _patch(stack, _sq_r_ca, "q_m3_seal", fake_seal)
            _patch(
                stack,
                _sq_jqm,
                "current_account_info",
                _sq_jqm.SqJqm(ucode="LAB-UCODE", mul=True),
            )
            return await _sq_r_ca.convert_batch_with_retry(
                "convert",
                [object()],
            )

        converted = asyncio.run(run_convert())
        result["convert"] = {
            "request": convert_calls.get("request_body"),
            "sealed_items": convert_calls.get("sealed_items"),
            "result": _jsonable(converted),
        }

        neutralize.restore()

    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
