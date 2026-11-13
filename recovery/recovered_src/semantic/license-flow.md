# 许可证与启动流程

## 高层时序

```text
QApplication
  -> SqQiTask / qd_qi_dong
     -> FdsHhx startup probe
     -> qd_cl_jg / entry gate
     -> s_b_i_kaishi
        -> qd_r_spi_boot
           -> _spi_fetch
              -> _sq_r_bao.zq_r_item_hb
              -> _sq_r_req.sq_r_spi
           -> _apply_user_from_remote
              -> _sq_chk.hy_jx_bc
           -> ItemMemStore.bootstrap_item_memory
           -> LoadDataClass.getAutoMap
        -> local register/login fallback through _sq_req
```

## 请求信封

`fea/_sq_req.py` 和 `link/_sjk_cli.py` 实现恢复出的信封：

1. `jm._my_dt.jm_sc_aes_k()` 创建新的 16 字节 AES key。
2. `fea._sq_req.sq_sc_aq_nr(json, key)` 生成
   `iv || AES-CBC-PKCS7(json)`。
3. `fea._sq_req.sq_sc_aes_k(key)` 使用配置的 RSA 公钥和 PKCS1v15 包装 AES key。
4. 出站 JSON 携带 `v1c`（密文 hex）和 `v2k`（包装后的 key hex）。
5. `sq_jm_xy(source, key)` 用公钥校验 `response`/`sign` 对，拆分
   `iv_received`/`ciphertext_received`，解密并解析 JSON。

证据级别：字段名和原语顺序为 `exact`/`high`；常量未暴露字面量的端点特定
包装细节仍为 `inferred`。

## 线缆批量校验

`dclass.AutoBeanXXX.parse_wire` 重建执行票据批量：

1. 读取 `batch_id`、`exp`、`server_nonce`、`sign_batch` 和 `entries`；
2. 用 `_verify_sign_batch` 校验批量签名；
3. 通过 `_ticket_from_wire` 和 `_exec_from_wire` 重建每个条目；
4. 将 `compute_af(exec_obj)` 与票据 `af` 指纹比较；
5. 用 `_verify_sign_item` 校验条目签名；
6. 调用 `ensure_valid(ucode)` 并通过 `gy_wc_hx` 绑定账户。

字段顺序和调用序列来自 `0x5478800` 反编译常量；常量未暴露的精确线缆载荷
字节仍为推断。

## 配置与主机选择

`link/_tw_ctx.py` 拥有加密配置目录：

- `link/_tw_ceng.assem_rk_a()` 从常量区块恢复出的六个 `_KA*` 片段组装
  44 字节根 Fernet key。
- `TwCtx._ensure_built()` 解包 B/C/D 层密钥并解密 init 公钥 PEM。
- `TwCtx.tw_sjk_url()` 返回恢复出的 dev 端点
  `https://birder.jinsiqie.life/xb/iil`。
- `TwCtx.tw_sjk_pk_pem()` 返回请求信封使用的 RSA 公钥。
- 静态配置目录密钥（`_ENCRYPTED_STATIC_KEY`）派生自在许可证引导期间由
  `TwCtx.tw_yy_mk()` 安装的服务器提供根密钥；它不是静态常量。离线时该密钥
  不可用，因此 `TwCtx.tw_hq_by_k(name)` 以 `RuntimeError` 失败关闭，而不是
  返回伪造值。

`fea/_sq_hj.py` 通过 `src.py.version_code` 选择 dev/prod。生产构建为 `9.6.3`，
因此 `hj_prod_ok()` 是正常路径。`fea/_sq_req.py` 将该决策与配置主机组合。

## 本地回退

当远程启动路径无法产生账户时，`fea._sq_qi` 使用 `_sq_req.sq_zc` 或
`_sq_req.sq_jy_ma` 回退到本地注册/登录。这里不推断精确的服务端注册语义；
调用边界和请求构建器已重建。

## Union-code 文件

`fea/_sq_jqm.py` 拥有本地 `.code` / `.code.old` 载荷：

- `zh_code_pth()`：`%APPDATA%/Microsofteis/lang/union_code_release/union_code/.code`
- `zh_old_pth()`：旧的 `.code.old` 同级文件
- `_static_cipher()`：检查 `TwCtx.tw_jm_ok()` 并返回 TwCtx Fernet 实例
- `_zh_rd_code()`：解密文件、解析 JSON、提取 `ucode`、`status`、`grade`、
  `muli`，并更新 `current_account_info`
- `_zh_bc_uc()`：序列化 `{ucode, muli}` 并写入加密载荷
- `_read_ucode_from_legacy_bean()` / `_migrate_legacy_bean_if_needed()`：
  将 `.code.old` 迁移为 `.code`
- `zh_rd_code()` / `zh_jz_xx()` / `zh_sc_wj()`：公开的读取/刷新/写入包装器

`LEGACY_ACCOUNT_INFO_KEY` 的精确 JSON key 保留为脱敏字节常量；载荷 key 名和
迁移顺序从常量/varnames 推断。恢复过程只读写本地数据，不绕过也不伪造远程
许可证响应。
