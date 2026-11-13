# CommonCode 过滤/解析恢复笔记

针对所需 `CommonCode` 函数的仅静态重建。未启动目标可执行文件，也未运行
payload 脚本。

使用的证据：

- `agent-notes/nuitka_constants.json`
- `agent-notes/source_signatures.json`
- `agent-notes/decompiled/targets/0x5d57b10_CommonCode_match_duration_and_size.c`
- `agent-notes/decompiled/targets/0x5d58b30_cc_sigal_message_filter_by_base.c`
- `agent-notes/decompiled/targets/0x5d58f80_cc_group_has_legal_msg.c`
- `agent-notes/decompiled/targets/0x5d60130_CommonCode_generateFileNameBy.c`
- `agent-notes/decompiled/targets/0x5dfd3f0_CommonCode_random_start_end.c`
- `agent-notes/decompiled/targets/0x5e0e050_CommonCode_contain_duration.c`
- `agent-notes/decompiled/targets/0x5e0e810_CommonCode_message_to_parse_list.c`
- `agent-notes/decompiled/targets/0x5e11110_CommonCode_parse_ids.c`
- `agent-notes/decompiled/targets/0x80e93f0_helper_compare_ranges.c`
- `recovered_src/src/py/com/yun/mao/util/need/CommonCode.py`
- `recovered_src/src/py/com/yun/mao/util/need/utils.py`
- `recovered_src/src/py/com/yun/mao/util/need/AllBeanDef.py`

## 签名矩阵

| 函数 | varnames 元组 | 提议签名 | 返回 |
|---|---|---|---|
| `match_duration_and_size` | `('message', 'baseFilter', 'size_mb', 'duration')` | `(message, baseFilter)` | `bool` |
| `sigal_message_filter_by_base` | `('message', 'baseFilter')` | `(message, baseFilter)` | `bool` |
| `group_has_legal_msg` | `('messages', 'baseFilter', 'max_duration_message', 'max_size_message')` | `(messages, baseFilter)` | `bool` |
| `generateFileNameBy` | 一个文本/名称参数 | `(text)` | `str` |
| `contain_duration` | 一个文本/名称参数 | `(messages)` | `bool` |
| `message_to_parse_list` | `('messages', 'msg', 'id_to_objs', 'obj', 'uId', 'new_obj_list', 'objs', 'tart_text', 'tart_message', 'msg_ids', 'new_obj')` | `(messages)` | `list[ParseBean]` |
| `parse_ids` | `('parse',)` | `(parse)` | `list[int]` |
| `random_start_end` | `('count', 'top_num', 'exclude_ranges', 'source', 'entry_kid', 'pick_persisted_range', 'step_length', 'random_end', 'excludes', 'max_random_tries', '_', 'start', 'end', 'slot', 'fine_step')` | `(count, top_num, exclude_ranges=None, source=None, entry_kid=None)` | `tuple[int, int]` |

`match_duration_and_size`、`sigal_message_filter_by_base` 和
`group_has_legal_msg` 都采用双参数的公开形态。`group_has_legal_msg`
有两个额外局部变量：`max_duration_message` 和 `max_size_message`。

## match_duration_and_size 函数

提议实现：

```python
def match_duration_and_size(message, baseFilter) -> bool:
    size_mb = mediaSize(message)
    duration = getVideoDuration(message)
    if duration:
        duration_filter = baseFilter.durationFilterBean
        return duration_filter.min <= duration <= duration_filter.max
    size_filter = baseFilter.sizeFilterBean
    return size_filter.min <= size_mb <= size_filter.max
```

证据与控制流映射：

- 反编译开头将 `a3[0]` 读取为 message，将 `a3[1]` 读取为 `baseFilter`。
- 源码第 1083 行的第一个调用是 `mediaSize(message)`，并存入
  `size_mb`。
- 源码第 1084 行的第二个调用是 `getVideoDuration(message)`，并存入
  `duration`。
- `if duration:` 的假分支进入体积比较块。
- true 分支访问 `baseFilter.durationFilterBean`，然后访问字段
  `min` 和 `max`。
- false 分支访问 `baseFilter.sizeFilterBean`，然后访问字段
  `min` 和 `max`。
- 两个比较都使用 `0x80E93F0` 处的 helper，其错误文本为
  `"'<=' not supported between instances of ..."`；因此源码比较是
  `min <= value <= max`，而不是 `<` 或 `>=`。

观察到的确切属性：

