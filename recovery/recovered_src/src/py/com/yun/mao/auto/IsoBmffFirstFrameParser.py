# Recovered module: src.py.com.yun.mao.auto.IsoBmffFirstFrameParser
# Static reconstruction from Nuitka metadata, string constants, and control flow.
from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Iterator, Optional


# inferred: the numeric pool fixes the values but not their exact symbol order.
MAX_BOXES = 20000
MAX_MOOV_BYTES = 16 * 1024 * 1024
MAX_TRACKS = 32
MAX_CHUNKS = 500000
MAX_STSC_ENTRIES = 100000
MAX_SAMPLES = 2000000
MAX_STSS_ENTRIES = 100000
MAX_SAMPLE_SUM_OPS = 100000


class IsoBmffParseError(ValueError):
    """Raised when an ISO-BMFF box or sample table is malformed."""


@dataclass(frozen=True)
class Box:
    start: int
    size: int
    box_type: bytes
    header_size: int
    end: int

    @property
    def payload_start(self) -> int:
        return self.start + self.header_size


@dataclass(frozen=True)
class _ChunkOffsets:
    payload: bytes
    entries_start: int
    count: int
    width: int
    file_size: int

    def get(self, index: int) -> int:
        if index < 0 or index >= self.count:
            raise IsoBmffParseError("chunk index out of range")
        pos = self.entries_start + index * self.width
        if self.width == 4:
            value = _u32(self.payload, pos)
        else:
            value = _u64(self.payload, pos)
        if value <= 0 or value > self.file_size:
            raise IsoBmffParseError("chunk offset outside file")
        return value


@dataclass(frozen=True)
class _SampleSizes:
    payload: bytes
    entries_start: int
    count: int
    constant_size: int

    def get(self, index: int) -> int:
        if index < 0 or index >= self.count:
            raise IsoBmffParseError("sample index out of range")
        if self.constant_size:
            return self.constant_size
        return _u32(self.payload, self.entries_start + index * 4)


@dataclass(frozen=True)
class _StscEntry:
    first_chunk: int
    samples_per_chunk: int
    description: int


@dataclass(frozen=True)
class IsoBmffAnalysis:
    moov_complete: bool
    required_head_end: Optional[int]
    reason: str
    fragmented: bool = False


