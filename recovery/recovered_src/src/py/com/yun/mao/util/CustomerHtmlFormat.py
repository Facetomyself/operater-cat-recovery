# Recovered module: src.py.com.yun.mao.util.CustomerHtmlFormat
# Telethon entity offsets are UTF-16 code units; this module converts them to
# Telegram HTML tags and preserves custom emoji tags.
from __future__ import annotations

import html as _html
from collections import defaultdict


def code_unit_length(s: str) -> int:
    return sum(2 if ord(ch) > 0xFFFF else 1 for ch in str(s or ""))


def slice_by_cu(s: str, start_cu: int, length_cu: int, cum_cu=None) -> str:
    text = str(s or "")
    if cum_cu is None:
        cum = [0]
        for ch in text:
            cum.append(cum[-1] + (2 if ord(ch) > 0xFFFF else 1))
    else:
        cum = list(cum_cu)
    start_cu = max(0, int(start_cu))
    end_cu = start_cu + max(0, int(length_cu))

    def char_at(cu_value):
        for idx, value in enumerate(cum):
            if value >= cu_value:
                return idx
        return len(text)

    return text[char_at(start_cu):char_at(end_cu)]


def merge_overlapping_entities(entities):
    grouped = defaultdict(list)
    for entity in entities or []:
        grouped[getattr(entity, "type", None) or type(entity)].append(entity)
    merged = []
    for _, group in grouped.items():
        group = sorted(
            group,
            key=lambda e: (int(getattr(e, "offset", 0)), int(getattr(e, "length", 0))),
        )
        current = None
        for entity in group:
            if current is None:
                current = entity
                continue
            current_end = int(current.offset) + int(current.length)
            entity_end = int(entity.offset) + int(entity.length)
            if int(entity.offset) <= current_end:
                current.length = max(current_end, entity_end) - int(current.offset)
            else:
                merged.append(current)
                current = entity
        if current is not None:
            merged.append(current)
    return merged


def _type_name(entity) -> str:
    return type(entity).__name__


def _open_tag(entity) -> str:
    name = _type_name(entity)
    if name == "MessageEntityBold":
        return "<b>"
    if name == "MessageEntityItalic":
        return "<i>"
    if name == "MessageEntityUnderline":
        return "<u>"
    if name == "MessageEntityStrike":
        return "<s>"
    if name == "MessageEntitySpoiler":
        return "<tg-spoiler>"
    if name == "MessageEntityBlockquote":
        collapsed = " expandable" if getattr(entity, "collapsed", False) else ""
        return f"<blockquote{collapsed}>"
    if name == "MessageEntityCode":
        return "<code>"
    if name == "MessageEntityPre":
        language = getattr(entity, "language", "") or ""
        if language:
            return f'<pre language="{_html.escape(str(language), quote=True)}">'
        return "<pre>"
    if name in ("MessageEntityTextUrl", "MessageEntityUrl"):
        url = getattr(entity, "url", "") or ""
        if url:
            return f'<a href="{_html.escape(str(url), quote=True)}">'
        return "<a>"
    if name == "MessageEntityCustomEmoji":
        return f'<tg-emoji emoji-id="{getattr(entity, "document_id", "")}">'
    return ""


def _close_tag(entity) -> str:
    name = _type_name(entity)
    return {
        "MessageEntityBold": "</b>",
        "MessageEntityItalic": "</i>",
        "MessageEntityUnderline": "</u>",
        "MessageEntityStrike": "</s>",
        "MessageEntitySpoiler": "</tg-spoiler>",
        "MessageEntityBlockquote": "</blockquote>",
        "MessageEntityCode": "</code>",
        "MessageEntityPre": "</pre>",
        "MessageEntityTextUrl": "</a>",
        "MessageEntityUrl": "</a>",
        "MessageEntityCustomEmoji": "</tg-emoji>",
    }.get(name, "")


def _cu_to_char_map(text: str):
    cum = [0]
    char_of_cu = {}
    for index, ch in enumerate(text):
        width = 2 if ord(ch) > 0xFFFF else 1
        for unit in range(width):
            char_of_cu[cum[-1] + unit] = index
        cum.append(cum[-1] + width)
    char_of_cu[cum[-1]] = len(text)
    return cum, char_of_cu


def entities_to_html(text: str, entities, escape_html: bool = True) -> str:
    source = str(text or "")
    if not entities:
        return _html.escape(source, quote=False) if escape_html else source
    source = _html.escape(source, quote=False) if escape_html else source

    # Recompute the map on the unescaped text before inserting tags.
    raw = str(text or "")
    cum, char_of_cu = _cu_to_char_map(raw)
    starts = defaultdict(list)
    ends = defaultdict(list)
    for entity in entities or []:
        start = int(getattr(entity, "offset", 0) or 0)
        length = int(getattr(entity, "length", 0) or 0)
        end = start + length
        tag_open = _open_tag(entity)
        tag_close = _close_tag(entity)
        if not tag_open or not tag_close:
            continue
        starts[char_of_cu.get(start, len(raw))].append((entity, tag_open))
        ends[char_of_cu.get(end, len(raw))].append((entity, tag_close))

    out = []
    for index, ch in enumerate(raw):
        for entity, tag in sorted(
            ends.get(index, ()),
            key=lambda item: -int(getattr(item[0], "offset", 0)),
        ):
            out.append(tag)
        for entity, tag in sorted(
            starts.get(index, ()),
            key=lambda item: -int(getattr(item[0], "length", 0)),
        ):
            out.append(tag)
        out.append(_html.escape(ch, quote=False) if escape_html else ch)
    for entity, tag in sorted(
        ends.get(len(raw), ()),
        key=lambda item: -int(getattr(item[0], "offset", 0)),
    ):
        out.append(tag)
    return "".join(out)
