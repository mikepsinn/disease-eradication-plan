#!/bin/bash
# Run render-book-website.py in Docker container with volumes
# This approach mounts the local directory instead of copying files

set -e

echo "========================================"
echo "Docker Website Build (Volume Mount)"
echo "========================================"
echo ""

# Pull the official Quarto image
echo "Pulling Quarto Docker image..."
docker pull ghcr.io/quarto-dev/quarto:latest

# Create output directory
mkdir -p _book/warondisease

echo ""
echo "Running render-book-website.py in Docker container..."
echo ""

# Run the container with volume mounts
# Mount the current directory to /workspace in the container
docker run --rm \
    -v "$(pwd):/workspace" \
    -w /workspace \
    ghcr.io/quarto-dev/quarto:latest \
    bash -c "
        apt-get update -qq && \
        apt-get install -y python3 python3-pip python3-venv graphviz -qq && \
        pip3 install --no-cache-dir -r requirements.txt && \
        python3 -m ipykernel install --user --name dih-project-kernel --display-name 'DIH Project' && \
        python3 scripts/render-book-website.py --output-dir _book/warondisease
    "

EXIT_CODE=$?

echo ""
echo "========================================"
echo "Build Summary"
echo "========================================"
echo "Exit Code: $EXIT_CODE"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ SUCCESS: Website build completed!"
    echo ""
    if [ -f "_book/warondisease/index.html" ]; then
        echo "Website index found:"
        echo "  - index.html"
        
        # Count HTML files
        HTML_COUNT=$(find _book/warondisease -name "*.html" 2>/dev/null | wc -l)
        echo "  - Total HTML files: $HTML_COUNT"
    else
        echo "⚠ WARNING: index.html not found in _book/warondisease/"
    fi
    exit 0
else
    echo "✗ FAILED: Docker build exited with code $EXIT_CODE"
    echo "Check docker logs for details"
    exit $EXIT_CODE
fi

