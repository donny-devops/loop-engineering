#!/usr/bin/env pwsh
param(
  [Parameter(Position=0)][string]$Command,
  [Parameter(ValueFromRemainingArguments=$true)][string[]]$Args
)
$ErrorActionPreference='SilentlyContinue'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$modulesDir = Join-Path $scriptDir 'modules'
$cmdFile = Join-Path $modulesDir "$Command.ps1"
if (-not (Test-Path $cmdFile)) {
  Write-Host "Unknown command: $Command"
  Write-Host "Available: doctor, audit, deploy, optimize, security, agents, workflow"
  exit 1
}
& $cmdFile @Args
