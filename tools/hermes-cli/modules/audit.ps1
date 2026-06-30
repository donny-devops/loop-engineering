#!/usr/bin/env pwsh
param([string]$Path=".")
Write-Host "[hermes audit] Scanning $Path"
if (Test-Path "$Path\.grok\skills") { Write-Host "  Skills found" } else { Write-Host "  No skills dir" }
if (Test-Path "$Path\.github\workflows") { Write-Host "  Workflows found" } else { Write-Host "  No workflows dir" }
Write-Host "[hermes audit] Complete"
