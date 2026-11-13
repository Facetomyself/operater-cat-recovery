from __future__ import annotations

import datetime
from types import SimpleNamespace

from src.py.com.yun.mao.util.need.CommonCode import (
    boolToStr,
    current_time,
    geneRamdomId,
    get_max_duration_message,
    get_max_size_message,
    getVideoDuration,
    mediaSize,
    message_has_button,
    messages_has_button,
    messages_has_video,
)


def test_bool_and_time_helpers():
    assert boolToStr(True) == "是"
    assert boolToStr(False) == "否"
    now = datetime.datetime.now()
    assert current_time().startswith(now.strftime("%Y-%m-%d %H"))


def test_random_id_is_unique_and_shaped():
    existing = {1, 2}
    value = geneRamdomId(existing)
    assert value not in existing
    assert 10000000000000000 <= value <= 99999999999999999


def test_message_button_and_video_helpers():
    button_msg = SimpleNamespace(reply_markup=object())
    plain_msg = SimpleNamespace(reply_markup=None)
    video_msg = SimpleNamespace(video=object())
    assert message_has_button(button_msg)
    assert not message_has_button(plain_msg)
    assert messages_has_button([plain_msg, button_msg])
    assert messages_has_video([plain_msg, video_msg])


def test_duration_and_size_extraction():
    video = SimpleNamespace(video=SimpleNamespace(duration=120))
    document = SimpleNamespace(document=SimpleNamespace(size=2048))
    assert getVideoDuration(video) == 120
    assert getVideoDuration(SimpleNamespace(duration=30)) == 30
    assert mediaSize(document) == 2048


def test_max_message_selectors():
    messages = [
        SimpleNamespace(
            video=SimpleNamespace(duration=10),
            document=SimpleNamespace(size=100),
        ),
        SimpleNamespace(
            video=SimpleNamespace(duration=60),
            document=SimpleNamespace(size=900),
        ),
    ]
    assert get_max_duration_message(messages) is messages[1]
    assert get_max_size_message(messages) is messages[1]