def _u32(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise IsoBmffParseError("truncated uint32")
    return struct.unpack_from(">I", data, offset)[0]


def _u64(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 8 > len(data):
        raise IsoBmffParseError("truncated uint64")
    return struct.unpack_from(">Q", data, offset)[0]


def _box_at(data: bytes, start: int, parent_end: int) -> Box:
    if start < 0 or start + 8 > parent_end or start + 8 > len(data):
        raise IsoBmffParseError("truncated box header")
    size = _u32(data, start)
    box_type = data[start + 4 : start + 8]
    header_size = 8
    if size == 1:
        if start + 16 > parent_end or start + 16 > len(data):
            raise IsoBmffParseError("truncated extended box header")
        size = _u64(data, start + 8)
        header_size = 16
        if size < header_size:
            raise IsoBmffParseError("invalid box size")
    elif size == 0:
        size = parent_end - start
    elif size < header_size:
        raise IsoBmffParseError("invalid box size")
    end = start + size
    if end > parent_end:
        raise IsoBmffParseError("box exceeds parent")
    return Box(start, size, box_type, header_size, end)


def _iter_boxes(data: bytes, start: int, end: int) -> Iterator[Box]:
    pos = start
    count = 0
    while pos < end:
        count += 1
        if count > MAX_BOXES:
            raise IsoBmffParseError("too many boxes")
        box = _box_at(data, pos, end)
        if box.end <= pos:
            raise IsoBmffParseError("non-advancing box")
        yield box
        pos = box.end
    if pos != end:
        raise IsoBmffParseError("box layout does not cover parent")


def _first_child(data: bytes, parent: Box, box_type: bytes) -> Optional[Box]:
    for box in _children(data, parent):
        if box.box_type == box_type:
            return box
    return None


def _children(data: bytes, parent: Box) -> Iterator[Box]:
    if parent.end > len(data):
        raise IsoBmffParseError("box exceeds parent")
    yield from _iter_boxes(data, parent.payload_start, parent.end)


def _scan_top_level(data: bytes) -> list[Box]:
    boxes: list[Box] = []
    pos = 0
    while pos + 8 <= len(data):
        try:
            box = _box_at(data, pos, len(data))
        except IsoBmffParseError:
            break
        boxes.append(box)
        if box.end <= pos:
            break
        pos = box.end
    return boxes


def _complete_moov_candidates(
    data: bytes,
    candidates: Optional[list[Box]] = None,
    search_from: int = 0,
) -> Optional[Box]:
    for box in candidates or ():
        if box.box_type == b"moov" and box.end <= len(data):
            return box
    search_from = max(0, int(search_from or 0))
    marker = data.find(b"moov", max(0, search_from - 4))
    while marker >= 0:
        start = marker - 4
        if start >= 0:
            try:
                box = _box_at(data, start, len(data))
            except IsoBmffParseError:
                box = None
            if box is not None and box.box_type == b"moov" and box.end <= len(data):
                return box
        marker = data.find(b"moov", marker + 1)
    return None


def _top_level_has(head: bytes, box_type: bytes) -> bool:
    return any(box.box_type == box_type for box in _scan_top_level(head))


def _declared_first_mdat_end(head: bytes) -> Optional[int]:
    for box in _scan_top_level(head):
        if box.box_type == b"mdat":
            return box.end
    marker = head.find(b"mdat", 4)
    while marker >= 0:
        start = marker - 4
        try:
            size = _u32(head, start)
            if size == 1:
                size = _u64(head, start + 8)
            if size >= 8:
                return start + size
        except IsoBmffParseError:
            pass
        marker = head.find(b"mdat", marker + 1)
    return None


def _strict_tail_moov(
    head: bytes,
    tail: bytes,
    file_size: int,
) -> tuple[Optional[Box], int, bytes]:
    # inferred: the decompiled init fixes the surrounding locals, not the tuple shape.
    if not tail or file_size <= 0:
        return None, 0, b""
    tail_offset = max(0, int(file_size) - len(tail))
    allowed_suffix_types = {b"free", b"skip", b"mfro", b"mfra", b"wide", b"uuid"}
    markers = [index for index in range(4, len(tail) - 3) if tail[index : index + 4] == b"moov"]
    for marker in markers:
        start = marker - 4
        try:
            box = _box_at(tail, start, len(tail))
        except IsoBmffParseError:
            continue
        if box.box_type != b"moov" or box.end > len(tail):
            continue
        suffix = tail[box.end :]
        suffix_ok = True
        pos = 0
        while pos + 8 <= len(suffix):
            try:
                child = _box_at(suffix, pos, len(suffix))
            except IsoBmffParseError:
                suffix_ok = False
                break
            if child.box_type not in allowed_suffix_types:
                suffix_ok = False
                break
            pos = child.end
        if suffix_ok and pos == len(suffix):
            logical = Box(
                tail_offset + box.start,
                box.size,
                box.box_type,
                box.header_size,
                tail_offset + box.end,
            )
            return logical, tail_offset, suffix
    return None, tail_offset, b""


def _parse_chunk_offsets(data: bytes, stbl: Box, file_size: int) -> _ChunkOffsets:
    matches = [
        box
        for box in _children(data, stbl)
        if box.box_type in (b"stco", b"co64")
    ]
    if len(matches) != 1:
        raise IsoBmffParseError("exactly one stco/co64 is required")
    box = matches[0]
    if box.end > len(data):
        raise IsoBmffParseError("truncated chunk offset table")
    width = 4 if box.box_type == b"stco" else 8
    payload = data[box.payload_start : box.end]
    count = _u32(payload, 0)
    if count <= 0 or count > MAX_CHUNKS:
        raise IsoBmffParseError("invalid chunk count")
    entries_start = 4
    if entries_start + count * width != len(payload):
        raise IsoBmffParseError("invalid chunk offset table length")
    result = _ChunkOffsets(payload, entries_start, count, width, file_size)
    for index in (0, count - 1):
        result.get(index)
    return result


def _parse_stsc(data: bytes, stbl: Box, chunk_count: int) -> tuple[_StscEntry, ...]:
    box = _first_child(data, stbl, b"stsc")
    if box is None:
        raise IsoBmffParseError("missing stsc")
    if box.end > len(data):
        raise IsoBmffParseError("truncated stsc")
    payload = data[box.payload_start : box.end]
    count = _u32(payload, 0)
    if count <= 0 or count > MAX_STSC_ENTRIES:
        raise IsoBmffParseError("invalid stsc count")
    entries_start = 4
    if entries_start + count * 12 != len(payload):
        raise IsoBmffParseError("invalid stsc length")
    entries: list[_StscEntry] = []
    previous = 0
    for index in range(count):
        pos = entries_start + index * 12
        first_chunk = _u32(payload, pos)
        samples_per_chunk = _u32(payload, pos + 4)
        description = _u32(payload, pos + 8)
        if (
            first_chunk <= previous
            or samples_per_chunk <= 0
            or first_chunk > chunk_count
        ):
            raise IsoBmffParseError("invalid stsc entry")
        previous = first_chunk
        entries.append(_StscEntry(first_chunk, samples_per_chunk, description))
    if not entries or entries[0].first_chunk != 1:
        raise IsoBmffParseError("stsc must start at chunk 1")
    return tuple(entries)


def _parse_stsz(data: bytes, stbl: Box) -> _SampleSizes:
    box = _first_child(data, stbl, b"stsz")
    if box is None:
        raise IsoBmffParseError("missing stsz")
    if box.end > len(data):
        raise IsoBmffParseError("truncated stsz")
    payload = data[box.payload_start : box.end]
    constant_size = _u32(payload, 0)
    count = _u32(payload, 4)
    if count <= 0 or count > MAX_SAMPLES:
        raise IsoBmffParseError("invalid sample count")
    entries_start = 8
    expected_length = entries_start + (0 if constant_size else count * 4)
    if expected_length != len(payload):
        raise IsoBmffParseError("invalid stsz length")
    return _SampleSizes(payload, entries_start, count, constant_size)


def _first_sync_sample(data: bytes, stbl: Box, sample_count: int) -> int:
    box = _first_child(data, stbl, b"stss")
    if box is None:
        return 1
    if box.end > len(data):
        raise IsoBmffParseError("truncated stss")
    payload = data[box.payload_start : box.end]
    count = _u32(payload, 0)
    if count <= 0 or count > MAX_STSS_ENTRIES or count > sample_count:
        raise IsoBmffParseError("invalid stss count")
    if 4 + count * 4 != len(payload):
        raise IsoBmffParseError("invalid stss length")
    first = _u32(payload, 4)
    if first <= 0 or first > sample_count:
        raise IsoBmffParseError("invalid sync sample")
    return first


def _find_path(data: bytes, parent: Box, path: tuple[bytes, ...]) -> Optional[Box]:
    current = parent
    for box_type in path:
        child = _first_child(data, current, box_type)
        if child is None:
            return None
        current = child
    return current


def _handler_is_video(data: bytes, trak: Box) -> bool:
    hdlr = _find_path(data, trak, (b"mdia", b"hdlr"))
    if hdlr is None or hdlr.end > len(data):
        return False
    return (
        hdlr.payload_start + 12 <= hdlr.end
        and data[hdlr.payload_start + 8 : hdlr.payload_start + 12] == b"vide"
    )


def _track_enabled(data: bytes, trak: Box) -> bool:
    tkhd = _first_child(data, trak, b"tkhd")
    if tkhd is None or tkhd.end > len(data) or tkhd.payload_start + 4 > tkhd.end:
        return True
    version_flags = _u32(data, tkhd.payload_start)
    return bool(version_flags & 0x000001)


def _sample_end_for_track(
    data: bytes,
    trak: Box,
    file_size: int,
    target_sample: int,
) -> Optional[int]:
    stbl = _find_path(data, trak, (b"mdia", b"minf", b"stbl"))
    if stbl is None:
        raise IsoBmffParseError("missing video sample table")
    offsets = _parse_chunk_offsets(data, stbl, file_size)
    stsc = _parse_stsc(data, stbl, offsets.count)
    sizes = _parse_stsz(data, stbl)
    if target_sample <= 0 or target_sample > sizes.count:
        raise IsoBmffParseError("sample index out of range")

    mapped_samples = 0
    for index, entry in enumerate(stsc):
        last_chunk = (
            stsc[index + 1].first_chunk - 1
            if index + 1 < len(stsc)
            else offsets.count
        )
        mapped_samples += max(0, last_chunk - entry.first_chunk + 1) * entry.samples_per_chunk
    if mapped_samples > MAX_SAMPLES:
        raise IsoBmffParseError("stsc sample capacity exceeds budget")
    if mapped_samples != sizes.count:
        raise IsoBmffParseError("stsc/stsz sample count mismatch")

    sample_cursor = 1
    target_chunk = 0
    index_in_chunk = 0
    chunk_first_sample = 1
    for index, entry in enumerate(stsc):
        last_chunk = (
            stsc[index + 1].first_chunk - 1
            if index + 1 < len(stsc)
            else offsets.count
        )
        if last_chunk < entry.first_chunk:
            raise IsoBmffParseError("invalid stsc entry")
        run_chunks = last_chunk - entry.first_chunk + 1
        run_samples = run_chunks * entry.samples_per_chunk
        if sample_cursor <= target_sample < sample_cursor + run_samples:
            relative = target_sample - sample_cursor
            target_chunk = entry.first_chunk + relative // entry.samples_per_chunk
            index_in_chunk = relative % entry.samples_per_chunk
            chunk_first_sample = sample_cursor + (
                (target_chunk - entry.first_chunk) * entry.samples_per_chunk
            )
            break
        sample_cursor += run_samples
    if target_chunk <= 0:
        raise IsoBmffParseError("sync sample is not mapped by stsc")

    chunk_offset = offsets.get(target_chunk - 1)
    relative = 0
    if index_in_chunk > MAX_SAMPLE_SUM_OPS:
        raise IsoBmffParseError("too many samples in target chunk")
    for sample_index in range(chunk_first_sample, chunk_first_sample + index_in_chunk):
        size = sizes.get(sample_index - 1)
        if size <= 0:
            raise IsoBmffParseError("invalid sample size")
        relative += size
    sample_size = sizes.get(target_sample - 1)
    if sample_size <= 0:
        raise IsoBmffParseError("invalid sample size")
    byte_end = chunk_offset + relative + sample_size
    if chunk_offset >= file_size or byte_end > file_size:
        raise IsoBmffParseError("video sample range outside file")
    return byte_end


def _top_level_moov(head: bytes) -> Optional[Box]:
    for box in _scan_top_level(head):
        if box.box_type == b"moov":
            return box
    return None


def _required_video_head(
    data: bytes,
    moov: Box,
    file_size: int,
) -> tuple[bool, Optional[int], bool, Optional[str]]:
    try:
        root = list(_children(data, moov))
    except IsoBmffParseError as exc:
        return False, None, False, str(exc)
    tracks = [box for box in root if box.box_type == b"trak"]
    if len(tracks) > MAX_TRACKS:
        return False, None, False, "invalid track count"
    video_tracks = [box for box in tracks if _handler_is_video(data, box)]
    if not video_tracks:
        return False, None, False, "no video track"
    enabled = [box for box in video_tracks if _track_enabled(data, box)]
    selected = enabled[0] if enabled else video_tracks[0]
    fragmented_hint = any(box.box_type in (b"mvex", b"moof", b"mfra") for box in root)
    if fragmented_hint:
        return True, moov.end, True, None
    try:
        stbl = _find_path(data, selected, (b"mdia", b"minf", b"stbl"))
        if stbl is None:
            raise IsoBmffParseError("missing video sample table")
        sizes = _parse_stsz(data, stbl)
        first_index = _first_sync_sample(data, stbl, sizes.count)
        required = _sample_end_for_track(data, selected, file_size, first_index)
    except IsoBmffParseError as exc:
        return True, moov.end, False, str(exc)
    return True, required or moov.end, False, None


def analyze_iso_bmff(moov: bytes, file_size: int) -> IsoBmffAnalysis:
    """Validate the head of an ISO-BMFF file and locate the first frame end.

    ``moov`` is the downloaded head buffer (not necessarily the complete file).
    The returned ``required_head_end`` is the byte offset needed for ffmpeg to
    decode the first sync sample.  A fragmented MP4 only guarantees a complete
    ``moov``; the caller must continue with its moof/mdat strategy.
    """

    file_size = max(0, int(file_size or 0))
    if not moov:
        return IsoBmffAnalysis(False, None, "moov_not_complete")
    moov_box = _top_level_moov(moov)
    if moov_box is None:
        moov_box = _complete_moov_candidates(moov)
    if moov_box is None:
        return IsoBmffAnalysis(False, None, "moov_not_complete")
    if moov_box.end > len(moov):
        return IsoBmffAnalysis(False, None, "moov_not_complete")
    ok, required, fragmented, reason = _required_video_head(moov, moov_box, file_size)
    if fragmented:
        return IsoBmffAnalysis(True, required, "fragmented", True)
    if not ok:
        return IsoBmffAnalysis(False, required, reason or "no video track")
    return IsoBmffAnalysis(True, required, reason or "ok")


def detect_container(head: bytes, suffix: str) -> str:
    head = bytes(head or b"")
    suffix = str(suffix or "").lower()
    if len(head) >= 12 and head[:4] == b"RIFF" and head[8:12] == b"AVI ":
        return "avi"
    raw_probe = head[:65536]
    raw_m4v = any(
        marker in raw_probe
        for marker in (b"\x00\x00\x01\xb0", b"\x00\x00\x01 ", b"\x00\x00\x01\xb6")
    )
    top_boxes = _scan_top_level(head)
    is_iso_bmff = any(
        box.box_type in (b"ftyp", b"moov", b"mdat", b"moof", b"mvex", b"free", b"wide")
        for box in top_boxes
    )
    if raw_m4v and not is_iso_bmff:
        return "raw_m4v"
    if not is_iso_bmff:
        if suffix in (".mp4", ".mov", ".m4v"):
            return "raw_m4v" if suffix == ".m4v" else "unknown"
        return "raw_m4v" if raw_m4v else "unknown"
    fragmented = any(box.box_type in (b"moof", b"mfra") for box in top_boxes)
    if not fragmented:
        moov_box = next((box for box in top_boxes if box.box_type == b"moov"), None)
        if moov_box is not None and moov_box.end <= len(head):
            try:
                fragmented = any(
                    box.box_type == b"mvex" for box in _children(head, moov_box)
                )
            except IsoBmffParseError:
                fragmented = False
    return "fragmented_mp4" if fragmented else "classic_mp4"


def estimate_tail_metadata_bytes(
    moov: bytes,
    file_size: int,
    max_bytes: int = MAX_MOOV_BYTES,
) -> int:
    file_size = max(0, int(file_size or 0))
    max_bytes = max(0, int(max_bytes or 0))
    if not moov or file_size <= len(moov) or max_bytes <= 0:
        return 0
    mdat_end = _declared_first_mdat_end(moov)
    if mdat_end is None:
        remaining = file_size
    else:
        remaining = max(0, file_size - max(0, int(mdat_end)))
    return min(remaining, max_bytes)


def head_has_incomplete_top_level_moov(head: bytes) -> bool:
    head = bytes(head or b"")
    if not head:
        return False
    boxes = _scan_top_level(head)
    parsed_end = boxes[-1].end if boxes else 0
    for box in boxes:
        if box.box_type == b"moov" and box.end > len(head):
            return True
    marker = head.find(b"moov", max(0, parsed_end - 4))
    while marker >= 4:
        start = marker - 4
        incomplete_type = b"moov"
        try:
            size = _u32(head, start)
            header_size = 8
            if size == 1:
                if start + 16 > len(head):
                    return True
                size = _u64(head, start + 8)
                header_size = 16
            if size == 0:
                return True
            if size < header_size:
                raise IsoBmffParseError("invalid box size")
            if start + size > len(head):
                return incomplete_type == b"moov"
        except IsoBmffParseError:
            return True
        marker = head.find(b"moov", marker + 1)
    return False
