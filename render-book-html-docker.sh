#!/bin/bash
# Render the book website using Docker
# This ensures a consistent build environment across all platforms

set -e  # Exit on error

echo "================================================================================"
echo "Building Docker image for HTML rendering..."
echo "================================================================================"
docker compose -f docker-compose.html-build.yml build

echo ""
echo "================================================================================"
echo "Running HTML rendering in Docker..."
echo "================================================================================"
docker compose -f docker-compose.html-build.yml up

echo ""
echo "================================================================================"
echo "HTML rendering complete!"
echo "Output location: _book/warondisease/"
echo "================================================================================"
