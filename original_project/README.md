# 原项目归档

`app/` 是原项目 `operater-cat` 的本地整理副本，包含目标可执行文件、DLL、
运行时资源、第三方包和原始 UI 资源。

这个目录不会进入 public git 树：原始文件体积大，且包含第三方软件和二进制。
`BINARY_MANIFEST.json` 记录了被忽略的大文件/二进制路径、大小和 SHA-256。

## 关键文件

- `app/运营猫.exe`：原始目标，执行不安全。
- `app/constant.ini`：运行时常量。
- `app/sitecustomize.py`：启动环境注入。
- `app/ui/`：原始 UI 资源。
- `app/findings.json`、`app/report.md`、`app/triage.md`：分析产物副本。

## 使用规则

- 不要直接运行 `运营猫.exe` 或任何 `static_hybrid*.exe`。
- 只在一次性隔离 VM 中做动态验证，阻断电源 API 和外部网络。
- 公开仓库只保留清单和小型元数据，不提交原始二进制。
