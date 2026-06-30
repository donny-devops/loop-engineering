#!/usr/bin/env pwsh
Write-Host "[hermes workflow] Listing workflows..."
if (Test-Path ".github\workflows") { Get-ChildItem .\.github\workflows\*.yml | Select-Object Name }
