---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - Gathering（采集产出与技能成长）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [gathering, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0004
  - ADR-0005
Test-Refs: []
---

本页定义 T2 的采集纵切：选择资源点 -> 周期产出 -> 入库 -> 技能经验与解锁提示。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：采集周期、产量、稀有掉落 roll、经验增长与升级判定
- Godot：采集 UI、选择资源点交互、展示产出反馈
- Data：资源点与产出表建议数据驱动（不限定格式；存取口径见 ADR-0006）

## 2) 最小数据结构（建议）

- `GatheringNode`：id、requiredSkill、requiredLevel、cycleSeconds、outputs（主/副产物）
- `SkillState`：level、xp、milestones（如 10/20/...）

## 3) 数据驱动内容（写死）

- 资源点/产出表必须来自内容数据（JSON），落盘口径见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“数据驱动内容策略”。
- 建议模块文件（示例命名）：`res://Game.Godot/Content/base/gathering_nodes.json`、`res://Game.Godot/Content/base/skills.json`；DLC 内容同名模块落在 `res://Game.Godot/Content/dlc/<DlcId>/`。
- 稀有掉落表（若有）必须可被校验：权重/概率合法，引用的 itemId 存在（语义校验口径见总览）。

## 4) 关键事件（名称约束）

事件升格门槛统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“事件升格门槛（统一口径）”。

- `core.gathering.started`（开始采集与上下文）
- `core.gathering.stopped`（停止采集与原因）
- `core.resource.generated`（周期产出摘要，可用于 UI/统计/成就）
- `core.inventory.item.added`（采集产出入库）
- `core.skill.xp.changed`（经验变化，可选：UI 更细粒度展示）
- `core.skill.levelled_up`（技能升级）

Contracts（SSoT）：
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
- `Game.Core/Contracts/CoreLoop/SkillLevelledUp.cs`
- `Game.Core/Contracts/Gathering/GatheringStarted.cs`
- `Game.Core/Contracts/Gathering/GatheringStopped.cs`
- `Game.Core/Contracts/Gathering/ResourceGenerated.cs`
- `Game.Core/Contracts/Skills/SkillXpChanged.cs`

## 5) 验收（最小集）

- 玩家能选择至少 1 个采集技能与资源点开始挂机
- 到达一个采集周期后：背包数量变化可见 + 技能经验增长可见
- 若触发升级：提示可见，并可解锁至少一个新资源点或条件提示

## 6) 失败路径与降级（写死）

- 内容缺失/不合法：由内容校验在启动阶段拦截（Base 失败不可启动；DLC 失败禁用 DLC，口径见总览）。
- 运行时保护：若资源点引用的产出 itemId 不存在，视为内容错误；必须记录可观测错误并拒绝结算该周期（不得静默产出空物品）。

## 99) 变更影响面（跨纵切依赖）
- 影响 Crafting：材料链路与配方可用性。
- 影响 Save & Offline：离线结算口径与上限策略。
- 影响 UI Dashboard：产出与成长反馈展示。
