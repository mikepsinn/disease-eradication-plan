#!/usr/bin/env pwsh
# Build PDF using Docker (faster than act since dependencies are pre-installed)

param(
    [switch]$BuildImage,
    [switch]$SkipValidation
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker PDF Build" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($BuildImage -or -not (docker images -q pdf-build:latest 2>$null)) {
    Write-Host "Building Docker image (this may take a few minutes the first time)..." -ForegroundColor Yellow
    docker build -f Dockerfile.pdf-build -t pdf-build:latest .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "Using existing Docker image" -ForegroundColor Green
}

Write-Host ""
Write-Host "Building Docker image and running PDF build..." -ForegroundColor Cyan
Write-Host "This copies all files into the container (avoids filesystem issues)" -ForegroundColor Gray
Write-Host ""

$startTime = Get-Date

# Build and run - PDF is built during Docker build
docker-compose -f docker-compose.pdf-build.yml build --no-cache pdf-build

$buildExitCode = $LASTEXITCODE

if ($buildExitCode -eq 0) {
    Write-Host ""
    Write-Host "Extracting PDF from container..." -ForegroundColor Cyan
    
    # Create a temporary container to extract the PDF
    $containerId = docker create pdf-build:latest 2>&1
    if ($LASTEXITCODE -eq 0) {
        # Extract PDF to local _book directory
        New-Item -ItemType Directory -Force -Path "_book\warondisease" | Out-Null
        docker cp "${containerId}:/workspace/_book/warondisease" "_book\" 2>&1 | Out-Null
        docker rm $containerId | Out-Null
        
        Write-Host "✓ PDF extracted successfully" -ForegroundColor Green
    }
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Duration: $($duration.TotalMinutes.ToString('F2')) minutes" -ForegroundColor Cyan
Write-Host "Exit Code: $buildExitCode" -ForegroundColor $(if ($buildExitCode -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($buildExitCode -eq 0) {
    Write-Host "✓ SUCCESS: PDF build completed!" -ForegroundColor Green
    Write-Host ""
    if (Test-Path "_book\warondisease\*.pdf") {
        $pdfFiles = Get-ChildItem "_book\warondisease\*.pdf"
        Write-Host "PDF files found:" -ForegroundColor Green
        $pdfFiles | ForEach-Object { Write-Host "  - $($_.Name) ($([math]::Round($_.Length/1MB, 2)) MB)" -ForegroundColor Gray }
    } else {
        Write-Host "⚠ WARNING: PDF files not found in _book/warondisease/" -ForegroundColor Yellow
    }
    exit 0
} else {
    Write-Host "✗ FAILED: Docker build exited with code $buildExitCode" -ForegroundColor Red
    Write-Host "Check docker build logs for details" -ForegroundColor Yellow
    exit $buildExitCode
}

