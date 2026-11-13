# 离线协议实验室

这个目录只做**静态恢复树上的离线协议模拟**，不参与正式源码树、`MANIFEST.json`、
pytest 或任何打包流程。

## 安全边界

- 不启动 `运营猫.exe`、`static_hybrid*.exe` 或任何恢复入口。
- 不连接真实授权服务器、Telegram 或其他外网服务。
- 不生成真实卡密、不伪造真实 RSA 签名、不使用真实账号数据。
- 脚本把 `socket.create_connection` 和 `aiohttp.ClientSession` 替换为抛错 stub；
  所有响应来自 `fixtures/synthetic_responses.json`。
- 进入业务函数前调用 `sanitized.neutralize.apply()`，关闭反调试、关机和勒索入口。

## 运行

```powershell
cd D:\reverse_ENV\workspace\operater-cat
D:\reverse_ENV\.venv\Scripts\python.exe .\offline_protocol_lab\run_lab.py
```

输出写入 `offline_protocol_lab/run-output.json`，不会写入 `recovered_src`。

## 当前覆盖

1. `SjkCli.sjk_lq_qd()`：模拟授权引导响应，验证 `isSuccess` 分支。
2. `_sq_r_qi` 心跳入口：模拟 `r_spi`，把合成账号报告送入 `hy_jx_bc()`。
3. `ItemMemStore.bootstrap_item_memory()`：记录云端条目空/非空分支的入参。
4. `s_b_i_kaishi()` 的非 UI 核心路径：确认心跳之后仍会进入 `sq_jy_ma()`
   登录路径。`_sq_qi` 顶层直接 import PyQt5，当前 venv 没装，因此 lab 不导入
   这个 UI 包装模块，而是复刻同一段非 UI 调用顺序。
5. `_sq_r_ca.convert_batch_with_retry()`：记录转换请求体和返回条目，观察
   `sign_batch`、`kid` 的后处理。

## 已发现的恢复树契约问题

- `_sq_r_qi._apply_user_from_remote()` 先把外层响应的 `data` 解包，再调用
  `_sq_chk.hy_jx_bc()`；但 `hy_jx_bc()` 的恢复体第一行是 `data = oj["data"]`，
  因此直接传入内层账户字典会抛 `KeyError('data')`。
- 为了继续观察下游，`run_lab.py` 在 lab 内加了一个 `hy_jx_bc` shim：只在入参
  没有 `data` 键时包一层 `{"data": ...}`。该 shim 不属于恢复源码，也不修改
  `recovered_src`。

## 限制

- 真实响应需要服务端 RSA 私钥签名；本实验在 transport 边界注入合成结果，
  不代表可以伪造能通过真实验签的响应。
- `qd_r_spi_boot()` 在恢复树里直接调用异步 `_spi_fetch()` 而没有 `await`，
  因此脚本用同步 stub 替换 `_spi_fetch()`，这是为了隔离验证，不是修复源码。
- 本实验只能证明“字段如何被消费、分支如何走”，不能证明真实服务端返回值的
  业务含义；真实数据仍需合法授权或完整 mock 服务端。
