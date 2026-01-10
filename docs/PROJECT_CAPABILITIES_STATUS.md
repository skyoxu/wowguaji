# 项目能力状态总览（wowguaji）

> 目的：从“可运行 + 可测试 + 可导出 + 可审计（logs/**）”的角度，概览 wowguaji 作为 Godot 4.5 + C#/.NET 8（Windows-only）模板当前具备的能力与可选增强方向。

范围声明：本文件只覆盖 Godot+C# 模板能力，不维护旧前端/旧桌面壳相关能力清单。

---

## 1) 已具备（Implemented）

- 三层架构：`Game.Core`（纯 C#）/ `Game.Godot`（适配层）/ 场景与 Glue（Godot）
- 数据存储：SQLite + ConfigFile（Settings SSoT），路径与审计约束见 ADR-0006/ADR-0023/ADR-0019
- 测试体系：xUnit（Core）+ GdUnit4（场景），支持 headless
- 质量门禁编排：`py -3 scripts/python/quality_gates.py`（产出写入 `logs/**`）
- Base/ADR/Overlay 文档骨架：`docs/architecture/base/**`、`docs/adr/**`、`docs/architecture/overlays/**`

---

## 2) 进行中/可选增强（Backlog-like）

- Release Health（Sentry）：对齐 ADR-0003，完善 CI 的 release-health 门禁与审计工件
- 性能预算与门禁：对齐 ADR-0015，补齐更多场景的 P95 采样与阈值治理
- 安全烟测扩充：对齐 ADR-0019，覆盖外链/网络白名单/文件越权/权限默认拒绝等三态用例

---

## 3) 常用入口

- 文档索引：`docs/PROJECT_DOCUMENTATION_INDEX.md`
- 任务回链校验：`py -3 scripts/python/task_links_validate.py`
- 一键门禁：`py -3 scripts/python/quality_gates.py --typecheck --lint --unit --scene --security --perf`
