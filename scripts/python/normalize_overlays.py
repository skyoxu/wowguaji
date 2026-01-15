#!/usr/bin/env python3
"""
Normalize Overlay 08 markdown files for maintainability and searchability.

Scope (current):
  docs/architecture/overlays/PRD-WOWGUAJI-T2/08/*.md

Goals:
- Keep overlays lightweight (NOT SSoT for tasks/contracts/tests).
- Keep Test-Refs field (allowed to be empty).
- Add fixed english Tags for search and filtering.
- Add a short "用途边界（防误用）" section if missing.
- Add a short "变更影响面" section if missing.
- Write a JSON report under logs/ci/<YYYY-MM-DD>/.

Encoding:
- Read/write markdown as UTF-8 (no BOM).

Usage (Windows):
  py -3 scripts/python/normalize_overlays.py
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


@dataclass(frozen=True)
class OverlaySpec:
    intent: str
    tags: list[str]
    title_override: str | None = None
    add_misuse_guard: bool = True
    add_impact_section: bool = True


FIXED_TAGS: set[str] = {
    "t2",
    "overview",
    "core_loop",
    "gathering",
    "crafting",
    "combat",
    "regions_map",
    "save_offline",
    "dlc",
    "ui_dashboard",
    "index",
    "checklist",
}


SPECS: dict[str, OverlaySpec] = {
    "_index.md": OverlaySpec(intent="Index", tags=["index", "t2"], add_misuse_guard=False, add_impact_section=False),
    "ACCEPTANCE_CHECKLIST.md": OverlaySpec(
        intent="Checklist",
        tags=["checklist", "t2"],
        title_override="功能纵切验收清单（wowguaji）",
        add_misuse_guard=False,
        add_impact_section=False,
    ),
    "08-Feature-Slice-WOWGUAJI-T2.md": OverlaySpec(intent="Overview", tags=["overview", "t2"]),
    "08-Feature-Slice-Core-Loop.md": OverlaySpec(intent="FeatureSlice", tags=["core_loop", "t2"]),
    "08-Feature-Slice-Gathering.md": OverlaySpec(intent="FeatureSlice", tags=["gathering", "t2"]),
    "08-Feature-Slice-Crafting.md": OverlaySpec(intent="FeatureSlice", tags=["crafting", "t2"]),
    "08-Feature-Slice-Combat.md": OverlaySpec(intent="FeatureSlice", tags=["combat", "t2"]),
    "08-Feature-Slice-Regions-Map.md": OverlaySpec(intent="FeatureSlice", tags=["regions_map", "t2"]),
    "08-Feature-Slice-Save-Offline.md": OverlaySpec(intent="FeatureSlice", tags=["save_offline", "t2"]),
    "08-Feature-Slice-DLC.md": OverlaySpec(intent="FeatureSlice", tags=["dlc", "t2"]),
    "08-Feature-Slice-UI-Dashboard.md": OverlaySpec(intent="FeatureSlice", tags=["ui_dashboard", "t2"]),
}


def ensure_fixed_tags(tags: list[str]) -> list[str]:
    out = []
    for t in tags:
        if t not in FIXED_TAGS:
            raise ValueError(f"Tag not in fixed set: {t}")
        if t not in out:
            out.append(t)
    return out


def parse_front_matter(text: str) -> tuple[dict[str, Any] | None, str, str]:
    """
    Return (fm_dict_or_none, fm_raw_or_empty, body).

    We keep parsing minimal. Unknown keys are preserved by re-emitting the raw block
    with inserted/updated lines for Intent/SSoT/Tags.
    """

    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None, "", text
    fm_raw = m.group(1)
    body = text[m.end() :]
    # Keep only the 5 canonical keys for light validation (do not drop unknown keys).
    fm = {"PRD-ID": None, "Title": None, "Status": None, "ADR-Refs": [], "Test-Refs": []}
    current = None
    for line in fm_raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" in s and not s.startswith("-"):
            k, v = s.split(":", 1)
            k = k.strip()
            v = v.strip()
            if k in fm:
                current = k
                if k in {"ADR-Refs", "Test-Refs"}:
                    fm[k] = []
                    if v:
                        fm[k].append(v)
                else:
                    fm[k] = v if v else None
            else:
                current = None
            continue
        if s.startswith("-") and current in {"ADR-Refs", "Test-Refs"}:
            fm[current].append(s[1:].strip())
    return fm, fm_raw, body


def upsert_front_matter_lines(fm_raw: str, spec: OverlaySpec) -> str:
    lines = fm_raw.splitlines()

    def has_key(prefix: str) -> bool:
        return any(l.strip().startswith(prefix) for l in lines)

    tags = ensure_fixed_tags(spec.tags)
    tags_line = f"Tags: [{', '.join(tags)}]"

    # Optionally override Title (used for non-slice docs like checklists).
    if spec.title_override:
        replaced = False
        new_lines: list[str] = []
        for l in lines:
            if l.strip().startswith("Title:"):
                new_lines.append(f"Title: {spec.title_override}")
                replaced = True
            else:
                new_lines.append(l)
        lines = new_lines
        if not replaced:
            insert_title_at = None
            for i, l in enumerate(lines):
                if l.strip().startswith("PRD-ID:"):
                    insert_title_at = i + 1
                    break
            if insert_title_at is None:
                insert_title_at = 0
            lines.insert(insert_title_at, f"Title: {spec.title_override}")

    # Insert after Status if possible, else near top.
    insert_at = None
    for i, l in enumerate(lines):
        if l.strip().startswith("Status:"):
            insert_at = i + 1
            break
    if insert_at is None:
        insert_at = 0

    # Intent
    if not has_key("Intent:"):
        lines.insert(insert_at, f"Intent: {spec.intent}")
        insert_at += 1
    # SSoT (fixed)
    if not has_key("SSoT:"):
        lines.insert(insert_at, "SSoT: task_views")
        insert_at += 1

    # Tags (override existing)
    new_lines = []
    for l in lines:
        if l.strip().startswith("Tags:"):
            continue
        new_lines.append(l)
    lines = new_lines

    # Add tags after SSoT if present, else after Intent/Status.
    insert_at = None
    for i, l in enumerate(lines):
        if l.strip().startswith("SSoT:"):
            insert_at = i + 1
            break
    if insert_at is None:
        for i, l in enumerate(lines):
            if l.strip().startswith("Intent:"):
                insert_at = i + 1
                break
    if insert_at is None:
        insert_at = 0
    lines.insert(insert_at, tags_line)

    return "\n".join(lines).strip("\n")


def ensure_section(body: str, header: str, content_lines: list[str]) -> str:
    if header in body:
        return body
    # Insert after the first non-empty paragraph, conservatively.
    parts = body.splitlines()
    out: list[str] = []
    inserted = False
    seen_text = False
    for i, line in enumerate(parts):
        out.append(line)
        if not inserted:
            if line.strip():
                # track we've seen some body text; insert after the first blank line following it
                seen_text = True
            elif seen_text:
                out.extend(["", header, *content_lines, ""])
                inserted = True
    if not inserted:
        # body is empty or no blank line found; append at end
        if out and out[-1].strip():
            out.append("")
        out.extend([header, *content_lines, ""])
    return "\n".join(out).rstrip() + "\n"


def strip_section(body: str, header: str) -> tuple[str, bool]:
    """
    Remove a top-level (## ...) section by exact header line.

    Removes from the header line up to (but not including) the next '## ' header,
    or end of file.
    """

    lines = body.splitlines(keepends=True)
    start = None
    for i, l in enumerate(lines):
        if l.strip() == header:
            start = i
            break
    if start is None:
        return body, False

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    new_body = "".join(lines[:start] + lines[end:]).lstrip("\n")
    return new_body, True


def insert_misuse_guard_near_top(body: str, header: str, content_lines: list[str]) -> str:
    """
    Insert a section before the first '## ' heading, keeping the intro text above.
    """

    m = re.search(r"^##\s", body, flags=re.MULTILINE)
    if not m:
        section = "\n".join([header, *content_lines]).rstrip()
        return (body.rstrip() + "\n\n" + section + "\n").rstrip() + "\n"

    pos = m.start()
    before = body[:pos].rstrip()
    after = body[pos:].lstrip()
    section = "\n".join([header, *content_lines]).rstrip()
    return (before + "\n\n" + section + "\n\n" + after).rstrip() + "\n"


def append_section_at_end(body: str, header: str, content_lines: list[str]) -> str:
    section = "\n".join([header, *content_lines]).rstrip()
    return (body.rstrip() + "\n\n" + section + "\n").rstrip() + "\n"


def impact_lines_for(tags: list[str]) -> list[str]:
    # Minimal, high-signal links between slices (not tasks/contracts).
    if "core_loop" in tags:
        return [
            "- 影响所有纵切：tick 推进、状态机边界与可回归性。",
            "- 改动若引入高频更新，需回看“事件升格门槛”与 UI 刷新策略。",
        ]
    if "gathering" in tags:
        return [
            "- 影响 Crafting：材料链路与配方可用性。",
            "- 影响 Save & Offline：离线结算口径与上限策略。",
            "- 影响 UI Dashboard：产出与成长反馈展示。",
        ]
    if "crafting" in tags:
        return [
            "- 影响 Gathering：材料输入与产出平衡。",
            "- 影响 Combat：装备/消耗品对战斗结果的可观察变化。",
            "- 影响 Save & Offline：配方解锁与产物持久化。",
        ]
    if "combat" in tags:
        return [
            "- 影响 Regions & Map：解锁条件与区域推进节奏。",
            "- 影响 UI Dashboard：战斗结算与掉落反馈。",
            "- 影响 Save & Offline：离线战斗口径（T2 不模拟）。",
        ]
    if "regions_map" in tags:
        return [
            "- 影响 Gathering/Combat：区域内可用资源点与怪物池。",
            "- 影响 DLC：DLC 区域的可见/锁定/进入与回馈。",
            "- 影响 UI Dashboard：地图入口与锁定提示。",
        ]
    if "save_offline" in tags:
        return [
            "- 影响所有纵切：存档兼容与离线结算决定整体可回归性。",
            "- 影响 DLC：DLC 启用与内容版本需要可恢复且可降级。",
        ]
    if "dlc" in tags:
        return [
            "- 影响 Regions & Map：DLC 区域的解锁与入口呈现。",
            "- 影响 Gathering/Crafting/Combat：DLC 内容对主循环的回馈联动。",
            "- 影响 Save & Offline：DLC 启用状态与内容版本的可恢复/降级。",
        ]
    if "ui_dashboard" in tags:
        return [
            "- 影响所有纵切：入口编排决定闭环可玩度与可观察性。",
            "- UI 刷新需遵循事件升格门槛：边界点事件 + 状态快照节流。",
        ]
    if "overview" in tags:
        return [
            "- 本页改动会影响所有纵切页的统一口径（内容策略/事件升格门槛/降级规则）。",
            "- 若调整“写死策略”，需同步检查每个纵切页的引用是否仍一致。",
        ]
    return ["- 影响面：待补充（应只描述纵切之间的依赖关系，不写任务/契约细节）。"]


def normalize_file(path: Path, spec: OverlaySpec) -> dict[str, Any]:
    before = path.read_text(encoding="utf-8")
    fm, fm_raw, body = parse_front_matter(before)

    changed = False

    if fm_raw:
        new_fm_raw = upsert_front_matter_lines(fm_raw, spec)
        new_text = f"---\n{new_fm_raw}\n---\n\n{body.lstrip()}"
        changed = changed or (new_text != before)
    else:
        # Create a minimal front matter block if missing (kept small).
        tags = ensure_fixed_tags(spec.tags)
        fm_block = "\n".join(
            [
                "PRD-ID: PRD-WOWGUAJI-T2",
                f"Title: {path.stem}",
                "Status: Active",
                f"Intent: {spec.intent}",
                "SSoT: task_views",
                f"Tags: [{', '.join(tags)}]",
                "ADR-Refs: []",
                "Test-Refs: []",
            ]
        )
        new_text = f"---\n{fm_block}\n---\n\n{before.lstrip()}"
        changed = True

    # Re-parse after front matter update.
    _, _, body2 = parse_front_matter(new_text)

    # Ensure stable placement by stripping and re-inserting.
    if spec.add_misuse_guard:
        misuse_header = "## 0) 用途边界（防误用）"
        misuse_lines = [
            "- 本页只维护：纵切边界、关键流程、数据约束、失败与降级、验收口径、变更影响面。",
            "- 本页不承载：任务拆分/优先级/排期；也不作为任务与实现细节的单一真相来源。",
            "- `Test-Refs` 允许为空；测试清单与回归入口以任务视图文件的后续脚本校验为准。",
        ]
        body2, _ = strip_section(body2, misuse_header)
        body2 = insert_misuse_guard_near_top(body2, misuse_header, misuse_lines)

    if spec.add_impact_section:
        impact_header = "## 99) 变更影响面（跨纵切依赖）"
        body2, _ = strip_section(body2, impact_header)
        body2 = append_section_at_end(body2, impact_header, impact_lines_for(spec.tags))

    # Rebuild final text with existing front matter.
    m = FRONT_MATTER_RE.match(new_text)
    if not m:
        raise RuntimeError(f"Front matter missing after normalization: {path}")
    fm_raw2 = m.group(1)
    final_text = f"---\n{fm_raw2}\n---\n\n{body2.lstrip()}"

    if final_text != before:
        path.write_text(final_text, encoding="utf-8")
        changed = True

    return {
        "file": path.as_posix(),
        "intent": spec.intent,
        "tags": spec.tags,
        "changed": changed,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    overlay_dir = root / "docs" / "architecture" / "overlays" / "PRD-WOWGUAJI-T2" / "08"
    if not overlay_dir.exists():
        raise SystemExit(f"Overlay dir not found: {overlay_dir}")

    results: list[dict[str, Any]] = []
    unknown: list[str] = []
    for md in sorted(overlay_dir.glob("*.md")):
        spec = SPECS.get(md.name)
        if not spec:
            unknown.append(md.name)
            continue
        results.append(normalize_file(md, spec))

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = root / "logs" / "ci" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "overlays-normalize.json"
    report = {
        "generatedAt": date_str,
        "overlayDir": str(overlay_dir.as_posix()),
        "fixedTags": sorted(FIXED_TAGS),
        "files": results,
        "unknownFiles": unknown,
    }
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
