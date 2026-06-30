#!/usr/bin/env python3
"""secret-scanner: Fast path scanner for tracked files."""
import pathlib, re, sys

PATTERNS = [
    re.compile(r"(password|passwd|pwd|secret|token|api_key|apikey|private_key|BEGIN RSA|BEGIN OPENSSH)"),
]

def scan_file(p):
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        return
    hits = [pat.pattern for pat in PATTERNS if pat.search(text)]
    if hits:
        print(f"{p}: {hits}")

def main():
    root = pathlib.Path(".")
    for f in root.rglob("*"):
        if f.is_file() and ".git" not in str(f) and "node_modules" not in str(f):
            scan_file(f)

if __name__ == "__main__":
    main()
