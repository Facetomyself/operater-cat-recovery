# Recovered module: src.py.com.yun.mao.util.need.utils
# Pure helpers used across the licence, flow, media and UI layers.
from __future__ import annotations

import hashlib
import os
import random
import re
import shutil
import string
import time
from pathlib import Path
from typing import Any, Iterable


PIC_SUFFIXES = (".jpg", ".png", ".jpeg")
VIDEO_SUFFIXES = (".MP4", ".mp4")


def get_format_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_format_date() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def format_time(seconds: int) -> str:
    seconds = max(0, int(seconds or 0))
    hour, rem = divmod(seconds, 3600)
    minute, sec = divmod(rem, 60)
    return f"{hour}小时{minute}分{sec}秒" if hour else (
        f"{minute}分{sec}秒" if minute else f"{sec}秒"
    )


def format_remaining_time(total_seconds: int) -> str:
    return format_time(total_seconds)


def gen_array(length: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(max(0, int(length))))


def generate_random_en(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(max(0, int(length))))


def generate_random_chinese(length: int = 3) -> str:
    if length <= 0:
        return ""
    return "".join(chr(random.randint(0x4E00, 0x9FFF)) for _ in range(int(length)))


def gen_id_by_ns() -> str:
    return str(int(time.time() * 1000)) + generate_random_en(4).lower()


def gen_unit_name_by_ns_len(length: int = 10) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(max(1, int(length))))


def gen_unit_name_by_ns() -> str:
    return "J" + gen_unit_name_by_ns_len(10)


