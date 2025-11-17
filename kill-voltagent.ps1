#!/usr/bin/env pwsh
# Kill all VoltAgent server instances

Write-Host "`nSearching for VoltAgent processes...`n" -ForegroundColor Cyan

# Get all listening ports in the VoltAgent range
$killList = @()
$ports = @(3141) + (4300..4350)

foreach ($p in $ports) {
    $listening = netstat -ano | Select-String ":$p\s.*LISTENING"
    if ($listening) {
        foreach ($line in $listening) {
            if ($line -match '\s+(\d+)\s*$') {
                $killList += $Matches[1]
            }
        }
    }
}

$killList = $killList | Select-Object -Unique

if ($killList.Count -eq 0) {
    Write-Host "[OK] No VoltAgent processes found.`n" -ForegroundColor Green
    exit 0
}

Write-Host "Found $($killList.Count) process(es) to kill:`n" -ForegroundColor Yellow

foreach ($procId in $killList) {
    $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "  PID $procId - $($proc.ProcessName)" -ForegroundColor White
    } else {
        Write-Host "  PID $procId - (process info unavailable)" -ForegroundColor Gray
    }
}

Write-Host "`nKilling processes...`n" -ForegroundColor Red

$killed = 0
foreach ($procId in $killList) {
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    if ($LASTEXITCODE -eq 0 -or $?) {
        Write-Host "  [KILLED] PID $procId" -ForegroundColor Green
        $killed++
    } else {
        Write-Host "  [FAILED] PID $procId" -ForegroundColor Red
    }
}

Write-Host "`nKilled $killed process(es)" -ForegroundColor Cyan

Start-Sleep -Milliseconds 500
$check = netstat -ano | Select-String ":3141\s.*LISTENING"
if ($check) {
    Write-Host "[WARNING] Port 3141 still in use!`n" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Port 3141 is now free!`n" -ForegroundColor Green
}
