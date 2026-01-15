---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - Crafting（材料->配方->产物/装备）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [crafting, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0004
  - ADR-0005
Test-Refs: []
---

本页定义 T2 的制作纵切：选择配方 -> 材料校验与扣减 -> 制作完成 -> 产物入库（可包含装备）。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：配方校验、材料扣减、制作计时、产物生成、经验增长与解锁
- Godot：配方列表 UI、材料不足提示、制作进度条与完成反馈

## 2) 最小数据结构（建议）

- `Recipe`：id、inputs（物品与数量）、output、craftSeconds、requiredSkillLevel、xpReward
- `Equipment`：基础属性字段（攻击/防御/HP 等），用于影响战斗或效率

## 3) 数据驱动内容（写死）

- 配方与装备基础数据必须来自内容数据（JSON），落盘口径见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“数据驱动内容策略”。
- 建议模块文件（示例命名）：`res://Game.Godot/Content/base/recipes.json`、`res://Game.Godot/Content/base/items.json`；DLC 内容同名模块落在 `res://Game.Godot/Content/dlc/<DlcId>/`。
- 合并策略默认“只新增 ID”；DLC 通过新增配方/材料与主世界产生回馈，而不是覆盖主世界同名配方。

## 4) 关键事件（名称约束）

事件升格门槛统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“事件升格门槛（统一口径）”。

- `core.inventory.item.added`（制作产物入库）
- `core.crafting.completed`（制作完成摘要）
- `core.recipe.unlocked`（配方解锁，用于提示/引导）
- `core.equipment.equipped`（装备变更，用于战斗数值刷新）
- `core.skill.levelled_up`（制作技能升级，可选）

Contracts（SSoT）：
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
- `Game.Core/Contracts/CoreLoop/SkillLevelledUp.cs`
- `Game.Core/Contracts/Crafting/CraftingCompleted.cs`
- `Game.Core/Contracts/Crafting/RecipeUnlocked.cs`
- `Game.Core/Contracts/Crafting/EquipmentEquipped.cs`

## 5) 验收（最小集）

- 至少 1 个制作技能 + 若干配方可用
- 材料不足时拒绝并提示；材料足够时制作完成并入库
- 若制作产物为装备：装备后对战斗数值产生可观察影响（UI 或战斗结果）

## 6) 失败路径与降级（写死）

- 内容缺失/不合法：由内容校验在启动阶段拦截（Base 失败不可启动；DLC 失败禁用 DLC，口径见总览）。
- 运行时保护：若配方引用的 itemId 不存在，视为内容错误；必须记录可观测错误并拒绝执行该配方（不得静默产出空物品）。

## 99) 变更影响面（跨纵切依赖）
- 影响 Gathering：材料输入与产出平衡。
- 影响 Combat：装备/消耗品对战斗结果的可观察变化。
- 影响 Save & Offline：配方解锁与产物持久化。
