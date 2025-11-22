# Disease Eradication Plan - Makefile
# Simplifies common development tasks

.PHONY: help setup install validate render clean

# Default target - show help
help:
	@echo "Disease Eradication Plan - Available Commands:"
	@echo ""
	@echo "  make setup      - Complete setup (create venv, install all dependencies)"
	@echo "  make install    - Install dependencies only (assumes venv exists)"
	@echo "  make validate   - Run pre-render validation checks"
	@echo "  make render     - Render book to HTML"
	@echo "  make outline    - Generate outline from all headings in chapter files"
	@echo "  make clean      - Remove generated files (_book, .quarto)"
	@echo ""

# Detect OS for venv activation
ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = .venv\Scripts\activate
	PYTHON = .venv\Scripts\python.exe
	RM = rmdir /s /q
else
	VENV_ACTIVATE = . .venv/bin/activate
	PYTHON = .venv/bin/python
	RM = rm -rf
endif

# Complete setup - create venv and install everything
setup:
	@echo "Creating Python virtual environment..."
	python -m venv .venv
	@echo ""
	@echo "Installing Python dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo ""
	@echo "Installing Node.js dependencies..."
	npm install
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "  - Run 'make validate' to check your changes"
	@echo "  - Run 'make render' to build the book"

# Install dependencies (assumes venv already exists)
install:
	@echo "Installing Python dependencies..."
	$(PYTHON) -m pip install -r requirements.txt
	@echo ""
	@echo "Installing Node.js dependencies..."
	npm install
	@echo ""
	@echo "Dependencies installed!"

# Run validation checks
validate:
	@echo "Running pre-render validation..."
	$(PYTHON) scripts/pre-render-validation.py

# Render the book to HTML
render:
	@echo "Rendering book..."
	quarto render

# Generate outline from headings
outline:
	@echo "Generating outline from chapter headings..."
	$(PYTHON) scripts/generate-outline.py --output OUTLINE-GENERATED.MD

# Clean generated files
clean:
	@echo "Cleaning generated files..."
ifeq ($(OS),Windows_NT)
	if exist _book $(RM) _book
	if exist .quarto $(RM) .quarto
else
	$(RM) _book .quarto
endif
	@echo "Clean complete!"
