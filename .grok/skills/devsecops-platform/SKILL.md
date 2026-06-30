# DevSecOps Platform
Unified security pipeline aggregating:
- CodeQL (SAST)
- Secret scanning (gitleaks/trufflehog)
- SEOM (static analysis)
- CVE monitoring (Dependabot, OSV)
- License audit (FOSSA / scan)
- Dependency review (renovate/dependabot)
- Container scanning (Trivy, Grype)
Output: monthly scorecard + prioritized remediation
