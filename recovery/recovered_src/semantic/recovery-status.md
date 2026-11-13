# 恢复状态

## 精确或高置信度

- Loader 表中的 app/resource 条目：`357/357` 均有对应源文件。
- 精确函数名：`492/492`；类方法：`1167/1167`。
- `module_index.json`：357 个条目，315 个正文，31 个包，
  11 个常量，0 个空条目。
- `DTopClass` bean 的 dataclass 字段集与编译后的 `__init__` varnames 匹配
  （`CommentRuleBean`、`SuperFlowBean`、`AutoBean` 以及小型 bean）。
- `DTopClassHelper` 的 auto-bean 工厂链和 `dic_to_*` 转换器。
- `AutoBeanXXX.ensure_valid` 的过期/hash/签名检查以及 `parse_wire`
  批量校验。
- `_lk_gy_w` 的 `A|`/`B|`/`C|` HMAC payload 和 `gy_jc_a1..a8` 链。
- `_fds_sj` 已解码 catalog：71 个 stem、9 个 prefix、27 个 module stem、
  29 个 window keyword、308 条消息、六个 abort part。
- `FdsHhx` 探测节奏和 `fh_cj` 响应阈值。
- `_fds_rt` 响应分支和 `_fds_tan` 七链映射。
- `_tw_ceng` 根密钥组装和 `TwCtx` B/C/D 层解包；dev endpoint 和 init
  public-key PEM 均可成功解码。

## 推断或部分恢复

- 最大 `setupUi` 函数的 UI 布局几何（受 Hex-Rays 大小限制）；
  widget 名称、类型和布局边已恢复。
- `CMCode` 和 `VideoWaterUtilsToSmallFile` 中的媒体/水印/预览流水线
  属于行为级重建。
- 混淆包的操作数顺序已由测试固定；内联 `Popen`/权限回退细节仍属推断。
- `_fds_tan` 的 `wb_*` 分支组合以及三个 `_wb_jk_*` kernel32 函数体
  由 code-object 行表和常量重建。
- 七条 `_fds_tan` 探测链都是无参数函数，由 `try_begin_abort()` 控制；
  门禁忙时会直接返回，不会导入任何链步骤。
- `TwCtx` 的静态配置 cipher key（`_ENCRYPTED_STATIC_KEY`）尚未解决；
  `tw_hq_by_k` 会失败关闭。
- 卡密/union-code 链路已归档到 `card-key-analysis.md`；请求 envelope、
  本地 `.code` 读写和 `AutoBeanXXX` 票据校验均可读。

## 门禁

- 在 `recovered_src` 下运行 `python -m pytest -q`：455 个用例。
- `_re/validate_all.py`：compileall、manifest、UI、import、signature、
  dispatch、exact-name、class-method 和 constructor 审计全部通过。
- `src` 范围内的 Ruff `F` 检查通过。

## 安全

本次恢复不包含目标执行、Frida attach、debugger attach 或网络重放。
反调试和关停路径仅为静态证据。