def init_folder(path: str | Path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def is_exit_file(file_path: str | Path) -> bool:
    return Path(file_path).is_file()


def is_exit_folder(folder: str | Path) -> bool:
    return Path(folder).is_dir()


def is_valid_media_file_path(pic_file_path: str | Path) -> tuple[bool, str]:
    path = Path(pic_file_path)
    if not path.is_absolute():
        return False, "请输入媒体绝对路径！"
    if not path.exists():
        return False, "路径不存在: " + str(path)
    if not path.is_file():
        return False, "这不是一个文件: " + str(path)
    if path.suffix not in PIC_SUFFIXES + VIDEO_SUFFIXES:
        return False, "这不是一个媒体文件: " + str(path)
    return True, "路径合法: " + str(path)


def check_file_size_less_than(file_path: str | Path, size_limit: int = 20) -> bool:
    try:
        return os.path.getsize(file_path) / 1024 / 1024 <= float(size_limit)
    except Exception:
        return False


def safe_del_file(file_path: str | Path) -> bool:
    try:
        Path(file_path).unlink(missing_ok=True)
        return True
    except Exception:
        return False


def safe_del_folder(folder: str | Path) -> bool:
    try:
        shutil.rmtree(folder, ignore_errors=True)
        return True
    except Exception:
        return False


def safe_copy_file(source: str | Path, target: str | Path) -> bool:
    try:
        init_folder(Path(target).parent)
        shutil.copy2(source, target)
        return True
    except Exception:
        return False


def move_file_overwrite(source: str | Path, target: str | Path) -> bool:
    try:
        init_folder(Path(target).parent)
        shutil.move(str(source), str(target))
        return True
    except Exception:
        return False


def copy_folder(source_folder: str | Path, target_folder: str | Path) -> bool:
    try:
        shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
        return True
    except Exception:
        return False


def delete_files_in_folder(folder: str | Path) -> bool:
    try:
        for item in Path(folder).iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink(missing_ok=True)
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
        return True
    except Exception:
        return False


def random_item_from_dict(mapping: dict):
    return random.choice(list(mapping.keys())) if mapping else None


def split_session(session: str) -> tuple[str, str]:
    path = Path(str(session or ""))
    return str(path.parent), path.name


def extract_username_or_channel(source_url: str) -> str:
    text = str(source_url or "").strip()
    match = re.search(r"https?://t\.me/([^/]+)/?", text)
    if match:
        return match.group(1)
    if text.startswith("@"):
        return text[1:]
    return text.split("/")[-1]


def extract_last_number(source_url: str) -> int:
    numbers = re.findall(r"\d+", str(source_url or ""))
    return int(numbers[-1]) if numbers else 0


def is_legal_user_name(name: str) -> bool:
    return bool(re.match(r"^@[A-Za-z0-9_]{5,32}$", str(name or "").strip()))


def is_public_link(source: str) -> bool:
    return str(source or "").strip().lower().startswith("https")


def is_pure_alpha_username(source: str) -> bool:
    text = str(source or "").strip().lstrip("@")
    return bool(text) and text.isalpha()


def is_mixed_username(source: str) -> bool:
    text = str(source or "").strip().lstrip("@")
    return bool(re.search(r"[A-Za-z]", text) and re.search(r"\d", text))


def is_legal_source(source: str) -> bool:
    text = str(source or "").strip()
    return bool(text) and (
        is_public_link(text)
        or text.lstrip("-").isdigit()
        or text.startswith("@")
    )


def strict_check_source(source: str, error_tip: str = "") -> tuple[bool, int]:
    text = str(source or "").strip()
    if not text:
        return False, -1
    if text.lstrip("-").isdigit():
        return True, int(text)
    username = extract_username_or_channel(text)
    return (bool(username), -1)


def safe_parse_to_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def parse_int(value: Any) -> tuple[bool, int]:
    try:
        return True, int(str(value).strip())
    except (TypeError, ValueError):
        return False, 0


def parse_source_parts(param_source: str) -> tuple[str | None, str | None]:
    source = str(param_source or "").strip()
    if source.startswith("https://t.me/c/"):
        parts = source[len("https://t.me/c/") :].split("/")
        channel_id_str = parts[0].strip() if parts else ""
        topic_id_str = parts[1].strip() if len(parts) > 1 else ""
        return channel_id_str or None, topic_id_str or None
    if "|" in source:
        channel, topic = source.split("|", 1)
        return channel.strip(), topic.strip()
    return source or None, None


def convertPrivateIdIfNeed(channel):
    text = str(channel or "").strip()
    if text.lstrip("-").isdigit() and not text.startswith("-100"):
        return "-100" + text
    return text


def convertSourceToIdOrAt(orign_source: str) -> str:
    text = str(orign_source or "").strip()
    if text.startswith("https://t.me/c/"):
        return text
    return extract_username_or_channel(text)


def convertLinkIfNeed(channel):
    text = str(channel or "").strip()
    if text.lstrip("-").isdigit():
        return convertPrivateIdIfNeed(text)
    if not text.startswith("@"):
        return "@" + text
    return text


def convertMessageLinkIfNeed(channel, msgId: int):
    return f"{convertLinkIfNeed(channel)}/{int(msgId)}"


def remove_links(text: str) -> str:
    return re.sub(r"https?://\S+", "", str(text or "")).strip()


def html_to_mark_down(html_str: str) -> str:
    try:
        import html2text

        return html2text.html2text(str(html_str or ""))
    except Exception:
        return re.sub(r"<[^>]+>", "", str(html_str or ""))


def sanitize_filename_with_regex(filename: str, replacement: str = "_") -> str:
    text = re.sub(r'[<>:"/\\|?*\r\n\t]', replacement, str(filename or ""))
    return re.sub(r"^\.", replacement, text).strip() or "file"


def get_first_n_elements(lst: list, n: int) -> list:
    return list(lst or [])[: max(0, int(n))]


def get_last_n_elements(arr: list, n: int) -> list:
    return list(arr or [])[-max(0, int(n)) :] if n else []


def clip_array_to_length(arr: list, length: int) -> list:
    return list(arr or [])[: max(0, int(length))]


def random_sample(arr: list, n: int) -> list:
    return random.sample(list(arr or []), min(max(0, int(n)), len(arr or [])))


def get_random_in_range(min_value: int, max_value: int) -> int:
    return random.randint(int(min_value), int(max_value))


def get_random_element(arr: list):
    return random.choice(arr) if arr else None


def is_photo_message(message: Any) -> bool:
    return bool(getattr(message, "photo", None)) or (
        isinstance(message, dict) and bool(message.get("photo"))
    )


def is_video_message(message: Any) -> bool:
    return bool(getattr(message, "video", None)) or (
        isinstance(message, dict) and bool(message.get("video"))
    )


def calculate_md5(file_path: str | Path, byte_block: int = 4096) -> str:
    try:
        digest = hashlib.md5()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(byte_block), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except Exception:
        return ""


def modify_media_md5(file_path: str | Path) -> bool:
    try:
        with open(file_path, "ab") as file:
            file.write(b"\x00")
        return True
    except Exception:
        return False


def calculate_target_length(text: str, min_length: int = 20, max_length: int = 100) -> int:
    text_len = len(str(text or ""))
    return min(max_length, max(min_length, text_len))


def truncate_text(text: str, max_length: int = 100) -> str:
    value = str(text or "")
    return value if len(value) <= max_length else value[:max_length] + "..."


def truncate_string(s: str, length: int = 10) -> str:
    value = str(s or "")
    return value if len(value) <= length else value[:length] + "..."


def str_to_lines(text: str) -> list:
    return str(text or "").split("\n")


def lines_to_str(lines: Iterable[Any]) -> str:
    return "\n".join(str(line) for line in lines or [])


def mask_key(key: str, visible_head: int = 8, visible_tail: int = 8, mask_char: str = "*") -> str:
    text = str(key or "")
    if len(text) <= visible_head + visible_tail:
        return text
    return text[:visible_head] + mask_char * (len(text) - visible_head - visible_tail) + text[-visible_tail:]


def mask_ucode(ucode: str) -> str:
    text = str(ucode or "")
    if len(text) <= 12:
        return mask_key(text, 2, 2)
    return text[:10] + "********" + text[-4:]


def un_mask_ucode(value: str) -> str:
    return str(value or "").replace("*", "")


def clean_code(value: str) -> str:
    return str(value or "").strip().replace("\r", "").replace("\n", "")


def grade_to_card_str(grade: str) -> str:
    mapping = {
        "beginner": "初级卡",
        "advanced": "高级卡",
        "geek": "极客卡",
        "experience": "体验卡",
        "youke": "游客",
        "freeze": "冻结",
    }
    return mapping.get(str(grade or "").lower(), str(grade or "游客"))


def genHuiyuanGrade(grade: str) -> str:
    return grade_to_card_str(grade)


def gen_grade_card_str(grade: str) -> str:
    return grade_to_card_str(grade)


def select_days_to_request_params(days: str) -> int:
    return safe_parse_to_int(str(days or "0").replace("day", ""), 0)


def select_grade_to_request_params(grade: str) -> str:
    return str(grade or "").strip().lower()


def is_valid_bot(name: str) -> bool:
    return bool(re.match(r"^@.*bot$", str(name or "").strip(), re.IGNORECASE))


def validate_xai_api_key(api_key: str) -> tuple[bool, str]:
    text = str(api_key or "").strip()
    if not text.startswith("xai-"):
        return False, "xai key must start with xai-"
    return (len(text) > 8), "" if len(text) > 8 else "xai key is too short"


def strTobool(value: Any) -> bool:
    return str(value).strip().lower() in ("1", "true", "yes", "y", "on")


def strTobool2(value: Any, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return strTobool(value)


def net_status(host: str = "1.1.1.1", port: int = 53, timeout: float = 1.0) -> bool:
    import socket

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def get_screen_size():
    try:
        from PyQt5.QtWidgets import QApplication

        screen = QApplication.desktop().screenGeometry()
        return screen.width(), screen.height()
    except Exception:
        return 1920, 1080


def add_font(font_size: int = 12, font_path: str | None = None):
    try:
        from PIL import ImageFont

        if font_path:
            return ImageFont.truetype(font_path, font_size)
        return ImageFont.load_default()
    except Exception:
        return None


def water_font_size(font_size: int) -> int:
    return max(1, int(font_size or 12))


def copy_text_to_clipboard(text_to_copy: str) -> bool:
    try:
        from PyQt5.QtWidgets import QApplication

        QApplication.clipboard().setText(str(text_to_copy or ""))
        return True
    except Exception:
        return False


def copy_html_to_clipboard(html_str: str) -> bool:
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QMimeData

        data = QMimeData()
        data.setHtml(str(html_str or ""))
        QApplication.clipboard().setMimeData(data)
        return True
    except Exception:
        return False


def generate_hash(value: str) -> str:
    """Return the SHA-256 key used by the Qt single-instance guards."""
    digest = hashlib.sha256()
    digest.update(str(value or "").encode("utf-8"))
    return digest.hexdigest()


_SHARED_MEMORY_GUARD = None
_SYSTEM_SEMAPHORE_GUARD = None


def is_already_running_semaphore(channel_id: str = "MyUniqueAppID") -> bool:
    """Check the inferred Qt single-instance shared-memory/semaphore pair."""
    global _SHARED_MEMORY_GUARD, _SYSTEM_SEMAPHORE_GUARD
    try:
        from PyQt5.QtCore import QSharedMemory, QSystemSemaphore
    except Exception:
        return False
    raw = str(channel_id or "MyUniqueAppID")
    key = generate_hash(raw.replace("https://t.me/", "").replace("@", ""))
    shared_memory = QSharedMemory(key)
    if shared_memory.attach():
        return True
    if not shared_memory.create(1):
        return True
    _SHARED_MEMORY_GUARD = shared_memory
    semaphore = QSystemSemaphore(key, 1)
    semaphore.acquire()
    _SYSTEM_SEMAPHORE_GUARD = semaphore
    return False


def is_already_running() -> bool:
    return is_already_running_semaphore("MyUniqueAppID")


def is_already_running_memory() -> bool:
    return is_already_running_semaphore("MyUniqueAppID")


def process_in_value_name(value_name: str) -> str:
    return str(value_name or "").replace("%", "_")
