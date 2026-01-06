#!/bin/bash
# PostToolUse hook: Check Python files for errors
# Reads file path from stdin JSON (tool_input.file_path)

# Read JSON from stdin and extract file_path
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Only check Python files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
    exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

echo "[Python Linter] Checking $FILE_PATH..." >&2

# Determine Python command
if [[ -f ".venv/Scripts/python.exe" ]]; then
    PYTHON_CMD=".venv/Scripts/python.exe"
elif [[ -f ".venv/bin/python" ]]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python"
fi

# Run py_compile for syntax check
"$PYTHON_CMD" -m py_compile "$FILE_PATH" 2>&1
COMPILE_EXIT=$?

if [ $COMPILE_EXIT -ne 0 ]; then
    echo "[ERROR] Syntax error in $FILE_PATH" >&2
    exit 2
else
    echo "[OK] Python syntax valid" >&2
    exit 0
fi
