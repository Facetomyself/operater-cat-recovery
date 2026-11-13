# CommonCode 辅助函数恢复笔记

范围：`src.py.com.yun.mao.util.need.CommonCode`

使用的输入：

- `agent-notes/nuitka_constants.json`
- `agent-notes/source_signatures.json`
- `agent-notes/function_name_map_exact.json`
- `agent-notes/decompiled/targets/0x5d5e160_CommonCode_str_id_tip.c`
- `agent-notes/decompiled/targets/0x5d6e690_CommonCode_real_time_increase_params.c`
- `agent-notes/decompiled/targets/0x5d6f9d0_CommonCode_parseVideoDuration.c`
- `agent-notes/decompiled/targets/0x5d70000_CommonCode_parseVideoIndex.c`
- `agent-notes/decompiled/targets/0x5d70630_CommonCode_globalPicWater.c`
- `agent-notes/decompiled/targets/0x5d70cc0_CommonCode_globalVideoWater.c`
- `agent-notes/decompiled/targets/0x5d71350_CommonCode_privatePicWater.c`
- `agent-notes/decompiled/targets/0x5d71860_CommonCode_privateVideoWater.c`
- `agent-notes/decompiled/targets/0x5e007c0_CommonCode_findAutoBeanBySource.c`
- `agent-notes/decompiled/targets/0x5d785d0_CommonCode_obtain_comment_to_id.c`
- `agent-notes/decompiled/targets/0x5dc50f0_CommonCode_gen_base_filter.c`
- `recovered_src/src/py/com/yun/mao/util/need/CommonCode.py`
- `recovered_src/src/py/com/yun/mao/util/need/AllBeanDef.py`
- `recovered_src/src/py/com/yun/mao/dclass/DTopClass.py`
- `recovered_src/tests/test_commoncode_recovered_helpers.py`

置信度图例：

- `high`：签名与行为由 `co_varnames`、常量、反编译分支和/或现有测试确认。
- `medium`：签名已确认，但一个属性名或一个异常分支是推断的。
- `low`：只能恢复外层形态；不要当作精确结论。

## 现有模块级常量/导入

`CommonCode.py` 已定义：

```python
VIDEO_DURATION_TIERS = (60, 180, 300, 600, 1800, 3600, 5400, 7200, 9000)
```

恢复出的模块已经导入了 `utils`、`datetime`、`random`、`time` 和
`asyncio`。`parseVideoDuration` 与 `parseVideoIndex` 复用现有的
`VIDEO_DURATION_TIERS` 常量。它们属于 `CommonCode`；较早的重建还曾把它们
复制到 `NewConfig`，这是错误的，现已移除。

---

## 1. str_id_tip 函数

签名：`str_id_tip(last_id, diff_dan_wei) -> str`

置信度：`high`

证据：

- `co_varnames` 元组 `('last_id', 'diff_dan_wei')`。
- 反编译第 1387/1388/1390 行根据 `last_id > 0` 分支。
- 常量 `"最后"`、`"ID："`、`"ID没有变化"`。
- 现有测试期望 `"最后12ID：13"` 和 `"最后0ID没有变化"`。

提议实现：

```python
def str_id_tip(last_id, diff_dan_wei) -> str:
    if last_id > 0:
        return "最后" + str(last_id) + "ID：" + str(diff_dan_wei)
    return "最后" + str(last_id) + "ID没有变化"
```

返回形态：`str`。

分支：

- `last_id > 0`：在 `"ID："` 后包含差值。
- 否则：始终报告 `"ID没有变化"`，包括 `last_id == 0`
  且 `diff_dan_wei != 0` 的情况。
- 非数值 `last_id` 的类型错误不会被原始代码捕获。

---

## 2. parseVideoDuration 函数

签名：`parseVideoDuration(index) -> int`

置信度：`high`

证据：

- `co_varnames` 元组 `('index',)`。
- 反编译第 1838-1854 行是一串相等测试。
- 常量中的档位值：`60, 180, 300, 600, 1800, 3600, 5400, 7200, 9000`。
- 现有测试覆盖每个档位以及 `99 -> 60` 回退。

提议实现：

```python
def parseVideoDuration(index) -> int:
    for tier_index, duration in enumerate(VIDEO_DURATION_TIERS):
        if index == tier_index:
            return duration
    return 60
```

返回形态：`int` 秒。

分支：

- 相等命中：返回匹配的档位时长。
- 未命中：返回 `60`（由反编译第 1854 行和测试确认）。
- 原始代码使用 `==` 比较；不会用 `int(index)` 强制转换字符串索引，
  因此该实现有意保留相等测试。

---

## 3. parseVideoIndex 函数

签名：`parseVideoIndex(duration) -> int`

