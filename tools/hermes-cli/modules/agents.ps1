#!/usr/bin/env pwsh
Write-Host "[hermes agents] Listing agents..."
if (Test-Path "\.grok\agents") { Get-ChildItem .\.grok\agents | Select-Object Name }
if (Test-Path "\.grok\subagents") { Write-Host "`nSubagents:"; Get-ChildItem .\.grok\subagents | Select-Object Name }
