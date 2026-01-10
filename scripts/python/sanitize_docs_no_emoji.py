#!/usr/bin/env python3
"""
Sanitize docs by removing/replacing emoji/dingbat/pictographic symbols.

Why:
- Repo policy forbids emoji characters in all files.
- Some historical docs used pictographic symbols which break this policy.

This script scans .md/.txt files under a root directory and applies a
deterministic replacement mapping, writing a JSON report under:
  logs/ci/<YYYY-MM-DD>/emoji-sanitize.json

Usage (Windows):
  py -3 scripts/python/sanitize_docs_no_emoji.py --root docs --write
  py -3 scripts/python/sanitize_docs_no_emoji.py --write --extra README.md AGENTS.md CLAUDE.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


# Basic emoji/symbol ranges (not exhaustive; intended for policy enforcement).
RANGES: List[Tuple[int, int]] = [
    (0x1F300, 0x1F5FF),
    (0x1F600, 0x1F64F),
    (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F),
    (0x1F780, 0x1F7FF),
    (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF),
    (0x1FA00, 0x1FAFF),
    (0x2600, 0x26FF),
    (0x2700, 0x27BF),
]

# Extra codepoints that show up in this repo and are treated as pictographic.
EXTRA_CODEPOINTS = {
    0x2192,  # RIGHTWARDS ARROW
    0x2194,  # LEFT RIGHT ARROW
    0x23F3,  # HOURGLASS
    0x23F8,  # PAUSE BUTTON
    0x2934,  # ARROW POINTING RIGHTWARDS THEN CURVING UPWARDS
}

VS16 = 0xFE0F  # Variation Selector-16


def is_emoji(cp: int) -> bool:
    if cp == VS16:
        return True
    if cp in EXTRA_CODEPOINTS:
        return True
    return any(a <= cp <= b for a, b in RANGES)


# Deterministic replacements (ASCII-only).
REPLACE_CP: Dict[int, str] = {
    VS16: "",
    0x2192: "->",
    0x2194: "<->",
    0x23F3: "[PENDING]",
    0x23F8: "[PAUSE]",
    0x2934: "[UP]",
    0x2605: "*",
    0x2606: "*",
    0x26AB: "-",
    0x26AA: "-",
    0x2609: "[SUN]",
    0x2705: "[OK]",
    0x2713: "[OK]",
    0x274C: "[X]",
    0x2753: "[?]",
    0x26A0: "[WARN]",
    0x26A1: "[FAST]",
    0x27A1: "->",
    0x1F4CA: "[REPORT]",
    0x1F4C8: "[TREND]",
    0x1F6A8: "[ALERT]",
    0x1F680: "[RELEASE]",
    0x1F512: "[LOCK]",
    0x1F511: "[KEY]",
    0x1F504: "[SYNC]",
    0x1F3AF: "[GOAL]",
    0x1F3D7: "[ARCH]",
    0x1F9EA: "[TEST]",
    0x1F916: "[AI]",
    0x1F9ED: "[COMPASS]",
    0x1F4BB: "[DEV]",
    0x1F4CB: "[CHECKLIST]",
    0x1F517: "[LINK]",
    0x1F4C1: "[DIR]",
    0x1F4DE: "[CONTACT]",
    0x1F4AF: "[100]",
    0x1F534: "O",
    0x1F7E0: "O",
    0x1F7E1: "O",
    0x1F7E2: "O",
}


def iter_text_files(root: Path) -> List[Path]:
    out: List[Path] = []
    if root.is_file():
        out.append(root)
        return out
    for fp in root.rglob("*"):
        if not fp.is_file():
            continue
        if fp.suffix.lower() in {".md", ".txt"}:
            out.append(fp)
    out.sort(key=lambda p: p.as_posix())
    return out


def sanitize_text(text: str) -> tuple[str, Counter, Counter]:
    repl_counts = Counter()
    unknown_counts = Counter()
    out_parts: List[str] = []
    for ch in text:
        cp = ord(ch)
        if not is_emoji(cp):
            out_parts.append(ch)
            continue
        if cp in REPLACE_CP:
            repl = REPLACE_CP[cp]
            repl_counts[cp] += 1
            out_parts.append(repl)
        else:
            unknown_counts[cp] += 1
    return "".join(out_parts), repl_counts, unknown_counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="docs", help="Root directory to scan (default: docs)")
    ap.add_argument("--extra", nargs="*", default=[], help="Extra files to scan (e.g., README.md AGENTS.md)")
    ap.add_argument("--write", action="store_true", help="Write changes back to files")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    roots = [repo_root / args.root] + [repo_root / p for p in args.extra]

    files: List[Path] = []
    for r in roots:
        if r.exists():
            files.extend(iter_text_files(r))
    files = sorted(set(files), key=lambda p: p.as_posix())

    total_hits = 0
    hit_files = 0
    changed_files: List[str] = []
    repl_total = Counter()
    unknown_total = Counter()

    for fp in files:
        try:
            raw = fp.read_text(encoding="utf-8")
        except Exception:
            continue
        sanitized, repl_counts, unknown_counts = sanitize_text(raw)
        hits = sum(repl_counts.values()) + sum(unknown_counts.values())
        if hits == 0:
            continue
        total_hits += hits
        hit_files += 1
        repl_total.update(repl_counts)
        unknown_total.update(unknown_counts)
        if args.write and sanitized != raw:
            fp.write_text(sanitized, encoding="utf-8")
            changed_files.append(fp.relative_to(repo_root).as_posix())

    date = dt.date.today().strftime("%Y-%m-%d")
    out_dir = repo_root / "logs" / "ci" / date
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "emoji-sanitize.json"

    report = {
        "scanned_files": len(files),
        "hit_files": hit_files,
        "total_hits": total_hits,
        "write": bool(args.write),
        "changed_files": changed_files,
        "replacements_by_cp": [{"cp": cp, "hex": hex(cp), "count": n} for cp, n in repl_total.most_common()],
        "unknown_by_cp": [{"cp": cp, "hex": hex(cp), "count": n} for cp, n in unknown_total.most_common()],
    }

    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(
        "EMOJI_SANITIZE "
        f"scanned={report['scanned_files']} hit_files={report['hit_files']} "
        f"total_hits={report['total_hits']} write={report['write']} out={out_path}"
    )
    if unknown_total:
        print("EMOJI_SANITIZE unknown codepoints detected; update mapping if needed.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
