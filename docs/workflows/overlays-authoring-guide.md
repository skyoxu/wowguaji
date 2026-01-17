# overlays 编写与维护指南（wowguaji 口径）

本指南的目标是：让 `docs/architecture/overlays/**` **自己可维护、可检索、可避免误用**。

## 非 SSoT 声明（止损边界）

- overlays 不是任务的单一事实源（SSoT）。
- 任务真相以任务文件为准：`.taskmaster/tasks/tasks.json` 与视图任务文件（例如 `.taskmaster/tasks/tasks_back.json`、`.taskmaster/tasks/tasks_gameplay.json`）。
- PRD 仅作参考；overlays 不承载任务拆分、排期或实现步骤。

## 适用范围

- 本指南只覆盖 overlays 自身的写作与维护，不规定代码实现方式。
- 08 章只写在 overlays：`docs/architecture/overlays/<PRD-ID>/08/`。

## 目录结构（固定）

每个 `PRD-ID` 一套 overlays（建议只维护一个 08 目录）：

```text
docs/
  architecture/
    overlays/
      <PRD-ID>/
        08/
          _index.md
          ACCEPTANCE_CHECKLIST.md
          08-Feature-Slice-*.md
```

约定：

- 文件名使用英文（路径稳定，降低 Windows/CI 的编码与差异比较风险）。
- 正文用中文（便于团队阅读与 review）。
- `PRD-ID` 在 overlays 里只作为“目录键/检索入口”，不要求与 PRD 文档强绑定。

## Front Matter 最小约束（必须）

每个 `08/*.md` 页面必须包含 YAML front matter，且字段必须存在（允许空数组，但不能缺字段）：

- `PRD-ID`
- `Title`
- `Status`（仅允许：`Active` / `Proposed` / `Template`）
- `Intent`（建议：`Index` / `Checklist` / `Overview` / `FeatureSlice`）
- `SSoT`（建议固定：`task_views`，用于强调 overlays 的非 SSoT 定位）
- `Tags`（英文固定集，用于检索；见下一节）
- `ADR-Refs`（允许为空）
- `Arch-Refs`（允许为空）
- `Test-Refs`（允许为空，但必须维护；不能弃用）

示例：

```md
---
PRD-ID: PRD-WOWGUAJI-T2
Title: 功能纵切验收清单（wowguaji）
Status: Active
Intent: Checklist
SSoT: task_views
Tags: [checklist, t2]
ADR-Refs: []
Arch-Refs: []
Test-Refs: []
---
```

## Tags 固定集（英文）

当前仓库对 `PRD-WOWGUAJI-T2` 采用固定 Tags 集合（用于搜索过滤与脚本一致性）：

- `t2`
- `index`
- `checklist`
- `overview`
- `core_loop`
- `gathering`
- `crafting`
- `combat`
- `regions_map`
- `save_offline`
- `dlc`
- `ui_dashboard`

说明：

- 若新增新的 `PRD-ID` 或新的纵切主题，先明确该主题的 Tags，再决定是否扩展固定集（避免“自由标签”导致不可检索/不可统一）。

## 编辑纪律（最小规则）

- 新增/删除/重命名任一 `08/*.md`：必须同步更新同目录 `08/_index.md` 的导航（避免目录漂移）。
- `Test-Refs` 允许为空，但不能长期不维护；空值必须明确写成 `[]`，避免“字段缺失”。
- overlays 的正文只写“可读口径”（范围/非目标/失败与降级/验收要点/影响面），不要写成实现手册或排期文档。

## 自检与留痕（Windows）

推荐在提交前执行：

```powershell
py -3 scripts/python/normalize_overlays.py
py -3 scripts/python/validate_task_overlays.py
```

留痕约定：

- `normalize_overlays.py` 会在 `logs/ci/<YYYY-MM-DD>/` 输出审计 JSON。
- 其他脚本若只输出控制台，建议用重定向将输出留存在 `logs/ci/<YYYY-MM-DD>/`，便于排障与归档。

