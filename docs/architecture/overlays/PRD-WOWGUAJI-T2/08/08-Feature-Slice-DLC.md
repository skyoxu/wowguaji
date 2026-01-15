---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切 - DLC（地图DLC 最小接入与回馈）
Status: Active
Intent: FeatureSlice
SSoT: task_views
Tags: [dlc, t2]
ADR-Refs:
  - ADR-0018
  - ADR-0005
  - ADR-0006
Test-Refs: []
---

本页定义 T2 的 DLC 纵切：DLC 可开关、内容可加载、区域可见/可进、与主循环至少一次回馈联动。

## 0) 用途边界（防误用）
- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。
- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。
- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。

## 1) 纵切边界

- Core：DLC manifest 与启用状态、DLC 解锁状态、与主世界的数据联动规则
- Godot：DLC 区域显示、锁定提示、进入按钮与内容展示

## 2) 数据驱动内容（manifest + 模块，写死）

内容落盘与校验/合并/降级口径统一见：`08-Feature-Slice-WOWGUAJI-T2.md` 的“数据驱动内容策略”。

本纵切额外写死 DLC 结构约束（用于避免 DLC 变成“随便塞文件”）：
- DLC 根目录：`res://Game.Godot/Content/dlc/<DlcId>/`
- DLC 必须包含 manifest（示例名）：`res://Game.Godot/Content/dlc/<DlcId>/manifest.json`
- manifest 必须明确列出该 DLC 提供的模块文件（regions/recipes/items/monsters 等），并声明版本字段（如 `schemaVersion`）

合并约束（保守止损）：
- 默认只允许新增 ID，不允许覆盖 Base 同名 ID；冲突则禁用 DLC
- DLC 必须至少对主循环产生一次“回馈”：新增资源/材料/配方之一可被主世界使用（不允许完全割裂）

## 3) 最小要求（T2 必须可验证）

- DLC 区域在地图上“可见但锁定”（未启用或未解锁时）
- 满足条件后可进入 DLC 区域
- DLC 至少一次回馈到主循环（例如 DLC 材料参与主世界配方）

## 4) 验收（最小集）

- DLC on/off 可被存档记录并在读档后保持一致
- 未启用 DLC 时相关内容不生效但数据不崩溃

Contracts（SSoT，最小引用用于文档校验）：
- `Game.Core/Contracts/CoreLoop/RegionUnlocked.cs`
- `Game.Core/Contracts/Dlc/DlcEnabled.cs`

## 5) 失败路径与降级（写死）

- DLC 内容缺失/校验失败：禁用该 DLC（主世界仍可玩），并在 UI 给出“DLC 不可用/被禁用”的明确提示。
- DLC 依赖的模块缺失：同样视为 DLC 无效并禁用，不允许部分加载导致引用悬空。

## 99) 变更影响面（跨纵切依赖）
- 影响 Regions & Map：DLC 区域的解锁与入口呈现。
- 影响 Gathering/Crafting/Combat：DLC 内容对主循环的回馈联动。
- 影响 Save & Offline：DLC 启用状态与内容版本的可恢复/降级。
