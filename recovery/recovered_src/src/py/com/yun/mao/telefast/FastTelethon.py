# Recovered module: src.py.com.yun.mao.telefast.FastTelethon
# Static reconstruction from Nuitka code-object metadata, module constants,
# and Hex-Rays control flow.  Network and file-transfer paths are translated,
# but this module is not executed by the reconstruction process.
from __future__ import annotations

import asyncio
import copy
import hashlib
import inspect
import logging
import math
import os
from collections import defaultdict
from typing import (
    AsyncGenerator,
    Awaitable,
    BinaryIO,
    DefaultDict,
    List,
    Optional,
    Tuple,
    Union,
)

from telethon import TelegramClient, helpers, utils
from telethon.crypto import AuthKey
from telethon.errors import (
    AuthKeyDuplicatedError,
    AuthKeyError,
    AuthKeyInvalidError,
    AuthKeyNotFound,
    AuthKeyUnregisteredError,
)
from telethon.network import MTProtoSender
from telethon.tl.alltlobjects import LAYER
from telethon.tl.functions import InvokeWithLayerRequest
from telethon.tl.functions.auth import (
    ExportAuthorizationRequest,
    ImportAuthorizationRequest,
)
from telethon.tl.functions.upload import (
    GetFileRequest,
    SaveBigFilePartRequest,
    SaveFilePartRequest,
)
from telethon.tl.types import (
    Document,
    InputDocumentFileLocation,
    InputFile,
    InputFileBig,
    InputFileLocation,
    InputPeerPhotoFileLocation,
    InputPhotoFileLocation,
)

from ..auto.down_load_config import down_load_part_size_kb, up_load_part_size_kb
from ..cd import Working
from ..config import YunYinMaoConfig
from ..util import FloodGuard
from ..util.FloodGuard import with_flood_retry
from . import RateTempClass
from .RateLimiterClass import DownRateLimiter, UpRateLimiter


_FAST_AUTH_CACHE_ATTR = "_client_dc_auth_cache"
_FAST_AUTH_LOCKS_ATTR = "_client_dc_auth_locks"
_client_dc_auth_cache = defaultdict(dict)
_fast_transfer_dc_auth_keys = defaultdict(dict)
_fast_transfer_dc_auth_locks: DefaultDict[Tuple[int, int], asyncio.Lock] = defaultdict(asyncio.Lock)
parallel_transfer_locks: DefaultDict[Tuple[int, int], asyncio.Lock] = defaultdict(asyncio.Lock)

_AUTH_KEY_ERRORS = (
    AuthKeyDuplicatedError,
    AuthKeyError,
    AuthKeyInvalidError,
    AuthKeyNotFound,
    AuthKeyUnregisteredError,
)

TG_MB_CHUNK = 1024 * 1024
TG_MAX_GET_FILE_LIMIT = 1024 * 1024
TG_FILE_ALIGN = 4096
TG_LARGE_FILE_THRESHOLD = 10 * 1024 * 1024
_MAX_CONNECTION_FULL_SIZE = 100 * 1024 * 1024
_MAX_CONNECTION_COUNT = 100

Logger = logging.getLogger("telefast")
TypeLocation = Union[
    Document,
    InputFileLocation,
    InputDocumentFileLocation,
    InputPhotoFileLocation,
    InputPeerPhotoFileLocation,
]


def _get_client_dc_auth(client, dc_id):
    cache = getattr(client, _FAST_AUTH_CACHE_ATTR, None)
    if cache is None:
        cache = {}
        setattr(client, _FAST_AUTH_CACHE_ATTR, cache)
    return cache.get(dc_id)


def _set_client_dc_auth(client, dc_id, auth_key):
    cache = getattr(client, _FAST_AUTH_CACHE_ATTR, None)
    if cache is None:
        cache = {}
        setattr(client, _FAST_AUTH_CACHE_ATTR, cache)
    cache[dc_id] = auth_key


def _invalidate_client_dc_auth(client, dc_id):
    cache = getattr(client, _FAST_AUTH_CACHE_ATTR, None)
    if cache is not None:
        cache.pop(dc_id, None)
    _client_dc_auth_cache.pop((id(client), dc_id), None)
    _fast_transfer_dc_auth_keys.pop((id(client), dc_id), None)


def _tg_normalize_limit(limit, file_size):
    """Clamp a Telegram get-file limit to one valid MTProto response."""

    file_size = max(0, int(file_size or 0))
    if file_size == 0:
        return 0
    requested = file_size if limit is None else int(limit)
    if requested <= 0:
        requested = file_size
    return max(1, min(requested, file_size, TG_MAX_GET_FILE_LIMIT))


