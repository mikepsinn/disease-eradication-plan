# Test economics PDF build locally using ACT
# Prerequisites: Docker must be running, ACT must be installed
# Install ACT: choco install act-cli  (or see https://github.com/nektos/act)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "LOCAL ECONOMICS PDF BUILD TEST" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info 2>&1 | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if ACT is installed
if (!(Get-Command act -ErrorAction SilentlyContinue)) {
    Write-Host "❌ ERROR: ACT is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Install ACT:" -ForegroundColor Yellow
    Write-Host "  - Windows: choco install act-cli" -ForegroundColor Yellow
    Write-Host "  - Or download from: https://github.com/nektos/act/releases" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ ACT is installed" -ForegroundColor Green
Write-Host ""

# Navigate to project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $scriptDir "..")

Write-Host "Running economics build test with ACT..." -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: This will:" -ForegroundColor Yellow
Write-Host "  1. Pull Docker image (first time only, ~2GB)" -ForegroundColor Yellow
Write-Host "  2. Install Python dependencies in container" -ForegroundColor Yellow
Write-Host "  3. Render economics site (HTML + PDF)" -ForegroundColor Yellow
Write-Host "  4. Upload artifacts (viewable in ./act-artifacts/)" -ForegroundColor Yellow
Write-Host "  5. Skip Netlify deployment (no secrets in local test)" -ForegroundColor Yellow
Write-Host ""
Write-Host "This may take 15-30 minutes on first run..." -ForegroundColor Yellow
Write-Host ""

# Run the workflow with ACT
act workflow_dispatch `
    -W .github/workflows/test-economics-pdf.yml `
    -j test-economics `
    --artifact-server-path ./act-artifacts `
    --verbose

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "BUILD COMPLETE" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check for PDF in artifacts
$pdfPath = "act-artifacts/economics-site-test/dih-economic-models.pdf"
if (Test-Path $pdfPath) {
    Write-Host "✅ PDF generated successfully!" -ForegroundColor Green
    Write-Host "   Location: $pdfPath" -ForegroundColor Green
    Get-Item $pdfPath | Select-Object Name, Length, LastWriteTime | Format-List
} else {
    Write-Host "❌ PDF not found in expected location" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checking for PDFs in artifacts..." -ForegroundColor Yellow
    Get-ChildItem -Path act-artifacts -Filter *.pdf -Recurse -ErrorAction SilentlyContinue | Format-Table Name, Directory
    exit 1
}
