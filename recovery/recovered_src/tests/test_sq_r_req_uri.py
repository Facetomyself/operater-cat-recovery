from __future__ import annotations

from src.py.com.yun.mao.fea import _sq_r_req


def test_uri_wrappers_preserve_recovered_paths(monkeypatch):
    monkeypatch.setattr(
        _sq_r_req._sq_req,
        "URL_PRE_COM",
        lambda: "https://example.test/",
    )
    cases = (
        (_sq_r_req.sq_uri_r_spi, "r_spi"),
        (_sq_r_req.sq_uri_r_spui, "r_spui"),
        (_sq_r_req.sq_uri_r_ui, "r_ui"),
        (_sq_r_req.sq_uri_r_roi, "r_roi"),
        (_sq_r_req.sq_uri_r_ca, "r_ca"),
    )
    for func, path in cases:
        assert func() == f"https://example.test/{path}"