def _normalize_part_size(part_size_kb, file_size, download_length=None, part_size=None):
    """Return an aligned transfer part size in bytes."""

    file_size = max(0, int(file_size or 0))
    if part_size is None:
        if part_size_kb is None:
            part_size_kb = utils.get_appropriated_part_size(file_size)
        part_size = int(part_size_kb) * 1024
    part_size = max(TG_FILE_ALIGN, int(part_size))
    part_size = min(part_size, TG_MAX_GET_FILE_LIMIT)
    part_size -= part_size % TG_FILE_ALIGN
    if download_length is not None:
        download_length = max(0, int(download_length))
        if 0 < download_length < part_size:
            part_size = max(TG_FILE_ALIGN, download_length)
            part_size -= part_size % TG_FILE_ALIGN
            if part_size == 0:
                part_size = min(download_length, TG_FILE_ALIGN)
    return max(1, part_size)


async def stream_file(
    file_to_stream: BinaryIO,
    chunk_size: int = 1024,
) -> AsyncGenerator[bytes, None]:
    """Yield file chunks from a binary stream."""

    chunk_size = max(1, int(chunk_size))
    while True:
        data = file_to_stream.read(chunk_size)
        if not data:
            break
        yield data


async def file_to_stream(
    file_to_stream: BinaryIO,
    chunk_size: int = 1024,
) -> AsyncGenerator[bytes, None]:
    """Compatibility alias for the recovered ``stream_file`` generator."""

    async for chunk in stream_file(file_to_stream, chunk_size):
        yield chunk


class DownloadSender:
    def __init__(
        self,
        client: TelegramClient,
        dc_id: int,
        sender: MTProtoSender,
        file: TypeLocation,
        offset: int,
        limit: int,
        stride: int,
    ) -> None:
        self.client = client
        self.dc_id = dc_id
        self.sender = sender
        self.file = file
        self.offset = int(offset)
        self.limit = int(limit)
        self.stride = int(stride)
        self.file_size = int(getattr(file, "size", 0) or 0)
        self.count = 0
        self.last_offset = self.offset
        self._flood_event = asyncio.Event()
        self._flood_event.set()
        self._flood_lock = asyncio.Lock()

    async def next(self):
        remaining = self.file_size - self.offset
        if remaining <= 0 or self.count * self.stride >= remaining:
            return None

        offset = self.offset + self.count * self.stride
        limit = _tg_normalize_limit(self.limit, self.file_size - offset)
        if limit <= 0:
            return None
        self.count += 1
        self.last_offset = offset
        request = GetFileRequest(self.file, offset=offset, limit=limit, precise=True)

        async def request_part():
            async with self._flood_lock:
                if not self._flood_event.is_set():
                    await self._flood_event.wait()
            rate = max(1, int(getattr(RateTempClass, "down_load_rate", 1) or 1) * 100)
            DownRateLimiter(rate).wait()
            return await self.client._call(request)

        try:
            response = await with_flood_retry(
                request_part,
                max_retries=max(1, int(getattr(YunYinMaoConfig, "MAX_TRY_COUNT", 5) or 5)),
                prefix="下载",
            )
            FloodGuard.clean_flood_log()
            return bytes(response.bytes)
        except _AUTH_KEY_ERRORS:
            _invalidate_client_dc_auth(self.client, self.dc_id)
            raise

    async def disconnect(self) -> None:
        await self.sender.disconnect()


