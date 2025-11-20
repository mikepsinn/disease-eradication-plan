# Docker Website Build

This directory contains Docker configuration for building the HTML website.

## Files

- `Dockerfile.website-build` - Dockerfile for website build environment
- `docker-compose.website-build.yml` - Docker Compose orchestration  
- `build-website-docker.sh` - Linux/Mac build script
- `build-website-docker.ps1` - Windows PowerShell build script
- `run-website-docker.sh` - Alternative approach using volume mounts

## Usage

### On Linux/Mac:

```bash
# Using docker-compose (recommended)
./build-website-docker.sh

# Using volume mounts (alternative)
./run-website-docker.sh
```

### On Windows:

```powershell
# Using docker-compose
.\build-website-docker.ps1

# With specific options
.\build-website-docker.ps1 -BuildImage  # Force rebuild image
```

## Known Issues

### Network Restrictions in Build Environment

The Docker build process requires network access to:
- Download Quarto from quarto.org or GitHub
- Download Python packages from PyPI
- Install system dependencies from Ubuntu repositories

If you encounter network errors (DNS resolution failures, SSL certificate errors), you have these options:

#### Option 1: Use GitHub Actions

The repository's GitHub Actions workflows have proper network access and can build successfully. See `.github/workflows/publish.yml`.

#### Option 2: Build Locally Without Docker

If you have Quarto and Python installed locally:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Jupyter kernel
python -m ipykernel install --user --name dih-project-kernel --display-name "DIH Project"

# Run the build script
python scripts/render-book-website.py
```

#### Option 3: Use Docker with Local Network

In environments with unrestricted network access:

```bash
# Pull the base image
docker pull ghcr.io/quarto-dev/quarto:latest

# Build the website
docker compose -f docker-compose.website-build.yml build website-build

# Extract the output
CONTAINER_ID=$(docker create website-build:latest)
docker cp ${CONTAINER_ID}:/workspace/_book/warondisease _book/
docker rm $CONTAINER_ID
```

## Architecture

The Docker setup uses a multi-stage approach:

1. **Base Image**: `ghcr.io/quarto-dev/quarto:latest` - Official Quarto image with Ubuntu 22.04
2. **Dependencies**: Installs Python 3, pip, graphviz, and required Python packages
3. **Project Files**: Copies all necessary files into the container
4. **Build**: Runs `python scripts/render-book-website.py`
5. **Output**: HTML files in `_book/warondisease/` 

## Troubleshooting

### "Could not resolve host" errors

Network restrictions prevent DNS resolution. Use Option 1 or 2 above.

### "SSL certificate verify failed" errors

Self-signed certificates in the environment block PyPI access. Use Option 1 or 2 above.

### Package installation failures

If pip cannot install packages, verify:
- Python 3 is installed: `python3 --version`
- pip is functional: `pip3 --version`
- Requirements are accessible: `ls requirements.txt`

### Missing output files

If the build completes but no HTML files are generated:
- Check logs for Quarto errors
- Verify `_quarto-book.yml` and `index-book.qmd` exist
- Run validation: `python scripts/pre-render-validation.py`

## See Also

- `Dockerfile.pdf-build` - PDF build configuration (similar approach)
- `scripts/render-book-website.py` - The main build script
- `.github/workflows/publish.yml` - GitHub Actions workflow
