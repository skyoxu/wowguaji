# wowguaji（Godot 4.5 + C#，Windows-only）

可复制、可测试、可导出（Windows Desktop EXE）的 Godot 4.5.1 + C#/.NET 8 项目模板与工程骨架。

入口文档与口径：
- `CLAUDE.md`
- `AGENTS.md`
- `docs/PROJECT_DOCUMENTATION_INDEX.md`

---

## 快速开始（从 0 到导出）

1) 安装 Godot 4.5.1 .NET（mono），并设置环境变量：
- `setx GODOT_BIN "C:\\Godot\\Godot_v4.5.1-stable_mono_win64.exe"`

2) 先跑 headless 冒烟（失败止损快）：
- `./scripts/ci/smoke_headless.ps1 -GodotBin "$env:GODOT_BIN"`

3) 在 Godot Editor 安装 Export Templates（Windows Desktop）。

4) 导出并对 EXE 冒烟：
- `./scripts/ci/export_windows.ps1 -GodotBin "$env:GODOT_BIN" -Output build\\Game.exe`
- `./scripts/ci/smoke_exe.ps1 -ExePath build\\Game.exe`

---

## 常用入口

- 文档索引：`docs/PROJECT_DOCUMENTATION_INDEX.md`
- Godot+C# 快速开始：`docs/TEMPLATE_GODOT_GETTING_STARTED.md`
- 测试框架：`docs/testing-framework.md`
- Base 架构骨干（arc42）：`docs/architecture/base/00-README.md`

---

## 命令与门禁（Windows）

- 一键门禁编排：`py -3 scripts/python/quality_gates.py --help`
- 单元测试：`dotnet test --collect:"XPlat Code Coverage"`

---

## 命名说明

- 仓库名：`wowguaji`
- 默认 Godot/.NET 工程名可能仍为 `GodotGame`（如需彻底改名，请同步更新 `project.godot`、`.sln`、`.csproj`、命名空间与 CI 脚本）
