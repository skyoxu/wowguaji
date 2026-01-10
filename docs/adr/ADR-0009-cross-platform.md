---
ADR-ID: ADR-0009
title: 跨平台适配策略（历史，已被 Windows-only 平台策略替代）
status: Superseded
decision-time: '2025-08-17'
deciders: [架构团队, 开发团队, UX团队]
archRefs: [CH01, CH07, CH09, CH11]
depends-on: []
depended-by: []
supersedes: []
superseded-by: [ADR-0011]
impact-scope: []
verification: []
monitoring-metrics: []
executable-deliverables: []
test-coverage: ''
---

# ADR-0009: 跨平台适配策略（历史）

## Status

本 ADR 已被 `docs/adr/ADR-0011-windows-only-platform-and-ci.md` 替代，仅保留为历史记录。

当前 `wowguaji` 模板目标为 Windows-only（运行时、CI、导出与发布），不再维护 macOS/Linux 的兼容策略与 OS 矩阵。

## Guidance（Current）

- 平台范围与 CI 策略以 `docs/adr/ADR-0011-windows-only-platform-and-ci.md` 为准。
- 如未来恢复跨平台，需要新增/替代 ADR 明确目标平台、验证矩阵、性能预算与发布策略，并同步质量门禁脚本与工件规范（见 `docs/architecture/base/07-dev-build-and-gates-v2.md` 与 `AGENTS.md`）。

## References

- `docs/adr/ADR-0011-windows-only-platform-and-ci.md`
- `docs/architecture/base/07-dev-build-and-gates-v2.md`
