# Recovered module: src.py.com.yun.mao.util.moviepy_ffmpeg_patch
# MoviePy ffmpeg stderr compatibility patch.
from __future__ import annotations

import locale


_PATCH_ATTR = "_yunyinmao_moviepy_stderr_patch"


def _decode_ffmpeg_stderr(raw: bytes) -> str:
    if not raw:
        return raw if isinstance(raw, str) else ""
    candidates = ["utf-8", "gbk", "cp936", "gb18030"]
    try:
        candidates.append(locale.getpreferredencoding(False) or "utf-8")
    except Exception:
        pass
    for enc in candidates:
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


def _stderr_bytes_as_utf8(raw: bytes) -> bytes:
    return _decode_ffmpeg_stderr(raw).encode("utf-8", errors="replace")


def apply_moviepy_ffmpeg_stderr_patch() -> None:
    """Patch ``moviepy.video.io.ffmpeg_reader`` once.

    The wrapper keeps the original ``sp.Popen`` behaviour but normalizes the
    bytes returned from ``communicate()`` to UTF-8 before MoviePy decodes
    them.  Missing MoviePy is treated as a no-op.
    """

    try:
        from moviepy.video.io import ffmpeg_reader
    except Exception:
        return None

    if getattr(ffmpeg_reader, _PATCH_ATTR, False):
        return None

    original_popen = ffmpeg_reader.sp.Popen

    class _PopenUtf8Stderr(original_popen):
        def communicate(self, input=None, timeout=None):
            try:
                stdout, stderr = super().communicate(input, timeout)
            except TypeError:
                stdout, stderr = super().communicate(input)
            if isinstance(stderr, (bytes, bytearray)):
                stderr = _stderr_bytes_as_utf8(bytes(stderr))
            return stdout, stderr

    ffmpeg_reader.sp.Popen = _PopenUtf8Stderr
    setattr(ffmpeg_reader, _PATCH_ATTR, True)
    return None