- `baseFilter.durationFilterBean`
- `baseFilter.sizeFilterBean`
- `.min`
- `.max`

推断边界：

- 属性名映射 `durationFilterBean` / `sizeFilterBean` 是根据两个不同分支
  以及 `nuitka_constants.json` 索引 40/41 处的 bean 常量推断的。
- `mediaSize(message)` 直接与体积过滤器比较。模块常量在 `size` 旁边包含
  `1024` 和 `2`，因此有效值预期为 MB（例如
  `round(size / 1024 / 1024, 2)`）。当前恢复出的
  `CommonCode.mediaSize` 返回字节；如果这些 bean 基于 MB，就不能原样
  使用。这是依赖问题，不是本文件所做的改动。
- 当前恢复出的 `DTopClass.DurationFilterBean` 暴露
  `duration_min`、`duration_max`、`duration_min_second` 和
  `duration_max_second`，但没有 `min`/`max`。反编译比较对两个 bean
  使用相同的两个字段槽位，因此运行时 bean 必须暴露 `min`/`max`
  （或者 DTopClass 模型需要在本文件之外做单独修正）。

## sigal_message_filter_by_base 函数

提议实现：

```python
def sigal_message_filter_by_base(message, baseFilter) -> bool:
    return match_duration_and_size(message, baseFilter)
```

证据：

- 反编译签名恰好读取两个参数。
- 主体立即用这两个参数调用一个模块级函数，并无分支地返回该结果。
- `source_signatures.json` 提供 varnames 元组 `('message', 'baseFilter')`。
- 该函数名不是生成器或 `any` 包装器；这个双参数调用直接委托给
  `match_duration_and_size`。

无需推断分支。唯一假设是反编译主体中的单个模块全局查找解析到
`match_duration_and_size`；周围调用图和恢复出的源码 stub 都指向该函数。

## group_has_legal_msg 函数

提议实现：

```python
def group_has_legal_msg(messages, baseFilter) -> bool:
    max_duration_message = get_max_duration_message(messages)
    if max_duration_message is None:
        max_size_message = get_max_size_message(messages)
        if max_size_message is None:
            return False
        return sigal_message_filter_by_base(max_size_message, baseFilter)
    return sigal_message_filter_by_base(max_duration_message, baseFilter)
```

证据与控制流映射：

- `source_signatures.json` 的 varnames：
  `('messages', 'baseFilter', 'max_duration_message', 'max_size_message')`。
- 反编译主体先调用 `0x5DF0D40` 处的模块函数，即
  `get_max_duration_message` 的精确主体。
- 如果该结果为 `Py_None`，则调用 `0x5DF19A0` 处的模块函数，即
  `get_max_size_message` 的精确主体。
- 如果体积结果同样为 `Py_None`，反编译代码返回 `Py_False`。
- 否则，将选中的 message 与 `baseFilter` 传给一次双参数调用，与
  `sigal_message_filter_by_base` 匹配。
- 两个 `Py_None` 检查是身份检查，不是 truthiness 检查。不要将它们替换为
  `if not max_duration_message`；有效的 message 对象必须按身份处理。

因此，该函数是“选取最大时长的 message，否则选取最大体积的 message，然后
应用基础过滤器”。它不是遍历每条 message 的循环。

## generateFileNameBy 函数

提议实现：

```python
def generateFileNameBy(text) -> str:
    from . import FileUtils

    return FileUtils.truncate_string(
        utils.sanitize_filename_with_regex(text),
        10,
    )
```

证据：

- 反编译主体调用一个模块函数，然后在其结果上调用一个方法/函数。
- 外层调用是恢复出的 `FileUtils.truncate_string`。
- 内层调用是恢复出的 `utils.sanitize_filename_with_regex`。
- 字面量 `10` 出现在 `CommonCode` 常量表中 `truncate_string` 附近；
  它是截断长度。
- 反编译函数带有常规 Nuitka 异常/展开路径，但没有显式的备用返回值。
  Python 层行为就是上面的直接双调用表达式。

推断边界：

- 除了一参数 code-object 形态之外，确切参数名没有独立恢复；恢复出的源码
  将其称为 `text`。为了补丁兼容性保留该名称。

## contain_duration 函数

提议实现：

```python
def contain_duration(messages) -> bool:
    from ...config import {{SECRET_yiwyjonl}}

    for duration in {{SECRET_yiwyjonl}}.YUAN_SHI_PIN_DURATION:
        if duration in messages:
            return True
    return False
```

