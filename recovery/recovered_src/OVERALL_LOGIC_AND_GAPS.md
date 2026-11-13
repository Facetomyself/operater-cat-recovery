# 整体逻辑与缺口清单

## 文档定位

这份文档是 `operater-cat 9.6.3` 恢复树的顶层导航，不替代 `semantic/` 中的
细节文档。它解决三个问题：

1. 整个程序从启动到业务执行的主链路是什么。
2. 现在已经有哪些文档、证据和测试，分别覆盖到哪一层。
3. 哪些地方仍是推断、契约不一致或必须服务端下发，下一步该补什么。

证据等级沿用 `semantic/README.md`：

- `exact`：名称、字段、常量或签名有静态元数据/运行时常量确认。
- `high`：控制流、字段映射或调用边界有多项静态证据。
- `inferred`：行为级重建，不声称逐字节等于原始源码。

当前基线：368 个源文件、3127 个函数、262 个类、20 份语义文档、
455 个离线用例；`_re/validate_all.py` 通过。

## 一句话结论

恢复树已经能解释“程序怎么组织、调用谁、需要什么数据”，但还不能宣称
“所有行为都与原程序逐字节一致”。尤其是账号能力、心跳条目、执行票据、
订单支付和外部 Telegram/AI 服务，仍然存在服务端数据或真实运行时依赖。

## 分层总图

```text
┌─────────────────────────────────────────────────────────────┐
│ UI 层                                                        │
│ MainWindow、tab.*、dialog.*、tray、QRunnable 任务、Qt signal │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 业务/运行时层                                                │
│ auto.*、monitor.*、telefast.*、login.*、record.*、remember.* │
│ proxy.*、config.*、log.*                                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 协议层                                                        │
│ _sjk_cli、_sq_req、_sq_r_req、_sq_r_ca、_sq_bao、_sq_zw      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 领域/状态层                                                  │
│ SqJqm、DTopClass、AutoBeanXXX、ItemMemStore、ParseBean       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 配置/密码/安全层                                             │
│ TwCtx、_tw_ceng、_jmpz_cy、_my_gk、_my_r_gk                  │
│ FdsHhx、_fds_*、_fdg_*、隐藏命令和勒索路径                   │
└─────────────────────────────────────────────────────────────┘
```

这不是严格单向依赖：UI 会直接读取 `SqJqm`，worker 会直接调用
`_sq_r_ca`，安全层也会在协议调用前后插入探针。分层图只用于阅读和排缺口。

## 主链路

### 1. 启动与入口门禁

```text
QApplication
  -> SqQiTask.run()
     -> qd_qi_dong()
        -> FdsHhx 启动探针 / qd_cl_jg()
        -> s_b_i_kaishi()
           -> qd_r_spi_boot()
              -> _spi_fetch() -> r_spi
              -> _apply_user_from_remote() -> hy_jx_bc()
              -> ItemMemStore.bootstrap_item_memory()
           -> 有 ucode: sq_jy_ma() 登录
           -> 无 ucode: sq_zc() 注册
```

关键点：

- `FdsHhx` 反调试/反分析路径在启动链前面，真实目标未纳入验证循环。
- `qd_r_spi_boot()` 是同步函数，但恢复体直接调用异步 `_spi_fetch()` 而没有
  `await`；这是当前恢复树的已知契约问题，详见下文 P0。
- `s_b_i_kaishi()` 在心跳之后仍然会走登录/注册请求，心跳不是启动终点。
- `PyQt5` 是完整 UI 启动的运行时依赖；当前 venv 未安装，离线实验不导入
  `_sq_qi` 的 UI 包装层。

### 2. 授权引导与加密配置

```text
SjkCli.sjk_lq_qd()
  -> sjk_zz_hb(version, exe_hash)
  -> AES-CBC 加密 + RSA 包装（v1c / v2k）
  -> response / sign 校验
  -> 服务端返回 rk / 授权数据

TwCtx
  -> _ENCRYPTED_STATIC_KEY
  -> _ENCRYPTED_CONFIGS
     -> _p_dh（主机）、_f_pk（请求公钥）、_r_pk（票据/HMAC）
     -> _r_u、_v_*、_s_* 等配置
```