置信度：`high`

证据：

- `co_varnames` 元组 `('duration',)`。
- 反编译第 1861-1877 行将 duration 与同样的九个档位比较。
- 返回档位索引 `0..8`；未匹配的值返回 `0`。
- 现有测试覆盖往返转换以及 `99 -> 0` 回退。

提议实现：

```python
def parseVideoIndex(duration) -> int:
    for tier_index, tier_duration in enumerate(VIDEO_DURATION_TIERS):
        if duration == tier_duration:
            return tier_index
    return 0
```

返回形态：`0..8` 范围内的 `int`。

分支：

- 相等命中：返回对应索引。
- 未命中：返回 `0`（由反编译第 1877 行和测试确认）。

---

## 4. privatePicWater 函数

签名：`privatePicWater(water)`

置信度：行为 `high`；参数名 `water` 为 `high`。

证据：

- `co_varnames` 元组 `('water',)`。
- 反编译 `0x5d71350` 第 117-155 行：
  - `None` -> 返回常量 `(False, '')`。
  - 否则读取 `enPic` 属性并测试 truthiness。
  - 为真 -> 构造二元组 `(True, water)`。
- 模块常量中存在常量 `(False, '')`。
- 现有测试期望 `(True, top)` / `(False, "")`。

提议实现：

```python
def privatePicWater(water):
    if water is not None and water.enPic:
        return True, water
    return False, ""
```

返回形态：`(bool, Water | str)`。

分支：

- `water is None`：`(False, "")`。
- `water.enPic` 为真：`(True, water)`。
- `water.enPic` 为假：`(False, "")`。
- 缺少 `enPic` 时原始代码抛出 `AttributeError`；没有使用 `getattr`
  默认值。

---

## 5. privateVideoWater 函数

签名：`privateVideoWater(water)`

置信度：`high`

证据：

- 形态与 `privatePicWater` 相同，但反编译 `0x5d71860` 读取不同的
  `enVideo` 属性（常量索引 `476`）。
- 为假时返回相同的 `(False, '')` 哨兵值。

提议实现：

```python
def privateVideoWater(water):
    if water is not None and water.enVideo:
        return True, water
    return False, ""
```

返回形态：`(bool, Water | str)`。

分支：

- `water is None`：`(False, "")`。
- `water.enVideo` 为真：`(True, water)`。
- `water.enVideo` 为假：`(False, "")`。

---

## 6. globalPicWater 函数

签名：`globalPicWater(top)`

置信度：行为 `high`；防御性 `top is None` 守卫为 `medium`，因为反编译主体
开头直接读取 `top.topArgs`。

证据：

- `co_varnames` 元组 `('top',)`。
- 反编译 `0x5d70630`：
  - 读取 `top.topArgs`。
  - 如果 `top.topArgs.water is None` -> `(False, '')`。
  - 重新读取 `top.topArgs.water.enPic`；为真 -> `(True, top.topArgs.water)`。
- 与私有 helper 相同的 `(False, '')` 哨兵值。
- 现有测试传入一个包含 `topArgs.water` 的 `top`。

提议实现：

```python
def globalPicWater(top):
    if top is None:
        return False, ""
    if top.topArgs.water is None:
        return False, ""
    if top.topArgs.water.enPic:
        return True, top.topArgs.water
    return False, ""
```

返回形态：`(bool, Water | str)`。

分支：

- `top is None`：防御性 `(False, "")`（推断）。
- `topArgs.water` 缺失/为 None：`(False, "")`。
- `water.enPic` 为真：`(True, water)`。
- 否则：`(False, "")`。

实现说明：原始表达式会两次求值 `top.topArgs.water`。如果该属性有副作用，
保留重复属性访问是有意的；对普通 dataclass/namespace 而言，只赋值一次在
行为上等价。

---

## 7. globalVideoWater 函数

签名：`globalVideoWater(top)`

置信度：`high`

证据：

- 形态与 `globalPicWater` 相同，但反编译 `0x5d70cc0` 读取
  `top.topArgs.water.enVideo`。

提议实现：

```python
def globalVideoWater(top):
    if top is None:
        return False, ""
    if top.topArgs.water is None:
        return False, ""
    if top.topArgs.water.enVideo:
        return True, top.topArgs.water
    return False, ""
```

返回形态：`(bool, Water | str)`。

分支：与 `globalPicWater` 相同，只是使用 `enVideo`。

---

## 8. real_time_increase_params 函数

签名：`real_time_increase_params(auto, new_start_id) -> None`

置信度：`high`

证据：

- `co_varnames` 元组 `('auto', 'new_start_id')`。
- 反编译第 1815/1816/1817 行：
  - 调用 `auto.set_increase_startId(new_start_id)`。
  - 调用 `LoadDataClass.addOrUpdate(auto)`。
  - 调用 `signals.global_ui_signal.update_increase_auto_bean.emit(auto)`。
