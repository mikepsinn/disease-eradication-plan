#!/bin/bash
# Docker HTML Build Script
# Builds the book HTML in a Docker container and extracts the output

set -e

echo "======================================================================="
echo "Docker HTML Build Script"
echo "======================================================================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed or not in PATH"
    echo ""
    echo "Please install Docker:"
    echo "  - Linux: https://docs.docker.com/engine/install/"
    echo "  - macOS: https://docs.docker.com/desktop/install/mac-install/"
    echo "  - Windows: https://docs.docker.com/desktop/install/windows-install/"
    echo ""
    exit 1
fi

echo "[*] Docker found: $(docker --version)"
echo ""

# Build the Docker image
echo "[*] Building Docker image (this may take 5-10 minutes on first run)..."
echo "    Subsequent builds will be faster due to layer caching."
echo ""

docker build -f Dockerfile.html-build -t dih-book-html:latest .

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Docker build failed"
    exit 1
fi

echo ""
echo "[OK] Docker image built successfully!"
echo ""

# Create a temporary container to extract the files
echo "[*] Extracting HTML output from container..."

# Create output directory if it doesn't exist
mkdir -p _book/warondisease

# Run a container from the image and copy the output
CONTAINER_ID=$(docker create dih-book-html:latest)

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to create container from image"
    exit 1
fi

echo "    Container ID: $CONTAINER_ID"

# Copy the HTML output
docker cp "$CONTAINER_ID:/workspace/_book/warondisease" _book/ 2>/dev/null || \
    echo "[WARNING] No HTML output found in container"

# Check if we got any files
if [ -d "_book/warondisease" ] && [ "$(ls -A _book/warondisease 2>/dev/null)" ]; then
    echo "[OK] HTML output extracted to _book/warondisease/"
    echo ""
    echo "Files extracted:"
    ls -lh _book/warondisease/ | head -20
else
    echo "[WARNING] No files were extracted. The build may have failed."
    echo ""
    echo "To debug, run:"
    echo "  docker run -it dih-book-html:latest /bin/bash"
fi

# Clean up the temporary container
docker rm "$CONTAINER_ID" > /dev/null

echo ""
echo "======================================================================="
echo "Build Complete!"
echo "======================================================================="
echo ""
echo "To view the generated HTML:"
echo "  1. Open _book/warondisease/index.html in your browser"
echo "  2. Or run: python -m http.server 8000 --directory _book/warondisease"
echo ""
echo "To clean up Docker images:"
echo "  docker rmi dih-book-html:latest"
echo ""
