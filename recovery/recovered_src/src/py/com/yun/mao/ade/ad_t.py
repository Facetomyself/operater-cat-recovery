# Recovered module: src.py.com.yun.mao.ade.ad_t
# AES-GCM file encryption helper reconstructed from the signature/varname
# evidence (Path, sec, AESGCM, key, nonce, ciphertext, enc_path).
from __future__ import annotations

import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from ..link._fds_jm import sec


def ad_t(file: str | os.PathLike[str], dry_run: bool = True) -> bytes | None:
    """Encrypt one file with AES-GCM.

    ``dry_run`` defaults to True in the reconstruction so an accidental import
    or call cannot modify evidence.
    """
    path = Path(file)
    if dry_run:
        return None
    key = bytes.fromhex(sec("a_ke_t_s_4k"))
    plaintext = path.read_bytes()
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
    enc_path = path.with_suffix(path.suffix + ".enc")
    enc_path.write_bytes(nonce + ciphertext)
    return nonce + ciphertext
