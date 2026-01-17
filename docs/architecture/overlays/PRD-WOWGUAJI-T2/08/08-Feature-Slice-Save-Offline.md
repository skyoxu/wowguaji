---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - Save & Offline（存档与离线收益）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [save_offline, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0005
  - ADR-0006
  - ADR-0019
  - ADR-0023
Test-Refs: []
---

本页定义 T2 的存档/离线纵切：`user://` 存档读写、版本化、离线收益结算与审计约束。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：存档 DTO、版本迁移（如有）、离线时长计算与 cap、结算规则
- Godot：触发保存的时机（退出/定时/关键节点）、离线结算弹窗与摘要展示

## 2) 安全与路径约束（引用 ADR-0019）

- 只允许写入 `user://`；拒绝绝对路径与越权路径
- 若写入失败必须产出审计日志（JSONL，路径规范见 `AGENTS.md` 6.3）

## 3) 离线收益口径（引用 docs/prd.txt）

- 只对采集/制作结算
- 离线战斗：T2 明确不模拟（拒绝或视为 0）

## 4) 内容版本与存档兼容（写死）

内容（Content）采用只读 JSON 数据驱动（见总览的“数据驱动内容策略”），存档必须记录“加载时的内容上下文”，以避免“读档后发现引用的内容不存在”的隐性错误。

最小建议（不限定实现载体）：
- 记录 Base 内容的 `schemaVersion`（或等价的版本标记）
- 记录启用的 DLC 列表（`DlcId[]`）与各自的版本标记（存在即可）

读档时的降级口径（写死）：
- Base 内容校验失败：视为不可启动（与总览一致）。
- DLC 内容缺失/校验失败：禁用该 DLC，相关入口显示为锁定并给出原因；存档可继续加载但不得崩溃。

## 5) 关键事件（名称约束）

事件升格门槛统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“事件升格门槛（统一口径）”。

- `core.offline.rewards.granted`

Contracts（SSoT）：
- `Game.Core/Contracts/CoreLoop/OfflineRewardsGranted.cs`

## 契约定义（补充：存档事件）

说明：以下事件用于存档/自动存档的最小取证链路（创建/加载/删除/自动存档开关与完成）。

### 事件

- **SaveCreated** (`core.save.created`)
  - 触发时机：保存成功后
  - 字段：`saveId`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Save/SaveCreated.cs`

- **SaveLoaded** (`core.save.loaded`)
  - 触发时机：读档成功后
  - 字段：`saveId`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Save/SaveLoaded.cs`

- **SaveDeleted** (`core.save.deleted`)
  - 触发时机：删除存档成功后
  - 字段：`saveId`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Save/SaveDeleted.cs`

- **AutoSaveEnabled** (`core.autosave.enabled`)
  - 触发时机：启用自动存档后
  - 字段：`intervalMs`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Save/AutoSaveEnabled.cs`

- **AutoSaveDisabled** (`core.autosave.disabled`)
  - 触发时机：关闭自动存档后
  - 字段：`occurredAt`
  - 契约位置：`Game.Core/Contracts/Save/AutoSaveDisabled.cs`

- **AutoSaveCompleted** (`core.autosave.completed`)
  - 触发时机：一次自动存档完成后
  - 字段：`saveId`, `intervalMs`, `occurredAt`
  - 契约位置：`Game.Core/Contracts/Save/AutoSaveCompleted.cs`

## 6) 验收（最小集）

- 存档写入与读档恢复一致（技能/背包/区域/DLC 状态）
- 离线结算生效且符合口径：仅采集/制作；离线战斗不生效
- DLC 缺失/校验失败时：主世界仍可运行，且 UI 能明确提示 DLC 被禁用（不可静默）

## 99) 变更影响面（跨纵切依赖）
- 影响所有纵切：存档兼容与离线结算决定整体可回归性。
- 影响 DLC：DLC 启用与内容版本需要可恢复且可降级。
