# Pre-commit Hooks Setup

This project uses pre-commit hooks to automatically run static analysis tools on Python code before commits.

## Tools Included

### 1. **Ruff** (Fast Linter & Formatter)
- **Replaces:** flake8, black, isort
- **What it does:**
  - Lints Python code for errors and style issues
  - Formats code automatically
  - Sorts imports
- **Why:** 10-100x faster than traditional tools

### 2. **MyPy** (Static Type Checker)
- **What it does:**
  - Checks for type errors
  - Validates type hints
  - Catches bugs before runtime
- **Configuration:** Ignores missing imports (for third-party libs)

### 3. **Pylint** (Comprehensive Linter)
- **What it does:**
  - **Detects duplicate code** (similarity analysis)
  - Comprehensive code quality checks
  - Complexity analysis
- **Why:** Catches issues that other tools miss, especially duplicate functions

### 4. **Vulture** (Unused Code Detection)
- **What it does:**
  - Finds unused functions, classes, variables
  - Helps keep codebase clean
- **Confidence threshold:** 80% (reduces false positives)

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
- `scripts/**/*.py` - All Python scripts
- `dih_models/**/*.py` - All model code

### What's Ignored
- Generated files
- Third-party code
- Jupyter notebooks (`.ipynb` files)

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

## Duplicate Code Detection

Pylint's duplicate detection works by:
1. Comparing function/method similarity
2. Flagging code blocks with >5 similar lines
3. Reporting similarity percentage

**Example output:**
```
scripts/script1.py:45: Similar lines in 2 files
scripts/script2.py:30: Similar lines in 2 files
```

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

