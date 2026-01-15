# 从 GM/NG 任务驱动首个 T2 可玩闭环实现

> 本文档总结“如何从 GM/NG 任务视图驱动 T2 最小可玩闭环”的建议，作为 wowguaji 项目的工作流参考。

## 1) 先用 PRD + Overlay 锁定 T2 场景流

- 在 PRD：打开 `docs/prd/PRD-WOWGUAJI-VS-0001.md`，确认 T2 闭环边界与验收条款。
- 在 Overlay（08 章纵切）：打开 `docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-WOWGUAJI-T2.md`，确认流程被“引用”且不复制 Base/ADR 阈值/策略。
- 在 Checklist：查看 `docs/architecture/overlays/PRD-WOWGUAJI-T2/08/ACCEPTANCE_CHECKLIST.md`，把可回归的验收条款落到任务 `acceptance` 与测试用例里。

建议把“首个可玩闭环”的最小场景流写成 6 步（便于自动化与回归）：
1) 新档启动进入主界面（仪表盘）
2) 选择活动开始 tick（采集或制作）并获得可见产出
3) 制作一件基础装备或消耗品（扣材料 -> 入库）
4) 进入一次自动战斗并获得掉落
5) 满足一个区域解锁条件并解锁新区域（或解锁 DLC 区域入口）
6) 存档 -> 退出 -> 再启动读档，触发一次离线收益结算（不包含离线战斗）

## 2) 基于任务视图的最小依赖闭包（建议顺序）

根据 `.taskmaster/tasks/tasks_back.json`（NG-*）与 `.taskmaster/tasks/tasks_gameplay.json`（GM-*）的 `depends_on`，建议按“先骨架与可测，再闭环集成”的顺序推进：

1. **NG-0002** —— Project setup & core architecture（工程结构/门禁入口）
2. **NG-0001** —— Core data models & serialization（存档核心模型与序列化）
3. **NG-0012** —— Headless smoke（严格模式，产物落 `logs/**`）
4. **GM-0105** —— Skill system（技能成长/解锁）
5. **GM-0106** —— Idle activity system（tick 驱动：采集/制作/战斗入口）
6. **GM-0101** —— Crafting & equipment（材料/配方/装备属性）
7. **GM-0103** —— Combat system（自动战斗 + 掉落）
8. **GM-0107** —— Region unlocking（区域/地图推进）
9. **GM-0104** —— DLC integration（DLC 可见/可进/一次回馈）
10. **GM-0102** —— Full loop integration（闭环集成 + 回归测试）

说明：如果发现 `depends_on` 与上面顺序冲突，以任务文件中的依赖为准，先把依赖图跑通再做重排。

## 3) 让任务真正“可驱动”：字段补齐与回链校验

对“闭环集成类任务”（例如 `GM-0102`）与“边界/门禁类任务”（例如 `NG-0012`）建议确保字段齐全：

- `owner` / `labels` / `layer`：便于分工与筛选
- `adr_refs` / `chapter_refs`：至少引用 1 条 Accepted ADR，并指向相关 Base 章节
- `overlay_refs`：指向本 PRD 的 08 章纵切与验收清单
- `test_refs`：只能写真实存在的测试文件路径（未落地测试时保持空列表）
- `acceptance`：必须可回归、可自动化取证（对应 `logs/**` 产物）

补齐后运行回链校验：

```bash
py -3 scripts/python/task_links_validate.py
```

## 4) 先做测试与场景骨架，再做逻辑

原则：先让“启动-退出-回归”跑通，再加系统复杂度。

- Core（xUnit）：优先覆盖 tick、离线结算、掉落 roll（可固定 seed）、区域解锁条件。
- Scenes（GdUnit4）：优先覆盖主入口场景可加载、关键 Signals 连通、核心 UI 节点可见。
- Headless smoke：把“启动/加载主场景/退出码/关键日志”固化为脚本判定，产物落 `logs/e2e/**`。

## 5) 示例验收条款（可用于任务 acceptance 与 Checklist）

> **T2 最小可玩闭环（GM-0102 对齐）**
> - 启动进入主界面，UI 可观察当前活动与关键数值
> - 采集或制作 tick 产生至少一种资源入库，并触发一次技能经验增长
> - 制作成功扣材料并产出物品（装备或消耗品）入库
> - 自动战斗至少完成 1 场并产生掉落入库
> - 解锁一个区域（主世界或 DLC 区域入口），且 UI 可见解锁状态变化
> - 存档/读档一致；离线收益结算生效且不包含离线战斗
> - 无未捕获异常；headless smoke 与基础门禁脚本可在 CI 跑通并产出 `logs/**`