class UploadSender:
    def __init__(
        self,
        client: TelegramClient,
        sender: MTProtoSender,
        file_id: int,
        part_count: int,
        big: bool,
        index: int,
        stride: int,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self.client = client
        self.sender = sender
        self.file_id = int(file_id)
        self.part_count = int(part_count)
        self.big = bool(big)
        self.index = int(index)
        self.stride = int(stride)
        self.loop = loop
        self.count = 0
        self._current_part = self.index
        self._pending = None

    async def next(self, part: bytes):
        part_index = self.index + self.count * self.stride
        if part_index >= self.part_count:
            return None
        self._current_part = part_index
        self.count += 1
        data = bytes(part)
        Logger.debug(
            "Sending file part %s/%s with %s bytes",
            part_index,
            self.part_count,
            len(data),
        )
        return await self._next(data)

    async def _next(self, data: bytes):
        if self.big:
            request = SaveBigFilePartRequest(
                self.file_id,
                self._current_part,
                self.part_count,
                data,
            )
        else:
            if len(data) > TG_MB_CHUNK:
                raise ValueError("file part exceeds Telegram chunk limit")
            request = SaveFilePartRequest(self.file_id, self._current_part, data)

        async def send_part():
            rate = max(1, int(getattr(RateTempClass, "up_load_rate", 1) or 1) * 100)
            UpRateLimiter(rate).wait()
            return await self.client._call(request)

        response = await with_flood_retry(
            send_part,
            max_retries=max(1, int(getattr(YunYinMaoConfig, "MAX_TRY_COUNT", 5) or 5)),
            prefix="上传",
        )
        FloodGuard.clean_flood_log()
        return response

    async def disconnect(self) -> None:
        await self.sender.disconnect()


class ParallelTransferrer:
    MAX_CONNECTION_COUNT = _MAX_CONNECTION_COUNT

    def __init__(self, client: TelegramClient) -> None:
        self.client = client
        self.senders: List[Union[DownloadSender, UploadSender]] = []
        self.upload_ticker = asyncio.Event()
        self.part_size = 0
        self.part_count = 0
        self.is_large = False
        self._upload_index = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._cleanup()

    async def _cleanup(self) -> None:
        senders = list(self.senders)
        self.senders.clear()
        if senders:
            await asyncio.gather(
                *(sender.disconnect() for sender in senders),
                return_exceptions=True,
            )
        self.upload_ticker.clear()
        Logger.debug("Parallel download finished, cleaning up connections")

    def _get_connection_count(
        self,
        file_size: int,
        max_count: int = MAX_CONNECTION_COUNT,
        full_size: int = _MAX_CONNECTION_FULL_SIZE,
    ) -> int:
        # inferred: exact integer tuning is embedded as constants, not source.
        file_size = max(0, int(file_size or 0))
        max_count = max(1, int(max_count or 1))
        full_size = max(1, int(full_size or 1))
        if file_size <= 0:
            return 1
        count = math.ceil(file_size * max_count / full_size)
        return max(1, min(max_count, count))

    @staticmethod
    def _normalize_part_size(
        part_size_kb,
        file_size,
        download_length=None,
        part_size=None,
    ) -> int:
        # inferred: Telegram part-size clamping from 1KB/4KB/MB constants.
        return _normalize_part_size(
            part_size_kb,
            file_size,
            download_length,
            part_size,
        )

    async def _connect_sender(self, sender, dc, auth=None, export_auth=True):
        # inferred: Telethon 1.x connection-factory compatibility is not
        # represented directly in the Nuitka constants.
        loggers = getattr(self.client, "_log", None)
        proxy = getattr(self.client, "_proxy", None)
        connection_factory = getattr(self.client, "_connection", None)
        if connection_factory is not None:
            try:
                connection = connection_factory(
                    dc.ip_address,
                    dc.port,
                    dc.id,
                    loggers=loggers,
                    proxy=proxy,
                )
            except TypeError:
                connection = connection_factory(
                    dc.ip_address,
                    dc.port,
                    dc.id,
                    loggers=loggers,
                )
            await sender.connect(connection)
        else:
            await sender.connect(dc.ip_address, dc.port)

        if export_auth and auth is not None:
            init_request = getattr(self.client, "_init_request", None)
            if init_request is not None:
                try:
                    init_request = copy.copy(init_request)
                    init_request.query = InvokeWithLayerRequest(
                        LAYER,
                        ImportAuthorizationRequest(id=auth.id, bytes=auth.bytes),
                    )
                    await sender.send(init_request)
                    return sender
                except AttributeError:
                    init_request = None
            if init_request is None:
                await sender.send(
                    InvokeWithLayerRequest(
                        LAYER,
                        ImportAuthorizationRequest(id=auth.id, bytes=auth.bytes),
                    )
                )
        return sender

    async def _create_sender(self, dc_id: int, export_auth: bool = True):
        key = (id(self.client), int(dc_id))
        async with _fast_transfer_dc_auth_locks[key]:
            cached = _get_client_dc_auth(self.client, dc_id)
            auth = None
            if cached is not None:
                auth_key = cached
            elif int(dc_id) == int(self.client.session.dc_id):
                auth_key = self.client.session.auth_key
                _set_client_dc_auth(self.client, dc_id, auth_key)
            else:
                Logger.debug("Exporting auth to DC %s", dc_id)
                auth = await self.client(ExportAuthorizationRequest(int(dc_id)))
                auth_key = AuthKey(auth.bytes)
                _set_client_dc_auth(self.client, dc_id, auth_key)
                _fast_transfer_dc_auth_keys[key][dc_id] = auth_key
                _client_dc_auth_cache[key][dc_id] = auth_key

            dc = self.client._get_dc(int(dc_id))
            loggers = getattr(self.client, "_log", None)
            proxy = getattr(self.client, "_proxy", None)
            try:
                sender = MTProtoSender(auth_key, loggers=loggers)
            except TypeError:
                sender = MTProtoSender(auth_key, loggers=loggers, proxy=proxy)
            return await self._connect_sender(
                sender,
                dc,
                auth=auth,
                export_auth=export_auth,
            )

    async def _create_download_sender(
        self,
        file: TypeLocation,
        index: int,
        part_size: int,
        stride: int,
        part_count: int,
        byte_offset: int,
    ) -> DownloadSender:
        dc_id = int(getattr(file, "dc_id", 0) or self.client.session.dc_id)
        sender = await self._create_sender(dc_id)
        download = DownloadSender(
            self.client,
            dc_id,
            sender,
            file,
            byte_offset + index * part_size,
            part_size,
            stride,
        )
        destination = getattr(file, "size", None)
        if destination is not None:
            download.file_size = int(destination)
        elif part_count > 0:
            download.file_size = byte_offset + part_count * part_size
        self.senders.append(download)
        return download

    async def _init_download(
        self,
        file: TypeLocation,
        part_size: int,
        stride: int,
        byte_offset: int,
        part_count: int,
    ):
        # inferred: interleaved sender assignment follows offset/stride fields.
        created = []
        connections = len(self.senders) or self._get_connection_count(
            int(getattr(file, "size", 0) or (part_count * part_size)),
        )
        connections = max(1, min(connections, max(1, part_count)))

        def get_part_count(index: int) -> int:
            if index >= part_count:
                return 0
            return max(0, math.ceil((part_count - index) / connections))

        for index in range(connections):
            if get_part_count(index) <= 0:
                break
            created.append(
                await self._create_download_sender(
                    file,
                    index,
                    part_size,
                    stride,
                    part_count,
                    byte_offset,
                )
            )
        return created

    async def _create_upload_sender(
        self,
        file_id: int,
        part_count: int,
        big: bool,
        index: int,
        stride: int,
    ) -> UploadSender:
        sender = await self._create_sender(self.client.session.dc_id)
        upload = UploadSender(
            self.client,
            sender,
            file_id,
            part_count,
            big,
            index,
            stride,
            asyncio.get_running_loop(),
        )
        self.senders.append(upload)
        return upload

    async def _init_upload(
        self,
        connections: int,
        file_id: int,
        part_count: int,
        big: bool,
    ) -> None:
        connections = max(1, min(int(connections), max(1, int(part_count))))
        stride = connections
        created = await asyncio.gather(
            *(
                self._create_upload_sender(
                    file_id,
                    part_count,
                    big,
                    index,
                    stride,
                )
                for index in range(connections)
            )
        )
        if len(created) != connections:
            raise RuntimeError("parallel upload sender initialization failed")

    async def init_upload(
        self,
        file_id: int,
        file_size: int,
        part_size_kb=None,
        connection_count=None,
    ):
        file_size = max(0, int(file_size or 0))
        if file_size <= 0:
            raise ValueError("file_size must be positive")
        part_size = _normalize_part_size(
            up_load_part_size_kb if part_size_kb is None else part_size_kb,
            file_size,
        )
        part_count = max(1, math.ceil(file_size / part_size))
        is_large = file_size > TG_LARGE_FILE_THRESHOLD
        connections = self._get_connection_count(
            file_size,
            max_count=int(connection_count or self.MAX_CONNECTION_COUNT),
        )
        connections = max(1, min(connections, part_count))
        self.part_size = part_size
        self.part_count = part_count
        self.is_large = is_large
        self._upload_index = 0
        await self._init_upload(connections, int(file_id), part_count, is_large)
        return self

    async def upload(self, data):
        # inferred: choose the least-used sender for the next part.
        self.upload_ticker.clear()
        for _ in range(len(self.senders)):
            available = [
                sender
                for sender in self.senders
                if sender.count * sender.stride + sender.index < sender.part_count
            ]
            if not available:
                break
            sender = min(available, key=lambda item: item.count)
            result = await sender.next(bytes(data))
            if result is not None:
                self._upload_index += 1
                self.upload_ticker.set()
                return result
        raise RuntimeError("no upload sender accepted the file part")

    async def finish_upload(self):
        # inferred: all parts are awaited by upload(); this is a consistency gate.
        pending = [getattr(sender, "_pending", None) for sender in self.senders]
        waiting = [task for task in pending if task is not None]
        if waiting:
            await asyncio.gather(*waiting, return_exceptions=True)
        if self._upload_index != self.part_count:
            raise ValueError(
                f"uploaded part count mismatch: {self._upload_index}/{self.part_count}"
            )
        return True

    async def download(
        self,
        file: TypeLocation,
        file_size: int,
        part_size_kb=None,
        connection_count=None,
        byte_offset: int = 0,
        download_length=None,
    ) -> AsyncGenerator[bytes, None]:
        # inferred: queueing preserves byte order while sender reads stay parallel.
        file_size = max(0, int(file_size or 0))
        byte_offset = int(byte_offset or 0)
        if byte_offset < 0 or byte_offset % 1024:
            raise ValueError(
                f"byte_offset must be a non-negative 1KB multiple: {byte_offset}"
            )
        available = max(0, file_size - byte_offset)
        download_length = _tg_normalize_limit(
            available if download_length is None else download_length,
            available,
        )
        if download_length <= 0:
            return
        part_size = _normalize_part_size(
            down_load_part_size_kb if part_size_kb is None else part_size_kb,
            file_size,
            download_length,
        )
        part_count = max(1, math.ceil(download_length / part_size))
        connections = self._get_connection_count(
            download_length,
            max_count=int(connection_count or self.MAX_CONNECTION_COUNT),
        )
        connections = max(1, min(connections, part_count))
        stride = part_size * connections
        created = await self._init_download(
            file,
            part_size,
            stride,
            byte_offset,
            part_count,
        )
        for sender in created:
            sender.file_size = min(sender.file_size, file_size) if sender.file_size else file_size

        queue: asyncio.Queue = asyncio.Queue()
        worker_errors = []

        async def worker(sender: DownloadSender) -> None:
            try:
                while not getattr(Working, "need_stop", False):
                    data = await sender.next()
                    if not data:
                        break
                    part = max(0, (sender.last_offset - byte_offset) // part_size)
                    await queue.put((part, data))
                if getattr(Working, "need_stop", False):
                    worker_errors.append(
                        RuntimeError("Parallel download stopped by user")
                    )
            except BaseException as exc:
                worker_errors.append(exc)
                raise
            finally:
                await queue.put(None)

        workers = [asyncio.create_task(worker(sender)) for sender in created]
        pending_chunks = {}
        next_part = 0
        finished = 0
        try:
            while finished < len(workers):
                item = await queue.get()
                if item is None:
                    finished += 1
                    continue
                part, data = item
                pending_chunks[part] = data
                while next_part in pending_chunks:
                    chunk = pending_chunks.pop(next_part)
                    Logger.debug("Part %s downloaded", next_part)
                    next_part += 1
                    yield chunk
            while next_part in pending_chunks:
                chunk = pending_chunks.pop(next_part)
                next_part += 1
                yield chunk
            if worker_errors:
                raise worker_errors[0]
        except asyncio.CancelledError:
            for task in workers:
                task.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
            raise
        finally:
            for task in workers:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
            await self._cleanup()


async def _internal_transfer_to_telegram(
    client: TelegramClient,
    response,
    progress_callback=None,
):
    # inferred: buffer-to-part mapping follows the recovered local variables.
    file_id = helpers.generate_random_long()
    file_size = getattr(response, "size", None)
    if file_size is None:
        file_size = helpers.get_file_size(response)
    file_size = int(file_size or 0)
    if file_size <= 0:
        raise ValueError("cannot upload an empty file")

    part_size = _normalize_part_size(up_load_part_size_kb, file_size)
    part_count = max(1, math.ceil(file_size / part_size))
    is_large = file_size > TG_LARGE_FILE_THRESHOLD
    uploader = ParallelTransferrer(client)
    await uploader.init_upload(file_id, file_size, up_load_part_size_kb)
    hash_md5 = hashlib.md5()
    buffer = bytearray()
    data_read = 0
    try:
        async for chunk in file_to_stream(response, part_size):
            buffer.extend(chunk)
            hash_md5.update(chunk)
            data_read += len(chunk)
            while len(buffer) >= part_size:
                data = bytes(buffer[:part_size])
                del buffer[:part_size]
                await uploader.upload(data)
                if progress_callback is not None:
                    result = progress_callback(data_read, file_size)
                    if inspect.isawaitable(result):
                        await result
        if buffer:
            await uploader.upload(bytes(buffer))
        await uploader.finish_upload()
    finally:
        await uploader._cleanup()

    name = getattr(response, "name", None) or "unnamed"
    if is_large:
        return InputFileBig(id=file_id, parts=part_count, name=name)
    return InputFile(
        id=file_id,
        parts=part_count,
        name=name,
        md5_checksum=hash_md5.hexdigest(),
    )


async def download_file(
    client: TelegramClient,
    location: TypeLocation,
    out: BinaryIO = None,
    progress_callback: Optional[Awaitable] = None,
    max_bytes: Optional[int] = None,
    byte_offset: int = 0,
    **kwargs,
):
    # inferred: ``file=`` alias keeps compatibility with the recovered
    # FastDownUpLoadUtils wrapper while the body uses the decompiled ``out``.
    if out is None:
        out = kwargs.pop("file", None)
    if kwargs:
        unknown = ", ".join(sorted(kwargs))
        raise TypeError(f"unexpected download_file arguments: {unknown}")
    if out is None:
        raise ValueError("out is required")

    byte_offset = int(byte_offset or 0)
    if byte_offset < 0 or byte_offset % 1024:
        raise ValueError(
            f"byte_offset must be a non-negative 1KB multiple: {byte_offset}"
        )

    file_size = getattr(location, "size", None)
    normalized_location = location
    if not hasattr(location, "dc_id"):
        normalized_location = utils.get_input_location(location)
        if file_size is None:
            file_size = getattr(location, "size", None)
    if file_size is None:
        raise ValueError("unable to determine the Telegram document size")
    file_size = int(file_size)
    download_length = _tg_normalize_limit(
        file_size - byte_offset if max_bytes is None else max_bytes,
        file_size - byte_offset,
    )
    if download_length <= 0:
        return 0

    written = 0
    auth_retried = False
    while True:
        downloader = ParallelTransferrer(client)
        try:
            async for chunk in downloader.download(
                normalized_location,
                file_size,
                down_load_part_size_kb,
                None,
                byte_offset,
                download_length,
            ):
                out.write(chunk)
                written += len(chunk)
                if progress_callback is not None:
                    result = progress_callback(written, download_length)
                    if inspect.isawaitable(result):
                        await result
                if written >= download_length:
                    break
            return written
        except _AUTH_KEY_ERRORS:
            if auth_retried:
                raise
            auth_retried = True
            _invalidate_client_dc_auth(
                client,
                int(getattr(normalized_location, "dc_id", 0) or client.session.dc_id),
            )
            if hasattr(out, "seek"):
                out.seek(byte_offset)
            written = 0
        except asyncio.CancelledError:
            raise


def _open_upload_source(file):
    if isinstance(file, (str, bytes, os.PathLike)):
        handle = open(file, "rb")
        return handle, int(os.path.getsize(file))
    return None, None


async def upload_file(
    client: TelegramClient,
    file,
    progress_callback=None,
):
    # inferred: use Telethon's normalizer when available, otherwise wrap a
    # plain seekable file object.
    handle, file_size = _open_upload_source(file)
    response = file
    close_after = handle is not None
    if handle is not None:
        response = handle
    try:
        normalizer = getattr(client, "_file_to_upload", None)
        if normalizer is not None and handle is None:
            normalized = normalizer(file)
            if inspect.isawaitable(normalized):
                normalized = await normalized
            if normalized is not None:
                response = normalized
        if getattr(response, "size", None) is None:
            if file_size is None:
                if not hasattr(response, "seek") or not hasattr(response, "tell"):
                    raise ValueError("upload source must be seekable or a filesystem path")
                position = response.tell()
                response.seek(0, os.SEEK_END)
                file_size = response.tell()
                response.seek(position)
            try:
                response.size = file_size
            except AttributeError:
                # inferred compatibility wrapper for plain file objects
                class _UploadSource:
                    def __init__(self, source, size):
                        self._source = source
                        self.size = size
                        self.name = getattr(source, "name", "unnamed")

                    def read(self, size=-1):
                        return self._source.read(size)

                response = _UploadSource(response, file_size)
        return await _internal_transfer_to_telegram(
            client,
            response,
            progress_callback,
        )
    finally:
        if close_after:
            handle.close()
