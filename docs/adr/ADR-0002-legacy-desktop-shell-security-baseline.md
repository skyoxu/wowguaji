---
ADR-ID: ADR-0002
title: LegacyDesktopShell 安全基线（历史，已被 Godot 安全基线替代）
status: Superseded
decision-time: '2025-08-17'
deciders: [架构团队, 安全团队]
archRefs: [CH02]
depends-on: []
depended-by: []
supersedes: []
superseded-by: [ADR-0019]
impact-scope: []
verification: []
monitoring-metrics: []
executable-deliverables: []
test-coverage: ''
---

# ADR-0002: LegacyDesktopShell 安全基线（历史）

## Status

本 ADR 已被 `docs/adr/ADR-0019-godot-security-baseline.md` 替代，仅保留为迁移历史与对照记录。

当前 `wowguaji` 模板运行时为 Godot 4.5 + C#（Windows-only），不包含 LegacyDesktopShell/Electron/Web 容器相关实现。

## Guidance（Current）

- 安全口径以 `docs/adr/ADR-0019-godot-security-baseline.md` 与 `docs/architecture/base/02-security-baseline-godot-v2.md` 为准。
- 外链/网络/文件/权限相关的实现与测试必须遵循 ADR-0019，并将审计与测试产物写入 `logs/**`（日志与工件口径见 `docs/architecture/base/03-observability-sentry-logging-v2.md` 与 `AGENTS.md` 的 6.3）。

## Why keep this file

- 用于解释“旧容器模型（CSP/contextIsolation/nodeIntegration 等）为什么不适用于 Godot”。
- 防止在新模板中误用旧目录/旧脚本/旧测试路径，导致安全口径漂移与门禁失效。

## References

- `docs/adr/ADR-0019-godot-security-baseline.md`
- `docs/adr/ADR-0011-windows-only-platform-and-ci.md`
- `docs/architecture/base/02-security-baseline-godot-v2.md`
