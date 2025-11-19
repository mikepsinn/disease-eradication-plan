# Quarto Installation Guide

## Current Issue

The render script `python scripts/render-book-website.py` requires Quarto CLI to be installed, but it's not currently available in this environment.

## Installation Options

### Option 1: Linux (Ubuntu/Debian)

Download and install the latest Quarto release:

```bash
# Download Quarto (latest version: 1.8.26 as of Nov 2024)
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.8.26/quarto-1.8.26-linux-amd64.tar.gz

# Extract to a local directory
mkdir -p ~/opt
tar -xzf quarto-1.8.26-linux-amd64.tar.gz -C ~/opt

# Add to PATH
echo 'export PATH="$HOME/opt/quarto-1.8.26/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
quarto --version
```

### Option 2: Using Package Manager (if available)

```bash
# For Ubuntu with sudo access
sudo apt-get install quarto

# Or using snap
snap install quarto
```

### Option 3: Docker

If you have Docker, you can use the official Quarto Docker image:

```bash
docker run --rm -v $(pwd):/workspace ghcr.io/quarto-dev/quarto:latest render /workspace
```

## Setup Complete Environment

Once Quarto is installed, complete the setup:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install the dih_models package
pip install -e .

# 3. Install Jupyter kernel
python -m ipykernel install --user --name dih-project-kernel --display-name "DIH Project"

# 4. Install Graphviz (for diagrams)
sudo apt-get install graphviz

# 5. Run the render script
python scripts/render-book-website.py
```

## Option 4: Docker (Recommended for Consistency)

**Best option if you want a reproducible environment without installing dependencies locally.**

### Quick Start with Docker

```bash
# Build and extract HTML (automated script)
bash scripts/docker-build-html.sh

# Or use docker-compose
docker-compose -f docker-compose.html-build.yml build

# Extract the built HTML
docker create --name dih-html-temp dih-book-html:latest
docker cp dih-html-temp:/workspace/_book/warondisease _book/
docker rm dih-html-temp
```

### Manual Docker Commands

```bash
# Build the Docker image
docker build -f Dockerfile.html-build -t dih-book-html:latest .

# Run the container (HTML will be built automatically)
docker run --name dih-html-build dih-book-html:latest

# Copy the output
docker cp dih-html-build:/workspace/_book/warondisease _book/
docker rm dih-html-build

# View the HTML
open _book/warondisease/index.html  # macOS
# Or: python -m http.server 8000 --directory _book/warondisease
```

### Available Docker Files

- `Dockerfile.html-build` - HTML website rendering
- `Dockerfile.pdf-build` - PDF book rendering (with LaTeX)
- `docker-compose.html-build.yml` - Compose file for HTML
- `docker-compose.pdf-build.yml` - Compose file for PDF

## Option 5: GitHub Actions (Zero Local Setup)

The project is configured to automatically build on GitHub Actions when you push to the main/master branch. The workflow handles all dependencies including Quarto installation.

See `.github/workflows/publish.yml` for the complete CI/CD setup.

## Verifying Setup

After installation, verify everything is working:

```bash
# Check Quarto version
quarto --version

# Check Python environment
python --version
pip list | grep -E "(pandas|numpy|matplotlib|jupyter)"

# Check if dih_models is installed
python -c "import dih_models; print('dih_models package installed successfully')"

# Run a test render
quarto render --help
```

## Troubleshooting

**Issue:** `Command 'quarto' not found in PATH`
- **Solution:** Ensure Quarto is installed and added to your PATH environment variable

**Issue:** Network restrictions (403 Forbidden)
- **Solution:** Try downloading Quarto on a different network, or use a VPN, or install via package manager

**Issue:** Missing Python dependencies
- **Solution:** Run `pip install -r requirements.txt` and `pip install -e .`
