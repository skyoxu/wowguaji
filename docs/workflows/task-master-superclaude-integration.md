# Taskmaster + SuperClaude 集成（wowguaji）

目标：把“文档口径（ADR/Base/Overlay）-> 任务（Taskmaster）-> 代码与测试（Godot+C#）-> 门禁与日志（logs/**）”串成可回归闭环。

范围：本仓库仅覆盖 Godot 4.5 + C#/.NET 8（Windows-only）。不包含旧前端或旧桌面壳相关工作流。

---

## 1) 任务文件约定（初始化后生成）

Taskmaster 相关文件在初始化后通常位于：

- `.taskmaster/tasks/tasks_back.json`
- `.taskmaster/tasks/tasks_gameplay.json`
- `.taskmaster/tasks/tasks.json`（MCP view）

本仓库提供的校验脚本会从仓库根目录解析这些路径；如果你尚未初始化 `.taskmaster`，先完成初始化再执行相关脚本。

---

## 2) 任务回链与验收（必须）

每个会落地为代码/测试的改动，任务里至少要包含：

- `adr_refs`：引用 1 条以上 Accepted ADR（最少 ADR-0005/ADR-0019/ADR-0004/ADR-0003）
- `chapter_refs`：引用 Base 章节（例如 CH01/CH02/CH03/CH07）
- `overlay_refs`：如涉及 08 功能纵切，指向 `docs/architecture/overlays/<PRD-ID>/08/**`
- `test_refs`：指向真实存在的 xUnit/GdUnit4 测试文件路径

校验命令：

- `py -3 scripts/python/task_links_validate.py`

---

## 3) 推荐执行节奏（TDD + 小步绿灯）

1. 选择一个任务，置为 `in-progress`
2. 写测试（先红后绿）
3. 实现并通过测试
4. 跑门禁并生成日志/工件
5. 更新任务的 `acceptance` 与 `test_refs`

门禁入口：

- `py -3 scripts/python/quality_gates.py --typecheck --lint --unit --scene --security --perf`

---

## 4) 常见失败止损

- 任务回链失败：先修 `adr_refs/chapter_refs/overlay_refs/test_refs`，不要先改实现
- 门禁失败：先看 `logs/ci/<YYYY-MM-DD>/` 与 `logs/unit/<YYYY-MM-DD>/`
- 编码/乱码：先跑 `py -3 scripts/python/check_encoding.py`，按报告修复到 UTF-8
