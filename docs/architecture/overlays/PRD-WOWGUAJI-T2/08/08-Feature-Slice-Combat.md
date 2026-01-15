---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - Combat（自动战斗与掉落）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [combat, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0004
  - ADR-0005
Test-Refs: []
---

本页定义 T2 的战斗纵切：选择怪物/区域 -> 自动战斗 tick -> 胜负结算 -> 掉落入库 -> 推进解锁条件。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：战斗结算（按攻击间隔/tick）、伤害规则、胜负判定、掉落 roll
- Godot：战斗入口 UI、战斗中展示（可简化）、结算弹窗与掉落展示

## 2) 最小数据结构（建议）

- `CombatantStats`：hp、attack、defense（可扩展命中/闪避）
- `Monster`：id、stats、lootTableId、attackIntervalSeconds
- `LootTable`：条目（itemId、weight、min/max、rarityTag）

## 3) 数据驱动内容（写死）

- 怪物与掉落表必须来自内容数据（JSON），落盘口径见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“数据驱动内容策略”。
- 建议模块文件（示例命名）：`res://Game.Godot/Content/base/monsters.json`、`res://Game.Godot/Content/base/loot_tables.json`；DLC 内容同名模块落在 `res://Game.Godot/Content/dlc/<DlcId>/`。

## 4) 关键事件（名称约束）

事件升格门槛统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“事件升格门槛（统一口径）”。

- `core.combat.ended`（胜负与掉落摘要）
- `core.combat.started`（进入战斗与上下文）
- `core.loot.dropped`（掉落摘要，用于 UI/成就/统计等订阅）
- `core.inventory.item.added`（掉落入库）

Contracts（SSoT）：
- `Game.Core/Contracts/CoreLoop/CombatEnded.cs`
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
- `Game.Core/Contracts/Combat/CombatStarted.cs`
- `Game.Core/Contracts/Combat/LootDropped.cs`

### 事件（补充：模板运行时演示）

- **PlayerDamaged** (`core.player.damaged`)
  - 触发时机：伤害结算后（当前模板为 CombatService 的 Publish）
  - 字段：`amount`, `type`, `critical`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Runtime/PlayerDamaged.cs`

## 5) 验收（最小集）

- 玩家能进入至少 1 场战斗并结束
- 胜利时获得金币/掉落至少一种，且背包可见变化
- 战斗结果能影响一个解锁条件（例如任务进度或区域解锁）

## 6) 失败路径与降级（写死）

- 内容缺失/不合法：由内容校验在启动阶段拦截（Base 失败不可启动；DLC 失败禁用 DLC，口径见总览）。
- 运行时保护：若发现怪物引用的 lootTableId 不存在，视为内容错误；必须记录可观测错误并拒绝继续产出（不得静默给空掉落）。

## 99) 变更影响面（跨纵切依赖）
- 影响 Regions & Map：解锁条件与区域推进节奏。
- 影响 UI Dashboard：战斗结算与掉落反馈。
- 影响 Save & Offline：离线战斗口径（T2 不模拟）。
