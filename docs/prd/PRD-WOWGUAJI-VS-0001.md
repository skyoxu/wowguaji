---
Story-ID: PRD-WOWGUAJI-VS-0001
Title: wowguaji T2 首个垂直切片 - 最小可玩闭环（放置RPG + 地图DLC）
Status: Active
ADR-Refs:
  - ADR-0018
  - ADR-0011
  - ADR-0004
  - ADR-0005
  - ADR-0006
  - ADR-0019
  - ADR-0003
  - ADR-0023
  - ADR-0025
Chapter-Refs:
  - CH01
  - CH02
  - CH03
  - CH04
  - CH05
  - CH06
  - CH07
  - CH10
Overlay-Refs:
  - docs/architecture/overlays/PRD-WOWGUAJI-T2/08/_index.md
  - docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-WOWGUAJI-T2.md
  - docs/architecture/overlays/PRD-WOWGUAJI-T2/08/ACCEPTANCE_CHECKLIST.md
Test-Refs: []
---

# PRD-WOWGUAJI-VS-0001：T2 首个垂直切片 - 最小可玩闭环

本 PRD 用于把 `docs/prd.txt`（T2 阶段单一事实来源）映射为“可执行的垂直切片”边界：明确闭环目标、约束、验收与 Overlay/任务回链。

## 1. 背景与目标（引用 CH01）

wowguaji 是一个 Windows-only 的 Godot 4.x（.NET/Mono）+ C# 单机离线放置类 RPG。T2 阶段目标是实现“最小可玩闭环（MVP Loop）”，可重复回归验证：

- 新档 -> 选择活动（采集/制作/战斗）-> 资源/经验增长
- 制作/装备提升 -> 战斗收益与掉落
- 区域解锁 -> 更高阶资源/配方/怪物
- 存档/读档 + 离线收益结算（不包含离线战斗）
- DLC 最小接入：DLC 区域可见/可解锁/可进入，并对主循环产生一次“资源/配方回馈”

## 2. 范围与非范围（引用 docs/prd.txt）

### 2.1 T2 必须交付

- 采集（2–3 个技能落地，结构可扩展）
- 制作（至少 1 个制作技能 + 若干配方）
- 自动战斗（基础属性与掉落表）
- 区域/地图与解锁条件
- 任务链（新手引导/关键节点结算）
- 存档（user://）与离线收益结算
- DLC：数据可开关、内容可进入、至少一次回馈到主世界循环

### 2.2 T2 明确不做（但需预留结构）

- 多人联机/排行榜/交易系统
- 深度 build（大天赋树/复杂循环）
- 离线战斗（T2 口径：不模拟，避免离线死亡负反馈）

## 3. 约束与口径（引用 ADR/CH，不复制阈值）

- 平台：Windows-only（ADR-0011）
- 分层：Ports & Adapters（ADR-0018 / ADR-0007 / ADR-0021）
- 契约与事件：CloudEvents 风格 + SSoT 落 `Game.Core/Contracts/**`（ADR-0004 / ADR-0020）
- 数据存储：仅 `res://`（只读）与 `user://`（读写），拒绝越权路径与绝对路径（ADR-0019）
- 可观测性：结构化日志 + Sentry Release Health（ADR-0003）
- 质量门禁：统一由脚本固化与产出 `logs/**`（ADR-0005）

## 4. 垂直切片验收（可回归、可取证）

### 4.1 功能验收（场景/交互）

- 新档启动后进入主界面，能选择一个活动开始挂机（采集/制作/战斗至少一种）
- UI 能观察到：当前活动、产出速率/剩余时间或 tick 进度、技能等级/经验变化
- 能完成一次“装备提升 -> 战斗收益 -> 满足解锁条件 -> 区域解锁”链路
- DLC 开关可用：DLC 区域可见且可进入，并触发一次回馈（例如 DLC 材料进入主世界配方）

### 4.2 数据与稳定性验收

- 存档写入 `user://` 成功，读档后关键状态一致（技能/背包/区域解锁/DLC 状态）
- 离线收益结算：仅采集/制作生效；离线战斗必须为 0 或显式拒绝（按 PRD 口径）
- 任何安全拒绝（路径越权/非 HTTPS 外链/离线模式出网）都记录到审计 JSONL（路径规范见 `AGENTS.md` 6.3）

## 5. 与 Overlay / 任务的对齐（SSoT 回链）

- 08 章纵切（本 PRD 的唯一 Overlay 入口）：
  - `docs/architecture/overlays/PRD-WOWGUAJI-T2/08/_index.md`
  - `docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-WOWGUAJI-T2.md`
  - `docs/architecture/overlays/PRD-WOWGUAJI-T2/08/ACCEPTANCE_CHECKLIST.md`
- 任务视图（Taskmaster / MCP view）：
  - `.taskmaster/tasks/tasks.json`（Taskmaster 生成）
  - `.taskmaster/tasks/tasks_back.json`（NG-* 视图）
  - `.taskmaster/tasks/tasks_gameplay.json`（GM-* 视图）

## 6. 测试与门禁（引用 ADR-0025 / ADR-0005，不复制阈值）

- xUnit：覆盖 Core 规则（tick、离线结算、掉落、区域解锁条件）
- GdUnit4：覆盖主入口场景加载与关键 Signals 连通（headless 可跑）
- 脚本门禁：`py -3 scripts/python/quality_gates.py ...` 产出统一落盘到 `logs/**`

Test-Refs 说明：Front-Matter 只引用仓库内真实存在的测试文件路径；若尚未落地测试，保持空列表。