证据与确切常量：

- 反编译主体将一个参数读入 `v4`，并迭代
  `{{SECRET_yiwyjonl}}.YUAN_SHI_PIN_DURATION`。
- 成员检查是 `PySequence_Contains(v4, item)`，因此源码操作是
  `item in messages`（参数是右侧容器），而不是 `messages in item`。
- 首次命中返回 `True`，循环结束后返回 `False`。
- `nuitka_constants.json` 给出确切配置列表：
  `['原视频时长', '完整版', '视频时长', '完整版']`。
- 恢复出的源码 stub 使用相同循环和参数名 `messages`；该参数语义上是
  文本 blob，但重命名会破坏使用恢复 API 的现有调用方。

除正常循环提前返回之外，没有推断其他分支。

## message_to_parse_list 函数

提议实现：

```python
def message_to_parse_list(messages):
    from .AllBeanDef import ParseBean

    id_to_objs = {}

    for msg in messages:
        if not msg:
            continue

        uId = getattr(msg, "grouped_id", None)
        if uId is None:
            uId = getattr(msg, "id")

        if uId not in id_to_objs:
            id_to_objs[uId] = []
        id_to_objs[uId].append(msg)

    new_obj_list = []
    for uId, objs in id_to_objs.items():
        tart_text, tart_message = getGroupTextAndMessage(objs)
        msg_ids = [getattr(obj, "id") for obj in objs]
        new_obj = ParseBean(
            uId,
            objs,
            tart_text,
            tart_message,
            msg_ids,
        )
        new_obj_list.append(new_obj)

    return new_obj_list
```

证据与控制流映射：

- 该函数有一个参数，并将 `id_to_objs` 构建为字典。
- 第一个循环检查 `bool(msg)`，跳过假值条目。
- 它读取 `msg.id`，然后读取 `msg.grouped_id`；如果 `grouped_id` 不是
  `None`，该值会替换 id 作为分组键。反编译测试是 `is not None`，
  因此 `grouped_id == 0` 仍然是键。
- 仅在键不存在时用 `[]` 创建桶，然后追加 message。这等价于
  `id_to_objs.setdefault(uId, []).append(msg)`，但保留了观察到的显式
  成员分支。
- 第二个循环迭代 `id_to_objs.items()`；每个值对应一个 `uId` 的有序
  message 列表。
- `getGroupTextAndMessage(objs)` 返回二元组。反编译代码将其解包为
  `tart_text` 和 `tart_message`。
- 随后它迭代同一组 `objs`，并从每个 `obj.id` 构建 `msg_ids`。
- 它按 `AllBeanDef.ParseBean` 使用的顺序，用五个位置值构造
  `ParseBean`：`uniId`、`messages`、`tart_text`、
  `tart_message`、`original_msg_ids`。
- 返回的列表是 `new_obj_list`。

所需依赖形态：

`getGroupTextAndMessage(messages)` 必须返回
`(tart_text, tart_message)`。当前恢复出的
`CommonCode.getGroupTextAndMessage(uni_id, messages)` 只返回字符串，
且签名不同；这是既有不匹配。反编译调用方传入一个参数并解包两个值，
因此本笔记将正确契约视为一参数、返回元组的形式。

`ParseBean` 必须接受上述五个位置字段。恢复出的
`AllBeanDef.ParseBean` 首先声明这五个字段，因此在那里进行位置构造是
有效的。

## parse_ids 函数

提议实现：

```python
def parse_ids(parse):
    ids = []
    for message in parse.messages:
        ids.append(message.id)
    return ids
```

证据：

- 反编译签名是一个参数。
- 它读取 `parse.messages`，迭代结果，读取每项的 `id`，并追加到新建列表。
- 它原样返回该列表。
- `source_signatures.json` 给出 varnames 元组 `('parse',)`。
- 当前恢复出的源码已有相同主体，但参数名是 `messages`；这里使用 `parse`
  以匹配 varnames 证据。

没有推断分支。反编译主体中没有排序、去重、过滤或整数转换。

## random_start_end 函数

提议实现：

