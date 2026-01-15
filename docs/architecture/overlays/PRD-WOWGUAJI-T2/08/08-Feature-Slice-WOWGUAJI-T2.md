---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - T2 最小可玩闭环（wowguaji）
Status: Active
Intent: Overview
SSoT: task_views
Tags: [overview, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0011
  - ADR-0004
  - ADR-0005
  - ADR-0019
  - ADR-0003
Test-Refs: []
---

本页定义 wowguaji 的 T2 阶段“最小可玩闭环”（放置采集/制作/战斗/区域解锁 + DLC 最小接入 + 存档/离线结算）的功能纵切边界、事件契约约束与验收挂钩。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1. 纵切目标（T2）

目标：实现可重复的最小闭环（可玩 + 可回归）：
- 新档 -> 选择活动（采集/制作/战斗）-> 资源/经验增长
- 制作/装备提升 -> 战斗收益与掉落
- 解锁区域 -> 更高阶资源/配方/怪物
- 存档/读档 + 离线收益结算（不含离线战斗）
- DLC 最小接入：DLC 区域可见/可解锁/可进入，并能与主循环发生一次“资源/配方回馈”

## 2. 分层与边界（Ports & Adapters）

遵循 ADR-0018 + ADR-0011（Windows-only）：
- `Game.Core/`：纯 C# 领域逻辑（不依赖 Godot，可 xUnit 快测）
- `Game.Godot/`：场景/UI/适配层（封装 Godot API，通过接口注入给 Core）
- `Tests/`：xUnit（Core 单测）
- `Tests.Godot/`：GdUnit4（场景/信号/Headless）

## 3. 关键实体与状态（最小集）

以 PRD 中的 T2 范围为准，本纵切最小状态建议包含：
- `GameState`：技能、背包、配方解锁、区域解锁、任务/成就进度、DLC 启用标记、版本号、`lastOnlineTime`
- `Skill`：等级/经验/解锁条件
- `Inventory`：堆叠、容量（或“模板阶段可配置容量”）
- `Region`：解锁条件、可用资源点/怪物池/商店（如有）
- `Activity`：当前活动（采集/制作/战斗）及其 tick 状态

## 4. 数据驱动内容策略（JSON + DLC 合并/校验/降级）

本项目把“内容（Content）”视为只读配置与表数据，用于驱动采集点、配方、怪物、掉落表、区域解锁等；与“存档（Save）”区分对待。

### 4.1 落盘位置（写死）

- 内容目录：`Game.Godot/Content/**`（Godot 路径：`res://Game.Godot/Content/**`）
- Base 内容：`Game.Godot/Content/base/`
- DLC 内容：`Game.Godot/Content/dlc/<DlcId>/`

建议的模块拆分（示例命名，用于治理与校验，不强制实现细节）：
- `skills.json`、`items.json`、`recipes.json`
- `gathering_nodes.json`
- `regions.json`
- `monsters.json`、`loot_tables.json`
- `dlc_manifest.json`（或 `manifest.json`）

### 4.2 合并策略（写死）

加载顺序：Base -> DLC（按启用列表与 manifest 顺序）。

默认合并规则（保守止损）：
- DLC 只能“新增 ID”，不得覆盖 Base 的同名 ID；发现冲突视为 DLC 无效并降级（见 4.4）。
- 引用关系必须可解析（例如配方引用的 itemId 必须存在；区域引用的采集点/怪物必须存在）。

### 4.3 校验策略（写死）

校验分两层：
- 语法层：JSON 可解析、`schemaVersion` 合法、字段类型正确、ID 唯一。
- 语义层：引用完整性（跨表引用）、约束一致性（例如解锁条件引用的技能/区域存在）。

### 4.4 降级策略（写死）

- Base 内容校验失败：视为不可启动，直接失败并输出可观测错误（避免“能跑但数据错”的隐性事故）。
- DLC 内容校验失败：禁用该 DLC（主流程仍可运行），并记录审计日志（JSONL，路径规范见 `AGENTS.md` 6.3）。
- 选配模块缺失：相关入口显示为“锁定/不可用”，并给出原因（不允许静默缺功能）。

## 5. 事件升格门槛（统一口径）

事件用于“模块间/层间的边界点”，不是用于传播每个 tick 的细节状态。为了避免事件泛滥与调试成本爆炸，本项目统一采用以下升格门槛：

- 只对“里程碑/边界点”升格为事件：开始/停止/完成/解锁/结算/失败（而不是进度条每次 +1）。
- 需要满足至少 2 个独立消费者才升格：例如 UI +（存档/统计/成就/审计）任一；否则走状态快照读取。
- 高频变化（tick/帧级）默认不事件化：必须先做聚合/节流（例如“结算事件”替代“每 tick 产出事件”）。
- 事件必须对应“可回放/可归因”的业务动作：发生时机明确、字段稳定、错误路径可审计。

## 6. 关键事件与契约（仅列闭环边界）

事件命名遵循 `${DOMAIN_PREFIX}.<entity>.<action>`，本纵切默认 `${DOMAIN_PREFIX}=core`（ADR-0004）。

纵切最小事件集（示例命名，最终以 Contracts SSoT 为准）：
- `core.inventory.item.added`：背包新增物品（采集产出/制作产出/战斗掉落/离线结算）
- `core.skill.levelled_up`：技能升级
- `core.region.unlocked`：区域解锁
- `core.combat.ended`：战斗结束（胜负/掉落摘要）
- `core.offline.rewards.granted`：离线收益已结算并入账

Contracts（SSoT，文档只引用路径，不复制内容）：
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
- `Game.Core/Contracts/CoreLoop/SkillLevelledUp.cs`
- `Game.Core/Contracts/CoreLoop/RegionUnlocked.cs`
- `Game.Core/Contracts/CoreLoop/CombatEnded.cs`
- `Game.Core/Contracts/CoreLoop/OfflineRewardsGranted.cs`

约束：
- 契约类型必须落盘于 `Game.Core/Contracts/**`，且不得引用 Godot API（可单测）。
- 适配层/场景层不得散落“事件 type 魔法字符串”；需通过 Contracts 常量化。

## 7. 核心流程（运行时骨干）

### 5.1 启动 -> 读档 -> 离线结算
- DataStore 从 `user://` 读取存档（拒绝绝对路径与越权路径，安全口径见 ADR-0019）
- 计算离线时长：`now - lastOnlineTime`，按 PRD 的上限策略做 cap
- 仅对采集/制作进行离线收益结算；离线战斗必须拒绝/为 0（口径：PRD）
- 写入 `core.offline.rewards.granted`（用于 UI 弹窗与审计）

### 5.2 Tick 驱动的活动系统
- TimeService（Godot Autoload）驱动 tick
- ActivitySystem（Core）处理：采集/制作/战斗的 tick 状态推进
- Core 先结算再发事件；UI 允许延迟播放动画但不得回写逻辑

### 5.3 采集 -> 产出 -> 技能增长
- 采集周期结束：产出物品入背包 -> 触发 `core.inventory.item.added`
- 增加技能经验，若升级：触发 `core.skill.levelled_up`

### 5.4 制作 -> 材料扣减 -> 产出 -> 装备/属性影响
- 校验材料与配方解锁
- 扣减材料、产出物品、（可选）装备影响战斗属性
- 触发 `core.inventory.item.added`

### 5.5 战斗 -> 掉落 -> 区域解锁推进
- 战斗按 tick 结算，产生胜负与掉落摘要
- 掉落入背包 -> `core.inventory.item.added`
- 战斗结束 -> `core.combat.ended`
- 若满足区域解锁条件 -> `core.region.unlocked`

### 5.6 DLC 最小接入（一次回馈）
- DLC Manifest（数据驱动）加载后注册区域/资源/配方
- DLC 区域必须可见但锁定；满足条件后可进入
- DLC 的资源/配方至少有一次回馈到主循环（例如 DLC 材料参与主线配方）

## 8. 可观测性与审计（引用，不复制）

可观测性/结构化日志/Sentry 口径见 ADR-0003 与 CH03。

本纵切要求：
- 涉及文件/网络/权限拒绝时必须产出审计（路径与字段见 AGENTS.md 6.3）
- Headless 冒烟/安全/性能的产物必须落盘到 `logs/**` 结构

## 9. 测试与门禁（对齐门禁口径，不复制阈值）

门禁口径见 ADR-0005。

建议的最小测试集：
- xUnit（Core）：活动 tick、离线结算、掉落 roll（可固定 seed）、区域解锁条件
- GdUnit4（Scenes）：主入口场景可加载、关键 Signals 连通、离线结算弹窗可见
- Headless smoke：`py -3 scripts/python/godot_tests.py --headless --suite smoke`（产物落盘见 `AGENTS.md` 6.3）

说明：测试对齐以后续的任务视图文件为准，本页不维护 `Test-Refs` 清单。

## 99) 变更影响面（跨纵切依赖）
- 本页改动会影响所有纵切页的统一口径（内容策略/事件升格门槛/降级规则）。
- 若调整“写死策略”，需同步检查每个纵切页的引用是否仍一致。
