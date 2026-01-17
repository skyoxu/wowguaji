---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - Regions & Map（区域与解锁推进）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [regions_map, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0004
  - ADR-0005
Test-Refs: []
---

本页定义 T2 的地图/区域纵切：区域列表 -> 条件提示 -> 解锁 -> 进入区域 -> 暴露采集点/怪物池。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：解锁条件判定（技能等级/任务进度/击杀 boss/关键道具）
- Godot：地图 UI（已解锁/未解锁/可解锁）、区域详情页与入口

## 2) 最小数据结构（建议）

- `Region`：id、name、unlockConditions、gatheringNodes、monsters
- `UnlockCondition`：type（skillLevel/questCompleted/bossDefeated/itemOwned）、parameters

## 3) 数据驱动内容（写死）

- Region/解锁条件的来源统一走内容数据（JSON），落盘口径见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“数据驱动内容策略”。
- 建议模块文件（示例命名）：`res://Game.Godot/Content/base/regions.json`，DLC 区域：`res://Game.Godot/Content/dlc/<DlcId>/regions.json`。
- 合并策略默认“只新增 ID，不允许覆盖 Base 同名 ID”；冲突视为 DLC 无效并降级（见总览）。

## 4) 关键事件（名称约束）

事件升格门槛统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“事件升格门槛（统一口径）”。

- `core.region.unlocked`

Contracts（SSoT）：
- `Game.Core/Contracts/CoreLoop/RegionUnlocked.cs`

## 5) 验收（最小集）

- 至少 2 个区域：初始区域 + 可解锁区域
- UI 能显示解锁条件，并在满足后解锁（状态变化可观察）
- 解锁后区域内至少暴露 1 个采集点或 1 个战斗入口

## 6) 失败路径与降级（写死）

- 区域数据缺失/不合法：Base 内容失败视为不可启动；DLC 内容失败则禁用 DLC 并保持主世界可玩（口径见总览）。
- UI 必须能区分：未解锁/可解锁/已解锁/内容缺失（错误态），不得静默隐藏入口。

## 99) 变更影响面（跨纵切依赖）
- 影响 Gathering/Combat：区域内可用资源点与怪物池。
- 影响 DLC：DLC 区域的可见/锁定/进入与回馈。
- 影响 UI Dashboard：地图入口与锁定提示。
