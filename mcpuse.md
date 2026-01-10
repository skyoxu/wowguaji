# MCP 工具使用指南（wowguaji）

本仓库以 Godot 4.5 + C#/.NET 8（Windows-only）为主线，默认不引入与旧前端/旧桌面壳相关的 MCP 工具与工作流。

## 1) Sequential Thinking

适用：复杂问题拆解、多步规划、方案评估。

约束：

- 输出可执行计划，不输出中间推理细节
- 小步推进，每步可验证

## 2) Context7

适用：查询 SDK/API/框架官方文档与示例。

流程：

- `resolve-library-id` -> `get-library-docs` -> 摘要成可执行要点

## 3) Serena

适用：符号级检索、跨文件引用分析、重构改名（尤其适合 C#）。

常用工具：

- 检索：`find_symbol`、`find_referencing_symbols`、`get_symbols_overview`
- 文本检索：`search_for_pattern`
- 安全编辑：`insert_before_symbol`、`insert_after_symbol`、`replace_symbol_body`、`rename_symbol`

策略：

- 单轮单符号，避免批量误改
- 改动前先确认影响范围（引用链 + 编译/测试）
- 重要输出包含文件路径与行号

## 4) 命令执行标准（Windows）

- 路径统一使用双引号包裹
- PowerShell 默认用 `py -3` 调用 Python
- 任何测试/审计输出统一写入 `logs/**`（见 `AGENTS.md`）

## 5) 常用校验入口

- 任务回链校验：`py -3 scripts/python/task_links_validate.py`
- 一键门禁编排：`py -3 scripts/python/quality_gates.py --typecheck --lint --unit --scene --security --perf`
