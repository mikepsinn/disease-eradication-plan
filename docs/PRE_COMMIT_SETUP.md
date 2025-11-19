# Pre-commit Hooks Setup

This project uses pre-commit hooks to automatically run static analysis tools on Python code before commits.

## Tools Included

**Minimal, practical setup** - Just Ruff. That's it.

### **Ruff** (Fast Linter & Formatter)
- **Replaces:** flake8, black, isort, mypy (for basic checks)
- **What it does:**
  - Catches syntax errors and bugs
  - Finds unused imports and variables
  - Formats code automatically
  - Sorts imports
  - Basic type checking (if you use type hints)
- **Why:** Fast, catches real issues, not pedantic, all-in-one

## Setup Instructions

### 1. Install Dev Dependencies

```powershell
# Activate your virtual environment first
.\venv\Scripts\Activate.ps1

# Install dev dependencies (includes pre-commit and all tools)
pip install -e .[dev]
```

### 2. Install Pre-commit Hooks

```powershell
# Run the setup script
.\scripts\setup-pre-commit.ps1

# Or manually:
pre-commit install
```

### 3. Verify Installation

```powershell
# Test on all files (first run may take a while)
pre-commit run --all-files
```

## Usage

### Automatic (Recommended)
Hooks run automatically on `git commit`. If issues are found:
- **Auto-fixable issues:** Fixed automatically, you'll need to stage and commit again
- **Non-fixable issues:** Commit is blocked until fixed

### Manual Runs

```powershell
# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Run a specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
pre-commit run pylint --all-files
```

### Skip Hooks (Emergency Only)

```powershell
git commit --no-verify
```

**Warning:** Only skip if absolutely necessary. Hooks catch real bugs!

## What Gets Checked

### Files Scanned
- All `.py` files in the repo

### What's Ignored
- Generated files (via `.gitignore`)
- Third-party code

## Common Issues & Solutions

### Issue: "pre-commit: command not found"
**Solution:** Install dev dependencies: `pip install -e .[dev]`

### Issue: "mypy: No module named 'types-all'"
**Solution:** The hook installs this automatically, but if it fails:
```powershell
pip install types-all
```

### Issue: Too many false positives from pylint
**Solution:** Adjust settings in `pyproject.toml` under `[tool.pylint.*]`

### Issue: Ruff formatting conflicts with existing code
**Solution:** Run `ruff format .` to format everything, then commit

## Configuration

All tool configurations are in `pyproject.toml`:

- `[tool.ruff]` - Ruff settings
- `[tool.mypy]` - MyPy type checking settings
- `[tool.pylint.*]` - Pylint settings

Hook configuration is in `.pre-commit-config.yaml`.

## What We Don't Include (And Why)

- **MyPy** - Installation issues, slow, only useful if you use type hints everywhere
- **Pylint** - Too strict, too many false positives, slows down commits
- **Vulture** - Too many false positives (unused code detection is tricky)
- **Complex duplicate detection** - Can be added later if needed, but usually not worth the noise

**Philosophy:** One tool (Ruff) that does everything well. Fast, practical, catches real bugs.

## Type Error Detection

MyPy catches:
- Type mismatches
- Missing type hints (optional, but recommended)
- Incorrect function signatures
- Import errors

**Example:**
```python
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", "world")  # MyPy error: Expected int, got str
```

## Updating Hooks

Hooks are pinned to specific versions. To update:

```powershell
pre-commit autoupdate
```

Then review changes in `.pre-commit-config.yaml` before committing.

## CI Integration

These same checks run in CI (GitHub Actions) to ensure code quality across all contributors.