关键点：

- `_sjk_cli` 的传输常量是 120 秒总超时、30 秒连接超时、4 次引导重试、
  1.5 秒退避，可重试状态为 `{408, 425, 429, 500, 502, 503, 504}`。
- `TwCtx` 的 B/C/D 层和内嵌配置目录是硬依赖；当前恢复树的敏感层是占位符，
  `TwCtx.tw_jm_ok()` 会失败关闭，`tw_hq_by_k()` 会抛 `RuntimeError`。
- 原程序是否每次都需要服务端 `rk` 取决于构建时静态密文能否由内嵌层解开；
  `rk` 是可参与解密的输入，但“配置密钥必须补齐”这一点不变。

### 3. 账号报告、心跳和条目

`SqJqm` 是内存账户对象，字段来自服务端 `data`：

- 身份：`ucode`、`status`、`grade`、`limit`
- 时间：`hours`、`startTime`、`endTime`、`remainingSec`、`expire`
- 能力：`hasExperi`、`experiDuration`、`botAbility`、`aiAbility`、`mul`
- 服务元数据：`sendAtName`、`keFu`、`cloudBot`、`maoContacts`、
  `priceConfig`、`modelList`、`apiKey`

`r_spi` 请求恢复出的字段为：

```text
uCode, instance_id, cfg_ver, item_hash
```

`qd_r_spi_boot()` 成功后会：

1. 用 `hy_jx_bc()` 构造新的 `SqJqm` 并写入 `current_account_info`。
2. 用 `ItemMemStore.bootstrap_item_memory()` 应用云端条目快照。
3. 在启动链后续继续调用 `sq_jy_ma()` 或 `sq_zc()`。

条目快照的本地/云端结构：

```text
{scheduler, autoMap, globalAdWrapper, water}
```

云端传输为 `base64(gzip(JSON))`；脏状态使用代际计数器，只有响应代际匹配时
才清除本地 dirty 标志。

### 4. 执行票据与转换

```text
_sq_r_ca.convert_batch_with_retry()
  -> build_convert_items()
  -> r_ca 请求
  -> 服务端返回 ordered items + sign_batch + ticket
  -> q_m3_seal()
  -> 给条目补 sign_batch
  -> kid 转 bytes

AutoBeanXXX.parse_wire()
  -> 校验 batch_id / exp / server_nonce / sign_batch
  -> 重建 ExecutionTicket / exec_obj
  -> compute_af(exec_obj) == ticket.af
  -> _verify_sign_item(kid, auto_type, ticket)
  -> ensure_valid(ucode)
  -> gy_wc_hx() 写入 _g0/_g1/_gx
```

`_lk_gy_w` 的三段 HMAC 载荷为：

```text
A | batch_id | kid | auto_type | exp
B | sign_item[:32] | ticket.uc_hash | sha256(ucode) | kid | ticket.mode
C | etid | sn | af | kid | auto_type
```

关键点：去卡密只能让本地门禁通过；没有服务端签发的 ticket/sign_batch，
转换批次和自动执行链路不能自然产生有效票据。

### 5. 业务执行层

- `auto.AutoWorker`：动态 fetch/parse 状态机、随机/递增重试、停止检查。
- `auto.AutoWorkerWrapper`：组级结果、发送计数、广告/保护内容、发布映射。
- `auto.FlowProcess` / `YunProcess` / `BanYunProtect` / `DownLoadProcess`：
  文本、媒体、预览、下载和云端发布分支。
- `monitor.*` / `telefast.*`：Telegram 监控、watchdog、限速和快速传输。
- `login.SessionLoader` / `login.NetTest` / `mthread.*`：
  session、自动登录、连通性测试和长期 worker。
- `record.*` / `remember.*` / `ad.*`：发布记录、评论复制账本、广告映射、
  随机桶和 remember 映射。
- `ai.*` / `prices.*` / `fea.*_file`：AI 文本、订单/支付、迁移/激活和解析任务。

## 现有文档盘点

### 语义文档