- 常量包括 `set_increase_startId`、`LoadDataClass`、`addOrUpdate`、
  `signals`、`global_ui_signal`、`update_increase_auto_bean`、`emit`。
- 调用方 `AutoWorker.py` 传入 `(mem_auto, new_start_id)`。

提议实现：

```python
def real_time_increase_params(auto, new_start_id) -> None:
    auto.set_increase_startId(new_start_id)
    from ...dclass import LoadDataClass
    from . import signals

    LoadDataClass.addOrUpdate(auto)
    signals.global_ui_signal.update_increase_auto_bean.emit(auto)
```

返回形态：`None`。

分支：

- 没有本地条件分支。三次调用产生的异常会向外传播。
- 该函数不返回 bean，也不返回更新后的 params。

---

## 9. findAutoBeanBySource 函数

签名：`findAutoBeanBySource(safeSource, all_legal_auto_beans)`

置信度：`medium`

证据：

- `co_varnames` 元组
  `('safeSource', 'all_legal_auto_beans', 'tart', 'auto', 'channel_part', '_')`。
- 反编译 `0x5e007c0` 创建结果列表，迭代第二个参数，调用
  `utils.parse_source_parts(...)`，解包二元结果，在第 1470 行执行成员测试，
  并在第 1471 行比较一个属性。
- 恢复出的 monitor 调用点使用
  `finder(safeSource, self.all_legal_auto_beans)`，并回退到检查
  `auto.getSource()`、`utils.parse_source_parts(...)` 和 `auto.safeSource`。
- 第二次比较的属性名解析在反编译输出中并非完全精确；`safeSource`
  属性是最强匹配。

提议实现：

```python
def findAutoBeanBySource(safeSource, all_legal_auto_beans):
    targetBeans = []
    for auto in all_legal_auto_beans or ():
        getter = getattr(auto, "getSource", None)
        source = getter() if callable(getter) else getattr(auto, "source", "")
        tart = utils.parse_source_parts(source)
        channel_part = tart[0] if tart else None
        if safeSource in (source, channel_part):
            targetBeans.append(auto)
            continue
        if getattr(auto, "safeSource", None) == safeSource:
            targetBeans.append(auto)
    return targetBeans
```

返回形态：`list[AutoBean]`（可能为空）。

分支：

- `source` 或解析后的频道部分等于 `safeSource`：追加该 bean。
- `auto.safeSource == safeSource`：追加该 bean。
- 不匹配：跳过该 bean。
- `or ()` 守卫是防御性的；反编译代码直接迭代参数，对 `None` 会抛出
  `TypeError`。

---

## 10. obtain_comment_to_id 函数

签名：`obtain_comment_to_id(ids)`

置信度：`high`

证据：

- `co_varnames` 元组 `('ids',)`。
- 类型注解常量：`{'ids': 'typing.List[int]'}`。
- 反编译 `0x5d785d0`：
  - `ids is None` -> `None`。
  - 精确 `type(ids) is not list` -> 原样返回 `ids`。
  - 空列表 -> `None`。
  - 非空列表 -> `ids[0]`。
- 现有测试：`[4, 5] -> 4`、`7 -> 7`、`None -> None`。

提议实现：

```python
def obtain_comment_to_id(ids):
    if ids is None:
        return None
    if type(ids) is not list:
        return ids
    if not ids:
        return None
    return ids[0]
```

返回形态：`int | list | None`，其中非列表输入会原样返回。

分支：

- `None`：`None`。
- 非列表：原样返回；包括元组和 list 子类。
- 空列表：`None`。
- 非空列表：第一个元素（即使第一个元素是 `0` 或假值）。

---

## 11. gen_base_filter 函数

签名：

`gen_base_filter(duration_min_str, duration_max_str, size_min_str, size_max_str)`

置信度：签名/校验顺序/返回对象形态为 `high`；
静默的最大时长解析失败分支为 `medium`。

证据：

- `co_varnames` 元组
  `('duration_min_str', 'duration_max_str', 'size_min_str', 'size_max_str',
  'success', 'duration_min', 'duration_max', 'size_min', 'size_max')`.
- 反编译行标记：2095、2099、2103、2107、2111、2115、2119、2123、
  2127, 2132, 2136.
- 常量：
  - `parse_int`
  - `BASE_FILTER_DU_MIN`, `BASE_FILTER_DU_MAX`
  - `BASE_FILTER_SIZE_MIN`, `BASE_FILTER_SIZE_MAX`
  - 最小时长整数错误
  - 带 `~` 和 `" 分钟"` 的时长范围消息
  - 时长最小值大于最大值错误
  - 最小体积整数错误
  - 带 `" MB"` 的体积范围消息
  - 最大体积整数错误
  - 体积最小值大于最大值错误
  - `BaseFilterBean`、`DurationFilterBean`、`SizeFilterBean`
