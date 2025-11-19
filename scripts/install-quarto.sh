#!/bin/bash
# Quarto Installation Script for Linux
# This script downloads and installs Quarto CLI to ~/opt/quarto

set -e

QUARTO_VERSION="1.8.26"
INSTALL_DIR="$HOME/opt"
QUARTO_URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"

echo "===================================================================="
echo "Quarto Installation Script"
echo "===================================================================="
echo ""
echo "This script will:"
echo "  1. Download Quarto ${QUARTO_VERSION} for Linux"
echo "  2. Extract to ${INSTALL_DIR}/quarto-${QUARTO_VERSION}"
echo "  3. Add Quarto to your PATH"
echo ""

# Create install directory
mkdir -p "${INSTALL_DIR}"
cd "${INSTALL_DIR}"

# Download Quarto
echo "[*] Downloading Quarto ${QUARTO_VERSION}..."
if command -v wget &> /dev/null; then
    wget -q --show-progress "${QUARTO_URL}" -O "quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"
elif command -v curl &> /dev/null; then
    curl -L "${QUARTO_URL}" -o "quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"
else
    echo "[ERROR] Neither wget nor curl is available. Please install one of them."
    exit 1
fi

# Extract archive
echo "[*] Extracting Quarto..."
tar -xzf "quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"

# Clean up tarball
rm "quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"

# Add to PATH
QUARTO_BIN="${INSTALL_DIR}/quarto-${QUARTO_VERSION}/bin"
echo ""
echo "[*] Installation complete!"
echo ""
echo "To use Quarto, add it to your PATH:"
echo ""
echo "    export PATH=\"${QUARTO_BIN}:\$PATH\""
echo ""
echo "To make this permanent, add the above line to your ~/.bashrc or ~/.zshrc:"
echo ""
echo "    echo 'export PATH=\"${QUARTO_BIN}:\$PATH\"' >> ~/.bashrc"
echo "    source ~/.bashrc"
echo ""

# Test if quarto works
if "${QUARTO_BIN}/quarto" --version &> /dev/null; then
    echo "[OK] Quarto installed successfully!"
    echo ""
    "${QUARTO_BIN}/quarto" --version
else
    echo "[WARNING] Installation completed but quarto command test failed."
    echo "          Please check the installation manually."
fi

echo ""
echo "===================================================================="
echo "Next steps:"
echo "===================================================================="
echo "1. Add Quarto to PATH (see instructions above)"
echo "2. Install Python dependencies: pip install -r requirements.txt"
echo "3. Install dih_models package: pip install -e ."
echo "4. Install Jupyter kernel: python -m ipykernel install --user --name dih-project-kernel --display-name 'DIH Project'"
echo "5. Run the render script: python scripts/render-book-website.py"
echo ""
