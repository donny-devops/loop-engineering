#!/usr/bin/env pwsh
Write-Host "[hermes doctor] Checking Hermes installation..."
$paths = @(
  "$env:USERPROFILE\AppData\Local\hermes\config.yaml",
  "$env:USERPROFILE\AppData\Local\hermes\skills",
  "$env:USERPROFILE\AppData\Local\hermes\profiles"
)
$ok = 0; $fail = 0
foreach ($p in $paths) {
  if (Test-Path $p) { Write-Host "  OK: $p"; $ok++ } else { Write-Host "  MISSING: $p"; $fail++ }
}
Write-Host "`nStatus: $ok ok, $fail missing"
if ($fail -gt 0) { exit 2 } else { exit 0 }
