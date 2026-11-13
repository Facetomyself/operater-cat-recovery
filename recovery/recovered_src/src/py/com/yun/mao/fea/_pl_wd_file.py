# Recovered module: src.py.com.yun.mao.fea._pl_wd_file
# Static reconstruction from the Nuitka module init, constants chunk,
# function metadata and Hex-Rays bodies.
#
# The module is a local proof/capability ledger.  The private masking helper
# ``_tg`` is confirmed by the genexpr constants; the public properties below
# (hashing, HMAC, 16/32 byte frames and compare_digest verification) are
# directly confirmed by the decompiled code.
from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
import time
from collections import deque
from typing import Dict, List, NamedTuple, Optional


class _Cap(NamedTuple):
    """A sealed proof frame: ``(nonce, proof_hash, mac, aux)``."""

    nonce: bytes
    proof: bytes
    mac: bytes
    aux: bytes


# Module state reconstructed from ``b_x1_trim``.
_g_mz = threading.RLock()
_sk: Optional[bytes] = None
_ph: bytes = b""
_ready: bool = False
_c_p: Optional[bytes] = None
_c_q: Optional[bytes] = None
_c_r: Optional[bytes] = None
_c_s: Optional[bytes] = None
_kid_ring: Dict[bytes, bytes] = {}

_q_fr: deque[float] = deque()
_hg_once: float = 0.0
_last_fail_ts: float = 0.0
_fail_gap: float = 8.0
_purge_after: float = 64116.0
_a_uk: int = 0


def _tg(n: int) -> bytes:
    """Return the private six-byte witness for ``n`` (17 -> 165 -> 255 mix)."""

    value = int(n)
    mixed = bytes((((value * 17) ^ 165) & 255) for _ in range(4))
    return mixed + value.to_bytes(2, "big")


def _shred(proof: bytes) -> Optional[bytes]:
    """Hash a proof buffer; non-buffer input is rejected."""

    if not isinstance(proof, (bytes, bytearray, memoryview)):
        return None
    return hashlib.sha256(bytes(proof)).digest()


def _mac(key: bytes, parts) -> bytes:
    """HMAC-SHA256 over the chunks in ``parts``."""

    signer = hmac.new(key, digestmod=hashlib.sha256)
    if isinstance(parts, (bytes, bytearray, memoryview)):
        parts = (bytes(parts),)
    for part in parts:
        signer.update(bytes(part))
    return signer.digest()


def _kid_key(kid: str) -> bytes:
    return hashlib.sha256((kid or "").encode("utf-8")).digest()


def _kid_mac(kid: str) -> bytes:
    assert _sk is not None
    return _mac(_sk, (_tg(75), _kid_key(kid)))


def _seal(
    tag: bytes,
    proof: bytes,
    aux: bytes,
) -> Optional[_Cap]:
    """Seal a proof frame with a random nonce and HMAC."""

    if _sk is None:
        return None
    sh = _shred(proof)
    if sh is None:
        return None
    nonce = secrets.token_bytes(16)
    mac = _mac(_sk, (tag, nonce, sh, aux))
    return _Cap(nonce=nonce, proof=sh, mac=mac, aux=aux)


def _unseal(tag: bytes, cap: Optional[_Cap]) -> bool:
    """Validate a sealed proof frame and its fixed component lengths."""

    if _sk is None or tag is None or cap is None:
        return False
    try:
        nonce, sh, mac, aux = cap
    except (TypeError, ValueError):
        return False
    if len(nonce) != 16 or len(sh) != 32 or len(mac) != 32:
        return False
    expect = _mac(_sk, (tag, nonce, sh, aux))
    return hmac.compare_digest(expect, mac)


def _purge_locked(now: float) -> None:
    """Drop stale failure timestamps while the caller holds ``_g_mz``."""

    cutoff = now - _purge_after
    while _q_fr and _q_fr[0] < cutoff:
        _q_fr.popleft()


def _bump_suspect_locked(now: float) -> bool:
    """Record one failure and report a repeated-failure condition."""

    _purge_locked(now)
    repeated = bool(_q_fr and now - _q_fr[-1] < _fail_gap)
    _q_fr.append(now)
    return repeated


def m_qv_open(proof: bytes) -> None:
    """Open a new proof slot and cache its digest."""

    global _c_p, _ready
    with _g_mz:
        _c_p = _shred(proof)
        _ready = _c_p is not None


def k_r9_fwd(proof: bytes, cap: Optional[_Cap]) -> None:
    """Forward a proof frame when both the proof and cap are present."""

    global _c_q
    if proof is None or cap is None:
        return
    with _g_mz:
        _c_q = _shred(proof)


def p_w2_sink(proof: bytes, cap: Optional[_Cap]) -> None:
    """Move the current proof frame to the second cache slot."""

    global _c_q, _c_r
    if proof is None or cap is None:
        return
    with _g_mz:
        _c_q, _c_r = _c_r, _shred(proof)


def q_m3_seal(batch_proof: bytes, kids: Optional[List[str]] = None) -> None:
    """Record a batch proof and install per-kid MACs in the ring."""

    global _ph, _c_s
    with _g_mz:
        _c_s = _shred(batch_proof)
        _ph = batch_proof
        if kids:
            for kid in kids:
                try:
                    _kid_ring[_kid_key(str(kid))] = _kid_mac(str(kid))
                except (AssertionError, TypeError, ValueError):
                    continue


def u_n7_pack(proof: bytes, tip: str) -> None:
    """Store the proof tip for the next flush."""

    global _ph, _c_r
    with _g_mz:
        _c_r = _shred(proof)
        _ph = str(tip).encode("utf-8", "surrogatepass")


def b_x1_trim() -> None:
    """Reset the module's proof caches."""

    global _sk, _ph, _ready, _c_p, _c_q, _c_r, _c_s, _kid_ring
    with _g_mz:
        _sk = None
        _ph = b""
        _ready = False
        _c_p = None
        _c_q = None
        _c_r = None
        _c_s = None
        _kid_ring = {}


def w_cd(
    chain_ok: bool,
    kid_ok: bool,
    gy_ok: bool,
    uc_ok: bool = True,
) -> int:
    """Map the first failed proof stage to its numeric status."""

    if not chain_ok:
        return 0
    if not kid_ok:
        return 2
    if not gy_ok:
        return 3
    if not uc_ok:
        return 4
    return 9


def q_lg(
    kind: int,
    reason: int,
    entry: int,
    n: int,
    ph: int,
) -> None:
    """Record a local proof diagnostic.

    The original body prints the diagnostic and updates the suspect counters;
    the textual format is not present in the static constants, so this keeps
    the state transition and leaves formatting to ``print``.
    """

    global _last_fail_ts
    now = time.time()
    with _g_mz:
        _last_fail_ts = now
        repeated = _bump_suspect_locked(now)
    print(kind, reason, entry, n, ph, repeated)
