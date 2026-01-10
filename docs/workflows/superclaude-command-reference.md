# SuperClaude 命令参考（wowguaji）

本仓库的主线是 Godot 4.5 + C#/.NET 8（Windows-only）。任何涉及旧前端/旧桌面壳/E2E Web 的内容不属于当前口径。

---

## 1) 推荐工作流（最短闭环）

1. 选定任务（Taskmaster）
2. 先写/改测试（xUnit，必要时补 GdUnit4）
3. 实现最小改动
4. 跑门禁脚本（产出写入 `logs/**`）
5. 生成提交信息与变更说明（SuperClaude）

---

## 2) 常用命令（Windows）

- 一键门禁编排：`py -3 scripts/python/quality_gates.py --typecheck --lint --unit --scene --security --perf`
- 任务回链校验：`py -3 scripts/python/task_links_validate.py`
- 三任务文件结构总检（如已初始化 `.taskmaster`）：`py -3 scripts/python/validate_task_master_triplet.py`

---

## 3) MCP 工具（最小集合）

默认只启用与 Godot+C# 相关的 MCP 工具：

- `serena`：符号级检索与安全编辑（C# 重构更稳）
- `context7`：官方文档与 API 查询

说明：本仓库不维护 Web UI E2E 相关 MCP 服务器配置与文档。
