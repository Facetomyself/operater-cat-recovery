from __future__ import annotations


def test_parse_source_parts_handles_private_links_and_pipes():
    from src.py.com.yun.mao.util.need import utils

    assert utils.parse_source_parts("https://t.me/c/123/45") == ("123", "45")
    assert utils.parse_source_parts("@channel|45") == ("@channel", "45")
    assert utils.parse_source_parts("") == (None, None)


def test_convert_dest_and_topic():
    from src.py.com.yun.mao.dclass.DTopClass import convertDest, convertDestTopic

    assert convertDest("https://t.me/c/123/45") == "-100123"
    assert convertDest("@channel|45") == "@channel"
    assert convertDestTopic("https://t.me/c/123/45") == 45
    assert convertDestTopic("@channel|topic") == "topic"
