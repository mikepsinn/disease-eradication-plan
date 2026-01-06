#!/bin/bash
# PostToolUse hook: Auto-regenerate variables after parameters.py changes
# Reads file path from stdin JSON (tool_input.file_path)

# Read JSON from stdin and extract file_path
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Only regenerate if parameters.py changed
if [[ ! "$FILE_PATH" =~ parameters\.py$ ]]; then
    exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

echo "[Auto-Regenerate] Parameters changed, regenerating variables..." >&2

# Determine Python command
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
