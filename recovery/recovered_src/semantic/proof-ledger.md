# 证明账本（`fea._pl_wd_file`）

## 用途

`_pl_wd_file` 是本地证明帧账本，不是 HTTP 传输层。它维护私有 HMAC 密钥、
固定大小的失败队列和少量摘要缓存。AI/CD/report 路径会调用这些函数，
用于在对象写回本地数据存储之前，证明该对象经过预期的请求链到达。

## 帧格式

静态证据确认该帧由四个元素组成：

```text
(nonce: 16 bytes, proof_hash: 32 bytes, mac: 32 bytes, aux: bytes)
```

`_shred(proof)` 对 bytes-like 输入计算 SHA-256。`_mac(key, parts)` 以
`hashlib.sha256` 作为摘要模块，对字节块序列计算 HMAC-SHA256。
`_seal(tag, proof, aux)` 创建随机 16 字节 nonce，并返回
`_Cap(nonce, proof_hash, mac, aux)`；`_unseal(tag, cap)` 检查三个固定长度，
并使用 `hmac.compare_digest` 比较重新计算出的 MAC。

`_kid_key(kid)` 对 UTF-8 kid 计算 SHA-256。`_kid_mac(kid)` 将模块密钥、
`_tg(75)` 与 kid 摘要混合。`_tg` 内部精确的 multiply/xor/and 操作数顺序
仍是从反编译生成器推断的；六字节输出形状以及追加的
`n.to_bytes(2, "big")` 已确认。

## 状态

- `_g_mz` 是模块级可重入锁。
- `_sk` 保存私有 MAC 密钥；`None` 会禁用封装。
- `_ph`、`_c_p`、`_c_q`、`_c_r`、`_c_s` 缓存证明字节串和摘要。
- `_kid_ring` 将 kid 摘要映射到每个 kid 对应的 MAC。
- `_q_fr` 是 `_purge_locked` 和 `_bump_suspect_locked` 使用的失败时间戳队列。

`b_x1_trim()` 是零参数重置例程。恢复源码中额外的可选参数是为更早的行为级
调用方保留的兼容性许可，并非来自原始 code object 的证据。

## 状态映射

`w_cd(chain_ok, kid_ok, gy_ok, uc_ok) -> int` 映射首个失败阶段：

| 阶段 | 结果 |
|---|---:|
| chain | 0 |
| kid | 2 |
| gy | 3 |
| uc | 4 |
| 全部通过 | 9 |

## 安全边界

证明账本本身不执行命令，也不访问网络。其私钥和精确 nonce 字节属于运行时
状态。不要运行原始可执行文件来获取其中任一值；外围 loader 仍包含破坏性的
反分析路径。
