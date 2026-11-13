# 领域模型

## 账户与许可证

`fea/_sq_jqm.py` 中的 `SqJqm` 是内存账户对象。字段从服务器的 `data` 对象和
运行时转储恢复：

- 身份：`ucode`、`status`、`grade`、`limit`
- 时间：`hours`、`startTime`、`endTime`、`remainingSec`、`expire`
- 能力：`hasExperi`、`experiDuration`、`botAbility`、`aiAbility`、`mul`
- 服务元数据：`sendAtName`、`keFu`、`cloudBot`、`maoContacts`、
  `priceConfig`、`modelList`、`apiKey`

`SqJqm` 方法只是投影，不做服务器计算：

- `gen_grade_card_str()` 将 grade 映射为显示标签（`游客`/`会员`/`冻结`）。
- `has_ai_ability()` 和 `has_bot_ability()` 将能力标志与 `1` 比较。
- `is_multi_permission()` 读取 `mul` 字段。
- `gen_ka_info()` 对多权限账户返回 `企业版`，否则返回 `个人版`。

`fea/_sq_chk.py` 是边界解析器。`hy_jx_bc(oj)` 校验响应形态，构造 `SqJqm`，
并更新 `current_account_info`/时间戳。`parse_report(oj)` 是报告路径使用的
状态分派器。

## 远程心跳结果

`fea/_r_hb_file.py` 定义 `RemoteHb`：

```text
terminal : bool   # caller must not retry when true
msg      : str    # transport or business error
data     : Any    # decoded business object
```

类方法 `success`、`failed_retry` 和 `failed_terminal` 编码了 `_spi_fetch`、
`_sq_r_ks` 和 `_sq_r_ca` 使用的重试策略。

## 条目快照与流程

`dclass.ItemMemStore` 拥有本地快照：

```text
{scheduler, autoMap, globalAdWrapper, water}
```

云端协议以 base64(gzip(JSON)) 传输该快照。脏状态使用代际计数器：

1. `mark_item_dirty()` 将代际加一。
2. 请求捕获当前代际。
3. `clear_item_dirty_if_generation(generation)` 仅在响应属于该代际时清除标志。

`dclass.LoadDataClass` 是 `DTopClass` 之上的持久化门面。它拥有 `autoMap`
（以 `kid` 为键）、调度器/全局广告状态和水设置。`dclass.DTopClass` 包含
可序列化的流程/自动 bean 及其类型判别符（`AUTO_BEAN_TYPE_*`）。

`dclass.DTopClassHelper.dic_to_Auto_obj` 是线缆/持久化字典入口。它先解包
`beanLike` 载荷，然后根据 `auto_type` 分派到恢复出的工厂：

| `auto_type` | 工厂 | Bean |
| --- | --- | --- |
| 1 | `parse_ban_yun_flow` | `BanYunBean` |
| 2 | `parse_auto_flow_or_yulan_flow` | `AutoFlowBean` |
| 3 | `parse_auto_flow_or_yulan_flow` | `YuLanBean` |
| 4 | `parse_down_load` | `DownLoadBean` |
| 5 | `parse_yun_auto` | `YunAutoBean` |
| 6 | `parse_yun_preview` | `YunPreViewBean` |

这些工厂应用标量身份字段（`kid`、`auto_type`、`priority`、`active`），并
递归重建嵌套 bean。

## 订单与解析实体

- `prices.CreateOrderResponseClass`：订单响应和订单值对象。
- `util.need.AllBeanDef`：可序列化请求/解析 bean（订单、充值、迁移、激活、解析）。
- `fea._xx_zy_file`：消息摘要、trace id 和解析载荷构建器。
- `fea._fs_jh_zb_file`：服务器计划组到 `ParseBean` 对象的映射。
- `fea._yjx_hb_file`：频道/评论心跳结果（`YjxHb`），携带解析 bean 或重试/终止消息。
