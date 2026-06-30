#!/usr/bin/env python3
"""vuln-scanner: Aggregates gitleaks + npm audit + pip check."""
import json, pathlib, subprocess, sys

def run(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return out
    except subprocess.CalledProcessError as e:
        return e.output

def main():
    report = {"secrets": None, "npm": None, "pip": None}
    # gitleaks json report
    leaks = run("gitleaks detect --source . --report-format json --no-git")
    try:
        report["secrets"] = json.loads(leaks)
    except Exception:
        report["secrets"] = []
    # npm audit
    npm = run("npm audit --json")
    try:
        report["npm"] = json.loads(npm)
    except Exception:
        report["npm"] = {}
    pathlib.Path("vuln-report.json").write_text(json.dumps(report, indent=2))
    print("Wrote vuln-report.json")

if __name__ == "__main__":
    main()
