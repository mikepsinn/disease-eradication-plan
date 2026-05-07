# Reduces Windows build I/O contention without weakening Defender.
# Disables Windows Search service (zero security cost) and prints OneDrive
# folder-exclusion instructions (no clean CLI; must be done via GUI).
# Self-elevates via UAC.

$ErrorActionPreference = 'Continue'

# Self-elevate if not already running as admin.
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
  Write-Host "Not elevated. Requesting UAC..." -ForegroundColor Yellow
  Write-Host "Press Alt+Y on the UAC prompt to approve." -ForegroundColor Yellow
  $pwsh = (Get-Process -Id $PID).Path
  $scriptPath = $MyInvocation.MyCommand.Path
  try {
    Start-Process -FilePath $pwsh -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"`"$scriptPath`"") -Verb RunAs -ErrorAction Stop
  } catch {
    Write-Host "UAC denied or failed: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
  }
  exit
}

Write-Host "=== Stopping and disabling Windows Search service ===" -ForegroundColor Cyan
try {
  $svc = Get-Service -Name WSearch -ErrorAction Stop
  if ($svc.Status -eq 'Running') {
    Stop-Service -Name WSearch -Force -ErrorAction Stop
    Write-Host "  [OK] WSearch stopped"
  } else {
    Write-Host "  [OK] WSearch already stopped"
  }
  Set-Service -Name WSearch -StartupType Disabled -ErrorAction Stop
  Write-Host "  [OK] WSearch startup set to Disabled"
  Write-Host ""
  Write-Host "  To re-enable later, run elevated:"
  Write-Host "    Set-Service WSearch -StartupType Automatic; Start-Service WSearch"
} catch {
  Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Verification ===" -ForegroundColor Cyan
$svc = Get-Service WSearch -ErrorAction SilentlyContinue
if ($svc) {
  Write-Host "  WSearch status:    $($svc.Status)"
  Write-Host "  WSearch startup:   $($svc.StartType)"
}

Write-Host ""
Write-Host "=== OneDrive: manual step required ===" -ForegroundColor Cyan
Write-Host "OneDrive has no clean CLI to exclude folders. Do this via GUI:"
Write-Host ""
Write-Host "  1. Click the OneDrive cloud icon in the system tray"
Write-Host "  2. Settings (gear icon) -> Sync and backup -> Advanced settings"
Write-Host "  3. 'Choose folders' button"
Write-Host "  4. Uncheck (in your project's folder tree):"
Write-Host "       _build_temp"
Write-Host "       _site"
Write-Host "       node_modules"
Write-Host "       .cache"
Write-Host "       logs"
Write-Host "  5. Click OK"
Write-Host ""
Write-Host "  Note: this only matters if your project is inside a OneDrive-synced"
Write-Host "  folder. If your project lives outside OneDrive (e.g. a plain E:\\code\\"
Write-Host "  path with no sync), there is nothing to exclude."
Write-Host ""

Write-Host "Done. You can close this window." -ForegroundColor Green
Write-Host "Press Enter to exit..."
Read-Host
