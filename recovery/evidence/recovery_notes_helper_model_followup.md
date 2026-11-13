# Helper 模型跟进：BaseFilterBean 与 AdvancedFilterBean

## 结论

`gen_base_filter` 返回 **`BaseFilterBean`**，而不是 `AdvancedFilterBean`。

正确的归属与当前恢复出的 `DTopClass.py` 相反：

| 类 | 拥有的字段 |
| --- | --- |
| `BaseFilterBean` | `durationFilterBean`, `sizeFilterBean` |
| `AdvancedFilterBean` | `keepSourceText`, `deleSourceText`, `deleLink`, `filterButton`, `discardNoTextResource`, `chaiZu`, `containWords`, `excludeWords` |
| `DurationFilterBean` | `duration_min`, `duration_max`, `duration_min_second`, `duration_max_second` |
| `SizeFilterBean` | `min`, `max` |

证据：

- `DTopClass` 常量：
  - 在 `gen_base_filter` 使用的类构造边界上，`BaseFilterBean.__init__`
    只有 `durationFilterBean` / `sizeFilterBean`。
  - `AdvancedFilterBean.__init__` 拥有八个通用过滤标志。
  - `DurationFilterBean.__init__` 拥有四个时长字段。
  - `SizeFilterBean.__init__` 拥有 `min` / `max`。
- `DTopClassHelper` 常量：
  - 显示文本读取 `durationFilterBean`、`min`、`max`、`sizeFilterBean`；
  - 通用转换器的 varnames 为
    `('dic', 'keepSourceText', 'deleSourceText', 'deleLink', 'filterButton',
    'discardNoTextResource', 'chaiZu', 'containWords', 'excludeWords')`;
  - `dic_to_baseFilter` 与 `dic_to_advancedFilterBean` 是两个不同的转换器。
- `CommonCode` 仅从 `DTopClass` 导入 `BaseFilterBean`、`DurationFilterBean`、
  `SizeFilterBean`。
- `gen_base_filter` 尾部精确构造：
  1. `DurationFilterBean(duration_min, duration_max)`;
  2. `SizeFilterBean(size_min, size_max)`;
  3. `BaseFilterBean(durationFilterBean, sizeFilterBean)`.

## 补丁字段

```python
@dataclass
class DurationFilterBean:
    duration_min: int = 0
    duration_max: int = 0
    duration_min_second: int = 0
    duration_max_second: int = 0


@dataclass
class SizeFilterBean:
    min: int = 0
    max: int = 0


@dataclass
class BaseFilterBean:
    durationFilterBean: Optional[DurationFilterBean] = None
    sizeFilterBean: Optional[SizeFilterBean] = None


@dataclass
class AdvancedFilterBean:
    keepSourceText: bool = True
    deleSourceText: bool = False
    deleLink: bool = False
    filterButton: bool = False
    discardNoTextResource: bool = False
    chaiZu: bool = False
    containWords: list = field(default_factory=list)
    excludeWords: list = field(default_factory=list)
```

`gen_base_filter` 成功返回：

```python
return BaseFilterBean(
    durationFilterBean=DurationFilterBean(
        duration_min=duration_min,
        duration_max=duration_max,
    ),
    sizeFilterBean=SizeFilterBean(
        min=size_min,
        max=size_max,
    ),
)
```

## 连锁修正

- `AutoBean.keepSourceText/filterButton/containWords/excludeWords/`
  `deleSourceText/deleLink` 必须读取 `self.advancedFilterBean`，而不是
  `self.baseFilter`。
- 时长/体积读取必须使用 `self.baseFilter.durationFilterBean` 和
  `self.baseFilter.sizeFilterBean`。
- `ConfigCommentRuleDialog` 必须构造：
  - `baseFilter = CommonCode.gen_base_filter(...)`；
  - `advancedFilterBean = AdvancedFilterBean(<eight generic fields>)`；
  - 不要把 `baseFilter`、`durationFilterBean` 或 `sizeFilterBean`
    传入 `AdvancedFilterBean`。
- `DTopClassHelper` 转换器必须互换：
  - `dic_to_baseFilter` -> 带嵌套 duration/size 的 `BaseFilterBean`；
  - `dic_to_advancedFilterBean` -> 带八个通用字段的
    `AdvancedFilterBean`。
