# 从 GM/NG 任务驱动首个 T2 场景实现

> 本文档总结“如何从 GM/NG 任务驱动首个 T2 场景实现”的建议，作为 wowguaji 项目的工作流参考。

## 1) 先用 PRD + Overlay 锁定 T2 场景流

- 在 `docs/prd/PRD-WOWGUAJI-VS-0001.md` 中，明确“最小 T2 Playable 场景流”：
  - 启动 -> 进入哪个 Guild Manager 场景
  - 完成一轮 Week/Phase 切换
  - 场景结束或返回菜单方式
- 在 Overlay：
  - 打开 `docs/architecture/overlays/PRD-Guild-Manager/08/08-Feature-Slice-Guild-Manager.md`，确认 T2 流程被引用（不重复阈值/策略）。
- 在 Checklist：
  - 查看 `docs/architecture/overlays/PRD-Guild-Manager/08/ACCEPTANCE_CHECKLIST.md`，确保有一条“首个 T2 Playable 场景流”的验收条款。

## 2) 基于完整 T2 的最小任务清单与顺序

根据 `.taskmaster/tasks/tasks_back.json` 与 `tasks_gameplay.json` 中的 `depends_on`，首个 T2 Playable 场景在 Taskmaster 语义下的最小依赖闭包建议按以下顺序推进：

1. **NG-0001** —— wowguaji 首个纵切 PRD <-> Overlay 映射
2. **NG-0020** —— Guild Manager 三层垂直切片骨架（Game.Core / Game.Godot / Tests.Godot）
3. **NG-0012** —— Python 版 headless smoke（strict 模式）
4. **NG-0021** —— 首个垂直切片的 xUnit/GdUnit4/smoke + CI 串联
5. **GM-0101** —— EventEngine Core（事件引擎骨干）
6. **GM-0103** —— GameTurnSystem + T2 回合/时间推进

## 3) 让任务真正“可驱动”：字段补齐建议

针对 `NG-0021` 与 `GM-0103`（也可以适度补充 `GM-0101`），建议检查并补齐以下字段：

- `owner`
- `labels`（例如 `t2-playable`, `gm-core-loop`, `godot-csharp`）
- `layer`
- `adr_refs`（至少包含 ADR-0019/ADR-0003/ADR-0004/ADR-0005/ADR-0011/ADR-0015 等）
- `chapter_refs`（例如 CH01/CH04/CH06/CH07）
- `overlay_refs`
  - `docs/architecture/overlays/PRD-Guild-Manager/08/08-Feature-Slice-Guild-Manager.md`
  - `docs/architecture/overlays/PRD-Guild-Manager/08/ACCEPTANCE_CHECKLIST.md`
- `test_refs`（指向实际存在的 xUnit/GdUnit4 测试文件）
- `acceptance`（条款要可验收、可回归）

补齐后运行回链校验：

```bash
py -3 scripts/python/task_links_validate.py
```

## 4) 先做测试与场景骨架，再做逻辑

### 4.1 Core 单元测试入口（xUnit）

- `Game.Core.Tests/Domain/GameTurnSystemTests.cs`
  - 覆盖 `StartNewWeek` 初始化与 `Advance` 的 Phase 切换
- `Game.Core.Tests/Domain/EventEngineTests.cs`
  - 覆盖三阶段执行顺序与事件发布/状态变更的可测行为

### 4.2 场景测试骨架（GdUnit4）

- `Tests.Godot/tests/Scenes/Guild/T2PlayableSceneTests.gd`
  - 启动 T2 场景
  - 模拟最小交互（例如点击“结束本周”）
  - 断言 UI 上 Week/Phase 变化

### 4.3 Godot 场景骨架

- 建议在 `Game.Godot/Scenes/` 下提供一个明确的 T2 入口场景（例如 `GuildManagerT2.tscn`），先保证可启动、可退出、UI 可观察。

## 5) 示例验收条款（可用于 Checklist 与任务 acceptance）

> **首个 T2 Playable 场景流（GM-0103 对齐）**
> - 启动后进入 Guild Manager T2 主场景（自动进入或一跳进入）
> - 场景展示当前 Week 与 Phase（Resolution / Player / AiSimulation）
> - 玩家可用最少点击完成一轮回合切换
> - 完成一轮后 Week 从 1 变为 2，Phase 回到 Resolution，且 UI 可观察
> - 流程无未捕获异常，GdUnit4 在 CI headless 通过
> - 对应行为由 xUnit 覆盖验证，并满足 ADR-0015 的回合循环性能软门禁