- 反编译尾部构造三个对象，每个对象带两个参数：
  1. 由 `(duration_min, duration_max)` 构造时长 bean；
  2. 由 `(size_min, size_max)` 构造体积 bean；
  3. 由 `(duration_bean, size_bean)` 构造基础 bean。
- 恢复出的配置值：时长范围 `0..6000` 分钟，体积范围
  `0..100000` MB。

提议实现：

```python
def gen_base_filter(
    duration_min_str,
    duration_max_str,
    size_min_str,
    size_max_str,
):
    from ...config import {{SECRET_yiwyjonl}}
    from ...dclass.DTopClass import (
        BaseFilterBean,
        DurationFilterBean,
        SizeFilterBean,
    )

    success, duration_min = utils.parse_int(duration_min_str)
    if not success:
        print("请输入最小时长，单位分钟，需要输入整数！")
        return None
    if (
        duration_min < {{SECRET_yiwyjonl}}.BASE_FILTER_DU_MIN
        or duration_min > {{SECRET_yiwyjonl}}.BASE_FILTER_DU_MAX
    ):
        print(
            f"请输入合理的视频时长过滤范围，范围是："
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_DU_MIN} ~ "
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_DU_MAX} 分钟"
        )
        return None

    success, duration_max = utils.parse_int(duration_max_str)
    if not success:
        # inferred: no max-duration parse-error string exists in the module
        # constants; the decompiled failure path returns None without a print.
        return None
    if (
        duration_max < {{SECRET_yiwyjonl}}.BASE_FILTER_DU_MIN
        or duration_max > {{SECRET_yiwyjonl}}.BASE_FILTER_DU_MAX
    ):
        print(
            f"请输入合理的视频时长过滤范围，范围是："
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_DU_MIN} ~ "
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_DU_MAX} 分钟"
        )
        return None
    if duration_min > duration_max:
        print("请输入合理的视频时长过滤范围，最小值不能大于最大值，单位分钟！")
        return None

    success, size_min = utils.parse_int(size_min_str)
    if not success:
        print("请输入最小体积大小，单位MB，需要输入整数！")
        return None
    if (
        size_min < {{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MIN
        or size_min > {{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MAX
    ):
        print(
            f"请输入合理的资源体积过滤范围，范围是："
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MIN} ~ "
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MAX} MB"
        )
        return None

    success, size_max = utils.parse_int(size_max_str)
    if not success:
        print("请输入最大体积大小，单位MB，需要输入整数！")
        return None
    if (
        size_max < {{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MIN
        or size_max > {{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MAX
    ):
        print(
            f"请输入合理的资源体积过滤范围，范围是："
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MIN} ~ "
            f"{{{SECRET_yiwyjonl}}.BASE_FILTER_SIZE_MAX} MB"
        )
        return None
    if size_min > size_max:
        print("请输入合理的资源体积过滤范围，最小值不能大于最大值，单位MB！")
        return None

    return BaseFilterBean(
        durationFilterBean=DurationFilterBean(
            min=duration_min,
            max=duration_max,
        ),
        sizeFilterBean=SizeFilterBean(
            min=size_min,
            max=size_max,
        ),
    )
```

返回形态：`BaseFilterBean | None`。

分支：

- 任意无效整数或越界值：打印对应消息并返回 `None`。
- `duration_min > duration_max` 或 `size_min > size_max`：打印
  最小值大于最大值消息并返回 `None`。
- 成功：返回包含 `DurationFilterBean` 和 `SizeFilterBean` 的
  `BaseFilterBean`；时长值保持分钟，体积值保持 MB。
- 允许相等（`min == max`）；只有 `min > max` 会被拒绝。

重要集成注意事项：

当前恢复出的 `recovered_src/src/py/com/yun/mao/dclass/DTopClass.py`
没有声明 `BaseFilterBean.durationFilterBean` /
`BaseFilterBean.sizeFilterBean`，且其 `DurationFilterBean` 使用
`duration_min`/`duration_max`，而不是其他恢复调用点使用的 `min`/`max`
名称。反编译 `gen_base_filter` 明确构造嵌套的时长/体积 bean，并将
它们传给第三个双参数构造函数。真正的补丁需要模型定义暴露这些嵌套字段和
`min`/`max`；该文件不在本笔记分配的编辑范围内。若不做该模型修正，
`gen_base_filter` 在结构上正确，但无法与当前恢复出的 `DTopClass.py`
运行时兼容。

---

