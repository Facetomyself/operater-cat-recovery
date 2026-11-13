from __future__ import annotations

import json

from src.py.com.yun.mao.config.NewConfig import (
    MAIN_MODEL_DING_SHI_TEXT,
    MAIN_MODEL_MONITOR_TEXT,
)
from src.py.com.yun.mao.record import PublishIdRecord


def test_publish_record_names_and_modes():
    assert PublishIdRecord.volume_file_name(7) == "data-0007.jsonl"
    assert PublishIdRecord.mode_text_of("monitor") == MAIN_MODEL_MONITOR_TEXT
    assert PublishIdRecord.mode_text_of("timing") == MAIN_MODEL_DING_SHI_TEXT


def test_publish_record_link_and_id_helpers():
    assert (
        PublishIdRecord.build_comment_message_link("@demo", 42, None, 7)
        == "https://t.me/demo/42?single&comment=7"
    )
    assert PublishIdRecord._channel_key("-100123456") == "123456"
    assert PublishIdRecord.lookup_ids("@Demo", {"demo": ["3", "4"]}) == [3, 4]
    assert PublishIdRecord.is_cfg_list_complete(
        ["demo"],
        {"demo": [3]},
    )
    assert PublishIdRecord._build_link_list(
        ["@demo"],
        {"demo": [5]},
    ) == ["https://t.me/demo/5"]
    assert PublishIdRecord.first_sent_msg_id([8, 9]) == 8
    assert PublishIdRecord.dest_id_map_from_dest_links(
        ["https://t.me/demo/9"],
        ["@demo"],
    ) == {"@demo": [9]}
    assert PublishIdRecord.maps_for_type(
        "云预览",
        {"dest": [1]},
        {"preview": [2]},
    ) == ({"preview": [2]}, {"dest": [1]})


def test_resolve_record_lists_returns_type_and_cfgs():
    auto = type(
        "Auto",
        (),
        {
            "auto_type": 2,
            "destes": ["@dest"],
            "yulan_destes": ["@preview"],
        },
    )()
    assert PublishIdRecord.resolve_record_lists(auto) == (
        "自动流",
        ["@dest"],
        ["@preview"],
    )


def test_append_if_complete_inner_builds_mapper(monkeypatch):
    captured = {}

    def _capture(kid, name, type_text, mapper_item):
        captured.update(
            kid=kid,
            name=name,
            type_text=type_text,
            mapper_item=mapper_item,
        )

    monkeypatch.setattr(PublishIdRecord, "_commit_mapper_item", _capture)

    auto = type(
        "Auto",
        (),
        {
            "auto_type": 3,
            "kid": " kid ",
            "destes": ["@preview"],
            "yulan_destes": ["@dest"],
            "getName": lambda self: " demo ",
            "getSource": lambda self: "@src",
        },
    )()
    parse = type("Parse", (), {"messages": [type("Msg", (), {"id": 99})()]})()
    group_result = type(
        "GroupResult",
        (),
        {
            "dest_id_map": {"@dest": [11]},
            "preview_id_map": {"@preview": [22]},
        },
    )()

    PublishIdRecord._append_if_complete_inner(
        auto,
        parse,
        group_result,
        "monitor",
    )

    assert captured["kid"] == "kid"
    assert captured["name"] == "demo"
    assert captured["type_text"] == "预览流"
    mapper = captured["mapper_item"]
    assert mapper["mode"] == MAIN_MODEL_MONITOR_TEXT
    assert mapper["source"] == "https://t.me/src/99"
    assert mapper["dest"] == ["https://t.me/preview/22"]
    assert mapper["preview"] == ["https://t.me/dest/11"]
    assert mapper["time"]


