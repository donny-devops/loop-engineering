#!/usr/bin/env python3
"""changelog-bot: Auto-draft CHANGELOG entries from recent commits."""
import subprocess, pathlib, re, sys

def get_commits(n=20):
    out = subprocess.check_output(["git", "log", f"-n", str(n), "--pretty=format:%h %s"] , text=True)
    return out.splitlines()

def categorize(c):
    if c.startswith("fix") or c.startswith("Fix"): return "Fixed"
    if c.startswith("feat"): return "Added"
    if c.startswith("chore"): return "Changed"
    if c.startswith("security"): return "Security"
    return "Changed"

def main():
    commits = get_commits()
    sections = {}
    for c in commits:
        msg = c.split(" ", 1)[-1]
        cat = categorize(msg)
        sections.setdefault(cat, []).append(msg)
    out = pathlib.Path("CHANGELOG.draft.md")
    out.write_text("\n".join(f"## {cat}\n" + "\n".join(f"- {m}" for m in ms)) for cat, ms in sections.items())
    print("Draft written to CHANGELOG.draft.md")

if __name__ == "__main__":
    main()
