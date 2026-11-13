from __future__ import annotations

import json
import random
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.py.com.yun.mao.remember import RandomBucketManager as rbm


@pytest.fixture(autouse=True)
def isolated_bucket_state(monkeypatch, tmp_path):
    monkeypatch.setattr(
        rbm,
        "YunYinMaoConfig",
        SimpleNamespace(abs_cache_dir=lambda: str(tmp_path)),
    )
    monkeypatch.setattr(
        rbm.CommonCode,
        "expand_random_group_fetch_id_window",
        lambda start, end: (start, end),
    )
    rbm.reset_memory_for_test()
    random.seed(7)
    yield
    rbm.reset_memory_for_test()


def test_geographic_segments_and_layout_math():
    assert rbm._build_geographic_segments(4, 100) == [
        (0, 99),
        (100, 199),
        (200, 299),
        (300, 399),
    ]
    generated = rbm._generate_random_bucket_ranges(4, 100)
    assert sorted(generated) == [
        [0, 99],
        [100, 199],
        [200, 299],
        [300, 399],
    ]
    assert rbm.auto_correct_step_length(50, 100) == 50
    assert rbm._calc_random_end(401, 100) == 500
    assert rbm._num_buckets(500, 100) == 5
    assert rbm._ranges_overlap(0, 10, 10, 20)
    assert not rbm._ranges_overlap(0, 9, 10, 20)
    assert rbm._range_conflicts(5, 8, [(8, 12)])


def test_invalid_layout_is_rebuilt_and_session_is_cleared():
    first = rbm.pick_next_bucket_range("source", "kid", 4, 400)
    assert first is not None
    key, state = rbm._resolve_context("source", "kid")
    assert key in rbm._bucket_map
    assert len(state["bucket_ranges"]) == 4
    assert rbm.session_tried_range_count("source", "kid") == 1

    state["bucket_ranges"] = []
    state["step_length"] = 999
    second = rbm.pick_next_bucket_range("source", "kid", 4, 400)
    assert second is not None
    assert len(state["bucket_ranges"]) == 4
    assert state["step_length"] == 100
    assert state["last_top_num"] == 400
    assert rbm.session_tried_range_count("source", "kid") == 1


def test_session_tried_ranges_record_count_and_clear():
    rbm.record_session_tried_range("source", "kid", 0, 99)
    rbm.record_session_tried_range("source", "kid", 0, 99)
    rbm.record_session_tried_range("source", "kid", 100, 199)
    assert rbm.get_session_tried_ranges("source", "kid") == [
        (0, 99),
        (100, 199),
    ]
    assert rbm.session_tried_range_count("source", "kid") == 2
    rbm.clear_session_tried_ranges("source", "kid")
    assert rbm.get_session_tried_ranges("source", "kid") == []
    assert rbm.session_tried_range_count("source", "kid") == 0


def test_pick_next_skips_persisted_and_session_ranges():
    assert rbm.bucket_count("source", "kid", 4, 400) == 4
    assert rbm.pick_next_bucket_range("source", "kid", 4, 400) is not None
    key, state = rbm._resolve_context("source", "kid")
    state["tried_buckets"] = [0, 1, 2]
    rbm.clear_session_tried_ranges("source", "kid")

    picked = rbm.pick_next_bucket_range("source", "kid", 4, 400)
    expected = tuple(state["bucket_ranges"][3])
    assert picked == (*expected, 3)
    assert expected in rbm.get_session_tried_ranges("source", "kid")

    rbm.record_session_tried_range("source", "kid", *expected)
    assert rbm.pick_next_bucket_range("source", "kid", 4, 400) is None


def test_pick_persisted_marks_buckets_and_restarts_after_exhaustion(capsys):
    first = rbm.pick_persisted_range("source", "kid", 2, 200)
    second = rbm.pick_persisted_range("source", "kid", 2, 200)
    assert first != second
    key, state = rbm._resolve_context("source", "kid")
    assert sorted(state["tried_buckets"]) == [0, 1]

    third = rbm.pick_persisted_range("source", "kid", 2, 200)
    assert third in {(0, 99), (100, 199)}
    assert len(state["tried_buckets"]) == 1
    output = capsys.readouterr().out
    assert "已全部枯竭" in output
    assert "开始新一轮轮询" in output


def test_persisted_state_is_read_after_restart():
    picked = rbm.pick_persisted_range("source", "kid", 2, 200)
    assert picked in {(0, 99), (100, 199)}
    key, state = rbm._resolve_context("source", "kid")
    expected = json.loads(json.dumps(state, ensure_ascii=False))
    path = Path(rbm._bucket_file("source", "kid"))
    assert path.is_file()

    rbm.reset_memory_for_test()
    assert key not in rbm._bucket_map
    rbm.load_random_bucket_map()

    assert key in rbm._bucket_map
    assert rbm._bucket_map[key] == expected
    loaded = rbm._bucket_map[key]
    assert loaded["step_length"] == 100
    assert loaded["last_top_num"] == 200
    assert len(loaded["tried_buckets"]) == 1
