#!/usr/bin/env python3
"""registry-sync: Sync patterns/registry.yaml with cron schedule truth."""
import json, pathlib, yaml, sys

REGISTRY = pathlib.Path("patterns/registry.yaml")
STATE = pathlib.Path("STATE.md")

def main():
    if not REGISTRY.exists():
        print("registry.yaml missing", file=sys.stderr)
        sys.exit(1)
    data = yaml.safe_load(REGISTRY.read_text())
    # Simple checker: ensure every active entry has a schedule
    missing = [e["id"] for e in data.get("entries", []) if e.get("active") and not e.get("schedule")]
    if missing:
        print(f"Missing schedules: {missing}")
        sys.exit(1)
    print(f"Registry OK — {len(data.get('entries', []))} entries")
    sys.exit(0)

if __name__ == "__main__":
    main()
