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

# Create logs directory if it doesn't exist
$logsDir = "logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Create timestamped log file in logs folder
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logFile = Join-Path $logsDir "act-economics-test-$timestamp.log"
Write-Host "Saving full output to: $logFile" -ForegroundColor Cyan
Write-Host ""

# Run the workflow with ACT (add timestamps to each line and tee to log file)
act workflow_dispatch `
    -W .github/workflows/test-economics-pdf.yml `
    -j test-economics `
    --artifact-server-path ./act-artifacts `
    --verbose 2>&1 | ForEach-Object {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "[$timestamp] $_"
    } | Tee-Object -FilePath $logFile

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "BUILD COMPLETE" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Full build log saved to: $logFile" -ForegroundColor Cyan
Write-Host ""

# Check for PDF in artifacts
# ACT creates numbered subdirectories for each run (1, 2, 3, etc.)
# Find the most recent run directory
$runDirs = Get-ChildItem -Path act-artifacts -Directory -ErrorAction SilentlyContinue | 
    Where-Object { $_.Name -match '^\d+$' } | 
    Sort-Object { [int]$_.Name } -Descending

if ($runDirs) {
    $latestRun = $runDirs[0].Name
    $pdfPath = "act-artifacts/$latestRun/economics-site-test/dih-economic-models.pdf"
    
    if (Test-Path $pdfPath) {
        Write-Host "✅ PDF generated successfully!" -ForegroundColor Green
        Write-Host "   Location: $pdfPath" -ForegroundColor Green
        $pdfFile = Get-Item $pdfPath
        Write-Host "   Size: $([math]::Round($pdfFile.Length / 1MB, 2)) MB" -ForegroundColor Green
        Write-Host "   Modified: $($pdfFile.LastWriteTime)" -ForegroundColor Green
        Write-Host ""
        Write-Host "✅ All validation checks passed!" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "❌ PDF not found at: $pdfPath" -ForegroundColor Red
    }
} else {
    Write-Host "❌ No ACT run directories found in act-artifacts/" -ForegroundColor Red
}

Write-Host ""
Write-Host "Checking for PDFs in artifacts..." -ForegroundColor Yellow
$foundPdfs = Get-ChildItem -Path act-artifacts -Filter *.pdf -Recurse -ErrorAction SilentlyContinue
if ($foundPdfs) {
    Write-Host "Found PDF(s):" -ForegroundColor Yellow
    $foundPdfs | ForEach-Object {
        Write-Host "  - $($_.FullName)" -ForegroundColor Yellow
        Write-Host "    Size: $([math]::Round($_.Length / 1MB, 2)) MB" -ForegroundColor Yellow
    }
} else {
    Write-Host "No PDF files found in artifacts directory." -ForegroundColor Red
}
exit 1
