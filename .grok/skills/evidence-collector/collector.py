"""Evidence collector for compliance audits."""
import json, pathlib, datetime

def collect(repo_root="."):
    root = pathlib.Path(repo_root)
    evidence = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "repo": str(root),
        "files": {
            "security_md": (root / "SECURITY.md").exists(),
            "codeowners": (root / "CODEOWNERS.md").exists(),
            "dependabot": (root / ".github/dependabot.yml").exists(),
            "workflows": len(list((root / ".github/workflows").glob("*.yml"))) if (root / ".github/workflows").exists() else 0,
        },
        "ci_runs": [],
    }
    pathlib.Path("compliance-evidence.json").write_text(json.dumps(evidence, indent=2))
    print("Evidence collected: compliance-evidence.json")

if __name__ == "__main__":
    collect()
