---
Intent: Index
SSoT: task_views
Tags: [index, t2]
PRD-ID: PRD-WOWGUAJI-T2
Title: 08 章功能纵切索引（wowguaji）
Arch-Refs: [CH01, CH03, CH07, CH10]
Updated: true
---

本目录聚合 `PRD-WOWGUAJI-T2` 的 08 章功能纵切页面与验收清单。

约束：
- 08 章只写“功能纵切”（实体/事件/SLI/门禁/验收/测试对齐）；跨切面口径只引用 Base/ADR，不在本文复制阈值/策略。
- 契约 SSoT 统一落盘到 `Game.Core/Contracts/**`（C#，不依赖 Godot）；文档仅引用路径，不复制契约全文。
- 数据驱动内容（Content）统一按 JSON 落盘在 `Game.Godot/Content/**`，并定义 DLC 合并/校验/降级策略；本目录只写口径，不在此处实现脚本。
- 事件只用于“里程碑/边界点”，遵循统一的“事件升格门槛”（见 `08-Feature-Slice-WOWGUAJI-T2.md`），避免把 tick 级细节事件化。
- 日志与工件路径统一遵循 `AGENTS.md` 的 `logs/**` 规范。

文件：
- 总览纵切：`08-Feature-Slice-WOWGUAJI-T2.md`
- 纵切拆分：
  - `08-Feature-Slice-Core-Loop.md`
  - `08-Feature-Slice-Gathering.md`
  - `08-Feature-Slice-Crafting.md`
  - `08-Feature-Slice-Combat.md`
  - `08-Feature-Slice-Regions-Map.md`
  - `08-Feature-Slice-Save-Offline.md`
  - `08-Feature-Slice-DLC.md`
  - `08-Feature-Slice-UI-Dashboard.md`
- 验收清单：`ACCEPTANCE_CHECKLIST.md`

Contracts（SSoT，引用路径用于校验存在性）：
- `Game.Core/Contracts/CoreLoop/InventoryItemAdded.cs`
