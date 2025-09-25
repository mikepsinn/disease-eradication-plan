# Setup script for Decentralized Institutes of Health project
# This script creates a virtual environment and installs all dependencies

Write-Host "Setting up DIH project environment..." -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Verify critical packages are installed
Write-Host "Verifying package installation..." -ForegroundColor Yellow
python -c "import plotly, pandas, yaml; print('All critical packages installed successfully')"

# Register Jupyter kernel for Quarto
Write-Host "Registering Jupyter kernel..." -ForegroundColor Yellow
python -m ipykernel install --user --name=dih-project-kernel --display-name "DIH Project Kernel"

Write-Host "Setup complete! You can now run 'quarto preview' to start the book." -ForegroundColor Green
Write-Host "Make sure to activate the virtual environment first: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