def test_append_if_complete_delegates_to_inner(monkeypatch):
    captured = {}

    def _capture(auto, parse, group_result, convert_mode=None):
        captured.update(
            auto=auto,
            parse=parse,
            group_result=group_result,
            convert_mode=convert_mode,
        )

    monkeypatch.setattr(PublishIdRecord, "_append_if_complete_inner", _capture)
    auto = object()
    parse = object()
    group_result = object()

    PublishIdRecord.append_if_complete(auto, parse, group_result, "monitor")

    assert captured == {
        "auto": auto,
        "parse": parse,
        "group_result": group_result,
        "convert_mode": "monitor",
    }


def test_publish_link_and_success_log(capsys):
    link = PublishIdRecord.log_publish_success("@demo", 42)
    assert link == "https://t.me/demo/42"
    assert capsys.readouterr().out == (
        PublishIdRecord.PUBLISH_SUCCESS_LOG_PREFIX + link + "\n"
    )


def test_publish_success_accepts_cmcode_call_shape(capsys):
    sent = [
        type("Message", (), {"id": 42})(),
        type("Message", (), {"id": 43})(),
    ]
    link = PublishIdRecord.log_publish_success(
        "@demo",
        9,
        sent,
        2,
    )
    assert link == "https://t.me/demo/43?single&comment=9"
    output = capsys.readouterr().out
    assert "https://t.me/demo/42?single&comment=9" in output
    assert "https://t.me/demo/43?single&comment=9" in output


def test_publish_record_writer_and_meta(tmp_path):
    PublishIdRecord.set_record_dir_for_test(str(tmp_path))
    PublishIdRecord.reset_memory_for_test()
    PublishIdRecord._commit_mapper_item(
        "kid-1",
        "demo",
        "自动流",
        {"source": "src", "dest": ["dest"]},
    )
    assert PublishIdRecord.flush_writes_for_test(3.0) is None
    assert (tmp_path / "data-0001.jsonl").exists()
    lines = list(PublishIdRecord.iter_mapper_lines(str(tmp_path)))
    assert len(lines) == 1
    assert lines[0]["kid"] == "kid-1"
    assert lines[0]["name"] == "demo"
    assert lines[0]["type"] == "自动流"
    assert lines[0]["mapper_item"] == {"source": "src", "dest": ["dest"]}
    meta = json.loads((tmp_path / "meta.json").read_text(encoding="utf-8"))
    assert meta["items"][0]["kid"] == "kid-1"
    PublishIdRecord.set_record_dir_for_test(None)


def test_lookup_dest_links_reads_jsonl_wrapper(tmp_path):
    PublishIdRecord.set_record_dir_for_test(str(tmp_path))
    PublishIdRecord.reset_memory_for_test()
    PublishIdRecord._commit_mapper_item(
        "kid-1",
        "demo",
        "自动流",
        {
            "source": "https://t.me/source/9",
            "dest": ["https://t.me/dest/10"],
        },
    )
    PublishIdRecord.flush_writes_for_test(3.0)
    PublishIdRecord.reset_memory_for_test()
    assert PublishIdRecord.lookup_dest_links_for_source(
        "@source",
        9,
        kid="kid-1",
    ) == ["https://t.me/dest/10"]
    PublishIdRecord.set_record_dir_for_test(None)


def test_publish_record_rotates_volume(tmp_path, monkeypatch):
    monkeypatch.setattr(PublishIdRecord, "VOLUME_MAX_BYTES", 1)
    PublishIdRecord.set_record_dir_for_test(str(tmp_path))
    PublishIdRecord.reset_memory_for_test()
    PublishIdRecord._commit_mapper_item("kid-1", "one", "自动流", {"n": 1})
    PublishIdRecord._commit_mapper_item("kid-2", "two", "自动流", {"n": 2})
    PublishIdRecord.flush_writes_for_test(3.0)
    names = sorted(path.name for path in tmp_path.glob("data-*.jsonl"))
    assert names == ["data-0001.jsonl", "data-0002.jsonl"]
    PublishIdRecord.set_record_dir_for_test(None)
