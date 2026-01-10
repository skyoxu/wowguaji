# 项目文档索引（wowguaji）

> 项目定位：Godot 4.5.1 + C#/.NET 8（Windows-only）可复制模板与工程骨架  
> 说明：`docs/migration/**` 是历史对照资料库，不作为当前口径的唯一来源

---

## Quick Links（先看这些）

- 项目总览：`../README.md`
- AI/协作规则（SSoT）：`../CLAUDE.md`、`../AGENTS.md`
- 快速开始：`TEMPLATE_GODOT_GETTING_STARTED.md`
- 测试框架：`testing-framework.md`
- 架构骨干导航（Base）：`architecture/base/00-README.md`

---

## 1) 入口文档（SSoT）

- `../README.md`：模板简介、常用入口
- `../CLAUDE.md`：协作口径、门禁、日志规范
- `../AGENTS.md`：Codex CLI 工作规范与止损机制

---

## 2) Getting Started（开始开发）

- `TEMPLATE_GODOT_GETTING_STARTED.md`：从 0 到可跑/可测/可导出（Windows）
- `testing-framework.md`：xUnit + GdUnit4 + 覆盖率/门禁（Windows）

---

## 3) 架构文档（Base-Clean，arc42 12 章）

目录：`architecture/base/`

- `architecture/base/00-README.md`：Base 导航与维护说明

---

## 4) ADR（架构决策记录）

目录：`adr/`

- `architecture/ADR_INDEX_GODOT.md`：ADR 索引（Accepted + Addenda）
- `adr/guide.md`：ADR 编写指南

---

## 5) Workflows（CI/协作手册）

目录：`workflows/`

- `workflows/GM-NG-T2-playable-guide.md`：可玩度/Release 工作流与 Release Health 说明
- `workflows/doc-stack-convergence-guide.md`：文档口径收敛与验证步骤
- `workflows/serena-mcp-command-reference.md`：Serena / Codex CLI 常用命令
- `workflows/superclaude-command-reference.md`：SuperClaude 工作流说明
- `workflows/task-master-superclaude-integration.md`：Taskmaster + SuperClaude 集成

---

## 6) Migration（历史对照与资料库）

目录：`migration/`

- `migration/MIGRATION_INDEX.md`

---

## 7) Scripts & CI（可执行入口）

### PowerShell（Windows）

说明：文档里出现的 `pwsh` 指 PowerShell 7；若本机未安装 `pwsh`，可用 `powershell -ExecutionPolicy Bypass -File <script.ps1>` 等价替代。

- `../scripts/ci/quality_gate.ps1`：一键门禁入口（产出 `logs/**`）
- `../scripts/ci/smoke_headless.ps1`：Godot headless 冒烟
- `../scripts/ci/export_windows.ps1`：导出 Windows EXE
- `../scripts/ci/check_perf_budget.ps1`：性能门禁（P95）
- `../scripts/ci/verify_base_clean.ps1`：Base-Clean 校验

### Python（py -3）

- `../scripts/python/quality_gates.py`：本地/CI 统一门禁编排
- `../scripts/python/check_sentry_secrets.py`：Sentry Secrets 软门禁（审计）
- `../scripts/python/check_encoding.py`：UTF-8/疑似乱码扫描（写入 `logs/ci/**`）
- `../scripts/python/scan_doc_stack_terms.py`：旧技术栈术语扫描（用于文档收敛取证）
- `../scripts/python/task_links_validate.py`：任务与 ADR/章节/Overlay 回链校验

---

## 8) 日志与工件（排障入口）

- 统一目录：`../logs/`
- 建议先看：`../logs/ci/<YYYY-MM-DD>/`
