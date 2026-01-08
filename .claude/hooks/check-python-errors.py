#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostToolUse hook: Check Python files for syntax errors
Reads file path from stdin JSON (tool_input.file_path)
"""
import json
import sys
import os
import py_compile

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

try:
    input_data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

file_path = input_data.get('tool_input', {}).get('file_path', '')

# Only check Python files
if not file_path.endswith('.py'):
    sys.exit(0)

# Resolve path relative to project dir if needed
project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
if not os.path.isabs(file_path):
    file_path = os.path.join(project_dir, file_path)

# Make sure file exists
if not os.path.exists(file_path):
    sys.exit(0)

# Get relative path for display
try:
    display_path = os.path.relpath(file_path, project_dir)
except ValueError:
    display_path = file_path

print(f"[Python Linter] Checking {display_path}...", file=sys.stderr)

try:
    py_compile.compile(file_path, doraise=True)
    print("[OK] Python syntax valid", file=sys.stderr)
    sys.exit(0)
except py_compile.PyCompileError as e:
    print(f"[ERROR] Syntax error in {display_path}", file=sys.stderr)
    print(str(e), file=sys.stderr)
    sys.exit(2)
except Exception as e:
    print(f"[ERROR] Failed to check {display_path}: {e}", file=sys.stderr)
    sys.exit(2)
