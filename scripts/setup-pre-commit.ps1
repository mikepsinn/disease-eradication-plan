#!/usr/bin/env pwsh
# Setup pre-commit hooks for Python static analysis
# Run this after installing dev dependencies

Write-Host "Setting up pre-commit hooks..." -ForegroundColor Cyan

# Check if pre-commit is installed
if (-not (Get-Command pre-commit -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: pre-commit is not installed." -ForegroundColor Red
    Write-Host "Install it with: pip install pre-commit" -ForegroundColor Yellow
    Write-Host "Or install all dev dependencies: pip install -e .[dev]" -ForegroundColor Yellow
    exit 1
}

# Install pre-commit hooks
Write-Host "Installing pre-commit hooks..." -ForegroundColor Cyan
pre-commit install

Write-Host ""
Write-Host "Pre-commit hooks installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "The following tools will run on every commit:" -ForegroundColor Cyan
Write-Host "  - ruff: Fast Python linter and formatter" -ForegroundColor White
Write-Host "  - mypy: Static type checker" -ForegroundColor White
Write-Host "  - pylint: Comprehensive linter with duplicate detection" -ForegroundColor White
Write-Host "  - vulture: Find unused code" -ForegroundColor White
Write-Host ""
Write-Host "To run manually on all files:" -ForegroundColor Yellow
Write-Host "  pre-commit run --all-files" -ForegroundColor White
Write-Host ""
Write-Host "To run on staged files only:" -ForegroundColor Yellow
Write-Host "  pre-commit run" -ForegroundColor White
Write-Host ""
Write-Host "To skip hooks for a commit:" -ForegroundColor Yellow
Write-Host "  git commit --no-verify" -ForegroundColor White

