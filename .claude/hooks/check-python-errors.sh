#!/bin/bash
# PostToolUse hook: Check Python files for errors using pyright
# Runs after Edit/Write operations on Python files

FILE_PATH="${CLAUDE_HOOK_FILE_PATH:-}"

# Only check Python files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
    exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

echo "[Python Linter] Checking $FILE_PATH..." >&2

# Use pyright for static type checking (if available)
if command -v pyright &> /dev/null; then
    pyright "$FILE_PATH" 2>&1 | head -n 20
    PYRIGHT_EXIT=$?
    if [ $PYRIGHT_EXIT -ne 0 ]; then
        echo "[ERROR] Pyright found issues in $FILE_PATH" >&2
    fi
fi

# Always run py_compile for syntax check
if [[ -f ".venv/Scripts/python.exe" ]]; then
    PYTHON_CMD=".venv/Scripts/python.exe"
elif [[ -f ".venv/bin/python" ]]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python"
fi

"$PYTHON_CMD" -m py_compile "$FILE_PATH" 2>&1
COMPILE_EXIT=$?

if [ $COMPILE_EXIT -ne 0 ]; then
    echo "[ERROR] Syntax error in $FILE_PATH" >&2
    exit 2
else
    echo "[OK] Python syntax valid" >&2
    exit 0
fi
