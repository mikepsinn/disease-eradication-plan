# Docker HTML Build Instructions

This guide explains how to render the book website using Docker for a consistent build environment.

## Prerequisites

- Docker installed and running
- Docker Compose V2 (integrated into Docker CLI)

## Quick Start

### Option 1: Using the Shell Script (Recommended)

```bash
./render-book-html-docker.sh
```

This will:
1. Build the Docker image with all dependencies (Quarto, Python, etc.)
2. Run the HTML rendering script
3. Output the rendered website to `_book/warondisease/`

### Option 2: Manual Docker Compose Commands

```bash
# Build the Docker image
docker compose -f docker-compose.html-build.yml build

# Run the rendering
docker compose -f docker-compose.html-build.yml up

# Clean up the container when done
docker compose -f docker-compose.html-build.yml down
```

### Option 3: Using Docker CP (Avoid Permission Issues)

If you encounter permission issues with volume mounting, use this alternative approach:

```bash
# Build the image
docker compose -f docker-compose.html-build.yml build

# Run the container (without volume mount)
docker run --name html-build-temp html-build

# Copy the output from the container
docker cp html-build-temp:/workspace/_book/_book/

# Remove the temporary container
docker rm html-build-temp
```

## What's Included in the Docker Image

The Docker image (`Dockerfile.html-build`) includes:

- **Ubuntu 22.04** base system
- **Quarto** (latest version) - for rendering the book
- **Python 3.11** - for running scripts and Jupyter notebooks
- **Chromium** - for rendering diagrams and charts
- **All Python dependencies** from `requirements.txt`:
  - Data science: pandas, numpy, matplotlib, seaborn, plotly
  - Jupyter: ipykernel, jupyter, jupyterlab
  - Utilities: PyYAML, graphviz, psutil
- **Jupyter kernel** configured for the project

## Build Process

The `render-book-website.py` script performs these steps:

1. **Prepare book files**:
   - Copies `_quarto-book.yml` → `_quarto.yml`
   - Copies `index-book.qmd` → `index.qmd`

2. **Run pre-validation**:
   - Regenerates `_variables.yml` from `dih_models/parameters.py`
   - Validates all `.qmd` files for undefined variables
   - Checks for common errors

3. **Render HTML**:
   - Executes `quarto render --to html`
   - Monitors for warnings and errors
   - Times out after 300 seconds of no output

4. **Run post-validation**:
   - Checks for broken links
   - Validates generated HTML
   - Verifies all assets are present

## Output

The rendered website will be in:
```
_book/warondisease/
├── index.html              # Main landing page
├── knowledge/              # All book chapters
├── assets/                 # Images, charts, diagrams
└── [other HTML files]      # Additional pages
```

## Troubleshooting

### Docker not found
```bash
# Check if Docker is installed
docker --version

# If not, install Docker Desktop:
# https://www.docker.com/products/docker-desktop/
```

### Permission denied errors
- On Linux, you may need to run with `sudo` or add your user to the `docker` group
- Alternatively, use Option 3 (docker cp) to avoid volume permission issues

### Build takes too long
- The first build downloads and installs all dependencies (may take 10-15 minutes)
- Subsequent builds are much faster due to Docker layer caching
- If stuck, check `build-html.log` for details

### Quarto errors during rendering
- Check the console output for specific error messages
- Common issues:
  - Undefined variables (check `_variables.yml`)
  - Missing images (check file paths in `.qmd` files)
  - Python errors in notebooks (check Jupyter kernel)

### Container uses too much disk space
```bash
# Clean up old containers and images
docker system prune -a

# Remove specific build artifacts
docker compose -f docker-compose.html-build.yml down --rmi all
```

## Updating Dependencies

If you modify `requirements.txt`, rebuild the Docker image:

```bash
# Force rebuild without cache
docker compose -f docker-compose.html-build.yml build --no-cache
```

## Comparison to PDF Build

This HTML build setup is similar to `Dockerfile.pdf-build` but optimized for web rendering:

| Feature | HTML Build | PDF Build |
|---------|------------|-----------|
| Base image | Ubuntu 22.04 | Ubuntu 22.04 |
| Quarto | ✓ | ✓ |
| Python 3.11 | ✓ | ✓ |
| Chromium | ✓ | ✓ |
| TinyTeX | ✗ (not needed) | ✓ (for LaTeX) |
| Output | HTML files | PDF file |
| Volume mount | Yes (for output) | No (use docker cp) |

## CI/CD Integration

### GitHub Actions Workflow

A test workflow is included at `.github/workflows/test-docker-html-build.yml` that:

- **Automatically runs** on push to `claude/fix-docker-book-rendering-*` branches
- **Can be triggered manually** via GitHub Actions UI (workflow_dispatch)
- **Tests both approaches**:
  1. Direct Docker Compose commands
  2. The `render-book-html-docker.sh` shell script
- **Validates output**: Checks for index.html and counts rendered files
- **Uploads artifacts**: HTML output and build logs for inspection

**To monitor the workflow:**

1. Go to: https://github.com/mikepsinn/decentralized-institutes-of-health/actions
2. Look for "Test Docker HTML Build" workflow
3. Check the run triggered by the latest commit
4. Download artifacts to inspect the rendered HTML

**To run manually:**

1. Go to: https://github.com/mikepsinn/decentralized-institutes-of-health/actions/workflows/test-docker-html-build.yml
2. Click "Run workflow"
3. Select your branch
4. Click "Run workflow"

### Integration Example for Deployment

For automated builds and deployment:

```yaml
# Example GitHub Actions workflow for deployment
- name: Build book website
  run: |
    docker compose -f docker-compose.html-build.yml build
    docker compose -f docker-compose.html-build.yml up

- name: Deploy to web
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./_book/warondisease
```

## Support

For issues or questions:
- Check `build-html.log` for detailed error messages
- Review the Quarto documentation: https://quarto.org
- File an issue in the project repository
