---
PRD-ID: PRD-Guild-Manager
Title: 功能纵切 - 公会管理器
Status: Active
ADR-Refs:
  - ADR-0019
  - ADR-0004
  - ADR-0005
  - ADR-0003
Test-Refs: []
---

本页是 wowguaji 的 08 章功能纵切文档，用于约束“公会管理器”模块的边界、契约与验收挂钩。

约束：

- 跨切面口径只引用 Base/ADR，不在本页复制阈值或策略
  - 目标与约束（CH01）：`docs/architecture/base/01-introduction-and-goals-v2.md`
  - 安全基线：见 `docs/architecture/base/02-security-baseline-godot-v2.md` 与 ADR-0019
  - 可观测性与日志（CH03）：`docs/architecture/base/03-observability-sentry-logging-v2.md` 与 ADR-0003
  - 事件/契约：见 ADR-0004；契约 SSoT 落盘在 `Game.Core/Contracts/**`
  - 门禁：见 ADR-0005
- 本模块的 C# 契约与事件类型不得引用 Godot API（可单测）
- 场景与 Glue 逻辑只放在 Godot 层；核心规则放在 Game.Core

功能范围要点（示例）：

- 公会核心：创建/解散/权限角色
- 成员管理：邀请/审批/踢出/角色变更
- 活动系统：团队活动/结算（如有）

测试与验收：

- xUnit：覆盖核心规则、状态机、DTO 映射（建议落在 `Game.Core.Tests/**`）
- GdUnit4：覆盖关键场景加载、Signals 连通与最小可玩闭环（建议落在 `Tests.Godot/**`）
- Test-Refs 只能列出仓库内真实存在的测试文件；不存在的路径不得写入本页 Front-Matter
