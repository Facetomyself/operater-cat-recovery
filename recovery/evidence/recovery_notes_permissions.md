# CommonCode 权限 / topic / stream 恢复笔记

范围：对提供的 Nuitka C 包装器、恢复出的 Python、常量表和函数名映射做
仅静态审查。未运行目标可执行文件或 payload 脚本。未修改 `recovered_src`。

下文使用的置信度标签：

- `[verified]`：签名或分支由包装器参数个数、已解码常量或 Hex-Rays 主体
  直接支持。
- `[inferred]`：调用/分支存在，但确切源码格式或 helper 的分组是根据相邻
  证据重建的。
- `[gap]`：提供的证据止于协程工厂；没有可用主体。

## 共享导入/常量

权限 helper 需要 `src.py.com.yun.mao.util.need.CommonCode` 中存在这些名称：

```python
from telethon.errors import ChannelInvalidError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetForumTopicsByIDRequest
from telethon.tl.types import Channel, ForumTopicDeleted

from . import utils
```

`utils.convertLinkIfNeed` 已在
`recovered_src/src/py/com/yun/mao/util/need/utils.py` 中实现。

相关已解码常量：

- `Channel`, `broadcast`, `post_messages`, `is_admin`, `is_creator`,
  `is_banned`, `participant`, `banned_rights`, `send_messages`,
  `default_banned_rights`.
- `get_input_entity`, `GetForumTopicsByIDRequest`, tuple `('peer', 'topics')`,
  `topics`, `ForumTopicDeleted`, `ChannelInvalidError`.
- `is_broadcast_comment_channel`, `GetFullChannelRequest`, `full_chat`,
  `linked_chat_id`.
- `{'prefix': 'common/check_comment_enable'}`.
- `block`, `执行失败`.

---

## checkSendPermission 函数

包装器参数个数为 4。函数的 varname 元组为：

```text
('name', 'client', 'd', 'me', 'errorMsg', 'entity', 'permissions',
 'can_send', 'participant', 'banned_rights', 'default_banned_rights', 'e')
```

因此可直接打补丁的签名为：

```python
async def checkSendPermission(name: str, client, d, me) -> str:
    ...
```

`[verified]` 该函数返回错误消息字符串，而不是 bool。帧槽初始化为空字符串，
仅有的非空赋值是两条权限错误消息。空字符串表示成功。

`[verified]` 第一个 await 是 `client.get_permissions(d, me)`。结果是
`permissions` 局部变量。`d` 是目标实体；`me` 是当前账号实体。

可直接打补丁的实现：

```python
async def checkSendPermission(name: str, client, d, me) -> str:
    try:
        permissions = await client.get_permissions(d, me)

        if isinstance(d, Channel) and d.broadcast:
            if permissions.post_messages:
                return ""
            return (
                f"当前账号 {name} 的目标频道/群组：{utils.convertLinkIfNeed(d)}"
                " 没有发布消息的权限！！请检查后重试！！"
                "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
                "并且需要具备发消息权限！]"
            )

        if permissions.is_admin or permissions.is_creator:
            return ""

        if permissions.is_banned:
            participant = permissions.participant
            if participant is None:
                return ""
            banned_rights = participant.banned_rights
            if banned_rights is None:
                return ""
            if banned_rights.send_messages:
                return (
                    f"当前账号 {name} 的目标频道/群组：{utils.convertLinkIfNeed(d)}"
                    " 没有发送消息的权限！！请检查后重试！！"
                    "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
                    "并且需要具备发消息权限！]"
                )
            return ""

        default_banned_rights = permissions.default_banned_rights
        if default_banned_rights is None:
            return ""
        if default_banned_rights.send_messages:
            return (
                f"当前账号 {name} 的目标频道/群组：{utils.convertLinkIfNeed(d)}"
                " 没有发送消息的权限！！请检查后重试！！"
                "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
                "并且需要具备发消息权限！]"
            )
        return ""
    except Exception as exc:
        return (
            f"权限检查异常: {name} {exc}"
            " 发生了异常请检查后重试！！"
            "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
            "并且需要具备发消息权限！]"
        )
```

