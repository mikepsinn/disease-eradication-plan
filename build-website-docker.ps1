#!/usr/bin/env pwsh
# Build website using Docker (faster than act since dependencies are pre-installed)

param(
    [switch]$BuildImage,
    [switch]$SkipValidation
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Website Build" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($BuildImage -or -not (docker images -q website-build:latest 2>$null)) {
    Write-Host "Building Docker image (this may take a few minutes the first time)..." -ForegroundColor Yellow
    docker build -f Dockerfile.website-build -t website-build:latest .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "Using existing Docker image" -ForegroundColor Green
}

Write-Host ""
Write-Host "Building Docker image and running website build..." -ForegroundColor Cyan
Write-Host "This copies all files into the container (avoids filesystem issues)" -ForegroundColor Gray
Write-Host ""

$startTime = Get-Date

# Build and run - Website is built during Docker build
docker compose -f docker-compose.website-build.yml build --no-cache website-build

$buildExitCode = $LASTEXITCODE

if ($buildExitCode -eq 0) {
    Write-Host ""
    Write-Host "Extracting HTML website from container..." -ForegroundColor Cyan
    
    # Create a temporary container to extract the HTML
    $containerId = docker create website-build:latest 2>&1
    if ($LASTEXITCODE -eq 0) {
        # Extract HTML to local _book directory
        New-Item -ItemType Directory -Force -Path "_book\warondisease" | Out-Null
        docker cp "${containerId}:/workspace/_book/warondisease" "_book\" 2>&1 | Out-Null
        docker rm $containerId | Out-Null
        
        Write-Host "✓ HTML website extracted successfully" -ForegroundColor Green
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
    Write-Host "✓ SUCCESS: Website build completed!" -ForegroundColor Green
    Write-Host ""
    if (Test-Path "_book\warondisease\index.html") {
        Write-Host "Website index found:" -ForegroundColor Green
        Write-Host "  - index.html" -ForegroundColor Gray
        
        # Count HTML files
        $htmlFiles = Get-ChildItem "_book\warondisease\*.html" -Recurse
        Write-Host "  - Total HTML files: $($htmlFiles.Count)" -ForegroundColor Gray
    } else {
        Write-Host "⚠ WARNING: index.html not found in _book/warondisease/" -ForegroundColor Yellow
    }
    exit 0
} else {
    Write-Host "✗ FAILED: Docker build exited with code $buildExitCode" -ForegroundColor Red
    Write-Host "Check docker build logs for details" -ForegroundColor Yellow
    exit $buildExitCode
}