| 文档 | 已覆盖内容 | 主要边界 |
| --- | --- | --- |
| `semantic/README.md` | 语义层入口、证据等级、恢复状态 | 导航，不含实现细节 |
| `semantic/domain-model.md` | `SqJqm`、`RemoteHb`、`ItemMemStore`、`DTopClass`、订单/解析实体 | 字段模型精确，生命周期边界为推断 |
| `semantic/license-flow.md` | 启动、机器码、授权报告、账户刷新、item bootstrap | 端点/服务端语义部分推断 |
| `semantic/card-key-analysis.md` | `.code`、AES/RSA 信封、HMAC A/B/C、`ensure_valid`、复现步骤 | 真实服务端密钥和票据仍不可得 |
| `semantic/order-and-item-flow.md` | 订单、检查/充值、迁移、激活、条目脏数据 | 服务端业务语义未闭环 |
| `semantic/parse-pipeline.md` | 消息摘要、计划组装、`ParseBean`、频道/评论解析 | 网络执行不在离线测试内 |
| `semantic/proof-ledger.md` | SHA-256/HMAC 证明帧、`_Cap`、kid ring、`_pl_wd_file` | `_tg` 操作数顺序为推断 |
| `semantic/auto-flow-and-workers.md` | Worker 结果契约、flow 家族、首帧封面 | 媒体/发布分支部分推断 |
| `semantic/monitor-and-telefast.md` | 监控跟进、watchdog、限速器、快速传输 | DC 认证和 flood 细节为推断 |
| `semantic/runtime-services.md` | mthread、login、proxy、record、remember、config、log | 生命周期/时序边界部分推断 |
| `semantic/ui-controllers-and-tabs.md` | tab controller、业务对话框、页面 family | UI 布局和持久化细节推断 |
| `semantic/ui-resource-reconstruction.md` | 生成 `Ui_Form`/`Ui_MainWindow`、widget/布局边 | 绝对几何和文本度量推断 |
| `semantic/ui-text-inventory.md` | `retranslateUi` 文本池和配对边界 | 文本度量/部分隐藏控件 |
| `semantic/anti-debug-catalogs.md` | 检测 catalog、消息表、探测节奏、七条 `_fds_tan` 链 | 反调试辅助函数仅静态 |
| `semantic/malicious-logic-analysis.md` | 反调试、关机、隐藏命令、勒索代码块 | 仅静态，绝不执行 |
| `semantic/obfuscated-packages.md` | `bz_uc`、`kv_nx`、`rm_qh`、`wp_jt` 分派 | 命令操作数顺序和脱敏值为推断 |
| `semantic/risk-boundaries.md` | 反调试/关停链、动态 `exec`、隐藏文件、安全规则 | 安全边界文档，不是实现细节 |
| `semantic/coverage-matrix.md` | 模块族到文档/测试/证据的映射 | 导航矩阵 |
| `semantic/engineering.md` | 测试、依赖、manifest、审计清单 | 工程流程，不含业务语义 |
| `semantic/recovery-status.md` | exact/high/inferred 范围、门禁状态 | 状态快照，会随代码变化 |

### 顶层与实验文档

| 文档 | 作用 |
| --- | --- |
| `README.md` | 恢复树入口、计数、关键文件导航 |
| `COVERAGE.md` | loader、AST、测试、UI、审计的覆盖率 |
| `RECOVERY_NOTES.md` | 恢复方法、加载表突破、置信度、优先级队列 |
| `SOURCE_RECOVERY_PLAN.md` | 当前状态和剩余恢复计划 |
| `decompiled/README.md` | Hex-Rays 输出与 Python 重建的层次说明 |
| `decompiled/anti_debug_map.md` | 反调试列表和响应层级 |
| `sanitized/README.md` | 可逆无害化层和启用方式 |
| `../offline_protocol_lab/README.md` | 离线协议实验的安全边界和覆盖范围 |
| `../offline_protocol_lab/findings.md` | 合成 `sjk_lq_qd`、`r_spi`、`r_ca` 的结果 |
| `../offline_protocol_lab/run-output.json` | 最近一次离线实验的机器可读输出 |

