#!/bin/bash
# SessionStart hook: Load project context on startup
# Shows todo status, git status, and file structure

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

echo "=== Disease Eradication Plan Book Context ===" >&2

# Check if todo.md exists
if [[ -f "todo.md" ]]; then
    echo "" >&2
    echo "[TODO Status]" >&2
    # Show first 10 lines of todo (cross-platform)
    if command -v head >/dev/null 2>&1; then
        head -n 10 todo.md 2>/dev/null | while IFS= read -r line; do echo "  $line"; done >&2
    else
        # Windows fallback: use PowerShell
        powershell -Command "Get-Content todo.md -Head 10 | ForEach-Object { Write-Host \"  $_\" }" 2>/dev/null >&2
    fi
    echo "  ..." >&2
fi

# Show git status
echo "" >&2
echo "[Git Status]" >&2
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    echo "  Branch: $BRANCH" >&2
    UNCOMMITTED=$(git status --porcelain 2>/dev/null | grep -c '^' || echo "0")
    echo "  Uncommitted changes: $UNCOMMITTED files" >&2
    echo "  Recent commits:" >&2
    git log --oneline -3 2>/dev/null | while IFS= read -r line; do echo "    $line"; done >&2
else
    echo "  Not a git repository" >&2
fi

# Check if _variables.yml is up-to-date (skip on Windows due to stat incompatibility)
echo "" >&2
echo "[Variables Status]" >&2
if [[ -f "_variables.yml" && -f "dih_models/parameters.py" ]]; then
    # Cross-platform check: just verify files exist
    # On Windows, stat command is incompatible - skip timestamp comparison
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OS" == "Windows_NT" ]]; then
        echo "  Files present (timestamp check skipped on Windows)" >&2
        echo "  Tip: Run regenerate script if parameters.py was modified" >&2
    else
        # Unix/macOS: proper timestamp check
        VARS_TIME=$(stat -c %Y "_variables.yml" 2>/dev/null || stat -f %m "_variables.yml" 2>/dev/null || echo "0")
        PARAMS_TIME=$(stat -c %Y "dih_models/parameters.py" 2>/dev/null || stat -f %m "dih_models/parameters.py" 2>/dev/null || echo "0")

        if [ "$VARS_TIME" -lt "$PARAMS_TIME" ]; then
            echo "  WARNING: _variables.yml is older than parameters.py" >&2
            echo "  Run: python scripts/generate-everything-parameters-variables-calculations-references.py" >&2
        else
            echo "  Variables up-to-date" >&2
        fi
    fi
else
    echo "  _variables.yml or parameters.py not found" >&2
fi

# Show file counts (cross-platform)
echo "" >&2
echo "[Book Structure]" >&2
if [[ -d "knowledge" ]]; then
    # Use git ls-files if in git repo (works everywhere)
    if git rev-parse --git-dir > /dev/null 2>&1; then
        QMD_COUNT=$(git ls-files "knowledge/*.qmd" 2>/dev/null | grep -c '^' || echo "0")
    elif command -v find >/dev/null 2>&1; then
        # Unix find
        QMD_COUNT=$(find knowledge -name "*.qmd" 2>/dev/null | grep -c '^' || echo "0")
    else
        # Windows fallback: PowerShell
        QMD_COUNT=$(powershell -Command "(Get-ChildItem -Path knowledge -Filter *.qmd -Recurse -File).Count" 2>/dev/null || echo "0")
    fi
    echo "  QMD files: $QMD_COUNT" >&2
fi
echo "  Book config: _quarto.yml" >&2

echo "============================================" >&2
echo "" >&2

exit 0
