#!/bin/bash
# Build website using Docker (faster than act since dependencies are pre-installed)

set -e

BUILD_IMAGE=false
SKIP_VALIDATION=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --build-image)
            BUILD_IMAGE=true
            shift
            ;;
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--build-image] [--skip-validation]"
            exit 1
            ;;
    esac
done

echo "========================================"
echo "Docker Website Build"
echo "========================================"
echo ""

if $BUILD_IMAGE || ! docker images -q website-build:latest > /dev/null 2>&1; then
    echo "Building Docker image (this may take a few minutes the first time)..."
    docker build -f Dockerfile.website-build -t website-build:latest .
    if [ $? -ne 0 ]; then
        echo "ERROR: Docker build failed"
        exit 1
    fi
    echo "✓ Docker image built successfully"
else
    echo "Using existing Docker image"
fi

echo ""
echo "Building Docker image and running website build..."
echo "This copies all files into the container (avoids filesystem issues)"
echo ""

START_TIME=$(date +%s)

# Build and run - Website is built during Docker build
docker compose -f docker-compose.website-build.yml build --no-cache website-build

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "Extracting HTML website from container..."
    
    # Create a temporary container to extract the HTML
    CONTAINER_ID=$(docker create website-build:latest 2>&1)
    if [ $? -eq 0 ]; then
        # Extract HTML to local _book directory
        mkdir -p _book/warondisease
        docker cp "${CONTAINER_ID}:/workspace/_book/warondisease" "_book/" 2>&1 > /dev/null
        docker rm "$CONTAINER_ID" > /dev/null
        
        echo "✓ HTML website extracted successfully"
    fi
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_MINUTES=$(echo "scale=2; $DURATION / 60" | bc)

echo ""
echo "========================================"
echo "Build Summary"
echo "========================================"
echo "Duration: ${DURATION_MINUTES} minutes"
echo "Exit Code: $BUILD_EXIT_CODE"
echo ""

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "✓ SUCCESS: Website build completed!"
    echo ""
    if [ -f "_book/warondisease/index.html" ]; then
        echo "Website index found:"
        echo "  - index.html"
        
        # Count HTML files
        HTML_COUNT=$(find _book/warondisease -name "*.html" | wc -l)
        echo "  - Total HTML files: $HTML_COUNT"
    else
        echo "⚠ WARNING: index.html not found in _book/warondisease/"
    fi
    exit 0
else
    echo "✗ FAILED: Docker build exited with code $BUILD_EXIT_CODE"
    echo "Check docker build logs for details"
    exit $BUILD_EXIT_CODE
fi

