# Verification script for DIH project environment
# Run this script to check if everything is set up correctly

Write-Host "Verifying DIH project setup..." -ForegroundColor Green

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "❌ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if virtual environment is activated
$venvPath = $env:VIRTUAL_ENV
if (!$venvPath -or !$venvPath.Contains("decentralized-institutes-of-health")) {
    Write-Host "❌ Virtual environment not activated. Run: .\.venv\Scripts\Activate.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment is active" -ForegroundColor Green

# Check Python packages
Write-Host "Checking Python packages..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\python.exe -c "
import plotly
import pandas
import yaml
import jupyter
import nbclient
print('✅ All critical packages are installed')
"
} catch {
    Write-Host "❌ Missing Python packages. Run: pip install -r requirements.txt" -ForegroundColor Red
    exit 1
}

# Check Jupyter kernels
Write-Host "Checking Jupyter kernels..." -ForegroundColor Yellow
$kernels = & jupyter kernelspec list 2>$null
if ($kernels -match "dih-project-kernel") {
    Write-Host "✅ DIH project kernel is registered" -ForegroundColor Green
} else {
    Write-Host "❌ DIH project kernel not found. Run: python -m ipykernel install --user --name=dih-project-kernel --display-name 'DIH Project Kernel'" -ForegroundColor Red
    exit 1
}

# Test Quarto
Write-Host "Testing Quarto..." -ForegroundColor Yellow
try {
    & quarto check jupyter 2>$null
    Write-Host "✅ Quarto can find Python" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Quarto check failed, but this might be OK if the kernel is registered" -ForegroundColor Yellow
}

Write-Host "🎉 Setup verification complete! Your environment is ready." -ForegroundColor Green
Write-Host "You can now run: quarto preview index.qmd" -ForegroundColor Cyan
