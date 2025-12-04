# PowerShell script to launch Chrome with remote debugging enabled
# This allows Puppeteer to connect to your existing browser session

# Find Chrome executable
$chromePath = "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"

if (-not (Test-Path $chromePath)) {
    Write-Host "Chrome not found at: $chromePath" -ForegroundColor Red
    Write-Host "Please update the path in this script or install Chrome." -ForegroundColor Yellow
    exit 1
}

Write-Host "Launching Chrome with remote debugging on port 9222..." -ForegroundColor Green
Write-Host "You can now log in to NotebookLM, then run the download script with --use-existing flag" -ForegroundColor Cyan
Write-Host ""

# Launch Chrome with remote debugging
Start-Process $chromePath -ArgumentList "--remote-debugging-port=9222"

Write-Host "Chrome launched! Now you can:" -ForegroundColor Yellow
Write-Host "  1. Log in to NotebookLM in the Chrome window" -ForegroundColor White
Write-Host "  2. Run: tsx scripts/download-notebooklm-files.ts <url> --use-existing" -ForegroundColor White

