# PRD-Guild-Manager 功能纵切验收清单（wowguaji）

## 基本信息

- PRD ID: `PRD-Guild-Manager`
- 功能纵切文档: `docs/architecture/overlays/PRD-Guild-Manager/08/08-Feature-Slice-Guild-Manager.md`
- 口径: Godot 4.5 + C#/.NET 8（Windows-only）

---

## 1) 文档与回链

- [ ] PRD 文档存在且可读：`docs/prd/PRD-WOWGUAJI-VS-0001.md`
- [ ] 08 章仅引用 Base/ADR，不复制阈值或跨切面策略
- [ ] 引用 Base 口径（至少 CH01/CH03）：
  - CH01：`docs/architecture/base/01-introduction-and-goals-v2.md`
  - CH03：`docs/architecture/base/03-observability-sentry-logging-v2.md`
- [ ] 文档中不存在旧前端/旧桌面壳语境（如 Electron/Web UI/LegacyE2E 等）
- [ ] `scripts/python/task_links_validate.py` 校验通过（任务/ADR/章节/Overlay/测试回链）

---

## 2) 契约与事件（SSoT）

- [ ] 契约落盘到 `Game.Core/Contracts/**`，且不依赖 Godot API
- [ ] 事件命名遵循 `${DOMAIN_PREFIX}.<entity>.<action>`，并常量化（避免魔法字符串）
- [ ] 变更契约时同步更新 xUnit 测试（覆盖核心 DTO/状态机）

---

## 3) 测试与门禁

- [ ] xUnit 单元测试覆盖核心规则（建议目录 `Game.Core.Tests/**`）
- [ ] GdUnit4 场景测试覆盖最小可玩闭环（建议目录 `Tests.Godot/**`）
- [ ] `py -3 scripts/python/quality_gates.py --unit --scene --security` 通过（产出写入 `logs/**`）

---

## 4) 安全与可观测性

- [ ] 安全基线对齐 ADR-0019（仅允许 `res://`/`user://`，拒绝越权路径与非 HTTPS）
- [ ] 关键审计写入 `logs/**`（安全/文件/网络/权限）
- [ ] Release Health 口径对齐 ADR-0003（Sentry 相关配置由 CI 软门禁审计）
