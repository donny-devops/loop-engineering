#!/usr/bin/env python3
"""issue-labeler: Auto-label issues based on content."""
import sys, pathlib, re

LABELS = {
    "bug": re.compile(r"bug|error|fail|crash", re.I),
    "enhancement": re.compile(r"enhance|improve|feature", re.I),
    "security": re.compile(r"security|vuln|secret|leak", re.I),
    "docs": re.compile(r"doc|readme|guide", re.I),
}

def main():
    if len(sys.argv) < 2:
        print("Usage: issue_labeler.py <title> [body]")
        sys.exit(1)
    title = sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else ""
    matches = [lbl for lbl, pat in LABELS.items() if pat.search(title + " " + body)]
    print(" ".join(matches) if matches else "triage")

if __name__ == "__main__":
    main()
