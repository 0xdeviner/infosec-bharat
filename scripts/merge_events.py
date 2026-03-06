#!/usr/bin/env python3
"""Merge submitted events into events.yaml with dedupe + stable sort.

Dedupe key: (name.lower().strip(), start_date, city.lower().strip())
Sort key: (start_date, name)

Usage:
  merge_events.py --base events.yaml --add submission.yaml --out events.yaml
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: Missing dependency PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    raise


def _load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    if raw == "":
        return {"events": []}
    doc = yaml.safe_load(raw)
    if doc is None:
        return {"events": []}
    if not isinstance(doc, dict):
        raise ValueError(f"{path}: top-level YAML must be a mapping")
    if "events" not in doc:
        doc["events"] = []
    if not isinstance(doc["events"], list):
        raise ValueError(f"{path}: `events` must be a list")
    return doc


def _key(ev: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        str(ev.get("name", "")).strip().lower(),
        str(ev.get("start_date", "")).strip(),
        str(ev.get("city", "")).strip().lower(),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--add", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    base = _load(args.base)
    add = _load(args.add)

    base_events: List[Dict[str, Any]] = [e for e in base.get("events", []) if isinstance(e, dict)]
    add_events: List[Dict[str, Any]] = [e for e in add.get("events", []) if isinstance(e, dict)]

    seen = {_key(e) for e in base_events}
    added_count = 0
    for e in add_events:
        k = _key(e)
        if k in seen:
            continue
        seen.add(k)
        base_events.append(e)
        added_count += 1

    def sort_key(e: Dict[str, Any]):
        return (str(e.get("start_date", "9999-99-99")), str(e.get("name", "")))

    base_events.sort(key=sort_key)

    out_doc = {"events": base_events}
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(out_doc, f, sort_keys=False, allow_unicode=True)

    print(f"Merged: +{added_count} new event(s); total={len(base_events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
