#!/usr/bin/env python3
"""doc-scanner: Check required docs and report gaps."""
import pathlib, sys

REQUIRED = ["README.md","SECURITY.md","CHANGELOG.md","CONTRIBUTING.md","CODEOWNERS.md","STATE.md"]
root = pathlib.Path(".")
missing = [f for f in REQUIRED if not (root / f).exists()]
if missing:
    print(f"Missing: {missing}")
    sys.exit(1)
print("Docs OK")
