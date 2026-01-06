#!/bin/bash
# PostToolUse hook: Auto-regenerate variables after parameters.py changes
# Runs after Edit/Write operations on parameters.py

FILE_PATH="${CLAUDE_HOOK_FILE_PATH:-}"

# Only regenerate if parameters.py changed
if [[ ! "$FILE_PATH" =~ parameters\.py$ ]]; then
    exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

echo "[Auto-Regenerate] Parameters changed, regenerating variables..." >&2

# Run the generation script
if [[ -f ".venv/Scripts/python.exe" ]]; then
    PYTHON_CMD=".venv/Scripts/python.exe"
elif [[ -f ".venv/bin/python" ]]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python"
fi

"$PYTHON_CMD" scripts/generate-everything-parameters-variables-calculations-references.py 2>&1

if [ $? -eq 0 ]; then
    echo "[OK] Variables regenerated successfully" >&2
    exit 0
else
    echo "[ERROR] Variable regeneration failed - check parameters.py syntax" >&2
    exit 2
fi
