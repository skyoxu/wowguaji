#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a contracts catalog (code inventory).

This script inventories code contracts under Game.Core/Contracts/** and produces
template-friendly artifacts under logs/**.

It is intentionally NOT a gate. It is a review/audit helper that supports:
  - browsing current EventType values quickly
  - spotting duplicate EventType constants
  - comparing task view `contractRefs[]` against what is implemented

Outputs (default):
  logs/ci/<YYYY-MM-DD>/contracts-catalog/contracts-catalog[--<PRD-ID>].md
  logs/ci/<YYYY-MM-DD>/contracts-catalog/summary.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


EVENT_TYPE_CONST_RE = re.compile(r'public\s+const\s+string\s+EventType\s*=\s*"([^"]+)"\s*;')
NAMESPACE_FILE_RE = re.compile(r"^\s*namespace\s+([A-Za-z0-9_.]+)\s*;\s*$", re.MULTILINE)
NAMESPACE_BLOCK_RE = re.compile(r"^\s*namespace\s+([A-Za-z0-9_.]+)\s*\{\s*$", re.MULTILINE)
PUBLIC_TYPE_RE = re.compile(
    r"\bpublic\s+(?:sealed\s+)?(?:partial\s+)?(record|class|enum|interface)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)
PUBLIC_INTERFACE_RE = re.compile(r"\bpublic\s+interface\s+([A-Za-z_][A-Za-z0-9_]*)\b", re.MULTILINE)


@dataclass(frozen=True)
class InterfaceItem:
    symbol: str
    path: str


def read_text_utf8_sig(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig", errors="replace")


def rel_posix(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def ensure_out_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def detect_namespace(text: str) -> str:
    m = NAMESPACE_FILE_RE.search(text)
    if m:
        return m.group(1)
    m = NAMESPACE_BLOCK_RE.search(text)
    if m:
        return m.group(1)
    return ""


def first_public_type(text: str) -> Optional[dict[str, str]]:
    m = PUBLIC_TYPE_RE.search(text)
    if not m:
        return None
    return {"kind": m.group(1), "name": m.group(2)}


def event_type_value(text: str) -> Optional[str]:
    m = EVENT_TYPE_CONST_RE.search(text)
    return m.group(1).strip() if m else None


def collect_public_interfaces(repo_root: Path, base_dir: Path) -> list[InterfaceItem]:
    if not base_dir.exists():
        return []

    items: list[InterfaceItem] = []
    for cs in sorted(base_dir.rglob("*.cs")):
        if any(seg in {"bin", "obj"} for seg in cs.parts):
            continue
        text = read_text_utf8_sig(cs)
        for m in PUBLIC_INTERFACE_RE.finditer(text):
            items.append(InterfaceItem(symbol=m.group(1), path=rel_posix(repo_root, cs)))
    items.sort(key=lambda x: (x.symbol, x.path))
    return items


def inventory_contracts(repo_root: Path, contracts_root: Path) -> dict[str, Any]:
    if not contracts_root.exists():
        raise FileNotFoundError(f"contracts root not found: {contracts_root}")

    cs_files = sorted(contracts_root.rglob("*.cs"))

    events: list[dict[str, Any]] = []
    other_types: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    seen_event_types: dict[str, str] = {}

    for cs in cs_files:
        if any(seg in {"bin", "obj"} for seg in cs.parts):
            continue

        text = read_text_utf8_sig(cs)
        ns = detect_namespace(text)
        first_type = first_public_type(text) or {"kind": "", "name": cs.stem}
        evt = event_type_value(text)
        rel_path = rel_posix(repo_root, cs)

        if evt:
            item = {
                "event_type": evt,
                "path": rel_path,
                "namespace": ns,
                "type_kind": first_type["kind"],
                "type_name": first_type["name"],
            }
            events.append(item)
            if evt in seen_event_types:
                duplicates.append({"event_type": evt, "first": seen_event_types[evt], "second": rel_path})
            else:
                seen_event_types[evt] = rel_path
            continue

        other_types.append(
            {
                "path": rel_path,
                "namespace": ns,
                "type_kind": first_type["kind"],
                "type_name": first_type["name"],
            }
        )

    events_sorted = sorted(events, key=lambda x: (x.get("event_type", ""), x.get("path", "")))
    other_sorted = sorted(other_types, key=lambda x: (x.get("namespace", ""), x.get("type_name", ""), x.get("path", "")))

    return {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "contracts_root": rel_posix(repo_root, contracts_root),
        "totals": {
            "cs_files": len([p for p in cs_files if p.is_file()]),
            "events": len(events_sorted),
            "other_types": len(other_sorted),
            "duplicate_event_types": len(duplicates),
        },
        "events": events_sorted,
        "other_types": other_sorted,
        "duplicate_event_types": duplicates,
    }


def load_tasks(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return [t for t in data if isinstance(t, dict)]
    if isinstance(data, dict):
        tasks = data.get("tasks")
        if isinstance(tasks, list):
            return [t for t in tasks if isinstance(t, dict)]
    return []


def collect_task_contract_refs(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for t in tasks:
        task_id = t.get("id") or t.get("task_id") or t.get("taskId")
        title = t.get("title") or t.get("name")
        refs = t.get("contractRefs") or t.get("contract_refs") or []
        if isinstance(refs, str):
            refs = [refs]
        if not isinstance(refs, list):
            refs = []
        refs_norm = sorted({str(x).strip() for x in refs if str(x).strip()})
        if not refs_norm:
            continue
        out.append({"id": str(task_id) if task_id is not None else None, "title": title, "contractRefs": refs_norm})
    out.sort(key=lambda x: (x.get("id") or "", x.get("title") or ""))
    return out


def md_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("`", "\\`")


def sanitize_filename_component(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return safe.strip("-") or "unnamed"


def render_iface_section(lines: list[str], title: str, items: list[InterfaceItem]) -> None:
    lines.append(f"## {title}")
    if not items:
        lines.append("- (none)")
        lines.append("")
        return
    for it in items:
        lines.append(f"- `{md_escape(it.symbol)}` -> `{md_escape(it.path)}`")
    lines.append("")


def render_catalog_md(
    *,
    prd_id: Optional[str],
    domain_prefix: str,
    inventory: dict[str, Any],
    ports: list[InterfaceItem],
    services: list[InterfaceItem],
    repositories: list[InterfaceItem],
    tasks_back: list[dict[str, Any]],
    tasks_gameplay: list[dict[str, Any]],
) -> str:
    lines: list[str] = []

    header_prd = f" ({md_escape(prd_id)})" if prd_id else ""
    lines.append(f"# Contracts Catalog{header_prd} (generated)")
    lines.append("")
    lines.append(f"- Generated at (UTC): `{md_escape(inventory['generated_at_utc'])}`")
    lines.append(f"- Generator: `scripts/python/generate_contracts_catalog.py`")
    lines.append(f"- Domain prefix filter: `{md_escape(domain_prefix)}.*`")
    lines.append("")

    totals = inventory["totals"]
    lines.append("## Totals")
    lines.append(f"- cs_files: {totals['cs_files']}")
    lines.append(f"- events: {totals['events']}")
    lines.append(f"- duplicate_event_types: {totals['duplicate_event_types']}")
    lines.append("")

    lines.append("## Sources (SSoT references)")
    lines.append(f"- Contracts (code): `{md_escape(inventory['contracts_root'])}`")
    lines.append("")

    lines.append("## Domain Events (EventType)")
    domain_events = [e for e in inventory["events"] if str(e.get("event_type", "")).startswith(domain_prefix + ".")]
    if not domain_events:
        lines.append("- (none)")
        lines.append("")
    else:
        for e in domain_events:
            type_name = e.get("type_name") or ""
            type_suffix = f" ({md_escape(type_name)})" if type_name else ""
            lines.append(f"- `{md_escape(e['event_type'])}` -> `{md_escape(e['path'])}`{type_suffix}")
        lines.append("")

    if inventory.get("duplicate_event_types"):
        lines.append("## Duplicate EventType (warning)")
        for dup in inventory["duplicate_event_types"]:
            lines.append(
                f"- `{md_escape(dup['event_type'])}`: `{md_escape(dup['first'])}` vs `{md_escape(dup['second'])}`"
            )
        lines.append("")

    render_iface_section(lines, "Ports (Core abstractions)", ports)
    render_iface_section(lines, "Services (Core abstractions)", services)
    render_iface_section(lines, "Repositories (persistence abstractions)", repositories)

    lines.append("## By task (contractRefs view)")
    if not tasks_back and not tasks_gameplay:
        lines.append("- (none)")
        lines.append("")
    else:
        if tasks_back:
            lines.append("### tasks_back.json")
            for t in tasks_back:
                label = t.get("id") or "(no-id)"
                title = t.get("title")
                title_suffix = f" - {md_escape(str(title))}" if title else ""
                lines.append(f"- **{md_escape(str(label))}**{title_suffix}")
                for r in t["contractRefs"]:
                    lines.append(f"  - `{md_escape(r)}`")
            lines.append("")
        if tasks_gameplay:
            lines.append("### tasks_gameplay.json")
            for t in tasks_gameplay:
                label = t.get("id") or "(no-id)"
                title = t.get("title")
                title_suffix = f" - {md_escape(str(title))}" if title else ""
                lines.append(f"- **{md_escape(str(label))}**{title_suffix}")
                for r in t["contractRefs"]:
                    lines.append(f"  - `{md_escape(r)}`")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a contracts catalog (code inventory).")
    parser.add_argument("--prd-id", default="", help="Optional PRD id label (used for output naming).")
    parser.add_argument("--domain-prefix", default="core", help="Domain prefix filter for EventType (default: core).")
    parser.add_argument("--contracts-root", default="Game.Core/Contracts", help="Contracts root directory (default: Game.Core/Contracts).")
    parser.add_argument("--tasks-back", default=".taskmaster/tasks/tasks_back.json", help="Optional tasks_back view path.")
    parser.add_argument("--tasks-gameplay", default=".taskmaster/tasks/tasks_gameplay.json", help="Optional tasks_gameplay view path.")
    parser.add_argument("--out-dir", default="", help="Optional output directory (default: logs/ci/<date>/contracts-catalog).")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    contracts_root = (root / args.contracts_root).resolve()

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = Path(args.out_dir) if args.out_dir else (root / "logs" / "ci" / date_str / "contracts-catalog")
    ensure_out_dir(out_dir)

    inv = inventory_contracts(root, contracts_root)
    ports = collect_public_interfaces(root, root / "Game.Core" / "Ports")
    services = collect_public_interfaces(root, root / "Game.Core" / "Services")
    repos = collect_public_interfaces(root, root / "Game.Core" / "Repositories")

    tasks_back_refs = collect_task_contract_refs(load_tasks(root / str(args.tasks_back)))
    tasks_gameplay_refs = collect_task_contract_refs(load_tasks(root / str(args.tasks_gameplay)))

    prd_id = args.prd_id.strip() or None
    md_name = "contracts-catalog.md" if not prd_id else f"contracts-catalog--{sanitize_filename_component(prd_id)}.md"
    out_md = out_dir / md_name
    out_json = out_dir / "summary.json"

    out_md.write_text(
        render_catalog_md(
            prd_id=prd_id,
            domain_prefix=str(args.domain_prefix).strip(),
            inventory=inv,
            ports=ports,
            services=services,
            repositories=repos,
            tasks_back=tasks_back_refs,
            tasks_gameplay=tasks_gameplay_refs,
        ),
        encoding="utf-8",
    )

    report = {
        "status": "ok",
        "generated_at_utc": inv["generated_at_utc"],
        "prd_id": prd_id,
        "domain_prefix": str(args.domain_prefix).strip(),
        "paths": {
            "contracts_root": inv["contracts_root"],
            "tasks_back": str(args.tasks_back),
            "tasks_gameplay": str(args.tasks_gameplay),
            "out_md": out_md.as_posix(),
            "out_json": out_json.as_posix(),
        },
        "counts": {
            "events": inv["totals"]["events"],
            "duplicate_event_types": inv["totals"]["duplicate_event_types"],
            "ports": len(ports),
            "services": len(services),
            "repositories": len(repos),
            "tasks_back_with_contractRefs": len(tasks_back_refs),
            "tasks_gameplay_with_contractRefs": len(tasks_gameplay_refs),
        },
    }
    out_json.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    print(f"CONTRACTS_CATALOG status=ok out_md={out_md.as_posix()} out_json={out_json.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
