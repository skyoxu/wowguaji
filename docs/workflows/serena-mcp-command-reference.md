# Serena MCP 常用命令参考（wowguaji）

> Serena MCP 是基于 LSP（Language Server Protocol）的符号级检索与重构工具，适合 C# 跨文件改动与 TDD 修复。

本文目标：给出“可复制的命令套路”。示例分两类：
- 通用模板：用 `<...>` 表示你需要替换的占位符
- 本仓库示例：只引用仓库内真实存在的文件（避免旧项目语境与失效路径）

---

## 0) 本仓库可用的示例目标（真实存在）

- `Game.Core/Services/EventBus.cs`（含 `IEventBus` 接口）
- `Game.Core/Services/CombatService.cs`（含 `CombatService` 类与 `ApplyDamage` 重载）
- `Game.Core.Tests/Services/CombatServiceTests.cs`（对应测试文件）

---

## 1) 查符号：`find_symbol`

用途：按名称路径模式查类/接口/方法等符号定义。

```bash
find_symbol "<name_path_pattern>" --relative_path "<file_or_dir>" --depth=1 --include_body=false
```

### 1.1 通用模板

```bash
# Fuzzy: find all symbols containing a keyword
find_symbol "<Keyword>" --substring_matching=true --depth=1

# Precise: find a symbol in a specific file
find_symbol "<TypeOrMemberName>" --relative_path "<relative_path_to_file>" --include_body=true
```

### 1.2 本仓库示例（推荐先跑这个确认工具可用）

```bash
find_symbol "IEventBus" --relative_path "Game.Core/Services/EventBus.cs" --depth=1 --include_body=false
find_symbol "CombatService/ApplyDamage" --relative_path "Game.Core/Services/CombatService.cs" --depth=0 --substring_matching=true
```

---

## 2) 看文件符号概览：`get_symbols_overview`

用途：快速了解一个文件里有哪些顶层符号（类/接口/方法列表）。

```bash
get_symbols_overview "<relative_path_to_file>" --depth=1
```

示例：

```bash
get_symbols_overview "Game.Core/Services/CombatService.cs" --depth=2
```

---

## 3) 查引用：`find_referencing_symbols`

用途：找到某个符号被哪些地方调用/引用（跨文件影响面分析）。

```bash
find_referencing_symbols "<name_path>" --relative_path "<file_path_containing_symbol>"
```

示例：

```bash
find_referencing_symbols "CombatService" --relative_path "Game.Core/Services/CombatService.cs"
```

---

## 4) 重命名：`rename_symbol`

用途：安全地跨文件重命名类/方法/接口（LSP-aware），避免漏改引用。

```bash
rename_symbol "<name_path>" --relative_path "<file_path_containing_symbol>" --new_name "<NewName>"
```

注意：
- 大范围重命名先跑 `find_referencing_symbols` 评估影响面
- 先让单测变红（或至少证明覆盖到改动点），再改名与修复

---

## 5) 改实现：`replace_symbol_body`

用途：替换某个符号的实现体（通常用于按 TDD 修复函数/方法）。

```bash
replace_symbol_body "<name_path>" --relative_path "<file_path_containing_symbol>" --body "<NEW_BODY>"
```

建议流程：
1) 用 `find_symbol` 把目标符号的现有实现取出来（确保你知道“body”边界）
2) 先写/改测试让它失败（red）
3) `replace_symbol_body` 改到通过（green）

---

## 6) 插入代码：`insert_before_symbol` / `insert_after_symbol`

用途：在某个符号定义前/后插入新内容（新增方法/新增类/新增 import）。

```bash
insert_before_symbol "<name_path>" --relative_path "<file_path_containing_symbol>" --body "<CONTENT>"
insert_after_symbol  "<name_path>" --relative_path "<file_path_containing_symbol>" --body "<CONTENT>"
```

提示：
- 新增成员优先 `insert_after_symbol "<ClassName>"`，把方法插入到类的末尾附近
- 新增 `using`/imports 优先插在文件第一个符号之前

---

## 7) 任意文本搜索：`search_for_pattern`

用途：当你不知道符号名（或要搜非代码文件）时，用正则查找。

```bash
search_for_pattern "<regex>" --relative_path "<file_or_dir>" --restrict_search_to_code_files=true
```

示例：

```bash
search_for_pattern "TODO\\(|FIXME" --relative_path "." --restrict_search_to_code_files=false
```

---

## 8) 最小实战套路（建议）

### 8.1 修一个方法（TDD）

1) 找符号：`find_symbol "<Class>/<Method>" --relative_path "<file>" --include_body=true`
2) 找引用：`find_referencing_symbols "<Class>/<Method>" --relative_path "<file>"`
3) 写/改测试（xUnit）让它失败
4) `replace_symbol_body` 修实现
5) 跑单测与门禁：`py -3 scripts/python/quality_gates.py --typecheck --lint --unit`

### 8.2 只做一次“安全重命名”

1) `find_referencing_symbols` 评估影响面
2) `rename_symbol` 一次性改名
3) 修编译与测试

---

## 9) 约束与止损

- 本仓库主线是 Godot + C#（Windows-only）；避免引用旧前端/旧桌面壳语境与失效路径。
- 任何会落地为代码/测试的改动：至少引用 1 条 Accepted ADR，并把产物落到 `logs/**`（见 `AGENTS.md`）。

