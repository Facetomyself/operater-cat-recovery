from __future__ import annotations


def test_commoncode_exposes_filter_and_replace_helpers():
    from src.py.com.yun.mao.util.need import CommonCode

    assert CommonCode.filter_words_to_str(["a", "b"]) == "a|b"
    assert CommonCode.str_to_filter_words("a|b") == ["a", "b"]
    assert CommonCode.str_to_replaces("a->b") == ["a->b"]
    assert CommonCode.replaces_to_str(["a->b"]) == "a->b"


def test_obtain_legal_files_filters_missing_paths(tmp_path):
    from src.py.com.yun.mao.util.need import CommonCode

    existing = tmp_path / "exists.txt"
    existing.write_text("ok", encoding="utf-8")
    missing = tmp_path / "missing.txt"
    assert CommonCode.obtain_legal_files(
        f"{existing}\n{missing}\n"
    ) == [str(existing)]
