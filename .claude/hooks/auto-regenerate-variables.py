#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostToolUse hook: Auto-regenerate variables after parameters.py changes
Reads file path from stdin JSON (tool_input.file_path)
"""
import json
import sys
import os
import subprocess

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore[union-attr]

# Import hook logger
def log_hook(name: str, msg: str) -> None:
    """Fallback no-op logger"""
    pass

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from hook_logger import log_hook  # type: ignore[no-redef]
except ImportError:
    pass  # Use fallback defined above

log_hook("auto-regenerate-variables", "hook triggered")

try:
    input_data = json.load(sys.stdin)
    log_hook("auto-regenerate-variables", f"input: {input_data.get('tool_input', {}).get('file_path', 'unknown')}")
except Exception:
    log_hook("auto-regenerate-variables", "failed to parse stdin")
    sys.exit(0)

file_path = input_data.get('tool_input', {}).get('file_path', '')

# Only regenerate if parameters.py changed
if not file_path.endswith('parameters.py'):
    sys.exit(0)

# Get project directory
project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
os.chdir(project_dir)

print("[Auto-Regenerate] Parameters changed, regenerating variables...", file=sys.stderr)

# Determine Python command
if os.path.exists(os.path.join(project_dir, '.venv', 'Scripts', 'python.exe')):
    python_cmd = os.path.join(project_dir, '.venv', 'Scripts', 'python.exe')
elif os.path.exists(os.path.join(project_dir, '.venv', 'bin', 'python')):
    python_cmd = os.path.join(project_dir, '.venv', 'bin', 'python')
else:
    python_cmd = 'python'

script_path = os.path.join(project_dir, 'scripts', 'generate-everything-parameters-variables-calculations-references.py')

try:
    result = subprocess.run(
        [python_cmd, script_path],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=120
    )

    if result.returncode == 0:
        print("[OK] Variables regenerated successfully", file=sys.stderr)
        sys.exit(0)
    else:
        print("[ERROR] Variable regeneration failed - check parameters.py syntax", file=sys.stderr)
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)
        sys.exit(2)
except subprocess.TimeoutExpired:
    print("[ERROR] Variable regeneration timed out after 120 seconds", file=sys.stderr)
    sys.exit(2)
except Exception as e:
    print(f"[ERROR] Failed to run regeneration: {e}", file=sys.stderr)
    sys.exit(2)
