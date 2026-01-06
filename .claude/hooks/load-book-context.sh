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
    # Show first 10 lines of todo
    head -n 10 todo.md | sed 's/^/  /' >&2
    echo "  ..." >&2
fi

# Show git status
echo "" >&2
echo "[Git Status]" >&2
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  Branch: $(git branch --show-current)" >&2
    UNCOMMITTED=$(git status --porcelain | wc -l)
    echo "  Uncommitted changes: $UNCOMMITTED files" >&2
    echo "  Recent commits:" >&2
    git log --oneline -3 | sed 's/^/    /' >&2
else
    echo "  Not a git repository" >&2
fi

# Check if _variables.yml is up-to-date
echo "" >&2
echo "[Variables Status]" >&2
if [[ -f "_variables.yml" && -f "dih_models/parameters.py" ]]; then
    VARS_TIME=$(stat -c %Y "_variables.yml" 2>/dev/null || stat -f %m "_variables.yml" 2>/dev/null || echo "0")
    PARAMS_TIME=$(stat -c %Y "dih_models/parameters.py" 2>/dev/null || stat -f %m "dih_models/parameters.py" 2>/dev/null || echo "0")

    if [ "$VARS_TIME" -lt "$PARAMS_TIME" ]; then
        echo "  WARNING: _variables.yml is older than parameters.py" >&2
        echo "  Run: .venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py" >&2
    else
        echo "  Variables up-to-date" >&2
    fi
else
    echo "  _variables.yml or parameters.py not found" >&2
fi

# Show file counts
echo "" >&2
echo "[Book Structure]" >&2
QMD_COUNT=$(find knowledge -name "*.qmd" 2>/dev/null | wc -l)
echo "  QMD files: $QMD_COUNT" >&2
echo "  Book config: _quarto.yml" >&2

echo "============================================" >&2
echo "" >&2

exit 0
