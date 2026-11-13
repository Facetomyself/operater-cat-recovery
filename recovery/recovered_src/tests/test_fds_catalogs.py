from __future__ import annotations


def test_detection_catalogs_match_recovered_lengths():
    from src.py.com.yun.mao.link import _fds_sj

    assert len(_fds_sj.STEMS) == 71
    assert len(_fds_sj.PREFIXES) == 9
    assert len(_fds_sj.MODULE_STEMS) == 27
    assert len(_fds_sj.WINDOW_KEYWORDS) == 29


def test_detection_catalogs_keep_representative_entries():
    from src.py.com.yun.mao.link import _fds_sj

    assert "x64dbg" in _fds_sj.STEMS
    assert "reclass.net" in _fds_sj.STEMS
    assert "cheatengine" in _fds_sj.PREFIXES
    assert "idaplg64" in _fds_sj.MODULE_STEMS
    assert "hex-rays" in _fds_sj.WINDOW_KEYWORDS
    assert "charles " in _fds_sj.WINDOW_KEYWORDS


def test_encoded_catalog_aliases_decode_to_the_same_values():
    from src.py.com.yun.mao.link import _fds_jm, _fds_sj

    assert _fds_jm.decode_str_tuple(
        _fds_sj.STEMS_ENC, _fds_sj.KEY
    ) == _fds_sj.STEMS
    assert _fds_jm.decode_str_tuple(
        _fds_sj.PREFIXES_ENC, _fds_sj.KEY
    ) == _fds_sj.PREFIXES
    assert _fds_jm.decode_str_tuple(
        _fds_sj.MODULE_STEMS_ENC, _fds_sj.KEY
    ) == _fds_sj.MODULE_STEMS
    assert _fds_jm.decode_str_tuple(
        _fds_sj.WINDOW_KEYWORDS_ENC, _fds_sj.KEY
    ) == _fds_sj.WINDOW_KEYWORDS
