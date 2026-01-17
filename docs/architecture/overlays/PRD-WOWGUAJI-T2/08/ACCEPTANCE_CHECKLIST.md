---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切验收清单（wowguaji）
Status: Active
Intent: Checklist
SSoT: task_views
Tags: [checklist, t2]
ADR-Refs: []
Test-Refs: []
---

# PRD-WOWGUAJI-T2 功能纵切验收清单（wowguaji）

## 基本信息

- PRD ID: `PRD-WOWGUAJI-T2`
- PRD 来源: `docs/prd.txt`
- 功能纵切文档: `docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-WOWGUAJI-T2.md`
- 口径: Godot 4.5 + C#/.NET 8（Windows-only）

---

## 1) 文档与回链

- [ ] PRD 文档存在且可读：`docs/prd.txt`
- [ ] 08 章只引用 Base/ADR，不复制阈值/策略（尤其是安全、可观测性、质量门禁）
- [ ] Base 口径引用完整（至少 CH01/CH02/CH03/CH07）：
  - CH01：`docs/architecture/base/01-introduction-and-goals-v2.md`
  - CH02：`docs/architecture/base/02-security-baseline-godot-v2.md`
  - CH03：`docs/architecture/base/03-observability-sentry-logging-v2.md`
  - CH07：`docs/architecture/base/07-dev-build-and-gates-v2.md`
- [ ] 文档中不出现旧前端/旧桌面壳语境（如 Electron/Web UI/LegacyE2E 等）

---

## 2) 数据驱动内容（写死）

- [ ] 内容（Content）采用只读 JSON 数据驱动，并约定落盘位置：`Game.Godot/Content/**`
- [ ] DLC 内容采用 manifest + 模块文件方式加载，加载顺序为 Base -> DLC
- [ ] 合并策略保守止损：DLC 默认只允许新增 ID，不允许覆盖 Base 同名 ID（冲突则禁用 DLC）
- [ ] 校验策略明确：至少包含 JSON 解析/版本字段/ID 唯一性/跨表引用完整性
- [ ] 降级策略明确：Base 内容失败不可启动；DLC 失败禁用 DLC 且主世界可玩；UI 必须可观察提示

---

## 3) 契约与事件（SSoT）

- [ ] 契约类型统一落盘：`Game.Core/Contracts/**`，且不依赖 Godot API
- [ ] 事件命名遵循 `${DOMAIN_PREFIX}.<entity>.<action>`，并常量化，避免魔法字符串
- [ ] 最小事件集覆盖“闭环关键节点”（采集/制作/战斗/区域解锁/离线结算）
- [ ] Contracts 路径引用可校验存在性（示例）：`Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
- [ ] 已定义并引用统一的“事件升格门槛”：只对里程碑/边界点升格，高频 tick 不事件化

---

## 4) 测试与门禁（对齐 ADR-0005）

- [ ] xUnit 覆盖 Core 关键规则（tick、离线结算、掉落、区域解锁等）
- [ ] GdUnit4 覆盖主入口场景加载与关键 Signals 连通（headless 可跑）
- [ ] 冒烟/门禁脚本可运行，并产出 `logs/**` 目录下的工件

---

## 5) 安全与可观测性（引用 ADR，不复制阈值）

- [ ] 安全基线对齐 ADR-0019：仅允许 `res://`/`user://`，拒绝越权路径，拒绝非 HTTPS 外链
- [ ] 关键拒绝路径写入审计 JSONL（字段与路径结构遵循 AGENTS.md 6.3）
- [ ] 可观测性对齐 ADR-0003：结构化日志路径一致，Release Health 口径不在本文件复制