分支说明：

- `[verified]` 广播频道路径检查 `post_messages`；成功时立即退出，不检查
  admin/banned 字段。
- `[verified]` 非广播和非 `Channel` 路径共享
  `is_admin/is_creator/is_banned/participant/banned_rights` 逻辑。
- `[verified]` 在 Telethon 中，`ChatBannedRights.send_messages=True` 表示
  该权限受限。主体根据真值分支，并在为真时发出“没有发送消息的权限”错误。
- `[inferred]` 异常字符串的拼接顺序来自三个已解码片段
  `权限检查异常: `、格式化后的 name/exception，以及
  ` 发生了异常请检查后重试！！[...]`。仅凭 C 包装器无法恢复 `exc`
  周围的确切空格。

---

## topic_exists_safe 函数

包装器参数个数为 3。varname 元组为：

```text
('client', 'group', 'topic_id', 'channel', 'result', 'exists', 'e')
```

可直接打补丁的签名：

```python
async def topic_exists_safe(client, group, topic_id) -> tuple[bool, str | None]:
    ...
```

`[verified]` 该函数执行两个 await：

1. `channel = await client.get_input_entity(group)`
2. `result = await client(GetForumTopicsByIDRequest(peer=channel, topics=[topic_id]))`

`[verified]` 存在性由 `result.topics` 推导：

```python
exists = bool(result.topics) and not isinstance(
    result.topics[0],
    ForumTopicDeleted,
)
```

可直接打补丁的实现：

```python
async def topic_exists_safe(client, group, topic_id) -> tuple[bool, str | None]:
    try:
        channel = await client.get_input_entity(group)
    except Exception:
        return False, f"无法找到群组: {group}"

    try:
        result = await client(
            GetForumTopicsByIDRequest(
                peer=channel,
                topics=[topic_id],
            )
        )
        exists = bool(result.topics) and not isinstance(
            result.topics[0],
            ForumTopicDeleted,
        )
        return exists, None
    except ChannelInvalidError:
        return False, "群组无效或没有权限"
    except Exception as exc:
        return False, f"发生未知错误: {exc} - {group}"
```

分支说明：

- `[verified]` `ForumTopicDeleted` 是已删除 topic 的哨兵值。
- `[verified]` `ChannelInvalidError` 精确映射为
  `(False, "群组无效或没有权限")`。
- `[inferred]` 通用第二异常格式化为
  `发生未知错误: {exc} - {group}`；常量证明前缀和 ` - ` 分隔符，而确切
  操作数顺序来自主体中的两个格式化元组片段。
- `[inferred]` 第一个 await 失败字符串为
  `无法找到群组: {group}`；该分支不保留异常参数。

---

## check_comment_enable 函数

包装器参数个数为 3。varname 元组为：

```text
('channel_part', 'client', 'entity', 'full_channel')
```

可直接打补丁的签名：

```python
async def check_comment_enable(channel_part, client, entity) -> bool:
    ...
```

参数顺序很重要：`channel_part` 在第一位，而不是 `client`。

`[verified]` 第一道门禁是 `is_broadcast_comment_channel(entity)`。
失败时记录 `频道 {channel_part} 不是广播频道，无法按评论区发布` 并返回
`False`。

`[verified]` 成功路径上的请求为：

```python
full_channel = await client(
    GetFullChannelRequest(entity),
    prefix="common/check_comment_enable",
)
```

`prefix` 关键字由已解码字典
`{'prefix': 'common/check_comment_enable'}` 和 call-ex 包装器证明。

可直接打补丁的实现：

