---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - Core Loop（tick/状态机/事件骨干）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [core_loop, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0004
  - ADR-0005
  - ADR-0006
  - ADR-0030
Test-Refs: []
---

本页定义 T2 最小可玩闭环的“运行时骨干”：tick 驱动、状态推进、事件发布与边界隔离。阈值/门禁策略只引用 Base/ADR，不在本文复制。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：纯 C# 规则（活动推进、离线结算、解锁条件、掉落 roll 等）
- Godot：场景装配、输入/时间适配、UI 展示、Signals 路由
- Contracts：事件类型与 DTO 的 SSoT，落盘 `Game.Core/Contracts/**`

## 2) 最小状态（建议）

- `GameState`：skills / inventory / regions / quests / dlc / version / lastOnlineTime
- `CurrentActivity`：类型（gather/craft/combat）+ 目标（资源点/配方/怪物/区域）+ tick 累计
- `RngState`：可选（用于测试可重复与回归）

## 3) 数据驱动内容（引用总览）

- 内容数据的落盘/加载/合并/校验/降级口径统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“数据驱动内容策略”。
- 本纵切只要求：Core 的规则计算不得依赖“硬编码表数据”；内容应来自可替换的加载结果（例如 Base + DLC 合并后的只读视图）。

## 4) Tick 驱动（运行时骨干）

建议采用“固定步进 + 累计时间”的 tick 模式：

- Godot TimeAdapter 只提供 `deltaSeconds` 与 `now`
- Core 以 `deltaSeconds` 推进活动，触发产出/战斗结算/升级等规则
- Core 产生领域事件；UI 只消费事件与状态快照，不回写规则

## 5) 最小事件集（名称约束）

事件升格门槛统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“事件升格门槛（统一口径）”；本页只列出闭环边界点。

事件命名遵循 `${DOMAIN_PREFIX}.<entity>.<action>`（ADR-0004），纵切最小集建议包含：

- `core.inventory.item.added`
- `core.skill.levelled_up`
- `core.combat.ended`
- `core.region.unlocked`
- `core.offline.rewards.granted`

Contracts（SSoT）：
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
- `Game.Core/Contracts/CoreLoop/SkillLevelledUp.cs`
- `Game.Core/Contracts/CoreLoop/CombatEnded.cs`
- `Game.Core/Contracts/CoreLoop/RegionUnlocked.cs`
- `Game.Core/Contracts/CoreLoop/OfflineRewardsGranted.cs`

## 契约定义（补充：模板运行时事件）

说明：以下事件用于现有模板的运行时演示/基础 UI 更新，命名与类型口径遵循 ADR-0004，并已迁移为 `core.*.*`。

### 事件

- **GameStarted** (`core.game.started`)
  - 触发时机：引擎示例 Start 时
  - 字段：`stateId`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Runtime/GameStarted.cs`

- **GameEnded** (`core.game.ended`)
  - 触发时机：引擎示例 End 时
  - 字段：`score`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Runtime/GameEnded.cs`

- **StateManagerUpdated** (`core.state.manager.updated`)
  - 触发时机：`GameStateManager.SetState(...)` 更新内部快照后
  - 字段：`occurredAt`
  - 契约位置：`Game.Core/Contracts/State/StateManagerUpdated.cs`


说明：最终事件契约以 `Game.Core/Contracts/**` 为准；场景/适配层不得散落魔法字符串。

## 6) 验收（可回归）

- Tick 推进可在 Core 单测中 deterministic 复现（可固定 seed）
- headless smoke 可验证“启动 -> 主场景加载 -> 核心状态可读 -> 退出码正常”，且产物落 `logs/**`

## 99) 变更影响面（跨纵切依赖）
- 影响所有纵切：tick 推进、状态机边界与可回归性。
- 改动若引入高频更新，需回看“事件升格门槛”与 UI 刷新策略。
