"""Generate compliance report from evidence."""
import json, pathlib

def generate():
    p = pathlib.Path("compliance-evidence.json")
    if not p.exists():
        print("No evidence found. Run collector first.")
        return
    data = json.loads(p.read_text())
    score = sum(1 for v in data["files"].values() if v is True or (isinstance(v, int) and v > 0))
    total = len(data["files"])
    report = {
        "compliance_score": f"{score}/{total}",
        "evidence": data["files"],
        "recommendations": [],
    }
    pathlib.Path("compliance-report.json").write_text(__import__('json').dumps(report, indent=2))
    print("Compliance report: compliance-report.json")

if __name__ == "__main__":
    generate()