```python
async def check_comment_enable(channel_part, client, entity) -> bool:
    if not is_broadcast_comment_channel(entity):
        print(f"频道 {channel_part} 不是广播频道，无法按评论区发布")
        return False

    full_channel = await client(
        GetFullChannelRequest(entity),
        prefix="common/check_comment_enable",
    )
    linked_chat_id = full_channel.full_chat.linked_chat_id
    if linked_chat_id:
        print(
            f"{channel_part} 已开启评论区 "
            f"(评论群组ID: {linked_chat_id})"
        )
        return True
    print(f"{channel_part} 未开启评论区")
    return False
```

分支说明：

- `[verified]` 结果属性链为
  `full_channel.full_chat.linked_chat_id`。
- `[verified]` `linked_chat_id` 为真时返回 `True`；为假时返回 `False`。
- `[inferred]` 仅从调用形态无法确认具体使用 `print` 还是 logger helper；
  恢复出的模块对这些消息使用 `print`。

---

## safe_try_run 函数

包装器参数个数为 1。varname 元组为：

```text
('block', 'result', 'e')
```

可直接打补丁的签名：

```python
async def safe_try_run(block):
    ...
```

`[verified]` 调用 `block` 并 await 其结果。主体中存在 Nuitka 的
`CALL_FUNCTION_0` 加 `GET_AWAITABLE` 模式。

`[verified]` 帧结果初始为 `False`。如果 awaited 结果恰好为 `False`，
主体抛出 `RuntimeError("执行失败")`；该异常随后被 `except Exception`
处理器吞掉，函数返回 `False`。

可直接打补丁的实现：

```python
async def safe_try_run(block):
    try:
        result = await block()
        if result is False:
            raise RuntimeError("执行失败")
        return result
    except Exception:
        return False
```

说明：

- `[verified]` `RuntimeError` 消息恰好是 `执行失败`。
- `[verified]` 主体中没有打印该消息的 `print`；它作为异常载荷使用并被吞掉。
- `[inferred]` `block` 是零参数 awaitable 工厂，不是裸协程对象。主体的
  call-then-await 序列支持 `block()`。

---

## checkEntityIsExist 函数

包装器参数个数为 6。这是唯一一处证据缺口：提供的 C 是 `0x5d671c0` 处的
async 工厂，而 `0x5d67630` 处的主体未包含在内。

最接近的恢复 varname 元组为：

```text
('client', 'auto', 'start_id', 'end_id', 'channel_part', 'topic_id',
 'source_entity')
```

`[inferred]` 参数是前六个名称：

```python
async def checkEntityIsExist(
    client,
    auto,
    start_id,
    end_id,
    channel_part,
    topic_id,
):
    ...
```

六参数个数由工厂验证。名称则根据相邻 varname 元组以及调用方的
source-entity/错误消息常量推断。

保守的可直接打补丁实现：

```python
async def checkEntityIsExist(
    client,
    auto,
    start_id,
    end_id,
    channel_part,
    topic_id,
):
    source = auto.getSource()
    try:
        source_entity = await client.get_input_entity(source)
    except Exception as exc:
        print(
            f"88 发生错误！当前操作的电报账号 "
            f"{channel_part} 的{source}  找不到了，请检查后重试！！"
            "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组！]"
        )
        return None

    if source_entity is None:
        print(
            f"发生错误！{channel_part} 的{source}  找不到了，请检查后重试！！"
            "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组！]"
        )
        return None
    return source_entity
```

`[gap]` 不要把这当作字节级精确结论。主体不在提供的证据中，因此以下问题
尚未解决：

- 调用方期望实体对象、bool，还是 `(entity, error)`；
- `start_id`、`end_id` 或 `topic_id` 是否参与探测；
- 日志 helper 是 `print` 还是 logger；
- 错误语句中确切的账号/名称插值。

如果调用方只检查 truthiness，返回实体是兼容的。如果它解包元组，则必须在
主体反编译后修正该实现。

---

## `_dr_vx_file` 和 `_qf_rn_file` 中的 `_kid_mac`

两个函数的参数个数都是 1。常量表证明相同的 key 配方：

- `_sk`、`_mac`、`_tg`、字面量 `(75,)`、`_kid_key`。
- `[verified]` 调用为
  `_mac(_pl_wd_file._sk, (_tg(75), _kid_key(kid)))`.