```python
def random_start_end(
    count,
    top_num,
    exclude_ranges=None,
    source=None,
    entry_kid=None,
):
    start = 0
    end = int(top_num)

    if source and entry_kid:
        from ...remember.RandomBucketManager import pick_persisted_range

        picked = pick_persisted_range(
            source,
            entry_kid,
            count,
            top_num,
        )
        if picked is not None:
            start, end = picked
            if (int(start), int(end)) != (0, int(top_num)):
                return int(start), int(end)

    excludes = exclude_ranges or []
    top_num = max(0, int(top_num))
    count = max(1, int(count))

    step_length = auto_correct_step_length(
        top_num,
        max(100, top_num // count),
    )
    random_end = (
        (top_num // step_length) * step_length
        if step_length
        else 0
    )

    max_random_tries = 64
    for slot in range(max_random_tries):
        start = random.randint(
            0,
            max(0, random_end - step_length),
        )
        end = min(top_num, start + step_length - 1)
        if not _random_range_conflicts(start, end, excludes):
            return start, end

    fine_step = 8
    print(
        "随机模式：可尝试 ID 窗口已基本用尽（已记录 "
        + str(len(excludes))
        + " 段），本轮回退纯随机"
    )
    start = random.randint(0, top_num)
    end = min(top_num, start + fine_step)
    return start, end
```

证据与控制流映射：

- 确切签名和默认形态来自 `source_signatures.json` 的 varnames，以及
  `nuitka_constants.json` 中的 `(None, None, None)` 默认值。
- 第一个受保护分支先测试 `source` 的 truthiness，再测试
  `entry_kid` 的 truthiness。
- 当两者都为真时，主体导入
  `src.py.com.yun.mao.remember.RandomBucketManager`，解析
  `pick_persisted_range`，并在本地随机回退之前调用它。
- 随后用 `exclude_ranges or []` 规范化 `exclude_ranges`。
- 使用由 `top_num` 和 `count` 派生的步长调用
  `auto_correct_step_length`；字面量 `100` 是常量组中的最小步长。
- `random_end` 用作窗口上界。
- `_random_range_conflicts` 是循环守卫；helper 常量
  `_random_ranges_overlap`、`start` 和 `end` 位于同一常量组。
- 字面量 `64` 和 `8` 出现在同一常量组；实现将它们分别赋给
  `max_random_tries` 和 `fine_step`。
- 确切日志字符串由两个常量拼接而成：
  `随机模式：可尝试 ID 窗口已基本用尽（已记录 ` 和
  ` 段），本轮回退纯随机`。

该函数的推断边界：

- 持久化范围分支形态置信度高：反编译代码仅在 `source` 和
  `entry_kid` 都为真时执行导入和调用。
- `pick_persisted_range` 使用的确切哨兵值未由恢复出的现代实现证明；
  该实现在耗尽时返回 `(0, top_num)`。因此上面的 `(0, top_num)` 比较是
  兼容性守卫，不是反编译字面量。
- `100`、`64`、`8` 和 `4` 的算术角色是根据它们在常量组中的位置推断的。
  特别是字面量 `4` 出现在该组中，但其确切源码用途尚未解决；在四个常量
  与源码行号匹配之前，不要把回退重试次数当作精确值。
- 纯随机回退后的最终返回在此重建中不会重新检查
  `_random_range_conflicts`。反编译尾部构造二元组并返回；如果调用方需要
  最终冲突复检，那属于尚未解决的尾部。

## 补丁集成说明

- 这些函数目前并不以这些确切主体存在于
  `recovered_src/src/py/com/yun/mao/util/need/CommonCode.py`；其中一些
  只有近似 stub。
- 不要添加 `async` 关键字。全部八个反编译主体都是普通同步函数。
- `match_duration_and_size` 假设运行时 bean 形态为
  `baseFilter.durationFilterBean.min/max` 和
  `baseFilter.sizeFilterBean.min/max`。应用补丁前先验证该形态；恢复出的
  DTopClass 模型与之不一致。
- `message_to_parse_list` 需要一参数、返回元组的
  `getGroupTextAndMessage`；恢复出的源码当前暴露的是双参数、返回字符串
  的变体。
- `random_start_end` 在函数内部惰性导入 `RandomBucketManager`，与反编译
  导入分支一致，并避免模块加载时的导入循环。

## 验证

- 已执行的静态交叉检查：varnames、函数名、源码行号、`Py_None` 身份检查、
  `PySequence_Contains`、`<=` helper 错误文本、`ParseBean` 字段顺序，以及
  确切的 `YUAN_SHI_PIN_DURATION` 列表。
- 运行时验证：按指令未执行。
- 未运行目标可执行文件；未修改 `recovered_src`。
