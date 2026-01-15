#!/usr/bin/env python3
"""
Validate Contracts coding rules (SSoT: Game.Core/Contracts/**).

This checker is defensive: it prevents drift in contract naming, docs, and dependencies.

Rules (high-level):
- No Godot dependency in Contracts.
- No dynamic/object in contract payloads (except DomainEvent envelope).
- EventType must follow ADR-0004 prefixes: core.*.* / ui.menu.* / screen.*.*.
- Event contracts must have XML docs (<summary>, <remarks>) and reference ADR + Overlay.
- Event contract files must be referenced by at least one Overlay 08 doc (backtick path).
- EventType should be referenced by at least one task view via contractRefs.

Artifacts:
- logs/ci/<YYYY-MM-DD>/contract-rules.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional


CONTRACTS_DIR = Path("Game.Core") / "Contracts"
OVERLAYS_DIR = Path("docs") / "architecture" / "overlays"
TASK_VIEWS = [
    Path(".taskmaster") / "tasks" / "tasks_back.json",
    Path(".taskmaster") / "tasks" / "tasks_gameplay.json",
]

EVENTTYPE_PREFIX_RE = re.compile(r"^(core|ui\.menu|screen)\.")
EVENTTYPE_ALLOWED_RE = re.compile(r"^(core|ui\.menu|screen)\.[a-z0-9_]+(\.[a-z0-9_]+)+$")
EVENTTYPE_CONST_RE = re.compile(r'public\s+const\s+string\s+EventType\s*=\s*"([^"]+)"\s*;')
CONTRACT_REF_RE = re.compile(r"`(Game\.Core/Contracts/[^`]+?\.cs)`")


ALLOW_OBJECT_FILES = {
    "Game.Core/Contracts/DomainEvent.cs",
}


@dataclass(frozen=True)
class Violation:
    code: str
    file: str
    message: str
    detail: Optional[str] = None


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def list_contract_cs_files(root: Path) -> List[Path]:
    contracts_root = root / CONTRACTS_DIR
    if not contracts_root.exists():
        return []
    return sorted([p for p in contracts_root.rglob("*.cs") if not p.name.endswith(".cs.uid")])


def list_overlay_docs(root: Path) -> List[Path]:
    overlays_root = root / OVERLAYS_DIR
    if not overlays_root.exists():
        return []
    docs: List[Path] = []
    for prd_dir in overlays_root.iterdir():
        if not prd_dir.is_dir():
            continue
        chapter_dir = prd_dir / "08"
        if not chapter_dir.exists():
            continue
        docs.extend(sorted(chapter_dir.glob("*.md")))
    return docs


def extract_overlay_contract_refs(md_text: str) -> List[str]:
    return CONTRACT_REF_RE.findall(md_text)


def collect_overlay_referenced_contracts(root: Path) -> set[str]:
    out: set[str] = set()
    for md in list_overlay_docs(root):
        text = read_text_utf8(md)
        out.update(extract_overlay_contract_refs(text))
    return out


def collect_task_contractrefs(root: Path) -> set[str]:
    out: set[str] = set()
    for view in TASK_VIEWS:
        p = root / view
        if not p.exists():
            continue
        try:
            tasks = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for t in tasks:
            for evt in (t.get("contractRefs") or []):
                if isinstance(evt, str) and evt:
                    out.add(evt)
    return out


def is_event_contract(text: str) -> bool:
    return EVENTTYPE_CONST_RE.search(text) is not None


def find_event_type(text: str) -> Optional[str]:
    m = EVENTTYPE_CONST_RE.search(text)
    return m.group(1) if m else None


def contains_forbidden_godot(text: str) -> bool:
    return ("using Godot" in text) or ("Godot." in text)


def find_forbidden_object_dynamic(text: str) -> List[str]:
    hits: List[str] = []
    if re.search(r"\bdynamic\b", text):
        hits.append("dynamic")
    if re.search(r"\bobject\b", text):
        hits.append("object")
    return hits


def has_xml_summary(text: str) -> bool:
    return "/// <summary>" in text and "/// </summary>" in text


def has_xml_remarks(text: str) -> bool:
    return "/// <remarks>" in text and "/// </remarks>" in text


def mentions_adr_in_remarks(text: str) -> bool:
    # Heuristic: we only require at least one ADR id mention.
    return "ADR-" in text


def mentions_overlay_in_remarks(text: str) -> bool:
    return ("Overlay:" in text) and ("docs/architecture/overlays/" in text)


def mentions_domain_event_line(text: str, event_type: str) -> bool:
    return f"Domain event: {event_type}" in text


def validate_event_type_value(path: str, event_type: str) -> List[Violation]:
    out: List[Violation] = []
    if "-" in event_type:
        out.append(Violation("eventtype.invalid_char", path, "EventType contains '-' (dash)."))
    if any(ch.isupper() for ch in event_type):
        out.append(Violation("eventtype.uppercase", path, "EventType contains uppercase letters."))
    if not EVENTTYPE_PREFIX_RE.match(event_type):
        out.append(Violation("eventtype.prefix", path, "EventType must start with core./ui.menu./screen."))
    if not EVENTTYPE_ALLOWED_RE.match(event_type):
        out.append(Violation("eventtype.pattern", path, "EventType contains invalid characters or structure.", event_type))
    return out


def validate_contract_file(
    root: Path,
    cs_file: Path,
    overlay_contract_refs: set[str],
    task_contract_refs: set[str],
) -> List[Violation]:
    rel = cs_file.relative_to(root).as_posix()
    out: List[Violation] = []

    try:
        text = read_text_utf8(cs_file)
    except UnicodeDecodeError as e:
        return [Violation("encoding.utf8", rel, "Contract file must be UTF-8.", str(e))]

    if contains_forbidden_godot(text):
        out.append(Violation("forbidden.godot", rel, "Contracts must not reference Godot APIs."))

    forbidden = find_forbidden_object_dynamic(text)
    if forbidden:
        if rel not in ALLOW_OBJECT_FILES:
            out.append(Violation("forbidden.object_dynamic", rel, "Contracts must not use object/dynamic.", ", ".join(sorted(set(forbidden)))))

    if is_event_contract(text):
        event_type = find_event_type(text)
        if not event_type:
            out.append(Violation("eventtype.missing", rel, "EventType constant missing or unreadable."))
            return out

        out.extend(validate_event_type_value(rel, event_type))

        if not has_xml_summary(text):
            out.append(Violation("xmldoc.summary.missing", rel, "Event contract must have <summary> XML docs."))
        if not has_xml_remarks(text):
            out.append(Violation("xmldoc.remarks.missing", rel, "Event contract must have <remarks> XML docs."))
        if has_xml_remarks(text) and not mentions_adr_in_remarks(text):
            out.append(Violation("xmldoc.remarks.adr", rel, "<remarks> must reference at least one ADR (e.g., ADR-0004)."))
        if has_xml_remarks(text) and not mentions_overlay_in_remarks(text):
            out.append(Violation("xmldoc.remarks.overlay", rel, "<remarks> should reference an Overlay 08 page path."))
        if not mentions_domain_event_line(text, event_type):
            out.append(Violation("xmldoc.summary.eventtype", rel, "<summary> should include 'Domain event: <EventType>'.", event_type))

        if rel.replace("\\", "/") not in overlay_contract_refs:
            out.append(Violation("overlay.reference.missing", rel, "Event contract file must be referenced by an Overlay 08 doc.", rel))

        if event_type not in task_contract_refs:
            out.append(Violation("tasks.contractrefs.missing", rel, "EventType should appear in at least one task view contractRefs.", event_type))

    return out


def write_report(root: Path, report: dict) -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = root / "logs" / "ci" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "contract-rules.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out_path


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Project root directory (default: current directory).")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()

    overlay_refs = collect_overlay_referenced_contracts(root)
    task_refs = collect_task_contractrefs(root)
    contract_files = list_contract_cs_files(root)

    violations: List[Violation] = []
    event_contracts = 0
    for cs in contract_files:
        try:
            text = read_text_utf8(cs)
            if is_event_contract(text):
                event_contracts += 1
        except UnicodeDecodeError:
            # validate_contract_file will report the encoding issue
            pass
        violations.extend(validate_contract_file(root, cs, overlay_refs, task_refs))

    report = {
        "ok": len(violations) == 0,
        "contracts_count": len(contract_files),
        "event_contracts_count": event_contracts,
        "overlay_contract_refs_count": len(overlay_refs),
        "task_contractrefs_unique_count": len(task_refs),
        "violations": [v.__dict__ for v in violations],
        "allow_object_files": sorted(ALLOW_OBJECT_FILES),
        "notes": {
            "adr_refs_required": True,
            "overlay_refs_required": True,
            "tasks_contractrefs_required": True,
        },
    }

    out_path = write_report(root, report)
    print(f"CONTRACT_RULES ok={report['ok']} violations={len(violations)} out={out_path}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