两个模块可直接打补丁的实现：

```python
def _kid_mac(kid: str) -> bytes:
    return _mac(_pl_wd_file._sk, (_tg(75), _kid_key(kid)))
```

按模块说明：

- `_dr_vx_file`：解析出的常量位于 `0x1489427E0`（`_sk`）、
  `0x1489427F0`（`_mac`）、`0x148942808`（`_tg`）、`0x148942810`
  （`(75,)`）、`0x148942818`（`_kid_key`）。
- `_qf_rn_file`：解析出的常量位于 `0x148940B60`（`_sk`）、
  `0x148940B70`（`_mac`）、`0x148940B88`（`_tg`）、`0x148940B90`
  （`(75,)`）、`0x148940B98`（`_kid_key`）。
- `[verified]` 两个主体都不包含显式 `assert _sk is not None` 分支。因此
  当前 `_pl_wd_file._kid_mac` 的 assert 是恢复时添加的便利措施，不是这两个
  函数已确认的行为。如果需要严格 parity，应省略该 assert。
- `[inferred]` `_tg(75)` 使用恢复出的 `_tg` 配方
  `((75 * 17) ^ 165) & 0xFF` 计算四个字节，再加上
  `75.to_bytes(2, "big")`，结果为 `b"\x5e\x5e\x5e\x5e\x00\x4b"`。
  除非 `_tg` 本身要被替换，否则继续调用 `_tg(75)`，不要硬编码这些字节。

两个恢复模块中已经存在局部 `_mac`、`_tg` 和 `_kid_key` helper，不应在
`_kid_mac` 内重复实现。

---

## FastTelethon 中的 stream_file

包装器参数个数为 2。默认元组解析为 `(1024,)`，因此确切签名为：

```python
async def stream_file(file_to_stream: BinaryIO, chunk_size: int = 1024):
    ...
```

`[verified]` 主体读取 `file_to_stream.read(chunk_size)`，遇到假值数据时
停止，并逐块产出每个非空 chunk。它是 **async generator**，不是当前
`recovered_src` 中的同步生成器。

可直接打补丁的实现：

```python
from typing import AsyncGenerator, BinaryIO


async def stream_file(
    file_to_stream: BinaryIO,
    chunk_size: int = 1024,
) -> AsyncGenerator[bytes, None]:
    while True:
        data = file_to_stream.read(chunk_size)
        if not data:
            break
        yield data
```

说明：

- `[verified]` 默认值是 `1024`，不是 `1024 * 1024`。
- `[verified]` 该 helper 中没有 `await`；它之所以是 async，只是因为它被
  声明为 async generator。
- `[inferred]` 返回注解是 `AsyncGenerator[bytes, None]`；生成器状态和
  `read` 调用已验证，但原始注解的确切拼写没有。
- 消费者必须使用 `async for`，而不是 `for`。

---

## 打补丁的最终结论

- `checkSendPermission`：用 `-> str` 错误消息逻辑替换 bool stub，参数顺序为
  `(name, client, d, me)`。
- `topic_exists_safe`：返回 `(exists, None)` 或 `(False, error)`，而不是裸
  bool。
- `check_comment_enable`：参数顺序为
  `(channel_part, client, entity)`，并使用
  `prefix="common/check_comment_enable"` 调用 `GetFullChannelRequest`。
- `safe_try_run`：await `block()`，将精确的 `False` 转换为被吞掉的
  `RuntimeError("执行失败")`，并在任何异常时返回 `False`。
- `_dr_vx_file`/`_qf_rn_file` 中的 `_kid_mac`：与 `_pl_wd_file` 相同的
  四常量 HMAC 配方，但不带未验证的 assert。
- `stream_file`：带默认 `chunk_size=1024` 的 async generator。
- `checkEntityIsExist`：仅有包装器证据；提议的六参数实现特意标记为
  inferred/gap。
