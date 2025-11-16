param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$QuartoArgs
)

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

$econConfig = "_quarto-economics.yml"
if (-not (Test-Path $econConfig)) {
    Write-Error "Missing $econConfig. Unable to preview economics website."
    exit 1
}

Copy-Item $econConfig "_quarto.yml" -Force

Write-Host "Previewing economics site (_quarto.yml <- $econConfig)..." -ForegroundColor Cyan
quarto preview @QuartoArgs
# Kill all running Quarto processes
Write-Host "Stopping any running Quarto processes..." -ForegroundColor Yellow
$quartoProcesses = Get-Process -Name "quarto" -ErrorAction SilentlyContinue
if ($quartoProcesses) {
    $quartoProcesses | Stop-Process -Force
    Write-Host "Stopped $($quartoProcesses.Count) Quarto process(es)" -ForegroundColor Green
} else {
    Write-Host "No Quarto processes found" -ForegroundColor Gray
}

# Kill any processes using the default Quarto preview port (4200)
$port = 4200
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Stopping process $($process.Name) (PID: $($process.Id)) using port $port" -ForegroundColor Yellow
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    }
}

# Wait a moment for processes to fully terminate
Start-Sleep -Seconds 1

# Preview the economics website from the parent directory
Write-Host "`nStarting economics website preview..." -ForegroundColor Cyan
quarto preview economics-site

