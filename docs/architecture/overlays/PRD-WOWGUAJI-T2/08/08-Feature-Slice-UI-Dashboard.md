---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - UI Dashboard（仪表盘式放置体验）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [ui_dashboard, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0005
  - ADR-0003
  - ADR-0022
Test-Refs: []
---

本页定义 T2 的 UI 纵切：用“仪表盘”把采集/制作/战斗/地图/背包/任务等入口串起来，确保关键反馈可观察、可回归测试。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：只提供状态快照与事件，不直接依赖 UI
- Godot：UI 组装、Signals 路由、动画与呈现
- Observability：关键交互与错误路径可追踪（引用 ADR-0003，不复制阈值）

## 2) UI 最小信息架构（建议）

- 主界面（Dashboard）
  - 当前活动：类型/目标/进度/产出速率
  - 关键数值：金币、主要资源摘要、关键技能等级
  - 快捷入口：Gathering / Crafting / Combat / Map / Inventory / Quests / Settings

## 3) 可测试性要求（引用 ADR-0025 / ADR-0005）

- 入口场景可 headless 加载
- 关键节点可见性与关键 Signals 连通可由 GdUnit4 断言
- UI 不包含不可控的随机逻辑；随机只在 Core 层并允许固定 seed

## 4) 事件消费门槛（引用总览）

UI 的订阅策略必须遵循总览的“事件升格门槛（统一口径）”：
- UI 只订阅“边界点事件”（开始/停止/完成/结算/解锁/失败），用于触发提示与刷新快照。
- tick/帧级变化不通过事件逐条推送；UI 应从状态快照读取并自行节流刷新，避免事件风暴导致卡顿与难以回归。

## 5) 数据驱动内容（写死）

- UI 的静态展示（名称/描述/图标路径/稀有度标签等）必须来自内容数据（JSON），落盘口径见总览的“数据驱动内容策略”。
- 若内容缺失或 DLC 被禁用：UI 必须显示为锁定/不可用并给出原因，不允许静默丢入口。

## 6) 验收（最小集）

- 新档启动后可一跳进入 Dashboard，并能开始至少一种活动
- 产出/升级/掉落/解锁等关键反馈在 UI 上可观察

Contracts（SSoT，最小引用用于文档校验）：
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`

## 契约定义（补充：UI 演示事件）

说明：现有模板的 HUD/面板示例会消费以下事件，用于验证 EventBus -> UI 的信号链路。

### 事件

- **ScoreUpdated** (`core.score.updated`)
  - 触发时机：分数变化后（引擎示例或 UI PublishSimple）
  - 字段：`score`, `added`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Runtime/ScoreUpdated.cs`

- **HealthUpdated** (`core.health.updated`)
  - 触发时机：生命值变化后（引擎示例或 UI PublishSimple）
  - 字段：`health`, `delta`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Runtime/HealthUpdated.cs`

- **PlayerMoved** (`core.player.moved`)
  - 触发时机：位置变化后（引擎示例）
  - 字段：`x`, `y`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Runtime/PlayerMoved.cs`

## 99) 变更影响面（跨纵切依赖）
- 影响所有纵切：入口编排决定闭环可玩度与可观察性。
- UI 刷新需遵循事件升格门槛：边界点事件 + 状态快照节流。
