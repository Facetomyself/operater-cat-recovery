from __future__ import annotations


def test_seal_roundtrip_and_tamper_rejection():
    from src.py.com.yun.mao.fea import _pl_wd_file

    _pl_wd_file._sk = b"k" * 32
    cap = _pl_wd_file._seal(b"tag", b"proof", b"aux")
    assert cap is not None
    assert _pl_wd_file._unseal(b"tag", cap)

    tampered = cap._replace(mac=cap.mac[:-1] + bytes([cap.mac[-1] ^ 1]))
    assert not _pl_wd_file._unseal(b"tag", tampered)
    assert not _pl_wd_file._unseal(b"other", cap)


def test_state_reset_and_stage_codes():
    from src.py.com.yun.mao.fea import _pl_wd_file

    assert _pl_wd_file.w_cd(False, True, True, True) == 0
    assert _pl_wd_file.w_cd(True, False, True, True) == 2
    assert _pl_wd_file.w_cd(True, True, False, True) == 3
    assert _pl_wd_file.w_cd(True, True, True, False) == 4
    assert _pl_wd_file.w_cd(True, True, True, True) == 9

    _pl_wd_file._sk = b"key"
    _pl_wd_file._ph = b"proof"
    _pl_wd_file._ready = True
    assert _pl_wd_file.b_x1_trim() is None
    assert _pl_wd_file._sk is None
    assert _pl_wd_file._ph == b""
    assert _pl_wd_file._ready is False


def test_b_x1_trim_resets_state_and_returns_none():
    from src.py.com.yun.mao.fea import _pl_wd_file

    _pl_wd_file._sk = b"key"
    _pl_wd_file._ph = b"proof"
    _pl_wd_file._ready = True
    _pl_wd_file._c_p = b"p"
    _pl_wd_file._c_q = b"q"
    _pl_wd_file._c_r = b"r"
    _pl_wd_file._c_s = b"s"
    _pl_wd_file._kid_ring = {b"k": b"v"}

    assert _pl_wd_file.b_x1_trim() is None
    assert _pl_wd_file._sk is None
    assert _pl_wd_file._ph == b""
    assert _pl_wd_file._ready is False
    assert _pl_wd_file._c_p is None
    assert _pl_wd_file._c_q is None
    assert _pl_wd_file._c_r is None
    assert _pl_wd_file._c_s is None
    assert _pl_wd_file._kid_ring == {}
