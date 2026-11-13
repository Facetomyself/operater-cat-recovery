from __future__ import annotations

from src.py.com.yun.mao.util.need import utils


def test_mask_key_and_unmask():
    masked = utils.mask_key("0123SECRET_PARTcdef", visible_head=4, visible_tail=4)
    assert masked.startswith("0123")
    assert masked.endswith("cdef")
    assert "*" in masked
    assert utils.un_mask_ucode(masked) == "0123cdef"


def test_remove_links_strips_urls():
    assert (
        utils.remove_links("see https://example.test/a and http://x.test/2")
        == "see  and"
    )
    assert utils.remove_links("no links") == "no links"


def test_link_checks():
    assert utils.is_public_link("https://t.me/demo")
    assert not utils.is_public_link("@private")
    assert utils.is_legal_user_name("@demo_user")
    assert not utils.is_legal_user_name("demo_user")


def test_parse_int_and_booleans():
    assert utils.parse_int("12") == (True, 12)
    assert utils.parse_int("abc") == (False, 0)
    assert utils.strTobool2("") is False
    assert utils.strTobool2("yes", default=True) is True


def test_identifier_generators():
    assert len(utils.gen_unit_name_by_ns_len(10)) == 10
    assert utils.gen_unit_name_by_ns()
    assert len(utils.generate_random_en(6)) == 6


def test_time_and_array_helpers():
    assert utils.format_remaining_time(125) == "2分5秒"
    assert len(utils.gen_array(3)) == 3
    assert utils.clip_array_to_length([1, 2, 3, 4], 2) == [1, 2]
    assert utils.get_first_n_elements([1, 2, 3], 2) == [1, 2]
    assert utils.get_last_n_elements([1, 2, 3], 2) == [2, 3]
    value = utils.get_random_in_range(5, 5)
    assert value == 5


def test_ucode_and_grade_helpers():
    assert utils.mask_ucode("yunyinmao-e95901ec-927293c0") == (
        "yunyinmao-********93c0"
    )
    assert utils.clean_code(" a\r\nb ") == "ab"
    assert utils.grade_to_card_str("beginner") == "初级卡"
    assert utils.genHuiyuanGrade("geek") == "极客卡"
    assert utils.gen_grade_card_str("unknown") == "unknown"
