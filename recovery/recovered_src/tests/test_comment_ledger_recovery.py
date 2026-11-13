from __future__ import annotations

import json
from types import SimpleNamespace

from src.py.com.yun.mao.record import CommentCopyLedger


def test_comment_ledger_writer_and_index_reload(tmp_path):
    CommentCopyLedger.set_dir_override_for_test(str(tmp_path))
    CommentCopyLedger.reset_for_test()
    CommentCopyLedger.mark_copied("src", 10, 20, "dest", 30, 40)
    CommentCopyLedger.flush_writes_for_test(3.0)
    path = tmp_path / "data-0001.jsonl"
    assert path.exists()
    row = json.loads(path.read_text(encoding="utf-8").strip())
    assert row["source"] == "src_10_20"
    assert row["dest"] == "dest_30_40"
    CommentCopyLedger.reset_for_test()
    assert CommentCopyLedger.already_copied("src", 10, 20, "dest", 30)
    CommentCopyLedger.set_dir_override_for_test(None)


def test_comment_ledger_skip_only_with_known_source_ids(tmp_path):
    CommentCopyLedger.set_dir_override_for_test(str(tmp_path))
    CommentCopyLedger.reset_for_test()
    CommentCopyLedger.mark_copied("src", 10, 20, "dest", 30, 40)
    CommentCopyLedger.flush_writes_for_test(3.0)
    parse = SimpleNamespace(
        messages=[SimpleNamespace(id=20)],
        source_channel="src",
        source_main_msg_id=10,
    )
    assert CommentCopyLedger.should_skip_comment_group(
        parse,
        {"dest": 30},
    ) is True
    assert CommentCopyLedger.should_skip_comment_group(object()) is False
    CommentCopyLedger.set_dir_override_for_test(None)


def test_comment_ledger_id_helpers():
    assert CommentCopyLedger.encode_id_key("a", 1, 2) == "a_1_2"
    assert CommentCopyLedger.decode_id_key("a_1_2") == ("a", 1, 2)
    assert CommentCopyLedger.extract_sent_ids([{"id": 1}, type("M", (), {"id": 2})()]) == [1, 2]
