# Recovered module: src.py.com.yun.mao.link._sjk_cli
# License bootstrap client.  The transport methods are reconstructed for
# analysis and are not invoked by the recovery pipeline.
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import aiohttp

from ._fds_jm import sec
from ._fds_tan import wb_sjk_hb
from ._sjk_bao import sjk_zz_hb
from ._tw_ctx import TwCtx


_HTTP_TIMEOUT_SEC = 120
_BOOTSTRAP_CONNECT_TIMEOUT_SEC = 30
_BOOTSTRAP_MAX_RETRY = 4
_BOOTSTRAP_RETRY_BASE_DELAY_SEC = 1.5
_RETRYABLE_HTTP_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})
_EXE_HASH_CACHE = "101db38faad3ba89f99a69ee3be2f45334332520a2a813a5e69caaa2d3d68ae0"


@dataclass
class SjkBr:
    lg: str = ""
    rk: str = ""


class SjkCli:
    _running_exe_path_cache: str | None = None

    @classmethod
    def _sjk_pkg_rt(cls) -> bool:
        return bool(
            getattr(sys, "frozen", False)
            or getattr(sys, "compiled", False)
            or hasattr(sys.modules.get("__main__"), "__compiled__")
        )

    @classmethod
    def _running_exe_path(cls) -> Path:
        if cls._running_exe_path_cache:
            return Path(cls._running_exe_path_cache)
        path = Path(sys.executable).resolve()
        cls._running_exe_path_cache = str(path)
        return path

    @classmethod
    def _resolve_version(cls) -> str:
        try:
            from src.py.version_code import version_code

            return str(version_code)
        except Exception:
            return "0"

    @classmethod
    def _current_exe_path(cls) -> Path:
        if cls._sjk_pkg_rt():
            return cls._running_exe_path()
        return Path(sys.argv[0]).resolve()

    @classmethod
    def _sha256_file(cls, file_path: str | Path, chunk_size: int = 8192) -> str:
        try:
            digest = hashlib.sha256()
            with open(file_path, "rb") as handle:
                for chunk in iter(lambda: handle.read(chunk_size), b""):
                    digest.update(chunk)
            return digest.hexdigest()
        except Exception as exc:
            print(sec("lk_hash_fail_tpl_02").format(e=exc))
            return ""

    @classmethod
    def _sjk_exe_hx(cls) -> str:
        if _EXE_HASH_CACHE:
            return _EXE_HASH_CACHE
        return cls._sha256_file(cls._current_exe_path())

    @classmethod
    def _sjk_validate_url(cls, url: str, dev: bool = False) -> bool:
        try:
            parsed = urlparse(str(url or ""))
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                return False
            if not dev and parsed.scheme != "https":
                return False
            return True
        except Exception:
            return False

    @classmethod
    def _sjk_validate_rk(cls, root_key: str) -> bool:
        if not root_key:
            return False
        try:
            TwCtx.tw_yy_mk(root_key)
            return bool(TwCtx.tw_hq_rk())
        except Exception:
            return False

    @classmethod
    def _sjk_validate_rk_only(cls, body: dict) -> bool:
        try:
            return cls._sjk_validate_rk(str(body.get("rk", "")))
        except Exception:
            return False

    @classmethod
    def _sjk_db_qq(cls, public_key: str, json_content: str):
        """Wrap the JSON body with the recovered AES/RSA envelope primitives."""
        try:
            from ..jm._my_util import aes_encrypt, rsa_encrypt_key

            dy_aes_key = os.urandom(16)
            ciphertext = aes_encrypt(json_content.encode("utf-8"), dy_aes_key)
            encrypted_aes_key = rsa_encrypt_key(
                public_key.encode("utf-8")
                if isinstance(public_key, str)
                else public_key,
                dy_aes_key,
            )
            return {
                "v1c": ciphertext.hex() if isinstance(ciphertext, bytes) else str(ciphertext),
                "v2k": encrypted_aes_key.hex()
                if isinstance(encrypted_aes_key, bytes)
                else str(encrypted_aes_key),
            }, dy_aes_key
        except Exception:
            return None, b""

    @classmethod
    def _sjk_jb_xy(cls, response_hex: str, sign_hex: str, dy_aes_key: bytes):
        try:
            from ..jm._my_util import aes_decrypt, jm_yq_qm

            response_bytes = bytes.fromhex(response_hex)
            sign_bytes = bytes.fromhex(sign_hex)
            verified = jm_yq_qm(response_bytes, sign_bytes)
            if verified is False:
                return None
            content_json = aes_decrypt(response_bytes, dy_aes_key)
            if isinstance(content_json, bytes):
                content_json = content_json.decode("utf-8")
            return json.loads(content_json)
        except Exception:
            return None

    @classmethod
    async def _sjk_post_once(
        cls,
        url: str,
        public_key: str,
        version: str,
        exe_hash: str,
        ssl_verify: bool = True,
    ):
        payload, dy_aes_key = cls._sjk_db_qq(
            public_key,
            sjk_zz_hb(version, exe_hash),
        )
        if payload is None:
            return None, None
        headers = {"Content-Type": "application/json"}
        timeout = aiohttp.ClientTimeout(
            total=_HTTP_TIMEOUT_SEC,
            connect=_BOOTSTRAP_CONNECT_TIMEOUT_SEC,
        )
        connector = aiohttp.TCPConnector(ssl=ssl_verify)
        try:
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
            ) as session:
                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status in _RETRYABLE_HTTP_STATUS:
                        return None, True
                    if resp.status != 200:
                        return None, False
                    outer = await resp.json(content_type=None)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None, True
        try:
            if not outer.get("isSuccess"):
                return None, False
            data = outer.get("data", {})
            response_hex = data.get("response", "")
            sign_hex = data.get("sign", "")
            inner = cls._sjk_jb_xy(response_hex, sign_hex, dy_aes_key)
            if inner is None:
                return None, False
            return inner, False
        except Exception:
            return None, False

    @classmethod
    async def sjk_lq_qd(
        cls,
        url: str | None = None,
        public_key: str | None = None,
        ssl_verify: bool = True,
    ) -> bool:
        """Bootstrap the license endpoint and validate the response."""
        try:
            if url is None:
                url = TwCtx.tw_sjk_url()
            if public_key is None:
                public_key = TwCtx.tw_sjk_pk_pem()
            if not cls._sjk_validate_url(url):
                return False
            version = cls._resolve_version()
            exe_hash = cls._sjk_exe_hx()
            last_retryable = False
            for attempt in range(_BOOTSTRAP_MAX_RETRY):
                result, retryable = await cls._sjk_post_once(
                    url,
                    public_key,
                    version,
                    exe_hash,
                    ssl_verify,
                )
                if result is not None:
                    return bool(result.get("isSuccess", True))
                last_retryable = retryable
                if not retryable:
                    break
                if attempt + 1 < _BOOTSTRAP_MAX_RETRY:
                    await asyncio.sleep(
                        _BOOTSTRAP_RETRY_BASE_DELAY_SEC * (attempt + 1)
                    )
            _ = last_retryable
            return False
        except Exception:
            return False

    @classmethod
    async def sjk_qd(cls, *args, **kwargs) -> bool:
        """Run the license/bootstrap path with the recovered endpoints."""
        try:
            if not await cls.sjk_lq_qd(*args, **kwargs):
                return False
            try:
                wb_sjk_hb()
            except Exception:
                pass
            try:
                from ._fds_rt import fs_sjk_ws

                result = fs_sjk_ws()
                if asyncio.iscoroutine(result):
                    result = await result
                return bool(result)
            except Exception:
                return True
        except Exception:
            return False


def sjk_qd_tb(*args, **kwargs) -> bool:
    """Synchronous launcher for the license bootstrap task."""
    return bool(asyncio.run(SjkCli.sjk_qd(*args, **kwargs)))
