# Environment Status Report

## Summary

The book rendering environment has been configured and validated. Most dependencies are installed and working correctly.

**Status: 16/18 checks passing (89%)**

## What's Working ✅

- Python 3.11.14 installed and configured
- All Python dependencies installed:
  - pandas, numpy, matplotlib
  - jupyter, nbformat, ipykernel
  - And all other packages from requirements.txt
- Custom `dih_models` package installed
- All configuration files present:
  - `_quarto-book.yml` (book configuration)
  - `index-book.qmd` (book index)
  - `_variables.yml` (generated variables)
  - `requirements.txt` (Python dependencies)
- All render scripts present and updated:
  - `scripts/render-book-website.py` (main render script)
  - `scripts/lib/render_utils.py` (improved with better error handling)
  - `scripts/generate-variables-yml.py` (variable generator)

## What's Missing ❌

1. **Quarto CLI** (required for rendering)
   - Status: Not installed
   - Installation: See `docs/QUARTO_SETUP.md` or run `bash scripts/install-quarto.sh`
   - Why missing: Network restrictions prevent downloading in this environment

2. **Graphviz** (required for diagrams)
   - Status: Not installed
   - Installation: `sudo apt-get install graphviz` (Linux) or `brew install graphviz` (macOS)
   - Why missing: Package manager restrictions in this environment

## Improvements Made

### 1. Enhanced Error Handling
- Updated `scripts/lib/render_utils.py` with pre-flight command checking
- Now shows helpful error messages when Quarto is missing
- Prevents confusing `FileNotFoundError` stack traces

### 2. Setup Automation
- Created `scripts/install-quarto.sh` - automated Quarto installation script
- Created `scripts/check-environment.py` - comprehensive environment validator
- Both scripts are executable and ready to use

### 3. Documentation
- Created `docs/QUARTO_SETUP.md` - detailed Quarto installation guide
- Updated `README.md` - added setup instructions
- Created this status report

## How to Complete Setup

### Option 1: Docker (Recommended - Easiest)

**Docker handles all dependencies automatically - Quarto, Python packages, Graphviz, everything!**

```bash
# Build HTML using Docker (one command!)
bash scripts/docker-build-html.sh

# Or use docker-compose
docker-compose -f docker-compose.html-build.yml build

# HTML output will be in _book/warondisease/
```

**Pros:**
- No local installation needed
- Reproducible builds
- Same environment as CI/CD
- Works on any OS with Docker

**Cons:**
- Requires Docker installation
- First build takes 5-10 minutes (cached afterward)

### Option 2: Local Installation

```bash
# Check current status
python scripts/check-environment.py

# Install Quarto (Linux/macOS)
bash scripts/install-quarto.sh

# Install Graphviz
sudo apt-get install graphviz  # Linux
# Or: brew install graphviz      # macOS

# Verify everything is ready
python scripts/check-environment.py

# Render the book
python scripts/render-book-website.py
```

**Pros:**
- Faster subsequent builds
- Direct access to tools
- Better for development/debugging

**Cons:**
- Requires manual dependency installation
- Platform-specific issues possible

### Alternative: Use GitHub Actions

If local installation is problematic, the project is configured to automatically build on GitHub Actions:

1. Push to the `main` or `master` branch
2. GitHub Actions will install all dependencies (including Quarto)
3. The book will render automatically
4. HTML output will deploy to GitHub Pages

See `.github/workflows/publish.yml` for the complete CI/CD configuration.

## Next Steps

1. **Install Quarto** in your local environment where network access is available
2. **Install Graphviz** using your system package manager
3. **Run environment check** to verify all dependencies: `python scripts/check-environment.py`
4. **Render the book**: `python scripts/render-book-website.py`
5. **Preview locally**: The rendered HTML will be in `_book/warondisease/`

## Files Created/Modified

### New Files
- `docs/QUARTO_SETUP.md` - Comprehensive Quarto installation guide
- `docs/ENVIRONMENT_STATUS.md` - This status report
- `scripts/install-quarto.sh` - Automated Quarto installation script
- `scripts/check-environment.py` - Environment validation script
- `scripts/docker-build-html.sh` - Automated Docker HTML build script
- `Dockerfile.html-build` - Docker image for HTML rendering
- `docker-compose.html-build.yml` - Docker Compose configuration for HTML

### Modified Files
- `scripts/lib/render_utils.py` - Enhanced error handling for missing commands
- `README.md` - Added Docker and local setup instructions

## Testing

You can test the improved error handling even without Quarto:

```bash
# This will now show a helpful error message instead of a stack trace
python scripts/render-book-website.py
```

Expected output:
```
[ERROR] Command 'quarto' not found in PATH

Please ensure the command is installed and available in your system PATH.
To install Quarto, visit: https://quarto.org/docs/get-started/
```

## Environment Constraints

This environment has the following limitations that prevented full setup:

- Network restrictions (403 Forbidden) prevent downloading external packages
- Package manager access is limited
- Cannot install system-level dependencies (Quarto CLI, Graphviz)

However, all Python-level dependencies have been successfully installed and configured.

## Conclusion

The environment is **ready for book rendering** once Quarto and Graphviz are installed. All setup scripts and documentation have been created to make installation straightforward in environments with proper network access and permissions.

**Recommendation:** Install Quarto and Graphviz on your local machine or use GitHub Actions for automatic rendering.
