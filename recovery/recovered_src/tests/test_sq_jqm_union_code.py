from __future__ import annotations


from src.py.com.yun.mao.fea import _sq_jqm


class _FakeCipher:
    prefix = b"ENC:"

    def encrypt(self, payload: bytes) -> bytes:
        return self.prefix + payload

    def decrypt(self, payload: bytes) -> bytes:
        if not payload.startswith(self.prefix):
            raise ValueError("bad payload")
        return payload[len(self.prefix) :]


def test_union_code_round_trip(tmp_path, monkeypatch):
    code_path = tmp_path / ".code"
    old_path = tmp_path / ".code.old"
    monkeypatch.setattr(_sq_jqm, "zh_code_pth", lambda: code_path)
    monkeypatch.setattr(_sq_jqm, "zh_old_pth", lambda: old_path)
    monkeypatch.setattr(_sq_jqm, "_static_cipher", lambda: _FakeCipher())
    monkeypatch.setattr(_sq_jqm, "current_account_info", _sq_jqm.SqJqm())

    _sq_jqm._zh_bc_uc("ucode-1", True)
    assert code_path.exists()
    ucode, mul = _sq_jqm._zh_rd_code(code_path)
    assert ucode == "ucode-1"
    assert mul is True
    assert _sq_jqm.zh_rd_code() == "ucode-1"


def test_legacy_union_code_read_and_migration(tmp_path, monkeypatch):
    code_path = tmp_path / ".code"
    old_path = tmp_path / ".code.old"
    monkeypatch.setattr(_sq_jqm, "zh_code_pth", lambda: code_path)
    monkeypatch.setattr(_sq_jqm, "zh_old_pth", lambda: old_path)
    monkeypatch.setattr(_sq_jqm, "_static_cipher", lambda: _FakeCipher())
    monkeypatch.setattr(_sq_jqm, "current_account_info", _sq_jqm.SqJqm())

    old_path.write_bytes(
        _FakeCipher().encrypt(b'{"ucode":"legacy","muli":1}')
    )
    assert _sq_jqm._read_ucode_from_legacy_bean() == "legacy"
    _sq_jqm._migrate_legacy_bean_if_needed()
    assert code_path.exists()
    assert _sq_jqm.zh_rd_code() == "legacy"


def test_zh_jz_xx_reads_and_updates_current_account(tmp_path, monkeypatch):
    code_path = tmp_path / ".code"
    monkeypatch.setattr(_sq_jqm, "zh_code_pth", lambda: code_path)
    monkeypatch.setattr(_sq_jqm, "zh_old_pth", lambda: tmp_path / ".code.old")
    monkeypatch.setattr(_sq_jqm, "_static_cipher", lambda: _FakeCipher())
    monkeypatch.setattr(_sq_jqm, "current_account_info", _sq_jqm.SqJqm())

    _sq_jqm._zh_bc_uc("ucode-2", True)
    _sq_jqm.zh_jz_xx()

    assert _sq_jqm.current_account_info.ucode == "ucode-2"
    assert _sq_jqm.current_account_info.mul is True


def test_zh_sc_wj_writes_current_account(tmp_path, monkeypatch):
    code_path = tmp_path / ".code"
    monkeypatch.setattr(_sq_jqm, "zh_code_pth", lambda: code_path)
    monkeypatch.setattr(_sq_jqm, "zh_old_pth", lambda: tmp_path / ".code.old")
    monkeypatch.setattr(_sq_jqm, "_static_cipher", lambda: _FakeCipher())
    monkeypatch.setattr(
        _sq_jqm,
        "current_account_info",
        _sq_jqm.SqJqm(ucode="ucode-3", mul=True),
    )

    _sq_jqm.zh_sc_wj()

    assert code_path.exists()
    assert _sq_jqm.zh_rd_code() == "ucode-3"


def test_zh_zw_uc_passthrough():
    assert _sq_jqm.zh_zw_uc("ucode-4") == "ucode-4"
