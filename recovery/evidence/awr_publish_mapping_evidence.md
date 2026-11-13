# AutoWorkerWrapper 发布映射恢复证据

仅静态证据；未执行目标及 `static_*.exe`。

## 函数身份

`0x5a13240_publish_record_init.c` 通过 Nuitka 初始化表建立函数指针/名称
关联：

- `src.py.com.yun.mao.record.PublishIdRecord` 初始化 RVA `0x5a13240`。
- `sub_145AB8FE0`（`0x5ab8fe0`）是 `_append_if_complete_inner`。
- `sub_145A0F220`（`0x5a0f220`）是 `append_if_complete`。
- `sub_145A76170`（`0x5a76170`）是 `_commit_mapper_item`。
- `sub_145A73DA0`（`0x5a73da0`）是 `resolve_record_lists`。

## 调用点

`agent-notes/decompiled/targets/0x51619d0_awr_foreach_body.c`：

- 全局 `append_if_complete` 查找位于第 5368-5396 行附近；
- 四参数调用位于第 5410-5432 行附近；
- 参数为 `auto`、`parse`、`group_result` 和
  `getattr(argsWrapper, "convert_mode", None)`；
- 恢复出的错误路径打印 `记录发布 ID 映射失败：` 并继续分组循环。

## Mapper 构造

`agent-notes/decompiled/targets/0x5ab8fe0_pir_append_inner.c` 构造：

- `time = utils.get_format_time()`；
- `mode = mode_text_of(convert_mode)`；
- `source = build_message_link(source_cfg, source_first_id)`；
- `dest = _build_link_list(dest_cfgs, dest_lookup)`；
- `preview = _build_link_list(preview_cfgs, preview_lookup)`，仅用于 preview
  结果类型。

`resolve_record_lists` 返回 `(type_text, dest_cfgs, preview_cfgs)`；
`type_text` 来自 `type_text_of(auto.auto_type)`。

`_commit_mapper_item` 存储一行包装后的 JSONL
`{kid, name, type, mapper_item}`。`lookup_dest_links_for_source` 从内存或
磁盘读取该包装内容，并匹配 `mapper_item.source` 与 `kid`。

## 剩余边界

`_source_first_id` 以及源消息没有 id 时的确切回退属于行为层面的内容。
Mapper 键、四参数调用和包装结构有静态证据支撑。