## 缺口清单

### P0：影响恢复结论正确性，应先确认

| 缺口 | 现有证据 | 需要补什么 |
| --- | --- | --- |
| `_apply_user_from_remote()` 与 `hy_jx_bc()` 入参不一致 | `offline_protocol_lab/run-output.json` 记录 `KeyError: 'data'` | 确认哪一侧是原始契约；在文档中固定 envelope 形状；修复前不要把心跳账号写入视为可信 |
| `qd_r_spi_boot()` 调用异步 `_spi_fetch()` 未 `await` | `fea/_sq_r_qi.py` 恢复体 | 明确 sync/async 边界；验证启动心跳是否实际生效；在测试中覆盖 coroutine 分支 |
| `TwCtx._ENCRYPTED_STATIC_KEY` 仍是占位符/不可解密 | `link/_tw_ctx.py`、`link/_jmpz_cy.py`；`tw_jm_ok()` 失败关闭 | 补齐真实层密钥或把整个配置目录标为“外部提供”；记录哪些功能依赖 `_p_dh`、`_f_pk`、`_r_pk` |
| 当前环境没有 PyQt5，`_sq_qi` 不能直接导入 | lab 第一次运行 `ModuleNotFoundError` | 在工程文档中区分“源码恢复”和“运行时依赖”；离线 harness 不使用 UI 包装层 |

### P1：协议与数据契约，决定“去卡密后还剩什么”

| 缺口 | 现有线索 | 需要补什么 |
| --- | --- | --- |
| `sjk_lq_qd` 的真实请求体和响应形状 | `_sjk_cli`、`_sjk_bao`、lab 参数记录 | 逐字段表：版本、exe hash、AES/RSA、`response/sign`、`rk`、错误码 |
| `r_spi` 的响应语义 | `_sq_r_qi`、`_sq_r_bao`、lab 输出 | 顶层 `isSuccess/item/is_register/data` 的字段字典；空/非空 item、注册/登录分支 |
| `r_ca` 的 ticket/wire 契约 | `_sq_r_ca`、`AutoBeanXXX`、`_lk_gy_w` | `sign_batch`、`kid`、`af`、`uc_hash`、`exec`、`beanLike` 的字段表和签名载荷 |
| `r_ui`、`r_roi`、`r_spui` 等路径 | `_sq_r_req` 的 endpoint 包装器 | 每个端点的请求/响应字段、重试和终态策略 |
| `parse_report` 的 status 语义 | `fea/_sq_chk.py` | status `0/1` 为什么返回 `None`；其他状态如何映射 `SqJqm` |
| `SqJqm` 能力字段的业务含义 | `domain-model.md`、`MainWindow` 显示逻辑 | `grade`、`hasExperi`、`aiAbility`、`botAbility`、`mul`、`remainingSec` 的 UI/worker 影响表 |
| 订单、充值、迁移、激活 | `order-and-item-flow.md`、`_sq_bao` | 请求体字段、响应状态、价格配置、`remainingSec` 变化 |
| 主机/证书固定 | `_sq_zw`、`_tw_ctx` | dev/prod 主机、证书指纹、失败缓存和回退顺序 |

### P2：行为级推断，影响“功能是否全正常”

| 缺口 | 现有文档 | 需要补什么 |
| --- | --- | --- |
| UI 绝对几何和七个 dyna 编辑对话框 | `ui-resource-reconstruction.md` | 用 Designer `.ui`/布局边补几何；保留推断标记 |
| 媒体、水印、预览、首帧封面 | `auto-flow-and-workers.md` | FFmpeg/ImageMagick 参数、失败回退、临时文件清理 |
| Telegram session、自动登录、DC、flood | `runtime-services.md`、`monitor-and-telefast.md` | 状态机、重试/封禁/断开路径、与 worker 的信号顺序 |
| AI 员工、API key、模型列表 | `domain-model.md`、`MainWindow` | 能力开关、无 key 分支、模型选择、失败记录 |
| 混淆包命令操作数顺序 | `obfuscated-packages.md` | 逐入口的 argv/权限/回退表；仅静态验证 |
| 发布记录、评论账本、remember/random bucket | `runtime-services.md` | 文件卷轮转、代际、并发和恢复边界 |
| 代理/网络配置 | `runtime-services.md` | SOCKS5 三元组、启停、失败回退 |

