---
title: Technical Contribution Guide
description: "Technical standards, development environment setup, and engineering best practices for the DIH project."
tags: [technical-guide, contributing, development, setup, standards]
---

# Technical Contribution Guide

**See also:**

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Overall contribution workflow and standards
- [STYLE_GUIDE.md](./STYLE_GUIDE.md) - Writing style and tone
- [DESIGN_GUIDE.md](./DESIGN_GUIDE.md) - Visual design standards

---

## Development Environment Setup

### Quick Start (Automated)

1. **Run the setup script**: `.\setup.ps1`
2. **Activate the environment**: `.\venv\Scripts\Activate.ps1`
3. **Verify setup**: `.\verify-setup.ps1`
4. **Preview the book**: `quarto preview index.qmd`

### Prerequisites

- Python 3.8+
- Quarto
- PowerShell (Windows)

### Manual Setup

If the automated setup doesn't work:

1. Create virtual environment: `python -m venv .venv`
2. Activate it: `.\venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Register Jupyter kernel: `python -m ipykernel install --user --name=dih-project-kernel --display-name "DIH Project Kernel"`

### Troubleshooting

- **"ModuleNotFoundError"**: Run `.\verify-setup.ps1` to check your environment
- **"Kernel not found"**: Re-run the Jupyter kernel registration step
- **Quarto errors**: Make sure your virtual environment is activated

## Technical Standards

- **Code:** Write new tools in TypeScript
- **Dependencies:** Use `npm` and include a `package.json`
- **Execution:** Run TypeScript directly with `tsx`. No compiled `.js` files in the repo.
- **Automated Formatting:** All `.qmd` files are subject to automated formatting checks based on the rules defined in [`FORMATTING_GUIDE.md`](../FORMATTING_GUIDE.md).
