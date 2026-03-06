#!/usr/bin/env python3
"""Validate InfoSec Bharat events YAML.

Supports input from:
- a file path (events.yaml)
- a raw YAML string (from GitHub issue form)

Exit codes:
 0 = valid
 2 = invalid
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception as e:
    print("ERROR: Missing dependency PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    raise


RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED_FIELDS = [
    "name",
    "description",
    "start_date",
    "end_date",
    "location",
    "city",
    "category",
    "event_type",
    "website_url",
    "organizer_name",
    "organizer_email",
]

ALLOWED_CATEGORY = {"Conference", "Meetup"}
ALLOWED_EVENT_TYPE = {"offline", "online", "hybrid"}

OPTIONAL_FIELDS = {
    "event_socials",
    "is_paid",
    "price_min",
    "price_max",
    "cfp_deadline",
    "tags",
}


def _parse_date(s: str) -> dt.date | None:
    if not isinstance(s, str) or not RE_DATE.match(s):
        return None
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def _is_blank(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    return False


def validate_events_doc(doc: Dict[str, Any]) -> Tuple[List[str], List[Dict[str, Any]]]:
    errors: List[str] = []
    events_out: List[Dict[str, Any]] = []

    if not isinstance(doc, dict):
        return (["Top-level YAML must be a mapping/object."], [])

    events = doc.get("events")
    if not isinstance(events, list):
        return (["YAML must contain an `events:` list."], [])
    # Allow empty `events: []` in the canonical repo file.
    if len(events) == 0:
        return ([], [])

    for i, ev in enumerate(events):
        path = f"events[{i}]"
        if not isinstance(ev, dict):
            errors.append(f"{path} must be a mapping/object.")
            continue

        # Unknown keys check (soft)
        unknown = set(ev.keys()) - (set(REQUIRED_FIELDS) | OPTIONAL_FIELDS)
        if unknown:
            errors.append(f"{path} has unknown field(s): {', '.join(sorted(unknown))}")

        # Required
        for k in REQUIRED_FIELDS:
            if k not in ev or _is_blank(ev.get(k)):
                errors.append(f"{path}.{k} is required")

        # Dates
        sd = _parse_date(ev.get("start_date"))
        ed = _parse_date(ev.get("end_date"))
        if sd is None:
            errors.append(f"{path}.start_date must be YYYY-MM-DD")
        if ed is None:
            errors.append(f"{path}.end_date must be YYYY-MM-DD")
        if sd and ed and ed < sd:
            errors.append(f"{path}.end_date must be on/after start_date")

        # Enums
        cat = ev.get("category")
        if isinstance(cat, str) and cat not in ALLOWED_CATEGORY:
            errors.append(f"{path}.category must be one of: {', '.join(sorted(ALLOWED_CATEGORY))}")
        et = ev.get("event_type")
        if isinstance(et, str) and et not in ALLOWED_EVENT_TYPE:
            errors.append(f"{path}.event_type must be one of: {', '.join(sorted(ALLOWED_EVENT_TYPE))}")

        # Payment logic
        if "is_paid" in ev and isinstance(ev.get("is_paid"), bool):
            is_paid = ev["is_paid"]
            if not is_paid:
                # If free, price_* should not be present
                if "price_min" in ev or "price_max" in ev:
                    errors.append(f"{path}: remove price_min/price_max when is_paid is false")
        # If price fields present, must be ints and consistent
        if "price_min" in ev:
            if not isinstance(ev.get("price_min"), int):
                errors.append(f"{path}.price_min must be an integer (INR)")
        if "price_max" in ev:
            if not isinstance(ev.get("price_max"), int):
                errors.append(f"{path}.price_max must be an integer (INR)")
        if isinstance(ev.get("price_min"), int) and isinstance(ev.get("price_max"), int):
            if ev["price_max"] < ev["price_min"]:
                errors.append(f"{path}.price_max must be >= price_min")

        # CFP date
        if "cfp_deadline" in ev:
            if _parse_date(ev.get("cfp_deadline")) is None:
                errors.append(f"{path}.cfp_deadline must be YYYY-MM-DD")

        # Tags
        if "tags" in ev:
            tags = ev.get("tags")
            if not isinstance(tags, list) or any(not isinstance(t, str) or t.strip() == "" for t in tags):
                errors.append(f"{path}.tags must be a list of non-empty strings")

        events_out.append(ev)

    return (errors, events_out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="Path to YAML file containing events:")
    ap.add_argument("--string", help="Raw YAML string")
    ap.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = ap.parse_args()

    if not args.file and not args.string:
        print("ERROR: Provide --file or --string", file=sys.stderr)
        return 2

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                raw = f.read()
        else:
            raw = args.string or ""

        doc = yaml.safe_load(raw)
    except Exception as e:
        print(f"YAML parse error: {e}")
        return 2

    errors, events = validate_events_doc(doc if doc is not None else {})

    if args.json:
        import json

        print(json.dumps({"valid": len(errors) == 0, "errors": errors, "eventCount": len(events)}, indent=2))
    else:
        if errors:
            print("INVALID")
            for e in errors:
                print(f"- {e}")
        else:
            print(f"VALID ({len(events)} event(s))")

    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