### P3：工程化与可验证性

| 缺口 | 需要补什么 |
| --- | --- |
| 协议字段字典 | 新增 `semantic/protocol-contracts.md`，每个字段带来源、类型、示例和证据等级 |
| 可复用离线 harness | 扩展 `offline_protocol_lab` 到 `parse_wire`、登录、订单；保持不联网 |
| 负向测试 | 缺失字段、错误签名、过期 `exp`、错误 `uc_hash`、空 item、重试终态 |
| 文档一致性 | 把计数、P0/P1 缺口和文档链接纳入检查，避免 `RECOVERY_NOTES` 再次漂移 |
| 证据追踪 | 每个协议结论附 RVA/常量/运行时常量或测试文件，不只写“推断” |

## 已有内容的强度

已经比较扎实的部分：

- 模块、类、函数名称和签名：loader/init 表与 492/1167 覆盖审计。
- 领域字段和构造契约：`DTopClass`、`SqJqm`、`ItemMemStore`、`RemoteHb`。
- UI widget 名称、类型和布局边：生成 `Ui_Form`/`Ui_MainWindow` 与审计。
- 反调试 catalog、消息表、七条探测链和响应阈值。
- 卡密本地文件、HMAC A/B/C、`AutoBeanXXX` 票据校验和可逆无害化。
- 发布记录、评论账本、remember/random bucket 的离线往返。
- 455 个离线用例、`validate_all.py` 的 compileall/manifest/UI/import/
  signature/dispatch/constructor 审计。

仍然薄弱的部分：

- 真实服务端响应形状和字段语义。
- `r_ca` 票据签名、`r_spi` 心跳、登录/注册/订单的真实业务状态。
- 媒体、Telegram、AI 运行时的真实网络和失败路径。
- UI 绝对几何、隐藏控件和 Designer 资源的历史差异。
- 目标程序的反调试/关机/勒索路径只能静态分析，不能执行验证。

## 推荐下一步

1. **先处理 P0 文档和契约**：把 `hy_jx_bc` 入参、`qd_r_spi_boot` async 边界、
   `TwCtx` 配置密钥写成明确契约，不要先把推断当结论。
2. **补 P1 协议字段字典**：新增 `semantic/protocol-contracts.md`，覆盖
   `sjk_lq_qd`、`r_spi`、`r_ca`、登录/注册/订单。
3. **扩展离线 lab**：在 `offline_protocol_lab` 内增加 `parse_wire`、登录失败、
   订单状态和空/脏 item 的合成用例，仍不联网。
4. **再做 P2 行为文档**：优先 Telegram session、AI 能力开关、媒体回退和
   UI 几何，不要一开始就追求全部函数逐字节一致。
5. **最后更新导航**：同步 `README.md`、`COVERAGE.md`、`coverage-matrix.md`
   和 `recovery-status.md`，把“已覆盖/推断/缺失”保持一致。

## 验收标准

当下面几条同时成立时，才能说“整体逻辑已经理清”：

- 每个模块族都有语义文档和至少一个离线证据/测试。
- P0 项要么修复，要么在文档中明确标为未解决并解释影响。
- P1 每个远程端点都有请求字段、响应字段、错误/重试策略和示例 fixture。
- P2 的推断项有边界说明，不把行为级重建写成 exact。
- `offline_protocol_lab` 不联网、不启动目标、不接触真实账号。
- `pytest -q` 为 455 个用例通过，`validate_all.py` 保持 `validation OK`。

## 相关证据

- `recovered_src/semantic/`
- `recovered_src/COVERAGE.md`
- `recovered_src/RECOVERY_NOTES.md`
- `recovered_src/SOURCE_RECOVERY_PLAN.md`
- `recovered_src/agent-notes/`
- `offline_protocol_lab/README.md`
- `offline_protocol_lab/findings.md`
- `offline_protocol_lab/run-output.json`
